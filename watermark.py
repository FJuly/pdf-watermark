#!/usr/bin/env python3
"""PDF Watermark Tool - Add text watermarks to PDF documents.

Usage:
    # Preset mode (recommended)
    python watermark.py -i input.pdf -o output.pdf -t "机密文件" --preset dense

    # Custom parameters
    python watermark.py -i input.pdf -o output.pdf -t "Draft" --font-size 10 --opacity 0.15 --cols 8 --rows 10

    # Preview mode (first page only, outputs PNG)
    python watermark.py -i input.pdf -t "样例" --preset dense --preview preview.png
"""

import argparse
import fitz
import math
import sys
import os

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

COLORS = {
    "gray": (0.5, 0.5, 0.5),
    "black": (0, 0, 0),
    "blue": (0.2, 0.4, 0.8),
    "red": (0.8, 0.2, 0.2),
}


def add_watermark(input_pdf, output_pdf, text, params):
    """Add watermark to all pages of a PDF."""
    doc = fitz.open(input_pdf)

    rad = math.radians(params["rotation"])
    rot_mat = fitz.Matrix(
        math.cos(rad),
        math.sin(rad),
        -math.sin(rad),
        math.cos(rad),
        0,
        0,
    )

    color = COLORS.get(params.get("color", "gray"), COLORS["gray"])
    stagger = params.get("stagger", True)

    for page in doc:
        pw = page.rect.width
        ph = page.rect.height

        x_step = pw / (params["cols"] + 1)
        y_step = ph / (params["rows"] + 1)

        for row in range(params["rows"]):
            for col in range(params["cols"]):
                x = x_step * (col + 1)
                y = y_step * (row + 1)

                if row % 2 == 1 and stagger:
                    x += x_step * 0.5

                shape = page.new_shape()
                pt = fitz.Point(x, y)
                shape.insert_text(
                    pt,
                    text,
                    fontsize=params["font_size"],
                    fontname="china-ss",
                    color=color,
                    morph=(pt, rot_mat),
                    fill_opacity=params["opacity"],
                )
                shape.commit()

    page_count = len(doc)
    doc.save(output_pdf)
    doc.close()

    total_watermarks = params["cols"] * params["rows"] * page_count
    print(f"Saved: {output_pdf}")
    print(f"Pages: {page_count}")
    print(f"Watermarks per page: {params['cols'] * params['rows']}")
    print(f"Total watermarks: ~{total_watermarks}")


def generate_preview(input_pdf, text, params, output_png):
    """Generate a preview image (first page only) with watermark."""
    doc = fitz.open(input_pdf)
    page = doc[0]

    rad = math.radians(params["rotation"])
    rot_mat = fitz.Matrix(
        math.cos(rad),
        math.sin(rad),
        -math.sin(rad),
        math.cos(rad),
        0,
        0,
    )

    color = COLORS.get(params.get("color", "gray"), COLORS["gray"])
    stagger = params.get("stagger", True)

    pw = page.rect.width
    ph = page.rect.height

    x_step = pw / (params["cols"] + 1)
    y_step = ph / (params["rows"] + 1)

    for row in range(params["rows"]):
        for col in range(params["cols"]):
            x = x_step * (col + 1)
            y = y_step * (row + 1)

            if row % 2 == 1 and stagger:
                x += x_step * 0.5

            shape = page.new_shape()
            pt = fitz.Point(x, y)
            shape.insert_text(
                pt,
                text,
                fontsize=params["font_size"],
                fontname="china-ss",
                color=color,
                morph=(pt, rot_mat),
                fill_opacity=params["opacity"],
            )
            shape.commit()

    pix = page.get_pixmap(dpi=150)
    pix.save(output_png)
    doc.close()

    print(f"Preview saved: {output_png}")


def check_pymupdf():
    """Check if PyMuPDF is installed."""
    try:
        import fitz
        print(f"PyMuPDF version: {fitz.__doc__.split()[0]}")
        return True
    except ImportError:
        print("Error: PyMuPDF not installed.")
        print("Install with: pip install pymupdf")
        return False


def build_params(args):
    """Build parameter dict from CLI arguments."""
    if args.preset:
        params = PRESETS[args.preset].copy()
    else:
        params = PRESETS["dense"].copy()

    if args.font_size is not None:
        params["font_size"] = args.font_size
    if args.opacity is not None:
        params["opacity"] = args.opacity
    if args.cols is not None:
        params["cols"] = args.cols
    if args.rows is not None:
        params["rows"] = args.rows
    if args.rotation is not None:
        params["rotation"] = args.rotation
    if args.color:
        params["color"] = args.color
    if args.no_stagger:
        params["stagger"] = False

    return params


def main():
    parser = argparse.ArgumentParser(
        description="Add text watermarks to PDF documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Presets:
  dense     12pt / 20% opacity / 6x8 grid  (recommended for confidential docs)
  light     16pt / 10% opacity / 3x4 grid  (subtle, for formal contracts)
  standard  14pt / 15% opacity / 4x6 grid  (balanced, general use)
  bold      18pt / 30% opacity / 2x3 grid  (highly visible, for drafts)

Examples:
  python watermark.py -i doc.pdf -o out.pdf -t "机密文件" --preset dense
  python watermark.py -i doc.pdf -o out.pdf -t "Draft" --font-size 10 --opacity 0.1
  python watermark.py -i doc.pdf -t "Preview" --preset dense --preview preview.png
        """,
    )

    parser.add_argument("--input", "-i", required=True, help="Input PDF file")
    parser.add_argument("--output", "-o", help="Output PDF file (required unless --preview)")
    parser.add_argument("--text", "-t", required=True, help="Watermark text")
    parser.add_argument(
        "--preset", "-p", choices=PRESETS.keys(), help="Use a preset configuration"
    )
    parser.add_argument("--font-size", type=int, help="Font size in points")
    parser.add_argument("--opacity", type=float, help="Opacity (0.0-1.0)")
    parser.add_argument("--cols", type=int, help="Grid columns")
    parser.add_argument("--rows", type=int, help="Grid rows")
    parser.add_argument("--rotation", type=int, help="Rotation angle in degrees")
    parser.add_argument("--color", choices=list(COLORS.keys()), help="Text color")
    parser.add_argument("--no-stagger", action="store_true", help="Disable staggered layout")
    parser.add_argument("--preview", metavar="PNG", help="Preview mode: generate PNG of first page only")
    parser.add_argument("--check", action="store_true", help="Check PyMuPDF installation and exit")

    args = parser.parse_args()

    if args.check:
        sys.exit(0 if check_pymupdf() else 1)

    if not args.input or not args.text:
        print("Error: --input and --text are required")
        sys.exit(1)

    if not check_pymupdf():
        sys.exit(1)

    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    params = build_params(args)

    if args.preview:
        generate_preview(args.input, args.text, params, args.preview)
    else:
        if not args.output:
            print("Error: --output required (or use --preview)")
            sys.exit(1)
        add_watermark(args.input, args.output, args.text, params)


if __name__ == "__main__":
    main()
