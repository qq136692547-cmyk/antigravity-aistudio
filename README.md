# Antigravity Google AI Studio (`antigravity-aistudio`)

<p align="center">
  <img src="assets/hero-banner.png" alt="Antigravity AI Studio Hero Banner" width="100%">
</p>

<p align="center">
  <a href="https://github.com/qq136692547-cmyk/antigravity-aistudio/stargazers"><img src="https://img.shields.io/github/stars/qq136692547-cmyk/antigravity-aistudio?style=for-the-badge&logo=github&color=FFD700" alt="GitHub Stars"></a>
  <a href="plugin.json"><img src="https://img.shields.io/badge/Antigravity-Plugin%20v0.2.0-9B72CB?style=for-the-badge&logo=google" alt="Antigravity Plugin"></a>
  <a href="https://aistudio.google.com"><img src="https://img.shields.io/badge/Frontier%20Models-Gemini%204%20Hydrogen%20%7C%20Argon%20%7C%20Neon%20%7C%20Carbon-4285F4?style=for-the-badge&logo=googlegemini" alt="Gemini 4 Models"></a>
  <a href="https://aistudio.google.com"><img src="https://img.shields.io/badge/Context%20Window-1%2C000%2C000%20Tokens-00C9A7?style=for-the-badge" alt="Context Window"></a>
  <a href="https://aistudio.google.com"><img src="https://img.shields.io/badge/Thinking%20Floor-High%20%2F%20XHigh-FF6B6B?style=for-the-badge" alt="Thinking Floor"></a>
  <a href="tests/run_tests.py"><img src="https://img.shields.io/badge/E2E%20Tests-255%2F255%20Passed-success?style=for-the-badge&logo=checkmarx" alt="Tests"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue?style=for-the-badge" alt="License"></a>
</p>

> **Supercharge Antigravity with Google AI Studio (v0.2.0 -- Pure Gemini 4 Architecture):** Offload heavy reasoning, 1M-token document analysis, few-shot prompt engineering, URL context synthesis, and SDK code exports to **Gemini 4** cloud models (`Thinking level >= High`) through Antigravity's built-in browser subagent -- **preserving 100% of your local IDE model quota.**

---

## 1. Overview & Value Proposition

### The Problem: Local Desktop Quota Depletion
When developing inside AI-first IDEs like Antigravity, desktop agent interactions consume metered, rate-limited local model quota (e.g., Gemini Neon, Gemini Hydrogen, Gemini Argon, Claude Opus). Performing long-context analysis (such as reading 500k-token repository documentation or massive log files), iterative few-shot prompt tuning, or deep multi-turn architectural brainstorming through the desktop agent quickly exhausts valuable daily quota allowances.

