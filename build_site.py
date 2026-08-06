#!/usr/bin/env python3
"""Build the Ripley Decision Advantage static site (EGON Space Retro system, Brand Guidelines v1.5).
Ripley identity on the EGON visual system. Six self-contained pages, fonts base64-embedded.
Source of truth for the Ripley mountain mark geometry: MARK_SVG below.
"""
import base64, html, os, pathlib, re, urllib.parse

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "site"
OUT.mkdir(exist_ok=True)

def b64(p):
    return base64.b64encode(open(p, "rb").read()).decode()

def svg_asset(name):
    """Inline an SVG wordmark. Strips width/height so CSS controls the size —
    the viewBox alone keeps the aspect ratio."""
    s = (ROOT / "assets" / name).read_text().strip()
    s = re.sub(r'<\?xml[^>]*\?>\s*', '', s)
    s = re.sub(r'\s(width|height)="[^"]*"', '', s, count=2)
    return s

OSWALD = b64(ROOT / "fonts" / "Oswald-700.woff2")
QUICKSAND = b64(ROOT / "fonts" / "Quicksand-700.woff2")

# Partner wordmarks for the Current work thumbnails, recoloured cream to sit on
# navy panels. EGON from the web-demo asset; DIN from the bigdin.net lockup.
EGON_WORDMARK = svg_asset("egon-wordmark.svg")
DIN_WORDMARK = svg_asset("din-wordmark.svg")

# ---- Ripley mountain mark: geometric filled silhouette, true-knockout zigzag snowcaps
# (EGON-style: fill-rule evenodd, page shows through the caps; fill:currentColor)
MARK_PATHS = (
    '<path fill="currentColor" fill-rule="evenodd" d="M34 34 L66 92 L2 92 Z '
    'M25.5 52 L42.5 52 L45.5 59 L41.5 54.5 L37.5 59 L33.5 54.5 L29.5 59 L25.5 54.5 L22 59 Z"/>'
    '<path fill="currentColor" fill-rule="evenodd" d="M78 10 L118 92 L38 92 Z '
    'M68 32.5 L88 32.5 L91.5 41 L87 35.5 L82.5 41 L78 35.5 L73.5 41 L69 35.5 L64.5 41 Z"/>'
)
def mark_svg(cls=""):
    return (f'<svg class="{cls}" viewBox="0 0 120 100" role="img" aria-label="Ripley mountain mark" '
            f'xmlns="http://www.w3.org/2000/svg">{MARK_PATHS}</svg>')

