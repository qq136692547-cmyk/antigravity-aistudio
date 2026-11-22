"""
generate_infographics.py
Renders two ultra-high-density technical infographics for the antigravity-aistudio v0.2.0 project:
1. assets/architecture-offload-pipeline.png (1920x1100)
2. assets/modular-skills-ecosystem.png (1920x1100)
Uses Pillow with Segoe UI and Consolas fonts. Strict 7-bit ASCII source.
"""

import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)


def get_font(name, size):
    font_paths = {
        "regular": "C:/Windows/Fonts/segoeui.ttf",
        "semibold": "C:/Windows/Fonts/segoeuisb.ttf",
        "bold": "C:/Windows/Fonts/segoeuib.ttf",
        "mono": "C:/Windows/Fonts/consola.ttf",
        "mono_bold": "C:/Windows/Fonts/consolab.ttf",
    }
    path = font_paths.get(name, font_paths["regular"])
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


# Color Palette
BG_DARK = (11, 15, 25)           # #0B0F19 deep slate navy
GRID_COLOR = (22, 31, 48)        # #161F30 subtle grid lines
CARD_BG = (17, 24, 39)           # #111827 card background
CARD_BG_ALT = (23, 32, 51)       # #172033 elevated card bg
BORDER_SUBTLE = (38, 50, 72)     # #263248 card border
BORDER_ACTIVE = (59, 130, 246)   # #3B82F6 blue border highlight
BORDER_CYAN = (0, 201, 167)      # #00C9A7 cyan border
BORDER_PURPLE = (155, 114, 203)  # #9B72CB purple border

TEXT_WHITE = (248, 250, 252)     # #F8FAFC crisp white
TEXT_MUTED = (148, 163, 184)     # #94A3B8 slate gray
TEXT_DIM = (100, 116, 139)       # #64748B dim text
TEXT_CYAN = (56, 189, 248)       # #38BDF8 light blue / cyan
TEXT_GREEN = (74, 222, 128)      # #4ADE80 emerald
TEXT_AMBER = (251, 191, 36)      # #FBBF24 amber
TEXT_PURPLE = (192, 132, 252)    # #C084FC purple

ACCENT_BLUE = (66, 133, 244)     # Google Blue
ACCENT_CYAN = (0, 201, 167)      # Teal/Cyan
ACCENT_GREEN = (52, 168, 83)     # Google Green
ACCENT_AMBER = (251, 188, 4)     # Google Yellow/Amber
ACCENT_RED = (234, 67, 53)       # Google Red
ACCENT_PURPLE = (155, 114, 203)  # Studio Purple


def draw_grid_background(draw, width, height, step=40):
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=GRID_COLOR, width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=GRID_COLOR, width=1)


def draw_badge(draw, x, y, text, font, bg_color, border_color, text_color):
    bbox = font.getbbox(text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 12, 6
    w, h = tw + pad_x * 2, th + pad_y * 2
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=bg_color, outline=border_color, width=1)
    draw.text((x + pad_x, y + pad_y - bbox[1]), text, font=font, fill=text_color)
    return w, h


def draw_pill(draw, x_right, y, text, font, bg_color, text_color):
    bbox = font.getbbox(text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 10, 4
    w, h = tw + pad_x * 2, th + pad_y * 2
    x = x_right - w
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=bg_color)
    draw.text((x + pad_x, y + pad_y - bbox[1]), text, font=font, fill=text_color)
    return w, h


def draw_stat_card(draw, x, y, w, h, stat_num, stat_label, subtext, accent_color):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD_BG, outline=BORDER_SUBTLE, width=1)
    draw.rounded_rectangle([x + 12, y, x + w - 12, y + 3], radius=2, fill=accent_color)

    font_num = get_font("bold", 26)
    font_label = get_font("semibold", 14)
    font_sub = get_font("regular", 12)

    draw.text((x + 18, y + 16), stat_num, font=font_num, fill=accent_color)
    draw.text((x + 18, y + 52), stat_label, font=font_label, fill=TEXT_WHITE)
    draw.text((x + 18, y + 73), subtext, font=font_sub, fill=TEXT_MUTED)


