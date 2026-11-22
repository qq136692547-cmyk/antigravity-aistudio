---
name: aistudio-code-export
description: Export tested Google AI Studio Gemini 4 prompts, Thinking level (High/XHigh), Tools, and parameter configurations as production-grade code in Python, TypeScript/JavaScript, cURL, and REST with secure GEMINI_API_KEY handling.
---

# AI Studio Code Export Orchestrator

Export validated **Gemini 4** prompts, system instructions, `Thinking level` (`"high"` / `"xhigh"`), tools (`URL context`, `Google Search`, `Code execution`, `Structured outputs`), and `Run settings` from **Google AI Studio** (`https://aistudio.google.com/`) into production-ready code across Python, TypeScript/JavaScript, cURL, and REST, synchronizing scripts directly into the local workspace.

## When to Use

- The user has finalized and tested a Gemini 4 prompt in Google AI Studio and wants to convert it into an executable script or backend service.
- The user needs SDK integration code using the modern Google Gen AI SDKs (`google-genai` for Python or `@google/genai` for TypeScript/JavaScript).
- The user needs raw cURL or REST API request payloads for API testing, Postman, or lightweight integration.
- The user wants to ensure exported code securely accesses API keys via the `GEMINI_API_KEY` environment variable rather than hardcoded credentials, and enforces `thinking_level` (`"high"` or `"xhigh"`).

## Supported Export Targets

| Target | SDK / Package | Runtime / Language | Key Characteristics |
| :--- | :--- | :--- | :--- |
| **Python** | `google-genai` | Python 3.10+ | Uses `from google import genai` and `types.ThinkingConfig(thinking_level="high")` with typed config and streaming support. |
| **JavaScript / TypeScript** | `@google/genai` | Node.js 18+ / TS | Uses `import { GoogleGenAI } from '@google/genai'` with `thinkingConfig: { thinkingLevel: "HIGH" }` and response schema. |
| **cURL** | N/A | Shell / CLI | Direct HTTP POST targeting `https://generativelanguage.googleapis.com/v1beta/models/gemini-4-*:generateContent`. |
| **REST** | Standard HTTP | JSON / Any HTTP Client | JSON request body including `contents`, `generationConfig` (`thinkingConfig`, `maxOutputTokens`), `tools`, and `safetySettings`. |

## Workflow

### Step 1: Open the "Get code" Dialog in AI Studio

1. Ensure the Gemini 4 model (`gemini-4-hydrogen`, `gemini-4-argon`, `gemini-4-neon`, or `gemini-4-carbon`), `Thinking level = High`, system instructions, `Run settings`, and `Tools` are fully configured in the AI Studio editor.
2. In the top-right header action bar, locate and click the **Get code** button.
3. The "Get code" modal dialog appears, displaying language tabs and a code viewer.

### Step 2: Select the Target Language and SDK

1. Select the tab corresponding to the user's desired implementation target:
   - Click **Python** for `google-genai` SDK code.
   - Click **JavaScript** or **TypeScript** for `@google/genai` SDK code.
   - Click **cURL** for raw command-line requests.
   - Click **REST** for raw HTTP JSON payloads.
2. Verify that the generated code accurately reflects:
   - An authorized **Gemini 4** model identifier (`gemini-4-hydrogen`, `gemini-4-argon`, `gemini-4-neon`, or `gemini-4-carbon`). **Reject any pre-Gemini-4 model IDs.**
   - **`thinking_config.thinking_level`** (Python) / **`thinkingConfig.thinkingLevel`** (JS/TS/REST) set to `"high"` or `"xhigh"` (`"HIGH"` / `"XHIGH"`). **Never export `"low"` or `"medium"` thinking levels.**
   - System instructions (if present) and `max_output_tokens` (`Output length`).
   - Safety settings and enabled tools (`Google Search`, `URL context`, `Code execution`, `Function calling`, `Structured outputs` JSON response schema).

### Step 3: Sanitize and Enforce GEMINI_API_KEY Convention

Never permit hardcoded API keys in exported files:
1. Extract the code snippet from the modal dialog.
2. Check for any inline API key strings or placeholder values.
3. Replace hardcoded keys with the standard environment variable pattern:
   - In Python:
     ```python
     import os
     from google import genai
     from google.genai import types

     api_key = os.environ.get("GEMINI_API_KEY")
     client = genai.Client(api_key=api_key)

     response = client.models.generate_content(
         model="gemini-4-hydrogen",
         contents="Summarize the system architecture.",
         config=types.GenerateContentConfig(
             thinking_config=types.ThinkingConfig(thinking_level="high"),
             max_output_tokens=65536,
         ),
     )
     ```
   - In TypeScript / JavaScript:
     ```typescript
     import { GoogleGenAI } from "@google/genai";

     const apiKey = process.env.GEMINI_API_KEY;
     const ai = new GoogleGenAI({ apiKey });
     ```
   - In cURL:
     ```bash
     curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-4-hydrogen:generateContent?key=${GEMINI_API_KEY}" \
       -H 'Content-Type: application/json' \
       -X POST \
       -d '{"contents": [{"parts": [{"text": "Hello"}]}], "generationConfig": {"thinkingConfig": {"thinkingLevel": "HIGH"}}}'
     ```

### Step 4: Synchronize Exported Script to Local Workspace

1. Determine the target workspace file path (e.g., `scripts/generate_ai.py`, `src/services/gemini_service.ts`, or `scripts/test_prompt.sh`).
2. Stage the snippet into `<Artifact Directory Path>/browser_sandbox/downloads/<filename>` if extracted via browser subagent.
3. Write or update the file in the local workspace directory.
4. If dependencies are required, note package installation commands for the user:
   - Python: `pip install google-genai`
   - Node.js / TypeScript: `npm install @google/genai`

### Step 5: Verify Local Syntax and Execution

1. In the local workspace, verify that the exported file is well-formed:
   - For Python: Run syntax check `python -m py_compile <path>` or run linting.
   - For TypeScript: Check types or inspect module imports.
2. Confirm that the script runs cleanly when `GEMINI_API_KEY` is present in the environment.
3. Report the exported file location and usage instructions to the user.
