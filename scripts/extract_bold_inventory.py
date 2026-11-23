from pathlib import Path
from collections import Counter
import json
import fitz

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "extracted" / "layout"
OUT.mkdir(parents=True, exist_ok=True)

SOURCES = [
    ("at weghlis.pdf", "at_weghlis"),
    ("at yeemel.pdf", "at_yeemel"),
]

def is_bold(span):
    font = str(span.get("font", ""))
    flags = int(span.get("flags", 0))
    return bool(flags & 16) or any(k in font.lower() for k in ("bold", "black", "heavy", "semibold", "demi"))

reports = []
for filename, stem in SOURCES:
    pdf_path = ROOT / filename
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)
    doc = fitz.open(pdf_path)
    output = OUT / f"{stem}-layout.jsonl"
    bold_output = OUT / f"{stem}-bold-lines.jsonl"
    fonts = Counter()
    lines_count = bold_lines_count = spans_count = bold_spans_count = 0

    with output.open("w", encoding="utf-8") as all_file, bold_output.open("w", encoding="utf-8") as bold_file:
        for page_number, page in enumerate(doc, start=1):
            data = page.get_text("dict", sort=True)
            for block_number, block in enumerate(data.get("blocks", [])):
                if block.get("type") != 0:
                    continue
                for line_number, line in enumerate(block.get("lines", [])):
                    spans = []
                    for span in line.get("spans", []):
                        txt = span.get("text", "")
                        if not txt:
                            continue
                        bold = is_bold(span)
                        font = str(span.get("font", ""))
                        fonts[font] += 1
                        spans_count += 1
                        if bold:
                            bold_spans_count += 1
                        spans.append({
                            "text": txt,
                            "bold": bold,
                            "font": font,
                            "size": round(float(span.get("size", 0)), 2),
                            "flags": int(span.get("flags", 0)),
                            "bbox": [round(float(v), 2) for v in span.get("bbox", [])],
                        })
                    if not spans:
                        continue
                    text = "".join(s["text"] for s in spans)
                    has_bold = any(s["bold"] for s in spans)
                    record = {
                        "source": filename,
                        "page": page_number,
                        "block": block_number,
                        "line": line_number,
                        "bbox": [round(float(v), 2) for v in line.get("bbox", [])],
                        "text": text,
                        "bold_text": "".join(s["text"] for s in spans if s["bold"]),
                        "has_bold": has_bold,
                        "spans": spans,
                    }
                    encoded = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
                    all_file.write(encoded + "\n")
                    lines_count += 1
                    if has_bold:
                        bold_file.write(encoded + "\n")
                        bold_lines_count += 1

    reports.append({
        "source": filename,
        "pages": len(doc),
        "layout_lines": lines_count,
        "bold_lines": bold_lines_count,
        "spans": spans_count,
        "bold_spans": bold_spans_count,
        "fonts": dict(fonts.most_common()),
        "layout_file": str(output.relative_to(ROOT)),
        "bold_lines_file": str(bold_output.relative_to(ROOT)),
    })
    doc.close()

(OUT / "bold-layout-report.json").write_text(
    json.dumps(reports, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(json.dumps(reports, ensure_ascii=False, indent=2))