### The Solution: Cloud Agent Offloading (Gemini 4 + Thinking >= High)
`antigravity-aistudio` v0.2.0 establishes an automated cloud offloading bridge to **Google AI Studio** ([aistudio.google.com](https://aistudio.google.com)):
- **Pure Gemini 4 Cloud Roster**: Direct web access to `Gemini 4 Hydrogen`, `Gemini 4 Argon`, `Gemini 4 Neon`, and `Gemini 4 Carbon` -- all unified with a `1,000,000` (`1M`) token context window. All pre-Gemini-4 models (`PaLM 2`, `Gemini 1.x`, `2.x`, `3.x`) are retired and blocked.
- **Hard Thinking Level Floor (`>= High`)**: Every cloud offload enforces `Thinking level = High` in the Web UI (`"high"` or `"xhigh"` in SDK/API `thinking_level`). `Low` and `Medium` thinking levels are strictly prohibited, including explicit Medium-to-High overrides for `Argon` and `Carbon`.
- **Desktop Quota Conservation**: Heavy reasoning, high-token reading, and exploratory iteration execute entirely in the cloud at zero desktop quota cost.
- **Zero Local Daemons**: Driven via Antigravity's lightweight built-in `browser` subagent (`Model: "flash"`). No local Playwright server, Selenium drivers, or external MCP daemons are required.
- **Seamless Local Sync**: Context and files are staged to the browser sandbox, processed in Google AI Studio with `Run settings` and `Tools` (`URL context`, `Structured outputs`, `Grounding with Google Search`, `Code execution`), and automatically synchronized back to your local codebase.

### Value Comparison

| Dimension | Standard Desktop Execution | Cloud Offload with `antigravity-aistudio` v0.2.0 |
| :--- | :--- | :--- |
| **Cloud Models** | Desktop metered allowances | **Pure Gemini 4** (`Hydrogen`, `Argon`, `Neon`, `Carbon`) |
| **Context Window** | Limited by desktop model context | **Unified 1,000,000 Tokens** (`1M` in / up to `64K` out) |
| **Thinking Floor** | Varies by local quota | **Enforced `Thinking level >= High`** (`Low`/`Medium` blocked) |
| **Local IDE Quota** | Consumes metered daily allowances | **Zero Desktop Quota Consumed** (Cloud Offload) |
| **External Dependencies** | Heavy local Playwright/Selenium daemons | **Zero Daemons** (Native Browser Subagent) |
| **Workflow Automation** | Manual prompt copying & re-typing | **Automated 6-Stage Lifecycle Pipeline** |
| **Safety & Boundaries** | Complex manual verification | **Fast-Path Auth, Paid Gate & Hard Safety Stops** |

---

## 2. Architecture & System Layers

<p align="center">
  <img src="assets/architecture-offload-pipeline.png" alt="Cloud Agent Offloading Architecture & Pipeline" width="100%">
</p>

`antigravity-aistudio` is structured across three core architectural layers:

```
antigravity-aistudio/
|-- plugin.json                          # Plugin manifest v0.2.0 conforming to agent-plugins schema
|-- README.md                            # Comprehensive user & developer documentation
|-- assets/
|   |-- logo.svg                         # Official plugin vector logo
|   |-- hero-banner.png                  # Cinematic 16:9 hero banner
|   |-- architecture-offload-pipeline.png # High-density Gemini 4 offload pipeline diagram
|   |-- modular-skills-ecosystem.png     # Modular 6-skill capability matrix diagram
|   |-- sponsor-wechat.png               # WeChat Pay sponsorship QR
|   `-- sponsor-usdt.png                 # USDT (BSC) sponsorship QR
|-- rules/
|   `-- AGENTS.md                        # Always-on operating rules, Gemini 4 & Thinking >= High policy
|-- skills/
|   |-- aistudio-offload/                # Master offload orchestrator & decision router
|   |   |-- SKILL.md
|   |   `-- references/
|   |       `-- offload-decision-matrix.md
|   |-- aistudio-chat-prompt/            # Conversational prompts & system instructions
|   |   `-- SKILL.md
|   |-- aistudio-structured-prompt/      # Tabular few-shot prompting & Structured outputs
|   |   `-- SKILL.md
|   |-- aistudio-parameter-tuning/       # Gemini 4 Run settings, Thinking level >= High & Tools
|   |   `-- SKILL.md
|   |-- aistudio-code-export/            # Production SDK code export (Python/TS/cURL/REST)
|   |   `-- SKILL.md
|   `-- aistudio-ui-sync-audit/          # Read-only live UI drift & Gemini 4 sync audit
|       |-- SKILL.md
|       `-- references/
|           `-- audit-checklist.md
|-- scripts/
|   `-- generate_infographics.py         # High-resolution 2K infographic asset generator
`-- tests/                               # 5-Tier E2E automated test suite
```

### System Architecture Flow

```
+-----------------------------------------------------------------------------------+
|                              LOCAL WORKSPACE                                      |
|                                                                                   |
|  [Developer Request] ---> [Offload Decision Engine]                               |
|                                  |                                                |
|             +--------------------+--------------------+                           |
|             | (Local Tasks)                           | (Cloud Offload Candidates)|
|             v                                         v                           |
|      [Local Shell / Git]                    [Browser Staging Area]                |
|      - File refactoring                     browser_sandbox/uploads/              |
|      - Running tests                                  |                           |
|      - Git commits                                    v                           |
|                                            [Browser Subagent (Flash)]             |
+-------------------------------------------------------|---------------------------+
                                                        |
                                                        v (HTTPS / Session Reuse)
+-----------------------------------------------------------------------------------+
|                         GOOGLE AI STUDIO (CLOUD NEXUS)                            |
|                                                                                   |
|      https://aistudio.google.com/                                                 |
|      - Gemini 4 Hydrogen (1M in / 64K out, Free & Paid default)                   |
|      - Gemini 4 Argon    (1M in / 32K out, Pro/Paid, switch Medium -> High)       |
|      - Gemini 4 Neon     (1M in / 64K out, Pro/Paid, repo-scale & multimodal)     |
|      - Gemini 4 Carbon   (1M in / 32K out, Paid gated, switch Medium -> High)     |
|      - Thinking level >= High | Output length | Media resolution | URL context    |
|      - Structured outputs | Search Grounding (default ON) | Code execution        |
+-------------------------------------------------------|---------------------------+
                                                        |
                                                        v (Extracted Outputs)
+-----------------------------------------------------------------------------------+
|                              LOCAL WORKSPACE                                      |
|                                                                                   |
|  [Destination Files] <--- [Local Synchronization] <--- browser_sandbox/downloads/ |
|  - docs/analysis.md       - Validate schemas                                      |
|  - src/model_schema.json  - Sanitize GEMINI_API_KEY & thinking_level >= high      |
|  - scripts/export.py      - Run 5-tier E2E regression tests                       |
+-----------------------------------------------------------------------------------+
```

---

## 3. Quick Start & Installation

### Installation from GitHub (Recommended)

Install directly into Antigravity with one command:

```bash
agy plugin install https://github.com/qq136692547-cmyk/antigravity-aistudio
```

### Manual / Local Installation

#### On Linux / macOS:
```bash
git clone https://github.com/qq136692547-cmyk/antigravity-aistudio.git
ln -s "$(pwd)/antigravity-aistudio" ~/.gemini/config/plugins/antigravity-aistudio
```

#### On Windows (PowerShell):
> **Note:** On Windows, Antigravity's plugin scanner skips NTFS Junctions and symlinks. Clone or copy into a real directory under `$HOME\.gemini\config\plugins\`:

```powershell
# Clone directly into Antigravity's plugins directory
git clone https://github.com/qq136692547-cmyk/antigravity-aistudio.git "$HOME\.gemini\config\plugins\antigravity-aistudio"

# Or copy an existing local clone
Copy-Item -Path "$PWD\antigravity-aistudio" -Destination "$HOME\.gemini\config\plugins\antigravity-aistudio" -Recurse -Force
```

### Manifest Validation

Validate plugin syntax and directory structure locally:

```bash
agy plugin validate . --strict
```

Once installed, manage or toggle the plugin on Antigravity's Customizations page.

---

## 4. Workload Offload Decision Framework & Gemini 4 Roster

The plugin includes an intelligent decision engine that automatically classifies developer tasks into **Local Execution** or **Cloud Offload Candidates** targeting authorized **Gemini 4** models.

### Authorized Gemini 4 Cloud Model Roster (Unified 1M Context)

| Model | API ID | Tier / Gate | Context / Max Output | Thinking Level Policy | Primary Workloads |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`Gemini 4 Hydrogen`** | `gemini-4-hydrogen` | Free & Paid (Default) | 1M in / 64K (`65536`) out | `High` (`"high"` / `"xhigh"`) | Routine long text/logs (4K-1M), JSON schemas, synthetic data, daily prompt iteration |
| **`Gemini 4 Argon`** | `gemini-4-argon` | Pro / Paid | 1M in / 32K (`32768`) out | **Switch Medium -> `High`** | Complex logic debugging, fine-grained engineering, knowledge problem solving |
| **`Gemini 4 Neon`** | `gemini-4-neon` | Pro / Paid | 1M in / 64K (`65536`) out | `High` (`"high"` / `"xhigh"`) | Repo-wide architecture, complex software engineering, multimodal & 64K long outputs |
| **`Gemini 4 Carbon`** | `gemini-4-carbon` | **Paid Gated** (Ultra / Paid API) | 1M in / 32K (`32768`) out | **Switch Medium -> `High`** | Extreme long-horizon reasoning, hardest math/science/architecture; fallback to Neon/Hydrogen if gated |

> **Strict Floor & Pruning Policy**: `Low` and `Medium` thinking levels are prohibited for all cloud offloads. All pre-Gemini-4 models (`PaLM 2`, `Gemini 1.0`, `1.5`, `2.0`, `2.5`, `3.x`) are deprecated and rejected.

### Workload Partitioning Matrix

| Workload Category | Execution Target | Criteria & Typical Operations |
| :--- | :--- | :--- |
| **Codebase Modifications** | **Local Machine** | File edits, multi-file refactoring, code formatting, patch application. |
| **Git Operations** | **Local Machine** | `git status`, `git diff`, staging, branching, committing, pushing. |
| **Test Execution** | **Local Machine** | Running `pytest`, `npm test`, `cargo test`, linters, and type checkers. |
| **System Commands** | **Local Machine** | Terminal execution, build compilation, OS diagnostic scripts. |
| **Quick Refactoring** | **Local Machine** | Local edits under 50 lines or trivial parameter renames. |
| **Long-Context Analysis** | **Cloud (AI Studio)** | Analyzing multi-file logs, docs, or transcripts >= 4,000 tokens (up to 1M tokens) on `Gemini 4 Hydrogen` / `Neon (High)`. |
| **Complex Debugging** | **Cloud (AI Studio)** | Deep root-cause isolation and fine-grained engineering on `Gemini 4 Argon (High)`. |
| **Deep Reasoning & Design** | **Cloud (AI Studio)** | Architectural tradeoff analysis and extreme math/logic proofs on `Gemini 4 Neon` / `Carbon (High)`. |
| **Few-Shot Prompt Engineering** | **Cloud (AI Studio)** | Calibrating system instructions, tabular input/output pairs, and few-shot examples. |
| **Structured Output Testing** | **Cloud (AI Studio)** | Refining and validating complex JSON schemas via `Structured outputs` in chat or `/prompts/new_structured`. |
| **Web Content Ingestion** | **Cloud (AI Studio)** | Reading live webpage bodies via `URL context` and `Grounding with Google Search`. |
| **Model Comparison** | **Cloud (AI Studio)** | Evaluating prompts across `Gemini 4 Hydrogen`, `Argon`, `Neon`, and `Carbon` (`Thinking: High`). |
| **Synthetic Data Generation** | **Cloud (AI Studio)** | Generating batch test fixtures, mock data, or synthetic corpora with `Gemini 4 Hydrogen (High)`. |
| **Production Code Export** | **Cloud (AI Studio)** | Converting tuned prompts into runnable Python, TypeScript, cURL, or REST code (`thinking_level: "high"`). |

### End-to-End Offload Pipeline

Every cloud offload execution follows a strict 6-stage lifecycle:

```
[1. Evaluate] --> [2. Stage] --> [3. Dispatch] --> [4. Execute] --> [5. Extract] --> [6. Sync]
```

1. **Evaluate**: Task is matched against the decision matrix in `offload-decision-matrix.md` and assigned an authorized Gemini 4 model.
2. **Stage**: Local context and files are copied to `<Artifact Directory Path>/browser_sandbox/uploads/`.
3. **Dispatch**: The built-in `browser` subagent opens `https://aistudio.google.com/` directly.
4. **Execute**: Gemini 4 cloud models process prompts with `Thinking level = High` and configured `Run settings` / `Tools`.
5. **Extract**: Responses, schemas, and exported code are retrieved into `browser_sandbox/downloads/`.
6. **Synchronize**: Artifacts are validated and merged back into the local workspace.

---

## 5. Autonomy Modes

`antigravity-aistudio` operates under two distinct autonomy modes:

### Checkpoint Mode (Default)
In `checkpoint` mode, the agent prepares prompts, selects the Gemini 4 model (`Thinking level: High`), stages files, and formulates the offload plan, but **pauses and requests user approval** before submitting prompts or triggering exports in Google AI Studio. This gives developers complete oversight over prompt content and execution flow.

### Auto Mode (Full-Auto)
In `auto` mode, the agent runs the offload lifecycle end-to-end without per-step confirmation: navigating the UI, enforcing `Thinking level = High`, configuring `Run settings` & `Tools`, submitting queries, extracting results, and writing files back to the workspace automatically.

### Triggering Auto Mode
Mention unattended cues anywhere in your prompt:
- `"auto mode"` / `"full-auto"`
- `"run unattended"`
- `"without asking for confirmation"`
- `"batch offload to AI Studio"`

You can switch modes at any point during a conversation by replying `"switch to auto mode"` or `"switch to checkpoint mode"`.

---

## 6. Modular Skills Suite Overview

<p align="center">
  <img src="assets/modular-skills-ecosystem.png" alt="Antigravity AI Studio Modular Skills Ecosystem" width="100%">
</p>

The plugin provides six dedicated skills covering the entire Google AI Studio Gemini 4 surface:

| Skill | Purpose | Mode / Model Invocation |
| :--- | :--- | :--- |
| **`aistudio-offload`** | Master cloud offload coordinator evaluating tasks against the Gemini 4 decision matrix and syncing results. | Standard |
| **`aistudio-chat-prompt`** | Orchestrating multi-turn chat prompts, system instructions, `Thinking level = High`, `URL context`, and file attachments in `/prompts/new_chat`. | Standard |
| **`aistudio-structured-prompt`** | Tabular few-shot prompting, input/output column configuration, and `Structured outputs` JSON schemas in `/prompts/new_structured`. | Standard |
| **`aistudio-parameter-tuning`** | Configuring Gemini 4 `Run settings` (`Thinking level >= High`, `Output length`, `Media resolution`, `Safety settings`, `Add stop sequence`) and `Tools` (`URL context`, `Search Grounding`, `Code execution`, `Function calling`, `Structured outputs`). | Standard |
| **`aistudio-code-export`** | Exporting production-ready client code (Python, TypeScript, cURL, REST) with `thinking_level` (`"high"`/`"xhigh"`) and `GEMINI_API_KEY` protection via `Get code`. | Standard |
| **`aistudio-ui-sync-audit`** | Read-only live UI audit across 7 canonical AI Studio surfaces to detect UI drift, Gemini 4 model updates, or deprecations. | Manual (`disable-model-invocation: true`) |

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
- **Paid Tier Gate (`Unlock Gemini 4 Carbon` / `PAID_TIER_REQUIRED`)**: If `Gemini 4 Carbon` triggers a paywall banner, immediately pauses and offers fallback to `Gemini 4 Neon (High)` or `Gemini 4 Hydrogen (High)`.
- **Rate Limits & Quota Exhaustion (`429 ResourceExhausted`)**: Catches quota barriers, reports them clearly, and offers model fallback (e.g., falling back to `Gemini 4 Hydrogen (High)`).
- **Safety Blocks (`HARM_CATEGORY_*`)**: Intercepts content safety blocks, reporting specific categories and enabling parameter or prompt adjustment.

---

## 9. Testing & Quality Assurance

`antigravity-aistudio` includes a comprehensive 5-Tier automated test suite with adversarial hardening:

```bash
python tests/run_tests.py
```

### Verification Results

```text
================================================================================
  ANTIGRAVITY-AISTUDIO 5-TIER E2E TEST SUITE RUNNER
================================================================================
Executing Tier 1 (Feature Coverage)......... PASS (95/95 passed)
Executing Tier 2 (Boundary & Corner)........ PASS (96/96 passed)
Executing Tier 3 (Cross-Feature & Pairwise). PASS (28/28 passed)
Executing Tier 4 (Real-World Scenarios)..... PASS (6/6 passed)
Executing Tier 5 (Adversarial Hardening).... PASS (30/30 passed)
--------------------------------------------------------------------------------
GRAND TOTAL: 255 / 255 PASSED (100% Pass Rate)
================================================================================
```

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=qq136692547-cmyk/antigravity-aistudio&type=Date)](https://star-history.com/#qq136692547-cmyk/antigravity-aistudio&Date)

---

## Support & Buy Me a Coffee

Building and maintaining open-source tools often happens deep into the night. If `antigravity-aistudio` helped preserve your precious desktop IDE model quota, streamlined your development workflow, or saved you hours of debugging, a warm cup of coffee is the sweetest fuel for the next late-night coding session!

<p align="center">
  <img src="assets/sponsor-wechat.png" alt="WeChat Pay" width="220">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/sponsor-usdt.png" alt="USDT BNB Smart Chain" width="220">
</p>

<p align="center">
  <b>WeChat Pay</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>USDT (BNB Smart Chain)</b><br>
  <code>0xaCa8773aaA80815811ce1a45d40c86A53e4224ef0</code>
</p>

> *Every bit of kindness and encouragement keeps this project active, polished, and free for the community. Thank you!*

---

## License

Apache-2.0 (c) 2026 [qq136692547-cmyk](https://github.com/qq136692547-cmyk). All rights reserved.
