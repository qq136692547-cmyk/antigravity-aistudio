# Google AI Studio Plugin Operating Rules

These rules apply whenever the user works with **Google AI Studio** (`https://aistudio.google.com/`) or offloads workloads to cloud models through this plugin.

## 1. Browser Delegation, Canonical Entry URL & Session Reuse

- Always drive Google AI Studio through Antigravity's built-in `browser` subagent (`invoke_subagent` with `TypeName: "browser"`, `Model: "flash"` unless the user explicitly requests another driver model). Do not use `curl`, raw Playwright scripts, or external browser launchers to interact with Google AI Studio.
- Always open **`https://aistudio.google.com/`** directly as the canonical entry URL (or deep-link directly to specialized views: `/prompts/new_chat`, `/prompts/new_structured`, `/prompts`, `/tune`, or `/apikey`). Avoid navigating through legacy redirect URLs or intermediary portals, which can trigger an unnecessary `accounts.google.com` Single Sign-On (SSO) redirect hop even when the user is already signed in.
- Within an AI Studio offload session, reuse the same `browser` subagent via `send_message` using its `conversationId` so the open workspace tab and authenticated session stay intact. Do not kill an idle `browser` subagent between steps.
- Give the `browser` subagent **semantic UI goals** (visible labels, controls, role targets, and visual verification criteria) rather than brittle CSS selectors, ensuring workflows remain resilient across Google AI Studio UI updates.

## 2. Fast-Path Authentication Check (Signed-In Shortcut)

Before assuming the user needs to sign in, always verify whether an authenticated Google AI Studio session is already active:

- **Check the current tab first** (if already on `https://aistudio.google.com/...`); otherwise navigate directly to `https://aistudio.google.com/`.
- **Verify signed-in state using visual, DOM, and network signals together**:
  - **Above-the-fold visual & DOM signals**: Presence of the user profile avatar in the header, the `+ Create prompt` (or `Create prompt`) button, the `Get API key` button, the navigation sidebar, or the recent prompts library table, alongside the explicit absence of any `Sign in` button.
  - **URL & network signals**: Page URL remains on `https://aistudio.google.com/` (such as `/prompts/new_chat`, `/prompts`, `/tune`, or `/?pli=1`) and backend API RPC requests return HTTP `200`.
  - **Sandbox constraint**: Do not attempt to read `document.cookie`, `localStorage`, or `sessionStorage` via `page.evaluate`, as those APIs are strictly blocked by the sandboxed browser runtime.
- **Shortcut**: As soon as the signed-in signals are confirmed, skip all authentication prompts and proceed directly to the requested task.
- Only pause with `LOGIN_REQUIRED` when opening `https://aistudio.google.com/` directly redirects to `accounts.google.com` or renders a logged-out landing page containing a `Sign in` button.

## 3. Local vs. Cloud Offload Decision Engine

The core architectural mission of `antigravity-aistudio` is **Cloud Agent Offloading**: tasks that do not require local machine execution are offloaded to **Gemini 4** frontier models inside Google AI Studio via the browser subagent. This preserves Antigravity desktop app model quota (such as Neon, Hydrogen, Argon, and Opus quota) for local development tasks.

### Authorized Gemini 4 Cloud Models & Thinking Level Floor

Only the four **Gemini 4** chat models (unified `1M` / `1,000,000` token context window) are permitted for cloud offloading:

1. **`Gemini 4 Hydrogen`** (`gemini-4-hydrogen`) -- `1M` input / `64K` (`65536`) output, Free & Paid default workhorse (`/prompts/new_chat` default). Use for routine long text/logs (4,000 to 1M tokens), structured JSON, batch synthetic data, and daily code/prompt iteration.
2. **`Gemini 4 Argon`** (`gemini-4-argon`) -- `1M` input / `32K` (`32768`) output, Pro/Paid tier. Use for complex logic debugging, fine-grained engineering, and knowledge problem solving. **Web UI defaults to Medium -- must explicitly switch `Thinking level` to `High`.**
3. **`Gemini 4 Neon`** (`gemini-4-neon`) -- `1M` input / `64K` (`65536`) output, Pro/Paid tier. Use for repo-wide architecture design, complex software engineering, deep multimodal/scientific analysis, and heavy tasks requiring 64K single-turn output.
4. **`Gemini 4 Carbon`** (`gemini-4-carbon`) -- `1M` input / `32K` (`32768`) output (supports multi-turn continuation up to 1M), **`Paid` gated** (requires Google AI Ultra or billed Paid API key). Use for extreme long-horizon reasoning and the hardest math/science/architecture tasks. **Web UI defaults to Medium -- must explicitly switch `Thinking level` to `High`.**

