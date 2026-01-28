+++
draft = false
date = 2026-01-28T00:00:00Z
title = "Why Your Prompt Cache Keeps Missing"
description = "Prompt caching can cut LLM costs by 90%, but subtle serialization issues break cache reuse. This post maps the failure patterns and engineering rules for high cache hit rates."
tags = ["LLM", "Prompt Caching", "OpenAI", "MLOps", "Cost Optimization"]
categories = ["Machine Learning", "Engineering"]
authors = ["Asad Ismail"]
+++

## Why you should care

Agentic workflows resend a large, mostly static context on every call: system instructions, tool schemas, and growing conversation history. Prompt caching can make those repeated input tokens far cheaper and reduce latency. But the failure modes are subtle: small changes can shift where your prompt diverges in the cached prefix and wipe most (or all) cached reuse, raising both cost and latency.

This post maps the failure patterns we hit in practice and the rules that kept cache hit rates high.

> **Scope:** We focus here on OpenAI's prompt caching behavior as observed via `cached_tokens` in API responses. Other providers (Anthropic, Google) also cache context but with different boundary rules. For a cross-provider evaluation including latency benchmarks, see [Lumer et al., "Don't Break the Cache" (2026)](https://arxiv.org/abs/2601.06007).

---

## Quick takeaway

- Prompt caching applies to a **prefix of one serialized token stream** (system + tools + messages), not to "your system prompt" as a separate unit.
- With tools enabled, putting per-request metadata (UUID/timestamp/run-id) in the system message can collapse cached tokens even if it "worked" without tools. Late bind dynamic metadata in a later message (typically user).
- Treat tool schemas + ordering as a cache contract: keep them stable, deterministic, and append-only when evolving.


## What OpenAI docs say (and what they leave implicit)

OpenAI's [prompt caching guide](https://platform.openai.com/docs/guides/prompt-caching) and [announcement post](https://openai.com/index/api-prompt-caching/) state:

- Put **static content at the beginning**, variable content at the end
- Caching requires a **1024 token minimum**, then grows in **128-token increments**
- **Tools and images must be identical** between requests for cache reuse
- Requests are **routed by prefix hash**, so cache hits depend on landing on a machine that has your prefix cached

All accurate. But the docs assume you understand how serialization works under the hood, and that's where teams trip up. For example, when tools are present, an edit at the end of your system message can still land "early" in the serialized token stream that caching actually sees, invalidating entire cached checkpoints and collapsing reuse to zero. We'll demonstrate this with experiments below.

## The real boundary: one serialized token stream 

Prompt caching does not operate on “system prompt”, “tools schema” and "user messages" as separate objects.

Regardless of the exact internal chat template, the provider must serialize:
- Structured output schema (if using response_format)
- System prompt
- Tools schema
- User messages

into one continuous token stream.
Caching applies to a prefix of that serialized stream.

Conceptually:

![Objects to tokens](/images/objects_to_tokens.png)


So “end of system message” in your source code is not a cache boundary. It is just a location inside a longer serialized stream.

**How boundaries increment:** Based on OpenAI docs and observing `cached_tokens` in API responses, caching reuses the longest matching prefix and grows in 128-token steps after the first 1024. A small edit can knock you back multiple steps, even if total prompt length barely changes.

---

## Where this breaks: two experiments

We ran two experiments to see how small changes affect caching in practice. All numbers come from actual API responses (`prompt_tokens`, `cached_tokens`).

### Experiment 1: UUID placement

We inserted a random UUID (in the real world this could be any dynamic content like a timestamp or session ID) in three locations: beginning of system, end of system, and end of user message.

**Without tools (system + user messages only):**

| UUID location | Prompt tokens | Cached tokens | Cache % |
|---|---:|---:|---:|
| No UUID (baseline) | 1,613 | 1,536 | 95.2% |
| System start | 1,637 | 0 | 0.0% |
| System end | 1,639 | 1,536 | 93.7% |
| User end | 1,640 | 1,536 | 93.7% |

UUID at the start of system breaks caching (early divergence). Appending at the end of system appeared safe here because the cached boundary (1,536) still matched.

**With tools (system + tools list + user messages):**

| UUID location | Prompt tokens | Cached tokens | Cache % |
|---|---:|---:|---:|
| No UUID (baseline) | 1,920 | 1,792 | 93.3% |
| System start | 1,944 | 0 | 0.0% |
| System end | 1,946 | 0 | 0.0% |
| User end | 1,947 | 1,792 | 92.0% |

With tools in the request, appending to the system message collapsed cached tokens to zero. Appending to the user message preserved cache reuse.

Why? With tools present, the "end of system" edit lands earlier in the serialized stream than the cached checkpoint, so it misses the cache.

**Practical rule:** Treat run IDs/timestamps as dynamic metadata and late bind them:

```python
# Often breaks cache when tools are present
system_prompt = f"{BASE_SYSTEM}\n\nRun ID: {uuid.uuid4()}"

# Preserves stable prefix
messages = [
    {"role": "system", "content": BASE_SYSTEM},
    {"role": "user", "content": f"{query}\n\nRun ID: {uuid.uuid4()}"},
]
```

If you need per-request metadata, put it in a later message, not system. This matters most when tools are enabled.

---

### Experiment 2: Tool ordering

Using a larger prompt (12,540 tokens total: system + tools array + user messages), we added the same new tool in two positions: prepend (beginning of tools array) vs append (end of tools array).

