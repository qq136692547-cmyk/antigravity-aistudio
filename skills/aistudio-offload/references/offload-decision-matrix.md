# Google AI Studio Offload Decision Matrix

This reference documents the formal workload partitioning criteria, compute intensity evaluations, token threshold boundaries, and **Gemini 4** model selection rules (`Thinking level >= High`) for routing tasks between the local machine and Google AI Studio cloud models.

## Workload Partitioning Matrix

| Workload Type | Execution Target | Token Threshold | Recommended Model | Rationale & Routing Protocol |
| :--- | :--- | :--- | :--- | :--- |
| **Codebase Modifications** | **Local Machine** | N/A | Local Workspace Tools | Applying file edits, patch refactoring, code formatting, and tree modifications must execute directly in the local workspace via file tools. |
| **Git Operations** | **Local Machine** | N/A | Local Shell Tools | Branch creation, commit staging, rebase, merge, tag, and push operations require local git repository state. |
| **Test Suite Execution** | **Local Machine** | N/A | Local Test Runner | Running unit, integration, and regression suites (e.g., pytest, npm test, cargo test) requires local environment dependencies. |
| **Shell & System Commands** | **Local Machine** | N/A | Local Shell | Compiling binaries, installing packages, querying OS environment variables, and inspecting local processes must run locally. |
| **Fast Single-File Tweaks** | **Local Machine** | <50 lines | Local Editor Tools | Trivial edits, single-line adjustments, and localized fixes are cheaper to execute directly than paying browser automation startup overhead. |
| **Long-Context Document Analysis** | **Cloud Offload** | >=4,000 tokens (up to 1M) | Gemini 4 Hydrogen / Neon (High) | Massive logs, entire repository snapshots, large technical specifications, and book-length context offloaded to Gemini 4 (1M context) in AI Studio. |
| **Complex Logic & Debugging** | **Cloud Offload** | Any | Gemini 4 Argon (High) | Intricate bug root-cause isolation, fine-grained engineering proofs, and multi-constraint knowledge solving (explicitly switch Argon from Medium to High). |
| **Heavy Architectural Reasoning** | **Cloud Offload** | Any | Gemini 4 Neon / Carbon (High) | Repo-scale architectural synthesis, 64K long outputs (Neon), and extreme long-horizon math/science reasoning (Carbon, Paid gated). |
| **Prompt Engineering & Iteration** | **Cloud Offload** | Any | Gemini 4 Hydrogen / Neon (High) | Iterative prompt refinement, few-shot prompt crafting, and system instruction tuning run in AI Studio without consuming desktop model quota. |
| **Model Capability Comparison** | **Cloud Offload** | Any | Gemini 4 Hydrogen vs Argon vs Neon vs Carbon | Side-by-side behavioral evaluation across authorized Gemini 4 models (all locked to `Thinking level = High`) in AI Studio. |
| **Structured JSON Schema Testing** | **Cloud Offload** | Any | Gemini 4 Hydrogen (High) | Rapid validation of `Structured outputs` JSON schemas in chat or `/prompts/new_structured`. |
| **Synthetic Dataset Generation** | **Cloud Offload** | Any | Gemini 4 Hydrogen (High) | Generating large batches of synthetic test cases, mock JSON fixtures, or domain training corpora (up to 64K output per turn). |
| **Multimodal Asset Analysis** | **Cloud Offload** | Files >100 KB | Gemini 4 Neon (High) | Inspecting high-resolution UI diagrams, audio, video, or PDFs using calibrated `Media resolution` (`High`) via sandbox staging. |
| **Web Content Ingestion** | **Cloud Offload** | Any | Gemini 4 Hydrogen / Neon (High) | Fetching and analyzing live webpage bodies directly via AI Studio `URL context` and `Grounding with Google Search`. |
| **Production Code Export** | **Cloud Offload** | Any | Gemini 4 Hydrogen / Neon (High) | Extracting validated prompt configurations into production SDK code (Python, TypeScript, cURL, REST) via `Get code` with `thinking_level: "high"`. |

## Token Threshold Boundaries

- **Local Processing Window (<4,000 tokens)**: Lightweight prompts, single-function docstring generation, and brief inline queries execute locally on desktop models without requiring cloud browser delegation.
- **Cloud Offload Threshold (>=4,000 tokens)**: Whenever context, documents, or logs reach or exceed 4,000 tokens, the task must route to Google AI Studio to conserve desktop model quota.
- **Unified Gemini 4 1M Context Window (4,000 to 1,000,000 tokens)**: All four Gemini 4 models support `1,000,000` (`1M`) input tokens. For corpora exceeding 1M tokens, segment inputs or use multi-turn continuation (such as `Gemini 4 Carbon` or `Gemini 4 Neon` chunked sessions).

## Cloud Model Selection Matrix (Thinking Level Floor >= High)

| Model Tier | API Identifier | Tier / Gate | Context & Output | Best Suited Tasks | Required Thinking Level |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Gemini 4 Hydrogen** | `gemini-4-hydrogen` | Free & Paid (Default) | 1M in / 64K out | Routine long text/logs, structured JSON, batch synthetic data, daily code & prompt iteration | `High` (Web UI) / `"high"` or `"xhigh"` (API) |
| **Gemini 4 Argon** | `gemini-4-argon` | Pro / Paid | 1M in / 32K out | Complex logic debugging, fine-grained engineering, knowledge problem solving | **Must switch Medium -> `High`** |
| **Gemini 4 Neon** | `gemini-4-neon` | Pro / Paid | 1M in / 64K out | Repo-scale architecture, complex software engineering, deep multimodal/science, 64K long outputs | `High` (Web UI) / `"high"` or `"xhigh"` (API) |
| **Gemini 4 Carbon** | `gemini-4-carbon` | **Paid Gated** (Ultra / Paid API Key) | 1M in / 32K out (multi-turn to 1M) | Extreme long-horizon reasoning, hardest math, science, and frontier architecture tasks | **Must switch Medium -> `High`**; fallback to Neon/Hydrogen if paywalled |

**Forbidden Thinking Levels**: `Low` and `Medium` thinking levels are strictly disallowed for all cloud offload tasks.

## Deprecated Models and Pruning Rules

The following legacy models are retired, obsolete, or prohibited for cloud offloading. Never target, select, or recommend these models in offload planning:
- **PaLM 2**: `palm-2`, `chat-bison`, `chat-bison-001`, `text-bison`, `text-bison-001`
- **Gemini 1.0**: `gemini-1.0-pro`, `gemini-1.0-ultra`
- **Gemini 1.5**: `gemini-1.5-pro`, `gemini-1.5-flash`
- **Gemini 2.0**: `gemini-2.0-flash`, `gemini-2.0-pro`
- **Gemini 2.5**: `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-flash-thinking`
- **Gemini 3.x**: `gemini-3-flash-preview`, `gemini-3.1-pro-preview`, `gemini-3.8-flash`

Always verify that proposed offload workflows target active **Gemini 4** series models on `https://aistudio.google.com/` with `Thinking level >= High`.