# ==============================================================================
# INFOGRAPHIC 1: ARCHITECTURE & OFFLOAD PIPELINE (v0.2.0 Pure Gemini 4)
# ==============================================================================
def generate_architecture_pipeline_infographic():
    width, height = 1920, 1100
    img = Image.new("RGB", (width, height), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_grid_background(draw, width, height, step=40)

    # 1. Header Section
    tag_font = get_font("mono_bold", 12)
    title_font = get_font("bold", 34)
    subtitle_font = get_font("regular", 16)

    bx = 60
    w1, _ = draw_badge(draw, bx, 35, "ANTIGRAVITY PLUGIN v0.2.0", tag_font, (20, 30, 45), ACCENT_BLUE, TEXT_CYAN)
    bx += w1 + 14
    w2, _ = draw_badge(draw, bx, 35, "PURE GEMINI 4 ARCHITECTURE", tag_font, (35, 25, 45), ACCENT_PURPLE, TEXT_PURPLE)
    bx += w2 + 14
    w3, _ = draw_badge(draw, bx, 35, "THINKING FLOOR HIGH+", tag_font, (15, 35, 25), ACCENT_GREEN, TEXT_GREEN)

    draw.text((60, 75), "Cloud Agent Offloading Architecture & Execution Pipeline", font=title_font, fill=TEXT_WHITE)
    draw.text((60, 122), "Zero-daemon bridge from Antigravity Local Workspace to Google AI Studio Gemini 4 Models (Hydrogen / Argon / Neon / Carbon)", font=subtitle_font, fill=TEXT_MUTED)

    # 2. Top Metric Cards (Row of 4)
    my = 160
    cw = 425
    ch = 100
    draw_stat_card(draw, 60, my, cw, ch, "1,000,000 Tokens", "Unified 1M Frontier Context", "All 4 Gemini 4 models (up to 64K output)", ACCENT_CYAN)
    draw_stat_card(draw, 515, my, cw, ch, "Thinking High+", "Mandatory Reasoning Floor", "High (UI) / high-xhigh (API); Low/Med banned", ACCENT_PURPLE)
    draw_stat_card(draw, 970, my, cw, ch, "0 Local Burn", "Desktop IDE Quota Shield", "Preserves local Neon, Argon & Opus quotas", ACCENT_GREEN)
    draw_stat_card(draw, 1425, my, cw, ch, "Zero Daemons", "Native Browser Subagent", "URL context + Search + 5-Tier E2E QA", ACCENT_BLUE)

    # 3. Main Architecture Diagram: 3 High-Density Columns
    col_y = 280
    col_h = 630

    # Column 1: LOCAL WORKSPACE (Antigravity IDE)
    c1_x, c1_w = 60, 560
    draw.rounded_rectangle([c1_x, col_y, c1_x + c1_w, col_y + col_h], radius=14, fill=CARD_BG, outline=BORDER_SUBTLE, width=1)
    draw.rounded_rectangle([c1_x, col_y, c1_x + c1_w, col_y + 45], radius=14, fill=CARD_BG_ALT)
    draw.rectangle([c1_x, col_y + 30, c1_x + c1_w, col_y + 45], fill=CARD_BG_ALT)
    draw.text((c1_x + 20, col_y + 12), "LOCAL WORKSPACE (Antigravity IDE)", font=get_font("bold", 16), fill=TEXT_CYAN)
    draw.text((c1_x + c1_w - 165, col_y + 14), "LOCAL BOUNDARY", font=get_font("mono_bold", 11), fill=TEXT_DIM)

    # Col 1 - Box A: Developer Request & Decision Engine
    bx_y = col_y + 60
    draw.rounded_rectangle([c1_x + 16, bx_y, c1_x + c1_w - 16, bx_y + 130], radius=8, fill=(20, 28, 44), outline=(45, 60, 85), width=1)
    draw.text((c1_x + 28, bx_y + 12), "1. Developer Task & Gemini 4 Router", font=get_font("bold", 14), fill=TEXT_WHITE)
    draw.text((c1_x + 28, bx_y + 36), "Input: Natural language prompt or automated offload trigger", font=get_font("regular", 12), fill=TEXT_MUTED)
    draw.text((c1_x + 28, bx_y + 56), "Evaluator: rules/AGENTS.md + offload-decision-matrix.md", font=get_font("mono", 11), fill=TEXT_CYAN)
    draw.text((c1_x + 28, bx_y + 80), "Split: Local Execution vs Gemini 4 Cloud Offload", font=get_font("semibold", 12), fill=TEXT_AMBER)
    draw.text((c1_x + 28, bx_y + 102), "[+] Enforces 4K+ token threshold & blocks pre-Gemini-4 models", font=get_font("regular", 11), fill=TEXT_MUTED)

    # Col 1 - Box B: Local Retained Operations (No Offload)
    bx_y = col_y + 205
    draw.rounded_rectangle([c1_x + 16, bx_y, c1_x + c1_w - 16, bx_y + 115], radius=8, fill=(16, 24, 38), outline=BORDER_SUBTLE, width=1)
    draw.text((c1_x + 28, bx_y + 12), "Local Execution Paths (Retained Locally)", font=get_font("bold", 13), fill=TEXT_MUTED)
    draw.text((c1_x + 28, bx_y + 34), "* File Edits: apply_edits, write_file (< 50 lines / surgical patches)", font=get_font("regular", 11), fill=TEXT_DIM)
    draw.text((c1_x + 28, bx_y + 54), "* Git Operations: git status, git diff, commits, branch management", font=get_font("regular", 11), fill=TEXT_DIM)
    draw.text((c1_x + 28, bx_y + 74), "* Test Suite: run_checks, pytest, npm test, cargo test execution", font=get_font("regular", 11), fill=TEXT_DIM)
    draw.text((c1_x + 28, bx_y + 94), "* Terminal Commands: Local build compilation, OS diagnostic scripts", font=get_font("regular", 11), fill=TEXT_DIM)

    # Col 1 - Box C: Local Sandbox Staging Contract
    bx_y = col_y + 335
    draw.rounded_rectangle([c1_x + 16, bx_y, c1_x + c1_w - 16, bx_y + 145], radius=8, fill=(20, 28, 44), outline=(38, 70, 95), width=1)
    draw.text((c1_x + 28, bx_y + 12), "2. Sandbox Staging Contract", font=get_font("bold", 14), fill=TEXT_WHITE)
    draw.text((c1_x + 28, bx_y + 36), "Directory: <ArtifactDir>/browser_sandbox/", font=get_font("mono_bold", 12), fill=TEXT_CYAN)
    draw.text((c1_x + 28, bx_y + 60), "- uploads/   : Local files staged for cloud ingestion", font=get_font("mono", 11), fill=TEXT_WHITE)
    draw.text((c1_x + 28, bx_y + 82), "- references/: Visual captures, UI mockups for inspection", font=get_font("mono", 11), fill=TEXT_MUTED)
    draw.text((c1_x + 28, bx_y + 104), "- downloads/ : Code, JSON schemas & artifacts returned", font=get_font("mono", 11), fill=TEXT_GREEN)
    draw.text((c1_x + 28, bx_y + 126), "Strict single-segment naming rule + sandbox boundary guard", font=get_font("regular", 11), fill=TEXT_AMBER)

    # Col 1 - Box D: Local Synchronization & Validation
    bx_y = col_y + 495
    draw.rounded_rectangle([c1_x + 16, bx_y, c1_x + c1_w - 16, bx_y + 115], radius=8, fill=(18, 30, 42), outline=BORDER_CYAN, width=1)
    draw.text((c1_x + 28, bx_y + 12), "6. Local Workspace Synchronization", font=get_font("bold", 14), fill=TEXT_GREEN)
    draw.text((c1_x + 28, bx_y + 36), "- Copies downloaded code/artifacts to target workspace files", font=get_font("regular", 11), fill=TEXT_WHITE)
    draw.text((c1_x + 28, bx_y + 56), "- Validates JSON Schema & enforces thinking_level High+", font=get_font("regular", 11), fill=TEXT_MUTED)
    draw.text((c1_x + 28, bx_y + 76), "- Strips raw keys (GEMINI_API_KEY) & runs 5-Tier E2E suite", font=get_font("regular", 11), fill=TEXT_CYAN)
    draw.text((c1_x + 28, bx_y + 96), "- Reports verified output (zero local quota burned)", font=get_font("semibold", 11), fill=TEXT_GREEN)

    # Column 2: BROWSER SUBAGENT AUTOMATION BRIDGE
    c2_x, c2_w = 645, 570
    draw.rounded_rectangle([c2_x, col_y, c2_x + c2_w, col_y + col_h], radius=14, fill=CARD_BG, outline=BORDER_SUBTLE, width=1)
    draw.rounded_rectangle([c2_x, col_y, c2_x + c2_w, col_y + 45], radius=14, fill=CARD_BG_ALT)
    draw.rectangle([c2_x, col_y + 30, c2_x + c2_w, col_y + 45], fill=CARD_BG_ALT)
    draw.text((c2_x + 20, col_y + 12), "BROWSER SUBAGENT BRIDGE (Zero-Daemon)", font=get_font("bold", 16), fill=ACCENT_BLUE)
    draw.text((c2_x + c2_w - 165, col_y + 14), "ISOLATED AGENT", font=get_font("mono_bold", 11), fill=TEXT_DIM)

    # Col 2 - Box A: Fast-Path Authentication & Safety Gate
    bx_y = col_y + 60
    draw.rounded_rectangle([c2_x + 16, bx_y, c2_x + c2_w - 16, bx_y + 130], radius=8, fill=(20, 28, 44), outline=(40, 65, 110), width=1)
    draw.text((c2_x + 28, bx_y + 12), "3. Fast-Path Auth & Security Guard", font=get_font("bold", 14), fill=TEXT_WHITE)
    draw.text((c2_x + 28, bx_y + 36), "- Reuses active Google AI Studio session (Zero cookies read)", font=get_font("regular", 12), fill=TEXT_CYAN)
    draw.text((c2_x + 28, bx_y + 56), "- Fast probe via Avatar / Prompts RPC signals (< 1.5s latency)", font=get_font("regular", 11), fill=TEXT_MUTED)
    draw.text((c2_x + 28, bx_y + 78), "Safety Stops (Fail Loudly):", font=get_font("semibold", 11), fill=TEXT_AMBER)
    draw.text((c2_x + 36, bx_y + 96), "* LOGIN_REQUIRED / CAPTCHA -> Immediate user handoff", font=get_font("regular", 11), fill=TEXT_MUTED)
    draw.text((c2_x + 36, bx_y + 112), "* Unlock Gemini 4 Carbon -> Pause & offer Neon/Hydrogen High", font=get_font("regular", 11), fill=TEXT_MUTED)

    # Col 2 - Box B: Autonomy Mode Dispatcher
    bx_y = col_y + 205
    draw.rounded_rectangle([c2_x + 16, bx_y, c2_x + c2_w - 16, bx_y + 115], radius=8, fill=(18, 26, 40), outline=BORDER_SUBTLE, width=1)
    draw.text((c2_x + 28, bx_y + 12), "Dual Autonomy Operating Modes", font=get_font("bold", 13), fill=TEXT_WHITE)
    draw.text((c2_x + 28, bx_y + 36), "CHECKPOINT MODE (Default Safe)", font=get_font("bold", 12), fill=TEXT_CYAN)
    draw.text((c2_x + 28, bx_y + 54), "Stages Gemini 4 model + Thinking High plan, pauses for approval", font=get_font("regular", 11), fill=TEXT_MUTED)
    draw.text((c2_x + 28, bx_y + 74), "AUTO MODE (Unattended Batch)", font=get_font("bold", 12), fill=TEXT_GREEN)
    draw.text((c2_x + 28, bx_y + 92), "Triggered by 'auto mode' / 'unattended' -- runs full lifecycle", font=get_font("regular", 11), fill=TEXT_MUTED)

    # Col 2 - Box C: Automation Execution Engine
    bx_y = col_y + 335
    draw.rounded_rectangle([c2_x + 16, bx_y, c2_x + c2_w - 16, bx_y + 145], radius=8, fill=(20, 28, 44), outline=(40, 65, 110), width=1)
    draw.text((c2_x + 28, bx_y + 12), "4. Subagent Action & Surface Orchestrator", font=get_font("bold", 14), fill=TEXT_WHITE)
    draw.text((c2_x + 28, bx_y + 36), "- Driver: Built-in Browser Subagent (Model: 'flash')", font=get_font("mono", 11), fill=TEXT_CYAN)
    draw.text((c2_x + 28, bx_y + 58), "- Surfaces: /prompts/new_chat, /new_structured, /prompts, /apikey", font=get_font("mono", 11), fill=TEXT_WHITE)
    draw.text((c2_x + 28, bx_y + 80), "- Thinking Floor: Explicitly sets Thinking level = High", font=get_font("regular", 11), fill=TEXT_GREEN)
    draw.text((c2_x + 28, bx_y + 102), "- Run Settings: Output length (64K/32K), Media res, Stop sequence", font=get_font("regular", 11), fill=TEXT_MUTED)
    draw.text((c2_x + 28, bx_y + 124), "- Tripwires: 429 ResourceExhausted, Paid gate, HARM safety stops", font=get_font("regular", 11), fill=TEXT_AMBER)

    # Col 2 - Box D: Extraction & Code Harvesting
    bx_y = col_y + 495
    draw.rounded_rectangle([c2_x + 16, bx_y, c2_x + c2_w - 16, bx_y + 115], radius=8, fill=(20, 28, 44), outline=BORDER_ACTIVE, width=1)
    draw.text((c2_x + 28, bx_y + 12), "5. Extraction & Code Harvesting", font=get_font("bold", 14), fill=TEXT_CYAN)
    draw.text((c2_x + 28, bx_y + 36), "- Triggers 'Get code' dialog in Google AI Studio", font=get_font("regular", 11), fill=TEXT_WHITE)
    draw.text((c2_x + 28, bx_y + 56), "- Exports Python, TypeScript, cURL, or REST (thinking_level=high)", font=get_font("regular", 11), fill=TEXT_MUTED)
    draw.text((c2_x + 28, bx_y + 76), "- Downloads Structured outputs schemas & tabular CSV evaluations", font=get_font("regular", 11), fill=TEXT_MUTED)
    draw.text((c2_x + 28, bx_y + 96), "- Staged to browser_sandbox/downloads/ for local ingestion", font=get_font("semibold", 11), fill=TEXT_GREEN)

    # Column 3: GOOGLE AI STUDIO (CLOUD FRONTIER NEXUS - GEMINI 4)
    c3_x, c3_w = 1240, 620
    draw.rounded_rectangle([c3_x, col_y, c3_x + c3_w, col_y + col_h], radius=14, fill=CARD_BG, outline=BORDER_SUBTLE, width=1)
    draw.rounded_rectangle([c3_x, col_y, c3_x + c3_w, col_y + 45], radius=14, fill=CARD_BG_ALT)
    draw.rectangle([c3_x, col_y + 30, c3_x + c3_w, col_y + 45], fill=CARD_BG_ALT)
    draw.text((c3_x + 20, col_y + 12), "GOOGLE AI STUDIO (Gemini 4 Cloud Nexus)", font=get_font("bold", 16), fill=TEXT_PURPLE)
    draw.text((c3_x + c3_w - 150, col_y + 14), "CLOUD ENGINE", font=get_font("mono_bold", 11), fill=TEXT_DIM)

    # Col 3 - Box A: Gemini 4 Model Ensemble (4 cards)
    bx_y = col_y + 56
    draw.rounded_rectangle([c3_x + 16, bx_y, c3_x + c3_w - 16, bx_y + 224], radius=8, fill=(28, 22, 42), outline=(75, 45, 110), width=1)
    draw.text((c3_x + 28, bx_y + 10), "Authorized Gemini 4 Roster (1M Context | Thinking High+)", font=get_font("bold", 13), fill=TEXT_PURPLE)

    models = [
        ("Gemini 4 Hydrogen", "1M in / 64K out | Free & Paid Default", "Routine logs (4K-1M), JSON schemas, batch data, prompt iteration", ACCENT_CYAN),
        ("Gemini 4 Argon", "1M in / 32K out | Switch Med -> High", "Complex logic debugging, fine-grained engineering & problem solving", ACCENT_BLUE),
        ("Gemini 4 Neon", "1M in / 64K out | Pro/Paid Flagship", "Repo-scale architecture, complex SWE, deep multimodal & 64K output", TEXT_PURPLE),
        ("Gemini 4 Carbon", "1M in / 32K out | Paid Gate + High", "Extreme long-horizon reasoning, hardest math/science (fallback if gated)", TEXT_AMBER),
    ]
    for m_idx, (m_name, m_meta, m_desc, m_col) in enumerate(models):
        my_card = bx_y + 34 + m_idx * 46
        draw.rounded_rectangle([c3_x + 26, my_card, c3_x + c3_w - 26, my_card + 40], radius=6, fill=(35, 28, 55))
        draw.text((c3_x + 36, my_card + 5), m_name, font=get_font("bold", 12), fill=TEXT_WHITE)
        draw.text((c3_x + 185, my_card + 6), m_meta, font=get_font("mono_bold", 10), fill=m_col)
        draw.text((c3_x + 36, my_card + 22), m_desc, font=get_font("regular", 10), fill=TEXT_MUTED)

    # Col 3 - Box B: Gemini 4 Run Settings & Tools
    bx_y = col_y + 292
    draw.rounded_rectangle([c3_x + 16, bx_y, c3_x + c3_w - 16, bx_y + 172], radius=8, fill=(22, 28, 44), outline=BORDER_SUBTLE, width=1)
    draw.text((c3_x + 28, bx_y + 10), "Gemini 4 Run Settings & Native Tools Panel", font=get_font("bold", 14), fill=TEXT_WHITE)
    draw.text((c3_x + 28, bx_y + 34), "- Thinking level: High (Web UI) / high, xhigh (API); Low/Med banned", font=get_font("regular", 11), fill=TEXT_GREEN)
    draw.text((c3_x + 28, bx_y + 56), "- Run settings: Output length (65536/32768), Media resolution, Stop seq", font=get_font("regular", 11), fill=TEXT_CYAN)
    draw.text((c3_x + 28, bx_y + 78), "- URL context: Reads full webpage body directly inside chat/API", font=get_font("regular", 11), fill=TEXT_WHITE)
    draw.text((c3_x + 28, bx_y + 100), "- Grounding with Google Search: Default ON (disables Func calling)", font=get_font("regular", 11), fill=TEXT_AMBER)
    draw.text((c3_x + 28, bx_y + 122), "- Structured outputs & Code execution: Chat + /new_structured JSON", font=get_font("regular", 11), fill=TEXT_WHITE)
    draw.text((c3_x + 28, bx_y + 144), "- Safety settings: 4 harm categories (legacy Temp/Top-P/K removed)", font=get_font("regular", 11), fill=TEXT_MUTED)

    # Col 3 - Box C: Production SDK Code Export Formats
    bx_y = col_y + 476
    draw.rounded_rectangle([c3_x + 16, bx_y, c3_x + c3_w - 16, bx_y + 140], radius=8, fill=(24, 30, 48), outline=(60, 80, 120), width=1)
    draw.text((c3_x + 28, bx_y + 10), "Production SDK Code Export Formats", font=get_font("bold", 14), fill=TEXT_WHITE)
    draw.text((c3_x + 28, bx_y + 34), "* Python SDK (google-genai) + ThinkingConfig(thinking_level='high')", font=get_font("mono_bold", 11), fill=TEXT_CYAN)
    draw.text((c3_x + 28, bx_y + 56), "* TypeScript / JS SDK (@google/genai) + thinkingConfig HIGH/XHIGH", font=get_font("mono_bold", 11), fill=TEXT_WHITE)
    draw.text((c3_x + 28, bx_y + 78), "* cURL & REST (models/gemini-4-hydrogen:generateContent)", font=get_font("mono_bold", 11), fill=TEXT_GREEN)
    draw.text((c3_x + 28, bx_y + 100), "* Structured JSON Schema Export + GEMINI_API_KEY env guard", font=get_font("mono_bold", 11), fill=TEXT_PURPLE)
    draw.text((c3_x + 28, bx_y + 120), "Pre-Gemini-4 models (PaLM 2, 1.x, 2.x, 3.x) strictly pruned", font=get_font("regular", 10), fill=TEXT_AMBER)

    # 4. Connecting Flow Arrows between Columns
    draw.line([(c1_x + c1_w, col_y + 125), (c2_x, col_y + 125)], fill=BORDER_ACTIVE, width=3)
    draw.polygon([(c2_x, col_y + 125), (c2_x - 10, col_y + 120), (c2_x - 10, col_y + 130)], fill=BORDER_ACTIVE)

    draw.line([(c2_x + c2_w, col_y + 125), (c3_x, col_y + 125)], fill=BORDER_PURPLE, width=3)
    draw.polygon([(c3_x, col_y + 125), (c3_x - 10, col_y + 120), (c3_x - 10, col_y + 130)], fill=BORDER_PURPLE)

    draw.line([(c3_x, col_y + 550), (c2_x + c2_w, col_y + 550)], fill=BORDER_CYAN, width=3)
    draw.polygon([(c2_x + c2_w, col_y + 550), (c2_x + c2_w + 10, col_y + 545), (c2_x + c2_w + 10, col_y + 555)], fill=BORDER_CYAN)

    draw.line([(c2_x, col_y + 550), (c1_x + c1_w, col_y + 550)], fill=BORDER_CYAN, width=3)
    draw.polygon([(c1_x + c1_w, col_y + 550), (c1_x + c1_w + 10, col_y + 545), (c1_x + c1_w + 10, col_y + 555)], fill=BORDER_CYAN)

    # 5. Bottom Lifecycle Stage Tracker (6-Stage Banner)
    bot_y = 930
    bot_h = 135
    draw.rounded_rectangle([60, bot_y, 1860, bot_y + bot_h], radius=12, fill=CARD_BG, outline=BORDER_SUBTLE, width=1)
    draw.text((80, bot_y + 14), "END-TO-END 6-STAGE GEMINI 4 CLOUD OFFLOAD LIFECYCLE", font=get_font("bold", 14), fill=TEXT_WHITE)
    draw.text((545, bot_y + 16), "Enforced Thinking High+, Paid-Gate Fallback, 7-Bit ASCII Compliance, Full E2E Verification", font=get_font("regular", 12), fill=TEXT_MUTED)

    stages = [
        ("[1] EVALUATE", "Select Gemini 4 model via matrix", ACCENT_BLUE),
        ("[2] STAGE", "Copy files to browser_sandbox/uploads/", ACCENT_CYAN),
        ("[3] DISPATCH", "Browser subagent opens aistudio.google.com", ACCENT_PURPLE),
        ("[4] EXECUTE", "1M context + Thinking level = High", ACCENT_AMBER),
        ("[5] EXTRACT", "Retrieve code, JSON schemas & outputs", ACCENT_GREEN),
        ("[6] SYNC", "Merge workspace files & run 5-tier tests", ACCENT_CYAN),
    ]

    sw = 280
    for idx, (st_title, st_desc, st_col) in enumerate(stages):
        sx = 80 + idx * 295
        sy = bot_y + 44
        draw.rounded_rectangle([sx, sy, sx + sw, sy + 75], radius=8, fill=(21, 30, 48), outline=st_col, width=1)
        draw.text((sx + 14, sy + 10), st_title, font=get_font("bold", 13), fill=st_col)
        draw.text((sx + 14, sy + 32), st_desc, font=get_font("regular", 10), fill=TEXT_WHITE)
        draw.text((sx + 14, sy + 50), "Step %d / 6" % (idx + 1), font=get_font("mono_bold", 10), fill=TEXT_MUTED)

    out_path = os.path.join(ASSETS_DIR, "architecture-offload-pipeline.png")
    img.save(out_path, "PNG", optimize=True)
    print("Generated:", out_path)


# ==============================================================================
# INFOGRAPHIC 2: MODULAR SKILLS ECOSYSTEM (v0.2.0 Pure Gemini 4)
# ==============================================================================
def generate_skills_ecosystem_infographic():
    width, height = 1920, 1100
    img = Image.new("RGB", (width, height), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_grid_background(draw, width, height, step=40)

    # 1. Header Section
    tag_font = get_font("mono_bold", 12)
    title_font = get_font("bold", 34)
    subtitle_font = get_font("regular", 16)

    bx = 60
    w1, _ = draw_badge(draw, bx, 35, "MODULAR ARCHITECTURE v0.2.0", tag_font, (20, 30, 45), ACCENT_BLUE, TEXT_CYAN)
    bx += w1 + 14
    w2, _ = draw_badge(draw, bx, 35, "6 GEMINI 4 SKILLS", tag_font, (35, 25, 45), ACCENT_PURPLE, TEXT_PURPLE)
    bx += w2 + 14
    w3, _ = draw_badge(draw, bx, 35, "THINKING FLOOR HIGH+", tag_font, (15, 35, 25), ACCENT_GREEN, TEXT_GREEN)

    draw.text((60, 75), "Antigravity AI Studio Modular Skills Ecosystem", font=title_font, fill=TEXT_WHITE)
    draw.text((60, 122), "Six specialized skills engineered for Google AI Studio Gemini 4 (1M Context, Thinking High+, URL Context, Structured Outputs)", font=subtitle_font, fill=TEXT_MUTED)

    # 2. Top Summary Pill Bar
    my = 158
    pw = 585
    ph = 56
    draw.rounded_rectangle([60, my, 60 + pw, my + ph], radius=8, fill=CARD_BG, outline=BORDER_SUBTLE, width=1)
    draw.text((78, my + 10), "ORCHESTRATION & CHAT PROMPTS", font=get_font("bold", 12), fill=TEXT_CYAN)
    draw.text((78, my + 28), "aistudio-offload  |  aistudio-chat-prompt", font=get_font("mono", 11), fill=TEXT_MUTED)

    draw.rounded_rectangle([665, my, 665 + pw, my + ph], radius=8, fill=CARD_BG, outline=BORDER_SUBTLE, width=1)
    draw.text((683, my + 10), "STRUCTURED OUTPUTS & RUN SETTINGS", font=get_font("bold", 12), fill=TEXT_PURPLE)
    draw.text((683, my + 28), "aistudio-structured-prompt  |  aistudio-parameter-tuning", font=get_font("mono", 11), fill=TEXT_MUTED)

    draw.rounded_rectangle([1270, my, 1270 + pw, my + ph], radius=8, fill=CARD_BG, outline=BORDER_SUBTLE, width=1)
    draw.text((1288, my + 10), "CODE EXPORT & DRIFT RECON", font=get_font("bold", 12), fill=TEXT_GREEN)
    draw.text((1288, my + 28), "aistudio-code-export  |  aistudio-ui-sync-audit", font=get_font("mono", 11), fill=TEXT_MUTED)

    # 3. 2x3 Skill Cards Grid
    grid_y = 235
    card_w = 585
    card_h = 390
    gap_x = 20
    gap_y = 20

    skills_data = [
        {
            "col": 0, "row": 0,
            "id": "aistudio-offload",
            "badge": "MASTER ORCHESTRATOR",
            "badge_col": ACCENT_CYAN,
            "target": "https://aistudio.google.com/",
            "desc": "Master coordinator routing tasks across Gemini 4 models (Hydrogen, Argon, Neon, Carbon) with Thinking High+ and paid-gate fallback.",
            "features": [
                "Gemini 4 Decision Matrix (Local vs 1M Cloud Offload)",
                "Fast-Path Auth Check (< 1.5s via recent session state)",
                "Dual Autonomy Modes: Checkpoint Mode & Full-Auto Mode",
                "Unlock Gemini 4 Carbon gate detection & Neon/Hydrogen fallback",
            ],
            "trigger": '"Offload 500k-token repo review to Gemini 4 Neon (High)"',
            "border": BORDER_CYAN
        },
        {
            "col": 1, "row": 0,
            "id": "aistudio-chat-prompt",
            "badge": "SYSTEM & MULTI-TURN",
            "badge_col": ACCENT_BLUE,
            "target": "https://aistudio.google.com/prompts/new_chat",
            "desc": "Orchestrates multi-turn chat sessions on Gemini 4 with persistent system instructions, 1M token gauge monitoring, and URL context.",
            "features": [
                "Dedicated System Instructions tuning & persona setup",
                "Enforces Thinking level = High (Argon/Carbon Med -> High)",
                "Multi-file uploads via setInputFiles + Media resolution",
                "Markdown transcript export to browser_sandbox/downloads/",
            ],
            "trigger": '"Run multi-turn architecture chat on Gemini 4 Argon (High)"',
            "border": ACCENT_BLUE
        },
        {
            "col": 2, "row": 0,
            "id": "aistudio-structured-prompt",
            "badge": "SCHEMA & FEW-SHOT",
            "badge_col": ACCENT_PURPLE,
            "target": "https://aistudio.google.com/prompts/new_structured",
            "desc": "Builds tabular few-shot examples and enforces strict JSON Schema via Structured outputs in /prompts/new_structured or chat.",
            "features": [
                "Tabular Few-Shot Editor with multi-column mapping",
                "Structured outputs JSON Schema constrained decoding",
                "Batch test case evaluation on Gemini 4 Hydrogen (High)",
                "CSV batch import/export synced to local workspace",
            ],
            "trigger": '"Build structured prompt with JSON schema on Gemini 4 Hydrogen"',
            "border": ACCENT_PURPLE
        },
        {
            "col": 0, "row": 1,
            "id": "aistudio-parameter-tuning",
            "badge": "RUN SETTINGS & TOOLS",
            "badge_col": ACCENT_AMBER,
            "target": "Studio Run settings & Tools Sidebar",
            "desc": "Calibrates Gemini 4 Run settings (Thinking level High+, Output length, Media resolution, Stop seq) and native Tools panel.",
            "features": [
                "Thinking level floor High+ (Low & Medium forbidden)",
                "Output length (65536/32768), Media resolution & Stop sequence",
                "URL context, Google Search Grounding (default ON) & Code exec",
                "Function calling auto-disable guard + 4-category Safety",
            ],
            "trigger": '"Set Gemini 4 Neon Thinking High, 64K output & URL context"',
            "border": ACCENT_AMBER
        },
        {
            "col": 1, "row": 1,
            "id": "aistudio-code-export",
            "badge": "PRODUCTION SDK EXPORT",
            "badge_col": ACCENT_GREEN,
            "target": "Studio 'Get code' Modal Dialog",
            "desc": "Harvests production-ready client integration code from Gemini 4 prompts across Python, TypeScript, cURL, and REST formats.",
            "features": [
                "Python SDK (google-genai) with thinking_level='high'/'xhigh'",
                "TypeScript SDK (@google/genai) & cURL/REST payload export",
                "Automated GEMINI_API_KEY placeholder protection",
                "Rejects pre-Gemini-4 model IDs before workspace sync",
            ],
            "trigger": '"Export Gemini 4 prompt as Python SDK script with thinking high"',
            "border": ACCENT_GREEN
        },
        {
            "col": 2, "row": 1,
            "id": "aistudio-ui-sync-audit",
            "badge": "UI RECON & DRIFT AUDIT",
            "badge_col": ACCENT_RED,
            "target": "7 Canonical AI Studio Surfaces",
            "desc": "Strictly read-only visual audit scanning AI Studio DOM to track Gemini 4 models, Run settings drift, and obsolete model pruning.",
            "features": [
                "Read-only DOM drift inspection across 7 canonical surfaces",
                "Safety-enforced read-only (disable-model-invocation: true)",
                "Verifies Gemini 4 roster & prunes pre-Gemini-4 models",
                "Updates audit-checklist.md calibration date (2026-11-22)",
            ],
            "trigger": '"Run UI sync audit to verify Gemini 4 models & Run settings"',
            "border": ACCENT_RED
        },
    ]

    for s in skills_data:
        cx = 60 + s["col"] * (card_w + gap_x)
        cy = grid_y + s["row"] * (card_h + gap_y)

        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=12, fill=CARD_BG, outline=BORDER_SUBTLE, width=1)

        draw.rounded_rectangle([cx, cy, cx + card_w, cy + 44], radius=12, fill=CARD_BG_ALT)
        draw.rectangle([cx, cy + 30, cx + card_w, cy + 44], fill=CARD_BG_ALT)

        draw.text((cx + 18, cy + 12), s["id"], font=get_font("bold", 15), fill=TEXT_WHITE)
        draw_pill(draw, cx + card_w - 14, cy + 10, s["badge"], get_font("mono_bold", 10), (30, 40, 60), s["badge_col"])

        draw.text((cx + 18, cy + 54), "TARGET: " + s["target"], font=get_font("mono", 10), fill=TEXT_DIM)

        wrapped_desc = textwrap.wrap(s["desc"], width=78)
        for d_idx, line in enumerate(wrapped_desc[:2]):
            draw.text((cx + 18, cy + 76 + d_idx * 18), line, font=get_font("regular", 11), fill=TEXT_MUTED)

        fb_y = cy + 125
        draw.rounded_rectangle([cx + 14, fb_y, cx + card_w - 14, fb_y + 160], radius=8, fill=(19, 27, 42), outline=s["border"], width=1)
        draw.text((cx + 26, fb_y + 10), "KEY CAPABILITIES & HIGHLIGHTS", font=get_font("mono_bold", 10), fill=s["badge_col"])

        for f_idx, feat in enumerate(s["features"]):
            draw.text((cx + 26, fb_y + 32 + f_idx * 26), "[+] " + feat, font=get_font("regular", 11), fill=TEXT_WHITE)

        tb_y = cy + 300
        draw.rounded_rectangle([cx + 14, tb_y, cx + card_w - 14, tb_y + 70], radius=8, fill=(16, 22, 35))
        draw.text((cx + 24, tb_y + 10), "SAMPLE PROMPT / TRIGGER:", font=get_font("mono_bold", 10), fill=TEXT_AMBER)
        draw.text((cx + 24, tb_y + 32), s["trigger"], font=get_font("mono", 11), fill=TEXT_CYAN)

    # 4. Bottom Assurance Strip
    bot_y = 1040
    draw.rounded_rectangle([60, bot_y, 1860, bot_y + 40], radius=8, fill=CARD_BG, outline=BORDER_SUBTLE, width=1)
    draw.text((80, bot_y + 12), "VERIFICATION GUARANTEE:", font=get_font("mono_bold", 11), fill=ACCENT_GREEN)
    draw.text((285, bot_y + 12), "All 6 Skills Verified by 5-Tier E2E Suite", font=get_font("semibold", 11), fill=TEXT_WHITE)
    draw.text((680, bot_y + 12), "* Pure Gemini 4", font=get_font("regular", 11), fill=TEXT_MUTED)
    draw.text((820, bot_y + 12), "* Thinking Floor High+", font=get_font("regular", 11), fill=TEXT_GREEN)
    draw.text((1030, bot_y + 12), "* 100% 7-Bit ASCII Compliant", font=get_font("regular", 11), fill=TEXT_CYAN)
    draw.text((1300, bot_y + 12), "* Apache-2.0 License", font=get_font("regular", 11), fill=TEXT_MUTED)
    draw.text((1510, bot_y + 12), "* Antigravity Plugin v0.2.0", font=get_font("regular", 11), fill=TEXT_PURPLE)

    out_path = os.path.join(ASSETS_DIR, "modular-skills-ecosystem.png")
    img.save(out_path, "PNG", optimize=True)
    print("Generated:", out_path)


if __name__ == "__main__":
    generate_architecture_pipeline_infographic()
    generate_skills_ecosystem_infographic()
    print("All infographics generated successfully.")
