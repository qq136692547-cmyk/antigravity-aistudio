# Google AI Studio Offload Decision Matrix

This reference documents the formal workload partitioning criteria, compute intensity evaluations, token threshold boundaries, and model selection rules for routing tasks between the local machine and Google AI Studio cloud models.

## Workload Partitioning Matrix

| Workload Type | Execution Target | Token Threshold | Recommended Model | Rationale & Routing Protocol |
| :--- | :--- | :--- | :--- | :--- |
| **Codebase Modifications** | **Local Machine** | N/A | Local Workspace Tools | Applying file edits, patch refactoring, code formatting, and tree modifications must execute directly in the local workspace via file tools. |
| **Git Operations** | **Local Machine** | N/A | Local Shell Tools | Branch creation, commit staging, rebase, merge, tag, and push operations require local git repository state. |
| **Test Suite Execution** | **Local Machine** | N/A | Local Test Runner | Running unit, integration, and regression suites (e.g., pytest, npm test, cargo test) requires local environment dependencies. |
| **Shell & System Commands** | **Local Machine** | N/A | Local Shell | Compiling binaries, installing packages, querying OS environment variables, and inspecting local processes must run locally. |
| **Fast Single-File Tweaks** | **Local Machine** | <50 lines | Local Editor Tools | Trivial edits, single-line adjustments, and localized fixes are cheaper to execute directly than paying browser automation startup overhead. |
| **Long-Context Document Analysis** | **Cloud Offload** | >4,000 tokens (up to 2M) | Gemini 2.5 Flash / Pro | Massive logs, entire repository snapshots, large technical specifications, and book-length context are offloaded to Gemini 2.5 in AI Studio. |
| **Heavy Architectural Reasoning** | **Cloud Offload** | Any | Gemini Flash Thinking / Pro | Complex algorithm design, multi-system architectural trade-offs, formal protocol proofs, and deep reasoning offloaded to cloud models. |
| **Prompt Engineering & Iteration** | **Cloud Offload** | Any | Gemini 2.5 Pro / Flash | Iterative prompt refinement, few-shot prompt crafting, and system instruction tuning run in AI Studio without consuming desktop model quota. |
| **Model Capability Comparison** | **Cloud Offload** | Any | Gemini 2.5 Pro vs Flash | Side-by-side behavioral evaluation across different model tiers (Flash vs Pro vs Flash Thinking) performed directly in the cloud workspace. |
| **Structured JSON Schema Testing** | **Cloud Offload** | Any | Gemini 2.5 Flash | Rapid validation of JSON schema structured outputs and constrained decoding in AI Studio structured prompt editor. |
| **Synthetic Dataset Generation** | **Cloud Offload** | Any | Gemini 2.5 Flash | Generating large batches of synthetic test cases, mock JSON fixtures, or domain training corpora offloaded to AI Studio cloud compute. |
| **Multimodal Asset Analysis** | **Cloud Offload** | Files >100 KB | Gemini 2.5 Pro / Flash | Inspecting high-resolution UI diagrams, long audio recordings, video clips, or multi-page PDF documents staged via the sandbox upload contract. |
| **Production Code Export** | **Cloud Offload** | Any | Gemini 2.5 Pro / Flash | Extracting validated prompt configurations into production-ready SDK code (Python, TypeScript, cURL, REST) using the AI Studio Get code dialog. |

## Token Threshold Boundaries

- **Local Processing Window (<4,000 tokens)**: Lightweight prompts, single-function docstring generation, and brief inline queries execute locally on desktop models without requiring cloud browser delegation.
- **Cloud Offload Threshold (>=4,000 tokens)**: Whenever context, documents, or logs reach or exceed 4,000 tokens, the task must route to Google AI Studio to conserve desktop model quota.
- **Gemini 2.5 Flash Window (4,000 to 1,000,000 tokens)**: Default cloud model for large-context processing, rapid drafting, synthetic data generation, and structured outputs.
- **Gemini 2.5 Pro Window (1,000,000 to 2,000,000 tokens)**: Extreme long-context corpus analysis, exhaustive log diagnostics, and repository-wide code comprehension.

## Cloud Model Selection Matrix

| Model Tier | Context Window | Best Suited Tasks | Default Parameter Preset |
| :--- | :--- | :--- | :--- |
| **Gemini 2.5 Flash** | 1,000,000 tokens | Fast drafting, structured JSON extraction, batch dataset generation, prompt testing | Temperature: 0.7, Top-P: 0.95, Top-K: 40 |
| **Gemini 2.5 Pro** | 2,000,000 tokens | Extreme-context analysis, intricate architectural synthesis, deep multimodal evaluation | Temperature: 0.2, Top-P: 0.95, Top-K: 40 |
| **Gemini Flash Thinking** | 1,000,000 tokens | Deep mathematical derivation, complex logic puzzles, security protocol formal verification | Thinking Budget: Auto / Configured |

## Deprecated Models and Pruning Rules

The following legacy models are retired or obsolete. Never target or recommend these models in offload planning:
- PaLM 2 (chat-bison, text-bison)
- Gemini 1.0 (gemini-1.0-pro, gemini-1.0-ultra)
- Gemini 1.5 Preview builds that have reached end-of-life

Always verify that proposed offload workflows use active Gemini 2.5 series models available on `https://aistudio.google.com/`.
