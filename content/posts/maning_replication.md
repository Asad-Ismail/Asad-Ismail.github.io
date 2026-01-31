+++
draft = false
date = 2026-01-28T00:00:00Z
title = "Testing Manus's Context Engineering Claims"
description = "Manus claims six techniques make their agent reliable at 50+ steps. I built a simple agent and ran ablations. 4 of 6 held up."
tags = ["LLMs", "Agents", "Context Engineering", "Prompt Caching"]
categories = ["Machine Learning", "Engineering"]
authors = ["Asad Ismail"]
+++
## Why you should care


Manus published a [blog post](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) describing how their agent typically runs for around 50 steps (tool calls) per task, and how context engineering techniques help maintain reliability over such long agent runs. They attribute this to six context engineering techniques: KV-cache stability, filesystem offloading, tool masking, goal recitation, error visibility, and few-shot variation.

I wanted to see if these claims hold up with actual numbers, so I built a simple agent and ran ablations against each technique.

## Quick takeaway

- 4 of 6 claims held up with measurable impact
- Breaking cache stability: 4x cost, 2.5x latency, task failure
- Skipping file offloading: 225K tokens → rate limit at step 5
- Recitation overhead on short tasks; probably helps at 50+ steps

## The test setup

Agent task: clean a 32K-row CSV (UCI Adult dataset). Fill missing values, clip outliers, add a computed column, validate output. Takes 5-10 tool calls. Simple enough to complete reliably, complex enough to show cache and token effects.

Stack: gpt-4o-mini, OpenAI flex tier, `prompt_cache_key` for cache routing, single non-streaming call per step for accurate metrics.

## The claims

| Claim | What They Say |
|-------|---------------|
| KV-cache stability | Keep prefix stable, append-only context, deterministic serialization |
| Filesystem as memory | Offload large content to files, read selectively (summary or full) |
| Mask, don't remove | Use logit masking to constrain tool selection without changing schema |
| Recitation | Rewrite todo.md each step to push goals to end of context |
| Error visibility | Leave failed actions in context so model learns to avoid repeating them |
| Few-shot variation | Add structured variation to break pattern mimicry in repetitive tasks |

## Results

| Variant | What I Changed | Steps | Success | Cache | Cost |
|---------|----------------|-------|---------|-------|------|
| **A1** | Baseline (all techniques) | 8 | ✅ | 89% | $0.024 |
| **B1** | Inject UUID each step | 15 | ❌ | 0% | $0.090 |
| **C1** | No file offloading | 5 | ❌ | — | — |
| **D1** | Remove tools dynamically | 15 | ❌ | 86% | $0.066 |
| **D2** | Use `tool_choice` instead | 8 | ✅ | 98% | $0.032 |
| **E2** | Remove recitation | 4 | ✅ | 75% | $0.014 |

## Breakdown

### B1: Cache breaking hurts

Injected a fresh UUID at system prompt start each step. Cache hit: 0%. Cost: 4x baseline. Agent drifted and failed after 15 steps.

Every step paid full prefill cost. No prefix reuse.

```
# What broke caching
system_prompt = f"Run ID: {uuid.uuid4()}\n\n{BASE_SYSTEM}"
```

### C1: Context explosion

Without file offloading, reading the 32K-row CSV dumped 200K+ tokens into messages. Hit rate limit at step 5.

![Token explosion per step](/images/c1_token_explosion.png)

Manus writes content to disk and reads selectively—summaries for orientation, full data when needed. Context stays small, but nothing is lost.

### D1 vs D2: Tool masking matters

D1 removed tools based on task state. When the tool list changed at step 6, cached tokens dropped from 12K to 1.6K.

D2 kept all tools but used `tool_choice` to constrain which tool the model could call. Cache stayed at 14K.

![D1 vs D2 cache comparison](/images/d1_vs_d2_cache.png)

```python
# D1: Breaks cache when tools change
tools = [t for t in ALL_TOOLS if t["function"]["name"] in allowed_this_step]

# D2: Preserves cache
tools = ALL_TOOLS  # always send full list
tool_choice = {"type": "function", "function": {"name": "task_complete"}}
```

If you need to gate tools per step, keep the schema stable and use `tool_choice`, app-layer validation, or prompt instructions instead of filtering. Never filter tools before sending—that's what broke D1.

### E2: Recitation is overhead on short tasks

Removing goal recitation instructions, the agent finished in 4 steps vs 8. For an 8-step task, recitation just adds steps.

But Manus averages 50 steps. At that length, restating goals probably prevents drift. Overhead worth paying.

## Gotchas

**Tool schemas serialize after system.** Putting UUID at system message *end* still broke cache when tools were present. Serialization order: system → tools → messages. An edit at "end of system" lands early in the token stream.

## Couldn't test

**Error recovery:** Manus keeps failed actions in context so the model learns from mistakes. Our task doesn't fail in recoverable ways often enough to measure this.

**Real logit masking:** Manus masks token logits during decoding based on a state machine. OpenAI doesn't expose this. `tool_choice` is the closest proxy.

**Few-shot variation:** Manus adds structured variation (different serialization, phrasing, formatting) when processing repetitive items like 20 resumes. Our task is a single pipeline—no repetitive subtasks where the model might copy its own rhythm.

## Bottom line

Cache stability and file offloading are real and measurable. Breaking either one tanks performance. Tool masking via `tool_choice` works. Recitation matters more as tasks get longer.

The techniques described by Manus worked for them—the hard part is wiring them up without accidentally breaking the cache. As always, your mileage may vary.

## Reproduce it

Code and instructions: [taming_agent_context/maning_context](https://github.com/Asad-Ismail/taming_agent_context/tree/main/maning_context)

## References

1. **Manus Blog Post** — Original context engineering claims.  
   [manus.im/blog/Context-Engineering-for-AI-Agents](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)

2. **OpenAI Prompt Caching Guide** — Official docs on caching behavior.  
   [platform.openai.com/docs/guides/prompt-caching](https://platform.openai.com/docs/guides/prompt-caching)

3. **Why Your Prompt Cache Keeps Missing** — My deep dive on cache failure patterns.  
   [/posts/prompt_caching/](/posts/prompt_caching/)
