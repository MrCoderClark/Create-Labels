import csv
import json
from pathlib import Path

import config


def load(path: str | Path, default_label: str = config.DEFAULT_LABEL_TEXT) -> list[dict]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {p}")
    records = _from_json(p) if p.suffix.lower() == ".json" else _from_csv(p)
    for r in records:
        r.setdefault("label", default_label)
    return records


def _from_csv(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _from_json(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)