CSS = """
:root{
  --red:#C8202F; --gold:#E8A82A; --blue:#4A6B8A; --navy:#1A2332; --cream:#F5EEE0;
  --red-soft:#D43545; --gold-soft:#F0BB52; --cream-soft:#FAF6EC;
}
@font-face{font-family:'Oswald';font-weight:700;font-style:normal;font-display:swap;
  src:url(data:font/woff2;base64,__OSWALD__) format('woff2');}
@font-face{font-family:'Quicksand';font-weight:700;font-style:normal;font-display:swap;
  src:url(data:font/woff2;base64,__QUICKSAND__) format('woff2');}
*{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
body{font-family:Arial,Helvetica,sans-serif;color:var(--navy);background:#fff;
  font-size:16px;line-height:1.5;}
.bar-red{height:10px;background:var(--red);}
.bar-gold{height:4px;background:var(--gold);}
/* header */
header{display:flex;align-items:center;justify-content:space-between;gap:24px;
  max-width:1060px;margin:0 auto;padding:18px 24px;}
.lockup{display:flex;align-items:center;gap:14px;color:var(--navy);text-decoration:none;}
.lockup svg{width:46px;height:38px;flex:none;}
.lockup .wm{font-family:'Quicksand',Arial,sans-serif;font-weight:700;font-size:23px;
  letter-spacing:.5px;line-height:1.05;}
.lockup .tag{font-family:Arial,sans-serif;font-weight:700;font-size:9.5px;
  letter-spacing:3.2px;color:var(--blue);margin-top:3px;}
nav{display:flex;gap:22px;flex-wrap:wrap;}
nav a{font-family:Arial,sans-serif;font-weight:700;font-size:12px;letter-spacing:2px;
  text-transform:uppercase;color:var(--navy);text-decoration:none;padding:4px 0;
  border-bottom:2px solid transparent;}
nav a:hover{color:var(--red);}
nav a.active{color:var(--red);border-bottom-color:var(--gold);}
/* layout */
main{max-width:1060px;margin:0 auto;padding:8px 24px 64px;}
/* type scale */
h1{font-family:'Oswald','Arial Black',Impact,sans-serif;font-weight:700;color:var(--red);
  font-size:44px;line-height:1.1;margin:34px 0 0;}
.h1-rule{width:120px;height:4px;background:var(--gold);margin:12px 0 26px;}
h2{font-family:Arial,sans-serif;font-weight:700;color:var(--navy);font-size:26px;
  line-height:1.2;margin:38px 0 10px;}
h3{font-family:Arial,sans-serif;font-weight:700;color:var(--blue);font-size:19px;
  line-height:1.3;margin:24px 0 6px;}
h4{font-family:Arial,sans-serif;font-weight:700;font-size:14px;letter-spacing:2px;
  text-transform:uppercase;margin:18px 0 4px;}
p{margin:0 0 12px;}
a{color:var(--blue);}
strong{font-weight:700;}
.num{font-family:'Courier New',Consolas,monospace;font-weight:700;}
/* bullets (§5.3): level-1 red filled square */
ul{list-style:none;margin:0 0 14px;}
ul li{padding-left:22px;position:relative;margin-bottom:7px;}
ul li::before{content:"\\25AA";color:var(--red);font-weight:700;position:absolute;left:0;top:0;}
ul ul{margin:7px 0 0;}
ul ul li::before{content:"\\2013";color:var(--navy);}
/* callout (§8.4) */
.callout{background:var(--cream);border-left:4px solid var(--blue);
  border-top:1.5px solid var(--blue);border-bottom:1.5px solid var(--blue);
  border-right:1px solid var(--gold);padding:20px 24px;margin:26px 0;}
.callout .ctitle{font-family:'Oswald',sans-serif;font-weight:700;color:var(--blue);
  font-size:19px;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;}
.callout p:last-child{margin-bottom:0;}
/* stars */
.stars{color:var(--red);letter-spacing:14px;font-size:18px;text-align:center;margin:18px 0;}
/* hero (title-slide anatomy, §9.1) */
.hero{text-align:center;padding:44px 0 10px;}
.hero svg{width:120px;height:100px;color:var(--navy);}
.hero .wm{font-family:'Quicksand',Arial,sans-serif;font-weight:700;font-size:46px;
  color:var(--navy);margin-top:10px;}
.hero .tag{font-family:Arial,sans-serif;font-weight:700;font-size:14px;letter-spacing:6px;
  color:var(--blue);text-transform:uppercase;margin-top:4px;}
.hero .rule{width:180px;height:3px;background:var(--gold);margin:22px auto;}
.hero h1{margin:0;}
.hero .sub{font-size:19px;color:var(--navy);margin-top:14px;}
.hero .doctype{font-style:italic;color:var(--blue);font-size:14px;margin-top:8px;}
/* services grid */
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px;margin:18px 0;}
.card{border:1px solid #ccc;border-top:4px solid var(--red);padding:18px;}
.card h3{margin-top:0;color:var(--navy);}
.card .kick{font-family:'Oswald',sans-serif;color:var(--red);font-size:13px;
  letter-spacing:2px;text-transform:uppercase;}
.icon{width:42px;height:42px;display:block;color:var(--navy);}
.card-icon{width:42px;height:42px;display:block;margin:10px 0 4px;color:var(--blue);
  transition:color .12s;}
h2 .icon{width:26px;height:26px;display:inline-block;vertical-align:-4px;margin-right:9px;
  color:var(--red);}
a.card{display:block;text-decoration:none;color:inherit;transition:background .12s,border-color .12s;}
a.card:hover .card-icon{color:var(--red);}
a.card:hover{background:var(--cream-soft);border-color:var(--red);}
a.card:hover h3{color:var(--red);}
a.card .mailcue{display:block;margin-top:10px;font-family:'Oswald',sans-serif;font-size:12px;
  letter-spacing:2px;text-transform:uppercase;color:var(--blue);}
a.card:hover .mailcue{color:var(--red);}
/* current work: two side-by-side blocks with wordmark thumbnails */
.work-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:22px;
  margin:18px 0 10px;}
.work-card{border:1px solid #ccc;border-top:4px solid var(--red);display:flex;
  flex-direction:column;}
/* Fixed panel height so both cards line up: the wordmarks have very different
   aspect ratios (EGON 4.2:1, DIN 2.4:1), so sizing by width alone left EGON's
   panel short. Cap both dimensions and let each mark land where it fits. */
.work-thumb{background:var(--navy);padding:20px 24px;display:flex;align-items:center;
  justify-content:center;height:140px;}
.work-thumb svg{max-height:64px;max-width:230px;width:auto;height:auto;display:block;}
.work-body{padding:16px 20px 20px;}
.work-body h3{margin:0 0 4px;color:var(--navy);font-size:17px;}
.work-body .meta{font-style:italic;color:var(--blue);font-size:13px;margin-bottom:10px;}
.work-body p{font-size:15px;}
.work-body ul{margin-bottom:10px;}
.work-body ul li{font-size:14px;margin-bottom:6px;}
/* ---- EGON graphics ---- */
/* hazard tiles */
.hz-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(94px,1fr));gap:10px;
  margin:16px 0 8px;}
.hz{background:var(--navy);color:var(--cream);padding:15px 6px 12px;text-align:center;}
.hz svg{width:28px;height:28px;color:var(--cream);margin:0 auto 8px;display:block;}
.hz span{font-weight:700;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;}
/* asset-class strip */
.ac-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(96px,1fr));gap:10px;margin:14px 0;}
.ac{border:1px solid #ccc;border-top:3px solid var(--blue);padding:11px 8px;text-align:center;
  font-weight:700;font-size:10.5px;letter-spacing:1.5px;text-transform:uppercase;color:var(--navy);}
/* then / now service-life diagram */
.tn-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:20px;margin:16px 0;}
.tn{border:1px solid #ccc;border-top:4px solid var(--red);padding:15px 18px 18px;}
.tn .k{font-family:'Oswald',sans-serif;font-size:23px;letter-spacing:2px;color:var(--navy);}
.tn .cap{font-weight:700;font-size:10.5px;letter-spacing:1.2px;text-transform:uppercase;
  color:var(--blue);margin:2px 0 14px;}
.tn-track{position:relative;height:62px;}
.tn-life,.tn-loss{position:absolute;height:24px;display:flex;align-items:center;
  justify-content:center;font-weight:700;font-size:9.5px;letter-spacing:1.5px;
  text-transform:uppercase;}
.tn-life{top:0;background:var(--blue);color:#fff;}
.tn-loss{top:32px;border:2px dashed var(--red);color:var(--red);}
.tn p{font-size:13px;margin:8px 0 0;}
/* ranked risks */
.risk{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline;padding:9px 0;
  border-bottom:1px solid #e4e4e4;}
.risk .rk{font-family:'Oswald',sans-serif;color:var(--red);font-size:14px;min-width:24px;}
.risk .rt{font-weight:700;font-size:15px;}
.risk .rd{font-size:13px;color:#555;flex:1 1 220px;}
.sev{font-weight:700;font-size:9.5px;letter-spacing:1.4px;text-transform:uppercase;
  padding:2px 7px;color:#fff;white-space:nowrap;}
.sev-c{background:var(--red);}
.sev-h{background:var(--gold);color:var(--navy);}
.sev-m{background:var(--blue);}
/* six-step flow */
.flow{display:grid;grid-template-columns:repeat(auto-fit,minmax(148px,1fr));gap:12px;margin:18px 0;}
.step{border:1px solid #ccc;border-top:3px solid var(--gold);padding:13px 14px 15px;}
.step .n{font-family:'Oswald',sans-serif;font-size:13px;letter-spacing:2px;color:var(--gold);}
.step .t{font-weight:700;font-size:12.5px;letter-spacing:1.2px;text-transform:uppercase;
  color:var(--navy);margin:5px 0 6px;}
.step p{font-size:13px;margin:0;color:#444;}
.step-art{width:100%;height:auto;display:block;margin:9px 0 10px;border:1px solid #dfe3e7;}
/* type chips */
.chip{font-weight:700;font-size:9.5px;letter-spacing:1.2px;text-transform:uppercase;
  padding:2px 8px;white-space:nowrap;}
.chip-g{background:var(--navy);color:var(--cream);}
.chip-n{background:var(--blue);color:#fff;}
.tbd{font-family:'Courier New',Consolas,monospace;font-weight:700;color:var(--blue);}
.srcnote{font-size:12px;color:#666;font-style:italic;margin-top:10px;}
/* asset scale band */
.stat-band{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:2px;
  background:var(--navy);margin:16px 0;}
.stat{padding:16px 12px;text-align:center;}
.stat .v{font-family:'Oswald',sans-serif;font-size:28px;color:var(--gold);line-height:1.1;}
.stat .l{font-size:10.5px;letter-spacing:1.4px;text-transform:uppercase;color:var(--cream);
  margin-top:5px;font-weight:700;}
/* quote (§9.4) */
.quote{margin:34px 0;padding:8px 0;text-align:center;}
.quote .q{font-family:'Oswald',sans-serif;font-weight:700;color:var(--red);
  font-size:28px;line-height:1.25;}
.quote .attr{color:var(--navy);font-size:14px;margin-top:10px;}
/* table (§8.5) */
table{border-collapse:collapse;width:100%;margin:18px 0;}
th{background:var(--red);color:#fff;font-family:'Oswald',Arial,sans-serif;font-weight:700;
  letter-spacing:1px;text-align:left;padding:12px 14px;font-size:15px;}
td{border:1px solid #ccc;padding:11px 14px;vertical-align:top;font-size:15px;}
tr:nth-child(even) td{background:var(--cream);}
td.dom{font-weight:700;white-space:nowrap;}
/* footer (§9.2 footer bar) */
footer{background:var(--navy);color:var(--cream-soft);}
.finner{max-width:1060px;margin:0 auto;padding:30px 24px;display:flex;flex-wrap:wrap;
  gap:22px;align-items:center;justify-content:space-between;}
.fmark{display:flex;align-items:center;gap:12px;color:var(--cream);}
.fmark svg{width:38px;height:32px;}
.fmark .wm{font-family:'Quicksand',Arial,sans-serif;font-weight:700;font-size:17px;}
.fmeta{color:var(--gold-soft);font-size:12px;letter-spacing:2px;text-transform:uppercase;
  font-weight:700;}
.fstars{color:var(--red-soft);letter-spacing:10px;font-size:14px;}
.flinks{display:flex;gap:16px;flex-wrap:wrap;}
.flinks a{color:var(--cream-soft);font-size:13px;text-decoration:none;}
.flinks a:hover{color:var(--gold-soft);text-decoration:underline;}
.fnote{width:100%;text-align:center;font-size:12px;color:#8FA0B8;margin-top:2px;}
.cta{display:inline-block;background:var(--red);color:#fff;font-family:'Oswald',sans-serif;
  font-weight:700;letter-spacing:2px;text-transform:uppercase;font-size:15px;
  padding:12px 26px;text-decoration:none;margin:10px 0;}
.cta:hover{background:var(--navy);color:var(--cream);}
.contact-big{font-size:22px;font-weight:700;}
.legal p, .legal li{font-size:15px;}
.legal h2{font-size:22px;margin-top:30px;}
@media (max-width:640px){
  h1{font-size:34px;} .hero .wm{font-size:34px;} header{flex-direction:column;gap:10px;}
  .quote .q{font-size:22px;}
}
""".replace("__OSWALD__", OSWALD).replace("__QUICKSAND__", QUICKSAND)

