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

## Only the EGON service page is in the nav

Nav is About / EGON / Tools / Contact. "EGON" points at `egon-service.html`.
The other two EGON pages build and deploy outside the nav:

- `egon.html` — product page plus the Avondale worked example. Linked from the
  index "Current work" section and from the service page.
- `egon-baltimore.html` — Baltimore Harbor worked example. Linked from `egon.html`.
- `egon-service.html` — EGON as a tech-enabled service: what the client receives,
  why a service, the three engagement phases, defensibility, how to buy. In the
  nav, and also linked from the index "Current work" card, the Status list on
  `egon.html`, and Services card 04. The federal card names no contract vehicle
  and no catalog pricing on purpose — see TERMS.md §12.

None of the three is link-private or access-gated. Gating `/egon` with Cloudflare
Access is an open task. To add the one-pager to the nav too, add
`("egon.html", "EGON one-pager")` to the `NAV` list; to take the service page
out, remove its entry.

## bio.html is also outside the nav

`bio.html` is the long-form biography, reached from a small grey "more" link
beside the "The principal" heading on the index. Three numbered sections —
AI/ML engineering, international security, founder — modelled on the Defense
Angel Network bio page.

## The CV download

`site/leigh-anne-miller-cv.pdf` is a committed binary, like the favicon PNGs.
The build does not generate or touch it; drop in a new file to update it.
Linked from `bio.html` under the lead and from the contact callout, via
`CV_FILE` / `CV_NAME` in `build_site.py`. Content rules apply to the PDF too —
check a replacement for banned copy before committing it.

## Worked-example figures are illustrative

Both EGON pages carry dollar figures that are illustrative, not analysis output.
Each page states this in a `srcnote` under its table — keep that label unless the
numbers are replaced with sourced ones. Rows are internally consistent:
ROI = avoided loss ÷ spend, and the rows sum to the program total. Fix the
arithmetic if you edit a figure.

No site intake has been run for Baltimore. Its hazards reflect publicly documented
characteristics of the upper Chesapeake, not a study.

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
