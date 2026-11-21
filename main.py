import argparse
import sys

import config
import label_doc
import reader


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Avery 61523 asset tag labels as a Word document"
    )
    parser.add_argument("--input", required=True, help="CSV or JSON file of asset records")
    parser.add_argument("--output", default="output/labels.docx", help="Output .docx path")
    parser.add_argument(
        "--default-label",
        default=config.DEFAULT_LABEL_TEXT,
        help="Header text used when a record has no 'label' field",
    )
    args = parser.parse_args()

    try:
        records = reader.load(args.input, args.default_label)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not records:
        print("No records found in input file.", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(records)} record(s) from {args.input}")
    label_doc.build(records, args.output)
    print(f"Labels written to {args.output}")


if __name__ == "__main__":
    main()
