# ripley-site

Static site for **ripleydecisionadvantage.net**. Six self-contained HTML pages, no
external dependencies at runtime — fonts are base64-embedded, all CSS is inline.
Deployed as a Cloudflare Worker with static assets (`ripley-site`).

## ⚠️ `build_site.py` is the source of truth — not the HTML

`site/*.html` is **generated output**. Editing those files directly works until the
next build, then your changes are gone. To change anything — copy, nav, colours,
layout — edit `build_site.py` and rebuild.

```bash
pip install fonttools brotli Pillow cairosvg
python3 build_site.py
```

That rewrites everything in `site/`. Open `site/index.html` in a browser to check.

## Layout

```
build_site.py     the whole site: CSS, page copy, nav, the mountain mark
fonts/            Oswald 700 + Quicksand 700, subset to woff2, base64'd at build
site/             generated — this is what gets deployed
```

## Pages

| File | In nav? | Notes |
|---|---|---|
| `index.html` | yes (About) | hero, firm, principal, services, track record, quote |
| `tools.html` | yes (Tools) | expertise groups + stack table |
| `contact.html` | yes (Contact) | email, phone, what to include |
| `egon.html` | **no — deliberately unlisted** | reachable by direct link only |
| `privacy.html` | footer | |
| `terms.html` | footer | |

### EGON is intentionally not in the nav

`egon.html` builds and deploys, but nothing on the public site links to it. Send the
URL directly to prospects rather than advertising the product. If you ever want it
public, add `("egon.html", "EGON")` back to the `NAV` list in `build_site.py`.

The phrase "Exit Value Enhancer" is not used anywhere. Don't reintroduce it.

## Design system

Palette: Red `#C8202F` · Gold `#E8A82A` · Blue `#4A6B8A` · Navy `#1A2332` · Cream `#F5EEE0`.
Oswald 700 for display, Arial for body. Red-square bullets, cream callouts with a blue
left rule, navy footer, five-star motif, red+gold edge bars.

The mountain mark lives as `MARK_PATHS` in `build_site.py` — a two-peak geometric
silhouette with true knockout snowcaps (`fill-rule: evenodd`, `fill: currentColor`, so
it inherits colour from context). That's the single source for the header lockup, the
hero, the footer and the favicons.

## Deploying

The Cloudflare Worker `ripley-site` serves `site/` and has both
`ripleydecisionadvantage.net` and `www.ripleydecisionadvantage.net` attached as custom
domains. Push to this repo, then redeploy the Worker (or wire up git-connected
deploys and skip the manual step).

## Content rules

- No mention of Pythia, anywhere, ever.
- No "Global DIN", `din-` asset paths, or EVE tokens — this is an external surface.
- No X / Moonshot Factory in the biography.
- The coinage "Resilient Intelligence" was dropped and stays dropped.
- Numbers over adjectives. Short sentences, active verbs, no coined terms.
