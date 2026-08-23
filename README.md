# Balcony Master — "One Solution for All"

Structured, mobile-first, SEO-optimised website for a Singapore balcony specialist coordinating
**outdoor decking, zip blinds and invisible grilles**.

## What changed in this version (v5)
1. **All three Zip Blind price cards are product VIDEOS** (manual / motorised / premium-smart),
   each with a ▶ overlay + "Video" tag; clicking opens a lightbox. Files:
   `assets/videos/blinds/zipblind-manual.mp4`, `zipblind-motorised.mp4`, `zipblind-smart.mp4`.
2. **"Zip-track" wording removed site-wide → "Zip blind"** (trademark-safe; *Ziptrak®* is a
   third-party brand). The service page URL is now **`zip-blinds-singapore.html`** and the nav label is **Zip Blinds**.
3. **New 5-year Zip Blind System warranty** with a service schedule:
   **1st & 2nd visits FREE**, **3rd/4th/5th visits S$250 labour each**, and **≥4 weeks' advance notice**
   required to schedule any repair. Shown as a highlighted card + in the general terms + Terms page.
4. **Senior-engineer QA pass** — see `SCORECARD.md`. Automated checks: **13/13 pass**
   (no broken links, balanced tags, valid JSON-LD, SEO essentials, a11y basics, all feature checks).

## Manage media (no coding)
- **Zip blind card videos:** replace the 3 files in `assets/videos/blinds/` (same names).
- **Project galleries:** edit `data/projects.js` (3 categories × 6 slots = 5 photos + 1 video).
  Drop files into `assets/images/projects/<cat>/` or `assets/videos/projects/<cat>/`.
- **Grille product photos (vertical):** `assets/images/grilles/product-{nylon,ptfe,nano}.webp`
- **Decking product photos:** `assets/images/decking/product-{wpc,chengal,stone}.webp`
Keep filenames the same and the site picks them up automatically.

## SEO (all pages)
Unique title + meta description + keywords, canonical, full Open Graph/Twitter with per-page image,
`robots max-image-preview:large`, geo tags. Structured data: `Organization`+`WebSite` on every page,
`BreadcrumbList` on inner pages, `FAQPage` where FAQs show, and `Service`+`OfferCatalog` (per-tier
prices) on each service page. One H1 per page, descriptive alt text, `sitemap.xml`, `robots.txt`, 404.
> On-page SEO improves crawling/understanding; no method guarantees Google's #1 or first page.

## Pricing (market-verified Aug 2026 — reasonable, unchanged)
| Service | Planning range |
|---|---|
| Decking — WPC / Chengal / marble-tiles-stone | S$18–45+/ft² |
| Zip blinds — manual / motorised / smart | S$18–45+/ft² |
| Invisible grilles — Nylon / PTFE / Nano | from S$8 / 10 / 16 /ft² |

## File structure
```
website/
├── index.html + 13 more pages (zip-blinds-singapore.html is the blinds page)
├── css/styles.css
├── js/config.js     ← EDIT: business details (phone, WhatsApp, email, GA4, form endpoint)
├── js/main.js       nav, forms, uploads, pricing tabs, hero video, product-video, lightbox, GA
├── js/gallery.js    renders the 3 project galleries
├── data/projects.js ← EDIT: your photos/videos (6 per section)
├── data/prices.json pricing source of truth
├── assets/images/… and assets/videos/… (incl. 3 zip-blind videos)
├── robots.txt  sitemap.xml  site.webmanifest
├── build.py         regenerates all HTML from shared partials
├── SCORECARD.md     senior-engineer / market-manager QA grade
└── README.md
```

## Go-live checklist
1. `js/config.js` — real name, UEN, phone, WhatsApp, email, form endpoint, GA4 ID.
2. Replace placeholder photos/videos with real, customer-approved media.
3. Have the **warranty terms reviewed by a qualified adviser** (they are seller-protective templates).
4. Replace `https://www.example.sg` in `build.py`, rebuild (`python build.py`).
5. Submit `sitemap.xml` in Google Search Console; set up Google Business Profile; remove the prototype banner.
