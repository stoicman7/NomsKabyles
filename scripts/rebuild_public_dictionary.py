from pathlib import Path
import copy
import json
import re
import statistics
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / "extracted" / "layout"
BASE = ROOT / "dictionary.json"
OUT = ROOT / "dictionary.json"
REPORT = ROOT / "extracted" / "bold-audit-report.json"

def norm(value):
    value = unicodedata.normalize("NFD", str(value or "").lower())
    value = "".join(c for c in value if not unicodedata.combining(c))
    value = value.replace("ɣ", "gh").replace("ɛ", "e").replace("ε", "e")
    value = value.replace("’", "'").replace("‘", "'").replace(chr(96), "'").replace("´", "'")
    value = value.replace("–", " ").replace("—", " ").replace("-", " ")
    return re.sub(r"\s+", " ", value).strip()

def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", norm(value)).strip("-") or "entry"

def public_name(value):
    value = str(value).strip()
    return value[:1].upper() + value[1:]

def line_text(row, min_size=10):
    return "".join(span["text"] for span in row.get("spans", []) if float(span.get("size", 0)) >= min_size)

def clean_meaning(value):
    value = str(value or "")
    value = re.sub(r"\([^()]{1,120}\b(?:18|19|20)\d{2}\s*:\s*\d+[^()]*\)", "", value)
    value = re.sub(r"\([^()]{1,120}\b[A-ZÀ-Ž][A-Za-zÀ-ž-]{2,}(?:\s+[A-ZÀ-Ž][A-Za-zÀ-ž-]+)*\s*:\s*\d+[^()]*\)", "", value)
    value = re.sub(r"\([^()]{1,120}\b[A-ZÀ-Ž][A-Za-zÀ-ž-]{2,},\s*(?:18|19|20)\d{2}[^()]*\)", "", value)
    value = re.sub(r"\([^()]{1,100}[A-Za-zÀ-ž.-]{2,20}\s*:\s*\d+[^()]*\)", "", value)
    # Catch citations that use comma-separated year/page formats or abbreviated references.
    value = re.sub(r"\s*\((?=[^()]{1,160}(?:(?:18|19|20)\d{2}\s*[:,]\s*\d+|(?:18|19|20)\d{2}\s*,\s*\d+|:\s*\d+|,\s*(?:18|19|20)\d{2}\s*\)))[^()]*\)", "", value)
    value = re.sub(r"\b(?:souligne|selon|d’après)\s+Ahmed[- ]\s*Zaid(?:[- ]\s*Chertouk)?\s*", "", value, flags=re.I)
    value = re.sub(r"\b[A-ZÀ-Ž][A-Za-zÀ-ž-]{2,}\s*,\s*(?:18|19|20)\d{2}[a-z]?\s*", "", value)
    value = re.sub(r"D’après\s+[A-ZÀ-Ž][A-Za-zÀ-ž' -]{2,60}\s*\(:\s*\d+\),?\s*", "", value, flags=re.I)
    value = re.sub(r"les significations relevées par Ahmed-Zaid rejoignent, pour beaucoup, ces sens, ainsi", "on retrouve également ces sens dans les termes", value, flags=re.I)
    value = re.sub(r"(?<=[A-Za-zÀ-ž])\d+(?=\s|[,.;:!?)]|$)", "", value)
    value = value.replace("►", "; ")
    value = re.sub(r"\s+([,.;:!?])", r"\1", value)
    value = re.sub(r"([,;])\s*[;,.]+", r"\1", value)
    value = re.sub(r"\s{2,}", " ", value)
    value = re.sub(r"\s*;\s*", "; ", value)
    value = re.sub(r";\s*\.", ".", value)
    value = re.sub(r"\.\s*;", ";", value)
    return value.strip(" ;,")

