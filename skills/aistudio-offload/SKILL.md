---
name: aistudio-offload
description: Master cloud offload coordinator evaluating tasks against the Decision Matrix, staging local assets to browser sandbox, delegating to browser subagent on Gemini 4 (Thinking >= High), and syncing outputs.
---

# AI Studio Cloud Offload Coordinator

Evaluate, route, and execute computational tasks in **Google AI Studio** (`https://aistudio.google.com/`) via Antigravity's built-in browser subagent on **Gemini 4** models (`Thinking level = High`) to conserve local desktop application model quota.

## When to Use

- The user asks to draft, analyze, or reason over large text documents, repository codebases, or log files reaching or exceeding 4,000 tokens (up to 1,000,000 tokens).
- The user requests complex architectural reasoning, algorithm derivation, debugging, or trade-off evaluation that would consume substantial desktop frontier model quota.
- The user requests iterative prompt engineering, few-shot prompt construction, or system instruction calibration in Google AI Studio.
- The user wants to compare model outputs across `Gemini 4 Hydrogen`, `Gemini 4 Argon`, `Gemini 4 Neon`, or `Gemini 4 Carbon`.
- The user requests structured JSON schema validation, synthetic dataset generation, or live webpage ingestion via `URL context`.
- Consult the full decision criteria in [Offload Decision Matrix](./references/offload-decision-matrix.md).

## Offload Lifecycle Pipeline

Every cloud offload execution follows a strict 6-stage lifecycle:

```
[1. Evaluate] --> [2. Stage] --> [3. Dispatch] --> [4. Execute] --> [5. Extract] --> [6. Sync]
```

### Stage 1: Task Evaluation

1. Check incoming task parameters against [Offload Decision Matrix](./references/offload-decision-matrix.md).
2. Determine whether the task requires local shell execution, git mutations, or direct file edits:
   - If local execution is mandatory (e.g., git commits, running pytest, compiling binaries), retain the task on the **Local Machine**.
   - If the task is purely reasoning, drafting, analyzing, or prompt testing, route to **Cloud Offload**.
3. Evaluate token volume and compute intensity:
   - Tasks under 4,000 tokens with low compute intensity remain local.
   - Tasks reaching or exceeding 4,000 tokens, or requiring multi-step reasoning, qualify for cloud offload.
4. Select an authorized **Gemini 4** cloud model (unified `1M` / `1,000,000` token context; **all pre-Gemini-4 models are strictly forbidden**):
   - **`Gemini 4 Hydrogen`** (`gemini-4-hydrogen`, `1M` in / `64K` out, Free & Paid default): Routine long text/logs (4,000 to 1M tokens), structured JSON, batch synthetic data, daily code & prompt iteration.
   - **`Gemini 4 Argon`** (`gemini-4-argon`, `1M` in / `32K` out, Pro/Paid): Complex logic debugging, fine-grained engineering, knowledge solving. (**Must switch Web UI `Thinking level` from default `Medium` to `High`.**)
   - **`Gemini 4 Neon`** (`gemini-4-neon`, `1M` in / `64K` out, Pro/Paid): Repo-wide architectural design, complex software engineering, deep multimodal/scientific analysis, heavy tasks needing 64K single-turn output.
   - **`Gemini 4 Carbon`** (`gemini-4-carbon`, `1M` in / `32K` out with multi-turn continuation up to 1M, **`Paid` gated**): Extreme long-horizon reasoning and hardest math/science/architecture tasks. (**Must switch Web UI `Thinking level` from default `Medium` to `High`; if `Unlock Gemini 4 Carbon` appears, pause and offer fallback to `Gemini 4 Neon (High)` or `Gemini 4 Hydrogen (High)`.**)

### Stage 2: Context and Asset Staging

The browser subagent operates in a sandboxed environment and cannot read arbitrary local directories:
1. Identify any local files (source code, logs, documents, images) required by the prompt.
2. Copy files to the staging directory:
   `<Artifact Directory Path>/browser_sandbox/uploads/<filename>`
3. Use a single-segment filename (e.g., `system_architecture.txt`, `sample_dataset.csv`).
4. Record staged filenames for the browser subagent dispatch payload.

### Stage 3: Browser Subagent Dispatch

1. Determine autonomy mode from user intent:
   - **`checkpoint` mode (default)**: Present the offload execution plan (target Gemini 4 model, `Thinking level: High`, prompt summary, staged assets) and pause for user confirmation before triggering cloud inference.
   - **`auto` mode**: Proceed directly to execution if the user specified unattended or automated operation (e.g., "auto mode", "full-auto", "run unattended").
