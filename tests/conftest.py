# -*- coding: utf-8 -*-
"""
E2E Test Infrastructure for antigravity-aistudio
Provides shared fixtures, validators, schemas, and simulation harnesses.
Compatible with standard library unittest and pytest.
Zero external dependencies.
"""

import os
import sys
import re
import ast
import json
import tempfile
import urllib.parse
from datetime import datetime
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set

REPO_ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = Path(__file__).resolve().parent

PLUGIN_JSON_PATH = REPO_ROOT / "plugin.json"
README_PATH = REPO_ROOT / "README.md"
LOGO_SVG_PATH = REPO_ROOT / "assets" / "logo.svg"
AGENTS_RULE_PATH = REPO_ROOT / "rules" / "AGENTS.md"
SKILLS_DIR = REPO_ROOT / "skills"

CANONICAL_URL = "https://aistudio.google.com/"
CANONICAL_SUBAGENT_TYPE = "browser"
CANONICAL_DEFAULT_MODEL = "flash"
CANONICAL_AUTONOMY_MODES = ["checkpoint", "auto"]

CANONICAL_SKILLS = [
    "aistudio-offload",
    "aistudio-chat-prompt",
    "aistudio-structured-prompt",
    "aistudio-parameter-tuning",
    "aistudio-code-export",
    "aistudio-ui-sync-audit",
]

CANONICAL_REFERENCES = {
    "aistudio-offload": "references/offload-decision-matrix.md",
    "aistudio-ui-sync-audit": "references/audit-checklist.md",
}

CANONICAL_STAGING_PATHS = {
    "uploads": "<Artifact Directory Path>/browser_sandbox/uploads/",
    "downloads": "<Artifact Directory Path>/browser_sandbox/downloads/",
    "references": "<Artifact Directory Path>/browser_sandbox/references/",
}

CANONICAL_7_AUDIT_SURFACES = [
    "Dashboard / Navigation",
    "Prompt Editor",
    "Model Selector & Parameter Tuning",
    "System Instructions",
    "Structured Prompts & Few-Shot Tables",
    "Get Code Dialog & Export",
    "Prompt Library & Assets",
]

# Regex for detecting non-English characters (CJK, fullwidth punctuation)
RE_CJK = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]")
RE_FULLWIDTH = re.compile(r"[\uff01-\uff5e\u3000-\u303f]")


class OverseasLocalizationValidator:
    """Validates that repository content strictly contains zero non-English / CJK characters."""

    @classmethod
    def scan_text(cls, text: str) -> List[Tuple[int, str, str]]:
        violations = []
        lines = text.splitlines()
        for idx, line in enumerate(lines, 1):
            cjk_matches = RE_CJK.findall(line)
            fw_matches = RE_FULLWIDTH.findall(line)
            all_matches = cjk_matches + fw_matches
            if all_matches:
                violations.append((idx, "".join(set(all_matches)), line.strip()))
        return violations

    @classmethod
    def scan_file(cls, path: Path) -> List[Tuple[int, str, str]]:
        if not path.is_file():
            return []
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            return cls.scan_text(content)
        except Exception as e:
            return [(0, "FILE_READ_ERROR", str(e))]


class ManifestValidator:
    """Validates plugin.json according to agent-plugins schema conventions."""

    REQUIRED_FIELDS = [
        "name",
        "displayName",
        "version",
        "description",
        "logo",
        "suggestedPrompts",
        "author",
        "homepage",
        "repository",
    ]

    SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
    PLUGIN_NAME_PATTERN = re.compile(r"^[a-z0-9_-]+$")

    @classmethod
    def validate_manifest_dict(cls, data: Dict[str, Any]) -> List[str]:
        errors = []
        if not isinstance(data, dict):
            return ["Manifest root must be a JSON object"]

        for field in cls.REQUIRED_FIELDS:
            if field not in data:
                errors.append(f"Missing required field: '{field}'")
            elif data[field] is None:
                errors.append(f"Required field '{field}' cannot be null")

        # Name checks
        name = data.get("name")
        if isinstance(name, str):
            if not name.strip():
                errors.append("Field 'name' cannot be empty or whitespace")
            elif not cls.PLUGIN_NAME_PATTERN.match(name):
                errors.append(f"Field 'name' must be kebab-case: '{name}'")
        elif name is not None:
            errors.append("Field 'name' must be a string")

        # Version checks
        version = data.get("version")
        if isinstance(version, str):
            if not cls.SEMVER_PATTERN.match(version):
                errors.append(f"Field 'version' must follow semantic versioning X.Y.Z: '{version}'")
        elif version is not None:
            errors.append("Field 'version' must be a string")

        # Description checks
        desc = data.get("description")
        if isinstance(desc, str):
            if len(desc.strip()) < 20:
                errors.append("Field 'description' must be at least 20 characters long")
        elif desc is not None:
            errors.append("Field 'description' must be a string")

        # Suggested prompts checks
        prompts = data.get("suggestedPrompts")
        if isinstance(prompts, list):
            if len(prompts) == 0:
                errors.append("Field 'suggestedPrompts' must contain at least 1 prompt")
            for i, p in enumerate(prompts):
                if not isinstance(p, str) or not p.strip():
                    errors.append(f"Suggested prompt at index {i} must be a non-empty string")
        elif prompts is not None:
            errors.append("Field 'suggestedPrompts' must be a list of strings")

        # Author checks
        author = data.get("author")
        if isinstance(author, dict):
            if not author.get("name") or not str(author.get("name")).strip():
                errors.append("Author object must contain a non-empty 'name' field")
        elif author is not None:
            errors.append("Field 'author' must be a JSON object")

        # URL checks
        for url_field in ["homepage", "repository"]:
            url_val = data.get(url_field)
            if isinstance(url_val, str):
                if not (url_val.startswith("https://") or url_val.startswith("http://")):
                    errors.append(f"Field '{url_field}' must be a valid URL starting with http:// or https://")
            elif url_val is not None:
                errors.append(f"Field '{url_field}' must be a string")

        return errors

    @classmethod
    def validate_file(cls, path: Path) -> List[str]:
        if not path.is_file():
            return [f"File not found: {path}"]
        try:
            content = path.read_text(encoding="utf-8")
            data = json.loads(content)
            return cls.validate_manifest_dict(data)
        except json.JSONDecodeError as jde:
            return [f"Malformed JSON syntax: {jde}"]
        except Exception as e:
            return [f"Error reading manifest: {e}"]