def extract_heads(source, first_page, last_page):
    rows = [json.loads(line) for line in (LAYOUT / f"{source}-layout.jsonl").open(encoding="utf-8")]
    heads = []
    for row_index, row in enumerate(rows):
        if not first_page <= row["page"] <= last_page or not row.get("text", "").strip():
            continue
        chunks, started, pending = [], False, ""
        for span in row.get("spans", []):
            text = span.get("text", "")
            if not started:
                if not text.strip():
                    continue
                if span.get("bold"):
                    started = True
                    chunks.append(text)
                else:
                    break
            elif span.get("bold"):
                chunks.append(pending)
                pending = ""
                chunks.append(text)
            elif re.fullmatch(r"[\s,;]*", text):
                pending += text
            else:
                break
        prefix = "".join(chunks).strip()
        if not prefix:
            continue
        full_text = row["text"].strip()
        has_colon = ":" in prefix
        remainder = full_text[len(prefix):].lstrip() if full_text.startswith(prefix) else ""
        valid = has_colon or remainder.startswith((":", "«", '"', "“", "‘", "(", "/"))
        if source == "at_weghlis" and row["page"] == 90 and prefix.startswith("Djaafer"):
            valid = True
        if source == "at_weghlis" and row["page"] == 126 and prefix.startswith("Khalef"):
            valid = True
        if not valid or "dictionnaire" in prefix.lower() or "avertissement" in prefix.lower():
            continue
        raw_names = prefix.split(":", 1)[0].strip(" ,;")
        names = []
        for token in re.split(r"\s*,\s*", raw_names):
            token = re.sub(r"\d+$", "", token.strip()).strip(" ,;:")
            if token and token.lower() not in {"(k.)"}:
                names.append(token)
        if not names:
            continue
        first_remainder = full_text.split(":", 1)[1].strip() if ":" in full_text else remainder.strip(" ,;:")
        heads.append({"source": source, "page": row["page"], "idx": row_index, "names": names, "first_remainder": first_remainder})
    return rows, heads

def extract_meaning(rows, head, next_index):
    first_line = line_text(rows[head["idx"]], 10)
    if ":" in first_line:
        first_body = first_line.split(":", 1)[1].strip()
    else:
        first_body = first_line
        for _ in range(len(head["names"]) + 2):
            stripped = False
            for name in sorted(head["names"], key=len, reverse=True):
                pattern = r"^\s*" + re.escape(name) + r"\d*(?=\s*[,;:]|\s|$)"
                updated = re.sub(pattern, "", first_body, count=1, flags=re.I)
                if updated != first_body:
                    first_body = updated.lstrip(" ,;:")
                    stripped = True
                    break
            if not stripped:
                break
    parts = [first_body] if first_body else []
    for index in range(head["idx"] + 1, next_index):
        row = rows[index]
        text = " ".join(line_text(row, 10).split()).strip()
        if re.match(r"^(?:Bibliographie|Indexe? des patronymes)\b", text, re.I):
            break
        if not text or re.fullmatch(r"\d{1,3}", text):
            continue
        sizes = [float(s.get("size", 0)) for s in row.get("spans", []) if s.get("text", "").strip()]
        if sizes and statistics.median(sizes) < 10:
            continue
        parts.append(text)
    return clean_meaning(re.sub(r"\s+", " ", " ".join(parts)).strip())

base = json.loads(BASE.read_text(encoding="utf-8"))
data = copy.deepcopy(base)
entries = data["entries"]
lookup = {}
for index, entry in enumerate(entries):
    for alias in [entry.get("name", "")] + entry.get("variants", []):
        if alias:
            lookup.setdefault(norm(alias), index)

all_groups, all_bold_spellings = [], set()
for source, first_page, last_page in [("at_weghlis", 7, 195), ("at_yeemel", 31, 114)]:
    rows, heads = extract_heads(source, first_page, last_page)
    for head_index, head in enumerate(heads):
        group = [public_name(name) for name in head["names"] if norm(name)]
        if not group:
            continue
        all_bold_spellings.update(norm(name) for name in group)
        next_index = heads[head_index + 1]["idx"] if head_index + 1 < len(heads) else len(rows)
        all_groups.append({"source": source, "page": head["page"], "group": group, "meaning": extract_meaning(rows, head, next_index)})

# Separate definitions that were accidentally joined in the earlier plain-text import.
# Also remove a following headword definition when that surname is bold in the other volume.
all_bold_names = sorted({name for item in all_groups for name in item["group"]}, key=len, reverse=True)
all_bold_pattern = re.compile(
    r"(?<![\w])(" + "|".join(re.escape(name) for name in all_bold_names) + r")\d*\s*:",
    re.I,
) if all_bold_names else None
for item in all_groups:
    body = item["meaning"]
    if body and all_bold_pattern:
        for match in all_bold_pattern.finditer(body):
            if norm(match.group(1)) != norm(item["group"][0]):
                body = body[:match.start()].rstrip(" ;,:")
                break
    item["meaning"] = body

