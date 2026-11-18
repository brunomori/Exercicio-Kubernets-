#!/usr/bin/env python3
"""Validate relative Markdown links in the repository root README."""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

root = Path(__file__).resolve().parents[1]
readme = root / "README.md"
missing = []
for target in re.findall(r"\]\(([^)]+)\)", readme.read_text(encoding="utf-8")):
    parsed = urlsplit(target.strip())
    if parsed.scheme or parsed.netloc or not parsed.path:
        continue
    path = root / unquote(parsed.path)
    if not path.exists():
        missing.append(target)
if missing:
    raise SystemExit("Broken relative README links:\n" + "\n".join(missing))
print("Relative README links: OK")
