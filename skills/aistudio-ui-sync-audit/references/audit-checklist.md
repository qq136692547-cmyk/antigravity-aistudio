# Google AI Studio UI Sync Audit Checklist

Last calibration date: 2026-11-22

This reference defines the 7 canonical audit surfaces, accessibility and visual inspection checkpoints, active **Gemini 4** model inventory, and deprecation pruning rules for keeping the `antigravity-aistudio` plugin synchronized with the live Google AI Studio web application (`https://aistudio.google.com/`).

## The 7 Canonical Audit Surfaces

Every periodic maintenance audit must systematically inspect each of the following 7 canonical surfaces using the browser subagent in strictly read-only mode:

### 1. Dashboard / Navigation (`https://aistudio.google.com/`)
- **Inspection Focus**: Main landing route, fast-path authentication indicators, top navigation bar, and primary call-to-action buttons.
- **Key UI Elements**:
  - User profile avatar / account menu in top right header.
  - `+ Create prompt` or `Create prompt` primary button.
  - `Get API key` link or button in the left sidebar / top navigation.
  - Left navigation drawer items (Prompts, Tune, API keys, Documentation).
  - Absence of logged-out banner or `Sign in` redirect button.

### 2. Prompt Editor (`https://aistudio.google.com/prompts/new_chat`, `/prompts/new_freeform`)
- **Inspection Focus**: Prompt composer, message input textarea, token count gauge (`1M` window), and media attachment controls.
- **Key UI Elements**:
  - Chat turn composer / input field with semantic placeholder text.
  - Live token count gauge displaying input and context tokens (up to `1,000,000`).
  - Attachment icon / file upload button for multimodal assets.
  - `Run` button (`Ctrl+Enter` shortcut indicator) and stop button during stream generation.
  - Model response rendering container and Markdown formatting blocks.

### 3. Model Selector & Parameter Tuning (`Run settings` & `Tools` Drawer)
- **Inspection Focus**: Active Gemini 4 model inventory, `Thinking level`, `Output length`, `Media resolution`, `Safety settings`, `Add stop sequence`, and `Tools` panel.
- **Key UI Elements**:
  - Model dropdown picker listing authorized Gemini 4 models (`Gemini 4 Hydrogen`, `Gemini 4 Argon`, `Gemini 4 Neon`, `Gemini 4 Carbon`) and any `Unlock Gemini 4 Carbon` paid gate badge.
  - `Thinking level` dropdown (verify Web UI defaults: `Hydrogen`/`Neon` vs `Argon`/`Carbon` defaulting to `Medium`, confirming plugin must switch to `High`). Confirm legacy `Temperature`, `Top-P`, `Top-K`, and `Thinking budget` sliders remain absent on Gemini 4.
  - `Output length` numeric limit (`65536` for Hydrogen/Neon, `32768` for Argon/Carbon).
  - `Media resolution` selector (`Default`, `Low`, `Medium`, `High`).
  - `Safety settings` modal with thresholds across the 4 harm categories (`Harassment`, `Hate Speech`, `Sexually Explicit`, `Dangerous Content`).
  - `Add stop sequence` input control.
  - `Tools` toggles: `Structured outputs` (JSON Schema), `Code execution`, `Function calling` (verify auto-disable behavior when `Grounding with Google Search` is active), `Grounding with Google Search` (default on in Gemini 4), and `URL context`.

### 4. System Instructions (Accordion Panel)
- **Inspection Focus**: Global system instructions input area and persistence across prompt modes.
- **Key UI Elements**:
  - Expandable / collapsible System Instructions drawer or accordion header.
  - Textarea supporting multi-line instructions, persona framing, and formatting directives.
  - Visual indicator showing whether system instructions are populated or empty.

### 5. Structured Prompts & Few-Shot Tables (`https://aistudio.google.com/prompts/new_structured`)
- **Inspection Focus**: Tabular few-shot example builder, column definitions, test case runner, and `Structured outputs` JSON schema editor.
- **Key UI Elements**:
  - Column header row with editable input/output column names and type selectors.
  - Example row editor with `+ Add example` button.
  - Test prompt section with `Run all test cases` button.
  - `Structured outputs` / response format selector for JSON Schema mode.
  - Inline JSON schema editor with validation status badges.
  - CSV import / export action buttons.

