# labels

Python CLI tool that generates **Avery 61523** metallic asset tag labels as a printable Word document.

Reads a CSV or JSON file of computer serial numbers and produces a `.docx` with Code 39 barcodes, formatted to print directly on Avery 61523 label sheets (40 labels per sheet, 3/4" × 1-1/2").

## Usage

```bash
uv run main.py --input data/assets.csv --output output/labels.docx
```

## See Also

- [Specification](docs/spec.md)
- [Agent & Branch Guide](AGENTS.md)
