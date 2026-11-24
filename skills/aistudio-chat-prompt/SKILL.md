---
name: aistudio-chat-prompt
description: Multi-turn conversational prompt orchestration in Google AI Studio with Gemini 4 (1M context, Thinking level >= High), system instructions, token gauge monitoring, multimodal attachments, URL context, and Markdown history export.
---

# AI Studio Chat Prompt Orchestrator

Design, execute, and manage multi-turn conversational dialogue sessions in **Google AI Studio** (`https://aistudio.google.com/prompts/new_chat`) on **Gemini 4** models (`Thinking level = High`) to offload interactive reasoning, customer simulation, and context-rich back-and-forth prompting to cloud models.

## When to Use

- The user wants to conduct a multi-turn conversation or interview simulation with `Gemini 4 Hydrogen`, `Gemini 4 Argon`, `Gemini 4 Neon`, or `Gemini 4 Carbon`.
- The user needs to test and refine persistent system instructions across multiple dialogue turns.
- The user wants to analyze multimodal attachments (images, audio recordings, video clips, PDFs) with calibrated `Media resolution` or live webpages via `URL context`.
- The user wants to export a completed cloud chat history transcript back into local Markdown workspace files.

## Workflow

### Step 1: Initialize Chat Session and Fast-Path Auth

1. Delegate to the `browser` subagent (`TypeName: "browser"`, `Model: "flash"`) targeting `https://aistudio.google.com/prompts/new_chat`.
2. Check for authenticated session indicators:
   - Presence of user profile avatar in the navigation bar.
   - Active chat prompt interface with model selector (defaulting to `Gemini 4 Hydrogen`) and message composer.
   - Absence of login prompts or `accounts.google.com` redirects.
3. If fast-path authentication succeeds, proceed directly to prompt setup without pausing.
4. Maintain the same `browser` subagent session via `send_message` across all conversational turns to preserve tab state and conversation context.

### Step 2: Select Gemini 4 Model and Enforce Thinking Level = High

1. Select the target **Gemini 4** model in `Run settings`:
   - `Gemini 4 Hydrogen` (`1M` in / `64K` out, Free & Paid default)
   - `Gemini 4 Argon` (`1M` in / `32K` out, Pro/Paid -- **switch `Thinking level` from default `Medium` to `High`**)
   - `Gemini 4 Neon` (`1M` in / `64K` out, Pro/Paid)
   - `Gemini 4 Carbon` (`1M` in / `32K` out, Paid gated -- **switch `Thinking level` from default `Medium` to `High`**; if `Unlock Gemini 4 Carbon` paywall appears, pause immediately and offer fallback to `Gemini 4 Neon (High)` or `Gemini 4 Hydrogen (High)`)
2. Verify **`Thinking level = High`** is active in `Run settings`. **`Low` and `Medium` thinking levels are strictly prohibited.**
3. Configure `Output length` (up to `65536` for Hydrogen/Neon or `32768` for Argon/Carbon), `Media resolution` (`Default` / `Low` / `Medium` / `High`), `Add stop sequence`, and **On-Demand `Tools`** (`Structured outputs`, `Code execution`, `Function calling`, `Grounding with Google Search` -- explicitly inspect and toggle **OFF** (`aria-checked="false"`) for internal-only tasks since live UI may default it ON; enable **ON** only for live web queries -- and `URL context` when URLs are supplied).

### Step 3: Configure System Instructions

1. Locate the **System Instructions** expandable panel in the chat editor.
2. If the user provided custom persona guidelines, operational constraints, or formatting rules, expand the panel and input the system instructions.
3. Confirm system instructions are saved and active in the editor session.

### Step 4: Stage and Upload Multimodal Attachments

If the conversation involves local files (images, audio, video, documents):
1. Copy each local asset to the staging folder:
   `<Artifact Directory Path>/browser_sandbox/uploads/<filename>`
2. Supported attachment file formats:
   - Images: `.png`, `.jpg`, `.jpeg`, `.webp`
   - Audio: `.mp3`, `.wav`
   - Video: `.mp4`
   - Documents: `.pdf`, `.txt`, `.csv`
3. Click the attachment / file upload button in the AI Studio chat composer.
4. Pass the bare single-segment filename from the staging folder to attach the media asset to the conversation turn.

### Step 5: Execute Conversational Turns and Monitor Token Gauge

For each user message in the dialogue sequence:
1. Input the user prompt into the chat composer textarea.
2. In `checkpoint` mode (default), present the proposed turn, Gemini 4 model (`Thinking level: High`), and media attachments to the user before submitting. In `auto` mode, submit directly.
3. Respect the **15-30s randomized pacing cooldown** between consecutive turns, submit the turn (click `Run` / `Send` or press `Ctrl+Enter`), and stay within the **5-8 calls/session** anti-abuse soft budget.
4. Monitor the live token gauge in the footer or header:
   - Note input token count and accumulated history tokens.
   - Ensure the total token count stays within the unified `1,000,000` (`1M`) token context window across all Gemini 4 models.
5. Wait for the model response stream to finish rendering.
6. Inspect response for account verification gates (`ACCOUNT_VERIFICATION_REQUIRED` / `aistudio.google.com/verify-account` -- zero-retry immediate halt and local fallback), safety blocks (`HARM_CATEGORY_*`), paid gates (`Unlock Gemini 4 Carbon`), or quota errors (`429 ResourceExhausted`).

### Step 6: Export Chat History to Local Markdown

Once the conversational session concludes:
1. Extract the full conversation history from the AI Studio chat container:
   - All user turns with prompt text and media attachment labels.
   - All model responses with formatted text, code blocks, and reasoning citations.
2. Format the dialogue as a structured Markdown document:

```markdown
# AI Studio Chat Transcript

- **Date**: YYYY-MM-DD
- **Target URL**: https://aistudio.google.com/prompts/new_chat
- **Model**: Gemini 4 Hydrogen / Argon / Neon / Carbon
- **Thinking Level**: High
- **System Instructions**: <Configured system instructions>

## Turn 1
**User**:
<User prompt>

**Model**:
<Model response>
```

3. Save the transcript to `<Artifact Directory Path>/browser_sandbox/downloads/chat_transcript.md`.
4. Synchronize the transcript to the destination workspace path (e.g., `docs/chat_transcript.md`).
5. Confirm the exported file is clean, well-formatted, and completely synchronized.