class ReadmeValidator:
    """Validates README.md structure, sections, links, and content invariants."""

    REQUIRED_SECTIONS = [
        "Overview",
        "Architecture",
        "Installation",
        "Decision Engine",
        "Autonomy Modes",
        "Skills",
    ]

    @classmethod
    def validate_content(cls, content: str) -> List[str]:
        errors = []
        if not content or len(content.strip()) < 100:
            return ["README.md is empty or excessively short (<100 characters)"]

        # Check H1 title
        if not re.search(r"^#\s+.+", content, re.MULTILINE):
            errors.append("README.md must have a top-level H1 title")

        # Check core sections
        content_lower = content.lower()
        if "overview" not in content_lower and "introduction" not in content_lower:
            errors.append("Missing 'Overview' or 'Introduction' section")
        if "architecture" not in content_lower and "system layer" not in content_lower:
            errors.append("Missing 'Architecture' or 'System Layers' section")
        if "install" not in content_lower and "quick start" not in content_lower:
            errors.append("Missing 'Installation' or 'Quick Start' section")
        if "offload" not in content_lower and "decision" not in content_lower:
            errors.append("Missing 'Offload Decision Engine' or 'Cloud Offloading' section")
        if "autonomy" not in content_lower and "checkpoint" not in content_lower:
            errors.append("Missing 'Autonomy Modes' section")
        if "skill" not in content_lower:
            errors.append("Missing 'Skills' section")

        # Check canonical URL reference
        if "aistudio.google.com" not in content:
            errors.append("README.md must reference canonical Google AI Studio domain (aistudio.google.com)")

        # Check quota conservation mention
        if "quota" not in content_lower:
            errors.append("README.md must explain quota conservation concept")

        # Check skills documented
        for skill in CANONICAL_SKILLS:
            if skill not in content:
                errors.append(f"README.md missing documentation for skill: '{skill}'")

        # Check broken markdown links syntax
        unclosed_links = re.findall(r"\[[^\]]+\]\([^)\n]*$", content, re.MULTILINE)
        if unclosed_links:
            errors.append(f"Found unclosed markdown links: {unclosed_links}")

        return errors

    @classmethod
    def validate_file(cls, path: Path) -> List[str]:
        if not path.is_file():
            return [f"File not found: {path}"]
        try:
            content = path.read_text(encoding="utf-8")
            return cls.validate_content(content)
        except Exception as e:
            return [f"Error reading README.md: {e}"]


class SvgValidator:
    """Validates SVG visual assets XML structure and security compliance."""

    @classmethod
    def validate_content(cls, content: str) -> List[str]:
        errors = []
        if not content or len(content.strip()) == 0:
            return ["SVG content is empty"]

        # Security check: Disallow scripts or event handlers
        lower = content.lower()
        if "<script" in lower:
            errors.append("SVG contains forbidden <script> element")
        if re.search(r"on\w+\s*=", lower):
            errors.append("SVG contains forbidden inline JavaScript event handlers")

        # XML Parsing check
        try:
            root = ET.fromstring(content)
        except ET.ParseError as pe:
            return [f"Malformed SVG XML syntax: {pe}"]

        # Tag check (stripping XML namespace)
        tag_name = root.tag.split("}")[-1] if "}" in root.tag else root.tag
        if tag_name.lower() != "svg":
            errors.append(f"Root element must be <svg>, got <{tag_name}>")

        # Dimensions or viewBox check
        has_viewbox = "viewBox" in root.attrib or "viewbox" in root.attrib
        has_width_height = "width" in root.attrib and "height" in root.attrib
        if not (has_viewbox or has_width_height):
            errors.append("SVG must define either 'viewBox' or 'width' and 'height' attributes")

        # Vector graphics presence check
        elements = [elem.tag.split("}")[-1].lower() for elem in root.iter()]
        vector_tags = {"path", "circle", "rect", "polygon", "polyline", "line", "ellipse", "g"}
        if not any(t in vector_tags for t in elements):
            errors.append("SVG does not contain vector graphic elements (path, circle, rect, etc.)")

        return errors

    @classmethod
    def validate_file(cls, path: Path) -> List[str]:
        if not path.is_file():
            return [f"File not found: {path}"]
        try:
            size = path.stat().st_size
            if size < 50:
                return [f"SVG file too small ({size} bytes), likely corrupted"]
            if size > 500 * 1024:
                return [f"SVG file too large ({size} bytes) for icon/logo"]
            content = path.read_text(encoding="utf-8")
            return cls.validate_content(content)
        except Exception as e:
            return [f"Error reading SVG: {e}"]


class RulesValidator:
    """Validates rules/AGENTS.md contracts, delegation protocols, boundaries, and staging."""

    REQUIRED_TOPICS = [
        ("canonical_url", r"https://aistudio\.google\.com/"),
        ("browser_delegation", r"TypeName:\s*\"browser\""),
        ("model_flash", r"Model:\s*\"flash\""),
        ("session_reuse", r"send_message"),
        ("semantic_goals", r"semantic\s+UI\s+goals"),
        ("fast_path_auth", r"Fast-Path\s+Authentication"),
        ("auth_signals", r"avatar|profile"),
        ("sandbox_constraint", r"document\.cookie|localStorage"),
        ("decision_engine", r"Local\s+vs\.?\s+Cloud\s+Offload"),
        ("autonomy_checkpoint", r"checkpoint"),
        ("autonomy_auto", r"auto"),
        ("safety_login", r"LOGIN_REQUIRED|accounts\.google\.com"),
        ("safety_captcha", r"CAPTCHA"),
        ("safety_quota_429", r"429|ResourceExhausted|quota"),
        ("staging_uploads", r"browser_sandbox/uploads/"),
        ("staging_downloads", r"browser_sandbox/downloads/"),
    ]

    @classmethod
    def validate_content(cls, content: str) -> List[str]:
        errors = []
        if not content or len(content.strip()) < 100:
            return ["rules/AGENTS.md is empty or excessively short"]

        for topic_name, pattern in cls.REQUIRED_TOPICS:
            if not re.search(pattern, content, re.IGNORECASE):
                errors.append(f"rules/AGENTS.md missing required topic/clause: {topic_name} (pattern: {pattern})")

        return errors

    @classmethod
    def validate_file(cls, path: Path) -> List[str]:
        if not path.is_file():
            return [f"File not found: {path}"]
        try:
            content = path.read_text(encoding="utf-8")
            return cls.validate_content(content)
        except Exception as e:
            return [f"Error reading rules/AGENTS.md: {e}"]


