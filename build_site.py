#!/usr/bin/env python3
"""Build the Ripley Decision Advantage static site (EGON Space Retro system, Brand Guidelines v1.5).
Ripley identity on the EGON visual system. Six self-contained pages, fonts base64-embedded.
Source of truth for the Ripley mountain mark geometry: MARK_SVG below.
"""
import base64, html, os, pathlib, urllib.parse

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "site"
OUT.mkdir(exist_ok=True)

def b64(p):
    return base64.b64encode(open(p, "rb").read()).decode()

OSWALD = b64(ROOT / "fonts" / "Oswald-700.woff2")
QUICKSAND = b64(ROOT / "fonts" / "Quicksand-700.woff2")

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
a.card{display:block;text-decoration:none;color:inherit;transition:background .12s,border-color .12s;}
a.card:hover{background:var(--cream-soft);border-color:var(--red);}
a.card:hover h3{color:var(--red);}
a.card .mailcue{display:block;margin-top:10px;font-family:'Oswald',sans-serif;font-size:12px;
  letter-spacing:2px;text-transform:uppercase;color:var(--blue);}
a.card:hover .mailcue{color:var(--red);}
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

EMAIL = "miller@ripleydecisionadvantage.net"

# Each card is a mailto link with the enquiry pre-written, so the visitor's
# first email arrives already scoped to the service they clicked.
SERVICES = [
    ("01", "Zero-to-one product engineering",
     "Bespoke AI/ML systems from first requirement to production. Architecture, build, launch.",
     "I am writing to inquire about your zero-to-one product engineering services, "
     "please contact me to start this discussion"),
    ("02", "MLOps & governance",
     "Deployment pipelines, model risk management, and audit-ready frameworks that survive "
     "regulatory review.",
     "I am writing to inquire about your MLOps and governance services, "
     "please contact me to start this discussion"),
    ("03", "Technical sales & pre-sales",
     "Demos, proofs of concept, and technical narratives that close. Engineering credibility in "
     "the room.",
     "I am writing to inquire about your technical sales and pre-sales services, "
     "please contact me to start this discussion"),
]

def service_cards():
    cards = []
    for kick, title, blurb, ask in SERVICES:
        # quote (not quote_plus): a "+" would render literally in the mail body
        query = urllib.parse.urlencode({"subject": title, "body": ask},
                                       quote_via=urllib.parse.quote)
        href = html.escape(f"mailto:{EMAIL}?{query}", quote=True)
        cards.append(
            f'  <a class="card" href="{href}">'
            f'<span class="kick">{kick}</span>'
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
  <p class="sub">Silicon Valley consulting for high-stakes, low-trust environments.</p>
  <p class="doctype">Full-service &middot; Private sector and public sector</p>
  <div class="stars">&#9733; &#9733; &#9733; &#9733; &#9733;</div>
</div>

<h2>The firm</h2>
<p>Ripley Decision Advantage is a full-service consulting firm. We advise on AI/ML tools and
workflow optimization for businesses and public-sector organizations. The result is measured in
your numbers: lower engineering costs, stronger product-market fit, and growing revenue &mdash;
not just a beautiful product.</p>

<h2>The principal</h2>
<p>Leigh Anne Miller architects and industrializes AI/ML systems for high-stakes, low-trust
environments &mdash; from Fortune&nbsp;50 boardrooms to post-conflict infrastructure. She embeds
with the client, runs the technical discovery, and stays hands-on through production: the same
person in the executive demo and in the codebase. Caltech AI/ML engineering certificate, Stanford
master&rsquo;s, Tufts BA. Prior roles include Google, Nielsen/Gracenote, Spinf&nbsp;AI, and
HP&nbsp;Inc.</p>

<h2>Track record</h2>
<ul>
  <li>Restarted the world&rsquo;s largest metadata platform build &mdash; stalled in the
  <span class="num">$300M</span> Gracenote business at Nielsen.</li>
  <li>Improved IRR accuracy by <span class="num">15%+</span> in regulated capital-markets work.</li>
  <li>Production AI systems in continuous service since <span class="num">2023</span>.</li>
  <li>Built and piloted multi-agent systems for decision support, for infrastructure investors
  across <span class="num">four</span> countries &mdash; ports, data centers, and district
  assets.</li>
</ul>

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

<h2>Services</h2>
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
  """
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

<div class="callout">
  <div class="ctitle">Referee, not advocate</div>
  <p>EGON prices the exposure and lets the return choose the lever. Where a nature-based move beats
  hard infrastructure per dollar, EGON says so. Where it doesn&rsquo;t, EGON stays quiet.</p>
</div>

<h2>Who it serves</h2>
<p>Defense-critical and allied industrial assets &mdash; shipyards, ports, mineral processing, and
the energy that powers the perimeter &mdash; concentrated on coasts, rivers, and water-stressed
basins, where physical exposure matures inside the ownership window.</p>

<h2>What you get</h2>
<ul>
  <li>Quantified exposure across storm, water, heat, and ground &mdash; for your specific asset,
  not a region.</li>
  <li>A mitigation shortlist ranked by risk-adjusted return, tested on one basis across gray,
  nature-based, and hybrid options.</li>
  <li>Every figure traceable to a source that can be challenged line by line.</li>
  <li>Defensible, exportable scenarios a human carries into their own decision &mdash; never a
  decision the machine makes.</li>
</ul>

<h2>Two jobs, one dollar</h2>
<p>For public infrastructure, EGON extends service life: it finds what extreme weather will cost a
specific asset, what protects it, and what that protection is worth. For investors, the same
analysis carries into the ownership case &mdash; what the asset is worth at sale, once the exposure
is priced and the mitigations are paid for. The commercial case stands on its own; the protected
capability rides on top at no cost to return.</p>

<h2>Status</h2>
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
  """
<h1>Languages &amp; tools</h1>
<div class="h1-rule"></div>

<h2>Expertise</h2>
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

<h2>Stack</h2>
<table>
  <tr><th>Domain</th><th>Working set</th></tr>
  <tr><td class="dom">Agentic AI</td><td>Model Context Protocol, agent-to-agent systems, Pydantic
  AI, Google Agent Development Kit, Semantic Kernel, LangGraph, CrewAI</td></tr>
  <tr><td class="dom">ML Ops</td><td>Arize, Weights &amp; Biases, Amazon and Google ML platforms,
  voice infrastructure via Vapi and Retell AI</td></tr>
  <tr><td class="dom">Software</td><td>Python, Java, Scala, TypeScript, JavaScript, React,
  Node.js, FastAPI</td></tr>
  <tr><td class="dom">Data</td><td>PostgreSQL, Snowflake, Google BigQuery, Databricks, vector
  databases, BI platforms</td></tr>
  <tr><td class="dom">Compliance</td><td>Financial-services compliance (SEC/FINRA), insurance
  regulatory alignment (NAIC), explainable AI (XAI)</td></tr>
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
  <p style="margin-top:8px"><a href="http://instagram.com/leighanne3000">Instagram:
  @leighanne3000</a></p>
</div>

<h2>What to include</h2>
<ul>
  <li>The decision you need to make, and by when.</li>
  <li>What you have tried, and what it cost.</li>
  <li>Any regulatory or audit constraints up front.</li>
</ul>
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
