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
- First person singular. The site speaks as Leigh Anne: "I", "my", "me", never
  "we" or "our" (2026-09-24: "it is only me"). Exceptions: the privacy and
  terms pages keep "we" as the Company, testimonial quotes keep "she", and
  bio.html stays in the third person.

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

## The principal thumbnails

The index "The principal" section is one intro line and three clickable
thumbnails, one per page of the three-page FDE infographic
`site/leigh-anne-miller-fde.pdf` (`FDE_FILE`, also a committed binary). Each
thumbnail opens the PDF at its page via `#page=N`. Nothing else about the
principal lives on the index; the long form is `bio.html`.

The infographic's HTML source is committed as `assets/fde-infographic-source.html`
(v2, 2026-09-24; it embeds its own Oswald fonts, so there is no font placeholder
to swap). Site-side edits live as override rules at the end of its `<style>`.
Both the served PDF and the thumbnails `assets/fde-p1.webp` … `fde-p3.webp`
(inlined as `FDE_THUMBS`) are rendered from it, so edit the source, then
regenerate both:

1. PDF: headless Chrome `--no-pdf-header-footer --print-to-pdf=…` on the source,
   copy to `site/leigh-anne-miller-fde.pdf`.
2. Thumbnails: for each page N, inject a style that neutralises the source's
   `@media screen` chrome (`html{background:#fff}body{padding:0}.page{margin:0;
   box-shadow:none}`) and hides the other pages with
   `.page:not(:nth-of-type(N)){display:none}`, then screenshot with
   `--window-size=816,1056 --force-device-scale-factor=2` and
   `cwebp -resize 680 0 -q 82`.

The source names the investor platform "DESS · stealth investor network", not
DIN/DAN, and its Case 2 carries bracketed `[tbd]` placeholders until filled.

The Field Record row on page 2 carries a navy tile per entry with a white-out
mark. HP, Nielsen and Google were knocked out of supplied images with Pillow
(`assets/logo-*-w.png`, embedded in the source as data URIs); DIN, DAN, EGON
and the Ripley mark reuse the SVGs already in the source; SpinF is type only.

No PDF rasterizer is installed on the build machine, and sips cannot crop from
a zero offset, so render page by page rather than cropping a strip. Each
`.page` is a fixed 11in with `overflow:hidden`, so anything that overflows
clips the footer: check the render after adding content.

## Index order

Hero · The firm and Track record side by side (`.two-col`) · Current work ·
The principal (thumbnails) · Stack (a striped band of chips from the `STACK` list;
a `(text, True)` entry is the row's red anchor chip) · quotes · Services.

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

**Full runbook: README.md § "Deploying — the runbook".** Four steps —
`python3 build_site.py` → review → commit → `./node_modules/.bin/wrangler deploy`.
Step 1 is not optional: skipping it deploys stale HTML while the diff looks right.
Verify on the RENDERED text, not raw HTML (copy wraps across lines), and allow a
few seconds for the edge cache.