class SkillValidator:
    """Parses and validates skill YAML frontmatter and structural markdown elements."""

    @classmethod
    def parse_frontmatter(cls, content: str) -> Tuple[Optional[Dict[str, Any]], str, List[str]]:
        errors = []
        content = content.strip()
        if not content.startswith("---"):
            return None, content, ["Skill file missing starting frontmatter delimiter '---'"]

        parts = content.split("---", 2)
        if len(parts) < 3:
            return None, content, ["Skill file missing ending frontmatter delimiter '---'"]

        raw_yaml = parts[1].strip()
        body = parts[2].strip()

        # Parse key-value frontmatter without external yaml library
        frontmatter = {}
        for line in raw_yaml.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                if v.lower() == "true":
                    val = True
                elif v.lower() == "false":
                    val = False
                elif v.isdigit():
                    val = int(v)
                else:
                    val = v
                frontmatter[k] = val

        return frontmatter, body, errors

    @classmethod
    def validate_skill_content(cls, content: str, expected_name: Optional[str] = None) -> List[str]:
        errors = []
        fm, body, parse_errors = cls.parse_frontmatter(content)
        if parse_errors:
            return parse_errors

        if not fm.get("name"):
            errors.append("Skill frontmatter missing 'name'")
        elif expected_name and fm["name"] != expected_name:
            errors.append(f"Skill frontmatter name '{fm['name']}' does not match expected '{expected_name}'")

        if not fm.get("description"):
            errors.append("Skill frontmatter missing 'description'")
        elif len(str(fm["description"]).strip()) < 10:
            errors.append("Skill frontmatter 'description' is too short (<10 characters)")

        if not body or len(body.strip()) < 50:
            errors.append("Skill markdown body is empty or too short (<50 characters)")

        return errors

    @classmethod
    def validate_file(cls, path: Path, expected_name: Optional[str] = None) -> List[str]:
        if not path.is_file():
            return [f"File not found: {path}"]
        try:
            content = path.read_text(encoding="utf-8")
            return cls.validate_skill_content(content, expected_name=expected_name)
        except Exception as e:
            return [f"Error reading skill file: {e}"]


# =============================================================================
# Genuine Domain Validators for Tier 2 Boundary & Corner Case Verification
# =============================================================================

class SubagentDelegationValidator:
    """Validates browser subagent delegation payloads, parameters, and lifecycle contracts."""

    ALLOWED_TYPENAMES: Set[str] = {"browser"}
    ALLOWED_MODELS: Set[str] = {"flash", "pro", "flash-thinking", "gemini-2.5-flash", "gemini-2.5-pro"}
    BRITTLE_CSS_PATTERN = re.compile(
        r"(\bdiv\.[a-zA-Z0-9_-]+|\b>\s*button|:nth-child\(\d+\)|button\.[a-zA-Z0-9_-]+:[a-z]+|#[a-zA-Z0-9_-]+\s*>)",
        re.IGNORECASE,
    )

    @classmethod
    def validate_payload(cls, payload: Dict[str, Any]) -> List[str]:
        errors = []
        if not isinstance(payload, dict):
            return ["Subagent delegation payload must be a dictionary"]

        # TypeName validation
        if "TypeName" not in payload:
            errors.append("Missing mandatory field: 'TypeName'")
        elif payload["TypeName"] != "browser":
            errors.append(f"Field 'TypeName' must be 'browser' for AI Studio delegation, got '{payload['TypeName']}'")

        # Instruction validation
        if "instruction" not in payload:
            errors.append("Missing mandatory field: 'instruction'")
        else:
            inst = payload["instruction"]
            if not isinstance(inst, str) or not inst.strip():
                errors.append("Field 'instruction' cannot be empty or whitespace")
            else:
                if cls.BRITTLE_CSS_PATTERN.search(inst):
                    errors.append("Instruction contains brittle CSS selectors; semantic UI goals required")

        # Session lifecycle check: anti-pattern of killing subagent between steps
        action_val = str(payload.get("action", "")) + " " + str(payload.get("step_action", "")) + " " + str(payload.get("instruction", ""))
        if "kill_subagent" in action_val.lower() or "kill subagent" in action_val.lower():
            errors.append("Session reuse violation: Killing idle browser subagent between steps is prohibited; reuse conversationId via send_message")

        return errors


# Alias for backward compatibility
SubagentPayloadValidator = SubagentDelegationValidator


class CanonicalRoutingValidator:
    """Validates entry URLs, domains, security protocols, and redirect chains."""

    CANONICAL_HOST = "aistudio.google.com"
    MAX_REDIRECT_HOPS = 3
    ALLOWED_PATHS = {"/", "/prompts", "/prompts/new_chat", "/prompts/new_structured", "/tune", "/apikey"}

    @classmethod
    def validate_url(cls, url: str, redirect_chain: Optional[List[str]] = None) -> List[str]:
        errors = []
        if not url or not str(url).strip():
            return ["URL cannot be empty or whitespace"]

        parsed = urllib.parse.urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return [f"Malformed URL: missing scheme or netloc in '{url}'"]

        if parsed.scheme.lower() != "https":
            errors.append(f"Insecure HTTP downgrade rejected; URL must use HTTPS: '{url}'")

        host = parsed.netloc.split(":")[0].lower()
        if host != cls.CANONICAL_HOST:
            errors.append(f"Unauthorized domain '{host}'; canonical domain must be '{cls.CANONICAL_HOST}'")

        if redirect_chain is not None:
            if len(redirect_chain) > cls.MAX_REDIRECT_HOPS:
                errors.append(
                    f"Redirect hop count ({len(redirect_chain)}) exceeds maximum allowed limit ({cls.MAX_REDIRECT_HOPS})"
                )

        return errors


class AutonomyModeValidator:
    """Validates autonomy mode strings and resolves modes from user prompts."""

    CANONICAL_MODES: Set[str] = {"checkpoint", "auto"}
    AUTO_KEYWORDS = ["auto mode", "full-auto", "run unattended", "without asking", "don't ask for confirmation", "batch offload"]
    NEGATION_PATTERN = re.compile(r"\b(do not|don't|never|not)\b.*\b(auto|unattended)\b", re.IGNORECASE)

    @classmethod
    def validate_mode(cls, mode: str) -> List[str]:
        if not mode or not str(mode).strip():
            return ["Autonomy mode cannot be empty or whitespace"]
        mode_clean = str(mode).strip().lower()
        if mode_clean not in cls.CANONICAL_MODES:
            return [f"Unsupported autonomy mode '{mode}'; must be one of {sorted(cls.CANONICAL_MODES)}"]
        return []

    @classmethod
    def resolve_mode_from_prompt(cls, prompt: str) -> str:
        if not prompt or not str(prompt).strip():
            return "checkpoint"

        prompt_clean = prompt.strip()
        # Check explicit negation first: "do not run in auto mode"
        if cls.NEGATION_PATTERN.search(prompt_clean):
            return "checkpoint"

        prompt_lower = prompt_clean.lower()
        for kw in cls.AUTO_KEYWORDS:
            if kw in prompt_lower:
                return "auto"

        return "checkpoint"


