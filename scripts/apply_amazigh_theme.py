from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "index.html"
html = path.read_text(encoding="utf-8")

if "--blue-primary:" in html and "background-size:260px 78px" in html:
    print("Blue-first Kabyle visual identity already present")
    raise SystemExit(0)

replacements = [
    ('<meta name="theme-color" content="#193d32">', '<meta name="theme-color" content="#006b9f">'),
    (
        ':root{--paper:#f8f9f6;--white:#fffefa;--ink:#182c3d;--forest:#123b57;--forest2:#006a52;--sage:#718895;--line:#e1e8e8;--lime:#fcd116;--amazigh-blue:#0081c9;--amazigh-green:#009a5b;--amazigh-yellow:#fcd116;--amazigh-red:#d21034;--shadow:0 24px 70px #123b5717}',
        ':root{--paper:#f6f9fb;--white:#fffefd;--ink:#18364a;--forest:#005b8e;--forest2:#0077b6;--sage:#718895;--line:#dce8ef;--lime:#f4d17c;--blue-primary:#006b9f;--blue-deep:#03496d;--amazigh-blue:#0081c9;--amazigh-green:#009a5b;--amazigh-yellow:#fcd116;--amazigh-red:#d21034;--clay:#a94d35;--motif-ink:#f2d7b4;--shadow:0 24px 70px #03496d18}'
    ),
    (
        'background:linear-gradient(90deg,var(--amazigh-blue) 0 25%,var(--amazigh-green) 25% 50%,var(--amazigh-yellow) 50% 75%,var(--amazigh-red) 75% 100%)',
        'background:linear-gradient(90deg,var(--blue-primary) 0 68%,var(--amazigh-yellow) 68% 79%,var(--amazigh-red) 79% 90%,var(--amazigh-green) 90% 100%)'
    ),
    (
        'background:linear-gradient(115deg,#123b57 0%,#006a52 100%);color:#fffefa',
        'background:linear-gradient(115deg,#033f63 0%,#006b9f 58%,#087eb6 100%);color:#fffefa'
    ),
    (
        'background:linear-gradient(115deg,#123b57,#007b5b);color:white',
        'background:linear-gradient(115deg,#03496d,#006b9f 70%,#087eb6);color:white'
    ),
    (
        'background:var(--amazigh-yellow);color:#17384d;font-size:12px;font-weight:800',
        'background:var(--blue-primary);color:#fff;font-size:12px;font-weight:800'
    ),
    (
        '.submit:hover{background:#cce5a2}',
        '.submit:hover{background:#03496d}'
    ),
    (
        'background:linear-gradient(180deg,var(--amazigh-blue) 0 33.333%,var(--amazigh-green) 33.333% 66.666%,var(--amazigh-yellow) 66.666% 100%)',
        'background:linear-gradient(180deg,var(--amazigh-blue) 0 54%,var(--amazigh-green) 54% 70%,var(--amazigh-yellow) 70% 86%,var(--amazigh-red) 86% 100%)'
    ),
    (
        'border:1px solid #e0f0c52a;border-radius:50%;box-shadow:0 0 0 45px #e0f0c508,0 0 0 95px #e0f0c508',
        'border:1px solid #f2d7b42a;border-radius:50%;box-shadow:0 0 0 45px #f2d7b408,0 0 0 95px #f2d7b408'
    ),
    (
        'border:1px solid #d9edb733;border-radius:50%;color:#d9edb7c9',
        'border:1px solid #f2d7b733;border-radius:50%;color:#f2d7b7c9'
    ),
    (
        'border:1px solid #d9edb72b;border-radius:50%',
        'border:1px solid #f2d7b72b;border-radius:50%'
    ),
    (
        'color:var(--amazigh-yellow);font-size:10px;font-weight:800;letter-spacing:2px;text-transform:uppercase',
        'color:var(--motif-ink);font-size:10px;font-weight:800;letter-spacing:2px;text-transform:uppercase'
    ),
    (
        'background:#fbfcf8}.inputwrap:focus-within{border-color:#9cb295;box-shadow:0 0 0 4px #bdd8a433;background:#fff',
        'background:#f8fbfd}.inputwrap:focus-within{border-color:#56a0c8;box-shadow:0 0 0 4px #0077b61c;background:#fff'
    ),
    (
        'border-color:#bdcfb7',
        'border-color:#8abbd5'
    ),
    (
        'color:#294b3b;font:500 clamp(20px,3vw,27px)/1.45',
        'color:#164765;font:500 clamp(20px,3vw,27px)/1.45'
    ),
    (
        '.suggestion:hover{background:#f3f7ee}',
        '.suggestion:hover{background:#eff7fb}'
    ),
    (
        '.choice:hover{border-color:#bdcfb7}',
        '.choice:hover{border-color:#8abbd5}'
    ),
]
for old, new in replacements:
    if old not in html:
        # Some palette anchors are deliberately optional if their selector is absent,
        # but every main structural colour anchor must be present.
        if old.startswith((":root", "background:linear-gradient(115deg", "background:var(--amazigh-yellow)")):
            raise SystemExit("Required blue-theme anchor not found: " + old[:120])
        continue
    html = html.replace(old, new, 1)

