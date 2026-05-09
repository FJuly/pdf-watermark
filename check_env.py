#!/usr/bin/env python3
"""Check Python and PyMuPDF installation for pdf-watermark skill."""

import subprocess
import sys
import shutil


def check_python():
    """Check if Python 3 is available."""
    python = shutil.which("python3") or shutil.which("python")
    if not python:
        return None, "Python not found"

    try:
        result = subprocess.run(
            [python, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        version = result.stdout.strip() or result.stderr.strip()
        return python, version
    except Exception as e:
        return python, f"Error checking version: {e}"


def check_pymupdf():
    """Check if PyMuPDF is installed."""
    python = shutil.which("python3") or shutil.which("python")
    if not python:
        return False, "Python not found", None

    try:
        result = subprocess.run(
            [python, "-c", "import fitz; print(fitz.__doc__.split()[0])"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            return True, version, None
        else:
            return False, None, result.stderr.strip()
    except Exception as e:
        return False, None, str(e)


def main():
    print("=" * 50)
    print("PDF Watermark - Environment Check")
    print("=" * 50)

    python_path, python_version = check_python()
    if python_path:
        print(f"Python: {python_version}")
        print(f"Path: {python_path}")
    else:
        print("Python: NOT FOUND")
        print()
        print("To install Python:")
        print("  macOS:   brew install python3")
        print("  Ubuntu:  sudo apt update && sudo apt install python3 python3-pip")
        print("  Windows: Download from https://python.org")
        print("  All:     Use uv - https://astral.sh/uv")
        sys.exit(1)

    print()

    has_pymupdf, pymupdf_version, error = check_pymupdf()
    if has_pymupdf:
        print(f"PyMuPDF: {pymupdf_version}")
        print()
        print("Environment is ready!")
    else:
        print("PyMuPDF: NOT FOUND")
        if error:
            print(f"Error: {error}")
        print()
        print("To install PyMuPDF:")
        print(f"  {python_path} -m pip install pymupdf")
        print()
        print("If installation fails, you may need system dependencies:")
        print("  macOS:   brew install mupdf swig freetype")
        print("  Ubuntu:  sudo apt install libfreetype6-dev")
        print("  Windows: Install VC++ Redistributable from Microsoft")
        sys.exit(1)


if __name__ == "__main__":
    main()