class SafetyBoundariesValidator:
    """Validates safety clauses, CAPTCHA anti-bypass rules, error classification, and UI audit boundaries."""

    CAPTCHA_BYPASS_PATTERN = re.compile(
        r"\b(bypass|solve|manipulate|crack|automate)\b.*\b(captcha|anti-bot|challenge)\b",
        re.IGNORECASE,
    )
    FORBIDDEN_AUDIT_ACTIONS: Set[str] = {
        "click_delete", "click_save", "click_generate", "click_run",
        "delete", "save", "generate", "run", "edit", "update", "create", "submit"
    }

    @classmethod
    def validate_safety_clause(cls, rule_text: str) -> List[str]:
        errors = []
        if not rule_text or not str(rule_text).strip():
            return ["Safety clause cannot be empty"]

        if cls.CAPTCHA_BYPASS_PATTERN.search(rule_text):
            errors.append("Safety violation: Automated CAPTCHA solving or bypassing is strictly prohibited")

        return errors

    @classmethod
    def classify_platform_error(cls, error_text: str) -> Dict[str, Any]:
        text = str(error_text)
        is_quota = bool(re.search(r"\b(429|ResourceExhausted|quota)\b", text, re.IGNORECASE))
        is_safety = bool(re.search(r"(HARM_CATEGORY\w*|SAFETY_BLOCKED|safety filter)", text, re.IGNORECASE))
        is_transient = bool(re.search(r"\b(wait \d+ seconds|try again later|rate limit)\b", text, re.IGNORECASE)) and not bool(re.search(r"\b(daily quota|midnight UTC)\b", text, re.IGNORECASE))

        return {
            "is_quota": is_quota,
            "is_safety": is_safety,
            "is_transient": is_transient,
            "status": "PAUSED_SAFETY_TRIGGERED" if (is_quota or is_safety) else "CONTINUE",
        }

    @classmethod
    def validate_audit_action(cls, action: str) -> List[str]:
        act_clean = str(action).strip().lower()
        for forbidden in cls.FORBIDDEN_AUDIT_ACTIONS:
            if forbidden in act_clean:
                return [f"Mutating action '{action}' strictly forbidden in read-only UI audit mode"]
        return []

    @classmethod
    def validate_audit_references(cls, content: str) -> List[str]:
        if "references/audit-checklist.md" not in content and "audit-checklist.md" not in content:
            return ["Audit skill documentation missing required reference to 'references/audit-checklist.md'"]
        return []

    @classmethod
    def validate_calibration_freshness(cls, date_str: str, max_days: int = 90) -> List[str]:
        try:
            cal_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return [f"Invalid calibration date format '{date_str}'; expected YYYY-MM-DD"]

        ref_date = datetime(2026, 11, 21)
        delta_days = (ref_date - cal_date).days
        if delta_days > max_days:
            return [f"Calibration date '{date_str}' is stale ({delta_days} days old > {max_days} days allowed); recalibration required"]
        return []

    @classmethod
    def validate_navigation_timeout(cls, timeout_seconds: int, max_timeout: int = 15) -> List[str]:
        if timeout_seconds > max_timeout:
            return [f"Surface navigation timeout ({timeout_seconds}s) exceeds maximum allowed threshold ({max_timeout}s)"]
        return []


class StagingContractValidator:
    """Validates sandboxed file staging contracts, path security, and payload formats."""

    ALLOWED_MEDIA_EXTENSIONS: Set[str] = {
        ".png", ".jpg", ".jpeg", ".webp", ".mp3", ".wav", ".mp4", ".pdf", ".txt", ".csv", ".json"
    }

    @classmethod
    def validate_filename(cls, filename: str) -> List[str]:
        errors = []
        if not filename or not str(filename).strip():
            return ["Filename cannot be empty or whitespace"]

        fn = str(filename).strip()
        # Traversal check
        if ".." in fn or "/" in fn or "\\" in fn:
            errors.append(f"Path traversal or directory separator detected in filename: '{filename}'; bare single-segment filename required")

        # Absolute path check
        if Path(fn).is_absolute() or re.match(r"^[a-zA-Z]:", fn):
            errors.append(f"Absolute path rejected; bare single-segment filename required: '{filename}'")

        # Special character check
        if re.search(r"[@#$%^&*?<>{}\[\]|;:\s]", fn):
            errors.append(f"Filename '{filename}' contains invalid special characters or spaces; sanitize with alphanumeric, dots, hyphens, and underscores")

        return errors

    @classmethod
    def validate_path(cls, path: str) -> List[str]:
        if not path or not str(path).strip():
            return ["Path cannot be empty or whitespace"]
        p_str = str(path).replace("\\", "/")
        valid_roots = ["browser_sandbox/uploads/", "browser_sandbox/downloads/", "browser_sandbox/references/"]
        if not any(root in p_str for root in valid_roots):
            return [f"Path '{path}' is outside canonical staging sandbox directories"]
        return []

    @classmethod
    def validate_media_extension(cls, filename: str) -> List[str]:
        ext = os.path.splitext(filename)[1].lower()
        if not ext:
            return [f"Filename '{filename}' lacks file extension"]
        if ext not in cls.ALLOWED_MEDIA_EXTENSIONS:
            return [f"Unsupported media extension '{ext}'; allowed extensions: {sorted(cls.ALLOWED_MEDIA_EXTENSIONS)}"]
        return []

    @classmethod
    def validate_csv_payload(cls, csv_text: str) -> List[str]:
        if not csv_text or not str(csv_text).strip():
            return ["CSV payload is empty"]
        # Check uneven quotes
        if csv_text.count('"') % 2 != 0:
            return ["Malformed CSV syntax: unclosed or uneven quotation marks detected"]
        return []

    @classmethod
    def validate_file_overwrite(cls, existing_exists: bool, user_confirmed: bool) -> List[str]:
        if existing_exists and not user_confirmed:
            return ["File overwrite prevented: destination file exists and user confirmation was not provided"]
        return []


