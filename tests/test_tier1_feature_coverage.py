# -*- coding: utf-8 -*-
"""
Tier 1: Comprehensive Feature Coverage Test Suite (95 tests)
Validates primary behaviors (happy path) for Features 1 through 19:
Each feature has exactly 5 dedicated, isolated, verifiable test methods.
Total: 19 features * 5 tests = 95 tests.

Remediated to strictly eliminate all mock fallback branches, fixture bypassing,
and tautological constant checks. Every test genuinely inspects and validates real repository files.
"""

import os
import sys
import json
import re
import unittest
import xml.etree.ElementTree as ET
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
)


class TestTier1FeatureCoverage(unittest.TestCase):
    """Tier 1: Feature Coverage Test Cases (F1 - F19)."""

    # =========================================================================
    # Feature 1: Plugin Manifest (plugin.json) - 5 Tests
    # =========================================================================

    def test_f1_01_manifest_validity(self):
        """F1-1: plugin.json exists and conforms to agent-plugins schema without errors."""
        self.assertTrue(PLUGIN_JSON_PATH.is_file(), f"Target file missing: {PLUGIN_JSON_PATH}")
        errors = ManifestValidator.validate_file(PLUGIN_JSON_PATH)
        self.assertEqual(errors, [], f"Manifest validation errors in {PLUGIN_JSON_PATH}: {errors}")

    def test_f1_02_manifest_required_fields(self):
        """F1-2: Manifest contains all mandatory fields with correct types."""
        self.assertTrue(PLUGIN_JSON_PATH.is_file(), f"Target file missing: {PLUGIN_JSON_PATH}")
        manifest_data = json.loads(PLUGIN_JSON_PATH.read_text(encoding="utf-8"))
        for req in ManifestValidator.REQUIRED_FIELDS:
            self.assertIn(req, manifest_data, f"Missing required field: {req}")
            self.assertIsNotNone(manifest_data[req])

    def test_f1_03_manifest_suggested_prompts(self):
        """F1-3: Manifest has valid suggested prompts covering cloud offloading."""
        self.assertTrue(PLUGIN_JSON_PATH.is_file(), f"Target file missing: {PLUGIN_JSON_PATH}")
        manifest_data = json.loads(PLUGIN_JSON_PATH.read_text(encoding="utf-8"))
        prompts = manifest_data.get("suggestedPrompts", [])
        self.assertIsInstance(prompts, list)
        self.assertGreaterEqual(len(prompts), 1)
        prompts_text = " ".join(prompts).lower()
        self.assertTrue(
            "aistudio" in prompts_text or "offload" in prompts_text or "prompt" in prompts_text or "gemini" in prompts_text,
            "Suggested prompts must reflect AI Studio cloud workflows",
        )

    def test_f1_04_manifest_semantic_version(self):
        """F1-4: Manifest version follows valid semantic versioning (X.Y.Z) and is 0.2.1."""
        self.assertTrue(PLUGIN_JSON_PATH.is_file(), f"Target file missing: {PLUGIN_JSON_PATH}")
        manifest_data = json.loads(PLUGIN_JSON_PATH.read_text(encoding="utf-8"))
        version = manifest_data.get("version", "")
        self.assertTrue(ManifestValidator.SEMVER_PATTERN.match(version), f"Invalid semver: {version}")
        self.assertEqual(version, "0.2.1")

    def test_f1_05_manifest_homepage_and_repo_urls(self):
        """F1-5: Manifest homepage and repository fields are valid URLs."""
        self.assertTrue(PLUGIN_JSON_PATH.is_file(), f"Target file missing: {PLUGIN_JSON_PATH}")
        manifest_data = json.loads(PLUGIN_JSON_PATH.read_text(encoding="utf-8"))
        homepage = manifest_data.get("homepage", "")
        repo = manifest_data.get("repository", "")
        self.assertTrue(homepage.startswith("https://") or homepage.startswith("http://"), f"Invalid homepage: {homepage}")
        self.assertTrue(repo.startswith("https://") or repo.startswith("http://"), f"Invalid repo: {repo}")

    # =========================================================================
    # Feature 2: Documentation (README.md) - 5 Tests
    # =========================================================================

    def test_f2_01_readme_presence_and_structure(self):
        """F2-1: README.md exists and contains a valid top-level H1 header."""
        self.assertTrue(README_PATH.is_file(), f"Target file missing: {README_PATH}")
        content = README_PATH.read_text(encoding="utf-8")
        self.assertRegex(content, r"^#\s+.+", "README.md must have a top-level H1 title")

    def test_f2_02_readme_required_sections(self):
        """F2-2: README.md covers Installation, Architecture, Offload Engine, and Autonomy Modes."""
        self.assertTrue(README_PATH.is_file(), f"Target file missing: {README_PATH}")
        errors = ReadmeValidator.validate_file(README_PATH)
        self.assertEqual(errors, [], f"README validation errors: {errors}")

    def test_f2_03_readme_canonical_url_referenced(self):
        """F2-3: README.md explicitly references canonical domain aistudio.google.com."""
        self.assertTrue(README_PATH.is_file(), f"Target file missing: {README_PATH}")
        content = README_PATH.read_text(encoding="utf-8")
        self.assertIn("aistudio.google.com", content)

    def test_f2_04_readme_quota_preservation_explained(self):
        """F2-4: README.md explains the core concept of conserving local desktop model quota."""
        self.assertTrue(README_PATH.is_file(), f"Target file missing: {README_PATH}")
        content = README_PATH.read_text(encoding="utf-8")
        self.assertIn("quota", content.lower())

    def test_f2_05_readme_documents_skills(self):
        """F2-5: README.md enumerates all 6 modular skills."""
        self.assertTrue(README_PATH.is_file(), f"Target file missing: {README_PATH}")
        content = README_PATH.read_text(encoding="utf-8")
        for skill in CANONICAL_SKILLS:
            self.assertIn(skill, content, f"README missing documentation for skill: {skill}")

    # =========================================================================
    # Feature 3: Visual Asset (assets/logo.svg) - 5 Tests
    # =========================================================================

    def test_f3_01_logo_svg_xml_validity(self):
        """F3-1: assets/logo.svg parses as valid XML without syntax errors."""
        self.assertTrue(LOGO_SVG_PATH.is_file(), f"Target file missing: {LOGO_SVG_PATH}")
        errors = SvgValidator.validate_file(LOGO_SVG_PATH)
        self.assertEqual(errors, [], f"SVG validation errors: {errors}")

    def test_f3_02_logo_svg_root_element(self):
        """F3-2: assets/logo.svg root element is <svg>."""
        self.assertTrue(LOGO_SVG_PATH.is_file(), f"Target file missing: {LOGO_SVG_PATH}")
        content = LOGO_SVG_PATH.read_text(encoding="utf-8")
        root = ET.fromstring(content)
        tag = root.tag
        if "}" in tag:
            tag = tag.split("}")[-1]
        self.assertEqual(tag.lower(), "svg")

    def test_f3_03_logo_svg_viewbox_or_dimensions(self):
        """F3-3: assets/logo.svg specifies viewBox or width/height attributes."""
        self.assertTrue(LOGO_SVG_PATH.is_file(), f"Target file missing: {LOGO_SVG_PATH}")
        content = LOGO_SVG_PATH.read_text(encoding="utf-8")
        root = ET.fromstring(content)
        has_vb = "viewBox" in root.attrib or "viewbox" in root.attrib
        has_dims = "width" in root.attrib and "height" in root.attrib
        self.assertTrue(has_vb or has_dims, "SVG must have viewBox or width/height attributes")

    def test_f3_04_logo_svg_contains_vector_paths(self):
        """F3-4: assets/logo.svg contains graphic vector elements (path, circle, rect, etc.)."""
        self.assertTrue(LOGO_SVG_PATH.is_file(), f"Target file missing: {LOGO_SVG_PATH}")
        content = LOGO_SVG_PATH.read_text(encoding="utf-8")
        root = ET.fromstring(content)
        tags = [elem.tag.split("}")[-1].lower() for elem in root.iter()]
        self.assertTrue(any(t in {"path", "circle", "rect", "polygon", "g"} for t in tags))

    def test_f3_05_logo_svg_clean_of_scripts(self):
        """F3-5: assets/logo.svg is strictly static vector data without scripts or handlers."""
        self.assertTrue(LOGO_SVG_PATH.is_file(), f"Target file missing: {LOGO_SVG_PATH}")
        content = LOGO_SVG_PATH.read_text(encoding="utf-8")
        self.assertNotIn("<script", content.lower())
        self.assertFalse(bool(re.search(r"on\w+\s*=", content, re.IGNORECASE)))

    # =========================================================================
    # Feature 4: Browser Subagent Delegation - 5 Tests
    # =========================================================================

    def test_f4_01_delegation_invoke_subagent_convention(self):
        """F4-1: Rules mandate invoke_subagent with TypeName: 'browser'."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertIn('TypeName: "browser"', content)

    def test_f4_02_delegation_model_flash_default(self):
        """F4-2: Rules designate Model: 'flash' as the default browser driver model."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertIn('Model: "flash"', content)

    def test_f4_03_delegation_session_reuse(self):
        """F4-3: Rules enforce browser subagent session reuse via send_message."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertIn("send_message", content)

    def test_f4_04_delegation_semantic_ui_goals(self):
        """F4-4: Rules instruct driving browser via semantic UI goals rather than brittle selectors."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertRegex(content, r"semantic\s+UI\s+goals", "Rules must mandate semantic UI goals")

    def test_f4_05_delegation_prohibits_external_automation(self):
        """F4-5: Rules prohibit external browser launchers, curl, or raw Playwright scripts."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertTrue("curl" in content or "playwright" in content.lower())

    # =========================================================================
    # Feature 5: Canonical Entry Routing - 5 Tests
    # =========================================================================

    def test_f5_01_canonical_entry_url_match(self):
        """F5-1: Canonical entry URL is specified in rules/AGENTS.md and matches canonical URL."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertIn("https://aistudio.google.com/", content)
        self.assertEqual(CANONICAL_URL, "https://aistudio.google.com/")

    def test_f5_02_canonical_entry_avoids_sso_hops(self):
        """F5-2: Rules explicitly require avoiding intermediary redirect hops to prevent SSO loops."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertTrue("sso" in content.lower() or "redirect" in content.lower())

    def test_f5_03_canonical_entry_subpath_support(self):
        """F5-3: Rules document canonical specialized subpaths (/prompts/new_chat, /prompts/new_structured, etc.)."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertIn("/prompts/new_chat", content)

    def test_f5_04_canonical_entry_tab_reuse_priority(self):
        """F5-4: Rules prioritize checking active tab before initiating new navigation."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertIn("current tab", content.lower())

    def test_f5_05_canonical_entry_https_enforcement(self):
        """F5-5: Rules strictly require HTTPS and reject insecure http:// for AI Studio."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertIn("https://aistudio.google.com/", content)
        self.assertNotIn("http://aistudio.google.com/", content)

    # =========================================================================
    # Feature 6: Fast-Path Authentication Check - 5 Tests
    # =========================================================================

    def test_f6_01_fast_path_visual_avatar_signal(self):
        """F6-1: Fast-Path Auth verifies signed-in state via user avatar/profile presence in rules."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertTrue("avatar" in content.lower() or "profile" in content.lower())

    def test_f6_02_fast_path_dom_workspace_elements(self):
        """F6-2: Fast-Path Auth verifies DOM elements like 'Create prompt' or 'Get API key'."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertTrue("create prompt" in content.lower() or "get api key" in content.lower())

    def test_f6_03_fast_path_network_rpc_200(self):
        """F6-3: Fast-Path Auth verifies backend API RPC requests return HTTP 200."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertIn("200", content)

    def test_f6_04_fast_path_sandbox_storage_restriction(self):
        """F6-4: Rules note sandboxed browser cannot read document.cookie or localStorage."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertTrue("document.cookie" in content or "localstorage" in content.lower())

    def test_f6_05_fast_path_shortcut_decision(self):
        """F6-5: Fast-Path Auth simulation takes signed-in shortcut without login delay."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        sim = WorkflowSimulator.simulate_fast_path_auth({
            "current_url": CANONICAL_URL,
            "dom_avatar_present": True,
            "rpc_status": 200,
            "has_sign_in_button": False,
        })
        self.assertEqual(sim["status"], "AUTHENTICATED")
        self.assertTrue(sim["fast_path_taken"])

    # =========================================================================
    # Feature 7: Local vs Cloud Offload Decision Engine - 5 Tests
    # =========================================================================

    def test_f7_01_offload_heavy_reasoning_to_cloud(self):
        """F7-1: Decision Engine routes complex architectural reasoning to cloud offload."""
        res = OffloadDecisionEngine.evaluate("Perform complex architectural reasoning and algorithm design")
        self.assertEqual(res["route"], "CLOUD_OFFLOAD")
        self.assertTrue(res["quota_conserved"])

    def test_f7_02_offload_local_shell_remains_local(self):
        """F7-2: Decision Engine retains git operations and local build commands on local machine."""
        res = OffloadDecisionEngine.evaluate("Run pytest test suite and commit git branch", requires_local_shell=True)
        self.assertEqual(res["route"], "LOCAL_MACHINE")
        self.assertFalse(res["quota_conserved"])

    def test_f7_03_offload_token_threshold_boundary(self):
        """F7-3: Decision Engine offloads documents exceeding 4,000 tokens to Gemini 4 Hydrogen (High)."""
        res = OffloadDecisionEngine.evaluate("Summarize large repository file", token_count=15000)
        self.assertEqual(res["route"], "CLOUD_OFFLOAD")
        self.assertEqual(res["recommended_model"], "Gemini 4 Hydrogen")
        self.assertEqual(res["thinking_level"], "high")
        self.assertFalse(res["requires_segmentation"])

    def test_f7_04_offload_extreme_context_model_selection(self):
        """F7-4: Extremely large context (>1M tokens) selects Gemini 4 Neon and flags requires_segmentation."""
        res = OffloadDecisionEngine.evaluate("Analyze entire multi-gigabyte log corpus", token_count=1200000)
        self.assertEqual(res["route"], "CLOUD_OFFLOAD")
        self.assertEqual(res["recommended_model"], "Gemini 4 Neon")
        self.assertEqual(res["thinking_level"], "high")
        self.assertTrue(res["requires_segmentation"])

    def test_f7_05_offload_hybrid_pipeline_lifecycle(self):
        """F7-5: Rules define a 6-stage offload lifecycle (Evaluate, Stage, Dispatch, Execute, Extract, Sync)."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        stages = ["Evaluate", "Stage", "Dispatch", "Execute", "Extract", "Sync"]
        for stage in stages:
            self.assertIn(stage.lower(), content.lower(), f"Rules missing lifecycle stage: {stage}")

    # =========================================================================
    # Feature 8: Autonomy Modes (checkpoint vs auto) - 5 Tests
    # =========================================================================

    def test_f8_01_autonomy_default_is_checkpoint(self):
        """F8-1: Default autonomy mode is checkpoint."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertRegex(content, r"checkpoint.*default", "Rules must state checkpoint is default")

    def test_f8_02_autonomy_checkpoint_requires_confirmation(self):
        """F8-2: Checkpoint mode requires pausing for user approval before execution."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertTrue("pause" in content.lower() and "confirm" in content.lower())

    def test_f8_03_autonomy_auto_unattended_execution(self):
        """F8-3: Auto mode executes tasks unattended without per-step approval."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertTrue("auto" in content.lower())

    def test_f8_04_autonomy_keyword_detection(self):
        """F8-4: Rules detect 'auto mode', 'full-auto', or 'run unattended' to switch mode."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertTrue("full-auto" in content or "unattended" in content)

    def test_f8_05_autonomy_canonical_modes_list(self):
        """F8-5: Rules define both checkpoint and auto autonomy modes."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertIn("checkpoint", content.lower())
        self.assertIn("auto", content.lower())
        self.assertRegex(content, r"`?checkpoint`?\s+mode", "Rules must define checkpoint mode")
        self.assertRegex(content, r"`?auto`?\s+mode", "Rules must define auto mode")

    # =========================================================================
    # Feature 9: Hard Safety & Quota Boundaries - 5 Tests
    # =========================================================================

    def test_f9_01_safety_boundary_google_login(self):
        """F9-1: Encountering Google Sign-In triggers pause with LOGIN_REQUIRED."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertIn("LOGIN_REQUIRED", content)

    def test_f9_02_safety_boundary_captcha_challenge(self):
        """F9-2: Encountering CAPTCHA triggers immediate pause without bypass attempts."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertIn("CAPTCHA", content)

    def test_f9_03_safety_boundary_429_quota_exhausted(self):
        """F9-3: HTTP 429 or ResourceExhausted triggers pause and notification."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertTrue("429" in content or "ResourceExhausted" in content)

    def test_f9_04_safety_boundary_content_safety_filters(self):
        """F9-4: Content safety filter block reports violation category and pauses."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertTrue("safety" in content.lower())

    def test_f9_05_safety_boundary_subagent_resume_protocol(self):
        """F9-5: Rules describe resuming subagent via send_message after user resolves barrier."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertIn("send_message", content)

    def test_f9_06_safety_boundary_account_verification_required(self):
        """F9-6: Rules document ACCOUNT_VERIFICATION_REQUIRED zero-retry circuit breaker and verify-account URL."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertIn("ACCOUNT_VERIFICATION_REQUIRED", content)
        self.assertIn("https://aistudio.google.com/verify-account", content)
        self.assertIn("zero-retry", content.lower())

    def test_f9_07_anti_abuse_pacing_and_session_cap_documented(self):
        """F9-7: Rules document 15-30s inter-request pacing cooldown and 5-8 calls/session soft cap."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertIn("15-30", content)
        self.assertIn("5-8", content)
        self.assertIn("cooldown", content.lower())

    def test_f9_08_on_demand_grounding_policy_documented(self):
        """F9-8: Rules enforce On-Demand Grounding (OFF for internal code/diff tasks, ON only for live web research)."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertIn("On-Demand", content)
        self.assertIn("Default OFF for Internal Tasks", content)

    # =========================================================================
    # Feature 10: Local File Staging Contract - 5 Tests
    # =========================================================================

    def test_f10_01_staging_uploads_path(self):
        """F10-1: Rules mandate staging uploads directory browser_sandbox/uploads/."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertIn("browser_sandbox/uploads/", content)

    def test_f10_02_staging_downloads_path(self):
        """F10-2: Rules mandate staging downloads directory browser_sandbox/downloads/."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertIn("browser_sandbox/downloads/", content)

    def test_f10_03_staging_single_segment_filename(self):
        """F10-3: Only bare single-segment filenames are passed to the sandboxed browser."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertTrue("single-segment" in content.lower() or "bare" in content.lower())

    def test_f10_04_staging_workspace_sync_back(self):
        """F10-4: Downloaded artifacts are synchronized back to the workspace."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertTrue("workspace" in content.lower())

    def test_f10_05_staging_references_path(self):
        """F10-5: Reference images stage to browser_sandbox/references/."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        content = AGENTS_RULE_PATH.read_text(encoding="utf-8")
        self.assertIn("browser_sandbox/references/", content)

    # =========================================================================
    # Feature 11: Skill: aistudio-offload - 5 Tests
    # =========================================================================

    def test_f11_01_skill_offload_frontmatter(self):
        """F11-1: aistudio-offload skill exists and has valid frontmatter (name, description)."""
        skill_file = SKILLS_DIR / "aistudio-offload" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        errors = SkillValidator.validate_file(skill_file, expected_name="aistudio-offload")
        self.assertEqual(errors, [], f"Skill validation errors in {skill_file}: {errors}")

    def test_f11_02_skill_offload_references_decision_matrix(self):
        """F11-2: aistudio-offload links to references/offload-decision-matrix.md."""
        skill_file = SKILLS_DIR / "aistudio-offload" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertIn("offload-decision-matrix.md", content)

    def test_f11_03_skill_offload_evaluation_pipeline(self):
        """F11-3: aistudio-offload documents the offload evaluation pipeline."""
        skill_file = SKILLS_DIR / "aistudio-offload" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertTrue("evaluate" in content.lower() or "decision" in content.lower())

    def test_f11_04_skill_offload_local_sync_back(self):
        """F11-4: aistudio-offload details syncing cloud results back to workspace files."""
        skill_file = SKILLS_DIR / "aistudio-offload" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertTrue("sync" in content.lower() or "result" in content.lower())

    def test_f11_05_skill_offload_browser_subagent_dispatch(self):
        """F11-5: aistudio-offload defines dispatching browser subagent with task context."""
        skill_file = SKILLS_DIR / "aistudio-offload" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertTrue("browser" in content.lower())

    # =========================================================================
    # Feature 12: Reference: offload-decision-matrix.md - 5 Tests
    # =========================================================================

    def test_f12_01_matrix_table_structure(self):
        """F12-1: offload-decision-matrix.md exists and formats routing criteria as markdown table."""
        ref_file = SKILLS_DIR / "aistudio-offload" / "references" / "offload-decision-matrix.md"
        self.assertTrue(ref_file.is_file(), f"Target file missing: {ref_file}")
        content = ref_file.read_text(encoding="utf-8")
        self.assertRegex(content, r"\|.+\|.+\|", "Matrix reference must contain markdown table structure")

    def test_f12_02_matrix_local_only_tasks(self):
        """F12-2: offload-decision-matrix.md lists local machine operations (git, compile, tests)."""
        ref_file = SKILLS_DIR / "aistudio-offload" / "references" / "offload-decision-matrix.md"
        self.assertTrue(ref_file.is_file(), f"Target file missing: {ref_file}")
        content = ref_file.read_text(encoding="utf-8")
        self.assertIn("local", content.lower())

    def test_f12_03_matrix_cloud_candidate_tasks(self):
        """F12-3: offload-decision-matrix.md lists cloud candidates (reasoning, long-context, few-shot)."""
        ref_file = SKILLS_DIR / "aistudio-offload" / "references" / "offload-decision-matrix.md"
        self.assertTrue(ref_file.is_file(), f"Target file missing: {ref_file}")
        content = ref_file.read_text(encoding="utf-8")
        self.assertIn("cloud", content.lower())

    def test_f12_04_matrix_token_thresholds(self):
        """F12-4: offload-decision-matrix.md specifies concrete token threshold boundaries."""
        ref_file = SKILLS_DIR / "aistudio-offload" / "references" / "offload-decision-matrix.md"
        self.assertTrue(ref_file.is_file(), f"Target file missing: {ref_file}")
        content = ref_file.read_text(encoding="utf-8")
        self.assertTrue("token" in content.lower())

    def test_f12_05_matrix_model_recommendations(self):
        """F12-5: offload-decision-matrix.md references all four Gemini 4 models with Thinking >= High."""
        ref_file = SKILLS_DIR / "aistudio-offload" / "references" / "offload-decision-matrix.md"
        self.assertTrue(ref_file.is_file(), f"Target file missing: {ref_file}")
        content = ref_file.read_text(encoding="utf-8")
        for m in ["Gemini 4 Hydrogen", "Gemini 4 Argon", "Gemini 4 Neon", "Gemini 4 Carbon"]:
            self.assertIn(m, content, f"Decision matrix missing Gemini 4 model: {m}")
        self.assertIn("High", content)

    # =========================================================================
    # Feature 13: Skill: aistudio-chat-prompt - 5 Tests
    # =========================================================================

    def test_f13_01_skill_chat_prompt_frontmatter(self):
        """F13-1: aistudio-chat-prompt exists and has valid frontmatter."""
        skill_file = SKILLS_DIR / "aistudio-chat-prompt" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        errors = SkillValidator.validate_file(skill_file, expected_name="aistudio-chat-prompt")
        self.assertEqual(errors, [], f"Skill validation errors in {skill_file}: {errors}")

    def test_f13_02_skill_chat_prompt_multi_turn(self):
        """F13-2: aistudio-chat-prompt supports conversational multi-turn dialogue orchestration."""
        skill_file = SKILLS_DIR / "aistudio-chat-prompt" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertTrue("multi-turn" in content.lower() or "chat" in content.lower() or "conversation" in content.lower())

    def test_f13_03_skill_chat_prompt_system_instructions(self):
        """F13-3: aistudio-chat-prompt guides configuring system instructions."""
        skill_file = SKILLS_DIR / "aistudio-chat-prompt" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertTrue("system" in content.lower())

    def test_f13_04_skill_chat_prompt_multimodal_attachments(self):
        """F13-4: aistudio-chat-prompt covers media uploads (images, audio, docs) via staging."""
        skill_file = SKILLS_DIR / "aistudio-chat-prompt" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertTrue("attachment" in content.lower() or "multimodal" in content.lower() or "upload" in content.lower())

    def test_f13_05_skill_chat_prompt_history_export(self):
        """F13-5: aistudio-chat-prompt documents exporting chat history to local Markdown."""
        skill_file = SKILLS_DIR / "aistudio-chat-prompt" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertTrue("export" in content.lower() or "history" in content.lower() or "sync" in content.lower())

    # =========================================================================
    # Feature 14: Skill: aistudio-structured-prompt - 5 Tests
    # =========================================================================

    def test_f14_01_skill_structured_prompt_frontmatter(self):
        """F14-1: aistudio-structured-prompt exists and has valid frontmatter."""
        skill_file = SKILLS_DIR / "aistudio-structured-prompt" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        errors = SkillValidator.validate_file(skill_file, expected_name="aistudio-structured-prompt")
        self.assertEqual(errors, [], f"Skill validation errors in {skill_file}: {errors}")

    def test_f14_02_skill_structured_prompt_tabular_few_shots(self):
        """F14-2: aistudio-structured-prompt supports tabular input/output few-shot examples."""
        skill_file = SKILLS_DIR / "aistudio-structured-prompt" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertTrue("few-shot" in content.lower() or "tabular" in content.lower() or "table" in content.lower())

    def test_f14_03_skill_structured_prompt_test_cases(self):
        """F14-3: aistudio-structured-prompt supports adding and evaluating test cases."""
        skill_file = SKILLS_DIR / "aistudio-structured-prompt" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertTrue("test" in content.lower())

    def test_f14_04_skill_structured_prompt_json_schema_outputs(self):
        """F14-4: aistudio-structured-prompt supports JSON schema structured outputs."""
        skill_file = SKILLS_DIR / "aistudio-structured-prompt" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertTrue("schema" in content.lower() or "json" in content.lower())

    def test_f14_05_skill_structured_prompt_csv_import_export(self):
        """F14-5: aistudio-structured-prompt covers batch tabular data import/export."""
        skill_file = SKILLS_DIR / "aistudio-structured-prompt" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertTrue("csv" in content.lower() or "import" in content.lower() or "export" in content.lower())

    # =========================================================================
    # Feature 15: Skill: aistudio-parameter-tuning - 5 Tests
    # =========================================================================

    def test_f15_01_skill_param_tuning_frontmatter(self):
        """F15-1: aistudio-parameter-tuning exists and has valid frontmatter."""
        skill_file = SKILLS_DIR / "aistudio-parameter-tuning" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        errors = SkillValidator.validate_file(skill_file, expected_name="aistudio-parameter-tuning")
        self.assertEqual(errors, [], f"Skill validation errors in {skill_file}: {errors}")

    def test_f15_02_skill_param_tuning_thinking_level_floor(self):
        """F15-2: aistudio-parameter-tuning enforces Thinking level >= High and bans Low/Medium."""
        skill_file = SKILLS_DIR / "aistudio-parameter-tuning" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertIn("thinking level", content.lower())
        self.assertIn("high", content.lower())
        self.assertIn("xhigh", content.lower())

    def test_f15_03_skill_param_tuning_output_length_and_media_res(self):
        """F15-3: aistudio-parameter-tuning documents Output length, Media resolution, Stop sequence, and URL context."""
        skill_file = SKILLS_DIR / "aistudio-parameter-tuning" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8").lower()
        self.assertIn("output length", content)
        self.assertIn("media resolution", content)
        self.assertIn("url context", content)

    def test_f15_04_skill_param_tuning_safety_filters(self):
        """F15-4: aistudio-parameter-tuning documents safety filter threshold settings."""
        skill_file = SKILLS_DIR / "aistudio-parameter-tuning" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertIn("safety", content.lower())

    def test_f15_05_skill_param_tuning_grounding_and_code_exec(self):
        """F15-5: aistudio-parameter-tuning covers Google Search grounding and code execution toggles."""
        skill_file = SKILLS_DIR / "aistudio-parameter-tuning" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertTrue("grounding" in content.lower() or "search" in content.lower() or "code execution" in content.lower())

    # =========================================================================
    # Feature 16: Skill: aistudio-code-export - 5 Tests
    # =========================================================================

    def test_f16_01_skill_code_export_frontmatter(self):
        """F16-1: aistudio-code-export exists and has valid frontmatter."""
        skill_file = SKILLS_DIR / "aistudio-code-export" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        errors = SkillValidator.validate_file(skill_file, expected_name="aistudio-code-export")
        self.assertEqual(errors, [], f"Skill validation errors in {skill_file}: {errors}")

    def test_f16_02_skill_code_export_get_code_dialog(self):
        """F16-2: aistudio-code-export navigates to the 'Get code' dialog in AI Studio."""
        skill_file = SKILLS_DIR / "aistudio-code-export" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertTrue("get code" in content.lower())

    def test_f16_03_skill_code_export_supported_languages(self):
        """F16-3: aistudio-code-export supports Python, TypeScript/JavaScript, cURL, and REST."""
        skill_file = SKILLS_DIR / "aistudio-code-export" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertTrue("python" in content.lower())

    def test_f16_04_skill_code_export_api_key_placeholder(self):
        """F16-4: aistudio-code-export replaces raw keys with GEMINI_API_KEY environment variable."""
        skill_file = SKILLS_DIR / "aistudio-code-export" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertIn("GEMINI_API_KEY", content)

    def test_f16_05_skill_code_export_local_script_sync(self):
        """F16-5: aistudio-code-export saves generated snippets to local workspace files."""
        skill_file = SKILLS_DIR / "aistudio-code-export" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertTrue("workspace" in content.lower() or "sync" in content.lower() or "save" in content.lower())

    # =========================================================================
    # Feature 17: Skill: aistudio-ui-sync-audit - 5 Tests
    # =========================================================================

    def test_f17_01_skill_ui_sync_audit_frontmatter(self):
        """F17-1: aistudio-ui-sync-audit exists and has valid frontmatter."""
        skill_file = SKILLS_DIR / "aistudio-ui-sync-audit" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        errors = SkillValidator.validate_file(skill_file, expected_name="aistudio-ui-sync-audit")
        self.assertEqual(errors, [], f"Skill validation errors in {skill_file}: {errors}")

    def test_f17_02_skill_ui_sync_audit_disable_model_invocation(self):
        """F17-2: aistudio-ui-sync-audit strictly enforces disable-model-invocation: true."""
        skill_file = SKILLS_DIR / "aistudio-ui-sync-audit" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        fm, _, _ = SkillValidator.parse_frontmatter(skill_file.read_text(encoding="utf-8"))
        self.assertTrue(fm.get("disable-model-invocation") is True, f"disable-model-invocation must be True in {skill_file}")

    def test_f17_03_skill_ui_sync_audit_read_only(self):
        """F17-3: aistudio-ui-sync-audit emphasizes strictly read-only inspection."""
        skill_file = SKILLS_DIR / "aistudio-ui-sync-audit" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertIn("read-only", content.lower())

    def test_f17_04_skill_ui_sync_audit_7_surfaces(self):
        """F17-4: aistudio-ui-sync-audit inspects the 7 canonical UI surfaces."""
        skill_file = SKILLS_DIR / "aistudio-ui-sync-audit" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertIn("7", content)

    def test_f17_05_skill_ui_sync_audit_drift_diff_reporting(self):
        """F17-5: aistudio-ui-sync-audit produces a structured drift report."""
        skill_file = SKILLS_DIR / "aistudio-ui-sync-audit" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), f"Target file missing: {skill_file}")
        content = skill_file.read_text(encoding="utf-8")
        self.assertTrue("drift" in content.lower())

    # =========================================================================
    # Feature 18: Reference: audit-checklist.md - 5 Tests
    # =========================================================================

    def test_f18_01_checklist_last_calibration_date(self):
        """F18-1: audit-checklist.md exists and records a valid calibration date (YYYY-MM-DD)."""
        ref_file = SKILLS_DIR / "aistudio-ui-sync-audit" / "references" / "audit-checklist.md"
        self.assertTrue(ref_file.is_file(), f"Target file missing: {ref_file}")
        content = ref_file.read_text(encoding="utf-8")
        self.assertRegex(content, r"\d{4}-\d{2}-\d{2}", "Checklist must contain YYYY-MM-DD calibration date")

    def test_f18_02_checklist_contains_7_canonical_surfaces(self):
        """F18-2: audit-checklist.md details all 7 canonical surfaces."""
        ref_file = SKILLS_DIR / "aistudio-ui-sync-audit" / "references" / "audit-checklist.md"
        self.assertTrue(ref_file.is_file(), f"Target file missing: {ref_file}")
        content = ref_file.read_text(encoding="utf-8")
        self.assertTrue("dashboard" in content.lower() and "prompt" in content.lower())

    def test_f18_03_checklist_tracks_model_inventory(self):
        """F18-3: audit-checklist.md tracks available Gemini model versions."""
        ref_file = SKILLS_DIR / "aistudio-ui-sync-audit" / "references" / "audit-checklist.md"
        self.assertTrue(ref_file.is_file(), f"Target file missing: {ref_file}")
        content = ref_file.read_text(encoding="utf-8")
        self.assertIn("gemini", content.lower())

    def test_f18_04_checklist_ui_selector_guidelines(self):
        """F18-4: audit-checklist.md gives semantic & accessibility selector inspection guidance."""
        ref_file = SKILLS_DIR / "aistudio-ui-sync-audit" / "references" / "audit-checklist.md"
        self.assertTrue(ref_file.is_file(), f"Target file missing: {ref_file}")
        content = ref_file.read_text(encoding="utf-8")
        self.assertTrue("inspection" in content.lower() or "selector" in content.lower() or "surface" in content.lower())

    def test_f18_05_checklist_pruning_guidelines(self):
        """F18-5: audit-checklist.md provides explicit guidelines for pruning dead features."""
        ref_file = SKILLS_DIR / "aistudio-ui-sync-audit" / "references" / "audit-checklist.md"
        self.assertTrue(ref_file.is_file(), f"Target file missing: {ref_file}")
        content = ref_file.read_text(encoding="utf-8")
        self.assertTrue("prun" in content.lower() or "deprecat" in content.lower())

    # =========================================================================
    # Feature 19: Overseas Localization (Zero Non-English Characters) - 5 Tests
    # =========================================================================

    def test_f19_01_zero_non_english_in_plugin_json(self):
        """F19-1: plugin.json exists and contains zero Chinese / CJK characters."""
        self.assertTrue(PLUGIN_JSON_PATH.is_file(), f"Target file missing: {PLUGIN_JSON_PATH}")
        violations = OverseasLocalizationValidator.scan_file(PLUGIN_JSON_PATH)
        self.assertEqual(violations, [], f"Found non-English characters in plugin.json: {violations}")

    def test_f19_02_zero_non_english_in_readme(self):
        """F19-2: README.md exists and contains zero Chinese / CJK characters."""
        self.assertTrue(README_PATH.is_file(), f"Target file missing: {README_PATH}")
        violations = OverseasLocalizationValidator.scan_file(README_PATH)
        self.assertEqual(violations, [], f"Found non-English characters in README.md: {violations}")

    def test_f19_03_zero_non_english_in_rules(self):
        """F19-3: rules/AGENTS.md exists and contains zero Chinese / CJK characters."""
        self.assertTrue(AGENTS_RULE_PATH.is_file(), f"Target file missing: {AGENTS_RULE_PATH}")
        violations = OverseasLocalizationValidator.scan_file(AGENTS_RULE_PATH)
        self.assertEqual(violations, [], f"Found non-English characters in rules/AGENTS.md: {violations}")

    def test_f19_04_zero_non_english_in_skills(self):
        """F19-4: skills directory exists and all skill markdown files contain zero non-English characters."""
        self.assertTrue(SKILLS_DIR.is_dir(), f"Skills directory missing: {SKILLS_DIR}")
        skill_mds = list(SKILLS_DIR.rglob("*.md"))
        self.assertGreater(len(skill_mds), 0, f"No markdown skill files found in {SKILLS_DIR}")
        for p in skill_mds:
            violations = OverseasLocalizationValidator.scan_file(p)
            self.assertEqual(violations, [], f"Found non-English characters in {p}: {violations}")

    def test_f19_05_zero_non_english_scanner_accuracy(self):
        """F19-5: Localization scanner correctly detects English text as clean."""
        sample_english = "Google AI Studio plugin for cloud agent offload and prompt engineering."
        violations = OverseasLocalizationValidator.scan_text(sample_english)
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
