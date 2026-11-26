#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E2E Test Suite Runner for antigravity-aistudio
Executes 5-tier test suite using standard Python unittest and reports structured breakdown.
Hardened with pre-flight repository sanity gates, strict threshold gates, and
whole-repository falsification resilience probe (--verify-falsification).
Zero external dependencies.
"""

import os
import sys
import time
import tempfile
import unittest
from pathlib import Path
from typing import List, Tuple

# Ensure tests and repo root are in python path
TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import conftest
from test_tier1_feature_coverage import TestTier1FeatureCoverage
from test_tier2_boundary_corner import TestTier2BoundaryCorner
from test_tier3_cross_feature import TestTier3CrossFeature
from test_tier4_real_world import TestTier4RealWorld
from test_tier5_adversarial_hardening import TestTier5AdversarialHardening

TIER_REQUIREMENTS = {
    "Tier 1 (Feature Coverage)": 99,
    "Tier 2 (Boundary & Corner)": 100,
    "Tier 3 (Cross-Feature & Pairwise)": 28,
    "Tier 4 (Real-World Scenarios)": 8,
    "Tier 5 (Adversarial Hardening)": 34,
}
MIN_TOTAL_TESTS = 269

MANDATORY_REPO_ARTIFACTS = [
    ("plugin.json", REPO_ROOT / "plugin.json", "file"),
    ("README.md", REPO_ROOT / "README.md", "file"),
    ("assets/logo.svg", REPO_ROOT / "assets" / "logo.svg", "file"),
    ("rules/AGENTS.md", REPO_ROOT / "rules" / "AGENTS.md", "file"),
    ("skills directory", REPO_ROOT / "skills", "dir"),
]


class TierSummaryResult(unittest.TestResult):
    """Custom TestResult collecting detailed tier statistics."""

    def __init__(self, tier_name: str):
        super().__init__()
        self.tier_name = tier_name
        self.passed = 0
        self.failed = 0
        self.errors_count = 0
        self.skipped_count = 0

    def addSuccess(self, test):
        super().addSuccess(test)
        self.passed += 1

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.failed += 1

    def addError(self, test, err):
        super().addError(test, err)
        self.errors_count += 1

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.skipped_count += 1


def pre_flight_repository_check() -> List[str]:
    """Ensures mandatory repository artifacts exist on disk before executing test suite."""
    missing = []
    for name, path, artifact_type in MANDATORY_REPO_ARTIFACTS:
        if artifact_type == "file" and not path.is_file():
            missing.append(f"Mandatory file missing: {name} (expected at {path})")
        elif artifact_type == "dir" and not path.is_dir():
            missing.append(f"Mandatory directory missing: {name} (expected at {path})")
    return missing


def probe_falsification_resilience() -> bool:
    """
    Proves whole-repository falsification resilience (Auditor Check 5).
    Simulates an empty repository by pointing conftest paths to an empty temp directory.
    Verifies that the test suite fails loudly and cannot be passed on phantom files.
    """
    print("\n" + "=" * 80)
    print("  WHOLE-REPOSITORY FALSIFICATION RESILIENCE PROBE")
    print("=" * 80)
    print("Simulating empty repository sandbox to verify fail-loudly invariants...")

    with tempfile.TemporaryDirectory(prefix="empty_probe_") as tmp_dir:
        fake_empty = Path(tmp_dir)

        # Save original conftest paths
        orig_root = conftest.REPO_ROOT
        orig_plugin = conftest.PLUGIN_JSON_PATH
        orig_readme = conftest.README_PATH
        orig_svg = conftest.LOGO_SVG_PATH
        orig_rule = conftest.AGENTS_RULE_PATH
        orig_skills = conftest.SKILLS_DIR

        try:
            # Re-point conftest paths to empty probe dir
            conftest.REPO_ROOT = fake_empty
            conftest.PLUGIN_JSON_PATH = fake_empty / "plugin.json"
            conftest.README_PATH = fake_empty / "README.md"
            conftest.LOGO_SVG_PATH = fake_empty / "assets" / "logo.svg"
            conftest.AGENTS_RULE_PATH = fake_empty / "rules" / "AGENTS.md"
            conftest.SKILLS_DIR = fake_empty / "skills"

            import test_tier1_feature_coverage as t1_mod
            import test_tier3_cross_feature as t3_mod

            t1_orig = (t1_mod.PLUGIN_JSON_PATH, t1_mod.README_PATH, t1_mod.LOGO_SVG_PATH, t1_mod.AGENTS_RULE_PATH, t1_mod.SKILLS_DIR)
            t3_orig = (t3_mod.PLUGIN_JSON_PATH, t3_mod.README_PATH, t3_mod.LOGO_SVG_PATH, t3_mod.AGENTS_RULE_PATH, t3_mod.SKILLS_DIR)

            t1_mod.PLUGIN_JSON_PATH = fake_empty / "plugin.json"
            t1_mod.README_PATH = fake_empty / "README.md"
            t1_mod.LOGO_SVG_PATH = fake_empty / "assets" / "logo.svg"
            t1_mod.AGENTS_RULE_PATH = fake_empty / "rules" / "AGENTS.md"
            t1_mod.SKILLS_DIR = fake_empty / "skills"

            t3_mod.PLUGIN_JSON_PATH = fake_empty / "plugin.json"
            t3_mod.README_PATH = fake_empty / "README.md"
            t3_mod.LOGO_SVG_PATH = fake_empty / "assets" / "logo.svg"
            t3_mod.AGENTS_RULE_PATH = fake_empty / "rules" / "AGENTS.md"
            t3_mod.SKILLS_DIR = fake_empty / "skills"

            # Probe Tier 1
            t1_suite = unittest.TestLoader().loadTestsFromTestCase(TestTier1FeatureCoverage)
            res1 = unittest.TestResult()
            t1_suite.run(res1)
            t1_fails = len(res1.failures) + len(res1.errors)

            # Probe Tier 3
            t3_suite = unittest.TestLoader().loadTestsFromTestCase(TestTier3CrossFeature)
            res3 = unittest.TestResult()
            t3_suite.run(res3)
            t3_fails = len(res3.failures) + len(res3.errors)

            # Probe Tier 4
            t4_suite = unittest.TestLoader().loadTestsFromTestCase(TestTier4RealWorld)
            res4 = unittest.TestResult()
            t4_suite.run(res4)
            t4_fails = len(res4.failures) + len(res4.errors)

            total_probe_fails = t1_fails + t3_fails + t4_fails
            print(f"Empty Probe Run - Tier 1: {t1_fails} failures, Tier 3: {t3_fails} failures, Tier 4: {t4_fails} failures")

            if t1_fails == 0 or t3_fails == 0 or t4_fails == 0:
                print("[PROBE FAILED] Test suite falsely passed on missing repository artifacts!")
                return False

            print(f"[PROBE PASSED] Suite successfully detected missing files: {total_probe_fails} total failures/errors raised.")
            print("=" * 80)
            return True

        finally:
            conftest.REPO_ROOT = orig_root
            conftest.PLUGIN_JSON_PATH = orig_plugin
            conftest.README_PATH = orig_readme
            conftest.LOGO_SVG_PATH = orig_svg
            conftest.AGENTS_RULE_PATH = orig_rule
            conftest.SKILLS_DIR = orig_skills

            if 't1_orig' in locals():
                t1_mod.PLUGIN_JSON_PATH, t1_mod.README_PATH, t1_mod.LOGO_SVG_PATH, t1_mod.AGENTS_RULE_PATH, t1_mod.SKILLS_DIR = t1_orig
            if 't3_orig' in locals():
                t3_mod.PLUGIN_JSON_PATH, t3_mod.README_PATH, t3_mod.LOGO_SVG_PATH, t3_mod.AGENTS_RULE_PATH, t3_mod.SKILLS_DIR = t3_orig


def run_tier(suite_class, tier_name: str) -> TierSummaryResult:
    suite = unittest.TestLoader().loadTestsFromTestCase(suite_class)
    result = TierSummaryResult(tier_name)
    suite.run(result)
    return result


def main():
    if "--verify-falsification" in sys.argv:
        passed = probe_falsification_resilience()
        return 0 if passed else 1

    start_time = time.time()
    print("=" * 80)
    print("  ANTIGRAVITY-AISTUDIO 5-TIER E2E TEST SUITE RUNNER")
    print("=" * 80)
    print(f"Repository Root: {REPO_ROOT}")
    print(f"Tests Directory: {TESTS_DIR}")
    print("-" * 80)

    # 1. Pre-Flight Repository Sanity Gate
    missing_artifacts = pre_flight_repository_check()
    if missing_artifacts:
        print("[PRE-FLIGHT SANITY GATE FAILED] Mandatory repository files are missing on disk:")
        for m in missing_artifacts:
            print(f"  - {m}")
        print("\nAborting test execution: repository is not in a testable state.")
        return 1
    print("[PRE-FLIGHT SANITY GATE PASSED] All mandatory repository artifacts exist on disk.")
    print("-" * 80)

    tiers = [
        ("Tier 1 (Feature Coverage)", TestTier1FeatureCoverage),
        ("Tier 2 (Boundary & Corner)", TestTier2BoundaryCorner),
        ("Tier 3 (Cross-Feature & Pairwise)", TestTier3CrossFeature),
        ("Tier 4 (Real-World Scenarios)", TestTier4RealWorld),
        ("Tier 5 (Adversarial Hardening)", TestTier5AdversarialHardening),
    ]

    tier_results = []
    total_passed = 0
    total_failed = 0
    total_errors = 0
    total_skipped = 0
    total_tests = 0

    for tier_name, test_class in tiers:
        print(f"Executing {tier_name}...", end=" ", flush=True)
        t_start = time.time()
        res = run_tier(test_class, tier_name)
        t_dur = time.time() - t_start
        tier_results.append((tier_name, res, t_dur))

        tier_total = res.testsRun
        total_tests += tier_total
        total_passed += res.passed
        total_failed += res.failed
        total_errors += res.errors_count
        total_skipped += res.skipped_count

        req = TIER_REQUIREMENTS.get(tier_name, 0)
        is_tier_clean = (res.passed >= req and res.failed == 0 and res.errors_count == 0)

        if is_tier_clean:
            print(f"PASS ({res.passed} passed in {t_dur:.3f}s)")
        else:
            print(f"FAIL ({res.failed} failures, {res.errors_count} errors, {res.passed}/{req} passed in {t_dur:.3f}s)")
            for failure in res.failures:
                print(f"\n[FAILURE] {failure[0]}:\n{failure[1]}")
            for error in res.errors:
                print(f"\n[ERROR] {error[0]}:\n{error[1]}")

    elapsed_total = time.time() - start_time

    # Print Summary Breakdown Table
    print("\n" + "=" * 80)
    print("  TEST EXECUTION SUMMARY BREAKDOWN")
    print("=" * 80)
    header = f"{'Tier Name':<35} | {'Target':<7} | {'Run':<5} | {'Passed':<6} | {'Failed':<6} | {'Status'}"
    print(header)
    print("-" * 80)

    all_thresholds_met = True
    for tier_name, res, dur in tier_results:
        req = TIER_REQUIREMENTS.get(tier_name, 0)
        # Strict Pass/Fail Condition: must have passed >= target, and 0 failures and 0 errors
        status = "PASS" if (res.passed >= req and res.failed == 0 and res.errors_count == 0) else "FAIL"
        if status != "PASS":
            all_thresholds_met = False
        row = f"{tier_name:<35} | >={req:<5} | {res.testsRun:<5} | {res.passed:<6} | {res.failed + res.errors_count:<6} | {status}"
        print(row)

    print("-" * 80)
    grand_status = "PASS" if (all_thresholds_met and total_passed >= MIN_TOTAL_TESTS and total_failed == 0 and total_errors == 0) else "FAIL"
    summary_row = f"{'GRAND TOTAL':<35} | >={MIN_TOTAL_TESTS:<5} | {total_tests:<5} | {total_passed:<6} | {total_failed + total_errors:<6} | {grand_status}"
    print(summary_row)
    print("=" * 80)
    print(f"Total Duration: {elapsed_total:.3f}s | Finished at: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")

    # Threshold verifications
    if total_passed < MIN_TOTAL_TESTS:
        print(f"\n[ERROR] Total passed tests count ({total_passed}) is below required minimum ({MIN_TOTAL_TESTS})!")
        return 1

    for tier_name, res, _ in tier_results:
        req = TIER_REQUIREMENTS.get(tier_name, 0)
        if res.passed < req:
            print(f"\n[ERROR] {tier_name} passed count ({res.passed}) is below required minimum ({req})!")
            return 1

    if total_failed > 0 or total_errors > 0:
        print(f"\n[FAILED] Test suite failed with {total_failed} failures and {total_errors} errors.")
        return 1

    print("\n[SUCCESS] 100% of E2E tests passed! All tier coverage gates satisfied.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