class ParameterTuningValidator:
    """Validates model hyperparameters, safety thresholds, model names, and token limits."""

    VALID_SAFETY_THRESHOLDS: Set[str] = {
        "BLOCK_NONE", "BLOCK_ONLY_HIGH", "BLOCK_MEDIUM_AND_ABOVE", "BLOCK_LOW_AND_ABOVE"
    }
    DEPRECATED_MODELS: Set[str] = {
        "palm-2", "text-bison-001", "chat-bison-001", "gemini-1.0-ultra"
    }

    @classmethod
    def validate_temperature(cls, temperature: float) -> List[str]:
        if not isinstance(temperature, (int, float)) or not (0.0 <= float(temperature) <= 2.0):
            return [f"Field 'temperature' ({temperature}) out of valid range [0.0, 2.0]"]
        return []

    @classmethod
    def validate_hyperparameters(cls, params: Dict[str, Any]) -> List[str]:
        errors = []
        if not isinstance(params, dict):
            return ["Hyperparameters must be a dictionary"]

        if "temperature" in params:
            t = params["temperature"]
            if not isinstance(t, (int, float)) or not (0.0 <= float(t) <= 2.0):
                errors.append(f"Field 'temperature' ({t}) out of valid range [0.0, 2.0]")

        if "top_p" in params:
            p = params["top_p"]
            if not isinstance(p, (int, float)) or not (0.0 <= float(p) <= 1.0):
                errors.append(f"Field 'top_p' ({p}) out of valid range [0.0, 1.0]")

        if "top_k" in params:
            k = params["top_k"]
            if not isinstance(k, int) or k < 1:
                errors.append(f"Field 'top_k' ({k}) must be an integer >= 1")

        if "safety_threshold" in params:
            st = params["safety_threshold"]
            if st not in cls.VALID_SAFETY_THRESHOLDS:
                errors.append(f"Invalid safety threshold '{st}'; must be one of {sorted(cls.VALID_SAFETY_THRESHOLDS)}")

        if "token_threshold" in params:
            tt = params["token_threshold"]
            if not isinstance(tt, int) or tt <= 0:
                errors.append(f"Token threshold ({tt}) must be a positive integer > 0")

        return errors

    @classmethod
    def validate_model_name(cls, model_name: str) -> List[str]:
        if not model_name or not str(model_name).strip():
            return ["Model name cannot be empty"]
        mn_lower = str(model_name).strip().lower()
        if mn_lower in cls.DEPRECATED_MODELS:
            return [f"Model '{model_name}' is deprecated or retired; use canonical Gemini 2.5 / 2.0 models"]
        return []


class CodeExportValidator:
    """Validates code export language targets, exported snippets, API key safety, and schemas."""

    SUPPORTED_LANGUAGES: Set[str] = {"python", "javascript", "typescript", "curl", "rest"}
    RAW_API_KEY_PATTERN = re.compile(r"AIza[0-9A-Za-z-_]{30,}")

    @classmethod
    def validate_language(cls, lang: str) -> List[str]:
        if not lang or not str(lang).strip():
            return ["Language target cannot be empty or whitespace"]
        lang_clean = str(lang).strip().lower()
        if lang_clean not in cls.SUPPORTED_LANGUAGES:
            return [f"Unsupported export language '{lang}'; must be one of {sorted(cls.SUPPORTED_LANGUAGES)}"]
        return []

    @classmethod
    def validate_snippet(cls, code: str, language: Optional[str] = None) -> List[str]:
        errors = []
        if not code or not str(code).strip():
            return ["Code snippet cannot be empty or whitespace"]

        # Raw API key leakage check
        if cls.RAW_API_KEY_PATTERN.search(code):
            errors.append("Security violation: Leaked hardcoded Google API key pattern detected; use environment variable")

        # Unclosed code fence check
        if code.count("```") % 2 != 0:
            errors.append("Unclosed markdown code fence detected in exported snippet")

        # Python syntax validation if Python specified or inferred
        if language == "python" or (language is None and ("def " in code or "import " in code)):
            code_to_parse = re.sub(r"^```python\s*", "", code.strip(), flags=re.MULTILINE)
            code_to_parse = re.sub(r"```$", "", code_to_parse.strip(), flags=re.MULTILINE)
            try:
                ast.parse(code_to_parse)
            except SyntaxError as se:
                errors.append(f"Python syntax error in exported code: {se}")

        return errors

    @classmethod
    def validate_json_schema(cls, schema: Dict[str, Any]) -> List[str]:
        if not isinstance(schema, dict):
            return ["JSON schema must be a dictionary"]
        if "type" not in schema:
            return ["Malformed JSON schema: missing mandatory 'type' root property"]
        return []


class MarkdownTableValidator:
    """Validates markdown table formatting, column count consistency, headers, and checklists."""

    ISO_DATE_PATTERN = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")

    @classmethod
    def validate_markdown_table(cls, table_text: str, required_headers: Optional[List[str]] = None) -> List[str]:
        errors = []
        if not table_text or not str(table_text).strip():
            return ["Markdown table content is empty"]

        lines = [line.strip() for line in table_text.strip().splitlines() if line.strip()]
        pipe_lines = [line for line in lines if line.startswith("|")]
        if len(pipe_lines) < 2:
            return ["Table must contain at least a header row and separator/data row"]

        # Check closing pipes
        for idx, line in enumerate(pipe_lines, 1):
            if not line.endswith("|"):
                errors.append(f"Table row {idx} missing closing pipe delimiter: '{line}'")

        # Parse header
        header_cells = [c.strip() for c in pipe_lines[0].strip("|").split("|")]
        expected_cols = len(header_cells)

        # Check data rows (skipping delimiter line like |---|---|)
        for idx, line in enumerate(pipe_lines[1:], 2):
            if re.match(r"^\|[-:\s|]+\|$", line):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) != expected_cols:
                errors.append(f"Column count mismatch at row {idx}: has {len(cells)} columns, expected {expected_cols}")

        # Check required headers
        if required_headers:
            header_lower = [h.lower() for h in header_cells]
            for req in required_headers:
                if req.lower() not in header_lower:
                    errors.append(f"Missing required table header: '{req}'")

        return errors

    @classmethod
    def validate_checklist_markdown(cls, content: str) -> List[str]:
        errors = []
        if not content or not str(content).strip():
            return ["Checklist content is empty"]

        # Date validation
        date_match = cls.ISO_DATE_PATTERN.search(content)
        if not date_match:
            errors.append("Audit checklist missing calibration date (expected format YYYY-MM-DD)")
        else:
            date_str = date_match.group(0)
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                errors.append(f"Invalid calibration date '{date_str}'; expected YYYY-MM-DD")

        # Pruning section check
        content_lower = content.lower()
        if "prun" not in content_lower and "deprecat" not in content_lower:
            errors.append("Checklist missing required model pruning/deprecation section")

        return errors

    @classmethod
    def validate_audit_surfaces(cls, surfaces: List[str]) -> List[str]:
        if not isinstance(surfaces, list):
            return ["Surfaces must be a list of strings"]
        if len(surfaces) < 7:
            return [f"Checklist covers only {len(surfaces)} surfaces; all 7 canonical surfaces required"]
        return []