# EGON is deliberately NOT in the public nav. egon.html still builds and is
# reachable by direct link — send it to prospects rather than advertising it.
NAV = [("index.html", "About"), ("tools.html", "Tools"), ("contact.html", "Contact")]

def page(fname, title, desc, body):
    ACT = ' class="active"'
    nav = "".join(
        f'<a href="{h}"{ACT if h == fname else ""}>{t}</a>' for h, t in NAV)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="favicon.ico" sizes="48x48">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<style>{CSS}</style>
</head>
<body>
<div class="bar-red"></div><div class="bar-gold"></div>
<header>
  <a class="lockup" href="index.html">{mark_svg()}
    <span><span class="wm">Ripley</span><br><span class="tag">DECISION&nbsp;ADVANTAGE</span></span>
  </a>
  <nav>{nav}</nav>
</header>
<main>
{body}
</main>
<div class="bar-gold"></div><div class="bar-red"></div>
<footer><div class="finner">
  <div class="fmark">{mark_svg()}<span class="wm">Ripley Decision Advantage</span></div>
  <div class="fstars">&#9733; &#9733; &#9733; &#9733; &#9733;</div>
  <div class="flinks">
    <a href="privacy.html">Privacy Policy</a>
    <a href="terms.html">Terms of Service</a>
    <a href="mailto:miller@ripleydecisionadvantage.net">miller@ripleydecisionadvantage.net</a>
  </div>
  <div class="fnote">&copy; 2026 Ripley Decision Advantage &middot; Silicon Valley, California</div>
