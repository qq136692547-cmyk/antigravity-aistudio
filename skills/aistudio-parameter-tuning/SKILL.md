---
name: aistudio-parameter-tuning
description: Model hyperparameter tuning in Google AI Studio covering temperature, top-p, top-k, thinking budget, safety filter thresholds, Google Search grounding, and Python code execution.
---

# AI Studio Parameter Tuning Orchestrator

Calibrate model hyperparameters, safety filter thresholds, grounding tools, and execution capabilities in **Google AI Studio** (`https://aistudio.google.com/`) to achieve optimal balance between creativity, determinism, reasoning depth, and factual verification.

## When to Use

- The user wants to adjust generation randomness (temperature) for deterministic code generation versus creative writing.
- The user needs to configure nucleus sampling (top-p) or candidate token pool size (top-k).
- The user wants to tune the thinking budget for Gemini Flash Thinking on complex reasoning problems.
- The user needs to relax or tighten content safety filter thresholds for specialized domain content.
- The user wants to toggle Google Search grounding for real-time web retrieval or enable Python code execution for mathematical verification.

## Supported Hyperparameters and Controls

### 1. Model Selection

Select the appropriate model tier in the top-right model dropdown:
- **Gemini 2.5 Flash**: Default model for high-throughput, low-latency, and cost-effective cloud generation (1M context window).
- **Gemini 2.5 Pro**: Flagship model for intricate architectural synthesis, deep analysis, and massive multimodal corpora (2M context window).
- **Gemini Flash Thinking**: Specialized reasoning model with explicit internal scratchpad thinking tokens.

### 2. Sampling Hyperparameters

| Parameter | Valid Range | Default | Recommended Setting by Task |
| :--- | :--- | :--- | :--- |
| **Temperature** | `0.0` to `2.0` | `1.0` (or `0.7`) | `0.0` - `0.2` for deterministic code, JSON extraction, math; `0.7` for general conversation; `1.2` - `1.5` for creative storytelling. |
| **Top-P (Nucleus Sampling)** | `0.0` to `1.0` | `0.95` | `0.95` for standard generation; lower to `0.8` for more focused vocabulary; `1.0` for full distribution. |
| **Top-K** | `1` to `100` | `40` | `40` for general text; lower values (`1` - `20`) restrict token choices to top candidates for stricter accuracy. |
| **Thinking Budget** | `0` to `65,536` tokens (or Auto) | Auto | Use Auto for adaptive reasoning; set higher explicit budget (e.g., `8192` - `16384`) for complex math or algorithm proofs. |

### 3. Safety Filter Thresholds

Google AI Studio provides 4 adjustable safety categories:
- **Harassment** (`HARM_CATEGORY_HARASSMENT`)
- **Hate Speech** (`HARM_CATEGORY_HATE_SPEECH`)
- **Sexually Explicit** (`HARM_CATEGORY_SEXUALLY_EXPLICIT`)
- **Dangerous Content** (`HARM_CATEGORY_DANGEROUS_CONTENT`)

Each category supports 4 threshold levels:
- **Block None**: Do not block any content based on this category (available with appropriate account verification).
- **Block Few**: Block only high-probability harm content.
- **Block Some** (Default): Block medium- and high-probability harm content.
- **Block Most**: Strictly block low-, medium-, and high-probability harm content.

### 4. Advanced Tools and Capabilities

- **Google Search Grounding**: Toggle on to allow Gemini to execute real-time web searches, retrieve recent information, and provide inline source citations with clickable web URLs.
- **Python Code Execution**: Toggle on to allow the model to write, compile, and execute Python code in a sandboxed runtime environment for calculations, data analysis, and symbolic mathematics.

## Workflow

### Step 1: Open Settings Drawer in AI Studio

1. In any prompt view (`/prompts/new_chat`, `/prompts/new_structured`, or existing prompt), locate the **Model settings** panel in the right sidebar.
2. If collapsed, click the settings toggle button in the top action bar to expand the parameter controls.

### Step 2: Adjust Sampling Sliders

1. **Set Temperature**: Drag the temperature slider or type the desired value in the input box within `[0.0, 2.0]`.
2. **Expand Advanced Settings**: Click **Advanced settings** to expose Top-P and Top-K controls.
3. **Set Top-P**: Enter target value within `[0.0, 1.0]`.
4. **Set Top-K**: Enter target integer within `[1, 100]`.
5. If using Gemini Flash Thinking, locate the **Thinking budget** slider and configure the token budget or select `Auto`.

### Step 3: Configure Safety Filter Settings

1. Click **Safety settings** in the sidebar.
2. In the safety modal, inspect current thresholds across all 4 harm categories.
3. Adjust sliders according to task requirements (e.g., adjust threshold to "Block Few" for security vulnerability research).
4. Save safety configurations.

### Step 4: Toggle Tools (Grounding and Code Execution)

1. Under the **Tools** section in the settings drawer:
   - Enable **Google Search** if the prompt requires current factual data or external references.
   - Enable **Code execution** if the prompt requires algorithmic computation or numerical calculations.
2. Confirm active tool indicators are highlighted in the UI.

### Step 5: Test and Verify Parameter Behavior

1. Execute test prompts to verify the model exhibits expected behavioral changes:
   - Verify low temperature produces deterministic, repeatable outputs.
   - Verify search grounding returns populated search queries and grounded sources.
   - Verify code execution displays executed Python code blocks and standard output.
2. Document the final calibrated hyperparameter preset in the project documentation or prompt metadata.
