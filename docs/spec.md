# Asset Label Generator — Specification

## Overview

A Python CLI tool that reads a CSV or JSON file of computer asset records and produces a Word document (`.docx`) pre-formatted for **Avery 61523** metallic asset tag labels. Each label displays an organization header, serial number text, and a scannable Code 39 barcode.

---

## Label Template — Avery 61528

| Property | Value |
|---|---|
| Part number | 61528 |
| Material | PermaTrack Metallic Silver |
| Label size | 1-1/4" (H) × 2-3/4" (W) |
| Labels per sheet | 14 (2 columns × 7 rows) |
| Sheet size | 8.5" × 11" |
| Top margin | ~0.50" |
| Left margin | ~1.25" |
| Horizontal gap between labels | ~0.50" |
| Vertical gap between labels | 0" |

Avery template reference: `61528`  
**Note**: Verify margins with a plain-paper test print before using metallic stock.

---

## Label Content

Each label contains three elements stacked vertically:

```
┌──────────────────────────┐
│   Property of HRA        │  bold, ~6pt, centered
│   Serial Number: 9VJ4R93 │  regular, ~5pt, centered
│   ▌▌▌▌▌ barcode ▌▌▌▌▌   │  Code 39 barcode image, centered
│       *9VJ4R93*          │  barcode caption, ~4pt, centered
└──────────────────────────┘
```

- **Header line** — configurable per-record or via global default (e.g. `"Property of HRA"`)
- **Serial number line** — prefixed with `"Serial Number: "`
- **Barcode** — Code 39 symbology; sized to ~1.3" × 0.35" to leave room for text lines
- **Barcode caption** — the serial number surrounded by Code 39 start/stop asterisks (`*9VJ4R93*`), displayed below the bars

---

## Input Format

### CSV (preferred for bulk entry — opens in Excel)

```csv
serial_number,label
9VJ4R93,Property of HRA
8XK2M11,Property of HRA
```

- `serial_number` — required; alphanumeric, no spaces
- `label` — optional; falls back to `DEFAULT_LABEL` in `config.py`

### JSON (alternative)

```json
[
  {"serial_number": "9VJ4R93", "label": "Property of HRA"},
  {"serial_number": "8XK2M11"}
]
```

---

## Output

A single `.docx` file containing one or more pages of a 4-column × 10-row table.

- Each table cell = one label
- Cells contain the header text, serial number text, and an embedded barcode PNG
- Unfilled cells on the last page are left blank to preserve the grid layout
- Cell dimensions and padding match the Avery 61523 physical layout for direct printing

---

## Phases

### Phase 1 — Core MVP
- `config.py` — template dimensions, font sizes, default label text
- `reader.py` — load CSV or JSON → `list[dict]`
- `barcode_gen.py` — generate Code 39 barcode PNG for a serial number string
- `label_doc.py` — build `.docx` from list of label dicts using `python-docx`
- `main.py` — CLI entry point wiring everything together

### Phase 2 — Polish & Validation
- Input validation: flag duplicate serials, invalid characters for Code 39
- Dry-run mode (`--preview`) that prints a summary without writing the file
- Support for a second optional field (e.g. `asset_tag` or `location`) on a third text line

### Phase 3 — Optional Enhancements
- QR code variant (for phones without barcode scanners)
- PDF output option via `reportlab`
- GUI wrapper or web form for one-off label generation

---

## CLI Usage

```bash
uv run main.py --input data/assets.csv --output output/labels.docx
uv run main.py --input data/assets.json --output output/labels.docx
uv run main.py --input data/assets.csv --output output/labels.docx --default-label "Property of HRA"
```

---

## Python Dependencies

| Package | Purpose |
|---|---|
| `python-docx` | Build the `.docx` table layout |
| `python-barcode` | Generate Code 39 barcode as PNG |
| `Pillow` | Resize/convert barcode image for embedding |

---

## Project Structure

```
labels/
├── main.py               # CLI entry point
├── config.py             # Avery 61523 dimensions, font sizes, defaults
├── reader.py             # CSV/JSON → list[dict]
├── barcode_gen.py        # Code 39 barcode PNG generator
├── label_doc.py          # .docx builder
├── data/
│   └── assets.csv        # Sample input
├── output/               # Generated .docx files (gitignored)
├── docs/
│   └── spec.md           # This file
├── AGENTS.md             # Agent/branch workflow guide
├── pyproject.toml
└── README.md
```

---

## Printing Notes

- Print test on plain paper first; hold up to the label sheet to verify alignment before printing on metallic stock
- Set printer to "actual size" / no scaling
- The Word table borders should be turned off before printing
