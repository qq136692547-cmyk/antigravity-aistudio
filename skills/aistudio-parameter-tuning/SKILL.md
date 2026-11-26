---
name: aistudio-parameter-tuning
description: Gemini 4 Run settings and Tools configuration in Google AI Studio covering Thinking level (floor >= High), Output length, Media resolution, Safety settings, Add stop sequence, Structured outputs, Code execution, Function calling, Grounding with Google Search, and URL context.
---

# AI Studio Parameter Tuning Orchestrator

Calibrate **Gemini 4** `Run settings` and `Tools` in **Google AI Studio** (`https://aistudio.google.com/`) to enforce reasoning depth (`Thinking level >= High`), output limits, media fidelity, safety filter thresholds, and grounded execution tools.

> **Gemini 4 UI Alignment Notice**: Google AI Studio's `Run settings` drawer for Gemini 4 has removed/hidden legacy `Temperature`, `Top-P`, `Top-K`, and numeric `Thinking budget` sliders. Behavior is governed directly by `Thinking level`, `Output length`, `Media resolution`, `Safety settings`, `Add stop sequence`, and the `Tools` panel.

## When to Use

- The user needs to select an authorized **Gemini 4** model and enforce **`Thinking level = High`** (Web UI) or `"high"` / `"xhigh"` (SDK/API `thinking_level`).
- The user wants to configure `Output length` (up to `65536` or `32768` tokens), `Media resolution`, or custom `Add stop sequence` strings.
- The user needs to relax or tighten content `Safety settings` across the 4 harm categories.
- The user wants to toggle `Tools` (`Structured outputs`, `Code execution`, `Function calling`, `Grounding with Google Search`, or `URL context`).

## Supported Models, Run Settings, and Tools

### 1. Authorized Gemini 4 Model Selection

Select one of the four authorized **Gemini 4** models (unified `1M` / `1,000,000` input context; **pre-Gemini-4 models are strictly prohibited**):

| Model | Context / Max Output | Tier / Gate | Web UI Default Thinking | Required Action |
| :--- | :--- | :--- | :--- | :--- |
| **`Gemini 4 Hydrogen`** (`gemini-4-hydrogen`) | 1M in / 64K (`65536`) out | Free & Paid (Default) | `High` | Verify `Thinking level = High`. |
| **`Gemini 4 Argon`** (`gemini-4-argon`) | 1M in / 32K (`32768`) out | Pro / Paid | `Medium` | **Explicitly switch `Thinking level` to `High`.** |
| **`Gemini 4 Neon`** (`gemini-4-neon`) | 1M in / 64K (`65536`) out | Pro / Paid | `High` | Verify `Thinking level = High`. |
| **`Gemini 4 Carbon`** (`gemini-4-carbon`) | 1M in / 32K (`32768`) out | **Paid Gated** | `Medium` | **Explicitly switch `Thinking level` to `High`**; pause & offer Neon/Hydrogen fallback if `Unlock Gemini 4 Carbon` appears. |

### 2. Gemini 4 Run Settings Controls

| Control | Valid Values / Range | Default | Policy & Recommended Setting |
| :--- | :--- | :--- | :--- |
| **Thinking level** | Web UI: `High` (SDK/API: `"high"`, `"xhigh"`) | `High` (Hydrogen/Neon), `Medium` (Argon/Carbon) | **Floor `>= High`**: Web UI MUST be set to `High`; SDK/API allows `"high"` or `"xhigh"`. **`Low` and `Medium` are strictly forbidden.** |
| **Output length** | `1` to `65536` (Hydrogen/Neon), `1` to `32768` (Argon/Carbon) | Model max (`65536` / `32768`) | Keep at `65536` (or `32768` on Argon/Carbon) for full-repo reviews and long code exports; cap lower only for concise schemas. |
| **Media resolution** | `Default`, `Low`, `Medium`, `High` | `Default` | Set `High` for dense UI screenshots, diagrams, and fine-print PDFs; `Low` / `Medium` for coarse video frame scanning. |
| **Add stop sequence** | String list | Empty | Add custom stop delimiters (e.g., `END_JSON`) when truncating structured templates. |

### 3. Safety Settings Thresholds

Google AI Studio provides 4 adjustable safety categories under `Safety settings`:
- **Harassment** (`HARM_CATEGORY_HARASSMENT`)
- **Hate Speech** (`HARM_CATEGORY_HATE_SPEECH`)
- **Sexually Explicit** (`HARM_CATEGORY_SEXUALLY_EXPLICIT`)
- **Dangerous Content** (`HARM_CATEGORY_DANGEROUS_CONTENT`)