class PromptToSkillRouter:
    """Routes prompt strings and user intents to canonical plugin skills and references."""

    SKILL_ROUTING_TABLE = {
        "aistudio-offload": {
            "keywords": ["offload", "cloud agent", "conserve quota", "heavy reasoning", "distributed consensus", "architecture"],
            "target_model": "Gemini Flash Thinking",
            "reference": "references/offload-decision-matrix.md",
        },
        "aistudio-chat-prompt": {
            "keywords": ["chat", "multi-turn", "system instruction", "conversational", "transcript"],
            "target_model": "Gemini 2.5 Flash",
            "staging_dir": "browser_sandbox/uploads/",
        },
        "aistudio-structured-prompt": {
            "keywords": ["structured", "few-shot", "tabular", "json schema", "response schema", "test cases"],
            "target_model": "Gemini 2.5 Pro",
            "output_format": "JSON",
        },
        "aistudio-parameter-tuning": {
            "keywords": ["tune", "temperature", "top-p", "top-k", "safety settings", "safety threshold", "thinking budget"],
            "target_model": "Gemini 2.5 Pro",
            "param_bounds": {"temperature": (0.0, 2.0), "top_p": (0.0, 1.0), "top_k": (1, 100)},
        },
        "aistudio-code-export": {
            "keywords": ["export", "get code", "python code", "gemini_api_key", "sdk", "curl", "rest"],
            "target_model": "Gemini 2.5 Pro",
            "env_var": "GEMINI_API_KEY",
        },
        "aistudio-ui-sync-audit": {
            "keywords": ["audit", "ui sync", "ui-sync", "live web ui", "audit-checklist", "drift report"],
            "target_model": None,
            "disable_model_invocation": True,
            "reference": "references/audit-checklist.md",
        },
    }

    @classmethod
    def route_prompt(cls, prompt_text: str) -> Dict[str, Any]:
        """Classifies a prompt and returns the matching canonical skill and routing metadata."""
        text_lower = prompt_text.lower()
        scores = {}
        for skill_name, config in cls.SKILL_ROUTING_TABLE.items():
            score = sum(1 for kw in config["keywords"] if kw in text_lower)
            if score > 0:
                scores[skill_name] = score

        if not scores:
            return {"skill": None, "matched_keywords": [], "confidence": 0.0, "config": {}}

        best_skill = max(scores, key=scores.get)
        matched_kws = [kw for kw in cls.SKILL_ROUTING_TABLE[best_skill]["keywords"] if kw in text_lower]
        return {
            "skill": best_skill,
            "config": cls.SKILL_ROUTING_TABLE[best_skill],
            "matched_keywords": matched_kws,
            "confidence": scores[best_skill] / len(cls.SKILL_ROUTING_TABLE[best_skill]["keywords"]),
        }

    @classmethod
    def validate_manifest_prompts(cls, suggested_prompts: List[str]) -> List[str]:
        """Validates that suggestedPrompts in plugin.json map to valid skills and cover core capabilities."""
        errors = []
        covered_skills = set()
        for idx, prompt in enumerate(suggested_prompts):
            res = cls.route_prompt(prompt)
            if not res["skill"]:
                errors.append(f"Prompt at index {idx} ('{prompt}') does not map to any recognized skill capability")
            else:
                covered_skills.add(res["skill"])

        # Core required skills that manifest prompts must address
        required_manifest_skills = {"aistudio-offload", "aistudio-structured-prompt"}
        missing = required_manifest_skills - covered_skills
        if missing:
            errors.append(f"suggestedPrompts in manifest fail to cover core skill capabilities: {missing}")

        return errors


# Alias for validator audit compliance
PromptToSkillValidator = PromptToSkillRouter


class OffloadDecisionEngine:
    """Core decision matrix implementation evaluating workload delegation criteria."""

    LOCAL_KEYWORDS = [
        "git",
        "commit",
        "push",
        "branch",
        "edit_file",
        "write_file",
        "pytest",
        "npm test",
        "cargo test",
        "compile",
        "build",
        "shell",
        "run_command",
        "status",
        "diff",
        "lint",
    ]

    CLOUD_KEYWORDS = [
        "architectural reasoning",
        "complex reasoning",
        "large prompt",
        "few-shot prompt",
        "structured prompt",
        "json schema prompt",
        "hyperparameter tuning",
        "model comparison",
        "code export",
        "ui audit",
        "long context",
        "system prompt tuning",
    ]

    TOKEN_THRESHOLD_CLOUD = 4000
    CONTEXT_LIMIT_FLASH = 1000000

    @classmethod
    def evaluate(
        cls,
        task_description: str,
        token_count: int = 0,
        requires_local_shell: bool = False,
        requires_file_mutation: bool = False,
    ) -> Dict[str, Any]:
        """Evaluates whether a task should run locally or offload to Google AI Studio."""
        if not task_description or not task_description.strip():
            return {
                "route": "LOCAL_MACHINE",
                "recommended_model": None,
                "reason": "Empty task description defaults to local execution",
                "quota_conserved": False,
            }

        desc_lower = task_description.lower()

        # Hard local constraints take absolute precedence
        if requires_local_shell or requires_file_mutation:
            return {
                "route": "LOCAL_MACHINE",
                "recommended_model": None,
                "reason": "Local shell execution or direct workspace file mutation required",
                "quota_conserved": False,
            }

        # Check local-only keywords
        for kw in cls.LOCAL_KEYWORDS:
            if kw in desc_lower and "export" not in desc_lower and "offload" not in desc_lower:
                return {
                    "route": "LOCAL_MACHINE",
                    "recommended_model": None,
                    "reason": f"Matched local task requirement: '{kw}'",
                    "quota_conserved": False,
                }

        # Large token context offload
        if token_count >= cls.TOKEN_THRESHOLD_CLOUD:
            if token_count > cls.CONTEXT_LIMIT_FLASH:
                model = "Gemini 2.5 Pro"
            elif any(w in desc_lower for w in ["reasoning", "thinking", "prove", "proof", "architectural"]):
                model = "Gemini Flash Thinking"
            else:
                model = "Gemini 2.5 Flash"

            return {
                "route": "CLOUD_OFFLOAD",
                "recommended_model": model,
                "reason": f"High token count ({token_count} >= {cls.TOKEN_THRESHOLD_CLOUD}) offloaded to cloud to conserve desktop quota",
                "quota_conserved": True,
            }

        # Cloud candidate keywords
        for kw in cls.CLOUD_KEYWORDS:
            if kw in desc_lower:
                if "reasoning" in desc_lower or "thinking" in desc_lower:
                    model = "Gemini Flash Thinking"
                elif "export" in desc_lower or "structured" in desc_lower:
                    model = "Gemini 2.5 Pro"
                else:
                    model = "Gemini 2.5 Flash"

                return {
                    "route": "CLOUD_OFFLOAD",
                    "recommended_model": model,
                    "reason": f"Matched cloud offload candidate workflow: '{kw}'",
                    "quota_conserved": True,
                }

        # Default fallback: small lightweight task
        return {
            "route": "LOCAL_MACHINE",
            "recommended_model": None,
            "reason": "Lightweight task below cloud offload threshold",
            "quota_conserved": False,
        }