### 6. Get Code Dialog & Export (`Get code` Modal)
- **Inspection Focus**: Code generation modal, supported programming languages, SDK conventions, `thinking_level` config, and snippet accuracy.
- **Key UI Elements**:
  - `Get code` trigger button in the prompt editor action bar.
  - Modal dialog with language selection tabs (Python, JavaScript/TypeScript, cURL, REST).
  - Code snippet text display area with one-click `Copy code` button.
  - SDK import statements (confirming `google-genai` for Python and `@google/genai` for JS/TS) and `thinking_level` emission (`"high"` / `"xhigh"`).
  - API key placeholder convention (verifying `GEMINI_API_KEY` environment variable usage).

### 7. Prompt Library & Assets (`https://aistudio.google.com/prompts`)
- **Inspection Focus**: Saved prompt management, version history, folder organization, and API key management view (`/apikey`).
- **Key UI Elements**:
  - Prompt list / grid view showing saved prompts, last modified timestamps, and target model tags.
  - Search and filter bar for finding prompts by name or tag.
  - Row action menus (Rename, Duplicate, Delete).
  - API key management interface at `/apikey` showing active keys, project associations, and creation dates.

## Active Model Inventory

The following **Gemini 4** models are verified active in Google AI Studio as of `2026-11-22`:

| Model Identifier | Display Name | Context & Output | Tier / Gate | Status & Thinking Policy |
| :--- | :--- | :--- | :--- | :--- |
| `gemini-4-hydrogen` | `Gemini 4 Hydrogen` | 1M in / 64K (`65536`) out | Free & Paid (Default) | Active -- Default on `/prompts/new_chat`; enforce `Thinking level = High` |
| `gemini-4-argon` | `Gemini 4 Argon` | 1M in / 32K (`32768`) out | Pro / Paid | Active -- UI defaults to `Medium`; MUST switch `Thinking level` to `High` |
| `gemini-4-neon` | `Gemini 4 Neon` | 1M in / 64K (`65536`) out | Pro / Paid | Active -- Flagship 64K output; enforce `Thinking level = High` |
| `gemini-4-carbon` | `Gemini 4 Carbon` | 1M in / 32K (`32768`) out (multi-turn to 1M) | **Paid Gated** (Ultra / Paid API Key) | Active (Paid Gate) -- UI defaults to `Medium`; MUST switch to `High`; fallback to Neon/Hydrogen if `Unlock Gemini 4 Carbon` appears |

## Semantic & Accessibility Inspection Guidelines

When driving the browser subagent during a sync audit:
1. Prefer semantic HTML roles and accessible labels over brittle CSS class selectors:
   - Use role targets such as `button[name='Create prompt']`, `combobox[name='Model']`, `tab[name='Python']`.
   - Inspect aria labels, tooltips, and visible text content.
2. If class names appear obfuscated (e.g., Angular or WebComponent dynamic hashes), rely on DOM structure, text matching, and visual relative positioning.
3. Record visual observations and DOM snapshots to verify that interface labels match plugin documentation.

## Deprecation Pruning Guidelines

Keep the plugin lean and prevent agents from executing stale or broken workflows:
1. **Identify Deprecated Features**:
   - Flag any models marked with deprecation badges (e.g., `Leaving soon`, `Retiring on <date>`).
   - Flag any UI menus, buttons, or subpaths that redirect to new interfaces or return 404.
2. **Prune Obsolete Models & Controls**:
   - Immediately remove or blacklist all retired pre-Gemini-4 models (`PaLM 2`, `Gemini 1.0`, `Gemini 1.5`, `Gemini 2.0`, `Gemini 2.5` including `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-flash-thinking`, and `Gemini 3.x` including `gemini-3-flash-preview`, `gemini-3.1-pro-preview`, `gemini-3.8-flash`) from plugin rules, skills, and decision matrices.
   - Remove deprecated `Temperature`, `Top-P`, `Top-K`, and `Thinking budget` sliders where superseded by Gemini 4 `Run settings` (`Thinking level`, `Output length`, `Media resolution`, `Add stop sequence`) and `Tools` (`URL context`, `Structured outputs`, `Grounding with Google Search`, `Code execution`, `Function calling`).
3. **Patch Drifted Selectors**:
   - Update navigation steps in skills when AI Studio relocates controls (e.g., if a settings drawer becomes a modal or moves to a different tab).
4. **Update Calibration Date**:
   - Record the new audit timestamp (`YYYY-MM-DD`) in this checklist after completing every verification pass.