Each category supports 4 threshold levels:
- **`BLOCK_NONE`** (`Block None`): Do not block content based on this category (with appropriate account verification).
- **`BLOCK_ONLY_HIGH`** (`Block Few`): Block only high-probability harm content.
- **`BLOCK_MEDIUM_AND_ABOVE`** (`Block Some`, Default): Block medium- and high-probability harm content.
- **`BLOCK_LOW_AND_ABOVE`** (`Block Most`): Strictly block low-, medium-, and high-probability harm content.

### 4. Tools Panel (Gemini 4 Capabilities)

- **`Structured outputs`**: Enforce strict JSON Schema decoding directly in chat prompt or `/prompts/new_structured`.
- **`Code execution`**: Sandboxed Python execution for symbolic math, algorithmic checks, and data transformation.
- **`Function calling`**: Custom tool/function declarations (**Note: automatically disabled when `Grounding with Google Search` is enabled**).
- **`Grounding with Google Search` (Audit & Research Policy)**: Real-time web search and inline URL citations. **Explicitly inspect `Tools` and verify/toggle it ON (`aria-checked="true"`) for Stage 1 research/architecture planning and all Stage 3 `git diff`/code audits** (live UI/model switches can leave it `OFF`, and ungrounded audits miss live spec checks). Toggle it **OFF** (`aria-checked="false"`) only when **`Function calling`** is required (Search disables Function calling) or for purely offline copywriting / JSON schema tasks.
- **`URL context`**: Directly fetches and reads URLs included in the prompt. Because AI Studio blocks or flags any prompt containing `http(s)://` strings when `URL context` is OFF, toggle it **ON** (`aria-checked="true"`) proactively whenever ANY URL appears in the prompt/diff (and click **`Enable URL Context`** + re-run if the inline banner appears).

## Workflow

### Step 1: Open Run Settings Drawer in AI Studio

1. In `/prompts/new_chat` or `/prompts/new_structured`, locate the **Run settings** panel in the right sidebar.
2. Verify the selected model is an authorized **Gemini 4** model (`Hydrogen`, `Argon`, `Neon`, or `Carbon`).
3. If `Unlock Gemini 4 Carbon` paywall appears, pause immediately (`PAID_TIER_REQUIRED`) and offer fallback to `Gemini 4 Neon (High)` or `Gemini 4 Hydrogen (High)`.

### Step 2: Enforce Thinking Level >= High & Calibrate Run Settings

1. **Set `Thinking level` to `High`**: Open the `Thinking level` dropdown and explicitly verify or select **`High`** (mandatory on `Argon` and `Carbon`, which default to `Medium`). Never leave `Thinking level` on `Low` or `Medium`.
2. **Set `Output length`**: Verify `Output length` fits the task (`<= 65536` for Hydrogen/Neon, `<= 32768` for Argon/Carbon).
3. **Set `Media resolution`**: Choose `High` for high-detail images/PDFs or `Default` for text-only tasks.
4. **Configure `Add stop sequence`**: Add stop sequences if deterministic delimiter stopping is needed.

### Step 3: Configure Safety Filter Settings

1. Click **Safety settings** in the `Run settings` sidebar.
2. Inspect current thresholds across all 4 harm categories (`Harassment`, `Hate Speech`, `Sexually Explicit`, `Dangerous Content`).
3. Adjust thresholds according to task requirements (e.g., `BLOCK_ONLY_HIGH` for security vulnerability research) and save.

### Step 4: Configure Tools Panel

1. Under **Tools** in the right sidebar:
   - Toggle **Structured outputs** and supply JSON Schema when strict JSON is needed.
   - Configure **Grounding with Google Search**: explicitly inspect and ensure it is **ON** (`aria-checked="true"`) for Stage 1 architecture/research and all Stage 3 `git diff`/code audits; toggle it **OFF** (`aria-checked="false"`) only when **Function calling** is required (Search disables Function calling) or for purely offline copywriting/JSON schema runs.
   - Enable **URL context** (`aria-checked="true"`) proactively before clicking `Run` whenever the prompt or pasted code/diff contains ANY `http://` or `https://` literal (and click **`Enable URL Context`** + re-run if the inline prompt card appears).
   - Enable **Code execution** for mathematical or algorithmic verification.

### Step 5: Test and Verify Parameter Behavior

1. Execute test prompts and confirm:
   - `Thinking level = High` reasoning traces / deep synthesis behave as expected.
   - `Grounding with Google Search` / `URL context` return grounded citations and fetched page details.
   - `Code execution` displays executed Python blocks and standard output.
2. Document the calibrated Gemini 4 configuration in project documentation or exported SDK code.