| Tool change | Prompt tokens | Cached tokens | Cache lost |
|---|---:|---:|---:|
| Baseline | 12,540 | 12,416 | — |
| Prepend new tool | 12,690 | 9,984 | 2,432 tokens |
| Append new tool | 12,692 | 12,032 | 384 tokens |

Prepending a tool moved the divergence earlier and wiped a much larger cached prefix. Appending preserved more cache reuse.

At smaller prompt sizes, tool changes sometimes collapsed caching to zero. If the available cache checkpoint falls inside the tools region and you modify tools, that checkpoint becomes invalid.

**Practical rule:** Treat tool ordering like an API contract:

```python
# Risky: can wipe cached prefix
tools = [new_tool] + existing_tools

# Safer: append-only evolution
tools = existing_tools + [new_tool]
```

### Gating tool availability without schema churn

You often want certain tools available only in specific steps—for example, allowing "write" tools only after user confirmation. The key is to do this without changing the tools array you send to the API.

Always send the full, stable tool schema. Control availability either in your application logic (validate after the LLM responds) or via prompt instructions (tell the LLM which tools to use this step):

```python
TOOLS_V1 = [tool_a, tool_b, tool_c, tool_d]  # always send this exact list

# Option 1: App-layer gating (validate after LLM responds)
response = openai.chat.completions.create(tools=TOOLS_V1, ...)
for tool_call in response.tool_calls:
    if tool_call.function.name not in allowed_this_step:
        # reject, ask for confirmation, or re-prompt

# Option 2: Prompt-layer gating (instruct in user message)
messages = [
    {"role": "system", "content": STABLE_SYSTEM},
    {"role": "user", "content": f"{query}\n\nFor this step, only use: {allowed_this_step}"},
]
response = openai.chat.completions.create(tools=TOOLS_V1, messages=messages, ...)
```

Both approaches keep the tools schema identical across requests, preserving cache reuse. Filtering tools before sending (`tools_for_step = [t for t in TOOLS_V1 if ...]`) would break caching—don't do it.

---

## Engineering playbook for high cache hit rates

Even with identical prompts and a stable cache key, you will see intermittent misses due to best effort routing and finite cache retention. Monitor caching as a distribution, not a single datapoint. These practices help maximize hit rates.

### 1) Treat the serialized stream as the cache boundary

Do not reason in "messages." Reason in "what becomes early tokens."

- Keep stable content early (system + stable tools).
- Late-bind dynamic content (UUIDs/timestamps/per-request metadata) into later messages.

### 2) Build a stable “cache spine”

Put in system:
- core instructions
- stable examples
- stable policies

Keep out of system:
- request IDs, timestamps
- user/session metadata that changes per call
- anything that varies by request or by experiment arm

### 3) Version toolsets and evolve append-only

- Do not reorder tools for "priority"
- Append new tools at the end
- Prefer feature flags / app-layer gating for availability, not schema churn

### 4) Use `prompt_cache_key` to cluster similar requests

[`prompt_cache_key`](https://platform.openai.com/docs/guides/prompt-caching#prompt-cache-key) is an optional request parameter that hints the API to route requests with the same key to workers that likely share cached prefixes.

Choose keys that group requests sharing the same prefix structure:

- One key per agent/workflow type
- Version the key when you change system prompts or tool schemas

### 5) Monitor cache performance explicitly

Compute and log:

```python
cached = resp.usage.prompt_tokens_details.cached_tokens
total = resp.usage.prompt_tokens
cache_rate = cached / max(total, 1)
```

Track:
- average cache rate per endpoint / agent variant
- P50/P95 cache rate
- variance over time (spikes indicate drift)

Alert on:
- sustained drop >5%
- sudden variance increase

## Common mistakes

- **Dynamic metadata at end of system message**: Appending request IDs, timestamps, or session info to the system prompt seems safe but breaks caching when tools are present.

- **Prepending new tools**: Adding tools at the start of the array seems natural for visibility but shifts divergence early and wipes more cached prefix.

- **Expecting 100% cache hits**: Caching is best-effort. Even with identical prompts and `prompt_cache_key`, you will see occasional misses due to routing, cache eviction, or overflow. Design for high hit rates, not guaranteed hits.

## Cost and latency impact

Using [GPT-5.2 pricing](https://platform.openai.com/docs/pricing) as an example:

- 10,000 calls/day
- 10,000 prompt tokens/call → 100M prompt tokens/day
- Uncached input: $1.75 / 1M tokens
- Cached input: $0.175 / 1M tokens (90% discount)

Then:

- **No caching:** 100M × $1.75 = **$175/day**
- **90% cached:**  
  - Uncached 10M × $1.75 = **$17.50/day**  
  - Cached 90M × $0.175 = **$15.75/day**  
  - Total = **$33.25/day**

Broken caching can easily push you back toward the $175/day regime, purely from prompt/tool drift.

**Latency:** Cache hits also reduce time to first token (TTFT). Research shows 13-31% TTFT improvement across providers, though actual latency depends on your API tier (standard, batch, or flex). Naive full-context caching can sometimes *increase* latency, so strategic cache control matters.

> Pricing varies by model. Check [current pricing](https://platform.openai.com/docs/pricing) for your chosen model.

## Bottom line

The docs say: "static early, variable late; tools identical."

Where teams trip:
- With tools present, "end of system" is not "late" in the serialized stream
- Tool ordering changes move divergence early
- Cache wins require treating system + tools as a stable contract and late binding everything else

Code: [taming_agent_context](https://github.com/Asad-Ismail/taming_agent_context/tree/main/maning_context)