</div></footer>
</body>
</html>
"""

# ---- "How EGON works" panel art. Six flat scenes at a common 200x120 box,
# drawn in the site palette plus three illustration tints (sky, water, land).
# Text uses Arial so nothing depends on the embedded display face.
SKY, WATER, LAND, GRAYPAN = "#E8EEF3", "#9FB6C9", "#C6D3C2", "#8A94A0"

def _site_scene(markers=""):
    return (f'<rect width="200" height="120" fill="{SKY}"/>'
            f'<path d="M0 30 Q60 22 112 32 T200 28 L200 60 L0 60 Z" fill="{WATER}"/>'
            f'<rect y="60" width="200" height="60" fill="{LAND}"/>'
            '<rect x="68" y="40" width="58" height="24" fill="#fff" stroke="#1A2332" '
            'stroke-width="1.5"/>'
            '<rect x="74" y="46" width="12" height="11" fill="#E8EEF3"/>'
            '<rect x="90" y="46" width="12" height="11" fill="#E8EEF3"/>'
            '<rect x="106" y="46" width="12" height="11" fill="#E8EEF3"/>'
            '<path d="M6 94 Q100 74 194 90" stroke="#1A2332" stroke-width="2.5" fill="none"/>'
            + markers)

FLOW_ART = {
    # 1 — price the exposure: the asset in its setting, one hazard flagged
    "price": _site_scene(
        '<circle cx="34" cy="50" r="5" fill="#2E6B4F"/>'
        '<rect x="130" y="86" width="10" height="10" fill="#C8202F"/>'),
    # 2 — quantify the loss: earnings curve falling away from the flat baseline
    "loss":
        '<rect width="200" height="120" fill="#F2F4F6"/>'
        '<line x1="28" y1="14" x2="28" y2="98" stroke="#1A2332" stroke-width="1.5"/>'
        '<line x1="28" y1="98" x2="186" y2="98" stroke="#1A2332" stroke-width="1.5"/>'
        '<line x1="28" y1="32" x2="186" y2="32" stroke="#1A2332" stroke-width="1" '
        'stroke-dasharray="4 3"/>'
        '<path d="M28 32 C82 38 132 58 186 84 L186 32 Z" fill="#D6DBE0"/>'
        '<path d="M28 32 C82 38 132 58 186 84" stroke="#1A2332" stroke-width="2.5" fill="none"/>'
        '<circle cx="186" cy="84" r="4" fill="#1A2332"/>'
        '<rect x="92" y="50" width="74" height="19" rx="9.5" fill="#1A2332"/>'
        '<text x="129" y="63.5" font-family="Arial,sans-serif" font-size="10" font-weight="700" '
        'fill="#F5EEE0" text-anchor="middle">EBITDA drag</text>',
    # 3 — test every move: the three option classes, tested on one basis
    "test":
        '<rect width="200" height="120" fill="#F7F8F9"/>'
        f'<rect x="16" y="12" width="168" height="28" fill="{GRAYPAN}"/>'
        '<text x="100" y="30.5" font-family="Arial,sans-serif" font-size="11" font-weight="700" '
        'letter-spacing="1.5" fill="#fff" text-anchor="middle">GRAY</text>'
        '<rect x="16" y="46" width="168" height="28" fill="#E6EFE8" stroke="#2E6B4F"/>'
        '<text x="100" y="64.5" font-family="Arial,sans-serif" font-size="11" font-weight="700" '
        'letter-spacing="1.5" fill="#2E6B4F" text-anchor="middle">NATURE-BASED</text>'
        '<rect x="16" y="80" width="168" height="28" fill="#FBF1DC" stroke="#E8A82A"/>'
        '<text x="100" y="98.5" font-family="Arial,sans-serif" font-size="11" font-weight="700" '
        'letter-spacing="1.5" fill="#9A6E12" text-anchor="middle">HYBRID</text>',
    # 4 — ROI is the referee: the return tips the beam, gray is not automatic
    "roi":
        '<rect width="200" height="120" fill="#F7F8F9"/>'
        '<polygon points="100,42 90,100 110,100" fill="#1A2332"/>'
        '<line x1="26" y1="64" x2="174" y2="34" stroke="#1A2332" stroke-width="3"/>'
        '<circle cx="100" cy="49" r="4.5" fill="#1A2332"/>'
        f'<rect x="26" y="66" width="38" height="24" fill="{GRAYPAN}"/>'
        '<text x="45" y="101" font-family="Arial,sans-serif" font-size="9.5" fill="#1A2332" '
        'text-anchor="middle">Gray</text>'
        '<rect x="136" y="10" width="38" height="24" fill="#4A6B8A"/>'
        '<text x="155" y="46" font-family="Arial,sans-serif" font-size="9.5" font-weight="700" '
        'fill="#2E6B4F" text-anchor="middle">NbS &#8212; higher ROI</text>',
    # 5 — you pick: a portfolio across the site, not one project
    "pick": _site_scene(
        '<circle cx="30" cy="52" r="5" fill="#2E6B4F"/>'
        '<circle cx="150" cy="34" r="5" fill="#2E6B4F"/>'
        '<circle cx="60" cy="104" r="5" fill="#2E6B4F"/>'
        '<circle cx="140" cy="70" r="5" fill="#E8A82A"/>'
        '<rect x="128" y="86" width="10" height="10" fill="#C8202F"/>'
        '<text x="30" y="68" font-family="Arial,sans-serif" font-size="7.5" fill="#1A2332" '
        'text-anchor="middle">shoreline</text>'
        '<text x="150" y="24" font-family="Arial,sans-serif" font-size="7.5" fill="#1A2332" '
        'text-anchor="middle">marsh cell</text>'
        '<text x="60" y="116" font-family="Arial,sans-serif" font-size="7.5" fill="#1A2332" '
        'text-anchor="middle">ridge &amp; berm</text>'),
    # 6 — the result: one outcome that carries two others with it
    "result":
        '<rect width="200" height="120" fill="#F7F8F9"/>'
        '<rect x="82" y="10" width="36" height="26" fill="#1A2332"/>'
        '<rect x="88" y="16" width="7" height="7" fill="#F5EEE0"/>'
        '<rect x="99" y="16" width="7" height="7" fill="#F5EEE0"/>'
        '<rect x="88" y="27" width="7" height="6" fill="#F5EEE0"/>'
        '<rect x="99" y="27" width="7" height="6" fill="#F5EEE0"/>'
        '<text x="100" y="48" font-family="Arial,sans-serif" font-size="9" font-weight="700" '
        'fill="#1A2332" text-anchor="middle">Longer-lasting infrastructure</text>'
        '<polygon points="94,54 106,54 100,63" fill="#E8A82A"/>'
        '<rect x="26" y="70" width="56" height="34" fill="#fff" stroke="#c9ced4"/>'
        '<text x="54" y="86" font-family="Arial,sans-serif" font-size="8.5" font-weight="700" '
        'fill="#1A2332" text-anchor="middle">Better defense</text>'
        '<text x="54" y="96" font-family="Arial,sans-serif" font-size="8.5" font-weight="700" '
        'fill="#1A2332" text-anchor="middle">readiness</text>'
        '<text x="100" y="91" font-family="Arial,sans-serif" font-size="15" font-weight="700" '
        'fill="#E8A82A" text-anchor="middle">+</text>'
        '<rect x="118" y="70" width="56" height="34" fill="#fff" stroke="#c9ced4"/>'
        '<text x="146" y="86" font-family="Arial,sans-serif" font-size="8.5" font-weight="700" '
        'fill="#1A2332" text-anchor="middle">Local economic</text>'
        '<text x="146" y="96" font-family="Arial,sans-serif" font-size="8.5" font-weight="700" '
        'fill="#1A2332" text-anchor="middle">benefit</text>',
}

def art(name):
    return (f'<svg class="step-art" viewBox="0 0 200 120" role="img" aria-hidden="true" '
            f'xmlns="http://www.w3.org/2000/svg">{FLOW_ART[name]}</svg>')

EMAIL = "miller@ripleydecisionadvantage.net"

# ---- Section icons. Same treatment as the mountain mark: 64x64 box, geometric
# fills, navy swapped for currentColor so each icon inherits colour from context
# (navy at rest, red on card hover). Cream detail stays literal.
ICONS = {
    "summit":
        '<polygon points="0,58 30,16 50,58" fill="currentColor"/>'
        '<rect x="29" y="4" width="2.4" height="23" fill="currentColor"/>'
        '<polygon points="31.4,4 46,9 31.4,14" fill="currentColor"/>',
    "shield":
        '<path fill="currentColor" fill-rule="evenodd" '
        'd="M 32 4 L 56 12 L 54 36 Q 52 52 32 60 Q 12 52 10 36 L 8 12 Z"/>',
    "podium":
        '<rect x="7" y="32" width="15" height="26" fill="currentColor"/>'
        '<rect x="24.5" y="18" width="15" height="40" fill="currentColor"/>'
        '<rect x="42" y="40" width="15" height="18" fill="currentColor"/>'
        '<rect x="5" y="58" width="54" height="3" fill="currentColor"/>'
        '<rect x="26.5" y="30" width="11" height="1.6" fill="#F5EEE0"/>'
        '<rect x="26.5" y="34" width="11" height="1.6" fill="#F5EEE0"/>'
        '<rect x="26.5" y="38" width="11" height="1.6" fill="#F5EEE0"/>',
    "compass":
        '<polygon points="32,5 37.5,26.5 59,32 37.5,37.5 32,59 26.5,37.5 5,32 26.5,26.5" '
        'fill="currentColor"/>'
        '<circle cx="32" cy="32" r="5" fill="#F5EEE0"/>'
        '<circle cx="32" cy="32" r="2" fill="currentColor"/>',
    "industrial":
        '<rect x="10" y="6" width="9" height="52" fill="currentColor"/>'
        '<rect x="5" y="58" width="50" height="4" fill="currentColor"/>'
        '<rect x="10" y="6" width="47" height="4.5" fill="currentColor"/>'
        '<polygon points="19,10.5 31,10.5 19,20" fill="currentColor"/>'
        '<rect x="50" y="10.5" width="2.6" height="15" fill="currentColor"/>'
        '<rect x="45" y="25" width="11" height="7" fill="currentColor"/>',
    "people":
        '<circle cx="21" cy="35" r="13" fill="currentColor"/>'
        '<circle cx="42" cy="38" r="13" fill="currentColor"/>'
        '<ellipse cx="42" cy="30" rx="15" ry="2.5" fill="currentColor"/>'
        '<rect x="41.2" y="19.5" width="1.6" height="10" fill="#F5EEE0"/>'
        '<rect x="29" y="29.9" width="26" height="1.1" fill="#F5EEE0"/>',
    "briefcase":
        '<rect x="11" y="24" width="42" height="30" fill="currentColor"/>'
        '<rect x="26" y="16" width="12" height="6" fill="currentColor"/>'
        '<rect x="28.5" y="17.4" width="7" height="3" fill="#F5EEE0"/>'
        '<rect x="11" y="32" width="42" height="2.4" fill="#F5EEE0"/>'
        '<rect x="28.5" y="35" width="7" height="5" fill="#F5EEE0"/>',
    # the red lens detail would vanish inside a red heading, so it maps to cream
    "glasses":
        '<circle cx="23" cy="33" r="9" fill="currentColor"/>'
        '<circle cx="23" cy="33" r="5.5" fill="#F5EEE0"/>'
        '<circle cx="41" cy="33" r="9" fill="currentColor"/>'
        '<circle cx="41" cy="33" r="5.5" fill="#F5EEE0"/>'
        '<rect x="30" y="31.4" width="4" height="2.2" fill="currentColor"/>'
        '<polygon points="14,30.5 9,27 7.5,29 12.5,32.5" fill="currentColor"/>'
        '<polygon points="50,30.5 55,27 56.5,29 51.5,32.5" fill="currentColor"/>',
    "link":
        '<g transform="rotate(40 32 32)">'
        '<ellipse cx="32" cy="23" rx="10.5" ry="15" fill="currentColor"/>'
        '<ellipse cx="32" cy="23" rx="5.5" ry="10" fill="#F5EEE0"/>'
        '<ellipse cx="32" cy="41" rx="10.5" ry="15" fill="currentColor"/>'
        '<ellipse cx="32" cy="41" rx="5.5" ry="10" fill="#F5EEE0"/></g>',
    # --- hazard glyphs. drought/quake/flood come from the EGON icon set;
    # storm, heat and wildfire are drawn to match (same 64 box, flat fills).
    "drought":
        '<path fill-rule="evenodd" fill="currentColor" d="M32 6 C32 6 50 27 50 40 '
        'a18 18 0 0 1 -36 0 C14 27 32 6 32 6 Z M30 19 L33 19 L31 45 L28 45 Z '
        'M20 33 H44 V35.4 H20 Z"/>',
    "quake":
        '<path fill-rule="evenodd" fill="currentColor" d="M6 32 h17 l3 -6 l4 8 l3 -5 l4 7 h21 '
        'v20 a2 2 0 0 1 -2 2 h-50 a2 2 0 0 1 -2 -2 z M30 38 L33 38 L31 58 L27 58 Z"/>',
    "flood":
        '<g fill="currentColor" fill-rule="evenodd">'
        '<path d="M 2 20 Q 12 10 22 20 T 42 20 T 62 20 L 62 26 Q 52 16 42 26 T 22 26 T 2 26 Z"/>'
        '<path d="M 2 34 Q 12 24 22 34 T 42 34 T 62 34 L 62 40 Q 52 30 42 40 T 22 40 T 2 40 Z"/>'
        '<path d="M 2 48 Q 12 38 22 48 T 42 48 T 62 48 L 62 54 Q 52 44 42 54 T 22 54 T 2 54 Z"/>'
        '</g>',
    "storm":
        '<path fill="currentColor" d="M18 38 a11 11 0 0 1 3 -21 a14 14 0 0 1 26 4 '
        'a9 9 0 0 1 -1 17 Z"/>'
        '<polygon fill="currentColor" points="34,36 22,56 30,56 26,62 43,42 34,42 38,36"/>',
    "heat":
        '<circle cx="32" cy="32" r="11" fill="currentColor"/>'
        '<g fill="currentColor">'
        '<rect x="30" y="3" width="4" height="10"/><rect x="30" y="51" width="4" height="10"/>'
        '<rect x="3" y="30" width="10" height="4"/><rect x="51" y="30" width="10" height="4"/>'
        '<g transform="rotate(45 32 32)">'
        '<rect x="30" y="3" width="4" height="10"/><rect x="30" y="51" width="4" height="10"/>'
        '<rect x="3" y="30" width="10" height="4"/><rect x="51" y="30" width="10" height="4"/>'
        '</g></g>',
    "wildfire":
        '<polygon fill="currentColor" points="32,3 38,17 35,16 41,27 45,23 47,34 44,45 36,55 '
        '28,59 20,51 18,38 23,28 26,33 26,19 30,25"/>',
}

def icon(name, cls="icon"):
    return (f'<svg class="{cls}" viewBox="0 0 64 64" aria-hidden="true" '
            f'xmlns="http://www.w3.org/2000/svg">{ICONS[name]}</svg>')

# Each card is a mailto link with the enquiry pre-written, so the visitor's
# first email arrives already scoped to the service they clicked.
SERVICES = [
    ("01", "summit", "Zero-to-one product engineering",
     "Bespoke AI/ML systems from first requirement to production. Architecture, build, launch.",
     "I am writing to inquire about your zero-to-one product engineering services, "
     "please contact me to start this discussion"),
    ("02", "shield", "MLOps & governance",
     "Deployment pipelines, model risk management, and audit-ready frameworks that survive "
     "regulatory review.",
     "I am writing to inquire about your MLOps and governance services, "
     "please contact me to start this discussion"),
    ("03", "podium", "Technical sales & pre-sales",
     "Demos, proofs of concept, and technical narratives that close. Engineering credibility in "
     "the room.",
     "I am writing to inquire about your technical sales and pre-sales services, "
     "please contact me to start this discussion"),
]

def service_cards():
    cards = []
    for kick, ico, title, blurb, ask in SERVICES:
        # quote (not quote_plus): a "+" would render literally in the mail body
        query = urllib.parse.urlencode({"subject": title, "body": ask},
                                       quote_via=urllib.parse.quote)
        href = html.escape(f"mailto:{EMAIL}?{query}", quote=True)
        cards.append(
            f'  <a class="card" href="{href}">'
            f'<span class="kick">{kick}</span>'
            f'{icon(ico, "card-icon")}'
            f'<h3>{html.escape(title)}</h3>'
            f'<p>{html.escape(blurb)}</p>'
            f'<span class="mailcue">Click to email &rarr;</span></a>')
    return "\n".join(cards)

SERVICE_CARDS = service_cards()

PAGES = {}

# ---------------------------------------------------------------- index
PAGES["index.html"] = ("Ripley Decision Advantage — AI/ML Consulting, Silicon Valley",
  "Silicon Valley consulting firm. AI/ML systems for high-stakes, low-trust environments.",
  f"""
