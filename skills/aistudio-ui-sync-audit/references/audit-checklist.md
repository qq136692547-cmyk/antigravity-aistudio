# Google AI Studio UI Sync Audit Checklist

Last calibration date: 2026-11-21

This reference defines the 7 canonical audit surfaces, accessibility and visual inspection checkpoints, active model inventory, and deprecation pruning rules for keeping the `antigravity-aistudio` plugin synchronized with the live Google AI Studio web application (`https://aistudio.google.com/`).

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
- **Inspection Focus**: Prompt composer, message input textarea, token count gauge, and media attachment controls.
- **Key UI Elements**:
  - Chat turn composer / input field with semantic placeholder text.
  - Live token count gauge displaying input and context tokens.
  - Attachment icon / file upload button for multimodal assets.
  - `Run` button (`Ctrl+Enter` shortcut indicator) and stop button during stream generation.
  - Model response rendering container and Markdown formatting blocks.

### 3. Model Selector & Parameter Tuning (Settings Drawer)
- **Inspection Focus**: Active model inventory, generation sliders, safety filter thresholds, and tools toggles.
- **Key UI Elements**:
  - Model dropdown picker listing currently available Gemini models.
  - Temperature slider (range `[0.0, 2.0]`) and direct numeric input box.
  - Advanced settings section containing Top-P (`[0.0, 1.0]`) and Top-K (`[1, 100]`) controls.
  - Thinking budget controls (for reasoning models such as Gemini Flash Thinking).
  - Safety settings modal with thresholds across the 4 harm categories.
  - Tool toggles: Google Search Grounding and Python Code Execution.

### 4. System Instructions (Accordion Panel)
- **Inspection Focus**: Global system instructions input area and persistence across prompt modes.
- **Key UI Elements**:
  - Expandable / collapsible System Instructions drawer or accordion header.
  - Textarea supporting multi-line instructions, persona framing, and formatting directives.
  - Visual indicator showing whether system instructions are populated or empty.

### 5. Structured Prompts & Few-Shot Tables (`https://aistudio.google.com/prompts/new_structured`)
- **Inspection Focus**: Tabular few-shot example builder, column definitions, test case runner, and JSON schema editor.
- **Key UI Elements**:
  - Column header row with editable input/output column names and type selectors.
  - Example row editor with `+ Add example` button.
  - Test prompt section with `Run all test cases` button.
  - Response format selector for Structured Output (JSON mode).
  - Inline JSON schema editor with validation status badges.
  - CSV import / export action buttons.

### 6. Get Code Dialog & Export (`Get code` Modal)
- **Inspection Focus**: Code generation modal, supported programming languages, SDK conventions, and snippet accuracy.
- **Key UI Elements**:
  - `Get code` trigger button in the prompt editor action bar.
  - Modal dialog with language selection tabs (Python, JavaScript/TypeScript, cURL, REST).
  - Code snippet text display area with one-click `Copy code` button.
  - SDK import statements (confirming `google-genai` for Python and `@google/genai` for JS/TS).
  - API key placeholder convention (verifying environment variable usage).

### 7. Prompt Library & Assets (`https://aistudio.google.com/prompts`)
- **Inspection Focus**: Saved prompt management, version history, folder organization, and API key management view (`/apikey`).
- **Key UI Elements**:
  - Prompt list / grid view showing saved prompts, last modified timestamps, and target model tags.
  - Search and filter bar for finding prompts by name or tag.
  - Row action menus (Rename, Duplicate, Delete).
  - API key management interface at `/apikey` showing active keys, project associations, and creation dates.

## Active Model Inventory

The following models are verified active in Google AI Studio as of the last calibration date:

| Model Identifier | Context Window | Default Use Case | Status |
| :--- | :--- | :--- | :--- |
| `gemini-2.5-flash` | 1,000,000 tokens | General reasoning, fast drafting, few-shot prompting | Active (Standard) |
| `gemini-2.5-pro` | 2,000,000 tokens | Complex architectural analysis, extreme-context synthesis | Active (Flagship) |
| `gemini-flash-thinking` | 1,000,000 tokens | Deep mathematical derivation, algorithm design | Active (Reasoning) |

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
2. **Prune Obsolete Models**:
   - Immediately remove references to retired models (e.g., PaLM 2, Bison, Gemini 1.0 series) from plugin rules, skills, and decision matrices.
3. **Patch Drifted Selectors**:
   - Update navigation steps in skills when AI Studio relocates controls (e.g., if a settings drawer becomes a modal or moves to a different tab).
4. **Update Calibration Date**:
   - Record the new audit timestamp in this checklist after completing every verification pass.
