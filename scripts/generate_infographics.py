"""
generate_infographics.py
Renders two ultra-high-density technical infographics for the antigravity-aistudio project:
1. assets/architecture-offload-pipeline.png (1920x1100)
2. assets/modular-skills-ecosystem.png (1920x1100)
Uses Pillow with Segoe UI and Consolas fonts.
"""

import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Font loading helpers
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

def draw_pill(draw, x, y, text, font, bg_color, text_color):
    bbox = font.getbbox(text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 10, 4
    w, h = tw + pad_x * 2, th + pad_y * 2
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=bg_color)
    draw.text((x + pad_x, y + pad_y - bbox[1]), text, font=font, fill=text_color)
    return w, h

def draw_stat_card(draw, x, y, w, h, stat_num, stat_label, subtext, accent_color):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD_BG, outline=BORDER_SUBTLE, width=1)
    # top accent line
    draw.rounded_rectangle([x + 12, y, x + w - 12, y + 3], radius=2, fill=accent_color)
    
    font_num = get_font("bold", 28)
    font_label = get_font("semibold", 14)
    font_sub = get_font("regular", 12)
    
    draw.text((x + 18, y + 16), stat_num, font=font_num, fill=accent_color)
    draw.text((x + 18, y + 54), stat_label, font=font_label, fill=TEXT_WHITE)
    draw.text((x + 18, y + 74), subtext, font=font_sub, fill=TEXT_MUTED)