<div class="hero">
  {mark_svg()}
  <div class="wm">Ripley</div>
  <div class="tag">Decision Advantage</div>
  <div class="rule"></div>
  <h1>AI/ML systems that ship.</h1>
  <p class="sub">Engineering for high-stakes, low-trust environments, anywhere.</p>
  <p class="doctype">Full-service &middot; Private sector and public sector</p>
  <div class="stars">&#9733; &#9733; &#9733; &#9733; &#9733;</div>
</div>

<h2>{icon("industrial")}The firm</h2>
<p>Ripley Decision Advantage is a full-service AI/ML engineering consulting firm. We advise on
tooling and workflow optimization for businesses and public-sector organizations. The result is measured in
your numbers: lower engineering costs, stronger product-market fit, and growing revenue &mdash;
not just a beautiful product.</p>

<h2>{icon("people")}The principal</h2>
<p>Leigh Anne Miller architects and industrializes AI/ML systems for high-stakes, low-trust
environments &mdash; from Fortune&nbsp;50 boardrooms to post-conflict infrastructure. She embeds
with the client, runs the technical discovery, and stays hands-on through production: the same
person in the executive demo and in the codebase.</p>
<ul>
  <li>A decade-plus in tech, the last four as an AI/ML engineer.</li>
  <li>Started as a classically trained international security and foreign policy analyst &mdash;
  under Dr.&nbsp;Pfaltzgraff at Tufts, then with Dr.&nbsp;Strmecki at the Smith Richardson
  Foundation, whose board has included Rumsfeld, Brzezinski and Woolsey, and today McMaster and
  Keane.</li>
  <li>Volunteers with the Department of War&rsquo;s Office of Net Assessment on AI-enabled
  scenario-based planning.</li>
  <li>Affiliated with the Institute for State Effectiveness in Washington,&nbsp;D.C.</li>
  <li>EGON applies that background: AI-enabled scenario tools for rebuilding the infrastructure
  behind US organic means of production, built for a two-front scenario.</li>
  <li>Caltech AI/ML engineering certificate, Stanford master&rsquo;s, Tufts BA.</li>
  <li>Prior roles: Google, Nielsen/Gracenote, and HP&nbsp;Inc.</li>
</ul>

<h2>{icon("compass")}Track record</h2>
<ul>
  <li>Restarted the world&rsquo;s largest metadata platform build &mdash; stalled in the
  <span class="num">$300M</span> Gracenote business at Nielsen.</li>
  <li>Improved IRR accuracy by <span class="num">15%+</span> in regulated capital-markets work.</li>
  <li>Production AI systems in continuous service since <span class="num">2023</span>.</li>
  <li>Built and piloted multi-agent systems for decision support, for infrastructure investors
  across <span class="num">four</span> countries &mdash; ports, data centers, and district
  assets.</li>
  <li>Shipped HP&rsquo;s first API-based data exchange and governance capability, for a
  <span class="num">$40B</span> channel-partner program.</li>
</ul>

<h2>{icon("summit")}Current work</h2>

<div class="work-grid">

  <div class="work-card">
    <div class="work-thumb">{EGON_WORDMARK}</div>
    <div class="work-body">
      <h3>Extreme-weather risk for defense-adjacent assets</h3>
      <p class="meta">Ripley Decision Advantage &middot; Palo Alto, CA &middot; New as of
      July 2026 &middot; Founder &amp; architect</p>
      <p>A multi-agent decision-support system that prices statistically significant
      extreme-weather risk for the assets defense depends on &mdash; shipyards, ports, mineral
      processing, and the energy that powers the perimeter.</p>
      <ul>
        <li><span class="num">20+</span> data loaders on a 1&ndash;6 hour refresh, fusing NOAA,
        OpenFEMA and ERDDAP ground truth with an economic ledger and <span class="num">45+</span>
        nature-based-solutions datasets.</li>
        <li>Orchestrated on Google&rsquo;s ADK over the Agent-to-Agent protocol, with custom
        validation and resilience layers.</li>
        <li>Isolated and API-first. It never plugs into a financial core &mdash; it exports
        verifiable data a human carries into their own models.</li>
      </ul>
      <p><a href="egon.html">Read the EGON one-pager</a> &mdash; deeper technical detail on
      request.</p>
    </div>
  </div>

  <div class="work-card">
    <div class="work-thumb">{DIN_WORDMARK}</div>
    <div class="work-body">
      <h3>AI tools for patriotic capital</h3>
      <p class="meta">Palo Alto, CA &middot; May 2026&ndash;present &middot; AI Solution
      Architect &middot; <a href="https://www.bigdin.net">bigdin.net</a> (team access only)</p>
      <p>A production investor-relations platform for a dual-use defense investor team &mdash;
      maritime industrial base, critical-mineral sovereignty, energy resilience. Architected and
      shipped solo, live with a real user base.</p>
      <ul>
        <li>A graph-backed warm-introduction engine on Neo4j scores relationship paths
        deterministically and auditably, behind hard safety gates.</li>
        <li>PII governance mapped to NIST AI RMF and SR&nbsp;11-7: three-tier privacy at the
        query layer, owner-scoped writes, Fernet encryption, hashed-payload audit trail.</li>
        <li>Data layer right-sized deliberately &mdash; PostgreSQL and recursive CTEs first,
        Spark rejected as over-scaled for the volume.</li>
      </ul>
    </div>
  </div>

