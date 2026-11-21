---
name: aistudio-offload
description: Master cloud offload coordinator evaluating tasks against the Decision Matrix, staging local assets to browser sandbox, delegating to browser subagent, and syncing outputs.
---

# AI Studio Cloud Offload Coordinator

Evaluate, route, and execute computational tasks in **Google AI Studio** (`https://aistudio.google.com/`) via Antigravity's built-in browser subagent to conserve local desktop application model quota.

## When to Use

- The user asks to draft, analyze, or reason over large text documents, repository codebases, or log files exceeding 4,000 tokens.
- The user requests complex architectural reasoning, algorithm derivation, or trade-off evaluation that would consume substantial desktop frontier model quota.
- The user requests iterative prompt engineering, few-shot prompt construction, or system instruction calibration in Google AI Studio.
- The user wants to compare model outputs across Gemini 2.5 Flash, Gemini 2.5 Pro, or Gemini Flash Thinking.
- The user requests structured JSON schema validation or synthetic dataset generation.
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
4. Select the target cloud model:
   - **Gemini 2.5 Flash**: Fast drafting, synthetic datasets, structured prompt testing (up to 1,000,000 tokens).
   - **Gemini 2.5 Pro**: Extreme-context analysis, repository-wide reasoning (1,000,000 to 2,000,000 tokens).
   - **Gemini Flash Thinking**: Deep logical deduction, math proofs, complex algorithm design.

### Stage 2: Context and Asset Staging

The browser subagent operates in a sandboxed environment and cannot read arbitrary local directories:
1. Identify any local files (source code, logs, documents, images) required by the prompt.
2. Copy files to the staging directory:
   `<Artifact Directory Path>/browser_sandbox/uploads/<filename>`
3. Use a single-segment filename (e.g., `system_architecture.txt`, `sample_dataset.csv`).
4. Record staged filenames for the browser subagent dispatch payload.

### Stage 3: Browser Subagent Dispatch

1. Determine autonomy mode from user intent:
   - **`checkpoint` mode (default)**: Present the offload execution plan (target model, prompt summary, staged assets) and pause for user confirmation before triggering cloud inference.
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
2. Configure model selection dropdown to the chosen Gemini 2.5 model tier.
3. Configure hyperparameters (Temperature, Top-P, Top-K, Thinking Budget, Safety Settings) per task requirements.
4. If staged assets exist, attach them via the file upload interface using the bare staged filename from `browser_sandbox/uploads/`.
5. Insert prompt text, system instructions, or few-shot examples into their designated input areas.
6. Trigger model execution (click `Run` or press `Ctrl+Enter`).
7. Monitor generation progress until completion.

### Stage 5: Output Extraction

1. Verify generation completed without safety blocks or quota errors.
2. Extract the model response text, tabular rows, or code snippet from the AI Studio editor DOM.
3. If exporting code, trigger the `Get code` modal, select the desired language (Python, TypeScript, cURL, REST), and copy the snippet.
4. Save the raw downloaded or extracted artifact into `<Artifact Directory Path>/browser_sandbox/downloads/<filename>`.

### Stage 6: Local Synchronization

1. Read the extracted output from `browser_sandbox/downloads/<filename>`.
2. Write the processed result to the destination workspace file (e.g., `docs/architecture_analysis.md`, `src/extracted_schema.json`).
3. If code was exported, replace any raw keys with the `GEMINI_API_KEY` environment variable.
4. Verify file integrity and formatting in the local workspace.
5. Present the final result summary to the user.

## Safety and Quota Boundary Protocol

Always enforce hard safety boundaries regardless of autonomy mode:
- **`LOGIN_REQUIRED`**: If redirected to `accounts.google.com`, pause and ask the user to complete Google authentication in the browser pane. Resume the same subagent session via `send_message` after sign-in.
- **`CAPTCHA_REQUIRED`**: Never attempt to bypass anti-bot challenges. Pause and ask the user to solve the challenge.
- **`QUOTA_EXHAUSTED` / `429 ResourceExhausted`**: If AI Studio displays a quota limit banner, pause and notify the user. Offer to switch to Gemini 2.5 Flash or wait for quota reset.
- **`SAFETY_BLOCKED`**: If response generation is blocked by safety filters (`HARM_CATEGORY_*`), report the category to the user and adjust prompt phrasing or safety thresholds.
