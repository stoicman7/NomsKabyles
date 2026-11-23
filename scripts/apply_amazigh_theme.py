from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "index.html"
html = path.read_text(encoding="utf-8")

replacements = [
    (':root{--paper:#f5f6ef;--white:#fffefa;--ink:#1b3028;--forest:#193d32;--forest2:#285745;--sage:#829486;--line:#e1e7dc;--lime:#d9edb7;--shadow:0 24px 70px #1b372b17}',
     ':root{--paper:#f8f9f6;--white:#fffefa;--ink:#182c3d;--forest:#123b57;--forest2:#006a52;--sage:#718895;--line:#e1e8e8;--lime:#fcd116;--amazigh-blue:#0081c9;--amazigh-green:#009a5b;--amazigh-yellow:#fcd116;--amazigh-red:#d21034;--shadow:0 24px 70px #123b5717}'),
    ('*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font-family:"DM Sans",system-ui,sans-serif;-webkit-font-smoothing:antialiased}',
     '*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font-family:"DM Sans",system-ui,sans-serif;-webkit-font-smoothing:antialiased}body:before{content:"";display:block;height:7px;background:linear-gradient(90deg,var(--amazigh-blue) 0 25%,var(--amazigh-green) 25% 50%,var(--amazigh-yellow) 50% 75%,var(--amazigh-red) 75% 100%)}'),
    ('.logo{width:46px;height:46px;display:grid;place-items:center;border-radius:15px;background:var(--forest);color:var(--lime);font:29px "Noto Sans Tifinagh",sans-serif;box-shadow:0 8px 18px #183d3226}',
     '.logo{width:46px;height:46px;display:grid;place-items:center;border:2px solid #fff;border-radius:15px;background:linear-gradient(180deg,var(--amazigh-blue) 0 33.333%,var(--amazigh-green) 33.333% 66.666%,var(--amazigh-yellow) 66.666% 100%);color:var(--amazigh-red);font:31px "Noto Sans Tifinagh",sans-serif;font-weight:700;box-shadow:0 8px 18px #123b5726}'),
    ('background:linear-gradient(115deg,#193d32,#285745);color:#fffefa',
     'background:linear-gradient(115deg,#123b57 0%,#006a52 100%);color:#fffefa'),
    ('color:var(--lime);font-size:10px;font-weight:800;letter-spacing:2px;text-transform:uppercase',
     'color:var(--amazigh-yellow);font-size:10px;font-weight:800;letter-spacing:2px;text-transform:uppercase'),
    ('background:var(--lime);color:var(--forest);font-size:12px;font-weight:800',
     'background:var(--amazigh-yellow);color:#17384d;font-size:12px;font-weight:800'),
    ('background:linear-gradient(115deg,#193f33,#285745);color:white',
     'background:linear-gradient(115deg,#123b57,#007b5b);color:white'),
    ('color:#d5e8b5;font-size:9px;font-weight:800',
     'color:var(--amazigh-yellow);font-size:9px;font-weight:800'),
    ('color:#def0c719;font:180px "Noto Sans Tifinagh",sans-serif',
     'color:#d2103440;font:180px "Noto Sans Tifinagh",sans-serif'),
    ('margin:0;font:500 clamp(34px,5vw,48px)/1.15 "Playfair Display",Georgia,serif',
     'margin:0;font:800 clamp(34px,5vw,48px)/1.15 "DM Sans",system-ui,sans-serif;letter-spacing:-1.1px'),
]
for old, new in replacements:
    if old not in html:
        raise SystemExit("Expected theme anchor not found: " + old[:100])
    html = html.replace(old, new, 1)

html = html.replace(
    '<span class="sub">Dictionnaire des noms kabyles</span>',
    '<span class="sub">ⵜⴰⵎⴰⵣⵉⵖⵜ · Noms kabyles</span>', 1)
html = html.replace(
    '<p class="eyebrow">Identité · mémoire · transmission</p>',
    '<p class="eyebrow"><span style="font:15px &quot;Noto Sans Tifinagh&quot;,sans-serif;letter-spacing:0">ⴰⵣⵓⵍ</span> · Identité · mémoire · transmission</p>', 1)
html = html.replace(
    '<span class="footerbrand">ⵣ Ismwaen</span>',
    '<span class="footerbrand">ⵣ Ismwaen · ⴰⵣⵓⵍ</span>', 1)

start = html.find('<link rel="icon"')
end = html.find('\n', start)
if start < 0 or end < 0:
    raise SystemExit("Favicon declaration not found")
favicon = '<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 64 64%27%3E%3Crect width=%2764%27 height=%2764%27 rx=%2718%27 fill=%27%23fffefa%27/%3E%3Cpath d=%27M8 8h48v16H8z%27 fill=%27%230081c9%27/%3E%3Cpath d=%27M8 24h48v16H8z%27 fill=%27%23009a5b%27/%3E%3Cpath d=%27M8 40h48v16H8z%27 fill=%27%23fcd116%27/%3E%3Ctext x=%2750%25%27 y=%2754%25%27 dominant-baseline=%27middle%27 text-anchor=%27middle%27 font-size=%2740%27 font-weight=%27700%27 fill=%27%23d21034%27%3E%E2%B5%A3%3C/text%3E%3C/svg%3E">'
html = html[:start] + favicon + html[end:]
path.write_text(html, encoding="utf-8")
print("Amazigh palette and Tifinagh identity applied to index.html")