</div>

<div class="callout">
  <div class="ctitle">Stack</div>
  <p><strong>Languages</strong> &middot; Python, Java, TypeScript, JavaScript, React, Node.js,
  FastAPI, Pydantic, SQLAlchemy</p>
  <p><strong>Data</strong> &middot; PostgreSQL as production core &mdash; array columns, recursive
  CTEs &middot; Neo4j/Cypher &middot; Elasticsearch kNN &middot; BigQuery, Snowflake,
  Databricks/Spark, dbt, Airflow</p>
  <p><strong>Agentic</strong> &middot; Google ADK &middot; A2A protocol &middot; LangChain routing
  with SuperAGI autonomy &middot; graph-grounded output verification &middot; bounded agent loops
  &middot; human-in-the-loop &middot; MCP</p>
  <p><strong>Infrastructure</strong> &middot; GCP (Cloud Run, Cloud SQL, Secret Manager) &middot;
  AWS &middot; multi-cloud via Shadeform &middot; Docker &middot; Kubernetes &middot; WebSockets
  &middot; Cloudflare &middot; Google OAuth&nbsp;2.0 &middot; Fernet &middot; circuit breakers and
  exponential backoff</p>
  <p><strong>Evaluation and governance</strong> &middot; promptfoo &middot; Arize &middot;
  Weights &amp; Biases &middot; OpenTelemetry &middot; NIST AI RMF &middot; SR&nbsp;11-7 &middot;
  PII governance and RBAC &middot; confidential computing (TEEs)</p>
</div>

<div class="quote">
  <div class="q">&ldquo;Considered near-impossible to do &mdash; but she did them with
  ease.&rdquo;</div>
  <div class="attr">&mdash; Peter Dunker, VP Technology, Cloud Enablement &amp; Infrastructure,
  Gracenote / Nielsen &mdash; on the unified data model and platform build</div>
</div>

<div class="quote">
  <div class="q">&ldquo;She has an unmatched ability to lead by influence and gets
  results.&rdquo;</div>
  <div class="attr">&mdash; Filiz Bahmanpour, VP (Product), Gracenote / Nielsen</div>
</div>

<h2>{icon("briefcase")}Services</h2>
<p>Click any service to open an email, already written.</p>
<div class="grid">
{SERVICE_CARDS}
</div>

<p style="text-align:center">
  <a class="cta" href="mailto:{EMAIL}">Something else &mdash; email us</a><br>
  <a href="mailto:{EMAIL}">{EMAIL}</a>
</p>

""")

# ---------------------------------------------------------------- egon
PAGES["egon.html"] = ("EGON | Ripley Decision Advantage",
  "EGON prices physical risk on real assets and ranks the mitigations that pay for themselves.",
  f"""
<h1>EGON</h1>
<div class="h1-rule"></div>
<h4 style="color:var(--blue);letter-spacing:4px;">Physical risk, priced</h4>

<p>EGON prices physical risk on real assets. For a given asset, EGON quantifies the physical
exposure the owner actually carries, then tests every available mitigation against it &mdash; hard
infrastructure, nature-based solutions, and hybrids &mdash; on a single return-on-investment
basis.</p>
<p>The output is not a hazard map or an exploratory dashboard. It is a prescriptive shortlist: the
specific resilience moves that pay for themselves within the ownership period, ranked by
risk-adjusted return, with every number traceable to a source that can be challenged line by
line.</p>

<h2>{icon("industrial")}The economy runs on exposed ground</h2>
<p>Highways, ports, waterways, levees and dams &mdash; the arteries that move freight and project
force &mdash; concentrate on coasts, rivers and water-stressed basins.</p>

<div class="ac-row">
  <div class="ac">Highways</div>
  <div class="ac">Ports</div>
  <div class="ac">Waterways</div>
  <div class="ac">Levees</div>
  <div class="ac">Dams</div>
</div>

<p>There, six stressors now mature inside the asset&rsquo;s service life, not after it.</p>

<div class="hz-row">
  <div class="hz">{icon("storm")}<span>Storm</span></div>
  <div class="hz">{icon("flood")}<span>Flooding</span></div>
  <div class="hz">{icon("heat")}<span>Heat</span></div>
  <div class="hz">{icon("wildfire")}<span>Wildfire</span></div>
  <div class="hz">{icon("quake")}<span>Earthquake</span></div>
  <div class="hz">{icon("drought")}<span>Drought</span></div>
</div>

<div class="tn-grid">
  <div class="tn">
    <div class="k">THEN</div>
    <div class="cap">Built for a past where these stressors were rare</div>
    <div class="tn-track">
      <div class="tn-life" style="left:0;width:58%">Service life</div>
      <div class="tn-loss" style="left:64%;width:36%">Loss window</div>
    </div>
    <p>The asset was built, used and replaced before its design basis was exceeded.</p>
  </div>
  <div class="tn">
    <div class="k">NOW</div>
    <div class="cap">The asset breaks on your watch, before end of service life</div>
    <div class="tn-track">
      <div class="tn-life" style="left:0;width:78%">Service life</div>
      <div class="tn-loss" style="left:46%;width:54%">Loss window</div>
    </div>
    <p>The expected loss window has moved inside the expected service-life window.</p>
  </div>
</div>

<div class="callout">
  <div class="ctitle">Referee, not advocate</div>
  <p>EGON prices the exposure and lets the return choose the lever. Where a nature-based move beats
  hard infrastructure per dollar, EGON says so. Where it doesn&rsquo;t, EGON stays quiet.</p>
</div>

<h2>{icon("compass")}How EGON works</h2>
<div class="flow">
  <div class="step"><span class="n">01</span><div class="t">Price the exposure</div>
    {art("price")}
    <p>Every hazard priced across the site &mdash; terminal, riverfront, halls and grid.</p></div>
  <div class="step"><span class="n">02</span><div class="t">Quantify the loss</div>
    {art("loss")}
    <p>Physical damage erodes earnings across the hold period.</p></div>
  <div class="step"><span class="n">03</span><div class="t">Test every move</div>
    {art("test")}
    <p>Gray, nature-based and hybrid options tested on one basis.</p></div>
  <div class="step"><span class="n">04</span><div class="t">ROI is the referee</div>
    {art("roi")}
    <p>The return picks the lever. Funding sources found and included.</p></div>
  <div class="step"><span class="n">05</span><div class="t">You pick</div>
    {art("pick")}
    <p>A portfolio of site-wide options, not a single project.</p></div>
  <div class="step"><span class="n">06</span><div class="t">The result</div>
    {art("result")}
    <p>Longer-lasting infrastructure, better readiness, local economic benefit.</p></div>
</div>

<h2>{icon("summit")}Worked example &mdash; Avondale, Louisiana</h2>
<p>A 254-acre riverfront terminal on the Mississippi at River Mile&nbsp;108, twenty miles upriver
from New Orleans, on a ten-year hold. Heavy fabrication on deepwater with rail and barge on the
same pad is scarce, and every operational day lost to river flood, surge or grid failure is
capacity the Gulf cannot replace quickly.</p>

<div class="stat-band">
  <div class="stat"><div class="v">254</div><div class="l">acre terminal</div></div>
  <div class="stat"><div class="v">1.5M</div><div class="l">sq ft under roof</div></div>
  <div class="stat"><div class="v">8,000</div><div class="l">ft deepwater frontage</div></div>
  <div class="stat"><div class="v">50</div><div class="l">heavy-duty cranes</div></div>
