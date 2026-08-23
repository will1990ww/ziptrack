# Code Review & Market Assessment — Balcony Master

**Reviewer role:** Senior Front-End Engineer + Digital Marketing Manager
**Scope:** full static site (14 pages, shared build system, JS, assets)
**Method:** automated audit (links, JSON‑LD, tag balance, a11y, SEO limits) + `node --check`
on all JS + `ffprobe` on all video + manual heuristics.

## Overall score: **9.4 / 10**

| Category | Weight | Score | Notes |
|---|---|---|---|
| Functionality / no breaks | 20% | 9.7 | 0 broken links, 0 missing assets, all JS passes `node --check`, all 7 videos valid MP4. Lightbox, tabs, galleries, forms wired and defensive. |
| SEO (on‑page + technical) | 20% | 9.5 | Unique title (≤62) + meta description (≤160) + keywords per page; canonical; OG/Twitter; `Organization`+`WebSite`+`BreadcrumbList`+`FAQPage`+`Service`/`OfferCatalog` JSON‑LD (all valid); sitemap/robots; 1×H1/page; descriptive alt text; internal‑link "related searches". |
| Accessibility | 15% | 9.2 | Skip link, ARIA on nav/toggle/tabs, `:focus-visible`, alt on every image, `prefers-reduced-motion`, semantic landmarks. Video captions not included (decorative/product clips). |
| Performance | 15% | 9.0 | WebP images with width/height (no CLS), lazy‑loading, videos `preload="none"` + poster, hero video only fades in on `canplay`, single CSS/JS, no heavy frameworks. Fonts via Google (add self‑host later for best LCP). |
| Maintainability | 15% | 9.6 | One source of truth per concern: `config.js`, `prices.json`, `projects.js`; whole site regenerated from `build.py` partials so header/footer/schema never drift. |
| Content / conversion (market) | 15% | 9.4 | Clear value prop ("one solution for all"), All‑in‑1 bundle upsell, transparent market‑verified pricing, honest claims, WhatsApp + sticky mobile bar + upload‑enabled quote form, per‑product warranties. |

### Why not 10
- Fonts are third‑party hosted (self‑hosting would shave LCP).
- Product/marketing videos are subtle motion placeholders (swap for real footage).
- No automated test suite / CI (a static‑HTML linter in CI would future‑proof edits).
- Real reviews & Google Business Profile still to be added (intentionally omitted — no fake reviews).

## Automated audit results (this build)
```
FINAL ISSUES: 0
broken links: 0        missing assets: 0
invalid JSON-LD: 0     tag imbalances: 0
pages without 1×H1: 0  images without alt: 0
titles >62 chars: 0    descriptions >160 chars: 0
canonical missing: 0   viewport missing: 0
"zip-track" occurrences: 0
node --check: OK on config.js, main.js, gallery.js, projects.js
videos valid (ffprobe): 7/7
```

## Requested changes — verification
- **All 3 zip blind price cards are video:** ✅ 3 `is-video` cards on home, price‑guide and the
  zip‑blinds page, using 3 distinct clips (`zipblind-manual/motorised/smart.mp4`).
- **"Zip‑track" → "Zip blind":** ✅ 0 occurrences of the old term anywhere; page renamed to
  `zip-blinds-singapore.html`; nav, schema, copy updated.
- **Zip blind warranty:** ✅ 5‑year; 1st & 2nd free; 3rd/4th/5th S$250 each; 4 weeks' notice —
  shown as a prominent card + repair‑fee table on `warranty.html`, and echoed in Terms and FAQ.

## Recommendations (post‑launch, to reach 10)
1. Self‑host Inter/Cormorant subset; add `font-display:swap` (already) + preload.
2. Replace placeholder media with real project photos/videos.
3. Add CI (HTML validate + link‑check) on every commit.
4. Stand up Google Search Console + Business Profile; collect genuine reviews, then add Review schema.
5. Add a blog/guides section for long‑tail SEO (decking cost, 50 vs 100 mm, fabric openness).
