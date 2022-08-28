#!/usr/bin/env python3
"""Convert Markdown files to styled PDF documents."""

import argparse
import sys
from pathlib import Path
import markdown
from weasyprint import HTML, CSS

DEFAULT_CSS = """
@page {
    size: A4;
    margin: 2cm;
}
body {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 12pt;
    line-height: 1.6;
    color: #333;
    max-width: 100%;
}
h1 {
    color: #2c3e50;
    border-bottom: 2px solid #3498db;
    padding-bottom: 10px;
    font-size: 24pt;
}
h2 {
    color: #2c3e50;
    border-bottom: 1px solid #bdc3c7;
    padding-bottom: 5px;
    font-size: 18pt;
}
h3 { color: #34495e; font-size: 14pt; }
code {
    background-color: #f8f9fa;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
    font-size: 10pt;
}
pre {
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 5px;
    border-left: 4px solid #3498db;
    overflow-x: auto;
}
pre code {
    background: none;
    padding: 0;
}
blockquote {
    border-left: 4px solid #3498db;
    margin: 1em 0;
    padding: 0.5em 1em;
    background-color: #f0f7fd;
    color: #555;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}
th, td {
    border: 1px solid #ddd;
    padding: 8px 12px;
    text-align: left;
}
th {
    background-color: #3498db;
    color: white;
}
tr:nth-child(even) { background-color: #f2f2f2; }
a { color: #3498db; text-decoration: none; }
hr { border: none; border-top: 2px solid #eee; margin: 2em 0; }
img { max-width: 100%; height: auto; }
ul, ol { padding-left: 2em; }
"""

DARK_CSS = """
@page {
    size: A4;
    margin: 2cm;
    background-color: #1a1a2e;
}
body {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 12pt;
    line-height: 1.6;
    color: #e0e0e0;
    background-color: #1a1a2e;
}
h1 { color: #00d2ff; border-bottom: 2px solid #00d2ff; padding-bottom: 10px; }
h2 { color: #00d2ff; border-bottom: 1px solid #444; padding-bottom: 5px; }
h3 { color: #7fdbff; }
code {
    background-color: #16213e;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
    color: #00d2ff;
}
pre {
    background-color: #16213e;
    padding: 15px;
    border-radius: 5px;
    border-left: 4px solid #00d2ff;
}
pre code { background: none; color: #e0e0e0; }
blockquote {
    border-left: 4px solid #00d2ff;
    padding: 0.5em 1em;
    background-color: #16213e;
    color: #aaa;
}
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #333; padding: 8px 12px; }
th { background-color: #0f3460; color: #00d2ff; }
tr:nth-child(even) { background-color: #16213e; }
a { color: #00d2ff; }
hr { border-top: 2px solid #333; }
"""


def convert_md_to_pdf(input_path: Path, output_path: Path, theme: str = "light"):
    md_content = input_path.read_text(encoding="utf-8")

    extensions = [
        "tables",
        "fenced_code",
        "codehilite",
        "toc",
        "nl2br",
        "sane_lists",
    ]
    html_body = markdown.markdown(md_content, extensions=extensions)

    html_full = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>{html_body}</body>
</html>"""

    css = DARK_CSS if theme == "dark" else DEFAULT_CSS

    HTML(string=html_full).write_pdf(
        str(output_path),
        stylesheets=[CSS(string=css)],
    )
    print(f"  Converted: {input_path.name} -> {output_path.name}")


def main():
    parser = argparse.ArgumentParser(description="Convert Markdown files to styled PDFs")
    parser.add_argument("input", nargs="+", help="Markdown file(s) to convert")
    parser.add_argument("-o", "--output", help="Output PDF path (single file only)")
    parser.add_argument("-t", "--theme", choices=["light", "dark"], default="light", help="PDF theme")
    parser.add_argument("--output-dir", help="Output directory for batch conversion")
    args = parser.parse_args()

    if args.output and len(args.input) > 1:
        print("Error: --output can only be used with a single input file.")
        sys.exit(1)

    output_dir = Path(args.output_dir) if args.output_dir else None
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    for input_file in args.input:
        input_path = Path(input_file)
        if not input_path.exists():
            print(f"  Skipping: '{input_file}' not found.")
            continue
        if not input_path.suffix.lower() in (".md", ".markdown"):
            print(f"  Skipping: '{input_file}' is not a Markdown file.")
            continue

        if args.output:
            output_path = Path(args.output)
        elif output_dir:
            output_path = output_dir / f"{input_path.stem}.pdf"
        else:
            output_path = input_path.with_suffix(".pdf")

        convert_md_to_pdf(input_path, output_path, theme=args.theme)

    print("\nDone!")


if __name__ == "__main__":
    main()