# ==============================================================================
# INFOGRAPHIC 1: ARCHITECTURE & OFFLOAD PIPELINE
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
    
    # Header badges
    bx = 60
    w1, _ = draw_badge(draw, bx, 35, "ANTIGRAVITY PLUGIN v0.1.0", tag_font, (20, 30, 45), ACCENT_BLUE, TEXT_CYAN)
    bx += w1 + 14
    w2, _ = draw_badge(draw, bx, 35, "CLOUD AGENT OFFLOADING", tag_font, (35, 25, 45), ACCENT_PURPLE, TEXT_PURPLE)
    bx += w2 + 14
    w3, _ = draw_badge(draw, bx, 35, "ZERO LOCAL QUOTA BURN", tag_font, (15, 35, 25), ACCENT_GREEN, TEXT_GREEN)
    
    draw.text((60, 75), "Cloud Agent Offloading Architecture & Execution Pipeline", font=title_font, fill=TEXT_WHITE)
    draw.text((60, 122), "Seamless bridge between Antigravity Local Workspace and Google AI Studio Frontier Models (Gemini 2.5 Pro / Flash / Thinking)", font=subtitle_font, fill=TEXT_MUTED)
    
    # 2. Top Metric Cards (Row of 4)
    my = 160
    cw = 425
    ch = 100
    draw_stat_card(draw, 60, my, cw, ch, "2,000,000 Tokens", "Maximum Frontier Context", "Gemini 2.5 Pro deep document ingestion", ACCENT_CYAN)
    draw_stat_card(draw, 515, my, cw, ch, "0 Tokens Burned", "Desktop IDE Quota Shield", "Preserves local Gemini & Claude quotas", ACCENT_GREEN)
    draw_stat_card(draw, 970, my, cw, ch, "Zero Daemons", "Native Browser Subagent", "No Playwright/Selenium servers needed", ACCENT_BLUE)
    draw_stat_card(draw, 1425, my, cw, ch, "251 / 251 Tests Pass", "5-Tier Hardened QA Suite", "Unit, boundary, cross-feature & adversarial", ACCENT_PURPLE)
    
    # 3. Main Architecture Diagram: 3 High-Density Columns
    col_y = 280
    col_h = 630
    
    # Column 1: LOCAL WORKSPACE (Antigravity IDE)
    c1_x, c1_w = 60, 560
    draw.rounded_rectangle([c1_x, col_y, c1_x + c1_w, col_y + col_h], radius=14, fill=CARD_BG, outline=BORDER_SUBTLE, width=1)
    # Header banner for Col 1
    draw.rounded_rectangle([c1_x, col_y, c1_x + c1_w, col_y + 45], radius=14, fill=CARD_BG_ALT)
    draw.rectangle([c1_x, col_y + 30, c1_x + c1_w, col_y + 45], fill=CARD_BG_ALT)
    draw.text((c1_x + 20, col_y + 12), "LOCAL WORKSPACE (Antigravity IDE)", font=get_font("bold", 16), fill=TEXT_CYAN)
    draw.text((c1_x + c1_w - 170, col_y + 14), "LOCAL BOUNDARY", font=get_font("mono_bold", 11), fill=TEXT_DIM)
    
    # Col 1 - Box A: Developer Request & Decision Engine
    bx_y = col_y + 60
    draw.rounded_rectangle([c1_x + 16, bx_y, c1_x + c1_w - 16, bx_y + 130], radius=8, fill=(20, 28, 44), outline=(45, 60, 85), width=1)
    draw.text((c1_x + 28, bx_y + 12), "1. Developer Task & Workload Classifier", font=get_font("bold", 14), fill=TEXT_WHITE)
    draw.text((c1_x + 28, bx_y + 36), "Input: Natural language user prompt or automated trigger", font=get_font("regular", 12), fill=TEXT_MUTED)
    draw.text((c1_x + 28, bx_y + 56), "Evaluator: rules/AGENTS.md (12-category workload matrix)", font=get_font("mono", 11), fill=TEXT_CYAN)
    draw.text((c1_x + 28, bx_y + 80), "Split Decision: Local Execution vs Cloud Offload Candidate", font=get_font("semibold", 12), fill=TEXT_AMBER)
    draw.text((c1_x + 28, bx_y + 102), "[+] Checks token budget, model capacity, reasoning depth", font=get_font("regular", 11), fill=TEXT_MUTED)
    
    # Col 1 - Box B: Local Retained Operations (No Offload)
    bx_y = col_y + 205
    draw.rounded_rectangle([c1_x + 16, bx_y, c1_x + c1_w - 16, bx_y + 115], radius=8, fill=(16, 24, 38), outline=BORDER_SUBTLE, width=1)
    draw.text((c1_x + 28, bx_y + 12), "Local Execution Paths (Retained Locally)", font=get_font("bold", 13), fill=TEXT_MUTED)
    draw.text((c1_x + 28, bx_y + 34), "* File Edits: apply_edits, write_file (< 50 lines / surgical refactoring)", font=get_font("regular", 11), fill=TEXT_DIM)
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
    draw.text((c1_x + 28, bx_y + 126), "Strict Single-Segment naming rule + Sandbox boundary enforcement", font=get_font("regular", 11), fill=TEXT_AMBER)
    
    # Col 1 - Box D: Local Synchronization & Validation
    bx_y = col_y + 495
    draw.rounded_rectangle([c1_x + 16, bx_y, c1_x + c1_w - 16, bx_y + 115], radius=8, fill=(18, 30, 42), outline=BORDER_CYAN, width=1)
    draw.text((c1_x + 28, bx_y + 12), "6. Local Workspace Synchronization", font=get_font("bold", 14), fill=TEXT_GREEN)
    draw.text((c1_x + 28, bx_y + 36), "- Copies downloaded code/artifacts to target workspace files", font=get_font("regular", 11), fill=TEXT_WHITE)
    draw.text((c1_x + 28, bx_y + 56), "- Validates JSON Schema conformance and strips secret keys", font=get_font("regular", 11), fill=TEXT_MUTED)
    draw.text((c1_x + 28, bx_y + 76), "- Runs local automated regression suite (251/251 tests passing)", font=get_font("regular", 11), fill=TEXT_CYAN)
    draw.text((c1_x + 28, bx_y + 96), "- Reports outcome to user with zero local model quota wasted", font=get_font("semibold", 11), fill=TEXT_GREEN)
    
    # Column 2: BROWSER SUBAGENT AUTOMATION BRIDGE
    c2_x, c2_w = 645, 570
    draw.rounded_rectangle([c2_x, col_y, c2_x + c2_w, col_y + col_h], radius=14, fill=CARD_BG, outline=BORDER_SUBTLE, width=1)
    draw.rounded_rectangle([c2_x, col_y, c2_x + c2_w, col_y + 45], radius=14, fill=CARD_BG_ALT)
    draw.rectangle([c2_x, col_y + 30, c2_x + c2_w, col_y + 45], fill=CARD_BG_ALT)
    draw.text((c2_x + 20, col_y + 12), "BROWSER SUBAGENT BRIDGE (Zero-Daemon)", font=get_font("bold", 16), fill=ACCENT_BLUE)
    draw.text((c2_x + c2_w - 175, col_y + 14), "ISOLATED AGENT", font=get_font("mono_bold", 11), fill=TEXT_DIM)
    
    # Col 2 - Box A: Fast-Path Authentication & Safety Gate
    bx_y = col_y + 60
    draw.rounded_rectangle([c2_x + 16, bx_y, c2_x + c2_w - 16, bx_y + 130], radius=8, fill=(20, 28, 44), outline=(40, 65, 110), width=1)
    draw.text((c2_x + 28, bx_y + 12), "3. Fast-Path Auth & Security Guard", font=get_font("bold", 14), fill=TEXT_WHITE)
    draw.text((c2_x + 28, bx_y + 36), "- Reuses active Google AI Studio web session (Zero credentials read)", font=get_font("regular", 12), fill=TEXT_CYAN)
    draw.text((c2_x + 28, bx_y + 58), "- Fast probe via Avatar / Prompts RPC signals (< 1.5s latency)", font=get_font("regular", 11), fill=TEXT_MUTED)
    draw.text((c2_x + 28, bx_y + 80), "Safety Stops (Fail Loudly):", font=get_font("semibold", 11), fill=TEXT_AMBER)
    draw.text((c2_x + 38, bx_y + 98), "* LOGIN_REQUIRED -> Pauses & invites user to sign in", font=get_font("regular", 11), fill=TEXT_MUTED)
    draw.text((c2_x + 38, bx_y + 114), "* CAPTCHA / Bot Gate -> Hands control directly to user (No bypass)", font=get_font("regular", 11), fill=TEXT_MUTED)
    
    # Col 2 - Box B: Autonomy Mode Dispatcher
    bx_y = col_y + 205
    draw.rounded_rectangle([c2_x + 16, bx_y, c2_x + c2_w - 16, bx_y + 115], radius=8, fill=(18, 26, 40), outline=BORDER_SUBTLE, width=1)
    draw.text((c2_x + 28, bx_y + 12), "Dual Autonomy Operating Modes", font=get_font("bold", 13), fill=TEXT_WHITE)
    draw.text((c2_x + 28, bx_y + 36), "CHECKPOINT MODE (Default Safe)", font=get_font("bold", 12), fill=TEXT_CYAN)
    draw.text((c2_x + 28, bx_y + 54), "Stages prompts & parameters, pauses for developer confirmation before run", font=get_font("regular", 11), fill=TEXT_MUTED)
    draw.text((c2_x + 28, bx_y + 74), "AUTO MODE (Unattended Batch)", font=get_font("bold", 12), fill=TEXT_GREEN)
    draw.text((c2_x + 28, bx_y + 92), "Triggered by 'auto mode' / 'unattended' -- runs full lifecycle automatically", font=get_font("regular", 11), fill=TEXT_MUTED)
    
    # Col 2 - Box C: Automation Execution Engine
    bx_y = col_y + 335
    draw.rounded_rectangle([c2_x + 16, bx_y, c2_x + c2_w - 16, bx_y + 145], radius=8, fill=(20, 28, 44), outline=(40, 65, 110), width=1)
    draw.text((c2_x + 28, bx_y + 12), "4. Subagent Action & Surface Orchestrator", font=get_font("bold", 14), fill=TEXT_WHITE)
    draw.text((c2_x + 28, bx_y + 36), "- Model: Built-in Browser Subagent (Model: 'flash')", font=get_font("mono", 11), fill=TEXT_CYAN)
    draw.text((c2_x + 28, bx_y + 58), "- Surface Routing: /prompts/new_chat, /new_structured, /tune", font=get_font("mono", 11), fill=TEXT_WHITE)
    draw.text((c2_x + 28, bx_y + 80), "- Multi-Modal Injection: Attaches files via setInputFiles", font=get_font("regular", 11), fill=TEXT_MUTED)
    draw.text((c2_x + 28, bx_y + 102), "- Parameter Control: Temperature, Top-P, Thinking Token Budget", font=get_font("regular", 11), fill=TEXT_MUTED)
    draw.text((c2_x + 28, bx_y + 124), "- Error Tripwires: Quota 429 backoff, Safety HARM block catchers", font=get_font("regular", 11), fill=TEXT_AMBER)
    
    # Col 2 - Box D: Extraction & Code Harvesting
    bx_y = col_y + 495
    draw.rounded_rectangle([c2_x + 16, bx_y, c2_x + c2_w - 16, bx_y + 115], radius=8, fill=(20, 28, 44), outline=BORDER_ACTIVE, width=1)
    draw.text((c2_x + 28, bx_y + 12), "5. Extraction & Code Harvesting", font=get_font("bold", 14), fill=TEXT_CYAN)
    draw.text((c2_x + 28, bx_y + 36), "- Triggers 'Get code' dialog in Google AI Studio", font=get_font("regular", 11), fill=TEXT_WHITE)
    draw.text((c2_x + 28, bx_y + 56), "- Exports Python SDK, TypeScript, cURL, or raw response text", font=get_font("regular", 11), fill=TEXT_MUTED)
    draw.text((c2_x + 28, bx_y + 76), "- Downloads JSON schema definitions & tabular few-shot tables", font=get_font("regular", 11), fill=TEXT_MUTED)
    draw.text((c2_x + 28, bx_y + 96), "- Staged to browser_sandbox/downloads/ for local ingestion", font=get_font("semibold", 11), fill=TEXT_GREEN)
    
    # Column 3: GOOGLE AI STUDIO (CLOUD FRONTIER NEXUS)
    c3_x, c3_w = 1240, 620
    draw.rounded_rectangle([c3_x, col_y, c3_x + c3_w, col_y + col_h], radius=14, fill=CARD_BG, outline=BORDER_SUBTLE, width=1)
    draw.rounded_rectangle([c3_x, col_y, c3_x + c3_w, col_y + 45], radius=14, fill=CARD_BG_ALT)
    draw.rectangle([c3_x, col_y + 30, c3_x + c3_w, col_y + 45], fill=CARD_BG_ALT)
    draw.text((c3_x + 20, col_y + 12), "GOOGLE AI STUDIO (aistudio.google.com)", font=get_font("bold", 16), fill=TEXT_PURPLE)
    draw.text((c3_x + c3_w - 160, col_y + 14), "CLOUD ENGINE", font=get_font("mono_bold", 11), fill=TEXT_DIM)
    
    # Col 3 - Box A: Frontier Model Ensemble
    bx_y = col_y + 60
    draw.rounded_rectangle([c3_x + 16, bx_y, c3_x + c3_w - 16, bx_y + 185], radius=8, fill=(28, 22, 42), outline=(75, 45, 110), width=1)
    draw.text((c3_x + 28, bx_y + 12), "Frontier Model Capabilities", font=get_font("bold", 14), fill=TEXT_PURPLE)
    
    # Model 1: Gemini 2.5 Pro
    draw.rounded_rectangle([c3_x + 28, bx_y + 36, c3_x + c3_w - 28, bx_y + 76], radius=6, fill=(35, 28, 55))
    draw.text((c3_x + 40, bx_y + 42), "Gemini 2.5 Pro", font=get_font("bold", 13), fill=TEXT_WHITE)
    draw.text((c3_x + 155, bx_y + 43), "2,000,000 Tokens Context", font=get_font("mono_bold", 11), fill=ACCENT_CYAN)
    draw.text((c3_x + 40, bx_y + 58), "Massive repo analysis, whole-codebase AST synthesis, complex multi-document reasoning", font=get_font("regular", 10), fill=TEXT_MUTED)
    
    # Model 2: Gemini 2.5 Flash
    draw.rounded_rectangle([c3_x + 28, bx_y + 84, c3_x + c3_w - 28, bx_y + 124], radius=6, fill=(35, 28, 55))
    draw.text((c3_x + 40, bx_y + 90), "Gemini 2.5 Flash", font=get_font("bold", 13), fill=TEXT_WHITE)
    draw.text((c3_x + 165, bx_y + 91), "Sub-second Latency", font=get_font("mono_bold", 11), fill=TEXT_AMBER)
    draw.text((c3_x + 40, bx_y + 106), "High-speed structured output, batch synthetic data, quick schema transformation", font=get_font("regular", 10), fill=TEXT_MUTED)
    
    # Model 3: Gemini Flash Thinking
    draw.rounded_rectangle([c3_x + 28, bx_y + 132, c3_x + c3_w - 28, bx_y + 172], radius=6, fill=(35, 28, 55))
    draw.text((c3_x + 40, bx_y + 138), "Gemini Flash Thinking", font=get_font("bold", 13), fill=TEXT_WHITE)
    draw.text((c3_x + 205, bx_y + 139), "Extended Thinking Budget", font=get_font("mono_bold", 11), fill=TEXT_GREEN)
    draw.text((c3_x + 40, bx_y + 154), "Mathematical proofs, algorithmic problem-solving, architectural tradeoff analysis", font=get_font("regular", 10), fill=TEXT_MUTED)
    
    # Col 3 - Box B: Native Studio Tools & Capabilities
    bx_y = col_y + 260
    draw.rounded_rectangle([c3_x + 16, bx_y, c3_x + c3_w - 16, bx_y + 170], radius=8, fill=(22, 28, 44), outline=BORDER_SUBTLE, width=1)
    draw.text((c3_x + 28, bx_y + 12), "Google AI Studio Native Tooling", font=get_font("bold", 14), fill=TEXT_WHITE)
    draw.text((c3_x + 28, bx_y + 36), "- System Instructions Tuning: Dedicated system prompt canvas", font=get_font("regular", 11), fill=TEXT_CYAN)
    draw.text((c3_x + 28, bx_y + 58), "- Tabular Few-Shot Editor: Multi-column input/output test fixtures", font=get_font("regular", 11), fill=TEXT_WHITE)
    draw.text((c3_x + 28, bx_y + 80), "- Strict JSON Schema Mode: Constrained decoding with 0-hallucination", font=get_font("regular", 11), fill=TEXT_GREEN)
    draw.text((c3_x + 28, bx_y + 102), "- Google Search Grounding: Live web query verification & citation", font=get_font("regular", 11), fill=TEXT_AMBER)
    draw.text((c3_x + 28, bx_y + 124), "- Cloud Code Execution: Sandboxed Python runner for algorithmic verify", font=get_font("regular", 11), fill=TEXT_WHITE)
    draw.text((c3_x + 28, bx_y + 146), "- Safety Thresholds: Configurable BLOCK_NONE / BLOCK_LOW per category", font=get_font("regular", 11), fill=TEXT_MUTED)
    
    # Col 3 - Box C: Production SDK Code Export Formats
    bx_y = col_y + 445
    draw.rounded_rectangle([c3_x + 16, bx_y, c3_x + c3_w - 16, bx_y + 165], radius=8, fill=(24, 30, 48), outline=(60, 80, 120), width=1)
    draw.text((c3_x + 28, bx_y + 12), "Production SDK Code Export Formats", font=get_font("bold", 14), fill=TEXT_WHITE)
    draw.text((c3_x + 28, bx_y + 36), "* Python SDK (google-genai / google.generativeai)", font=get_font("mono_bold", 11), fill=TEXT_CYAN)
    draw.text((c3_x + 28, bx_y + 58), "* TypeScript / JavaScript SDK (@google/genai)", font=get_font("mono_bold", 11), fill=TEXT_WHITE)
    draw.text((c3_x + 28, bx_y + 80), "* Raw cURL Command with header auth placeholders", font=get_font("mono_bold", 11), fill=TEXT_AMBER)
    draw.text((c3_x + 28, bx_y + 102), "* REST API Payload (models/gemini-2.5-pro:generateContent)", font=get_font("mono_bold", 11), fill=TEXT_GREEN)
    draw.text((c3_x + 28, bx_y + 124), "* JSON Schema Export for Pydantic / TypeScript validators", font=get_font("mono_bold", 11), fill=TEXT_PURPLE)
    draw.text((c3_x + 28, bx_y + 144), "Exported files staged directly to browser_sandbox/downloads/", font=get_font("regular", 11), fill=TEXT_DIM)
    
    # 4. Connecting Flow Arrows between Columns
    # Local to Bridge
    draw.line([(c1_x + c1_w, col_y + 125), (c2_x, col_y + 125)], fill=BORDER_ACTIVE, width=3)
    draw.polygon([(c2_x, col_y + 125), (c2_x - 10, col_y + 120), (c2_x - 10, col_y + 130)], fill=BORDER_ACTIVE)
    
    # Bridge to Cloud Studio
    draw.line([(c2_x + c2_w, col_y + 125), (c3_x, col_y + 125)], fill=BORDER_PURPLE, width=3)
    draw.polygon([(c3_x, col_y + 125), (c3_x - 10, col_y + 120), (c3_x - 10, col_y + 130)], fill=BORDER_PURPLE)
    
    # Cloud Studio to Bridge (Return)
    draw.line([(c3_x, col_y + 550), (c2_x + c2_w, col_y + 550)], fill=BORDER_CYAN, width=3)
    draw.polygon([(c2_x + c2_w, col_y + 550), (c2_x + c2_w + 10, col_y + 545), (c2_x + c2_w + 10, col_y + 555)], fill=BORDER_CYAN)
    
    # Bridge to Local (Sync)
    draw.line([(c2_x, col_y + 550), (c1_x + c1_w, col_y + 550)], fill=BORDER_CYAN, width=3)
    draw.polygon([(c1_x + c1_w, col_y + 550), (c1_x + c1_w + 10, col_y + 545), (c1_x + c1_w + 10, col_y + 555)], fill=BORDER_CYAN)
    
    # 5. Bottom Lifecycle Stage Tracker (6-Stage Banner)
    bot_y = 930
    bot_h = 135
    draw.rounded_rectangle([60, bot_y, 1860, bot_y + bot_h], radius=12, fill=CARD_BG, outline=BORDER_SUBTLE, width=1)
    draw.text((80, bot_y + 14), "END-TO-END 6-STAGE CLOUD OFFLOAD LIFECYCLE", font=get_font("bold", 14), fill=TEXT_WHITE)
    draw.text((500, bot_y + 16), "Guaranteed Safe Execution, Idempotent File Handoff, Full Verification", font=get_font("regular", 12), fill=TEXT_MUTED)
    
    stages = [
        ("[1] EVALUATE", "Classify task against 12-category matrix", ACCENT_BLUE),
        ("[2] STAGE", "Copy files to browser_sandbox/uploads/", ACCENT_CYAN),
        ("[3] DISPATCH", "Browser subagent opens aistudio.google.com", ACCENT_PURPLE),
        ("[4] EXECUTE", "Cloud model runs with up to 2M context", ACCENT_AMBER),
        ("[5] EXTRACT", "Retrieve code, JSON schemas & prompt responses", ACCENT_GREEN),
        ("[6] SYNC", "Merge artifacts into workspace & run 251 tests", ACCENT_CYAN),
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
# INFOGRAPHIC 2: MODULAR SKILLS ECOSYSTEM
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
    w1, _ = draw_badge(draw, bx, 35, "MODULAR ARCHITECTURE", tag_font, (20, 30, 45), ACCENT_BLUE, TEXT_CYAN)
    bx += w1 + 14
    w2, _ = draw_badge(draw, bx, 35, "6 SPECIALIZED SKILLS", tag_font, (35, 25, 45), ACCENT_PURPLE, TEXT_PURPLE)
    bx += w2 + 14
    w3, _ = draw_badge(draw, bx, 35, "100% SURFACE COVERAGE", tag_font, (15, 35, 25), ACCENT_GREEN, TEXT_GREEN)
    
    draw.text((60, 75), "Antigravity AI Studio Modular Skills Ecosystem", font=title_font, fill=TEXT_WHITE)
    draw.text((60, 122), "Six specialized skills providing seamless, zero-quota interaction with every corner of Google AI Studio", font=subtitle_font, fill=TEXT_MUTED)
    
    # 2. Top Summary Pill Bar
    my = 158
    pw = 585
    ph = 56
    # Pill 1
    draw.rounded_rectangle([60, my, 60 + pw, my + ph], radius=8, fill=CARD_BG, outline=BORDER_SUBTLE, width=1)
    draw.text((78, my + 10), "ORCHESTRATION & PROMPTS", font=get_font("bold", 12), fill=TEXT_CYAN)
    draw.text((78, my + 28), "aistudio-offload  |  aistudio-chat-prompt", font=get_font("mono", 11), fill=TEXT_MUTED)
    
    # Pill 2
    draw.rounded_rectangle([665, my, 665 + pw, my + ph], radius=8, fill=CARD_BG, outline=BORDER_SUBTLE, width=1)
    draw.text((683, my + 10), "STRUCTURED TYPES & TUNING", font=get_font("bold", 12), fill=TEXT_PURPLE)
    draw.text((683, my + 28), "aistudio-structured-prompt  |  aistudio-parameter-tuning", font=get_font("mono", 11), fill=TEXT_MUTED)
    
    # Pill 3
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
            "desc": "Master coordinator evaluating incoming tasks against the 12-category decision matrix, staging files, and synchronizing returned cloud outputs.",
            "features": [
                "12-Category Workload Matrix (Local vs Cloud Partitioning)",
                "Fast-Path Auth Check (< 1.5s via recent session state)",
                "Dual Autonomy Modes: Checkpoint Mode & Full-Auto Mode",
                "Automated Sandbox File Staging & Result Harmonization",
            ],
            "trigger": '"Offload repo architectural review of 500k tokens to Gemini 2.5 Pro"',
            "border": BORDER_CYAN
        },
        {
            "col": 1, "row": 0,
            "id": "aistudio-chat-prompt",
            "badge": "SYSTEM & MULTI-TURN",
            "badge_col": ACCENT_BLUE,
            "target": "https://aistudio.google.com/prompts/new_chat",
            "desc": "Orchestrates multi-turn chat prompts, system instructions, role persona definitions, and multi-file context attachments in AI Studio.",
            "features": [
                "Dedicated System Instructions tuning & optimization",
                "Multi-turn conversation history branching & prompt chaining",
                "Multi-file document attachment via setInputFiles",
                "Thinking token budget configuration for complex reasoning",
            ],
            "trigger": '"Tune system instruction for a technical documentation synthesizer"',
            "border": ACCENT_BLUE
        },
        {
            "col": 2, "row": 0,
            "id": "aistudio-structured-prompt",
            "badge": "SCHEMA & FEW-SHOT",
            "badge_col": ACCENT_PURPLE,
            "target": "https://aistudio.google.com/prompts/new_structured",
            "desc": "Constructs tabular few-shot input/output examples and enforces strict JSON Schema, Pydantic, and TypeScript structured outputs.",
            "features": [
                "Tabular Few-Shot Editor with multi-column mapping",
                "Zero-Hallucination JSON Schema constrained decoding",
                "Synthetic dataset and test fixture generation",
                "Direct schema sync to local pydantic / typescript models",
            ],
            "trigger": '"Build a structured prompt extracting AST symbols with strict JSON schema"',
            "border": ACCENT_PURPLE
        },
        {
            "col": 0, "row": 1,
            "id": "aistudio-parameter-tuning",
            "badge": "HYPERPARAMETERS & SAFETY",
            "badge_col": ACCENT_AMBER,
            "target": "Studio Parameter Sidebar & Tools Panel",
            "desc": "Calibrates model hyperparameters, thinking token budgets, Google Search grounding, code execution, and content safety thresholds.",
            "features": [
                "Dynamic temperature, top-p, and top-k calibration",
                "Extended thinking token budget control (up to 64k)",
                "Google Search Grounding & Code Execution toggles",
                "Granular safety filter threshold adjustments (BLOCK_NONE)",
            ],
            "trigger": '"Calibrate temperature to 0.2 and set thinking budget to 16k for code proofs"',
            "border": ACCENT_AMBER
        },
        {
            "col": 1, "row": 1,
            "id": "aistudio-code-export",
            "badge": "PRODUCTION SDK EXPORT",
            "badge_col": ACCENT_GREEN,
            "target": "Studio 'Get code' Modal Dialog",
            "desc": "Harvests production-ready client integration code from tuned prompts across Python, TypeScript, cURL, and REST API formats.",
            "features": [
                "Clean Python SDK (google-genai / google.generativeai) export",
                "TypeScript SDK integration boilerplate generation",
                "Automated GEMINI_API_KEY placeholder protection",
                "Direct write-back to project client and test scripts",
            ],
            "trigger": '"Export current prompt and schema as production Python SDK client script"',
            "border": ACCENT_GREEN
        },
        {
            "col": 2, "row": 1,
            "id": "aistudio-ui-sync-audit",
            "badge": "UI RECON & DRIFT AUDIT",
            "badge_col": ACCENT_RED,
            "target": "7 Canonical AI Studio Surfaces",
            "desc": "Read-only visual audit scanning AI Studio DOM to detect selector changes, new model capabilities, and deprecated UI features.",
            "features": [
                "Continuous DOM selector drift detection across 7 surfaces",
                "Safety-enforced read-only mode (disable-model-invocation: true)",
                "Checks for new Gemini checkpoint releases & capability flags",
                "Automated Markdown audit checklist generation",
            ],
            "trigger": '"Run UI sync audit to check if new Gemini 2.5 checkpoints are available"',
            "border": ACCENT_RED
        },
    ]
    
    for s in skills_data:
        cx = 60 + s["col"] * (card_w + gap_x)
        cy = grid_y + s["row"] * (card_h + gap_y)
        
        # Draw card container
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=12, fill=CARD_BG, outline=BORDER_SUBTLE, width=1)
        
        # Header banner inside card
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + 44], radius=12, fill=CARD_BG_ALT)
        draw.rectangle([cx, cy + 30, cx + card_w, cy + 44], fill=CARD_BG_ALT)
        
        # Skill ID
        draw.text((cx + 18, cy + 12), s["id"], font=get_font("bold", 15), fill=TEXT_WHITE)
        
        # Badge Pill
        draw_pill(draw, cx + card_w - 200, cy + 10, s["badge"], get_font("mono_bold", 10), (30, 40, 60), s["badge_col"])
        
        # Target URL
        draw.text((cx + 18, cy + 54), "TARGET: " + s["target"], font=get_font("mono", 10), fill=TEXT_DIM)
        
        # Description
        draw.text((cx + 18, cy + 76), s["desc"][:78], font=get_font("regular", 11), fill=TEXT_MUTED)
        draw.text((cx + 18, cy + 94), s["desc"][78:], font=get_font("regular", 11), fill=TEXT_MUTED)
        
        # Features Box
        fb_y = cy + 125
        draw.rounded_rectangle([cx + 14, fb_y, cx + card_w - 14, fb_y + 160], radius=8, fill=(19, 27, 42), outline=s["border"], width=1)
        draw.text((cx + 26, fb_y + 10), "KEY CAPABILITIES & HIGHLIGHTS", font=get_font("mono_bold", 10), fill=s["badge_col"])
        
        for f_idx, feat in enumerate(s["features"]):
            draw.text((cx + 26, fb_y + 32 + f_idx * 24), "[+] " + feat, font=get_font("regular", 11), fill=TEXT_WHITE)
            
        # Sample Trigger
        tb_y = cy + 300
        draw.rounded_rectangle([cx + 14, tb_y, cx + card_w - 14, tb_y + 70], radius=8, fill=(16, 22, 35))
        draw.text((cx + 24, tb_y + 10), "SAMPLE PROMPT / TRIGGER:", font=get_font("mono_bold", 10), fill=TEXT_AMBER)
        draw.text((cx + 24, tb_y + 32), s["trigger"], font=get_font("mono", 11), fill=TEXT_CYAN)
    
    # 4. Bottom Assurance Strip
    bot_y = 1040
    draw.rounded_rectangle([60, bot_y, 1860, bot_y + 40], radius=8, fill=CARD_BG, outline=BORDER_SUBTLE, width=1)
    draw.text((80, bot_y + 12), "VERIFICATION GUARANTEE:", font=get_font("mono_bold", 11), fill=ACCENT_GREEN)
    draw.text((275, bot_y + 12), "All 6 Skills Covered by 251 Automated E2E Tests", font=get_font("semibold", 11), fill=TEXT_WHITE)
    draw.text((680, bot_y + 12), "* Zero Daemons", font=get_font("regular", 11), fill=TEXT_MUTED)
    draw.text((820, bot_y + 12), "* Fast-Path Session Re-use", font=get_font("regular", 11), fill=TEXT_MUTED)
    draw.text((1050, bot_y + 12), "* 100% 7-Bit ASCII Compliant", font=get_font("regular", 11), fill=TEXT_CYAN)
    draw.text((1310, bot_y + 12), "* Apache-2.0 License", font=get_font("regular", 11), fill=TEXT_MUTED)
    draw.text((1520, bot_y + 12), "* Antigravity Plugin Ecosystem", font=get_font("regular", 11), fill=TEXT_PURPLE)
    
    out_path = os.path.join(ASSETS_DIR, "modular-skills-ecosystem.png")
    img.save(out_path, "PNG", optimize=True)
    print("Generated:", out_path)

if __name__ == "__main__":
    generate_architecture_pipeline_infographic()
    generate_skills_ecosystem_infographic()
    print("All infographics generated successfully.")