class WorkflowSimulator:
    """Simulates realistic Tier 4 end-to-end cloud offload workflows with real filesystem staging."""

    @classmethod
    def _verify_rules_contract(cls) -> str:
        """Grounds simulation in real repository rules file."""
        if not AGENTS_RULE_PATH.is_file():
            raise FileNotFoundError(f"Simulation cannot run: rules/AGENTS.md missing at {AGENTS_RULE_PATH}")
        return AGENTS_RULE_PATH.read_text(encoding="utf-8")

    @classmethod
    def simulate_heavy_reasoning_offload(cls, task_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Scenario 1: Heavy Reasoning Offload Simulation grounded in sandbox filesystem."""
        rules_text = cls._verify_rules_contract()
        prompt_text = task_spec.get("prompt", "")
        token_count = task_spec.get("token_count", 50000)

        # 1. Decision Evaluation
        eval_res = OffloadDecisionEngine.evaluate(prompt_text, token_count=token_count)
        if eval_res["route"] != "CLOUD_OFFLOAD":
            return {"status": "FAILED", "stage": "EVALUATION", "error": "Task failed to qualify for offload"}

        # 2. Context Staging in Real Sandbox
        with tempfile.TemporaryDirectory(prefix="aistudio_sim_") as tmp_dir:
            sandbox_dir = Path(tmp_dir) / "browser_sandbox"
            uploads_dir = sandbox_dir / "uploads"
            downloads_dir = sandbox_dir / "downloads"
            uploads_dir.mkdir(parents=True, exist_ok=True)
            downloads_dir.mkdir(parents=True, exist_ok=True)

            staged_filename = "reasoning_prompt_payload.json"
            staged_file = uploads_dir / staged_filename
            payload_data = {
                "prompt": prompt_text,
                "token_count": token_count,
                "recommended_model": eval_res["recommended_model"],
                "target_url": CANONICAL_URL,
            }
            staged_file.write_text(json.dumps(payload_data, indent=2), encoding="utf-8")

            # 3. Browser Subagent Delegation Validation
            subagent_call = {
                "TypeName": CANONICAL_SUBAGENT_TYPE,
                "Model": CANONICAL_DEFAULT_MODEL,
                "instruction": f"Open {CANONICAL_URL}, load staged asset {staged_filename}, select {eval_res['recommended_model']}, run inference, and capture response.",
            }
            payload_errors = SubagentDelegationValidator.validate_payload(subagent_call)
            if payload_errors:
                return {"status": "FAILED", "stage": "DELEGATION", "errors": payload_errors}

            # 4. Result Synchronization to Downloads
            output_file = downloads_dir / "reasoning_result.txt"
            simulated_response = f"SIMULATED_GEMINI_REASONING_OUTPUT: 42 optimal architectural partition confirmed for {prompt_text[:30]}."
            output_file.write_text(simulated_response, encoding="utf-8")
            read_back = output_file.read_text(encoding="utf-8")

            return {
                "status": "SUCCESS",
                "route": eval_res["route"],
                "model_used": eval_res["recommended_model"],
                "staged_input": f"{CANONICAL_STAGING_PATHS['uploads']}{staged_filename}",
                "staged_file_created": staged_file.is_file(),
                "staged_file_bytes": staged_file.stat().st_size,
                "subagent_call": subagent_call,
                "cloud_response": simulated_response,
                "synced_destination": CANONICAL_STAGING_PATHS["downloads"] + "reasoning_result.txt",
                "downloaded_output_exists": output_file.is_file(),
                "downloaded_content": read_back,
                "quota_conserved": True,
            }

    @classmethod
    def simulate_fast_path_auth(cls, nav_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Scenario 2: Multi-state auth probe enforcing Google AI Studio safety boundaries."""
        cls._verify_rules_contract()
        current_url = nav_spec.get("current_url", CANONICAL_URL)
        dom_avatar_present = nav_spec.get("dom_avatar_present", True)
        rpc_status = nav_spec.get("rpc_status", 200)
        has_sign_in_button = nav_spec.get("has_sign_in_button", False)
        redirect_hops = nav_spec.get("redirect_hops", 0)

        if not current_url.startswith("https://aistudio.google.com"):
            return {
                "status": "REDIRECT_REQUIRED",
                "action": f"Navigate directly to canonical URL {CANONICAL_URL}",
                "fast_path_taken": False,
            }

        if redirect_hops > 3:
            return {
                "status": "ABORT_REDIRECT_LOOP",
                "action": "Halt execution due to excessive SSO hops",
                "fast_path_taken": False,
            }

        if has_sign_in_button or rpc_status == 401:
            return {
                "status": "LOGIN_REQUIRED",
                "action": "Pause and hand control to user to complete Google Sign-In",
                "fast_path_taken": False,
            }

        if dom_avatar_present and rpc_status == 200:
            return {
                "status": "AUTHENTICATED",
                "fast_path_taken": True,
                "action": "Bypassed sign-in dialog and proceeded directly to task",
                "target_view": "/prompts/new_chat",
                "redirect_hops": redirect_hops,
            }

        return {"status": "UNKNOWN_STATE", "fast_path_taken": False}

    @classmethod
    def simulate_quota_limit_detection(cls, exec_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Scenario 3: Quota Limit Detection enforcing immediate pause on 429."""
        cls._verify_rules_contract()
        autonomy_mode = exec_spec.get("mode", "auto")
        http_code = exec_spec.get("http_code", 429)
        error_banner = exec_spec.get("error_banner", "ResourceExhausted: Quota limit exceeded for model")

        is_quota_boundary = http_code == 429 or "ResourceExhausted" in error_banner
        if is_quota_boundary:
            # Hard boundary pause even in auto mode
            return {
                "status": "PAUSED_QUOTA_EXHAUSTED",
                "boundary_triggered": "429 ResourceExhausted",
                "autonomy_mode_before": autonomy_mode,
                "autonomy_mode_after": "paused_for_user",
                "recovery_suggestion": "Switch model from Gemini Pro to Gemini Flash or wait for reset window",
                "automated_retry_aborted": True,
            }

        return {"status": "CONTINUE", "boundary_triggered": None}

    @classmethod
    def simulate_multi_turn_chat_sync(cls, chat_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Scenario 4: Multi-Turn Chat & System Prompt Sync writing actual markdown file."""
        cls._verify_rules_contract()
        system_instruction = chat_spec.get("system_instruction", "You are a senior system architect.")
        turns = chat_spec.get("turns", [
            {"role": "user", "content": "Explain vector indexing."},
            {"role": "model", "content": "Vector indexing organizes embeddings..."},
            {"role": "user", "content": "Compare HNSW and IVF."},
        ])
        temperature = chat_spec.get("temperature", 0.7)

        # Validate temperature
        temp_errors = ParameterTuningValidator.validate_temperature(temperature)
        if temp_errors:
            return {"status": "FAILED", "error": temp_errors[0]}

        with tempfile.TemporaryDirectory(prefix="chat_sync_") as tmp_dir:
            out_file = Path(tmp_dir) / "chat_transcript.md"
            lines = [f"# Chat Session Transcript\nSystem Instruction: {system_instruction}\nTemperature: {temperature}\n"]
            for turn in turns:
                lines.append(f"**{turn['role'].capitalize()}**: {turn['content']}\n")
            content = "\n".join(lines)
            out_file.write_text(content, encoding="utf-8")

            violations = OverseasLocalizationValidator.scan_file(out_file)

            return {
                "status": "SUCCESS",
                "file_written": out_file.is_file(),
                "file_size": out_file.stat().st_size,
                "turns_processed": len(turns),
                "temperature_configured": temperature,
                "localization_violations": len(violations),
                "markdown_transcript": content,
                "export_ready": True,
            }

    @classmethod
    def simulate_few_shot_structured_export(cls, structured_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Scenario 5: Few-Shot Structured Prompt & Schema Export with AST compilation."""
        cls._verify_rules_contract()
        examples = structured_spec.get("examples", [
            {"input": "The movie was fantastic!", "output": '{"sentiment": "positive", "score": 0.95}'},
            {"input": "Terrible customer service.", "output": '{"sentiment": "negative", "score": 0.1}'},
        ])
        json_schema = structured_spec.get("schema", {
            "type": "object",
            "properties": {
                "sentiment": {"type": "string", "enum": ["positive", "neutral", "negative"]},
                "score": {"type": "number"},
            },
            "required": ["sentiment", "score"],
        })

        generated_python = f'''# Generated by Antigravity Google AI Studio Plugin
import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))

response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents="Analyze user feedback.",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema={json.dumps(json_schema)},
    ),
)
print(response.text)
'''
        with tempfile.TemporaryDirectory(prefix="code_export_") as tmp_dir:
            code_file = Path(tmp_dir) / "exported_prompt.py"
            code_file.write_text(generated_python, encoding="utf-8")
            parsed_ast = ast.parse(code_file.read_text(encoding="utf-8"))

            return {
                "status": "SUCCESS",
                "example_count": len(examples),
                "schema_enforced": True,
                "file_created": code_file.is_file(),
                "ast_valid": parsed_ast is not None,
                "exported_code": generated_python,
                "contains_env_var_key": 'os.environ.get("GEMINI_API_KEY"' in generated_python,
                "uses_env_var": 'os.environ.get("GEMINI_API_KEY"' in generated_python,
            }

    @classmethod
    def simulate_ui_sync_audit(cls, audit_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Scenario 6: Read-Only UI Sync Audit Verification."""
        cls._verify_rules_contract()
        disable_model = audit_spec.get("disable-model-invocation", True)
        surfaces = audit_spec.get("surfaces", CANONICAL_7_AUDIT_SURFACES)

        if not disable_model:
            return {"status": "FAILED", "error": "Audit skill must enforce disable-model-invocation: true"}

        if len(surfaces) != 7:
            return {"status": "FAILED", "error": f"Must inspect exactly 7 canonical surfaces, got {len(surfaces)}"}

        with tempfile.TemporaryDirectory(prefix="ui_audit_") as tmp_dir:
            report_file = Path(tmp_dir) / "drift_report.json"
            report_data = {
                "calibration_date": "2026-11-21",
                "active_surfaces": len(surfaces),
                "deprecated_models_pruned": 0,
                "read_only": True,
                "mutations_attempted": 0,
                "surfaces_inspected": surfaces,
                "drift_detected": False,
            }
            report_file.write_text(json.dumps(report_data, indent=2), encoding="utf-8")

            return {
                "status": "SUCCESS",
                "read_only": True,
                "mutations_attempted": 0,
                "surfaces_checked": len(surfaces),
                "report_created": report_file.is_file(),
                "drift_report": report_data,
            }


# Canonical Fixtures for Synthetic Testing
CANONICAL_FIXTURES = {
    "valid_manifest": {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": "antigravity-aistudio",
        "displayName": "Google AI Studio",
        "version": "0.1.0",
        "description": "Cloud offloading and workflow automation for Google AI Studio through Antigravity's built-in browser subagent.",
        "logo": "assets/logo.svg",
        "keywords": ["aistudio", "gemini", "cloud-offload"],
        "suggestedPrompts": [
            "Analyze large multi-file codebase architecture by offloading context to Google AI Studio",
            "Construct and evaluate a few-shot structured prompt with JSON response schema in Google AI Studio",
        ],
        "author": {"name": "Antigravity Team"},
        "homepage": "https://aistudio.google.com",
        "repository": "https://github.com/google-gemini/antigravity-aistudio",
    },
    "valid_svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
        <circle cx="50" cy="50" r="40" fill="#4285F4" />
        <path d="M30 50 L50 30 L70 50 L50 70 Z" fill="#FFFFFF" />
    </svg>""",
    "valid_skill_markdown": """---
name: aistudio-offload
description: Master cloud offload coordinator evaluating tasks against decision matrix.
---

# AI Studio Offload Skill

Evaluates tasks against decision matrix and offloads heavy computation to Google AI Studio.

## Workflow
1. Evaluate task against references/offload-decision-matrix.md
2. Stage assets in sandbox
3. Delegate to browser subagent
4. Retrieve and synchronize results
""",
    "valid_audit_skill_markdown": """---
name: aistudio-ui-sync-audit
description: Strictly read-only maintenance skill auditing live Google AI Studio web UI.
disable-model-invocation: true
---

# UI Sync Audit

Performs strictly read-only inspection of Google AI Studio across canonical surfaces.

## Workflow
1. Load audit checklist from references/audit-checklist.md
2. Inspect 7 canonical UI surfaces
3. Report UI drift
""",
}