2. Dispatch Antigravity's built-in `browser` subagent:
   - Call `invoke_subagent` with `TypeName: "browser"` and `Model: "flash"`.
   - Provide direct canonical URL: `https://aistudio.google.com/`.
   - Provide semantic UI goals rather than brittle CSS selectors.
3. Perform Fast-Path Authentication Check:
   - Check if the page displays signed-in visual signals (user avatar in top bar, "Create prompt" button, "Get API key" link, recent prompts library).
   - Verify RPC network requests return HTTP 200.
   - If signed in, immediately skip authentication and proceed to prompt creation.
   - If redirected to `accounts.google.com` or a page with a prominent "Sign in" button, pause with `LOGIN_REQUIRED`.

### Stage 4: Cloud Execution

1. Navigate to the appropriate AI Studio interface:
   - Chat Prompt: `https://aistudio.google.com/prompts/new_chat`
   - Structured Prompt: `https://aistudio.google.com/prompts/new_structured`
2. Configure the model selector dropdown to the chosen **Gemini 4** model (`Gemini 4 Hydrogen`, `Argon`, `Neon`, or `Carbon`).
   - If `Unlock Gemini 4 Carbon` paywall appears, immediately pause (`PAID_TIER_REQUIRED`) and prompt the user to upgrade or fall back to `Gemini 4 Neon (High)` or `Gemini 4 Hydrogen (High)`.
3. Enforce the **Thinking Level Floor**: open `Run settings` and explicitly verify/set **`Thinking level = High`** (mandatory for `Argon` and `Carbon`, which default to `Medium`; **`Low` and `Medium` are forbidden**).
4. Configure Gemini 4 `Run settings` and `Tools` as needed (`Output length` up to `65536` or `32768`, `Media resolution`, `Safety settings`, `Add stop sequence`, `Structured outputs`, `Code execution`, `Function calling`, `Grounding with Google Search`, `URL context`). Note: legacy `Temperature`, `Top-P`, `Top-K`, and `Thinking budget` sliders are removed in Gemini 4.
5. If staged assets exist, attach them via the file upload interface using the bare staged filename from `browser_sandbox/uploads/`.
6. Insert prompt text, system instructions, or few-shot examples into their designated input areas.
7. Trigger model execution (click `Run` or press `Ctrl+Enter`) and monitor generation progress until completion.

### Stage 5: Output Extraction

1. Verify generation completed without safety blocks or quota errors.
2. Extract the model response text, tabular rows, or code snippet from the AI Studio editor DOM.
3. If exporting code, trigger the `Get code` modal, select the desired language (Python, TypeScript, cURL, REST), and copy the snippet.
4. Save the raw downloaded or extracted artifact into `<Artifact Directory Path>/browser_sandbox/downloads/<filename>`.

### Stage 6: Local Synchronization

1. Read the extracted output from `browser_sandbox/downloads/<filename>`.
2. Write the processed result to the destination workspace file (e.g., `docs/architecture_analysis.md`, `src/extracted_schema.json`).
3. If code was exported, replace any raw keys with the `GEMINI_API_KEY` environment variable and ensure `thinking_level` is `"high"` or `"xhigh"`.
4. Verify file integrity and formatting in the local workspace.
5. Present the final result summary to the user.

## Safety and Quota Boundary Protocol

Always enforce hard safety boundaries regardless of autonomy mode:
- **`LOGIN_REQUIRED`**: If redirected to `accounts.google.com`, pause and ask the user to complete Google authentication in the browser pane. Resume the same subagent session via `send_message` after sign-in.
- **`CAPTCHA_REQUIRED`**: Never attempt to bypass anti-bot challenges. Pause and ask the user to solve the challenge.
- **`PAID_TIER_REQUIRED` (`Unlock Gemini 4 Carbon`)**: If `Gemini 4 Carbon` displays a paid-tier gate, pause immediately and offer fallback to `Gemini 4 Neon (High)` or `Gemini 4 Hydrogen (High)`.
- **`QUOTA_EXHAUSTED` / `429 ResourceExhausted`**: If AI Studio displays a quota limit banner, pause and notify the user. Offer to fall back to `Gemini 4 Hydrogen (High)` or wait for quota reset.
- **`SAFETY_BLOCKED`**: If response generation is blocked by safety filters (`HARM_CATEGORY_*`), report the category to the user and adjust prompt phrasing or safety thresholds.
