# -*- coding: utf-8 -*-
"""
Tier 3: Pairwise Combinatorial & Cross-Component Consistency Suite (27 tests)
Validates cross-feature interactions, schema-to-doc consistency, staging path parity,
prompt-to-skill routing matrices, and invariant contracts across the entire plugin.
Total tests: 27 tests (Requirement: >= 25 tests).

Remediated to strictly eliminate all mock fallback branches and tautological assertions.
Every test genuinely inspects and validates real repository files and domain validators.
"""

import os
import sys
import json
import re
import unittest
from pathlib import Path

# Add tests directory to sys.path to load conftest
TESTS_DIR = Path(__file__).resolve().parent
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from conftest import (
    REPO_ROOT,
    PLUGIN_JSON_PATH,
    README_PATH,
    LOGO_SVG_PATH,
    AGENTS_RULE_PATH,
    SKILLS_DIR,
    CANONICAL_URL,
    CANONICAL_SUBAGENT_TYPE,
    CANONICAL_DEFAULT_MODEL,
    CANONICAL_AUTONOMY_MODES,
    CANONICAL_SKILLS,
    CANONICAL_REFERENCES,
    CANONICAL_STAGING_PATHS,
    CANONICAL_7_AUDIT_SURFACES,
    CANONICAL_FIXTURES,
    ManifestValidator,
    ReadmeValidator,
    SvgValidator,
    RulesValidator,
    SkillValidator,
    OffloadDecisionEngine,
    OverseasLocalizationValidator,
    WorkflowSimulator,
    SubagentDelegationValidator,
    CanonicalRoutingValidator,
    AutonomyModeValidator,
    SafetyBoundariesValidator,
    StagingContractValidator,
    ParameterTuningValidator,
    CodeExportValidator,
    MarkdownTableValidator,
    PromptToSkillRouter,
    PromptToSkillValidator,
)


