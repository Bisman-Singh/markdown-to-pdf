# Markdown to PDF Converter

Convert Markdown files into beautifully styled PDF documents with light and dark themes.

## Features

- Light and dark theme support
- Styled tables, code blocks, blockquotes
- Batch conversion (multiple files at once)
- Custom output directory
- Supports fenced code, tables, TOC, and more via Markdown extensions

## Usage

```bash
pip install -r requirements.txt

# Convert a single file
python main.py document.md

# Convert with dark theme
python main.py document.md --theme dark

# Custom output path
python main.py document.md -o output.pdf

# Batch convert
python main.py *.md --output-dir pdfs/
```

## Note

WeasyPrint requires system dependencies. On macOS: `brew install pango`. On Ubuntu: `apt install libpango-1.0-0 libpangoft2-1.0-0`.

<sub><sup>Originally developed and tested locally during learning. Later organized and pushed to GitHub for portfolio visibility.</sup></sub>
