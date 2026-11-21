# Antigravity Google AI Studio (`antigravity-aistudio`)

An open-source Antigravity plugin that packages **Google AI Studio** ([aistudio.google.com](https://aistudio.google.com)) as an intelligent cloud agent offload platform, powered by Antigravity's built-in `browser` subagent. Offload compute-intensive reasoning, multi-million token context analysis, prompt tuning, and code generation to Google AI Studio's cloud frontier models, conserving Antigravity desktop app model quota for local development tasks.

---

## 1. Overview & Value Proposition

### The Problem: Local Desktop Quota Depletion
When working in modern AI IDEs like Antigravity, desktop agent interactions consume metered, rate-limited local model quota (e.g., Gemini Neon, Gemini Hydrogen, Gemini Argon, Claude Opus). Performing long-context analysis (such as reading 500k-token repository documentations or massive log files), iterative few-shot prompt tuning, or deep multi-turn architectural brainstorming through the desktop agent quickly exhausts valuable daily quota allowances.

### The Solution: Cloud Agent Offloading
`antigravity-aistudio` solves this bottleneck by establishing an automated cloud offloading bridge to **Google AI Studio**:
- **Frontier Cloud Models**: Direct web access to Gemini 2.5 Pro (up to 2M tokens context window), Gemini 2.5 Flash, and Gemini Flash Thinking directly inside Google AI Studio.
- **Desktop Quota Conservation**: Heavy reasoning, high-token reading, and exploratory iteration execute entirely in the cloud at zero desktop quota cost.
- **Zero Local Daemons**: Driven via Antigravity's lightweight built-in `browser` subagent (`Model: "flash"`). No local Playwright server, Selenium drivers, or external MCP daemons are required.
- **Seamless Local Sync**: Context and files are staged to the browser sandbox, processed in Google AI Studio, and automatically retrieved and synchronized back to your local codebase.

---

## 2. Architecture & System Layers

`antigravity-aistudio` is structured across three core architectural layers:

```
antigravity-aistudio/
|-- plugin.json                          # Plugin manifest conforming to agent-plugins schema
|-- README.md                            # Comprehensive user & developer documentation
|-- assets/
|   `-- logo.svg                         # Official plugin vector logo
|-- rules/
|   `-- AGENTS.md                        # Always-on operating rules & offload decision engine
`-- skills/
    |-- aistudio-offload/                # Master offload orchestrator & decision router
    |   |-- SKILL.md
    |   `-- references/
    |       `-- offload-decision-matrix.md
    |-- aistudio-chat-prompt/            # Conversational prompts & system instructions
    |   `-- SKILL.md
    |-- aistudio-structured-prompt/      # Tabular few-shot prompting & JSON schemas
    |   `-- SKILL.md
    |-- aistudio-parameter-tuning/       # Hyperparameters, safety filters & grounding
    |   `-- SKILL.md
    |-- aistudio-code-export/            # Production SDK code export (Python/TS/cURL)
    |   `-- SKILL.md
    `-- aistudio-ui-sync-audit/          # Read-only live UI drift & model sync audit
        |-- SKILL.md
        `-- references/
            `-- audit-checklist.md
```

### Layer Breakdown
1. **Plugin Foundation Layer**: Defines plugin identity, metadata, branding, and standard agent operating rules in `rules/AGENTS.md`.
2. **Modular Skills Layer**: Six focused skills that automate specific Google AI Studio workflows and manage cloud-to-local data flow.
3. **Verification & Testing Layer**: Multi-tiered test suite ensuring manifest compliance, rule adherence, decision routing accuracy, and clean internationalization.

---

## 3. Quick Start & Installation

### Installation from GitHub (Recommended)

```bash
agy plugin install https://github.com/qq136692547-cmyk/antigravity-aistudio
```

### Local Development (Symlink)

```bash
git clone https://github.com/qq136692547-cmyk/antigravity-aistudio.git
ln -s "$(pwd)/antigravity-aistudio" ~/.gemini/config/plugins/antigravity-aistudio
```

### Manifest Validation

Validate plugin syntax and directory structure locally:

```bash
agy plugin validate . --strict
```

Once installed, enable or customize the plugin on Antigravity's Plugin Management page.

---

## 4. Workload Offload Decision Framework

The plugin includes an intelligent decision engine that automatically classifies developer tasks into **Local Execution** or **Cloud Offload Candidates**.

### Workload Partitioning Matrix

| Workload Category | Execution Target | Criteria & Typical Operations |
| :--- | :--- | :--- |
| **Codebase Modifications** | **Local Machine** | File edits, multi-file refactoring, code formatting, patch application. |
| **Git Operations** | **Local Machine** | `git status`, `git diff`, staging, branching, committing, pushing. |
| **Test Execution** | **Local Machine** | Running `pytest`, `npm test`, `cargo test`, linters, and type checkers. |
| **System Commands** | **Local Machine** | Terminal execution, build compilation, OS diagnostic scripts. |
| **Quick Refactoring** | **Local Machine** | Local edits under 50 lines or trivial parameter renames. |
| **Long-Context Analysis** | **Cloud (AI Studio)** | Analyzing multi-file logs, documentation repositories, or transcripts exceeding 32k tokens. |
| **Deep Reasoning & Design** | **Cloud (AI Studio)** | Architectural tradeoff analysis, algorithm synthesis, design brainstorming. |
| **Few-Shot Prompt Engineering**| **Cloud (AI Studio)** | Calibrating system instructions, tabular input/output pairs, and few-shot examples. |
| **Structured Output Testing** | **Cloud (AI Studio)** | Refining and validating complex JSON schemas and constrained decoding. |
| **Model Comparison** | **Cloud (AI Studio)** | Evaluating prompts across Gemini 2.5 Pro, Flash, and Flash Thinking models. |
| **Synthetic Data Generation** | **Cloud (AI Studio)** | Generating batch test fixtures, mock data, or synthetic corpora. |
| **Production Code Export** | **Cloud (AI Studio)** | Converting tuned prompts into runnable Python, TypeScript, or cURL code. |

### End-to-End Offload Pipeline

```
[Local Workspace] --> [Staging: browser_sandbox/uploads] --> [Browser Subagent]
                                                                     |
                                                                     v
[Local Workspace] <-- [Extract: browser_sandbox/downloads] <-- [Google AI Studio]
```

1. **Evaluate**: Task is matched against the decision matrix.
2. **Stage**: Local context and files are copied to the browser sandbox staging area.
3. **Dispatch**: The built-in `browser` subagent opens `https://aistudio.google.com/` directly.
4. **Execute**: Cloud models process prompts with full context window and tools enabled.
5. **Extract**: Responses, schemas, and exported code are retrieved into the sandbox.
6. **Synchronize**: Artifacts are validated and merged back into the local workspace.

---

## 5. Autonomy Modes

`antigravity-aistudio` operates under two distinct autonomy modes:

### Checkpoint Mode (Default)
In `checkpoint` mode, the agent prepares prompts, selects models, stages files, and formulates the offload plan, but **pauses and requests user approval** before submitting prompts or triggering exports in Google AI Studio. This gives developers complete oversight over prompt content and execution flow.

### Auto Mode (Full-Auto)
In `auto` mode, the agent runs the offload lifecycle end-to-end without per-step confirmation: navigating the UI, configuring model parameters, submitting queries, extracting results, and writing files back to the workspace automatically.

### Triggering Auto Mode
Mention unattended cues anywhere in your prompt:
- `"auto mode"` / `"full-auto"`
- `"run unattended"`
- `"without asking for confirmation"`
- `"batch offload to AI Studio"`

You can switch modes at any point during a conversation by replying `"switch to auto mode"` or `"switch to checkpoint mode"`.

---

## 6. Modular Skills Suite Overview

The plugin provides six dedicated skills covering the entire Google AI Studio surface:

| Skill | Purpose | Mode / Model Invocation |
| :--- | :--- | :--- |
| **`aistudio-offload`** | Master cloud offload coordinator evaluating tasks against the decision matrix and syncing results. | Standard |
| **`aistudio-chat-prompt`** | Orchestrating multi-turn chat prompts, system instructions, and file attachments in `/prompts/new_chat`. | Standard |
| **`aistudio-structured-prompt`** | Tabular few-shot prompting, input/output column configuration, and JSON schema outputs in `/prompts/new_structured`. | Standard |
| **`aistudio-parameter-tuning`** | Fine-tuning temperature, top-p, top-k, thinking budget, safety thresholds, search grounding, and code execution. | Standard |
| **`aistudio-code-export`** | Exporting production-ready client code (Python, TypeScript, cURL, REST) via the `Get code` dialog. | Standard |
| **`aistudio-ui-sync-audit`** | Read-only live UI audit across 7 canonical AI Studio surfaces to detect new features or model deprecations. | Manual (`disable-model-invocation: true`) |

---

## 7. Sandbox & Asset Staging Architecture

Antigravity's `browser` subagent runs inside a sandboxed environment with strict filesystem boundaries:
- **Upload Staging (`browser_sandbox/uploads/`)**: Any local files, datasets, or images meant for AI Studio prompt attachments are copied here with single-segment filenames before handing off to the browser subagent.
- **Reference Inspection (`browser_sandbox/references/`)**: Visual assets and UI snapshots are stored here for multi-modal inspection.
- **Download Retrieval (`browser_sandbox/downloads/`)**: Code snippets, exported JSON files, and prompt archives downloaded from AI Studio land here before being integrated into your project.

---

## 8. Security & Boundary Handling

The plugin enforces strict safety stops and never compromises security:
- **Fast-Path Authentication**: Detects active signed-in sessions via avatar, recent prompts, and RPC signals without reading forbidden cookie stores.
- **Google Sign-In Pause (`LOGIN_REQUIRED`)**: The agent never attempts to automate password entry or credentials. If logged out, it pauses and invites the user to sign in manually.
- **CAPTCHA & Bot Detection (`CAPTCHA_REQUIRED`)**: Never attempts to bypass verification challenges; immediately hands control to the user.
- **Rate Limits & Quota Exhaustion (`429 ResourceExhausted`)**: Catches quota barriers, reports them clearly, and offers model fallback (e.g., falling back to Gemini Flash).
- **Safety Blocks (`HARM_CATEGORY_*`)**: Intercepts content safety blocks, reporting specific categories and enabling parameter or prompt adjustment.

---

## License

Apache-2.0. Developed by the Antigravity Team.
