# Balcony Master — lionsin.com.sg (v9, review-finalised)

Four products: **balcony decking · zip blinds · invisible grilles · retractable roof**.
Domain https://www.lionsin.com.sg · Phone/WhatsApp +65 8341 7888 · Email bimprosg@outlook.com.

## Senior-review action plan — implemented (30/30 automated checks pass)
- **P1** `rel="nofollow noopener noreferrer"` on all new-tab links.
- **P4/5 Claims tightened & trademark-safe:** removed "child fall-protection", "pet-friendly",
  "100% retractable", "Real Singapore projects", "Somfy + Serge Ferrari" hard claims and
  "Strongest warranty scope". Cable-spacing described physically (not as a safety guarantee).
  "Teflon" → **PTFE** (Teflon™ noted nominatively). Zip/roof FAQs use defensible wording
  ("side-retained outdoor blinds", "vary by supplier … not affiliated").
- **P6** Removed the obsolete `<meta name="keywords">` from every page.
- **P7** Homepage canonical & `og:url` now the **root** `https://www.lionsin.com.sg/`; home links use `./`.
  (Add a server rule `/index.html → /` on your host for one clean URL.)
- **P8** Added a purpose-made **1200×630 social image** (`assets/images/social/og-home.jpg`) with
  `og:image:alt` and `twitter:image:alt`.
- **P9** Heading hierarchy fixed — project/feature/step titles are `<h3>`; footer uses a
  visually-hidden `<h2>` + `<h3>` columns (appearance via CSS, not heading level).
- **P10** Product/gallery images have descriptive `alt` text (not keyword stuffing).
- **P11** Form: JS toggles `aria-invalid`, builds an **error summary with links to each invalid field**,
  moves focus, and shows a dedicated **consent error**; values are preserved on failure.
- **P12** Enquiry fields wrapped in a `<fieldset>` with a visually-hidden `<legend>`.
- **P13** Hero video is deferred (idle/`load`), skipped for reduced-motion **and Save-Data**, and
  paused when off-screen or the tab is hidden.
- **P14** `config.js` and `main.js` load with **`defer`** (order preserved).
- **P15** Google Fonts reduced (Cormorant 600/700; Inter 400/500/600/700) with `display=swap`.
- **P16** Homepage is shorter — a compact **"from" price grid** + "Compare all packages" button;
  the full 4-tab pricing lives on the service pages and price-guide.
- **P20** JSON-LD consolidated into a single **`@graph`** per page (Organization, WebSite, WebPage,
  BreadcrumbList, and page FAQ/Service) so structured data and visible content stay in sync.

## Warranty — seller-protective (see warranty.html + terms.html)
Adds an explicit **limitation of liability** (capped at the price paid for the affected product),
**"repair or replace at our option is your sole and exclusive remedy"**, warranties **do not restart**
after a repair, an **entire-agreement** clause (marketing statements don't add to it), a clause that
**product descriptions are not a safety guarantee**, and expanded exclusions (misuse, wind above
stated limits, third-party work, structural/waterproofing, consequential loss). Nothing excludes
non-excludable statutory rights.

## Form & privacy
Form posts to **FormSubmit → bimprosg@outlook.com** (multipart, honeypot). The Privacy Notice now
**names FormSubmit**, explains that processing may occur **outside Singapore**, notes sensitive files
and offers a WhatsApp alternative. The UI shows **no hard file limits** (server must enforce those).

## Still owner-side before you rely on it (per reviewer)
1. Confirm every price & warranty period against your suppliers/policy.
2. Replace representative photos/videos with your own authorised project media.
3. Configure server-side upload validation (type/size/count/scan) and, if you keep FormSubmit,
   confirm its retention/security suits you; otherwise move to a server endpoint.
4. Add security headers/CSP, uptime & form monitoring after launch.
5. Activate the form once (click the FormSubmit confirmation email).

## Deploy / analytics
GitHub Pages: upload folder contents; `CNAME` + `.nojekyll` included. Search Console → submit
`sitemap.xml`. GA4: set `gaId` in `js/config.js` (events: generate_lead, quote_cta_click,
contact_call/whatsapp/email, video_play, pricing_tab).

## Pages
/ (index) · balcony-decking-singapore · zip-blinds-singapore · invisible-grille-singapore ·
retractable-roof-singapore · complete-balcony-solution · projects · price-guide · warranty ·
about · contact · privacy · terms · thank-you · 404
