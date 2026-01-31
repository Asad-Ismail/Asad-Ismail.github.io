+++
draft = false
date = 2026-01-28T00:00:00Z
title = "Why Your Prompt Cache Keeps Missing"
description = "Prompt caching can cut LLM costs by 90%, but small changes break cache reuse. This post covers the failure patterns and rules for high cache hit rates."
tags = ["LLMs", "Prompt Caching", "Cost Optimization"]
categories = ["Machine Learning", "Engineering"]
authors = ["Asad Ismail"]
+++
## Why you should care

Agentic workflows resend a large, mostly static context on every call: system instructions, tool schemas, and growing conversation history. Prompt caching can make those repeated tokens far cheaper and faster. But the failure modes are subtle: small changes can shift where your prompt diverges from the cached prefix and wipe most (or all) reuse.

This post covers the failure patterns I ran into and the rules that kept cache hit rates high.

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

I ran two experiments to see how small changes affect caching. All numbers come from actual API responses (`prompt_tokens`, `cached_tokens`).

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

With tools in the request, appending to the system message collapsed cached tokens to zero. Appending to the user message preserved reuse.

Why? Tools serialize after system. So "end of system" lands earlier in the token stream than you'd expect—before the cached checkpoint.

**Practical rule:** Late-bind dynamic metadata:

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

Prepending moved the divergence point earlier, wiping a larger prefix. Appending kept more cache.

At smaller prompt sizes, tool changes sometimes collapsed caching to zero—if the checkpoint falls inside the tools region, any tool modification invalidates it.

**Practical rule:** Treat tool ordering like an API contract:

```python
# Risky: can wipe cached prefix
tools = [new_tool] + existing_tools

# Safer: append-only evolution
tools = existing_tools + [new_tool]
```

> **Need to gate tool availability per step?** Send a stable schema and control access via `tool_choice`, app-layer validation, or prompt instructions—see [Testing Manus's Context Engineering Claims](/posts/maning_replication/) for patterns and experiment data.

---

## Playbook

Even with identical prompts and a stable cache key, you'll see intermittent misses—routing is best-effort and caches expire. Monitor as a distribution, not a single number.

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

## Cost and latency impact (napkin math)

Real-world cache performance varies. You won't hit 100% cache rates—routing, eviction, and prompt drift all cause misses. But even rough estimates show why this matters.

**Assumptions (GPT-5.2 pricing, adjust for your model):**

- 10,000 calls/day
- ~10,000 prompt tokens/call → ~100M prompt tokens/day
- Uncached input: $1.75 / 1M tokens
- Cached input: $0.175 / 1M tokens (90% discount)

**Scenario comparison:**

| Scenario | Effective cache rate | Daily cost (approx) |
|----------|---------------------|--------------------|
| No caching | 0% | ~$175 |
| Broken caching (drift/schema churn) | 20-40% | ~$120-140 |
| Healthy caching | 70-85% | ~$45-60 |
| Optimized (stable prefix + routing) | 85-95% | ~$30-45 |

The math is rough because:
- Not all tokens in a request are cacheable (only the matching prefix)
- Cache hit rate varies by time of day, traffic patterns, and API tier
- First request in a session always misses

Point is: broken caching costs 3-4x more. Monitor your actual `cached_tokens` to know where you stand.

**Latency:** Cache hits also reduce time to first token (TTFT). Lumer et al. measured 13-31% TTFT improvement across providers, though actual latency depends on your API tier (standard, batch, or flex). Naive full-context caching can sometimes *increase* latency, so strategic cache control matters.

> Pricing varies by model and changes over time. Check [current pricing](https://platform.openai.com/docs/pricing) for your model.

## Bottom line

The docs say: "static early, variable late; tools identical."

What they don't say:
- With tools present, "end of system" is not "late" in the serialized stream
- Tool ordering changes move divergence early
- Cache wins require treating system + tools as a stable contract and late binding everything else

Code: [taming_agent_context](https://github.com/Asad-Ismail/taming_agent_context/tree/main/maning_context)

---

## References

1. **OpenAI Prompt Caching Guide** — Official documentation on caching behavior, boundaries, and `prompt_cache_key`.  
   [platform.openai.com/docs/guides/prompt-caching](https://platform.openai.com/docs/guides/prompt-caching)

2. **OpenAI Prompt Caching Announcement** — Launch post with caching mechanics overview.  
   [openai.com/index/api-prompt-caching](https://openai.com/index/api-prompt-caching/)

3. **Lumer et al., "Don't Break the Cache" (2026)** — Cross-provider evaluation of prompt caching including latency benchmarks (13-31% TTFT improvement) and failure mode analysis.  
   [arxiv.org/abs/2601.06007](https://arxiv.org/abs/2601.06007)

4. **OpenAI Pricing** — Current token pricing for cached vs uncached input.  
   [platform.openai.com/docs/pricing](https://platform.openai.com/docs/pricing)

5. **Testing Manus's Context Engineering Claims** — Related post with tool gating experiments and cache stability ablations.  
   [/posts/maning_replication/](/posts/maning_replication/)