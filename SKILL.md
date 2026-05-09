---
name: pdf-watermark
description: "Add text watermarks to PDF documents with visual preset selection and custom parameter control"
version: "1.0"
author: claude-office-skills
license: MIT
category: pdf
tags:
  - pdf
  - watermark
  - annotation
  - editing
department: All
models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o
---

# PDF Watermark Skill

## Overview

Add text watermarks to PDF documents. This skill uses a pre-built Python script (`watermark.py`) for reliable execution.

**Pre-built Scripts**:
- `watermark.py` — Core watermark engine (CLI tool)
- `check_env.py` — Environment checker

**Core Library**: PyMuPDF (pymupdf)

**Key Capabilities**:
- Chinese and English text support (built-in CJK fonts)
- Adjustable transparency (10% - 50%)
- Grid-based density control (sparse to dense)
- Arbitrary rotation angles
- Staggered grid layout for better coverage
- Per-page automatic adaptation

## How to Use

### Mode A: Preset Selection (Recommended)

**Step 1**: Provide watermark text

```
User: Add watermark to my PDF
Skill: What text do you want in the watermark?
User: Internal Document
```

**Step 2**: Skill generates 4 preview images with user's text

**MUST**: Run the pre-built script in preview mode for each preset:

```bash
# Generate preview for each preset
python3 watermark.py -i assets/demo_page.pdf -t "用户文字" --preset dense --preview /tmp/preview_dense.png
python3 watermark.py -i assets/demo_page.pdf -t "用户文字" --preset light --preview /tmp/preview_light.png
python3 watermark.py -i assets/demo_page.pdf -t "用户文字" --preset standard --preview /tmp/preview_standard.png
python3 watermark.py -i assets/demo_page.pdf -t "用户文字" --preset bold --preview /tmp/preview_bold.png
```

**MUST**: Present the presets in this order (best first):

| Preset | Style | Use Case | Parameters |
|:---|:---|:---|:---|
| **1** | **⭐ Dense Protection (Recommended)** | **Confidential files, anti-leak** | **12pt / 20% opacity / 6x8 grid** |
| 2 | Light & Sparse | Formal contracts, external docs | 16pt / 10% opacity / 3x4 grid |
| 3 | Balanced Standard | General office documents | 14pt / 15% opacity / 4x6 grid |
| 4 | Bold Notice | Drafts, internal circulation | 18pt / 30% opacity / 2x3 grid |

**MUST**: Highlight preset #1 as the recommended choice for most documents.

**Step 3**: Use `question` tool for selection

**MUST**: Present the 4 preview images and use the `question` tool with multiple choice options. Do NOT ask user to type numbers.

Example:
```
Skill: [Shows 4 preview images]
       Please select a watermark style:
       
       1. ⭐ Dense Protection (Recommended) - Best for confidential docs
       2. Light & Sparse - Subtle, for formal contracts
       3. Balanced Standard - Medium visibility
       4. Bold Notice - Highly visible, for drafts
```

**Step 4**: Apply selected preset

After user selects a preset, run the script with the chosen parameters:

```bash
python3 watermark.py -i input.pdf -o output_watermarked.pdf -t "用户文字" --preset dense
```

### Mode B: Custom Parameters

Access by saying "custom" or directly specifying parameters.

**Direct CLI usage**:
```bash
python3 watermark.py -i input.pdf -o output.pdf -t "水印文字" \
  --font-size 10 --opacity 0.15 --cols 8 --rows 10 --rotation 45
```

| Parameter | CLI Flag | Default | Range |
|:---|:---|:---|:---|
| `text` | `-t, --text` | required | Any text, supports Chinese |
| `font_size` | `--font-size` | 12 | 8 - 36 (pt) |
| `opacity` | `--opacity` | 0.20 | 0.05 - 0.50 |
| `cols` | `--cols` | 6 | 2 - 12 |
| `rows` | `--rows` | 8 | 2 - 16 |
| `rotation` | `--rotation` | 45 | 0 - 360 (degrees) |
| `color` | `--color` | gray | gray/black/blue/red |
| `stagger` | `--no-stagger` | enabled | disable with flag |

## Environment Setup

### Check Environment

Run the environment checker before first use:

```bash
python3 check_env.py
```

Output if ready:
```
Python: Python 3.13.5
Path: /usr/bin/python3
PyMuPDF: PyMuPDF 1.27.2
Environment is ready!
```

### Install Python (if missing)