**Hard Thinking Level Floor (`>= High`)**:
- All cloud offload executions MUST use **`Thinking level = High`** in the Google AI Studio Web UI (`"high"` or `"xhigh"` in SDK/API `thinking_level`).
- **`Low` and `Medium` thinking levels are strictly prohibited** for cloud offload workloads.
- Gemini 4 `Run settings` no longer exposes legacy `Temperature`, `Top-P`, `Top-K`, or `Thinking budget` sliders; control generation via `Thinking level` (`High`), `Output length` (`65536` or `32768`), `Media resolution`, `Safety settings`, `Add stop sequence`, and the `Tools` panel (`Structured outputs`, `Code execution`, `Function calling`, `Grounding with Google Search`, `URL context`).

**Deprecated Model Blacklist (Strictly Prohibited)**:
- Never select or recommend any pre-Gemini-4 chat model, including `PaLM 2`, `Gemini 1.0`, `Gemini 1.5`, `Gemini 2.0`, `Gemini 2.5` (`gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-flash-thinking`), or `Gemini 3.x` (`gemini-3-flash-preview`, `gemini-3.1-pro-preview`, `gemini-3.8-flash`).

### Workload Partitioning Matrix

| Workload Type | Execution Target | Rationale & Routing Protocol |
| :--- | :--- | :--- |
| **Codebase Modifications** | **Local Machine** | Applying file edits, patch refactoring, and code styling must occur in the local workspace. |
| **Git Operations** | **Local Machine** | Branching, staging, committing, and pushing must run through local shell tools. |
| **Test Execution** | **Local Machine** | Running test suites (`pytest`, `npm test`, `cargo test`) requires local environment dependencies. |
| **Shell & System Commands** | **Local Machine** | Compiling binaries, installing packages, and querying OS status must execute locally. |
| **Fast Single-File Tweaks** | **Local Machine** | Trivial edits (<50 lines) are cheaper to execute directly than paying browser automation overhead. |
| **Long-Context Document Analysis** | **Cloud Offload (AI Studio)** | Large documents, massive logs, and repository-wide context (>4k tokens, up to 1M tokens) processed with `Gemini 4 Hydrogen` or `Gemini 4 Neon` (`Thinking: High`). |
| **Heavy Architectural Reasoning** | **Cloud Offload (AI Studio)** | Deep design synthesis, trade-off evaluations, and extreme math/algorithm derivation offloaded to `Gemini 4 Neon` or `Gemini 4 Carbon` (`Thinking: High`). |
| **Prompt Engineering & Few-Shot Tuning** | **Cloud Offload (AI Studio)** | Iterative prompt iteration, system instruction refinement, and few-shot table optimization run in AI Studio without burning desktop quota. |
| **Model Capability Comparison** | **Cloud Offload (AI Studio)** | Side-by-side evaluation across `Gemini 4 Hydrogen`, `Argon`, `Neon`, and `Carbon` (`Thinking: High`) performed directly in AI Studio. |
| **Structured JSON Schema Testing** | **Cloud Offload (AI Studio)** | Rapid testing of `Structured outputs` schemas in chat or `/prompts/new_structured` using `Gemini 4 Hydrogen` (`Thinking: High`). |
| **Synthetic Dataset Generation** | **Cloud Offload (AI Studio)** | Generating batch test cases, mock data, or synthetic domain corpora offloaded to `Gemini 4 Hydrogen` (`Thinking: High`). |
| **Multimodal Asset Analysis** | **Cloud Offload (AI Studio)** | Evaluating high-resolution images, audio clips, video, or PDFs via `Media resolution` (`High`) and `Gemini 4 Neon` (`Thinking: High`). |
| **Web Documentation Synthesis** | **Cloud Offload (AI Studio)** | Fetching and analyzing live web pages directly via AI Studio `URL context` and `Grounding with Google Search` tools. |
| **Production Code Export** | **Cloud Offload (AI Studio)** | Extracting optimized prompts into production SDK snippets (Python, TypeScript, cURL, REST) using the AI Studio `Get code` modal. |

### Offload Lifecycle Pipeline

