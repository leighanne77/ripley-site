# ripley-site — working notes

Static site for ripleydecisionadvantage.net. Deployed as a Cloudflare Worker
with static assets (`ripley-site`), apex + www attached.

## build_site.py is the source of truth

`site/*.html` is GENERATED. Never edit it — changes are lost on the next build.
All copy, CSS, nav and the mountain mark live in `build_site.py`.

Rebuild: `python3 build_site.py` (stdlib only — no dependencies needed).
fonttools/brotli/Pillow/cairosvg are only required to regenerate the woff2
fonts or the favicons, both of which are already committed.

## Content rules — do not violate

- NEVER mention Pythia. Anywhere. Hard rule.
- NEVER use "Exit Value Enhancer" or "exit-value enhancer". Banned copy.
- No "Global DIN", no `din-` asset paths, no EVE tokens — external surface.
- No X / Moonshot Factory in the biography.
- "Resilient Intelligence" was dropped and stays dropped.
- Voice: short sentences, active verbs, numbers over adjectives, no coined terms.

## EGON is deliberately unlisted

Nav is About / Tools / Contact. `egon.html` builds and deploys but nothing
links to it — the URL gets sent to prospects directly. To make it public, add
`("egon.html", "EGON")` back to the `NAV` list.

## Design system

Red #C8202F · Gold #E8A82A · Blue #4A6B8A · Navy #1A2332 · Cream #F5EEE0.
Oswald 700 display, Arial body. Red-square bullets, cream callouts with blue
left rule, navy footer, five-star motif, red+gold edge bars.

The mountain mark is `MARK_PATHS` — two-peak geometric silhouette, evenodd
knockout snowcaps, `fill:currentColor`. Single source for header lockup, hero,
footer and favicons.

## Deploys are manual

Pushing to GitHub does NOT update the live site. The Worker was deployed by
file upload, not git. Redeploy the Worker after pushing, or wire up
git-connected deploys.