</div>

<h3>The risks it faces</h3>
<div class="risk"><span class="rk">#1</span><span class="rt">Hurricane surge</span>
  <span class="sev sev-c">Critical</span>
  <span class="rd">Back-door pathway in behind the West Bank.</span></div>
<div class="risk"><span class="rk">#2</span><span class="rt">Mississippi River flood</span>
  <span class="sev sev-c">Critical</span>
  <span class="rd">Stage-frequency at the reach &mdash; river stage is not coastal sea level this
  far upriver.</span></div>
<div class="risk"><span class="rk">#3</span><span class="rt">Subsidence</span>
  <span class="sev sev-h">High</span>
  <span class="rd">Modifies every elevation rather than standing as a loss of its own.</span></div>
<div class="risk"><span class="rk">#4</span><span class="rt">Hurricane wind</span>
  <span class="sev sev-h">High</span>
  <span class="rd">Category 3&ndash;5 against a large envelope and heavy-duty cranes.</span></div>
<div class="risk"><span class="rk">#5</span><span class="rt">Relative sea-level rise</span>
  <span class="sev sev-m">Medium</span>
  <span class="rd">Measured at a gauge, not modelled from a regional average.</span></div>
<div class="risk"><span class="rk">#6</span><span class="rt">Extreme heat</span>
  <span class="sev sev-m">Medium</span>
  <span class="rd">Lost work hours and degradation on the fabrication floor.</span></div>

<h3>Ranked resilience opportunities</h3>
<p>Ranked by return, not by preference. Three nature-based moves clear the floodwall on
return per dollar &mdash; which is the whole point of letting ROI referee.</p>
<table>
  <tr><th>Move</th><th>Type</th><th>Spend</th><th>Avoided loss<br>(10-yr)</th><th>ROI</th></tr>
  <tr><td>Shell-reef breakwater &mdash; back-door surge attenuation</td>
    <td><span class="chip chip-n">Nature-based</span></td>
    <td class="num">$18M</td><td class="num">$67M</td><td class="num">3.7&times;</td></tr>
  <tr><td>Batture living shoreline along the frontage</td>
    <td><span class="chip chip-n">Nature-based</span></td>
    <td class="num">$12M</td><td class="num">$41M</td><td class="num">3.4&times;</td></tr>
  <tr><td>Beneficial-use marsh creation cell at the reach</td>
    <td><span class="chip chip-n">Nature-based</span></td>
    <td class="num">$9M</td><td class="num">$28M</td><td class="num">3.1&times;</td></tr>
  <tr><td>Terminal-perimeter floodwall and closure structures</td>
    <td><span class="chip chip-g">Gray</span></td>
    <td class="num">$48M</td><td class="num">$126M</td><td class="num">2.6&times;</td></tr>
  <tr><td>Land-bridge ridge and berm from dredged placement</td>
    <td><span class="chip chip-n">Nature-based</span></td>
    <td class="num">$22M</td><td class="num">$58M</td><td class="num">2.6&times;</td></tr>
  <tr><td><strong>Site-wide resilience program</strong></td>
    <td>&mdash;</td>
    <td class="num"><strong>$109M</strong></td><td class="num"><strong>$320M</strong></td>
    <td class="num"><strong>2.9&times;</strong></td></tr>
</table>

<p class="srcnote"><strong>Illustrative figures</strong>, sized to show the shape of an EGON
output rather than to state findings about this site. In a live engagement every cell carries its
citation, formula, model reference and sensitivity, and no number enters a payload before a source
that contains it is cited. ROI is avoided loss divided by spend over a ten-year hold. Committed and
underway public work is screened out as baseline, never re-proposed as an opportunity.</p>

<h2>{icon("shield")}What you get</h2>
<ul>
  <li>Quantified exposure across storm, water, heat and ground &mdash; for your specific asset,
  not a region.</li>
  <li>A mitigation shortlist ranked by risk-adjusted return, tested on one basis across gray,
  nature-based and hybrid options.</li>
  <li>Every figure traceable to a source that can be challenged line by line.</li>
  <li>Defensible, exportable scenarios a human carries into their own decision &mdash; never a
  decision the machine makes.</li>
</ul>

<h2>{icon("people")}Who it serves</h2>
<p>Defense-critical and allied industrial assets &mdash; shipyards, ports, mineral processing, and
the energy that powers the perimeter &mdash; concentrated on coasts, rivers, and water-stressed
basins, where physical exposure matures inside the ownership window.</p>

<h2>{icon("briefcase")}Two jobs, one dollar</h2>
<p>For public infrastructure, EGON extends service life: it finds what extreme weather will cost a
specific asset, what protects it, and what that protection is worth. For investors, the same
analysis carries into the ownership case &mdash; what the asset is worth at sale, once the exposure
is priced and the mitigations are paid for. The commercial case stands on its own; the protected
capability rides on top at no cost to return.</p>

<h2>{icon("glasses")}Status</h2>
<ul>
  <li>Built and piloted across ports, data centers, and district infrastructure in
  <span class="num">four</span> countries.</li>
  <li>Delivered by Ripley Decision Advantage. Demonstrations available under NDA.</li>
</ul>

<p style="text-align:center"><a class="cta" href="contact.html">Ask about EGON</a></p>
""")

# ---------------------------------------------------------------- tools
PAGES["tools.html"] = ("Languages & Tools | Ripley Decision Advantage",
  "Expertise and technical stack: agentic AI, MLOps, software, data, and compliance.",
  f"""
<h1>Languages &amp; tools</h1>
<div class="h1-rule"></div>

<h2>{icon("glasses")}Expertise</h2>
<h3>Strategic technical leadership</h3>
<ul>
  <li>Sales engineering &middot; product engineering &middot; executive AI strategy</li>
  <li>Industrialized AI delivery &middot; high-ROI use-case prioritization</li>
</ul>
<h3>Technical architecture</h3>
<ul>
  <li>AI solution architecture &middot; agentic AI &amp; orchestration</li>
  <li>Multimodal AI &middot; vision-language-action (VLA) systems</li>
</ul>
<h3>Governance &amp; systems</h3>
<ul>
  <li>Regulatory sandbox execution &middot; systems design methodologies</li>
  <li>Model risk management (MRM) automation</li>
</ul>

<h2>{icon("link")}Stack</h2>
<table>
  <tr><th>Domain</th><th>Working set</th></tr>
  <tr><td class="dom">Data</td><td>PostgreSQL as production core &mdash; array columns, recursive
  CTEs. Neo4j/Cypher for graph fact-checking and the warm-introduction engine. Elasticsearch kNN.
  Prior platform roles: BigQuery, Snowflake, Databricks/Spark, dbt, Airflow</td></tr>
  <tr><td class="dom">Pipelines</td><td>ETL and ingestion across <span class="num">20+</span>
  external-source loaders, entity resolution, data fusion, OSINT acquisition, provenance and
  lineage, data quality</td></tr>
  <tr><td class="dom">Agentic AI</td><td>LangChain routing with SuperAGI autonomy as a Compound AI
  System. A Google ADK build implementing Google&rsquo;s A2A protocol. Graph-grounded output
  verification. Pydantic-driven tool use, bounded agent loops, human-in-the-loop, MCP</td></tr>
  <tr><td class="dom">Software</td><td>Python, Java, TypeScript, JavaScript, React, Node.js,
  FastAPI, Pydantic, SQLAlchemy. AI-native delivery with Claude Code</td></tr>
  <tr><td class="dom">Infrastructure</td><td>AWS and GCP (Cloud Run, Cloud SQL, Secret Manager),
  multi-cloud via Shadeform, Docker, Kubernetes, Cloudflare, Google OAuth&nbsp;2.0, Fernet,
  circuit breakers and exponential backoff</td></tr>
  <tr><td class="dom">ML Ops</td><td>Arize, Weights &amp; Biases, promptfoo. Model evaluation,
  capability auditing, AI failure-mode analysis, boundary testing</td></tr>
  <tr><td class="dom">Voice</td><td>ASR/TTS and streaming audio &mdash; Vapi, Retell AI, Chirp,
  Groq, ElevenLabs, Deepgram</td></tr>
  <tr><td class="dom">Governance</td><td>NIST AI RMF, model risk management (SR&nbsp;11-7),
  SEC/FINRA and NAIC alignment, PII governance and RBAC, explainable AI (XAI), audit-trail
  architectures, confidential computing (TEEs), data contracts</td></tr>