grouped = {}
for group in all_groups:
    key = tuple(norm(name) for name in group["group"])
    record = grouped.setdefault(key, {"group": group["group"], "meanings": [], "sources": []})
    if group["meaning"]:
        record["meanings"].append(group["meaning"])
    record["sources"].append((group["source"], group["page"]))

added_entries, updated_variants = [], []
for record in grouped.values():
    group = record["group"]
    known_indices = []
    for name in group:
        index = lookup.get(norm(name))
        if index is not None and index not in known_indices:
            known_indices.append(index)
    missing_names = [name for name in group if norm(name) not in lookup]
    if not missing_names:
        continue
    if known_indices:
        target = known_indices[0]
        entry = entries[target]
        variants = entry.setdefault("variants", [])
        known_variant_keys = {norm(v) for v in variants + [entry["name"]]}
        for name in missing_names:
            if norm(name) not in known_variant_keys:
                variants.append(name)
                known_variant_keys.add(norm(name))
                lookup[norm(name)] = target
                updated_variants.append({"entry": entry["name"], "added_variant": name, "source_group": group})
        best = max(record["meanings"], key=len, default="")
        current = entry.get("meaning", "")
        if best and len(best) > len(current) * 1.25 and len(best) > 100:
            entry["meaning"] = best
            entry["shortMeaning"] = best if len(best) <= 500 else best[:497].rsplit(" ", 1)[0] + "…"
        continue
    canonical = group[0]
    variants = []
    for name in group[1:]:
        if norm(name) != norm(canonical) and norm(name) not in {norm(v) for v in variants}:
            variants.append(name)
    meanings = []
    for meaning in sorted(set(record["meanings"]), key=len, reverse=True):
        if not any(meaning in old or old in meaning for old in meanings):
            meanings.append(meaning)
    meaning = " ".join(meanings).strip() or "Signification à préciser."
    provisional = bool(re.search(r"\b(probable|probablement|pourrait|pourraient|serait|seraient|semble|semblent|peut-être|hypothèse|possible|possiblement|peu probable|on peut)\b", meaning, re.I))
    entry_id = slug(canonical)
    existing_ids = {e.get("id") for e in entries + added_entries}
    suffix, original_id = 2, entry_id
    while entry_id in existing_ids:
        entry_id = f"{original_id}-{suffix}"
        suffix += 1
    entry = {
        "id": entry_id,
        "name": canonical,
        "variants": variants,
        "meaning": meaning,
        "shortMeaning": meaning if len(meaning) <= 500 else meaning[:497].rsplit(" ", 1)[0] + "…",
    }
    if provisional:
        entry["qualification"] = "Interprétation proposée : le texte présente une ou plusieurs pistes, qui ne doivent pas être considérées comme une certitude étymologique."
    added_entries.append(entry)
    new_index = len(entries) + len(added_entries) - 1
    for alias in [canonical] + variants:
        lookup.setdefault(norm(alias), new_index)

entries.extend(added_entries)
data["totalEntries"] = len(entries)

# Rebuild every canonical entry from its own bold heading, including entries that already
# existed in the older dictionary. The previous importer only updated newly added names,
# which left neighbouring surname definitions joined together.
direct_meanings = {}
for item in all_groups:
    if not item["meaning"]:
        continue
    for name in item["group"]:
        direct_meanings.setdefault(norm(name), []).append(item["meaning"])

canonical_lookup = {}
variant_lookup = {}
for index, entry in enumerate(entries):
    canonical_lookup.setdefault(norm(entry.get("name", "")), []).append(index)
    for alias in entry.get("variants", []):
        variant_lookup.setdefault(norm(alias), []).append(index)

updated_direct_entries = []
for key, candidates in direct_meanings.items():
    indices = canonical_lookup.get(key) or variant_lookup.get(key) or []
    if not indices:
        continue
    best = max(candidates, key=lambda meaning: (len(meaning), meaning.count("«")))
    for index in indices:
        entry = entries[index]
        if entry.get("meaning", "") != best:
            entry["meaning"] = best
            entry["shortMeaning"] = best if len(best) <= 500 else best[:497].rsplit(" ", 1)[0] + "…"
            updated_direct_entries.append(entry["name"])

