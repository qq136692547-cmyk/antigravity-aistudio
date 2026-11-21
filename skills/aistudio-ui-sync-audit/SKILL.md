---
name: aistudio-ui-sync-audit
description: Strictly read-only maintenance skill auditing live Google AI Studio surfaces to detect UI drift, model updates, parameter changes, and deprecations without mutating cloud state.
disable-model-invocation: true
---

# AI Studio UI Sync Audit Orchestrator

Perform periodic, strictly read-only audits of the live **Google AI Studio** web application (`https://aistudio.google.com/`) via Antigravity's built-in browser subagent to detect interface drift, newly launched models, renamed buttons, modified parameter ranges, and deprecated features.

> **Important**: This maintenance skill sets `disable-model-invocation: true`. It is designed exclusively for manual or scheduled maintenance inspection and must never automatically trigger during standard creative or offloading workflows.

## Core Principles

1. **Strictly Read-Only Execution**: The browser subagent must never click action buttons that generate text, execute code, modify saved prompts, delete resources, or incur API quota during an audit.
2. **Ground Truth Over Memory**: Never guess UI changes. Base every finding on direct DOM inspection, accessibility tree queries, and visual screen observations from `https://aistudio.google.com/`.
3. **Four-Bucket Drift Classification**: Classify every observed difference into one of 4 buckets:
   - **Added**: Newly launched models, new prompt types, new tool toggles, or new SDK export languages.
   - **Changed**: Renamed buttons, shifted navigation routes, adjusted slider ranges, or altered dialog layouts.
   - **Deprecated**: Models or features displaying upcoming retirement warnings or deprecation badges.
   - **Removed / Obsolete**: Elements previously documented in the plugin that are absent in the live interface.
4. **Zero Non-English Characters**: All updated documentation, skills, and checklists must maintain 100% 7-bit ASCII compliance.

## Workflow

### Step 1: Load Audit Checklist and Baseline

1. Read the baseline configuration in [Audit Checklist](./references/audit-checklist.md).
2. Note the last calibration date and the list of active models.
3. Review the 7 canonical audit surfaces to inspect.

### Step 2: Dispatch Read-Only Browser Subagent

1. Call `invoke_subagent` with `TypeName: "browser"` and `Model: "flash"`, navigating to `https://aistudio.google.com/`.
2. Apply the Fast-Path Authentication Check from `rules/AGENTS.md`:
   - If signed in (user profile avatar visible, "Create prompt" button present, RPC 200), proceed immediately.
   - If redirected to `accounts.google.com`, pause and notify the user with `LOGIN_REQUIRED`.
3. Instruct the browser subagent to perform strictly read-only visual inspection across all 7 canonical surfaces:
   - **Surface 1: Dashboard / Navigation** (`https://aistudio.google.com/`): Check landing page elements, top header, left navigation sidebar items, and "Get API key" link.
   - **Surface 2: Prompt Editor** (`/prompts/new_chat`): Inspect message composer, token count gauge location, media attachment button, and run/stop controls.
   - **Surface 3: Model Selector & Parameter Tuning**: Open settings drawer, verify model dropdown options, check Temperature slider range (`[0.0, 2.0]`), Top-P (`[0.0, 1.0]`), Top-K (`[1, 100]`), thinking budget slider, safety categories, and tool toggles (Search Grounding, Python Code Execution).
   - **Surface 4: System Instructions**: Inspect system instructions accordion panel and multi-line editor textarea.
   - **Surface 5: Structured Prompts & Few-Shot Tables** (`/prompts/new_structured`): Inspect table column headers, example row editor, test case runner, JSON schema response format options, and CSV import/export buttons.
   - **Surface 6: Get Code Dialog & Export**: Open "Get code" dialog, inspect available language tabs (Python `google-genai`, TypeScript/JavaScript `@google/genai`, cURL, REST), and verify API key environment variable placeholders.
   - **Surface 7: Prompt Library & Assets** (`/prompts`, `/apikey`): Inspect prompt library table, search/filter controls, and API key management view.

### Step 3: Produce Structured Drift Diff Report

Compare the live observations against current plugin files (`rules/AGENTS.md`, `skills/`, `plugin.json`, `README.md`) and generate a structured report:

```markdown
# AI Studio UI Sync Audit Report

- **Audit Timestamp**: YYYY-MM-DD
- **Inspected URL**: https://aistudio.google.com/
- **Surfaces Inspected**: 7 of 7 canonical surfaces
- **Status**: PASSED (Read-only)

## Drift Diff Summary

### Added
- [Item or None detected]

### Changed
- [Item or None detected]

### Deprecated
- [Item or None detected]

### Removed / Obsolete
- [Item or None detected]
```

### Step 4: Patch and Prune Plugin Files

If UI drift was detected:
1. Update `skills/` files to reflect new button names, navigation paths, or parameter controls.
2. Prune deprecated models or removed features from `rules/AGENTS.md`, `skills/aistudio-offload/references/offload-decision-matrix.md`, and skills documentation.
3. Update [Audit Checklist](./references/audit-checklist.md) with the new calibration date and updated model inventory.
4. Run the test suite to confirm zero regressions and verify 100% 7-bit ASCII compliance.
