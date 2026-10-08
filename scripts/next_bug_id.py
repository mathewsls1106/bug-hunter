#!/usr/bin/env python3
"""Calcula el siguiente ID de bug y los nombres de archivo estandarizados.

Uso:
    python next_bug_id.py --dir bug-reports --title "KeyError en parse_order con qty nulo"

Salida (JSON):
    {"id": "BUG-007", "number": 7, "date": "20261008", "slug": "keyerror-en-parse-order-con-qty-nulo",
     "report": "BUG-007_20261008_keyerror-en-parse-order-con-qty-nulo.md",
     "test": "test_bug_007_keyerror_en_parse_order_con_qty_nulo.py"}
"""
import argparse
import json
import re
import unicodedata
from datetime import date
from pathlib import Path

PATTERN = re.compile(r"^BUG-(\d{3,})_")


def slugify(text: str, max_len: int = 40) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return text[:max_len].rstrip("-") or "sin-titulo"


def next_number(directory: Path) -> int:
    numbers = []
    if directory.is_dir():
        for f in directory.iterdir():
            m = PATTERN.match(f.name)
            if m:
                numbers.append(int(m.group(1)))
    return max(numbers, default=0) + 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dir", default="bug-reports", help="Carpeta de reportes")
    parser.add_argument("--title", required=True, help="Título corto del hallazgo")
    args = parser.parse_args()

    number = next_number(Path(args.dir))
    stamp = date.today().strftime("%Y%m%d")
    slug = slugify(args.title)
    bug_id = f"BUG-{number:03d}"
    print(json.dumps({
        "id": bug_id,
        "number": number,
        "date": stamp,
        "slug": slug,
        "report": f"{bug_id}_{stamp}_{slug}.md",
        "test": f"test_bug_{number:03d}_{slug.replace('-', '_')}.py",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