When an offload candidate is detected, follow the strict 6-stage lifecycle:
1. **Task Evaluation**: Verify the task matches cloud offload criteria using the decision matrix and assign an authorized Gemini 4 model.
2. **Context Staging**: Prepare prompts, system instructions, and required files in `<Artifact Directory Path>/browser_sandbox/uploads/`.
3. **Browser Dispatch**: Delegate the prompt to the `browser` subagent targeting `https://aistudio.google.com/`.
4. **Cloud Execution**: Run model inference in Google AI Studio with `Thinking level = High`, calibrated `Output length` / `Media resolution` / `Tools`, and safety settings.
5. **Output Extraction**: Capture model responses, generated structured data, or exported code snippets.
6. **Local Synchronization**: Write extracted artifacts back to the workspace and execute local verification.

## 4. Autonomy Modes (Checkpoint vs. Auto)

Two execution modes govern cloud offloading workflows:

- **`checkpoint` mode (default)**: The agent prepares the prompt text, system instructions, Gemini 4 model & `Thinking level = High` configurations, and staged sandbox assets, then **pauses and presents the offload plan to the user for confirmation** before triggering generation or code export in Google AI Studio.
- **`auto` mode (full-auto)**: The agent executes the entire pipeline end-to-end -- navigating AI Studio, selecting the Gemini 4 model, enforcing `Thinking level = High`, executing prompts, extracting outputs, and synchronizing workspace files -- without pausing for per-step approval.

### Detecting Mode from the User's Prompt

- Automatically enable `auto` mode whenever the user's prompt signals unattended or batch execution in any language -- for example: `"auto mode"`, `"full-auto"`, `"run unattended"`, `"without asking"`, `"don't ask for confirmation"`, or `"batch offload"`.
- If the user does not specify a mode, use `checkpoint` mode by default and inform the user that they can switch to `auto` mode at any time (e.g., by replying `"switch to auto mode"`).

## 5. Hard Safety & Platform Boundaries (Both Modes)

Even in `auto` mode, the agent must immediately pause and hand control to the user when encountering:

- **Google Sign-In / Authentication (`LOGIN_REQUIRED`)**: Protected authentication origins cannot be automated. Request that the user sign in inside the browser pane, then resume the same `browser` subagent via `send_message`.
- **CAPTCHA / Bot Challenges (`CAPTCHA_REQUIRED`)**: Never attempt to solve, manipulate, or bypass anti-bot challenges. Pause and ask the user to complete verification.
- **Paid Tier Gate (`Unlock Gemini 4 Carbon` / `PAID_TIER_REQUIRED`)**: If selecting `Gemini 4 Carbon` triggers an `Unlock Gemini 4 Carbon` paywall or upgrade prompt, immediately pause, notify the user, and offer fallback options to `Gemini 4 Neon (High)` or `Gemini 4 Hydrogen (High)`.
- **Quota Exhaustion or Rate Limits (`429 ResourceExhausted` / `QUOTA_EXHAUSTED`)**: When AI Studio returns a rate limit error banner or quota threshold dialog, pause and notify the user. Offer to fall back from `Gemini 4 Carbon` / `Gemini 4 Neon` to `Gemini 4 Hydrogen (High)` or wait for quota reset.
- **Content Safety Filter Blocks (`HARM_CATEGORY_*` / `SAFETY_BLOCKED`)**: When prompt generation is blocked by safety filters (e.g., Harassment, Hate Speech, Sexually Explicit, Dangerous Content), extract the specific block reason, report it to the user, and offer to adjust prompt phrasing or model safety threshold settings.

## 6. Local File Staging Contract

The Antigravity `browser` subagent operates in a sandboxed runtime environment and cannot directly access arbitrary local workspace directories:

- **For Web Uploads (Media, Documents, Data)**: Copy each file from the local workspace to `<Artifact Directory Path>/browser_sandbox/uploads/<filename>` (using a single-segment filename) and pass the bare `<filename>` to the `browser` subagent.
- **For Visual Reference Inspection**: Copy reference images or diagrams to `<Artifact Directory Path>/browser_sandbox/references/<filename>` and supply the absolute path to inspection tools.
- **For Downloaded Artifacts & Code Exports**: Save downloaded code snippets, JSON schemas, or prompt configurations into `<Artifact Directory Path>/browser_sandbox/downloads/<filename>`. Then copy and integrate the final assets into the destination workspace directory.