</table>

<div class="callout">
  <div class="ctitle">Selection discipline</div>
  <p>Tools are chosen per engagement &mdash; on fit, auditability, and total cost of ownership,
  never on fashion. If a simpler tool survives the audit, the simpler tool wins.</p>
</div>

<div class="quote">
  <div class="q">&ldquo;She was 100% responsible for a successful outcome and got it done in
  less than three months.&rdquo;</div>
  <div class="attr">&mdash; Michael Khait, now CTO &amp; Co-founder, TrustPoint Technologies</div>
</div>
""")

# ---------------------------------------------------------------- contact
PAGES["contact.html"] = ("Contact | Ripley Decision Advantage",
  "Contact Ripley Decision Advantage. Email miller@ripleydecisionadvantage.net.",
  """
<h1>Contact</h1>
<div class="h1-rule"></div>
<p>One email starts it. Describe the problem; we answer with questions, not a pitch.</p>

<div class="callout">
  <div class="ctitle">Reach me directly</div>
  <p class="contact-big"><a href="mailto:miller@ripleydecisionadvantage.net">miller@ripleydecisionadvantage.net</a></p>
  <p class="contact-big"><a href="tel:+16504696032">+1&#8209;650&#8209;469&#8209;6032</a>
  <span style="font-size:14px;font-weight:400">(call or text)</span></p>
  <p style="margin-top:8px"><a href="https://www.linkedin.com/in/leighannemillerengineering/">LinkedIn:
  leighannemillerengineering</a></p>
</div>

<div class="stars">&#9733; &#9733; &#9733; &#9733; &#9733;</div>
""")

# ---------------------------------------------------------------- privacy
PAGES["privacy.html"] = ("Privacy Policy | Ripley Decision Advantage",
  "Privacy policy for Ripley Decision Advantage.",
  """
<div class="legal">
<h1>Privacy Policy</h1>
<div class="h1-rule"></div>
<p><em>Last updated March 9, 2024.</em></p>
<p>This policy describes how Ripley Decision Advantage handles personal data for visitors and for
those responding to our advertisements. We respect your privacy rights. We will not send you news,
special offers, or general information about other goods, services, and events similar to those you
have already purchased or enquired about unless you have opted in to receive such information.</p>

<h2>Interpretation and definitions</h2>
<p>Capitalized terms have the following meanings. <strong>Company</strong> (also &ldquo;We&rdquo;)
means Ripley Decision Advantage. <strong>Device</strong> means any device that can access the
Service, such as a computer, phone, or tablet. <strong>Personal Data</strong> means information
that identifies an individual. <strong>Service</strong> means our advertisement, website, or
application. <strong>Service Provider</strong> means a third party that processes data on our
behalf. <strong>Usage Data</strong> means information collected automatically through use of the
Service. <strong>You</strong> means the individual or entity accessing the Service.</p>

<h2>Data we collect</h2>
<p><strong>Personal Data.</strong> We may ask for your name, email address, phone number, location
information, and personal preferences or requirements.</p>
<p><strong>Usage Data.</strong> Collected automatically when the Service is used.</p>

<h2>How we use personal data</h2>
<ul>
  <li>To provide, maintain, and monitor the Service.</li>
  <li>To manage your account and registration.</li>
  <li>To perform contracts for products or services you purchase.</li>
  <li>To contact you with updates and security notices.</li>
  <li>To handle your requests.</li>
  <li>To evaluate business transfers or asset sales.</li>
  <li>For analytics and to improve the Service.</li>
</ul>

<h2>Sharing</h2>
<p>Personal information may be shared with Service Providers that monitor Service usage; with
parties involved in a business transfer; with affiliated companies; with business partners offering
products or promotions; with other users when you post in public areas; and with third parties with
your consent.</p>

<h2>Retention</h2>
<p>We retain Personal Data only as long as necessary for the purposes above and to comply with
legal obligations.</p>

<h2>Transfer</h2>
<p>Your information may be processed outside your jurisdiction. By providing information, you
consent to that transfer.</p>

<h2>Disclosure</h2>
<p>We may disclose data when required by law, court order, or government request, and where
necessary to protect rights, investigate wrongdoing, protect user safety, or limit legal
liability.</p>

<h2>Security</h2>
<p>We use commercially acceptable means to protect your Personal Data. No method of transmission
or storage is absolutely secure.</p>

<h2>Third-party links</h2>
<p>The Service links to external sites. We are not responsible for third-party content or privacy
practices.</p>

<h2>Changes</h2>
<p>Updates to this policy are posted on this page.</p>

<h2>Contact</h2>
<p>Questions: <a href="mailto:miller@ripleydecisionadvantage.net">miller@ripleydecisionadvantage.net</a></p>
</div>
""")

# ---------------------------------------------------------------- terms
PAGES["terms.html"] = ("Terms of Service | Ripley Decision Advantage",
  "Terms of service for Ripley Decision Advantage.",
  """
<div class="legal">
<h1>Terms of Service</h1>
<div class="h1-rule"></div>

<h2>Conditions of use</h2>
<p>We provide our AI/ML consulting services to you subject to the conditions in this document. Our
offerings include custom model development, MLOps implementation, vendor evaluation, and workflow
optimization.</p>

<h2>Privacy policy</h2>
<p>Please review our <a href="privacy.html">Privacy Policy</a> before continuing. It covers data
collection practices and information-security matters, including those related to AI model
training.</p>

<h2>Copyright</h2>
<p>Content published on this website &mdash; digital downloads, images, texts, graphics, logos, AI
models, and algorithms &mdash; is the property of Ripley Decision Advantage and protected by
international copyright law.</p>

<h2>Communications</h2>
<p>All interactions occur electronically. By subscribing to updates you consent to receive emails
about AI/ML developments. All notices, disclosures, agreements, and other communications we
provide to you electronically meet the legal requirement that such communications be in
writing.</p>

<h2>Applicable law</h2>
<p>United States law governs these terms and any disputes, without regard to conflict-of-law
principles.</p>

<h2>Disputes</h2>
<p>Any dispute shall be arbitrated by state or federal court in the United States, and you consent
to the exclusive jurisdiction of such courts.</p>

<h2>Comments, reviews, and emails</h2>
<p>You may post content provided it is not obscene, illegal, defamatory, threatening, or
infringing. We reserve the right to remove or edit submissions, and we retain a non-exclusive,
royalty-free, irrevocable right to use, reproduce, publish, and modify such content.</p>

<h2>License and site access</h2>
<p>We grant you access for personal use only. Downloading or modifying AI models requires our
written authorization.</p>

<h2>User account</h2>
<p>You are responsible for maintaining the confidentiality of your credentials and for all
activity under your account. We may terminate accounts at our discretion.</p>
</div>
""")

for fname, (title, desc, body) in PAGES.items():
    (OUT / fname).write_text(page(fname, title, desc, body))
    print(f"wrote {fname}  {os.path.getsize(OUT / fname):,} bytes")

# standalone favicon.svg (navy tile, cream mark — EGON §3.2 approach, Ripley mark)
FAV = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
<rect width="128" height="128" rx="24" fill="#1A2332"/>
<g transform="translate(4,16)" color="#F5EEE0">{MARK_PATHS}</g>
</svg>"""
(OUT / "favicon.svg").write_text(FAV)
print("wrote favicon.svg")
