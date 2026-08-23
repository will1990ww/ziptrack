# Handover Guide — Balcony Master website

A practical, non-technical guide to running and updating the site.

## 1. Preview the site locally
Any static server works. Easiest:
```
cd website
python -m http.server 8000
# open http://localhost:8000
```

## 2. Change business details (phone, WhatsApp, email…)
Open **`js/config.js`** and edit the values. They update across every page automatically:
- `phone` / `phoneDisplay`  — the call link and shown number
- `whatsapp`                — WhatsApp number (digits only, e.g. 6591234567)
- `email`                   — email link
- `formEndpoint`            — leave "" for demo; paste a Formspree/Web3Forms URL to go live
- `gaId`                    — "G-XXXXXXXXXX" to enable Google Analytics 4

## 3. Add / change project photos & videos
Edit **`data/projects.js`**. Three sections (decking, blinds, grilles), 6 slots each
(5 photos + 1 video). For each item:
```js
{ type:"image", src:"assets/images/projects/decking/my-photo.webp",
  title:"Tampines condo", meta:"WPC · 9 m² · 2 days" }
{ type:"video", src:"assets/videos/projects/blinds/my-clip.mp4",
  poster:"assets/images/projects/blinds/my-photo.webp",
  title:"Open/close demo", meta:"Motorised" }
{ type:"empty" }   // shows an "Add photo/video" placeholder
```
Then drop the file into the matching folder and refresh the Projects page.

## 4. Swap product photos / videos on the pricing cards
Keep the **same filenames** and just replace the files:
- Zip blind videos: `assets/videos/blinds/zipblind-manual.mp4`, `-motorised.mp4`, `-smart.mp4`
  (each card shows a poster image `assets/images/blinds/product-*.webp` — replace those too if you like)
- Grille photos: `assets/images/grilles/product-nylon.webp`, `-ptfe.webp`, `-nano.webp`
- Decking photos: `assets/images/decking/product-wpc.webp`, `-chengal.webp`, `-stone.webp`

## 5. Change prices or warranty wording
- Displayed prices live in **`build.py`** (functions `price_panel_*`). Edit, then run `python build.py`.
- `data/prices.json` is the machine-readable record (keep it in sync for your own reference).
- Warranty text is in `build.py` → `page_warranty()`; rebuild after editing.

## 6. Rebuild the site after any `build.py` / data change
```
python build.py
```
This regenerates all 14 HTML pages from the shared header/footer/schema so nothing drifts.

## 7. Go live
1. Fill in `js/config.js`.
2. Replace placeholder media with real photos/videos.
3. In `build.py`, set `SITE` to your real domain, then `python build.py`.
4. Upload the whole `website/` folder to your host.
5. Submit `sitemap.xml` in Google Search Console; create a Google Business Profile.
6. Remove the yellow prototype banner (top of `build.py`, the `proto-banner` div).

## 8. Zip blind warranty (quick reference for staff)
- **5-year** system warranty.
- **1st & 2nd** service visits: **free**.
- **3rd, 4th, 5th** visits: **S$250 labour each** (+ parts).
- **4 weeks** advance notice to schedule a repair.
- Motor follows the motor manufacturer's own warranty.