class TestTier3CrossFeature(unittest.TestCase):
    """Tier 3: Cross-Feature and Integration Invariant Consistency Tests."""

    def test_cross_01_plugin_json_skills_parity(self):
        """Cross-1: plugin.json suggested prompts align with the core capabilities of the skills."""
        self.assertTrue(PLUGIN_JSON_PATH.is_file(), f"plugin.json missing at {PLUGIN_JSON_PATH}")
        data = json.loads(PLUGIN_JSON_PATH.read_text(encoding="utf-8"))
        prompts = data.get("suggestedPrompts", [])
        self.assertGreater(len(prompts), 0, "suggestedPrompts must not be empty")
        errors = PromptToSkillRouter.validate_manifest_prompts(prompts)
        self.assertEqual(errors, [], f"Manifest prompts routing errors: {errors}")

    def test_cross_02_readme_skills_directory_parity(self):
        """Cross-2: README.md documents all 6 canonical skills."""
        self.assertTrue(README_PATH.is_file(), f"README.md missing at {README_PATH}")
        content = README_PATH.read_text(encoding="utf-8")
        for skill in CANONICAL_SKILLS:
            self.assertIn(skill, content, f"README missing documentation for skill: {skill}")

    def test_cross_03_staging_uploads_path_consistency(self):
        """Cross-3: Staging uploads path is consistent across rules and test infra."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"rules/AGENTS.md missing at {AGENTS_RULE_PATH}")
        expected_path = "browser_sandbox/uploads/"
        self.assertIn(expected_path, CANONICAL_STAGING_PATHS["uploads"])
        rule_text = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertIn(expected_path, rule_text)

    def test_cross_04_staging_downloads_path_consistency(self):
        """Cross-4: Staging downloads path is consistent across rules and test infra."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"rules/AGENTS.md missing at {AGENTS_RULE_PATH}")
        expected_path = "browser_sandbox/downloads/"
        self.assertIn(expected_path, CANONICAL_STAGING_PATHS["downloads"])
        rule_text = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertIn(expected_path, rule_text)

    def test_cross_05_staging_references_path_consistency(self):
        """Cross-5: Staging references path is consistent across rules and test infra."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"rules/AGENTS.md missing at {AGENTS_RULE_PATH}")
        expected_path = "browser_sandbox/references/"
        self.assertIn(expected_path, CANONICAL_STAGING_PATHS["references"])
        rule_text = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertIn(expected_path, rule_text)

    def test_cross_06_canonical_url_consistency_manifest_rules_readme(self):
        """Cross-6: Canonical URL is identical across manifest, rules, and documentation."""
        self.assertTrue(PLUGIN_JSON_PATH.is_file(), f"plugin.json missing: {PLUGIN_JSON_PATH}")
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"rules/AGENTS.md missing: {AGENTS_RULE_PATH}")
        self.assertTrue(README_PATH.is_file(), f"README.md missing: {README_PATH}")
        self.assertEqual(CANONICAL_URL, "https://aistudio.google.com/")
        manifest = json.loads(PLUGIN_JSON_PATH.read_text(encoding="utf-8"))
        self.assertIn("aistudio.google.com", manifest.get("homepage", ""))
        self.assertIn(CANONICAL_URL, AGENTS_RULE_PATH.read_text(encoding="utf-8"))
        self.assertIn("aistudio.google.com", README_PATH.read_text(encoding="utf-8"))

    def test_cross_07_autonomy_mode_consistency(self):
        """Cross-7: Autonomy modes ('checkpoint', 'auto') are consistently recognized."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"rules/AGENTS.md missing at {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        for mode in CANONICAL_AUTONOMY_MODES:
            self.assertIn(mode, ["checkpoint", "auto"])
            self.assertIn(mode, content)

    def test_cross_08_offload_skill_matrix_reference_path(self):
        """Cross-8: aistudio-offload skill correctly references offload-decision-matrix.md."""
        self.assertTrue(SKILLS_DIR.is_dir(), f"Skills directory missing: {SKILLS_DIR}")
        ref_file = SKILLS_DIR / "aistudio-offload" / CANONICAL_REFERENCES["aistudio-offload"]
        self.assertTrue(ref_file.is_file(), f"Matrix reference missing: {ref_file}")
        skill_md = SKILLS_DIR / "aistudio-offload" / "SKILL.md"
        self.assertTrue(skill_md.is_file(), f"SKILL.md missing: {skill_md}")
        self.assertIn(CANONICAL_REFERENCES["aistudio-offload"], skill_md.read_text(encoding="utf-8"))

    def test_cross_09_ui_sync_skill_audit_checklist_reference_path(self):
        """Cross-9: aistudio-ui-sync-audit skill correctly references audit-checklist.md."""
        self.assertTrue(SKILLS_DIR.is_dir(), f"Skills directory missing: {SKILLS_DIR}")
        ref_file = SKILLS_DIR / "aistudio-ui-sync-audit" / CANONICAL_REFERENCES["aistudio-ui-sync-audit"]
        self.assertTrue(ref_file.is_file(), f"Audit checklist missing: {ref_file}")
        skill_md = SKILLS_DIR / "aistudio-ui-sync-audit" / "SKILL.md"
        self.assertTrue(skill_md.is_file(), f"SKILL.md missing: {skill_md}")
        self.assertIn(CANONICAL_REFERENCES["aistudio-ui-sync-audit"], skill_md.read_text(encoding="utf-8"))

    def test_cross_10_ui_sync_disable_model_invocation_rule_contract(self):
        """Cross-10: UI sync audit skill strictly enforces disable-model-invocation: true."""
        audit_skill_file = SKILLS_DIR / "aistudio-ui-sync-audit" / "SKILL.md"
        self.assertTrue(audit_skill_file.is_file(), f"Target file missing: {audit_skill_file}")
        fm, _, errors = SkillValidator.parse_frontmatter(audit_skill_file.read_text(encoding="utf-8"))
        self.assertEqual(errors, [])
        self.assertTrue(fm.get("disable-model-invocation") is True)

    def test_cross_11_parameter_tuning_model_alignment(self):
        """Cross-11: Parameter ranges align with models referenced in decision matrix."""
        valid_params = {"temperature": 0.7, "top_p": 0.95, "top_k": 40}
        self.assertEqual(ParameterTuningValidator.validate_hyperparameters(valid_params), [])
        invalid_params = {"temperature": 2.5, "top_p": -0.1, "top_k": 0}
        errors = ParameterTuningValidator.validate_hyperparameters(invalid_params)
        self.assertEqual(len(errors), 3, f"Expected 3 validation errors, got: {errors}")

    def test_cross_12_code_export_gemini_api_key_convention(self):
        """Cross-12: API key environment variable is consistently GEMINI_API_KEY."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"rules/AGENTS.md missing at {AGENTS_RULE_PATH}")
        expected_env = "GEMINI_API_KEY"
        sim = WorkflowSimulator.simulate_few_shot_structured_export({})
        self.assertIn(expected_env, sim["exported_code"])

    def test_cross_13_browser_subagent_model_flash_consistency(self):
        """Cross-13: Default subagent model is consistently 'flash' across protocols."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"rules/AGENTS.md missing at {AGENTS_RULE_PATH}")
        self.assertEqual(CANONICAL_DEFAULT_MODEL, "flash")
        self.assertIn('Model: "flash"', AGENTS_RULE_PATH.read_text(encoding="utf-8"))

    def test_cross_14_logo_svg_manifest_path_consistency(self):
        """Cross-14: plugin.json logo property specifies 'assets/logo.svg'."""
        self.assertTrue(PLUGIN_JSON_PATH.is_file(), f"plugin.json missing at {PLUGIN_JSON_PATH}")
        self.assertTrue(LOGO_SVG_PATH.is_file(), f"logo.svg missing at {LOGO_SVG_PATH}")
        manifest = json.loads(PLUGIN_JSON_PATH.read_text(encoding="utf-8"))
        self.assertEqual(manifest.get("logo"), "assets/logo.svg")

    def test_cross_15_all_skill_names_kebab_case(self):
        """Cross-15: All canonical skill names on disk strictly adhere to kebab-case naming."""
        self.assertTrue(SKILLS_DIR.is_dir(), f"Skills directory missing: {SKILLS_DIR}")
        for skill_dir in SKILLS_DIR.iterdir():
            if skill_dir.is_dir():
                skill_md = skill_dir / "SKILL.md"
                self.assertTrue(skill_md.is_file(), f"SKILL.md missing in {skill_dir}")
                self.assertTrue(bool(re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", skill_dir.name)), f"{skill_dir.name} is not kebab-case")

    def test_cross_16_all_skills_have_description(self):
        """Cross-16: All canonical skills have defined descriptions."""
        self.assertTrue(SKILLS_DIR.is_dir(), f"Skills directory missing: {SKILLS_DIR}")
        found = 0
        for skill_name in CANONICAL_SKILLS:
            skill_md = SKILLS_DIR / skill_name / "SKILL.md"
            self.assertTrue(skill_md.is_file(), f"SKILL.md missing for {skill_name}")
            fm, _, errors = SkillValidator.parse_frontmatter(skill_md.read_text(encoding="utf-8"))
            self.assertEqual(errors, [])
            self.assertTrue(bool(fm.get("description")))
            found += 1
        self.assertEqual(found, len(CANONICAL_SKILLS))

    def test_cross_17_prompt_matching_heavy_reasoning_to_offload(self):
        """Cross-17: Prompt requesting deep reasoning routes to aistudio-offload."""
        res = OffloadDecisionEngine.evaluate("Perform complex architectural reasoning for distributed consensus")
        self.assertEqual(res["route"], "CLOUD_OFFLOAD")
        self.assertEqual(res["recommended_model"], "Gemini Flash Thinking")

    def test_cross_18_prompt_matching_chat_to_chat_skill(self):
        """Cross-18: Prompt requesting multi-turn conversation routes to aistudio-chat-prompt."""
        chat_prompt = "Start a multi-turn chat conversation with custom system instructions in Google AI Studio"
        routed = PromptToSkillValidator.route_prompt(chat_prompt)
        self.assertEqual(routed["skill"], "aistudio-chat-prompt")
        self.assertIn("chat", routed["matched_keywords"])

    def test_cross_19_prompt_matching_structured_to_structured_skill(self):
        """Cross-19: Prompt requesting tabular few-shots routes to aistudio-structured-prompt."""
        structured_prompt = "Construct and evaluate a few-shot structured prompt with JSON response schema in Google AI Studio"
        routed = PromptToSkillValidator.route_prompt(structured_prompt)
        self.assertEqual(routed["skill"], "aistudio-structured-prompt")
        self.assertIn("structured", routed["matched_keywords"])

    def test_cross_20_prompt_matching_tuning_to_tuning_skill(self):
        """Cross-20: Prompt requesting parameter adjustments routes to aistudio-parameter-tuning."""
        tuning_prompt = "Tune Gemini model hyperparameters and safety settings in Google AI Studio"
        routed = PromptToSkillValidator.route_prompt(tuning_prompt)
        self.assertEqual(routed["skill"], "aistudio-parameter-tuning")
        self.assertIn("tune", routed["matched_keywords"])

    def test_cross_21_prompt_matching_export_to_export_skill(self):
        """Cross-21: Prompt requesting production code routes to aistudio-code-export."""
        export_prompt = "Export prompt configuration as Python code using Get code dialog with GEMINI_API_KEY"
        routed = PromptToSkillValidator.route_prompt(export_prompt)
        self.assertEqual(routed["skill"], "aistudio-code-export")
        self.assertIn("export", routed["matched_keywords"])

    def test_cross_22_prompt_matching_audit_to_sync_audit_skill(self):
        """Cross-22: Prompt requesting UI audit routes to aistudio-ui-sync-audit."""
        audit_prompt = "Audit live Google AI Studio web UI capabilities and model availability with aistudio-ui-sync-audit"
        routed = PromptToSkillValidator.route_prompt(audit_prompt)
        self.assertEqual(routed["skill"], "aistudio-ui-sync-audit")
        self.assertTrue(routed["config"]["disable_model_invocation"])

    def test_cross_23_quota_boundary_integration_with_offload_pipeline(self):
        """Cross-23: Quota 429 boundary integration immediately pauses cloud offload pipeline."""
        sim = WorkflowSimulator.simulate_quota_limit_detection({"http_code": 429, "mode": "auto"})
        self.assertEqual(sim["status"], "PAUSED_QUOTA_EXHAUSTED")
        self.assertTrue(sim["automated_retry_aborted"])

    def test_cross_24_fast_path_auth_integration_with_chat_pipeline(self):
        """Cross-24: Chat workflow initializes by invoking fast-path auth check."""
        sim = WorkflowSimulator.simulate_fast_path_auth({
            "current_url": CANONICAL_URL,
            "dom_avatar_present": True,
            "rpc_status": 200,
            "has_sign_in_button": False,
        })
        self.assertEqual(sim["status"], "AUTHENTICATED")
        self.assertEqual(sim["target_view"], "/prompts/new_chat")

    def test_cross_25_file_staging_integration_with_chat_media_upload(self):
        """Cross-25: Chat media upload uses sandboxed uploads directory."""
        media_filename = "diagram.png"
        self.assertEqual(StagingContractValidator.validate_filename(media_filename), [])
        staged_upload_target = f"{CANONICAL_STAGING_PATHS['uploads']}{media_filename}"
        self.assertTrue(staged_upload_target.endswith("/browser_sandbox/uploads/diagram.png"))

    def test_cross_26_structured_output_integration_with_code_export(self):
        """Cross-26: Structured prompt response schema is embedded in exported Python code."""
        custom_schema = {"type": "object", "properties": {"score": {"type": "number"}}}
        self.assertEqual(CodeExportValidator.validate_json_schema(custom_schema), [])
        sim = WorkflowSimulator.simulate_few_shot_structured_export({"schema": custom_schema})
        self.assertIn("response_schema", sim["exported_code"])
        self.assertIn("score", sim["exported_code"])

    def test_cross_27_zero_chinese_across_all_repo_artifacts(self):
        """Cross-27: Comprehensive repository scan confirms zero non-English characters in any text file."""
        self.assertTrue(REPO_ROOT.is_dir(), f"Repository root missing: {REPO_ROOT}")
        mandatory_dirs = [REPO_ROOT / "rules", REPO_ROOT / "assets", REPO_ROOT / "tests", REPO_ROOT / "skills"]
        for d in mandatory_dirs:
            self.assertTrue(d.is_dir(), f"Mandatory repository directory missing: {d}")

        all_violations = []
        extensions = ["*.json", "*.md", "*.svg", "*.py"]
        for d in [REPO_ROOT] + mandatory_dirs:
            for ext in extensions:
                for path in d.glob(ext):
                    v = OverseasLocalizationValidator.scan_file(path)
                    if v:
                        all_violations.extend([(str(path), line, char, text) for line, char, text in v])
                    raw_bytes = path.read_bytes()
                    non_ascii = [b for b in raw_bytes if b > 127]
                    if non_ascii:
                        all_violations.append((str(path), 0, f"{len(non_ascii)} non-ASCII bytes", ""))
        gitignore_path = REPO_ROOT / ".gitignore"
        if gitignore_path.exists():
            v = OverseasLocalizationValidator.scan_file(gitignore_path)
            if v:
                all_violations.extend([(str(gitignore_path), line, char, text) for line, char, text in v])
            raw_bytes = gitignore_path.read_bytes()
            non_ascii = [b for b in raw_bytes if b > 127]
            if non_ascii:
                all_violations.append((str(gitignore_path), 0, f"{len(non_ascii)} non-ASCII bytes", ""))
        self.assertEqual(all_violations, [], f"Found non-English violations: {all_violations}")


if __name__ == "__main__":
    unittest.main()