# A spelling with its own standalone bold heading is a dictionary entry, not merely
# a variant of another surname. Split it into its own record if an earlier import merged it.
single_head_names = {
    name for item in all_groups if len(item["group"]) == 1 for name in item["group"]
}
canonical_norms = {norm(entry.get("name", "")) for entry in entries}
split_standalone_names = []
for name in sorted(single_head_names, key=lambda value: value.casefold()):
    key = norm(name)
    if key in canonical_norms:
        continue
    owner_indices = variant_lookup.get(key, [])
    body = max(direct_meanings.get(key, [""]), key=len, default="")
    if not body:
        body = "Renvoi à vérifier dans le dictionnaire."
    for owner_index in owner_indices:
        entries[owner_index]["variants"] = [
            alias for alias in entries[owner_index].get("variants", []) if norm(alias) != key
        ]
    new_id = slug(name)
    existing_ids = {entry.get("id") for entry in entries}
    base_id = new_id
    suffix = 2
    while new_id in existing_ids:
        new_id = f"{base_id}-{suffix}"
        suffix += 1
    new_entry = {
        "id": new_id,
        "name": name,
        "variants": [],
        "meaning": body,
        "shortMeaning": body if len(body) <= 500 else body[:497].rsplit(" ", 1)[0] + "…",
    }
    if re.search(r"\b(probable|probablement|pourrait|pourraient|serait|seraient|semble|semblent|peut-être|hypothèse|possible|possiblement|désignerait|viendrait)\b", body, re.I):
        new_entry["qualification"] = "Interprétation proposée : le texte présente une ou plusieurs pistes, qui ne doivent pas être considérées comme une certitude étymologique."
    entries.append(new_entry)
    canonical_norms.add(key)
    split_standalone_names.append(name)

data["totalEntries"] = len(entries)

# Remove bibliography-like citations from every public definition, including legacy entries.
cleaned_reference_entries = 0
for entry in entries:
    previous = entry.get("meaning", "")
    cleaned = clean_meaning(previous)
    if cleaned != previous:
        cleaned_reference_entries += 1
    entry["meaning"] = cleaned
    entry["shortMeaning"] = cleaned if len(cleaned) <= 500 else cleaned[:497].rsplit(" ", 1)[0] + "…"

ids = [entry.get("id") for entry in entries]
if len(ids) != len(set(ids)):
    raise ValueError("Duplicate entry IDs detected")
search_keys = {
    norm(alias)
    for entry in entries
    for alias in [entry.get("name", "")] + entry.get("variants", [])
    if alias
}
missing = sorted(name for name in all_bold_spellings if name not in search_keys)
if missing:
    raise ValueError("Bold surnames still missing from search index: " + ", ".join(missing))

owners = {}
for entry in entries:
    for alias in [entry.get("name", "")] + entry.get("variants", []):
        if alias:
            owners.setdefault(norm(alias), set()).add(entry["id"])
collisions = {key: sorted(value) for key, value in owners.items() if len(value) > 1}

REPORT.parent.mkdir(parents=True, exist_ok=True)
report = {
    "original_entries": len(base["entries"]),
    "corrected_entries": len(entries),
    "new_entry_records": len(added_entries),
    "bold_groups_scanned": len(all_groups),
    "distinct_bold_spellings_scanned": len(all_bold_spellings),
    "bold_spellings_missing_after_fix": len(missing),
    "variants_added_to_existing_entries": len(updated_variants),
    "normalized_alias_collision_keys": len(collisions),
    "entries_cleaned_of_bibliographic_references": cleaned_reference_entries,
    "entries_rebuilt_from_own_bold_headings": len(set(updated_direct_entries)),
    "standalone_names_split_from_variants": split_standalone_names,
    "added_entry_names": [entry["name"] for entry in added_entries],
    "added_variants": updated_variants,
    "validation": {"unique_ids": True, "all_bold_spellings_searchable": True, "bold_spelling_keys": len(all_bold_spellings)},
}
REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, indent=2))
