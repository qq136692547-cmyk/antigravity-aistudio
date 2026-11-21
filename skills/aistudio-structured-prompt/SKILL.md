---
name: aistudio-structured-prompt
description: Tabular few-shot structured prompting in Google AI Studio with input/output example columns, test case evaluation, JSON schema outputs, and CSV batch import/export.
---

# AI Studio Structured Prompt Orchestrator

Design, test, and evaluate tabular few-shot structured prompts and JSON schema constrained outputs in **Google AI Studio** (`https://aistudio.google.com/prompts/new_structured`) to offload data extraction, classification, and schema enforcement workloads to cloud models.

## When to Use

- The user wants to construct few-shot prompts using a table of input and output examples.
- The user needs guaranteed JSON structured outputs conforming to a strict JSON schema.
- The user wants to run batch evaluations across multiple test cases without local model quota expenditure.
- The user wants to import an existing tabular dataset via CSV, run cloud inference across rows, and export results back to the local workspace.

## Workflow

### Step 1: Navigate to Structured Prompt Editor

1. Delegate to the `browser` subagent (`TypeName: "browser"`, `Model: "flash"`) targeting `https://aistudio.google.com/prompts/new_structured`.
2. Confirm active session via Fast-Path Authentication Check (user avatar visible, structured table editor loaded, RPC status HTTP 200).
3. If fast-path authentication succeeds, proceed directly to table definition.

### Step 2: Configure Table Schema and Columns

1. In the structured prompt editor, define the table column headers:
   - **Input Columns**: Define one or more input fields (e.g., `Input Text`, `Context`, `Source Language`).
   - **Output Columns**: Define the target output field (e.g., `Expected JSON`, `Sentiment`, `Classification Label`).
2. Optionally specify global system instructions or prompt prefixes in the preamble field above the example table.

### Step 3: Populate Few-Shot Examples

1. Add representative few-shot rows demonstrating the desired input-to-output mapping.
2. For each example row:
   - Enter realistic input values in the input column cells.
   - Enter gold-standard reference outputs in the output column cells.
3. Include diverse edge cases (e.g., empty optional fields, non-standard punctuation, multi-sentence inputs) to ensure model robustness.

### Step 4: Configure JSON Schema Structured Outputs

1. In the right-hand settings drawer, open the **Response format** or **Structured output** section.
2. Select **JSON** response format.
3. Supply a valid JSON schema definition specifying expected types, required properties, and descriptions. For example:

```json
{
  "type": "object",
  "properties": {
    "entity_name": { "type": "string" },
    "confidence_score": { "type": "number" },
    "categories": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": ["entity_name", "confidence_score", "categories"]
}
```

4. Verify that schema validation passes without syntax errors in the AI Studio editor.

### Step 5: Add Test Cases and Run Cloud Evaluation

1. In the **Test your prompt** section below the few-shot table, add one or more test cases.
2. Input the test values for each input column.
3. In `checkpoint` mode (default), present the test cases and example count to the user before running. In `auto` mode, trigger batch execution immediately.
4. Click `Run all test cases` or click `Run` on individual test rows.
5. Inspect the generated model outputs in the output column cells:
   - Confirm outputs adhere to the configured JSON schema.
   - Verify accuracy against expected transformations.

### Step 6: CSV Batch Import and Export

For large-scale dataset evaluations:
1. **Importing CSV Data**:
   - Stage the source CSV file into `<Artifact Directory Path>/browser_sandbox/uploads/<filename>.csv`.
   - Use AI Studio's table import option to load rows into the structured prompt table.
2. **Exporting Completed Results**:
   - Click the export button in the table header to download evaluation results as CSV or JSON.
   - Save the exported file into `<Artifact Directory Path>/browser_sandbox/downloads/<filename>.csv`.
   - Synchronize the file back to the workspace (e.g., `data/evaluated_results.csv`).
3. Confirm that exported data contains all evaluated test rows and matches local column expectations.
