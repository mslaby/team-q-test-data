"""
json_to_pdf.py

A simple command-line tool to convert a JSON file to a formatted PDF.

Usage:
    python json_to_pdf.py input.json output.pdf

Dependencies:
    pip install reportlab
"""

import argparse
import json
import os
import sys

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Preformatted
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def json_to_pdf(input_file: str, output_file: str, page_size: str = "A4") -> None:
    """
    Reads a JSON file and writes its pretty-printed contents into a PDF.

    :param input_file: Path to the input JSON file.
    :param output_file: Path for the generated PDF file.
    :param page_size: The page size for the PDF ('A4' or 'LETTER').
    """
    # Choose page size
    if page_size.upper() == "LETTER":
        pagesize = letter
    else:
        pagesize = A4

    # Register a font
    pdfmetrics.registerFont(TTFont("DejaVuSans", "./fonts/dejavu-sans/DejaVuSans.ttf"))

    # Load JSON data
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON - {e}")
        sys.exit(1)

    # Pretty-print JSON
    pretty_json = json.dumps(data, indent=4, ensure_ascii=False)

    # Prepare PDF document
    doc = SimpleDocTemplate(
        output_file,
        pagesize=pagesize,
        title=os.path.basename(output_file),
        author="json_to_pdf script",
    )

    styles = getSampleStyleSheet()
    style = styles["Code"] if "Code" in styles else styles["Normal"]
    style.fontName = "DejaVuSans"
    style.fontSize = 8
    style.leading = 10

    # Create flowable
    flowables = []
    flowables.append(Preformatted(pretty_json, style))

    # Build PDF
    try:
        doc.build(flowables)
        print(f"Success: PDF generated at '{output_file}'")
    except Exception as e:
        print(f"Error: Failed to build PDF - {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a JSON file into a formatted PDF document."
    )
    parser.add_argument("input", help="Path to the input JSON file")
    parser.add_argument("output", help="Path to the output PDF file")
    parser.add_argument(
        "--page-size",
        choices=["A4", "LETTER"],
        default="A4",
        help="Page size for the PDF (default: A4)",
    )

    args = parser.parse_args()
    json_to_pdf(args.input, args.output, args.page_size)
