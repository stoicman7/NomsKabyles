from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "index.html"
html = path.read_text(encoding="utf-8")

required = [
    "ISMWAEN_KABYLE_LAYOUT_V2",
    'id="search-meta"',
    "Dictionnaire des noms kabyles",
    "--lime:#FCD116;",
]
if all(marker in html for marker in required) and "ⴰⵣⵓⵍ" not in html and "ⵜⴰⵎⴰⵣⵉⵖⵜ" not in html:
    print("Ismwaen blue-first layout and Kabyle motif register already applied")
    raise SystemExit(0)

raise SystemExit("index.html does not match the current Ismwaen layout; review it before applying the theme.")
