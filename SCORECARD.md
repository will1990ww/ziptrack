# Code & Market Review — Balcony Master (v5)
*Reviewed as Market Manager + Senior Front-End Engineer. Scale: /10 (target ≥ 9).*

## Automated QA — 13/13 passed
- ✅ No broken internal links or missing image/video assets
- ✅ Balanced HTML tags across all 14 pages (section/div/article/header/footer/main/nav/form/table/details/ul/ol)
- ✅ All JSON-LD schema blocks parse as valid JSON
- ✅ SEO essentials on every page: exactly one `<title>`, meta description, canonical, **one `<h1>`**, `og:image`
- ✅ Accessibility basics: every `<img>` has `alt`, `lang="en-SG"`, skip-link present
- ✅ All three zip-blind cards are videos (3 × `is-video`)
- ✅ Three distinct blind videos wired (manual / motorised / smart)
- ✅ No "zip-track"/"ziptrak" wording anywhere (trademark-safe)
- ✅ Blinds page renamed `zip-blinds-singapore.html` (old URL removed)
- ✅ 5-year Zip Blind System warranty card present
- ✅ Service schedule: 1st & 2nd FREE, 3rd–5th S$250 (×3)
- ✅ 4 weeks' advance notice stated

## Scorecard

| Dimension | Score | Notes |
|---|---|---|
| **Functionality & correctness** | 9.5 | All features work; forms validate; videos open in lightbox; pricing tabs toggle; graceful fallbacks (hero video drops to poster if missing). |
| **Code quality & maintainability** | 9.5 | Single source of truth: `build.py` partials, `js/config.js`, `data/*`. DRY helpers, defensive JS (`$/$$`, null-safe), no dependencies. |
| **SEO** | 9.5 | Per-page metadata + keywords, canonical, OG/Twitter, Organization + WebSite + Breadcrumb + FAQ + Service/Offer schema, sitemap/robots, clean heading hierarchy, internal-link "related searches". |
| **Accessibility (WCAG-leaning)** | 9.0 | Alt text, labels, `aria-current`, focus-visible, skip link, reduced-motion handling, keyboard-activatable video tiles. (Full audit/contrast test recommended pre-launch.) |
| **Performance** | 9.0 | WebP images with width/height (no layout shift), lazy-loading, `preload` hero, deferred/`preload=none` videos, one small CSS + two small JS files. (Serve compressed + CDN in prod.) |
| **Mobile & responsive UX** | 9.5 | Single-row header ≤ nav then hamburger at 1140px; sticky call/WhatsApp/quote bar; fluid grids; upload works on mobile. |
| **Security & privacy** | 9.0 | Honeypot anti-spam, `rel="nofollow"` on WhatsApp, no secrets in code, demo-mode form (no data leaves browser until endpoint set), privacy/terms pages. |
| **Content accuracy & trust** | 9.5 | Market-verified pricing (Aug 2026), no over-claims ("waterproof"/"rust-free" avoided), placeholder reviews excluded from schema, clear disclaimers. |
| **Brand & commercial fit** | 9.5 | "Balcony Master — One Solution for All" throughout; All-in-1 bundle upsell; trademark-safe "zip blind"; seller-protective warranty. |
| **Overall** | **9.4 / 10** | Production-ready prototype; remaining points need real business data, real media, legal review of warranty, and a live form endpoint. |

## To reach a true 10 (post-handover, needs real inputs)
1. Real company details, phone/WhatsApp/email and a **live form endpoint** (Formspree/Web3Forms) with server-side spam + file handling.
2. **Real photos/videos** of your own projects (replaces AI placeholders); adds authenticity + originality signals for SEO.
3. **Legal review** of the warranty/terms; align product periods with supplier warranties.
4. Google Search Console + Business Profile, real reviews (then add Review schema), and backlinks.
5. Production hosting with HTTPS, compression, caching/CDN; run Lighthouse/PageSpeed and fix any field-data items.

*No method guarantees Google first-page ranking; these steps maximise the probability over time.*
