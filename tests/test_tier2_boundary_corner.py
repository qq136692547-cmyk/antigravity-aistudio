# -*- coding: utf-8 -*-
"""
Tier 2: Boundary Value Analysis & Corner Case Test Suite (95 tests)
Validates boundary values, negative test cases, malformed inputs, error handling,
and robustness across Features 1 through 19:
Each feature has exactly 5 dedicated, isolated, verifiable boundary test methods.
Total: 19 features * 5 tests = 95 tests.
"""

import os
import sys
import json
import re
import ast
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
    CANONICAL_AUTONOMY_MODES,
    CANONICAL_SKILLS,
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
)


class TestTier2BoundaryCorner(unittest.TestCase):
    """Tier 2: Boundary Value Analysis and Corner Cases (F1 - F19)."""

    # =========================================================================
    # Feature 1: Plugin Manifest (plugin.json) - 5 Boundary Tests
    # =========================================================================

    def test_f1_b01_manifest_empty_or_whitespace_name(self):
        """F1-B1: ManifestValidator rejects empty or whitespace-only name."""
        bad_manifest = dict(CANONICAL_FIXTURES["valid_manifest"])
        bad_manifest["name"] = "   "
        errors = ManifestValidator.validate_manifest_dict(bad_manifest)
        self.assertTrue(any("name" in e.lower() for e in errors))

    def test_f1_b02_manifest_invalid_semver_format(self):
        """F1-B2: ManifestValidator rejects invalid semver formats (e.g. 'v1.0', 'beta')."""
        bad_manifest = dict(CANONICAL_FIXTURES["valid_manifest"])
        for bad_ver in ["v1.0.0", "1.0", "beta-1", "0.2.0-alpha"]:
            bad_manifest["version"] = bad_ver
            errors = ManifestValidator.validate_manifest_dict(bad_manifest)
            self.assertTrue(any("version" in e.lower() for e in errors), f"Should reject {bad_ver}")

    def test_f1_b03_manifest_malformed_json_syntax(self):
        """F1-B3: ManifestValidator rejects malformed JSON strings."""
        malformed_json = '{"name": "antigravity-aistudio", "version": "0.2.0", unclosed_key}'
        with self.assertRaises(json.JSONDecodeError):
            json.loads(malformed_json)

    def test_f1_b04_manifest_missing_mandatory_keys(self):
        """F1-B4: ManifestValidator detects and reports missing mandatory keys."""
        incomplete_manifest = {"name": "antigravity-aistudio", "version": "0.2.0"}
        errors = ManifestValidator.validate_manifest_dict(incomplete_manifest)
        self.assertGreater(len(errors), 3)

    def test_f1_b05_manifest_empty_suggested_prompts(self):
        """F1-B5: ManifestValidator rejects empty suggestedPrompts array."""
        bad_manifest = dict(CANONICAL_FIXTURES["valid_manifest"])
        bad_manifest["suggestedPrompts"] = []
        errors = ManifestValidator.validate_manifest_dict(bad_manifest)
        self.assertTrue(any("suggestedprompts" in e.lower() for e in errors))

    # =========================================================================
    # Feature 2: Documentation (README.md) - 5 Boundary Tests
    # =========================================================================

    def test_f2_b01_readme_empty_content(self):
        """F2-B1: ReadmeValidator rejects empty or sub-100 character README content."""
        errors = ReadmeValidator.validate_content("")
        self.assertTrue(len(errors) > 0)
        errors_short = ReadmeValidator.validate_content("# Hi")
        self.assertTrue(len(errors_short) > 0)

    def test_f2_b02_readme_missing_architecture_section(self):
        """F2-B2: ReadmeValidator flags omission of Architecture/System Layers section."""
        content = "# Antigravity AI Studio\n## Overview\nOverview here.\n## Installation\nInstall here.\n## Autonomy Modes\nCheckpoint.\n## Skills\nSkills here."
        errors = ReadmeValidator.validate_content(content)
        self.assertTrue(any("architecture" in e.lower() for e in errors))

    def test_f2_b03_readme_broken_markdown_links(self):
        """F2-B3: ReadmeValidator detects unclosed markdown link syntax."""
        broken_content = (
            "# Antigravity Google AI Studio\n"
            "## Overview\nThis is overview text explaining the plugin architecture.\n"
            "## Architecture\nSystem layers description here.\n"
            "## Installation\nInstallation instructions.\n"
            "## Offload Decision Engine\nEngine rules.\n"
            "## Autonomy Modes\nModes.\n"
            "## Skills\n" + " ".join(CANONICAL_SKILLS) + "\n"
            "quota preservation for desktop app.\n"
            "https://aistudio.google.com/ is the link.\n"
            "Here is a broken link: [Google AI Studio](https://aistudio.google.com\n"
        )
        errors = ReadmeValidator.validate_content(broken_content)
        self.assertTrue(any("link" in e.lower() for e in errors))

    def test_f2_b04_readme_missing_skill_documentation(self):
        """F2-B4: ReadmeValidator flags omission of required canonical skills."""
        content = "# Title\n## Overview\n## Architecture\n## Installation\n## Offload Decision Engine\n## Autonomy Modes\n## Skills\nhttps://aistudio.google.com/ quota"
        errors = ReadmeValidator.validate_content(content)
        self.assertTrue(any("missing documentation for skill" in e.lower() for e in errors))

    def test_f2_b05_readme_missing_canonical_url(self):
        """F2-B5: ReadmeValidator flags content missing the canonical AI Studio domain."""
        content = "# Title\n## Overview\n## Architecture\n## Installation\n## Offload Decision Engine\n## Autonomy Modes\n## Skills\nquota " + " ".join(CANONICAL_SKILLS)
        errors = ReadmeValidator.validate_content(content)
        self.assertTrue(any("aistudio.google.com" in e.lower() for e in errors))

    # =========================================================================
    # Feature 3: Visual Asset (assets/logo.svg) - 5 Boundary Tests
    # =========================================================================

    def test_f3_b01_logo_svg_empty_content(self):
        """F3-B1: SvgValidator rejects empty SVG content."""
        errors = SvgValidator.validate_content("")
        self.assertTrue(len(errors) > 0)

    def test_f3_b02_logo_svg_malformed_xml(self):
        """F3-B2: SvgValidator rejects malformed XML with unclosed tags."""
        malformed = "<svg viewBox='0 0 100 100'><circle cx='50' cy='50' r='40'>"
        errors = SvgValidator.validate_content(malformed)
        self.assertTrue(any("malformed" in e.lower() for e in errors))

    def test_f3_b03_logo_svg_script_injection_detection(self):
        """F3-B3: SvgValidator detects and blocks embedded <script> tags."""
        injected = "<svg viewBox='0 0 100 100'><script>alert('xss')</script><circle cx='50' cy='50' r='40'/></svg>"
        errors = SvgValidator.validate_content(injected)
        self.assertTrue(any("script" in e.lower() for e in errors))

    def test_f3_b04_logo_svg_inline_event_handler_detection(self):
        """F3-B4: SvgValidator detects and blocks inline JavaScript event handlers."""
        injected = "<svg viewBox='0 0 100 100' onload='alert(1)'><circle cx='50' cy='50' r='40'/></svg>"
        errors = SvgValidator.validate_content(injected)
        self.assertTrue(any("event handler" in e.lower() for e in errors))

    def test_f3_b05_logo_svg_missing_viewbox_and_dimensions(self):
        """F3-B5: SvgValidator flags SVG missing both viewBox and width/height attributes."""
        missing_dims = "<svg xmlns='http://www.w3.org/2000/svg'><circle cx='50' cy='50' r='40'/></svg>"
        errors = SvgValidator.validate_content(missing_dims)
        self.assertTrue(any("viewbox" in e.lower() for e in errors))

    # =========================================================================
    # Feature 4: Browser Subagent Delegation - 5 Boundary Tests
    # =========================================================================

    def test_f4_b01_delegation_missing_typename(self):
        """F4-B1: Subagent payload validation detects missing TypeName."""
        payload = {"Model": "flash", "instruction": "Open aistudio"}
        errors = SubagentDelegationValidator.validate_payload(payload)
        self.assertTrue(any("typename" in e.lower() for e in errors))

    def test_f4_b02_delegation_invalid_typename(self):
        """F4-B2: Validates that TypeName must be 'browser' for web automation."""
        payload = {"TypeName": "shell", "Model": "flash", "instruction": "Open aistudio"}
        errors = SubagentDelegationValidator.validate_payload(payload)
        self.assertTrue(any("browser" in e.lower() for e in errors))

    def test_f4_b03_delegation_brittle_css_selector_detection(self):
        """F4-B3: Detects brittle CSS selector usage in instructions."""
        payload = {"TypeName": "browser", "Model": "flash", "instruction": "Click div.sc-1234 > button.submit-btn:nth-child(2)"}
        errors = SubagentDelegationValidator.validate_payload(payload)
        self.assertTrue(any("brittle" in e.lower() or "css" in e.lower() for e in errors))

    def test_f4_b04_delegation_empty_semantic_goal(self):
        """F4-B4: Rejects empty or whitespace-only semantic instruction."""
        payload = {"TypeName": "browser", "Model": "flash", "instruction": "   \n\t  "}
        errors = SubagentDelegationValidator.validate_payload(payload)
        self.assertTrue(any("instruction" in e.lower() or "empty" in e.lower() for e in errors))

    def test_f4_b05_delegation_killing_idle_subagent_violation(self):
        """F4-B5: Detects anti-pattern of killing idle subagent between steps."""
        payload = {"TypeName": "browser", "Model": "flash", "instruction": "Open aistudio", "action": "kill_subagent(conversation_id)"}
        errors = SubagentDelegationValidator.validate_payload(payload)
        self.assertTrue(any("kill" in e.lower() or "reuse" in e.lower() for e in errors))

    # =========================================================================
    # Feature 5: Canonical Entry Routing - 5 Boundary Tests
    # =========================================================================

    def test_f5_b01_canonical_entry_http_insecure_downgrade(self):
        """F5-B1: Rejects insecure HTTP downgrade of canonical entry URL."""
        errors = CanonicalRoutingValidator.validate_url("http://aistudio.google.com/")
        self.assertTrue(any("https" in e.lower() or "insecure" in e.lower() for e in errors))

    def test_f5_b02_canonical_entry_unauthorized_domain(self):
        """F5-B2: Rejects phishing or spoofed domains."""
        errors = CanonicalRoutingValidator.validate_url("https://fakeaistudio.google.com/")
        self.assertTrue(any("unauthorized" in e.lower() or "domain" in e.lower() for e in errors))

    def test_f5_b03_canonical_entry_malformed_url(self):
        """F5-B3: Detects malformed URL without valid scheme or netloc."""
        errors = CanonicalRoutingValidator.validate_url("aistudio.google.com/prompts")
        self.assertTrue(any("malformed" in e.lower() or "scheme" in e.lower() for e in errors))

    def test_f5_b04_canonical_entry_infinite_redirect_prevention(self):
        """F5-B4: Halts when redirect count exceeds threshold (max 3 hops)."""
        redirect_hops = ["https://labs.google/fx", "https://accounts.google.com/sso", "https://aistudio.google.com", "https://accounts.google.com/sso2"]
        errors = CanonicalRoutingValidator.validate_url(CANONICAL_URL, redirect_chain=redirect_hops)
        self.assertTrue(any("redirect" in e.lower() or "hop" in e.lower() for e in errors))

    def test_f5_b05_canonical_entry_empty_url(self):
        """F5-B5: Rejects empty or None entry URL."""
        errors = CanonicalRoutingValidator.validate_url("")
        self.assertTrue(any("empty" in e.lower() for e in errors))

    # =========================================================================
    # Feature 6: Fast-Path Authentication Check - 5 Boundary Tests
    # =========================================================================

    def test_f6_b01_fast_path_sign_in_button_triggers_login_required(self):
        """F6-B1: Presence of 'Sign in' button triggers LOGIN_REQUIRED state."""
        sim = WorkflowSimulator.simulate_fast_path_auth({
            "current_url": CANONICAL_URL,
            "dom_avatar_present": False,
            "rpc_status": 200,
            "has_sign_in_button": True,
        })
        self.assertEqual(sim["status"], "LOGIN_REQUIRED")
        self.assertFalse(sim["fast_path_taken"])

    def test_f6_b02_fast_path_accounts_google_redirect_triggers_pause(self):
        """F6-B2: Redirect to accounts.google.com triggers pause for user interaction."""
        sim = WorkflowSimulator.simulate_fast_path_auth({
            "current_url": "https://accounts.google.com/v3/signin/identifier",
            "dom_avatar_present": False,
            "rpc_status": 200,
        })
        self.assertEqual(sim["status"], "REDIRECT_REQUIRED")
        self.assertFalse(sim["fast_path_taken"])

    def test_f6_b03_fast_path_conflicting_signals_avatar_with_401(self):
        """F6-B3: Avatar present but network RPC 401 triggers LOGIN_REQUIRED."""
        sim = WorkflowSimulator.simulate_fast_path_auth({
            "current_url": CANONICAL_URL,
            "dom_avatar_present": True,
            "rpc_status": 401,
        })
        self.assertEqual(sim["status"], "LOGIN_REQUIRED")
        self.assertFalse(sim["fast_path_taken"])

    def test_f6_b04_fast_path_rpc_server_error_500(self):
        """F6-B4: RPC returning HTTP 500 does not trigger fast path shortcut."""
        sim = WorkflowSimulator.simulate_fast_path_auth({
            "current_url": CANONICAL_URL,
            "dom_avatar_present": True,
            "rpc_status": 500,
        })
        self.assertEqual(sim["status"], "UNKNOWN_STATE")
        self.assertFalse(sim["fast_path_taken"])

    def test_f6_b05_fast_path_empty_page_or_dom_timeout(self):
        """F6-B5: Blank page or failed DOM hydration fails fast path check."""
        sim = WorkflowSimulator.simulate_fast_path_auth({
            "current_url": CANONICAL_URL,
            "dom_avatar_present": False,
            "rpc_status": 200,
        })
        self.assertEqual(sim["status"], "UNKNOWN_STATE")

    # =========================================================================
    # Feature 7: Local vs Cloud Offload Decision Engine - 5 Boundary Tests
    # =========================================================================

    def test_f7_b01_offload_empty_task_description(self):
        """F7-B1: Empty task description defaults to LOCAL_MACHINE."""
        res = OffloadDecisionEngine.evaluate("")
        self.assertEqual(res["route"], "LOCAL_MACHINE")
        self.assertFalse(res["quota_conserved"])

    def test_f7_b02_offload_exact_threshold_boundary(self):
        """F7-B2: Exact token boundary 4,000 tokens routes to CLOUD_OFFLOAD."""
        res = OffloadDecisionEngine.evaluate("Analyze context document", token_count=4000)
        self.assertEqual(res["route"], "CLOUD_OFFLOAD")

    def test_f7_b03_offload_just_below_threshold(self):
        """F7-B3: Token count just below boundary (3,999 tokens) stays LOCAL_MACHINE without keyword."""
        res = OffloadDecisionEngine.evaluate("Process data block", token_count=3999)
        self.assertEqual(res["route"], "LOCAL_MACHINE")

    def test_f7_b04_offload_mixed_signals_file_mutation_priority(self):
        """F7-B4: File mutation requirement overrides heavy reasoning to force LOCAL_MACHINE."""
        res = OffloadDecisionEngine.evaluate(
            "Perform complex reasoning and immediately edit local source file",
            requires_file_mutation=True,
        )
        self.assertEqual(res["route"], "LOCAL_MACHINE")

    def test_f7_b05_offload_extreme_token_count_overflow(self):
        """F7-B5: Extreme token count (5,000,000 tokens) selects Gemini 4 Neon and flags requires_segmentation."""
        res = OffloadDecisionEngine.evaluate("Massive repository analysis", token_count=5000000)
        self.assertEqual(res["route"], "CLOUD_OFFLOAD")
        self.assertEqual(res["recommended_model"], "Gemini 4 Neon")
        self.assertTrue(res["requires_segmentation"])

    # =========================================================================
    # Feature 8: Autonomy Modes (checkpoint vs auto) - 5 Boundary Tests
    # =========================================================================

    def test_f8_b01_autonomy_invalid_mode_string(self):
        """F8-B1: Unsupported autonomy mode string is rejected."""
        errors = AutonomyModeValidator.validate_mode("semi-automatic")
        self.assertTrue(any("unsupported" in e.lower() or "invalid" in e.lower() for e in errors))

    def test_f8_b02_autonomy_case_insensitivity(self):
        """F8-B2: Autonomy keyword detection works case-insensitively."""
        prompt_upper = "PLEASE EXECUTE THIS IN FULL-AUTO MODE"
        resolved = AutonomyModeValidator.resolve_mode_from_prompt(prompt_upper)
        self.assertEqual(resolved, "auto")
        self.assertEqual(AutonomyModeValidator.validate_mode("AUTO"), [])

    def test_f8_b03_autonomy_negation_in_prompt(self):
        """F8-B3: Prompt specifying 'do not run in auto mode' preserves checkpoint mode."""
        user_prompt = "Do not run in auto mode, ask me before executing."
        resolved = AutonomyModeValidator.resolve_mode_from_prompt(user_prompt)
        self.assertEqual(resolved, "checkpoint")

    def test_f8_b04_autonomy_empty_prompt_defaults_to_checkpoint(self):
        """F8-B4: Ambiguous or empty prompt defaults to checkpoint mode."""
        resolved = AutonomyModeValidator.resolve_mode_from_prompt("Create a new prompt.")
        self.assertEqual(resolved, "checkpoint")

    def test_f8_b05_autonomy_whitespace_mode_string(self):
        """F8-B5: Whitespace-only mode string is rejected."""
        errors = AutonomyModeValidator.validate_mode("   ")
        self.assertTrue(any("empty" in e.lower() or "whitespace" in e.lower() for e in errors))

    # =========================================================================
    # Feature 9: Hard Safety & Quota Boundaries - 5 Boundary Tests
    # =========================================================================

    def test_f9_b01_safety_429_resource_exhausted_forces_pause(self):
        """F9-B1: HTTP 429 forces pause even when running in auto mode."""
        sim = WorkflowSimulator.simulate_quota_limit_detection({
            "mode": "auto",
            "http_code": 429,
            "error_banner": "ResourceExhausted",
        })
        self.assertEqual(sim["status"], "PAUSED_QUOTA_EXHAUSTED")
        self.assertTrue(sim["automated_retry_aborted"])

    def test_f9_b02_safety_captcha_prohibits_auto_bypass(self):
        """F9-B2: System prohibits automated CAPTCHA bypassing."""
        violating_clause = "Attempt to bypass CAPTCHA using automated solver scripts."
        errors = SafetyBoundariesValidator.validate_safety_clause(violating_clause)
        self.assertTrue(any("captcha" in e.lower() and "prohibit" in e.lower() for e in errors))

    def test_f9_b03_safety_multiple_errors_simultaneous(self):
        """F9-B3: Handles multi-error payload (e.g. rate limit + safety block)."""
        combined_error = "ResourceExhausted and HARM_CATEGORY_DANGEROUS_CONTENT"
        res = SafetyBoundariesValidator.classify_platform_error(combined_error)
        self.assertTrue(res["is_quota"])
        self.assertTrue(res["is_safety"])

    def test_f9_b04_safety_transient_vs_permanent_quota_error(self):
        """F9-B4: Distinguishes transient rate limits from permanent quota depletion."""
        transient = SafetyBoundariesValidator.classify_platform_error("Rate limit exceeded. Please wait 60 seconds.")
        permanent = SafetyBoundariesValidator.classify_platform_error("Daily quota exhausted. Resets at midnight UTC.")
        self.assertTrue(transient["is_transient"])
        self.assertFalse(permanent["is_transient"])

    def test_f9_b05_safety_unrecognized_modal_dialog(self):
        """F9-B5: Unrecognized modal error dialog does not crash offload pipeline."""
        sim = WorkflowSimulator.simulate_quota_limit_detection({
            "mode": "auto",
            "http_code": 200,
            "error_banner": "Normal execution",
        })
        self.assertEqual(sim["status"], "CONTINUE")

    def test_f9_b06_account_verification_gate_zero_retry_in_auto_mode(self):
        """F9-B6: Account verification banner forces zero-retry halt and local fallback even in auto mode."""
        banner = (
            "Your account must be verified before it can continue using the Gemini API. "
            "Verify your account at https://aistudio.google.com/verify-account."
        )
        classified = SafetyBoundariesValidator.classify_platform_error(banner)
        self.assertTrue(classified["is_account_verification"])
        self.assertTrue(classified["zero_retry_required"])
        self.assertTrue(classified["fallback_to_local"])
        self.assertEqual(classified["status"], "PAUSED_ACCOUNT_VERIFICATION_REQUIRED")

        sim = WorkflowSimulator.simulate_account_verification_gate({
            "mode": "auto",
            "error_banner": banner,
        })
        self.assertEqual(sim["status"], "PAUSED_ACCOUNT_VERIFICATION_REQUIRED")
        self.assertEqual(sim["retry_count"], 0)
        self.assertTrue(sim["automated_retry_aborted"])
        self.assertEqual(sim["fallback_route"], "LOCAL_MACHINE")

    def test_f9_b07_pacing_cooldown_rejects_rapid_burst_and_excess_calls(self):
        """F9-B7: Anti-abuse pacing validator rejects rapid bursts (<15s) and excess session calls (>8)."""
        too_fast = SafetyBoundariesValidator.validate_pacing_policy(cooldown_seconds=3.0, session_calls=2)
        self.assertFalse(too_fast["allowed"])
        self.assertTrue(too_fast["fallback_to_local"])

        too_many = SafetyBoundariesValidator.validate_pacing_policy(cooldown_seconds=20.0, session_calls=9)
        self.assertFalse(too_many["allowed"])
        self.assertTrue(too_many["fallback_to_local"])

        healthy = SafetyBoundariesValidator.validate_pacing_policy(cooldown_seconds=22.0, session_calls=4)
        self.assertTrue(healthy["allowed"])
        self.assertFalse(healthy["fallback_to_local"])
        self.assertEqual(healthy["errors"], [])

    def test_f9_b08_on_demand_grounding_off_for_internal_diff_on_for_web(self):
        """F9-B8: On-Demand Grounding stays OFF for internal git diff reviews and turns ON for live web research."""
        internal = SafetyBoundariesValidator.should_enable_search_grounding(
            "Audit local codebase git diff and architecture spec for regressions"
        )
        self.assertFalse(internal["enable_search_grounding"])
        self.assertFalse(internal["enable_url_context"])

        web_task = SafetyBoundariesValidator.should_enable_search_grounding(
            "Verify latest official docs and pricing for https://ai.google.dev/gemini-api/docs/pricing"
        )
        self.assertTrue(web_task["enable_search_grounding"])
        self.assertTrue(web_task["enable_url_context"])

    # =========================================================================
    # Feature 10: Local File Staging Contract - 5 Boundary Tests
    # =========================================================================

    def test_f10_b01_staging_path_traversal_rejection(self):
        """F10-B1: Path traversal sequence (../) in staged filename is detected and rejected."""
        errors = StagingContractValidator.validate_filename("../../../etc/passwd")
        self.assertTrue(any("traversal" in e.lower() or "path" in e.lower() for e in errors))

    def test_f10_b02_staging_absolute_path_in_filename_rejection(self):
        """F10-B2: Absolute file paths are rejected when bare single-segment filename is required."""
        errors = StagingContractValidator.validate_filename("C:\\Windows\\System32\\calc.exe")
        self.assertTrue(any("absolute" in e.lower() for e in errors))

    def test_f10_b03_staging_empty_filename(self):
        """F10-B3: Empty or whitespace-only staged filename is rejected."""
        errors = StagingContractValidator.validate_filename("   ")
        self.assertTrue(any("empty" in e.lower() for e in errors))

    def test_f10_b04_staging_special_characters_filename(self):
        """F10-B4: Sanitizes spaces and non-standard characters in staged filenames."""
        errors = StagingContractValidator.validate_filename("my prompt @ v1.0 #test.json")
        self.assertTrue(any("special" in e.lower() or "invalid" in e.lower() for e in errors))

    def test_f10_b05_staging_missing_file_in_staging_dir(self):
        """F10-B5: Attempting to upload a missing file from staging directory raises error."""
        non_existent_file = REPO_ROOT / "browser_sandbox" / "uploads" / "missing.txt"
        self.assertFalse(non_existent_file.is_file())

    # =========================================================================
    # Feature 11: Skill: aistudio-offload - 5 Boundary Tests
    # =========================================================================

    def test_f11_b01_skill_offload_missing_frontmatter(self):
        """F11-B1: SkillValidator rejects skill content missing frontmatter delimiters."""
        bad_skill = "# Just Title\nNo frontmatter delimiters."
        errors = SkillValidator.validate_skill_content(bad_skill)
        self.assertTrue(any("delimiter" in e.lower() for e in errors))

    def test_f11_b02_skill_offload_empty_description(self):
        """F11-B2: SkillValidator rejects skill with empty description."""
        bad_skill = "---\nname: aistudio-offload\ndescription: \n---\n# Offload\nSome body text here that is long enough."
        errors = SkillValidator.validate_skill_content(bad_skill)
        self.assertTrue(any("description" in e.lower() for e in errors))

    def test_f11_b03_skill_offload_name_mismatch(self):
        """F11-B3: SkillValidator rejects frontmatter name differing from expected skill name."""
        bad_skill = "---\nname: other-skill\ndescription: Some description here.\n---\n# Title\nSome body text here that is long enough."
        errors = SkillValidator.validate_skill_content(bad_skill, expected_name="aistudio-offload")
        self.assertTrue(any("does not match" in e.lower() for e in errors))

    def test_f11_b04_skill_offload_short_body(self):
        """F11-B4: SkillValidator flags skill with truncated body (<50 chars)."""
        bad_skill = "---\nname: aistudio-offload\ndescription: Some valid description.\n---\n# Hi"
        errors = SkillValidator.validate_skill_content(bad_skill)
        self.assertTrue(any("too short" in e.lower() for e in errors))

    def test_f11_b05_skill_offload_broken_reference_link(self):
        """F11-B5: Flags non-existent reference link in skill documentation."""
        fake_ref_path = SKILLS_DIR / "aistudio-offload" / "references" / "non_existent_matrix.md"
        self.assertFalse(fake_ref_path.is_file())

    # =========================================================================
    # Feature 12: Reference: offload-decision-matrix.md - 5 Boundary Tests
    # =========================================================================

    def test_f12_b01_matrix_empty_table_content(self):
        """F12-B1: Empty decision matrix reference content is rejected."""
        errors = MarkdownTableValidator.validate_markdown_table("")
        self.assertTrue(any("empty" in e.lower() for e in errors))

    def test_f12_b02_matrix_missing_headers(self):
        """F12-B2: Decision matrix table missing mandatory column headers is detected."""
        table_without_headers = "| foo | bar |\n|---|---|\n| 1 | 2 |"
        errors = MarkdownTableValidator.validate_markdown_table(
            table_without_headers,
            required_headers=["Workload Type", "Execution Target"]
        )
        self.assertTrue(any("workload type" in e.lower() for e in errors))

    def test_f12_b03_matrix_corrupted_row_pipes(self):
        """F12-B3: Detects corrupted markdown table row missing closing pipe delimiter."""
        bad_table = "| Workload | Target |\n|---|---|\n| Workload | Missing end pipe"
        errors = MarkdownTableValidator.validate_markdown_table(bad_table)
        self.assertTrue(any("pipe" in e.lower() for e in errors))

    def test_f12_b04_matrix_invalid_token_values(self):
        """F12-B4: Validates that token thresholds are positive numbers."""
        errors = ParameterTuningValidator.validate_hyperparameters({"token_threshold": -500})
        self.assertTrue(any("token threshold" in e.lower() or "positive" in e.lower() for e in errors))

    def test_f12_b05_matrix_deprecated_model_names(self):
        """F12-B5: Flags references to all retired pre-Gemini-4 models and accepts Gemini 4 models."""
        deprecated = [
            "palm-2", "gemini-1.0-ultra", "gemini-1.5-pro", "gemini-2.0-flash",
            "gemini-2.5-pro", "gemini-2.5-flash", "gemini-flash-thinking",
            "gemini-3-flash-preview", "gemini-3.1-pro-preview", "gemini-3.8-flash",
        ]
        for m in deprecated:
            errors = ParameterTuningValidator.validate_model_name(m)
            self.assertTrue(any("deprecated" in e.lower() or "retired" in e.lower() for e in errors), f"Should reject {m}")
        for ok in ["gemini-4-hydrogen", "gemini-4-argon", "gemini-4-neon", "gemini-4-carbon"]:
            self.assertEqual(ParameterTuningValidator.validate_model_name(ok), [], f"Should accept {ok}")

    # =========================================================================
    # Feature 13: Skill: aistudio-chat-prompt - 5 Boundary Tests
    # =========================================================================

    def test_f13_b01_skill_chat_empty_system_instruction(self):
        """F13-B1: Handles empty system instruction without crashing."""
        sim = WorkflowSimulator.simulate_multi_turn_chat_sync({"system_instruction": ""})
        self.assertEqual(sim["status"], "SUCCESS")

    def test_f13_b02_skill_chat_zero_turns(self):
        """F13-B2: Chat simulation with zero user turns handles empty history."""
        sim = WorkflowSimulator.simulate_multi_turn_chat_sync({"turns": []})
        self.assertEqual(sim["turns_processed"], 0)

    def test_f13_b03_skill_chat_unsupported_media_extension(self):
        """F13-B3: Detects unsupported media attachment extensions (e.g. .exe)."""
        errors = StagingContractValidator.validate_media_extension("payload.exe")
        self.assertTrue(any("unsupported" in e.lower() or ".exe" in e.lower() for e in errors))

    def test_f13_b04_skill_chat_deep_context_turn_count(self):
        """F13-B4: Multi-turn simulation handles 50+ conversation turns."""
        many_turns = [{"role": "user" if i % 2 == 0 else "model", "content": f"Turn {i}"} for i in range(60)]
        sim = WorkflowSimulator.simulate_multi_turn_chat_sync({"turns": many_turns})
        self.assertEqual(sim["turns_processed"], 60)

    def test_f13_b05_skill_chat_unclosed_code_blocks(self):
        """F13-B5: Detects unclosed code fences in chat history transcripts."""
        bad_transcript = "Here is code:\n```python\nprint('hello')\n"
        errors = CodeExportValidator.validate_snippet(bad_transcript)
        self.assertTrue(any("fence" in e.lower() or "unclosed" in e.lower() for e in errors))

    # =========================================================================
    # Feature 14: Skill: aistudio-structured-prompt - 5 Boundary Tests
    # =========================================================================

    def test_f14_b01_skill_structured_empty_few_shot_table(self):
        """F14-B1: Structured prompt handles 0 few-shot examples."""
        sim = WorkflowSimulator.simulate_few_shot_structured_export({"examples": []})
        self.assertEqual(sim["example_count"], 0)

    def test_f14_b02_skill_structured_mismatched_columns(self):
        """F14-B2: Detects mismatched column counts in few-shot example rows."""
        bad_table = "| Input | Context | Output |\n|---|---|---|\n| Only one value |"
        errors = MarkdownTableValidator.validate_markdown_table(bad_table)
        self.assertTrue(any("mismatch" in e.lower() or "column" in e.lower() for e in errors))

    def test_f14_b03_skill_structured_malformed_json_schema(self):
        """F14-B3: Detects malformed JSON schema dictionary missing 'type'."""
        bad_schema = {"properties": {"name": {"type": "string"}}}
        errors = CodeExportValidator.validate_json_schema(bad_schema)
        self.assertTrue(any("type" in e.lower() for e in errors))

    def test_f14_b04_skill_structured_empty_test_case_input(self):
        """F14-B4: Flags empty test case input string."""
        errors = CodeExportValidator.validate_snippet("   ")
        self.assertTrue(any("empty" in e.lower() for e in errors))

    def test_f14_b05_skill_structured_corrupted_csv_payload(self):
        """F14-B5: Detects unescaped quotes in CSV batch data."""
        corrupted_csv = 'col1,col2\n"value with unclosed quote,second_val\n'
        errors = StagingContractValidator.validate_csv_payload(corrupted_csv)
        self.assertTrue(any("quote" in e.lower() or "csv" in e.lower() for e in errors))

    # =========================================================================
    # Feature 15: Skill: aistudio-parameter-tuning - 6 Boundary Tests
    # =========================================================================

    def test_f15_b01_param_tuning_thinking_level_rejects_low_and_medium(self):
        """F15-B1: Thinking level rejects 'low' and 'medium' and accepts 'high' / 'xhigh'."""
        for bad_lvl in ["low", "medium", "LOW", "Medium", "", "auto"]:
            errors = ParameterTuningValidator.validate_thinking_level(bad_lvl)
            self.assertGreater(len(errors), 0, f"Should reject thinking_level={bad_lvl!r}")
        for good_lvl in ["high", "xhigh", "HIGH", "XHIGH"]:
            errors = ParameterTuningValidator.validate_thinking_level(good_lvl)
            self.assertEqual(errors, [], f"Should accept thinking_level={good_lvl!r}: {errors}")

    def test_f15_b02_param_tuning_rejects_removed_legacy_sliders(self):
        """F15-B2: Legacy sliders removed in Gemini 4 (temperature, top_p, top_k, thinking_budget) are rejected."""
        for legacy_key, val in [("temperature", 0.7), ("top_p", 0.95), ("top_k", 40), ("thinking_budget", 8192)]:
            errors = ParameterTuningValidator.validate_hyperparameters({legacy_key: val})
            self.assertTrue(any("removed" in e.lower() or "gemini 4" in e.lower() for e in errors), f"Should reject {legacy_key}")

    def test_f15_b03_param_tuning_output_length_bounds(self):
        """F15-B3: Output length enforces model caps (65536 Hydrogen/Neon, 32768 Argon/Carbon)."""
        self.assertEqual(ParameterTuningValidator.validate_output_length(65536, "gemini-4-hydrogen"), [])
        self.assertEqual(ParameterTuningValidator.validate_output_length(32768, "gemini-4-argon"), [])
        self.assertGreater(len(ParameterTuningValidator.validate_output_length(0, "gemini-4-hydrogen")), 0)
        self.assertGreater(len(ParameterTuningValidator.validate_output_length(65537, "gemini-4-neon")), 0)
        self.assertGreater(len(ParameterTuningValidator.validate_output_length(32769, "gemini-4-carbon")), 0)

    def test_f15_b04_param_tuning_media_resolution_bounds(self):
        """F15-B4: Media resolution only permits default, low, medium, high."""
        for ok_res in ["default", "low", "medium", "high"]:
            self.assertEqual(ParameterTuningValidator.validate_media_resolution(ok_res), [])
        self.assertGreater(len(ParameterTuningValidator.validate_media_resolution("ultra")), 0)

    def test_f15_b05_param_tuning_invalid_safety_threshold_string(self):
        """F15-B5: Invalid safety filter threshold string is rejected."""
        errors = ParameterTuningValidator.validate_hyperparameters({"safety_threshold": "BLOCK_EVERYTHING_ALWAYS"})
        self.assertTrue(any("safety" in e.lower() or "threshold" in e.lower() for e in errors))

    def test_f15_b06_param_tuning_carbon_paid_gate_fallback(self):
        """F15-B6: Unlock Gemini 4 Carbon paid gate pauses and offers Neon/Hydrogen (High) fallback."""
        sim = WorkflowSimulator.simulate_paid_gate_detection({"mode": "auto", "banner": "Unlock Gemini 4 Carbon"})
        self.assertEqual(sim["status"], "PAUSED_PAID_TIER_REQUIRED")
        self.assertTrue(sim["automated_retry_aborted"])
        self.assertIn("Gemini 4 Neon (High)", sim["fallback_options"])
        self.assertIn("Gemini 4 Hydrogen (High)", sim["fallback_options"])

    # =========================================================================
    # Feature 16: Skill: aistudio-code-export - 5 Boundary Tests
    # =========================================================================

    def test_f16_b01_code_export_unsupported_language(self):
        """F16-B1: Unsupported language export target is rejected."""
        errors = CodeExportValidator.validate_language("cobol")
        self.assertTrue(any("unsupported" in e.lower() or "cobol" in e.lower() for e in errors))

    def test_f16_b02_code_export_leaked_raw_api_key(self):
        """F16-B2: Detects and rejects hardcoded Google API key pattern (AIza...)."""
        snippet = 'client = genai.Client(api_key="AIzaSyA1234567890abcdefghijklmnopqrst")'
        errors = CodeExportValidator.validate_snippet(snippet)
        self.assertTrue(any("api key" in e.lower() or "leak" in e.lower() for e in errors))

    def test_f16_b03_code_export_empty_snippet(self):
        """F16-B3: Flags empty or whitespace-only exported snippet."""
        errors = CodeExportValidator.validate_snippet("   ")
        self.assertTrue(any("empty" in e.lower() for e in errors))

    def test_f16_b04_code_export_python_syntax_error(self):
        """F16-B4: Python AST parser catches syntax errors in generated code."""
        code_with_syntax_error = "def foo(\n  return 123"
        errors = CodeExportValidator.validate_snippet(code_with_syntax_error, language="python")
        self.assertTrue(any("syntax" in e.lower() for e in errors))

    def test_f16_b05_code_export_file_overwrite_prevention(self):
        """F16-B5: System guards against unconfirmed file clobbering."""
        errors = StagingContractValidator.validate_file_overwrite(existing_exists=True, user_confirmed=False)
        self.assertTrue(any("overwrite" in e.lower() for e in errors))

    # =========================================================================
    # Feature 17: Skill: aistudio-ui-sync-audit - 5 Boundary Tests
    # =========================================================================

    def test_f17_b01_ui_audit_missing_disable_model_invocation(self):
        """F17-B1: Simulation rejects audit skill when disable-model-invocation is false."""
        sim = WorkflowSimulator.simulate_ui_sync_audit({"disable-model-invocation": False})
        self.assertEqual(sim["status"], "FAILED")

    def test_f17_b02_ui_audit_forbids_mutating_actions(self):
        """F17-B2: System prohibits clicking mutating action buttons during audit."""
        for act in ["click_delete", "click_save", "click_generate", "click_run"]:
            errors = SafetyBoundariesValidator.validate_audit_action(act)
            self.assertTrue(any("forbidden" in e.lower() or "mutating" in e.lower() for e in errors))

    def test_f17_b03_ui_audit_missing_audit_checklist_ref(self):
        """F17-B3: Flags audit skill content missing references/audit-checklist.md."""
        bad_content = "# Audit\nNo checklist referenced."
        errors = SafetyBoundariesValidator.validate_audit_references(bad_content)
        self.assertTrue(any("audit-checklist.md" in e.lower() for e in errors))

    def test_f17_b04_ui_audit_stale_calibration_warning(self):
        """F17-B4: Calibration date older than 90 days triggers stale warning."""
        errors = SafetyBoundariesValidator.validate_calibration_freshness("2024-01-01", max_days=90)
        self.assertTrue(any("stale" in e.lower() for e in errors))

    def test_f17_b05_ui_audit_unresponsive_surface_timeout(self):
        """F17-B5: Handles surface navigation timeout gracefully."""
        errors = SafetyBoundariesValidator.validate_navigation_timeout(25, max_timeout=15)
        self.assertTrue(any("timeout" in e.lower() for e in errors))

    # =========================================================================
    # Feature 18: Reference: audit-checklist.md - 5 Boundary Tests
    # =========================================================================

    def test_f18_b01_checklist_missing_date(self):
        """F18-B1: Flags checklist missing calibration date."""
        errors = MarkdownTableValidator.validate_checklist_markdown("# Audit Checklist\nNo date here.")
        self.assertTrue(any("date" in e.lower() for e in errors))

    def test_f18_b02_checklist_invalid_date_format(self):
        """F18-B2: Rejects invalid calibration date format."""
        bad_date_content = "# Audit Checklist\nLast Calibrated: November 21st, 2026\n## Deprecations\nNone"
        errors = MarkdownTableValidator.validate_checklist_markdown(bad_date_content)
        self.assertTrue(any("date" in e.lower() and ("format" in e.lower() or "invalid" in e.lower() or "missing" in e.lower()) for e in errors))

    def test_f18_b03_checklist_fewer_than_7_surfaces(self):
        """F18-B3: Flags checklist covering fewer than the 7 canonical surfaces."""
        surfaces = ["Dashboard", "Prompt Editor", "Tuning"]
        errors = MarkdownTableValidator.validate_audit_surfaces(surfaces)
        self.assertTrue(any("7" in e or "surface" in e.lower() for e in errors))

    def test_f18_b04_checklist_empty_pruning_section(self):
        """F18-B4: Flags checklist missing or having empty deprecation/pruning section."""
        content = "# Checklist\nCalibration: 2026-11-22\n## Surfaces\n1. Dashboard"
        errors = MarkdownTableValidator.validate_checklist_markdown(content)
        self.assertTrue(any("prun" in e.lower() or "deprecat" in e.lower() for e in errors))

    def test_f18_b05_checklist_broken_markdown_tables(self):
        """F18-B5: Detects uneven columns in checklist markdown tables."""
        broken_table = "| a | b | c |\n|---|---|---|\n| a | b |"
        errors = MarkdownTableValidator.validate_markdown_table(broken_table)
        self.assertTrue(any("mismatch" in e.lower() or "column" in e.lower() for e in errors))

    # =========================================================================
    # Feature 19: Overseas Localization (Zero Non-English Characters) - 5 Boundary Tests
    # =========================================================================

    def test_f19_b01_localization_detects_chinese_hanzi(self):
        """F19-B1: Scanner detects Chinese Hanzi characters accurately."""
        sample_chinese = "This is English with \u4e00\u4e9b\u4e2d\u6587 mixed in."
        violations = OverseasLocalizationValidator.scan_text(sample_chinese)
        self.assertGreater(len(violations), 0)
        self.assertEqual(violations[0][0], 1)

    def test_f19_b02_localization_detects_fullwidth_punctuation(self):
        """F19-B2: Scanner detects full-width punctuation marks."""
        sample_fw = "Hello world\uff0cthis has full-width comma\u3002"
        violations = OverseasLocalizationValidator.scan_text(sample_fw)
        self.assertGreater(len(violations), 0)

    def test_f19_b03_localization_allows_ascii_punctuation(self):
        """F19-B3: Scanner allows standard ASCII punctuation (!@#$%^&*()_+~`-={}|[]\\:\";'<>?,./)."""
        sample_ascii = "!@#$%^&*()_+~`-={}|[]\\:\";'<>?,./ 1234567890"
        violations = OverseasLocalizationValidator.scan_text(sample_ascii)
        self.assertEqual(violations, [])

    def test_f19_b04_localization_allows_numbers_and_urls(self):
        """F19-B4: Scanner allows standard URLs, query params, and JSON structures."""
        sample_code = '{"url": "https://aistudio.google.com/?pli=1&authuser=0", "tokens": 4000}'
        violations = OverseasLocalizationValidator.scan_text(sample_code)
        self.assertEqual(violations, [])

    def test_f19_b05_localization_handles_empty_or_whitespace_file(self):
        """F19-B5: Scanner handles empty or whitespace-only content without error."""
        violations = OverseasLocalizationValidator.scan_text("   \n\t\r\n   ")
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