# Traditional Kabyle pottery/tattoo repertoire: a repeated register of diamonds,
# interlocking triangles, checkerboard squares, crosses, dots and comb-like lines.
# This is a decorative interpretation, not a claim that one pattern has one fixed meaning.
motif_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 78">
<g fill="none" stroke="#f2d7b4" stroke-width="1.7" stroke-linejoin="miter" opacity=".95">
<path d="M0 9H260M0 69H260"/>
<path d="M12 39l14-17 14 17-14 17zM52 39l14-17 14 17-14 17zM92 39l14-17 14 17-14 17zM172 39l14-17 14 17-14 17zM212 39l14-17 14 17-14 17zM252 39l8-10v20z"/>
<path d="M36 61L52 20l16 41zM76 20l16 41 16-41zM156 61l16-41 16 41zM196 20l16 41 16-41z"/>
<path d="M120 22h32v32h-32zM120 22l16 16-16 16M152 22l-16 16 16 16M136 22v32M120 38h32"/>
<path d="M8 63v-8m6 8V49m6 14V45m6 18V49m6 14V45m6 18V49m6 14V55"/>
<path d="M224 63v-8m6 8V49m6 14V45m6 18V49m6 14V45m6 18V49"/>
</g>
<g fill="#f2d7b4">
<circle cx="26" cy="39" r="2.2"/><circle cx="66" cy="39" r="2.2"/><circle cx="106" cy="39" r="2.2"/>
<circle cx="186" cy="39" r="2.2"/><circle cx="226" cy="39" r="2.2"/>
<path d="M132 16h8v3h-8zM132 59h8v3h-8z"/>
</g>
</svg>"""
motif_uri = "url('data:image/svg+xml," + quote(motif_svg, safe="") + "')"
motif_css = f"""
/* Kabyle geometric register inspired by pottery and tattoo motifs */
.hero:before{{
  content:"";position:absolute;z-index:0;left:0;right:0;bottom:0;height:78px;
  background-image:{motif_uri};background-repeat:repeat-x;background-size:260px 78px;
  opacity:.48;pointer-events:none
}}
.entrytop:before{{
  content:"";position:absolute;z-index:0;left:0;right:0;bottom:0;height:58px;
  background-image:{motif_uri};background-repeat:repeat-x;background-size:260px 78px;
  opacity:.23;pointer-events:none
}}
.hero:after{{border-color:#f2d7b42a}}
.entrytop:after{{color:#f2d7b423}}
.entryname,.entrykicker,.variants{{position:relative;z-index:1}}
.herocopy{{position:relative;z-index:2}}
"""
if ".hero:before{content:" not in html:
    html = html.replace("</style>", motif_css + "\n</style>", 1)

# A compact ornamental band made of a lozenge and cross motif, matching the register above.
html = html.replace(
    '<span class="sub">ⵜⴰⵎⴰⵣⵉⵖⵜ · Noms kabyles</span>',
    '<span class="sub">ⵜⴰⵎⴰⵣⵉⵖⵜ · Noms kabyles</span>', 1
)
path.write_text(html, encoding="utf-8")
print("Applied blue-first palette and Kabyle geometric pottery/tattoo register")