| Platform | Command |
|:---|:---|
| macOS | `brew install python3` |
| Ubuntu/Debian | `sudo apt update && sudo apt install python3 python3-pip` |
| Fedora | `sudo dnf install python3 python3-pip` |
| Windows | Download from [python.org](https://python.org) |

**Recommended**: Use `uv` (does not require pre-installed Python):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.12
```

### Install PyMuPDF

```bash
python3 -m pip install pymupdf
```

If installation fails, install system dependencies first:

| Platform | Dependencies |
|:---|:---|
| macOS | `brew install mupdf swig freetype` |
| Ubuntu/Debian | `sudo apt install libfreetype6-dev` |
| Windows | Install [VC++ Redistributable](https://learn.microsoft.com/cpp/windows/latest-supported-vc-redist) |

Then retry: `python3 -m pip install pymupdf`

## Troubleshooting

| Error | Cause | Fix |
|:---|:---|:---|
| `PyMuPDF not installed` | Missing package | `python3 -m pip install pymupdf` |
| `'fitz.h' file not found` | Missing MuPDF headers (macOS/Linux) | Install system deps (see above), then retry |
| `ImportError: DLL load failed` | Missing VC++ runtime (Windows) | Install VC++ Redistributable |
| `GLIBC_2.33 not found` | Linux distro too old | Upgrade OS, or build from source with `--no-build-isolation` |
| `fontname 'china-ss' not found` | PyMuPDF version too old | `pip install --upgrade pymupdf` |

## Preset Definitions

**Preset order: Best first (dense is recommended for most use cases)**

```python
PRESETS = {
    "dense": {
        "font_size": 12,
        "opacity": 0.20,
        "cols": 6,
        "rows": 8,
        "rotation": 45,
        "color": "gray",
        "stagger": True,
    },
    "light": {
        "font_size": 16,
        "opacity": 0.10,
        "cols": 3,
        "rows": 4,
        "rotation": 45,
        "color": "gray",
        "stagger": True,
    },
    "standard": {
        "font_size": 14,
        "opacity": 0.15,
        "cols": 4,
        "rows": 6,
        "rotation": 45,
        "color": "gray",
        "stagger": True,
    },
    "bold": {
        "font_size": 18,
        "opacity": 0.30,
        "cols": 2,
        "rows": 3,
        "rotation": 30,
        "color": "gray",
        "stagger": True,
    },
}
```

## Interaction Flow

```
[Trigger] "Add watermark" / "pdf-watermark"
    |
    v
[Step 0] Check environment
    | Run: python3 check_env.py
    | If missing → guide installation
    v
[Step 1] Ask for watermark text
    | (supports Chinese, English, numbers)
    v
[Step 2] Generate 4 preview images
    | Run watermark.py --preview for each preset
    | (using assets/demo_page.pdf as background)
    v
[Step 3] Present options using question tool
    | MUST: use question tool with multiple choice
    | MUST: preset #1 dense is first and highlighted
    |                                    |
    | User selects preset                | User says "custom"
    v                                    v
[Step 4a] Run watermark.py      [Step 4b] Collect custom params
    | with selected preset               |
    | -i input -o output                 v
    |                                    [Step 5] Run watermark.py
    v                                    with custom args
[Step 6] Confirm and deliver                                   
    | output PDF
    v
[Done]
```

## Best Practices

1. **Text Length**: Keep watermark text under 10 characters for optimal visual density. Longer text automatically reduces font size.

2. **Opacity Guidelines**:
   - 10% - 15%: Barely visible, suitable for formal documents
   - 20%: Balanced visibility without obstructing content (recommended)
   - 30%+: Very visible, for drafts and notices only

3. **Density Guidelines**:
   - Sparse (3x4): ~12 watermarks per page
   - Standard (4x6): ~24 watermarks per page
   - Dense (6x8): ~48 watermarks per page
   - Very Dense (8x10+): Consider reducing opacity to avoid clutter

4. **Rotation**: 45° is standard for diagonal watermarks. 0° for horizontal, 90° for vertical.

5. **Font Size vs Grid**: Smaller fonts work better with denser grids. Large fonts (18pt+) should use sparse grids to avoid overlap.

## Boundary Handling

| Scenario | Response |
|:---|:---|
| Empty text input | Prompt "Please enter watermark text" |
| Text > 20 characters | Auto-scale font size down, warn user |
| Special characters | Filter or escape non-printable chars |
| "Same as last time" / "一样" | Reuse context from previous session |
| Scanned/image PDF | Works normally (watermark overlays on top) |
| Batch multiple PDFs | Loop with same parameters |
| "Cancel" / "算了" at any step | Exit without saving |
| "Preview first page only" | Process page 1, show PNG, wait for confirmation |
| Environment check fails | Show installation guide from Environment Setup |

## Examples

### Example 1: Quick Preset Application

```
User: Add watermark to report.pdf
Skill: What text for the watermark?
User: Internal Only
Skill: [Runs 4 preview generations...]
       [Shows 4 previews via question tool]
User: [Selects "Dense Protection (Recommended)"]
Skill: [Runs: python3 watermark.py -i report.pdf -o report_watermarked.pdf -t "Internal Only" --preset dense]
       Done. report_watermarked.pdf (48 watermarks per page)
```

### Example 2: Custom Parameters

```bash
python3 watermark.py -i doc.pdf -o out.pdf -t "Draft v2" \
  --font-size 10 --opacity 0.25 --cols 8 --rows 10
```

### Example 3: Preview Only

```bash
python3 watermark.py -i doc.pdf -t "Preview" --preset dense --preview preview.png
```

### Example 4: Context Reuse

```
User: Add watermark to another PDF
Skill: Reusing last config: "Internal Only" + Dense preset
       Target file?
User: summary.pdf
Skill: [Runs watermark.py with cached params]
       Done. summary_watermarked.pdf
```

## Asset Files

| File | Purpose |
|:---|:---|
| `SKILL.md` | This documentation |
| `watermark.py` | Core watermark engine (CLI script) |
| `check_env.py` | Environment checker |
| `assets/demo_page.pdf` | Template for preview generation |
| `assets/sample_dense.png` | Preset 1 visual reference (recommended) |
| `assets/sample_light.png` | Preset 2 visual reference |
| `assets/sample_standard.png` | Preset 3 visual reference |
| `assets/sample_bold.png` | Preset 4 visual reference |

## Dependencies

- Python >= 3.8
- PyMuPDF >= 1.23.0 (`pip install pymupdf`)

## Notes

- Watermarks are added as vector text (not images), keeping output PDF size minimal
- Watermarks appear on all pages by default
- Each page adapts to its own dimensions (supports mixed page sizes)
- Output filename: `{original}_watermarked.pdf`
