from pathlib import Path
import json
import fitz

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "extracted"
OUT.mkdir(exist_ok=True)

sources = [
    ("at weghlis.pdf", "at_weghlis.txt"),
    ("at yeemel.pdf", "at_yeemel.txt"),
]

report = []
for source_name, output_name in sources:
    source_path = ROOT / source_name
    if not source_path.exists():
        raise FileNotFoundError(source_path)

    document = fitz.open(source_path)
    sections = []
    pages_with_text = 0
    total_chars = 0
    page_stats = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text", sort=True).strip()
        char_count = len(text)
        total_chars += char_count
        if text:
            pages_with_text += 1
        page_stats.append({"page": page_number, "characters": char_count})
        sections.append(
            f"\n\n===== PAGE {page_number} =====\n\n{text}"
        )

    output_path = OUT / output_name
    output_path.write_text("".join(sections).lstrip(), encoding="utf-8")

    report.append({
        "source": source_name,
        "output": output_name,
        "pages": len(document),
        "pages_with_text": pages_with_text,
        "total_characters": total_chars,
        "likely_scanned": pages_with_text == 0,
        "page_stats": page_stats,
    })
    document.close()

(OUT / "extraction-report.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(json.dumps(report, ensure_ascii=False, indent=2))
