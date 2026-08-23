#!/usr/bin/env python3
"""
Static site assembler — Balcony Master ("One Solution for All").
v5 changes:
  * All three zip-blind price cards are product videos.
  * "Zip-track" wording replaced with "Zip blind" site-wide (trademark-safe).
  * Detailed 5-year zip-blind system warranty (service schedule + advance notice).
  * Senior-engineer pass: valid JSON-LD, a11y labels, no dead sections.
Run:  python build.py
"""
import os, datetime, html, json

OUT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.example.sg"   # TODO: real domain before launch
BRAND = "Balcony Master"
TAGLINE = "One Solution for All"

NAV = [
    ("Decking", "outdoor-decking-singapore.html"),
    ("Zip Blinds", "zip-blinds-singapore.html"),
    ("Invisible Grilles", "invisible-grille-singapore.html"),
    ("All-in-1", "complete-balcony-solution.html"),
    ("Projects", "projects.html"),
    ("Pricing", "price-guide.html"),
    ("Warranty", "warranty.html"),
]
def nav_links(active):
    return "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h==active else ""}>{l}</a></li>' for l, h in NAV)
def mobile_links(active):
    return "".join(f'<a href="{h}"{" aria-current=\"page\"" if h==active else ""}>{l}</a>' for l, h in NAV) + \
        '<a href="about.html">About</a><a href="contact.html" class="mm-cta">Get a quote →</a>'

CHECK = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>'
ARROW = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
PHONE_SVG = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
PLAY_SM = '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>'
BRAND_LOGO = f'<a href="index.html" class="brand" aria-label="{BRAND} — {TAGLINE}"><span class="mark" aria-hidden="true">BM</span><span class="bt"><b>{BRAND}</b><span>{TAGLINE}</span></span></a>'

def global_ld():
    org = {
        "@context":"https://schema.org","@type":"HomeAndConstructionBusiness",
        "@id":f"{SITE}/#business","name":BRAND,"alternateName":"Balcony Master Singapore",
        "slogan":TAGLINE,"url":f"{SITE}/","image":f"{SITE}/assets/images/hero-poster.webp",
        "logo":f"{SITE}/assets/images/hero-poster.webp","telephone":"+65-8000-0000",
        "email":"hello@balconymaster.sg","priceRange":"$$",
        "areaServed":{"@type":"Country","name":"Singapore"},
        "address":{"@type":"PostalAddress","addressLocality":"Singapore","addressCountry":"SG"},
        "description":"Singapore balcony specialist — one solution for outdoor decking, zip blinds and invisible grilles. Supply and installation for HDB, condo and landed homes.",
        "knowsAbout":["outdoor decking Singapore","composite decking","Chengal decking","zip blinds","motorised outdoor blinds","invisible grille","balcony safety grille","invisible grille price Singapore"],
        "makesOffer":[
            {"@type":"Offer","itemOffered":{"@type":"Service","name":"Outdoor decking supply and installation"}},
            {"@type":"Offer","itemOffered":{"@type":"Service","name":"Zip blind supply and installation"}},
            {"@type":"Offer","itemOffered":{"@type":"Service","name":"Invisible grille supply and installation"}}
        ],
        "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"09:00","closes":"18:00"}]
    }
    website = {"@context":"https://schema.org","@type":"WebSite","@id":f"{SITE}/#website",
               "url":f"{SITE}/","name":BRAND,"publisher":{"@id":f"{SITE}/#business"},"inLanguage":"en-SG"}
    return (f'<script type="application/ld+json">{json.dumps(org)}</script>'
            f'<script type="application/ld+json">{json.dumps(website)}</script>')

def head(title, desc, path, keywords="", og_image="assets/images/hero-poster.webp", extra_ld="", active=""):
    canonical = f"{SITE}/{path}"
    kw = f'<meta name="keywords" content="{html.escape(keywords)}">' if keywords else ""
    return f'''<!DOCTYPE html>
<html lang="en-SG"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{kw}
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#1E4D3B">
<meta name="geo.region" content="SG"><meta name="geo.placename" content="Singapore">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE}/{og_image}"><meta property="og:locale" content="en_SG">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}"><meta name="twitter:image" content="{SITE}/{og_image}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="image" href="{og_image}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="css/styles.css">
<link rel="manifest" href="site.webmanifest">
<script src="js/config.js"></script>
{global_ld()}
{extra_ld}
</head><body>
<a href="#main" class="skip-link">Skip to content</a>
<div class="proto-banner">Prototype preview — business details, prices, product claims &amp; reviews are placeholders pending verification.</div>
<header class="site-header">
  <div class="container nav">
    {BRAND_LOGO}
    <nav aria-label="Primary"><ul class="nav-links">{nav_links(active)}</ul></nav>
    <div class="nav-cta">
      <a class="nav-phone" data-tel href="#">{PHONE_SVG}<span data-phone-text>+65 8000 0000</span></a>
      <a href="contact.html" class="btn btn-primary">Get a quote</a>
      <button class="menu-toggle" id="menuToggle" aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      </button>
    </div>
  </div>
  <div class="container mobile-menu" id="mobileMenu">{mobile_links(active)}</div>
</header>
<main id="main">'''

def breadcrumb(trail):
    parts, ld_items = [], []
    for i, (label, href) in enumerate(trail):
        if href:
            parts.append(f'<a href="{href}">{label}</a>'); url = f"{SITE}/{href}"
        else:
            parts.append(f'<span aria-current="page" style="color:var(--green-900);font-weight:600">{label}</span>'); url = None
        item = {"@type":"ListItem","position":i+1,"name":label}
        if url: item["item"] = url
        ld_items.append(item)
    crumbs = '<span>›</span>'.join(parts)
    ld = '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":ld_items}) + '</script>'
    return f'<nav class="breadcrumbs container" aria-label="Breadcrumb">{crumbs}</nav>{ld}'

def footer(extra_js=""):
    return f'''</main>
<footer class="site-footer"><div class="container">
  <div class="footer-grid">
    <div class="footer-brand">{BRAND_LOGO}
      <p>Singapore's balcony specialist — one solution for flooring, weather control and safety, coordinated under one roof.</p></div>
    <div class="footer-col"><h5>Services</h5><ul>
      <li><a href="outdoor-decking-singapore.html">Outdoor decking</a></li>
      <li><a href="zip-blinds-singapore.html">Zip blinds</a></li>
      <li><a href="invisible-grille-singapore.html">Invisible grilles</a></li>
      <li><a href="complete-balcony-solution.html">All-in-1 bundle</a></li></ul></div>
    <div class="footer-col"><h5>Explore</h5><ul>
      <li><a href="price-guide.html">Price guide</a></li>
      <li><a href="projects.html">Projects</a></li>
      <li><a href="warranty.html">Warranty</a></li>
      <li><a href="about.html">About</a></li></ul></div>
    <div class="footer-col"><h5>Get in touch</h5><ul>
      <li><a data-tel href="#"><span data-phone-text>+65 8000 0000</span></a></li>
      <li><a data-wa href="#">WhatsApp us</a></li>
      <li><a data-email href="#">Email us</a></li>
      <li><a href="contact.html">Book a site survey</a></li>
      <li><a href="privacy.html">Privacy</a> · <a href="terms.html">Terms</a></li></ul></div>
  </div>
  <div class="footer-bottom">
    <span>© <span data-year>2026</span> <span data-site="legalName">{BRAND}</span>. All rights reserved.</span>
    <span>Prices are indicative planning ranges. Final pricing follows a measured site survey. GST may apply.</span>
  </div>
</div></footer>
<div class="mobile-bar">
  <a data-tel href="#" class="call">📞<span>Call</span></a>
  <a data-wa href="#" class="wa">💬<span>WhatsApp</span></a>
  <a href="contact.html" class="quote">✏️<span>Get quote</span></a>
</div>
<script src="js/main.js"></script>
{extra_js}
</body></html>'''

def upload_field():
    return ('<div class="field"><label>Floor plan or balcony photos <span style="font-weight:400;color:var(--muted)">(optional)</span></label>'
            '<label class="upload"><input type="file" name="attachments" accept="image/*,.pdf" multiple>'
            '<span class="u-ic" aria-hidden="true">📎</span><b>Tap to upload your floor plan or balcony photos</b>'
            '<span>JPG, PNG or PDF · you can add a few files</span><div class="u-files"></div></label></div>')

def quote_form_inner(service="", with_name=False):
    name_field = ('<div class="field"><label for="qf-name">Name <span class="req">*</span></label>'
                  '<input id="qf-name" name="name" type="text" autocomplete="name" required><span class="err">Please enter your name.</span></div>') if with_name else ""
    return f'''<form data-quote-form novalidate>
      <h3>Tell us the basics</h3><p class="sub">Add your floor plan or balcony photos for a faster, more accurate quote.</p>
      <div class="form-error-summary" role="alert"></div>
      <div class="honeypot" aria-hidden="true"><label>Company website<input type="text" name="company_website" tabindex="-1" autocomplete="off"></label></div>
      <input type="hidden" name="service_preselect" value="{service}"><input type="hidden" name="product" value="">
      <div class="field-row">
        <div class="field"><label for="qf-prop">Property type <span class="req">*</span></label>
          <select id="qf-prop" name="property" required><option value="" disabled selected>Select…</option><option>Condominium</option><option>Landed</option><option>HDB</option><option>Commercial</option></select><span class="err">Please select a property type.</span></div>
        <div class="field"><label for="qf-svc">Service needed</label>
          <select id="qf-svc" name="service"><option value="" disabled selected>Select…</option><option>Decking</option><option>Zip blinds</option><option>Invisible grilles</option><option>All three</option></select></div>
      </div>
      {name_field}
      <div class="field"><label for="qf-mob">Mobile number <span class="req">*</span></label>
        <input id="qf-mob" name="mobile" type="tel" placeholder="+65 8XXX XXXX" autocomplete="tel" required><span class="err">Please enter a valid mobile number.</span></div>
      {upload_field()}
      <label class="checkbox"><input type="checkbox" name="consent" required> I agree to be contacted and to the storing of these details per the <a href="privacy.html" style="color:var(--green);text-decoration:underline">Privacy Notice</a>. <span class="req">*</span></label>
      <button type="submit" class="btn btn-primary btn-block">Request my quote</button>
      <p class="form-note">Demo mode — files stay in your browser until a secure endpoint is set in <code>js/config.js</code>.</p>
    </form>
    <div class="form-success"><div class="check">{CHECK}</div><h3 style="color:var(--green-900)">Thank you — request received</h3>
      <p class="sub" style="margin-top:.5rem">We'll reach out within one business day to arrange your free site survey.</p>
      <a data-wa class="btn btn-primary" style="margin-top:.5rem">Send photos on WhatsApp</a></div>'''

def sticky_quote_form(service=""):
    return f'''<section id="quote" class="quote section"><div class="container quote-grid">
  <div class="quote-copy reveal">
    <span class="eyebrow">Start your project</span>
    <h2 class="section-title" style="color:#fff">Request a measured, itemised quote</h2>
    <p>Share a few details — and upload your floor plan or balcony photos — to begin. We'll arrange a free site survey and prepare an itemised quotation, no obligation.</p>
    <ul><li>Free site survey &amp; measurement</li><li>Honest recommendation for your property</li><li>Transparent, itemised pricing with GST stated</li></ul>
  </div>
  <div class="form-card reveal">{quote_form_inner(service)}</div>
</div></section>'''

def write(path, title, desc, body, trail=None, keywords="", og_image="assets/images/hero-poster.webp", extra_ld="", extra_js="", active=""):
    crumb = breadcrumb(trail) if trail else ""
    doc = head(title, desc, path, keywords, og_image, extra_ld, active) + crumb + body + footer(extra_js)
    with open(os.path.join(OUT, path), "w", encoding="utf-8") as f: f.write(doc)
    print("wrote", path, f"({len(doc)} bytes)")

def faq_ld_json(qas):
    data = {"@context":"https://schema.org","@type":"FAQPage",
            "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qas]}
    return '<script type="application/ld+json">' + json.dumps(data) + '</script>'
def service_ld(name, desc, offers, url):
    data = {"@context":"https://schema.org","@type":"Service","serviceType":name,
            "provider":{"@id":f"{SITE}/#business"},"areaServed":"Singapore","url":f"{SITE}/{url}","description":desc,
            "hasOfferCatalog":{"@type":"OfferCatalog","name":name,"itemListElement":[
                {"@type":"Offer","name":n,"priceCurrency":"SGD","price":p,
                 "priceSpecification":{"@type":"UnitPriceSpecification","price":p,"priceCurrency":"SGD","unitText":"per square foot"}} for n,p in offers]}}
    return '<script type="application/ld+json">' + json.dumps(data) + '</script>'
def faq_section(qas):
    items = ""
    for i, (q, a) in enumerate(qas):
        items += f'<details class="qa"{" open" if i==0 else ""}><summary>{q}<span class="plus" aria-hidden="true"></span></summary><div class="ans">{a}</div></details>'
    return f'<section class="section alt"><div class="container"><span class="eyebrow reveal">Common questions</span><h2 class="section-title reveal">Answers before you commit</h2><div class="faq reveal mt-2">{items}</div></div></section>'
def table(headers, rows):
    thead = "".join(f"<th scope=\"col\">{h}</th>" for h in headers)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="spec"><thead><tr>{thead}</tr></thead><tbody>{trs}</tbody></table>'
def plain(t):
    import re
    return re.sub("<[^>]+>", "", t).replace("&amp;", "&")

def related_block(title, links):
    chips = "".join(f'<a href="{h}">{l}</a>' for l, h in links)
    return (f'<section class="section"><div class="container"><span class="eyebrow reveal">{title}</span>'
            f'<div class="reveal" style="display:flex;flex-wrap:wrap;gap:.6rem;margin-top:1rem">{chips}</div></div></section>')

# ---------- price card: photo OR video ----------
def price_card(name, amount_html, who, bullets, cta_href, featured=False, ribbon=None,
               photo=None, badge=None, video=None, poster=None):
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    rib = f'<span class="ribbon">{ribbon}</span>' if ribbon else ""
    btn = "btn-primary" if featured else "btn-ghost"
    media_html = ""
    if video:
        b = f'<span class="pc-badge">{badge}</span>' if badge else ""
        media_html = (f'<div class="pc-photo is-video" data-video-box data-src="{video}" data-poster="{poster}">'
                      f'<img src="{poster}" width="900" height="640" alt="{name} — product video" loading="lazy">{b}'
                      f'<span class="pc-vtag">▶ Video</span>'
                      f'<button class="pc-play" aria-label="Play {name} video"><span>{PLAY_SM}</span></button></div>')
    elif photo:
        b = f'<span class="pc-badge">{badge}</span>' if badge else ""
        media_html = f'<div class="pc-photo"><img src="{photo}" width="900" height="640" alt="{name}" loading="lazy">{b}</div>'
    return (f'<div class="price-card {"featured" if featured else ""} reveal">{media_html}'
            f'<div class="pc-body">{rib}<h3>{name}</h3><p class="who">{who}</p><div class="amt">{amount_html}</div>'
            f'<ul>{lis}</ul><a href="{cta_href}" class="btn {btn}">Plan this</a></div></div>')

def price_panel_decking():
    cards = (
        price_card("Entry composite / WPC", 'S$18–23<small>per ft² supply &amp; install</small>', "Price-conscious, straightforward installs",
                   ["Entry-grade capped WPC","Standard colours &amp; detailing","Standard corrosion-resistant fixings"], "contact.html?service=decking&tier=essential",
                   photo="assets/images/decking/product-wpc.webp", badge="Value") +
        price_card("Mid-range capped WPC", 'S$24–32<small>per ft² supply &amp; install</small>', "Most homeowners seeking durability &amp; value",
                   ["Upgraded capped WPC &amp; finish","Concealed / upgraded fixings","Better edge &amp; drainage detailing"], "contact.html?service=decking&tier=performance", featured=True, ribbon="Popular",
                   photo="assets/images/decking/product-chengal.webp", badge="Popular") +
        price_card("Premium / marble, tiles &amp; stone", 'S$33–45+<small>per ft² supply &amp; install</small>', "Design-led, hardwood or stone finishes",
                   ["Premium boards, Chengal, marble, tiles or stone","Aluminium subframe, complex edges &amp; steps","Upgraded hardware"], "contact.html?service=decking&tier=premium",
                   photo="assets/images/decking/product-stone.webp", badge="Premium")
    )
    return (f'<div data-price-panel="decking"><h3 style="font-family:var(--sans);margin:1.6rem 0 .3rem">Decking planning packages</h3>'
            f'<div class="grid price-grid">{cards}</div>'
            f'<p class="lead" style="margin-top:1rem;font-size:.9rem">Complex raised decks, steps, aluminium subframes, difficult access or marble/tile/stone finishes are priced after survey.</p></div>')

def price_panel_blinds():
    # ALL THREE cards are product videos
    cards = (
        price_card("Manual zip blind", 'S$18–28<small>per ft² supply &amp; install</small>', "Simple, reliable, budget-friendly",
                   ["Manual zip-lock operation","Solar-mesh fabric options","Standard track colours"], "contact.html?service=blinds&tier=manual",
                   video="assets/videos/blinds/zipblind-manual.mp4", poster="assets/images/blinds/product-manual.webp", badge="Value") +
        price_card("Motorised zip blind", 'S$25–35<small>per ft² supply &amp; install</small>', "Convenient daily use",
                   ["Tubular motor &amp; remote","Solar-mesh or denser fabric","Electrical point coordinated"], "contact.html?service=blinds&tier=motorised", featured=True, ribbon="Popular",
                   video="assets/videos/blinds/zipblind-motorised.mp4", poster="assets/images/blinds/product-motorised.webp", badge="Popular") +
        price_card("Premium / smart zip blind", 'S$30–45+<small>per ft² supply &amp; install</small>', "Branded systems, app &amp; voice control",
                   ["Premium branded system","Smart-home / app control","Premium fabric options"], "contact.html?service=blinds&tier=premium",
                   video="assets/videos/blinds/zipblind-smart.mp4", poster="assets/images/blinds/product-smart.webp", badge="Premium")
    )
    return (f'<div data-price-panel="blinds" hidden style="display:none"><h3 style="font-family:var(--sans);margin:1.6rem 0 .3rem">Zip blind planning packages</h3>'
            f'<div class="grid price-grid">{cards}</div>'
            f'<p class="lead" style="margin-top:1rem;font-size:.9rem">Tap ▶ on any card to watch that zip blind in action. Every zip blind system carries our <a href="warranty.html" style="color:var(--green);text-decoration:underline">5-year warranty</a>. Whole-project examples: small single-panel manual ≈ S$800–1,200; standard manual condo balcony ≈ S$1,200–2,000; comparable motorised ≈ S$1,800–2,800. Minimum panel size (~30–32 ft²) and electrical work quoted separately. Swap the clips anytime — drop <code>.mp4</code> files into <code>assets/videos/blinds/</code>.</p></div>')

def price_panel_grilles():
    cards = (
        price_card("Nylon fixed grille", 'from S$8<small>per ft² · 3-year warranty</small>', "Indoor-facing balconies, value option",
                   ["Stainless-steel core, nylon coating","Vertical cables · 50 mm or 100 mm","Physical sample provided"], "contact.html?service=grilles&product=nylon",
                   photo="assets/images/grilles/product-nylon.webp", badge="Entry") +
        price_card("PTFE / Teflon fixed grille", 'from S$10<small>per ft² · 5-year warranty</small>', "Most homes &amp; higher floors",
                   ["Non-stick, UV-stable Teflon coating","Vertical cables · 50 mm or 100 mm","Physical sample provided"], "contact.html?service=grilles&product=ptfe", featured=True, ribbon="Popular",
                   photo="assets/images/grilles/product-ptfe.webp", badge="Most popular") +
        price_card("Nano all-weather grille", 'from S$16<small>per ft² · 10-year warranty</small>', "Exposed / coastal balconies (premium)",
                   ["Premium coating — supplier data on request","Vertical cables · 50 mm or 100 mm","Strongest warranty scope"], "contact.html?service=grilles&product=nano",
                   photo="assets/images/grilles/product-nano.webp", badge="Top tier")
    )
    return (f'<div data-price-panel="grilles" hidden style="display:none"><h3 style="font-family:var(--sans);margin:1.6rem 0 .3rem">Invisible-grille systems</h3>'
            f'<div class="grid price-grid">{cards}</div>'
            f'<p class="lead" style="margin-top:1rem;font-size:.9rem">The three product photos above are stored in <code>assets/images/grilles/</code> — swap them anytime. Openable grilles, 50 mm spacing surcharge and minimum-order value confirmed after measurement.</p></div>')

def bundle_banner():
    return f'''<div class="bundle reveal">
      <div>
        <span class="b-tag">★ All-in-1 · One Solution for All</span>
        <h3>Do all three together and save</h3>
        <p>Book decking, zip blinds and invisible grilles as one project and we pass on the efficiency: one site survey, one schedule, one coordinated team and one warranty conversation — at a better combined price than three separate contractors.</p>
        <ul class="b-list">
          <li>Single itemised quote across all three services</li>
          <li>Details that align — deck height, blind tracks &amp; grille anchors planned together</li>
          <li>One accountable team from survey to handover</li>
        </ul>
      </div>
      <div class="b-cta">
        <div class="b-save">Save up to 10%*</div>
        <a href="contact.html?service=all" class="btn btn-gold">Get my All-in-1 quote</a>
        <a href="complete-balcony-solution.html" class="btn btn-light">How it works</a>
      </div>
    </div>
    <p class="lead" style="font-size:.82rem;margin-top:.6rem">*Indicative combined saving versus commissioning the three services separately; confirmed in your itemised quotation after a free site survey.</p>'''

def read_rates_note():
    return ('<div class="price-note reveal"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 8h.01M11 12h1v4h1"/></svg>'
            '<span><strong>How to read these rates:</strong> figures are indicative supply-and-install planning ranges above the minimum order size, verified against current Singapore market references (Aug 2026). Subframe upgrades, electrical work, restricted access, complex shapes and GST may be additional. Confirmed at your free site survey.</span></div>')

def trust_section():
    items = [("Written warranties","Separate product, workmanship and manufacturer coverage — defined scope and claim process."),
             ("Real specifications","Product systems, coatings, spacing and fixings published — not vague claims."),
             ("Condo approval help","Guidance on MCST approved colours, working hours and paperwork."),
             ("Itemised quotes","Inclusions, exclusions and GST stated up front — no surprises.")]
    cards = "".join(f'<div class="feature-item reveal"><div class="ic">{CHECK}</div><h4>{t}</h4><p>{d}</p></div>' for t, d in items)
    return f'<section class="section"><div class="container"><span class="eyebrow reveal">Why homeowners choose us</span><h2 class="section-title reveal">Specified properly. Installed carefully. Supported after.</h2><div class="grid feature-grid mt-2">{cards}</div></div></section>'

FAQ_5010 = ("What's the difference between 50 mm and 100 mm spacing?",
            "Both are available on all our vertical-cable grille systems. <strong>50 mm</strong> places the cables closer together for a denser barrier — the spacing many households choose to be <strong>pet-friendly</strong> for cats and small dogs — and it costs a little more. <strong>100 mm</strong> is more widely spaced with a lighter, more open look, commonly chosen for <strong>child fall-protection</strong> on balconies. We confirm the right spacing for your household at the survey rather than making blanket safety claims.")
FAQ_MCST = ("Do you help with condo (MCST) approval?",
            "Yes. We provide guidance on approved colours, working-hour restrictions and the documentation your management usually requests. Note that many condominiums also require a <strong>renovation/management deposit paid by the home owner</strong> to the managing agent (MA) or MCST before work starts — typically refunded by the MA after their inspection. We help prepare the submission, but the <strong>MA deposit is arranged directly by the home owner</strong>.")
FAQ_ZIPWARR = ("What does the zip blind warranty cover?",
            "Our zip blind systems carry a <strong>5-year warranty</strong>. Servicing within the warranty is <strong>free for the 1st and 2nd visits</strong>; the <strong>3rd, 4th and 5th visits carry a labour charge of S$250 each</strong>. Please give at least <strong>4 weeks' advance notice</strong> for repair/service scheduling. See the <a href='warranty.html' style='color:var(--green);text-decoration:underline'>Warranty page</a> for full terms.")

# ====================================================== HOME
def home():
    faqs = [
        ("How much does a balcony makeover cost in Singapore?",
         "As planning ranges: outdoor decking is about S$18–45+ per ft², zip blinds about S$18–45+ per ft², and invisible grilles from about S$8 per ft². Bundling all three as an All-in-1 project is usually cheaper than three separate contractors. Final pricing follows a free site survey."),
        ("Can zip blinds fully stop Singapore rain?",
         "They dramatically reduce wind-driven rain, heat and glare and make a balcony usable in most weather. No zip blind system is fully watertight in all wind-driven-rain conditions — we recommend the right fabric density for your exposure rather than claiming a fully waterproof result."),
        ("Which invisible-grille coating should I choose — Nylon, PTFE or Nano?",
         "All three are vertical-cable balcony systems in 50 mm or 100 mm spacing. We provide physical samples and confirm the exact specification, colour, warranty and price in your quotation."),
        FAQ_5010, FAQ_MCST,
    ]
    body = f'''
<section class="hero" aria-label="Introduction">
  <div class="hero-media">
    <img src="assets/images/hero-balcony.webp" width="1536" height="1024" alt="Beautiful Singapore balcony with composite decking, motorised zip blinds and invisible grille railing at golden hour" fetchpriority="high">
    <video data-hero-video muted loop playsinline preload="none" poster="assets/images/hero-poster.webp" src="assets/videos/hero.mp4" aria-hidden="true"></video>
  </div>
  <div class="container hero-inner">
    <span class="eyebrow">Decking · Zip Blinds · Invisible Grilles</span>
    <h1>Outdoor Living,<br>Designed for Singapore</h1>
    <p>Balcony Master is your <strong>one solution for all</strong> — decking, weather-control zip blinds and safety grilles, supplied and installed with clear specifications, honest planning prices and dependable after-sales support.</p>
    <div class="hero-actions">
      <a href="contact.html" class="btn btn-primary">Get a site-measured quote</a>
      <a href="projects.html" class="btn btn-light">See completed projects</a>
    </div>
    <div class="hero-trust">
      <div>{CHECK} One team for all three</div>
      <div>{CHECK} Material grades disclosed</div>
      <div>{CHECK} Written warranty options</div>
      <div>{CHECK} Singapore-based support</div>
    </div>
  </div>
</section>

<section class="section"><div class="container">
  <span class="eyebrow reveal">One specialist, three layers</span>
  <h2 class="section-title reveal">Everything your balcony needs, coordinated under one roof</h2>
  <p class="lead reveal">The walking surface, the weather-control enclosure and the safety boundary — specified together so the finish, drainage and details work as a system.</p>
  <div class="grid services-grid">
    <article class="service-card reveal"><a href="outdoor-decking-singapore.html" class="thumb"><img src="assets/images/decking/service-decking-small.webp" width="900" height="600" alt="Warm capped composite WPC decking boards on a sunny Singapore balcony" loading="lazy"><span class="badge">Flooring</span></a>
      <div class="service-body"><span class="service-tag">Flooring</span><h3>Outdoor Decking &amp; Flooring</h3>
      <p>Capped WPC, natural Chengal, and outdoor marble, tiles and stone on properly detailed subframes with drainage and corrosion-resistant fixings.</p>
      <a class="service-link" href="outdoor-decking-singapore.html">Explore decking {ARROW}</a></div></article>
    <article class="service-card reveal"><a href="zip-blinds-singapore.html" class="thumb"><img src="assets/images/blinds/service-blinds-small.webp" width="900" height="600" alt="Condo balcony enclosed with motorised zip blinds and solar-mesh fabric at dusk" loading="lazy"><span class="badge">Weather</span></a>
      <div class="service-body"><span class="service-tag">Weather control</span><h3>Zip Blind Balcony Systems</h3>
      <p>Manual and motorised zip blind systems with solar-mesh options — reducing heat, glare, wind-driven rain and improving privacy. Backed by a 5-year warranty.</p>
      <a class="service-link" href="zip-blinds-singapore.html">Explore zip blinds {ARROW}</a></div></article>
    <article class="service-card reveal"><a href="invisible-grille-singapore.html" class="thumb"><img src="assets/images/grilles/service-grilles-small.webp" width="900" height="600" alt="Vertical near-invisible stainless steel grille cables on a balcony with a panoramic city view" loading="lazy"><span class="badge">Safety</span></a>
      <div class="service-body"><span class="service-tag">Safety</span><h3>Balcony Invisible Grilles</h3>
      <p>Vertical-cable Nylon, PTFE and Nano invisible-grille systems for balconies, available with 50&nbsp;mm or 100&nbsp;mm spacing.</p>
      <a class="service-link" href="invisible-grille-singapore.html">Explore grilles {ARROW}</a></div></article>
  </div>
</div></section>

<section class="section alt"><div class="container">
  <span class="eyebrow reveal">Why coordinate all three?</span>
  <h2 class="section-title reveal">One solution for all — fewer contractors, cleaner details</h2>
  <p class="lead reveal">When flooring, blinds and grilles are planned separately, the interfaces — drainage falls, track fixings, cable anchors — often clash. Coordinating them avoids rework and keeps one team responsible for the finished balcony.</p>
  <div class="grid feature-grid">
    <div class="feature-item reveal"><div class="ic">{CHECK}</div><h4>One site survey</h4><p>Measure floor, enclosure and safety line together — no repeated visits.</p></div>
    <div class="feature-item reveal"><div class="ic">{CHECK}</div><h4>Details that align</h4><p>Deck height, blind tracks and grille anchors planned so nothing fights for the same fixing.</p></div>
    <div class="feature-item reveal"><div class="ic">{CHECK}</div><h4>Single point of contact</h4><p>One itemised quote, one schedule, one warranty conversation.</p></div>
    <div class="feature-item reveal"><div class="ic">{CHECK}</div><h4>Better combined price</h4><p>Our All-in-1 bundle saves versus three separate contractors.</p></div>
  </div>
</div></section>

<section class="section"><div class="container">
  <span class="eyebrow reveal">Real Singapore projects</span>
  <h2 class="section-title reveal">Proof before promises</h2>
  <p class="lead reveal">A selection of completed balconies — the exact systems, materials and details we'd specify for you.</p>
  <div class="grid projects-grid">
    <a class="project big reveal" href="projects.html"><img src="assets/images/projects/condo-balcony-wpc-01.webp" width="1200" height="800" alt="Condo balcony with composite decking, zip blinds and grille, skyline view" loading="lazy"><div class="project-meta"><span class="t">Condo · All-in-1</span><h4>Skyline balcony — all three</h4><p>Decking · zip blinds · invisible grille</p></div></a>
    <a class="project reveal" href="projects.html"><img src="assets/images/projects/motorised-zip-blinds-01.webp" width="1200" height="800" alt="Balcony with motorised zip blinds" loading="lazy"><div class="project-meta"><span class="t">Condo · Zip blinds</span><h4>Motorised zip blind enclosure</h4><p>2 panels · solar mesh</p></div></a>
    <a class="project reveal" href="projects.html"><img src="assets/images/projects/nano-grille-01.webp" width="1200" height="800" alt="Vertical invisible grilles on a balcony" loading="lazy"><div class="project-meta"><span class="t">Safety</span><h4>Vertical invisible grille</h4><p>50 mm or 100 mm spacing</p></div></a>
  </div>
  <div class="center mt-2"><a href="projects.html" class="btn btn-ghost">Browse the full gallery {ARROW}</a></div>
</div></section>

<section class="section alt"><div class="container">
  <span class="eyebrow reveal">Transparent planning ranges</span>
  <h2 class="section-title reveal">Planning packages by service</h2>
  <p class="lead reveal">Each service is priced on its own basis — or bundle all three and save. Every rate is a planning starting point; final pricing follows a free site survey. See the full <a href="price-guide.html" style="color:var(--green);text-decoration:underline">price guide</a>.</p>
  <div class="svc-toggle reveal" role="tablist" aria-label="Choose a service" data-price-toggle>
    <button role="tab" aria-selected="true" data-target="decking">Decking</button>
    <button role="tab" aria-selected="false" data-target="blinds">Zip Blinds</button>
    <button role="tab" aria-selected="false" data-target="grilles">Invisible Grilles</button>
  </div>
  {price_panel_decking()}{price_panel_blinds()}{price_panel_grilles()}
  {bundle_banner()}
  {read_rates_note()}
</div></section>

{trust_section()}
{faq_section(faqs)}
{sticky_quote_form()}
'''
    write("index.html",
          "Balcony Master Singapore | Outdoor Decking, Zip Blinds & Invisible Grilles",
          "Balcony Master — one solution for all: outdoor decking, zip blinds and invisible grilles in Singapore for HDB, condo & landed. Clear specs, transparent prices, 5-year zip blind warranty. Bundle & save.",
          body, trail=None,
          keywords="balcony renovation Singapore, outdoor decking Singapore, composite decking, Chengal decking, zip blinds Singapore, motorised outdoor blinds, invisible grille Singapore, invisible grille price, balcony safety grille, HDB balcony, condo balcony",
          extra_ld=faq_ld_json([(q, plain(a)) for q, a in faqs]), active="")

# ====================================================== SERVICE PAGES
def service_page(path, title, desc, keywords, hero_eyebrow, h1, hero_p, intro_html, spec_table,
                 panel_fn, faqs, service_key, trail_label, og_image, service_ld_block, related):
    body = f'''
<section class="page-hero"><div class="container">
  <span class="eyebrow">{hero_eyebrow}</span><h1>{h1}</h1><p>{hero_p}</p>
  <div class="hero-actions" style="margin-top:1.2rem"><a href="contact.html?service={service_key}" class="btn btn-primary">Get a quote for this</a><a href="price-guide.html" class="btn btn-light">See full price guide</a></div>
</div></section>
<section class="section"><div class="container"><div class="prose reveal">{intro_html}</div></div></section>
<section class="section alt"><div class="container"><span class="eyebrow reveal">Specifications</span><h2 class="section-title reveal">Compare the options</h2><div class="table-wrap reveal mt-2">{spec_table}</div></div></section>
<section class="section"><div class="container"><span class="eyebrow reveal">Planning ranges</span><h2 class="section-title reveal">Indicative pricing</h2><p class="lead reveal">Planning starting points, verified against current Singapore market references — confirmed at a free site survey.</p>{panel_fn().replace(' hidden style="display:none"','')}{read_rates_note()}</div></section>
{faq_section(faqs)}
{related}
{sticky_quote_form(service_key)}
'''
    extra_ld = faq_ld_json([(q, plain(a)) for q, a in faqs]) + service_ld_block
    write(path, title, desc, body, trail=[("Home", "index.html"), (trail_label, None)],
          keywords=keywords, og_image=og_image, extra_ld=extra_ld, active=path)

def page_decking():
    intro = '''
<h2>Outdoor decking &amp; flooring in Singapore</h2>
<p>A balcony floor has to cope with sun, sudden rain and constant humidity. We supply and install <strong>capped WPC (composite) decking</strong>, natural <strong>Chengal and Balau hardwood</strong>, and outdoor <strong>marble, porcelain tiles and stone</strong> on properly detailed subframes — with drainage falls, corrosion-resistant fixings and clean edge trims so the finish lasts. We work on HDB balconies and service yards, condo balconies, and landed patios, pool decks and roof terraces.</p>
<p>Current Singapore references put installed decking from roughly <strong>S$18 per ft²</strong> for entry composite (market average near S$27), rising above <strong>S$45 per ft²</strong> for premium hardwood, modified timber, or marble and stone. We publish planning ranges rather than a single misleading "from" price.</p>
<h3>Composite (WPC) vs Chengal vs marble &amp; stone</h3>
<ul><li><strong>Capped WPC / composite decking:</strong> low-maintenance, colour-stable, termite- and rot-resistant — the popular all-rounder for condo balconies.</li>
<li><strong>Chengal &amp; Balau hardwood:</strong> dense tropical timbers with a warm natural grain; weather to silver-grey unless oiled.</li>
<li><strong>Outdoor marble, porcelain tiles &amp; stone:</strong> cool underfoot and easy to wipe clean — ideal for pool surrounds and wet areas.</li></ul>
<div class="callout">Substructure, drainage, site preparation, difficult access and complex shapes can substantially affect price. An itemised quotation after survey is more useful than a board-only rate.</div>
'''
    spec = table(["Option","Feel & look","Upkeep","Best for","Planning from"], [
        ["Entry composite / WPC","Uniform, modern","Low","Value, straightforward balconies","S$18–23 / ft²"],
        ["Mid-range capped WPC","Richer texture, colour-stable","Low","Most homeowners","S$24–32 / ft²"],
        ["Premium composite / Chengal hardwood","Natural grain, premium","Medium (oiling optional)","Design-led, landed patios","S$33–45+ / ft²"],
        ["Outdoor marble, tiles &amp; stone","Stone-like, cool underfoot","Low","Pool surrounds, wet areas","Price on survey"],
    ])
    faqs = [
        ("How much does outdoor decking cost in Singapore?",
         "Installed decking commonly starts around S$18 per ft² for entry composite and can exceed S$45 per ft² for premium hardwood, modified timber, or marble and stone. Your final rate depends on the finish, subframe, drainage, access and site preparation."),
        ("Is composite or Chengal decking better for a Singapore balcony?",
         "Capped WPC is lower-maintenance and colour-stable; Chengal is a premium natural hardwood that can be oiled to retain colour. Both perform well on a properly ventilated subframe with drainage. We recommend based on your exposure, look and budget."),
        ("Can you lay marble, porcelain tiles or stone on a balcony?",
         "Yes. Outdoor marble, porcelain tiles and natural stone are cool underfoot and easy to clean, which suits pool surrounds and wet areas. We confirm loading, drainage and waterproofing protection at survey."),
        FAQ_MCST,
    ]
    related = related_block("Related searches we cover", [
        ("Outdoor decking Singapore","outdoor-decking-singapore.html"),("Composite / WPC decking","outdoor-decking-singapore.html"),
        ("Chengal decking","outdoor-decking-singapore.html"),("Balcony decking price","price-guide.html"),
        ("Pool deck / stone flooring","outdoor-decking-singapore.html"),("Decking + blinds + grille bundle","complete-balcony-solution.html")])
    sld = service_ld("Outdoor decking supply and installation",
                     "Supply and installation of composite (WPC), Chengal hardwood, and outdoor marble/tile/stone decking for balconies, patios and pool decks in Singapore.",
                     [("Entry composite / WPC decking","18"),("Mid-range capped WPC decking","24"),("Premium / marble, tiles & stone decking","33")],
                     "outdoor-decking-singapore.html")
    service_page("outdoor-decking-singapore.html",
                 "Outdoor Decking Singapore | Composite, Chengal, Marble, Tiles & Stone | Balcony Master",
                 "Outdoor decking in Singapore — capped WPC/composite, Chengal & Balau hardwood, and outdoor marble, tiles and stone. Planning from S$18/ft². Free site survey for HDB, condo & landed.",
                 "outdoor decking Singapore, composite decking Singapore, WPC decking, Chengal decking, Balau decking, balcony decking price Singapore, pool deck, timber decking, marble tiles stone flooring balcony",
                 "Outdoor decking", "Outdoor Decking &amp; Flooring in Singapore",
                 "Capped WPC/composite, natural Chengal, and outdoor marble, tiles and stone — installed on properly detailed subframes with drainage and corrosion-resistant fixings.",
                 intro, spec, price_panel_decking, faqs, "decking", "Outdoor decking",
                 "assets/images/decking/service-decking-small.webp", sld, related)

def page_blinds():
    intro = '''
<h2>Zip blinds for Singapore balconies</h2>
<p><strong>Zip blinds</strong> (also called zip-screen or zip-lock outdoor blinds) run the fabric edge inside a track on both sides, so the screen stays taut and greatly reduces heat, glare, wind and wind-driven rain. They turn an exposed balcony into a usable space for most of the year — for HDB, condo and landed homes. Choose <strong>manual or motorised</strong> operation, with solar-mesh or blockout fabrics. Every zip blind system we install carries our <strong>5-year warranty</strong>.</p>
<p>Current Singapore references place manual systems from roughly <strong>S$18–28 per ft²</strong>, motorised from <strong>S$25–35 per ft²</strong>, and premium branded or smart systems from <strong>S$30–45+ per ft²</strong>, with a minimum panel size around 30–32 ft². Typical whole-project examples range from about S$800 for a small single-panel manual blind to S$2,800 for a comparable motorised condo balcony.</p>
<h3>Manual vs motorised, and choosing fabric openness</h3>
<p>Manual suits smaller openings and tighter budgets; motorised suits daily use, wider or higher panels and smart-home control. Fabric openness sets the balance of shade, view and airflow: 0–1% for blackout and privacy, 5% for balanced everyday use, 10% for more ventilation, and ~30% insect-screen weaves for maximum airflow.</p>
<div class="callout">We describe zip blinds as reducing glare, heat and wind-driven rain — subject to site exposure and operating conditions. We do not advertise a blind as fully "waterproof", "rainproof" or "windproof" without test reports covering the exact product.</div>
'''
    spec = table(["Openness","Light control","Outward view","Best for","Planning"], [
        ["0–1% Blackout","Highest","Low","Privacy, glare, west sun","S$18–35+ / ft²"],
        ["5% ScreenView","High","Balanced","Everyday balconies","S$18–35+ / ft²"],
        ["10% Ventilation","Medium","Good","Airflow with shade","S$18–35+ / ft²"],
        ["30% Insect screen","Low","Highest","Ventilation, bug control","S$18–35+ / ft²"],
    ])
    faqs = [
        ("How much do zip blinds cost in Singapore?",
         "Planning ranges are about S$18–28/ft² for manual, S$25–35/ft² for motorised, and S$30–45+/ft² for premium or smart systems, with a minimum panel around 30–32 ft². A standard condo balcony is often S$1,200–2,000 manual or S$1,800–2,800 motorised."),
        FAQ_ZIPWARR,
        ("Can zip blinds stop rain completely?",
         "They dramatically reduce wind-driven rain, heat and glare and make a balcony usable in most weather. No zip blind system is fully watertight in every wind-driven-rain condition — we match fabric density and detailing to your exposure rather than claiming a fully waterproof result."),
        ("Manual or motorised — which should I choose?",
         "Manual is simple, reliable and budget-friendly for smaller openings. Motorised suits daily use and wider or higher panels, and can integrate with smart-home control. We advise based on panel size, frequency of use and whether an electrical point is available."),
        FAQ_MCST,
    ]
    related = related_block("Related searches we cover", [
        ("Zip blinds Singapore","zip-blinds-singapore.html"),("Motorised outdoor blinds","zip-blinds-singapore.html"),
        ("Balcony blinds price","price-guide.html"),("Outdoor roller blinds condo","zip-blinds-singapore.html"),
        ("Rain & heat balcony screen","zip-blinds-singapore.html"),("Blinds + decking + grille bundle","complete-balcony-solution.html")])
    sld = service_ld("Zip blind supply and installation",
                     "Supply and installation of manual and motorised zip blinds with solar-mesh fabrics for HDB, condo and landed balconies in Singapore. 5-year system warranty.",
                     [("Manual zip blind","18"),("Motorised zip blind","25"),("Premium / smart zip blind","30")],
                     "zip-blinds-singapore.html")
    service_page("zip-blinds-singapore.html",
                 "Zip Blinds Singapore | Manual & Motorised Balcony Blinds | Balcony Master",
                 "Zip blinds in Singapore — manual & motorised, solar-mesh options for HDB, condo & landed balconies. Planning S$18–45+/ft², 5-year warranty. Reduce heat, glare & wind-driven rain.",
                 "zip blinds Singapore, zip screen blinds, motorised outdoor blinds Singapore, balcony blinds Singapore, outdoor roller blinds, condo balcony blinds, HDB balcony blinds, rainproof outdoor blinds",
                 "Zip blinds", "Zip Blind Balcony Systems in Singapore",
                 "Manual and motorised zip blind systems with solar-mesh options — reducing heat, glare, wind and wind-driven rain, subject to site exposure. 5-year warranty.",
                 intro, spec, price_panel_blinds, faqs, "blinds", "Zip blinds",
                 "assets/images/blinds/service-blinds-small.webp", sld, related)

def page_grilles():
    intro = '''
<h2>Balcony invisible grilles in Singapore</h2>
<p><strong>Invisible grilles</strong> use fine, tensioned stainless-steel cables — laid <strong>vertically</strong> between slim aluminium tracks — a near-invisible safety boundary that keeps your view, light and airflow. They suit HDB windows and balconies, condo balconies and landed homes, in 50&nbsp;mm or 100&nbsp;mm cable spacing. We offer three coatings to match exposure and budget.</p>
<p>Online 2026 references show standard fixed installations commonly around <strong>S$8–10 per ft²</strong> (one guide cites S$7–15), basic promotions from around <strong>S$4.90 per ft²</strong>, openable systems from around <strong>S$18.50 per ft²</strong>, and fixed balconies ranging roughly S$480–3,000 depending on size and spacing.</p>
<h3>Nylon vs PTFE (Teflon) vs Nano</h3>
<ul><li><strong>Nylon-coated — from S$8/ft², 3-year warranty.</strong> Value option, well positioned in the market.</li>
<li><strong>PTFE / Teflon-coated — from S$10/ft², 5-year warranty.</strong> Non-stick, UV-stable; good for higher floors.</li>
<li><strong>Nano all-weather — from S$16/ft², 10-year warranty.</strong> Premium; supplier data available on request.</li></ul>
<div class="callout">We don't state "100% rust-free", "child-proof", "pet-proof", "anti-climbing" or a specific force resistance unless it's supported by testing and our installation specification. We confirm the stainless grade, cable diameter, track spec and written warranty scope in your quotation.</div>
'''
    spec = table(["Coating","Core","Warranty","Best for","Planning from"], [
        ["Nylon-coated","Stainless-steel wire","3-year","Indoor-facing balconies, value","S$8 / ft²"],
        ["PTFE / Teflon-coated","304/316 stainless (confirmed at quote)","5-year","Most homes, higher floors","S$10 / ft²"],
        ["Nano all-weather","Premium 316 (data on request)","10-year","Exposed / coastal balconies","S$16 / ft²"],
        ["Openable system","As specified","As specified","Cleaning &amp; aircon access","Quotation after survey"],
    ])
    faqs = [
        ("How much does an invisible grille cost in Singapore?",
         "Standard fixed grilles commonly fall around S$8–10 per ft² (some guides quote S$7–15), with basic promotions from about S$4.90/ft². A fixed balcony can range roughly S$480–3,000 depending on size and cable spacing. Openable systems cost more due to the moving mechanism."),
        FAQ_5010,
        ("Are invisible grilles safe for children and pets?",
         "Our vertical-cable systems come in 50 mm (denser, popular for pets) or 100 mm (lighter look, chosen for child fall-protection) spacing. We recommend the spacing at survey and confirm the stainless grade, cable diameter and tensioning in your quotation rather than making blanket safety claims."),
        ("Is the premium Nano option worth it?",
         "It carries the longest warranty and suits exposed or coastal balconies. Because it's a premium price, we back it with the specific supplier data sheet, confirmed 316 stainless core and cable diameter — so you can compare it fairly against the S$10 option."),
        FAQ_MCST,
    ]
    related = related_block("Related searches we cover", [
        ("Invisible grille Singapore","invisible-grille-singapore.html"),("Invisible grille price","price-guide.html"),
        ("Invisible grille HDB","invisible-grille-singapore.html"),("Balcony safety grille","invisible-grille-singapore.html"),
        ("Cat / pet-safe grille (50 mm)","invisible-grille-singapore.html"),("Grille + decking + blinds bundle","complete-balcony-solution.html")])
    sld = service_ld("Invisible grille supply and installation",
                     "Supply and installation of vertical-cable invisible grilles (Nylon, PTFE/Teflon, Nano) for HDB windows, condo and landed balconies in Singapore, in 50 mm or 100 mm spacing.",
                     [("Nylon fixed grille","8"),("PTFE / Teflon fixed grille","10"),("Nano all-weather fixed grille","16")],
                     "invisible-grille-singapore.html")
    service_page("invisible-grille-singapore.html",
                 "Invisible Grille Singapore | Nylon, PTFE & Nano (Vertical) | Balcony Master",
                 "Invisible grille in Singapore — vertical-cable Nylon (from S$8/ft²), PTFE (from S$10/ft²) & Nano (from S$16/ft²), 50mm or 100mm spacing for HDB, condo & landed. Free site survey.",
                 "invisible grille Singapore, invisible grille price Singapore, invisible grille HDB, invisible window grille, balcony invisible grille, nylon teflon nano grille, cat safe grille, pet safe grille",
                 "Invisible grilles", "Balcony Invisible Grilles in Singapore",
                 "Vertical-cable Nylon, PTFE and Nano invisible-grille systems for balconies and windows, in 50 mm or 100 mm spacing — verified specs and written warranties.",
                 intro, spec, price_panel_grilles, faqs, "grilles", "Invisible grilles",
                 "assets/images/grilles/service-grilles-small.webp", sld, related)

# ====================================================== COMPLETE
def page_complete():
    body = f'''
<section class="page-hero"><div class="container">
  <span class="eyebrow">All-in-1 · One Solution for All</span><h1>The Complete Balcony Solution</h1>
  <p>Floor, weather-control enclosure and safety boundary — surveyed once, specified together, installed in the right sequence, and priced better as a bundle.</p>
  <div class="hero-actions" style="margin-top:1.2rem"><a href="contact.html?service=all" class="btn btn-primary">Plan my All-in-1 balcony</a><a href="projects.html" class="btn btn-light">See projects</a></div>
</div></section>
<section class="section"><div class="container">{bundle_banner()}</div></section>
<section class="section alt"><div class="container"><div class="prose reveal"><h2>Why plan the three together</h2>
  <p>Decking height, blind tracks and grille anchors all compete for the same edges and fixings. Coordinating them avoids clashes, reduces rework and keeps one team accountable for the finished balcony — and it costs less than hiring three separate contractors.</p><h3>The right installation sequence</h3></div>
  <div class="grid steps mt-2">
    <div class="step reveal"><div class="n">1</div><h4>Survey &amp; design</h4><p>Measure floor, enclosure and safety line together; confirm MCST needs.</p></div>
    <div class="step reveal"><div class="n">2</div><h4>Safety grilles</h4><p>Fix vertical cable tracks and anchors while the structure is accessible.</p></div>
    <div class="step reveal"><div class="n">3</div><h4>Decking</h4><p>Set subframe, drainage falls and boards to the correct finished height.</p></div>
    <div class="step reveal"><div class="n">4</div><h4>Zip blinds</h4><p>Install tracks, fabric and any motor/electrical last, aligned to the deck.</p></div>
  </div>
</div></section>
{sticky_quote_form("all")}
'''
    write("complete-balcony-solution.html",
          "All-in-1 Balcony Bundle Singapore | Decking + Zip Blinds + Grilles | Balcony Master",
          "Balcony Master All-in-1: outdoor decking, zip blinds and invisible grilles surveyed once, specified together and installed in sequence — one itemised quote at a better bundled price.",
          body, trail=[("Home", "index.html"), ("All-in-1", None)],
          keywords="complete balcony renovation Singapore, balcony makeover, decking blinds grille package, all in one balcony contractor Singapore",
          active="complete-balcony-solution.html")

# ====================================================== PROJECTS
def gallery_cat(cat, icon, title, blurb):
    return (f'<div class="gallery-cat reveal"><div class="gallery-cat-head"><div class="gc-ic" aria-hidden="true">{icon}</div>'
            f'<h3>{title}</h3><p>{blurb}</p></div><div class="media-grid" data-gallery="{cat}"></div></div>')

def page_projects():
    body = f'''
<section class="page-hero"><div class="container">
  <span class="eyebrow">Real Singapore projects</span><h1>Completed balconies &amp; installations</h1>
  <p>Organised by service — each section shows <strong>6 slots (5 photos + 1 video)</strong> you manage yourself. Drop files into the matching folder and edit <code>data/projects.js</code>. Empty slots show where to add more.</p>
</div></section>
<section class="section"><div class="container">
  {gallery_cat("decking", "🪵", "Decking projects", "WPC, Chengal, and marble/tile/stone finishes. Folders: assets/images/projects/decking/ and assets/videos/projects/decking/")}
  {gallery_cat("blinds", "🌧️", "Zip blind projects", "Manual & motorised enclosures. Folders: assets/images/projects/blinds/ and assets/videos/projects/blinds/")}
  {gallery_cat("grilles", "🛡️", "Invisible grille projects", "Vertical Nylon, PTFE & Nano, 50mm / 100mm. Folders: assets/images/projects/grilles/ and assets/videos/projects/grilles/")}
  <div class="callout reveal">Each real case study should show property type, general area (with permission), the products &amp; specification, approximate area, install duration, before/after photos and a customer-approved review. Original evidence outperforms stock photography for trust and search.</div>
</div></section>
{sticky_quote_form()}
'''
    extra_js = '<script src="data/projects.js"></script>\n<script src="js/gallery.js"></script>'
    write("projects.html",
          "Projects | Decking, Zip Blinds & Invisible Grilles Singapore | Balcony Master",
          "Completed Singapore balcony projects by Balcony Master, organised by service — outdoor decking, zip blinds and invisible grilles, with photo and video galleries.",
          body, trail=[("Home", "index.html"), ("Projects", None)],
          keywords="balcony projects Singapore, decking portfolio, zip blinds installation, invisible grille installation photos",
          extra_js=extra_js, active="projects.html")

# ====================================================== PRICE GUIDE
def page_price_guide():
    body = f'''
<section class="page-hero"><div class="container"><span class="eyebrow">Transparent planning ranges</span><h1>Singapore price guide 2026</h1>
  <p>Indicative supply-and-install planning ranges, verified against current market references (Aug 2026). Each service is priced on its own basis — or bundle all three and save.</p></div></section>
<section class="section"><div class="container">
  <div class="svc-toggle reveal" role="tablist" aria-label="Choose a service" data-price-toggle>
    <button role="tab" aria-selected="true" data-target="decking">Decking</button>
    <button role="tab" aria-selected="false" data-target="blinds">Zip Blinds</button>
    <button role="tab" aria-selected="false" data-target="grilles">Invisible Grilles</button>
  </div>
  {price_panel_decking()}{price_panel_blinds()}{price_panel_grilles()}
  {bundle_banner()}
  {read_rates_note()}
  <div class="prose reveal mt-2"><h2>What changes your final price</h2>
    <ul><li><strong>Decking:</strong> finish (WPC, Chengal, marble/tile/stone), subframe, drainage, site prep, difficult access and complex shapes.</li>
    <li><strong>Zip blinds:</strong> opening size, number of panels, motor brand, fabric openness, electrical work and minimum panel charge (~30–32 ft²).</li>
    <li><strong>Grilles:</strong> stainless grade, cable diameter, track spec, 50 mm vs 100 mm spacing, fixed vs openable and install height.</li></ul>
    <div class="callout">These are planning ranges, not contractual prices. They have been checked against current Singapore market rates and sit within the normal range. Your published rates should reflect your supplier cost, labour, warranty exposure, minimum order and target margin.</div>
  </div>
</div></section>
{sticky_quote_form()}
'''
    write("price-guide.html",
          "Price Guide 2026 | Decking, Zip Blinds & Invisible Grille Prices Singapore",
          "2026 Singapore price guide — outdoor decking (from S$18/ft²), zip blinds (S$18–45+/ft²) and invisible grilles (from S$8/ft²). Market-verified ranges, bundle & save.",
          body, trail=[("Home", "index.html"), ("Price guide", None)],
          keywords="decking price Singapore, zip blinds price Singapore, invisible grille price Singapore, balcony renovation cost, per square foot rates",
          active="price-guide.html")

# ====================================================== WARRANTY
def warr_card(name, term, covered, excluded, extra=None, hl=False, schedule_html=""):
    cov = "".join(f"<li>{c}</li>" for c in covered)
    exc = "".join(f"<li>{c}</li>" for c in excluded)
    ex = f'<h4>Conditions</h4><ul>{"".join(f"<li>{c}</li>" for c in extra)}</ul>' if extra else ""
    return (f'<div class="warr-card{" hl" if hl else ""} reveal"><div class="wh"><h3>{name}</h3><span class="term">{term}</span></div>'
            f'{schedule_html}'
            f'<h4>What is covered</h4><ul>{cov}</ul>'
            f'<h4>What is NOT covered</h4><ul class="excl">{exc}</ul>{ex}</div>')

def zip_service_schedule():
    return ('<h4>Service visits during the 5-year warranty</h4>'
            '<table class="svc-sched"><thead><tr><th scope="col">Service visit</th><th scope="col">Labour charge</th></tr></thead><tbody>'
            '<tr><td>1st visit</td><td class="free">FREE</td></tr>'
            '<tr><td>2nd visit</td><td class="free">FREE</td></tr>'
            '<tr><td>3rd visit</td><td class="paid">S$250</td></tr>'
            '<tr><td>4th visit</td><td class="paid">S$250</td></tr>'
            '<tr><td>5th visit</td><td class="paid">S$250</td></tr>'
            '</tbody></table>'
            '<p style="font-size:.82rem;color:var(--muted);margin:.2rem 0 .2rem">Please give at least <strong>4 weeks\u2019 advance notice</strong> to schedule any repair or service visit. Parts/materials, motor/electrical faults and out-of-scope items are quoted separately.</p>')

def page_warranty():
    common_excl = [
        "Damage from misuse, accident, alteration, or work by third parties not authorised by us",
        "Normal wear, weathering, fading or patina, and colour change over time",
        "Damage from extreme weather, storms, falling objects, vandalism or force majeure",
        "Movement, cracking or water ingress originating from the building structure or existing waterproofing",
        "Consequential or indirect loss of any kind",
    ]
    common_cond = [
        "Warranty is non-transferable and applies to the original paying customer at the installed address",
        "Valid only when the invoice is fully paid and the product is used and maintained as advised",
        "Claims must be reported in writing; we inspect before any remedy",
        "Our sole obligation is repair or replacement of the defective part, at our option; labour outside the stated free visits is chargeable",
        "A call-out/inspection fee applies to no-fault visits or issues outside warranty scope",
    ]
    zip_card = warr_card(
        "Zip Blind System", "5-year",
        ["Fabric, tracks, bottom bar and zip-lock components against manufacturing defects for 5 years",
         "Workmanship of our installation (fixings, alignment, tensioning) for 5 years",
         "Re-tensioning and adjustment arising from our installation, within the service-visit schedule"],
        common_excl + ["Wind damage when the blind is left down in strong wind against our advice",
         "Water ingress in wind-driven rain (zip blinds reduce, not eliminate, rain)",
         "Fabric soiling, mildew from lack of cleaning, and pet damage"],
        common_cond + ["Blind must be raised in stormy / high-wind conditions as advised",
         "Motor, remote and smart-control electronics follow the manufacturer's own warranty",
         "Advance notice of at least 4 weeks is required to schedule any service or repair visit"],
        hl=True, schedule_html=zip_service_schedule())
    cards = (
        zip_card +
        warr_card("Outdoor Decking (WPC / Chengal / stone)", "Product + 1-yr workmanship",
            ["Manufacturing defects in supplied boards/tiles per the maker's terms","Workmanship defects in our subframe &amp; fixings for 12 months","Re-securing of any board that lifts due to our installation within 12 months"],
            common_excl + ["Oiling/sealing of natural timber and routine cleaning","Heat build-up, minor expansion/contraction and natural timber movement","Planter, pot, furniture, footfall scratching or staining"], common_cond) +
        warr_card("Zip Blind — motor (if selected)", "Motor per manufacturer",
            ["Tubular motor &amp; receiver defects per the motor maker's warranty","Remote pairing/setup issues reported within the workmanship period"],
            common_excl + ["Damage from incorrect power supply, power surges or unauthorised electrical work","Batteries, remotes and smart-home app/third-party integration issues","Water damage from exposure beyond the motor's IP rating"],
            common_cond + ["Electrical supply must comply with our specification and be installed by a licensed electrician"]) +
        warr_card("Invisible Grille — Nylon-coated", "3-year limited",
            ["Cable, coating and track defects under normal residential use for 3 years","One complimentary re-tensioning within the first 12 months","Anchor/fixing workmanship for the warranty period"],
            common_excl + ["Coating wear from abrasion, cleaning chemicals or pets","Corrosion where cables are cut, drilled or modified after install","Sagging caused by hanging objects/loads on the cables"], common_cond) +
        warr_card("Invisible Grille — PTFE / Teflon", "5-year limited",
            ["Cable, PTFE coating and track defects under normal use for 5 years","One complimentary re-tensioning within the first 18 months","Anchor/fixing workmanship for the warranty period"],
            common_excl + ["Coating wear from abrasion, cleaning chemicals or pets","Corrosion where cables are cut, drilled or modified after install","Sagging caused by hanging objects/loads on the cables"], common_cond) +
        warr_card("Invisible Grille — Nano all-weather", "10-year limited",
            ["Cable, nano-coating and track defects under normal use for 10 years","Annual courtesy tension check on request for the first 3 years","Anchor/fixing workmanship for the warranty period"],
            common_excl + ["Coating wear from abrasion, cleaning chemicals or pets","Corrosion where cables are cut, drilled or modified after install","Sagging caused by hanging objects/loads on the cables"],
            common_cond + ["Supplier data sheet defines the coating performance; claims assessed against it"])
    )
    body = f'''
<section class="page-hero"><div class="container"><span class="eyebrow">After-sales</span><h1>Warranty &amp; support</h1>
  <p>Every product carries a clear, written warranty with a defined scope and claim process. Our headline <strong>Zip Blind System warranty is 5 years</strong>, with the first two service visits free and a fixed labour charge thereafter. Full details are confirmed in your quotation and invoice.</p></div></section>
<section class="section"><div class="container">
  <div class="warr-grid">{cards}</div>
  <div class="prose reveal mt-2">
    <h2>General warranty terms</h2>
    <ol>
      <li><strong>Zip blind service schedule.</strong> Within the 5-year zip blind warranty, the <strong>1st and 2nd service visits are free</strong>; the <strong>3rd, 4th and 5th visits carry a labour charge of S$250 each</strong>. Parts/materials and out-of-scope work are quoted separately.</li>
      <li><strong>Advance notice.</strong> Please provide at least <strong>4 weeks' notice</strong> to schedule any repair or service visit so we can plan parts, access and manpower.</li>
      <li><strong>Coverage &amp; remedy.</strong> Warranties cover genuine manufacturing or workmanship defects only. Our sole obligation is to repair or replace the defective part at our option; this is your exclusive remedy.</li>
      <li><strong>Registration &amp; payment.</strong> Cover starts on the installation completion date and is valid only when the invoice is paid in full. Warranty is non-transferable.</li>
      <li><strong>Maintenance.</strong> Products must be cleaned and used as advised. Failure to maintain, or use outside intended purpose, voids cover.</li>
      <li><strong>Exclusions.</strong> Wear, weathering, misuse, third-party work, structural/waterproofing issues, weather events and consequential loss are excluded.</li>
      <li><strong>Liability cap.</strong> To the extent permitted by law, our total liability is limited to the amount paid for the affected product. Statutory rights are unaffected.</li>
    </ol>
    <div class="callout">These terms are a seller-protective template for layout and planning. Have them reviewed by a qualified adviser and align the product-specific periods with your suppliers' written warranties before publishing.</div>
  </div>
</div></section>
{sticky_quote_form()}
'''
    write("warranty.html",
          "Warranty & Support | 5-Year Zip Blind Warranty | Balcony Master Singapore",
          "Balcony Master warranties — 5-year zip blind system warranty (1st & 2nd service free, 3rd–5th S$250 labour, 4 weeks' notice), plus decking and invisible grilles (Nylon 3-yr, PTFE 5-yr, Nano 10-yr).",
          body, trail=[("Home", "index.html"), ("Warranty", None)],
          keywords="zip blind warranty Singapore, 5 year warranty balcony blinds, invisible grille warranty, decking warranty",
          active="warranty.html")

# ====================================================== ABOUT / CONTACT / LEGAL
def page_about():
    body = f'''
<section class="page-hero"><div class="container"><span class="eyebrow">About us</span><h1>Balcony Master — one solution for all</h1>
  <p>We coordinate decking, zip blinds and invisible grilles so the finish, drainage and safety details work together — with honest specifications and transparent, market-checked planning prices.</p></div></section>
<section class="section"><div class="container"><div class="prose reveal">
  <h2>How we work</h2><p>We start with a free site survey, recommend the right system for your property and exposure, and prepare a single itemised quotation with inclusions, exclusions and GST stated up front. Installation follows a sensible sequence — safety line, floor, then enclosure — so nothing has to be undone.</p>
  <h2>What we stand for</h2><ul><li>One accountable team for all three services</li><li>Planning-price ranges checked against the Singapore market, not one misleading "from" figure</li><li>Written warranties with a defined scope and claim process</li><li>Genuine project evidence and real reviews only</li></ul>
  <div class="callout">Company details on this prototype are placeholders. Confirm the registered name, UEN, contact numbers and warranty scope in <code>js/config.js</code> before publishing.</div>
</div></div></section>
{sticky_quote_form()}
'''
    write("about.html", "About | Balcony Master — Decking, Zip Blinds & Invisible Grilles Singapore",
          "About Balcony Master — Singapore's one-solution balcony specialist coordinating decking, zip blinds and invisible grilles with verified specs and transparent prices.",
          body, trail=[("Home", "index.html"), ("About", None)],
          keywords="balcony specialist Singapore, about Balcony Master", active="")

def page_contact():
    body = f'''
<section class="page-hero"><div class="container"><span class="eyebrow">Get in touch</span><h1>Request a free, measured quote</h1>
  <p>Tell us the basics and upload your floor plan or balcony photos — we'll arrange a free site survey and prepare an itemised quotation, no obligation.</p></div></section>
<section class="section"><div class="container two-col">
  <div class="prose reveal"><h2>Talk to us</h2><p>Fastest response is on WhatsApp with a couple of photos or your floor plan.</p>
    <ul><li>Phone: <a data-tel href="#"><span data-phone-text>+65 8000 0000</span></a></li><li>WhatsApp: <a data-wa href="#">message us</a></li><li>Email: <a data-email href="#"></a></li></ul>
    <p>Hours: Mon–Sat, 9am–6pm. Serving HDB, condo and landed properties islandwide.</p></div>
  <div class="form-card reveal">{quote_form_inner("", with_name=True)}</div>
</div></section>
'''
    write("contact.html", "Contact | Free Site Survey & Quote | Balcony Master",
          "Contact Balcony Master for a free site survey and itemised quote on decking, zip blinds and invisible grilles in Singapore. Upload your floor plan or balcony photos.",
          body, trail=[("Home", "index.html"), ("Contact", None)],
          keywords="balcony contractor Singapore contact, free quote decking blinds grille", active="")

def simple_page(path, title, desc, h1, prose, trail_label):
    body = f'<section class="page-hero"><div class="container"><span class="eyebrow">Legal</span><h1>{h1}</h1></div></section><section class="section"><div class="container"><div class="prose reveal">{prose}</div></div></section>'
    write(path, title, desc, body, trail=[("Home", "index.html"), (trail_label, None)])

def page_privacy():
    simple_page("privacy.html", "Privacy Notice | Balcony Master", "Privacy notice for Balcony Master — how we collect and use enquiry details and uploads.", "Privacy Notice",
        '<p><em>Template only — review with a qualified adviser before publishing.</em></p><h2>What we collect</h2><p>When you submit an enquiry we collect the details you provide (name, mobile number, property type) and any files you upload (floor plans or balcony photos) to prepare a quotation and arrange a site survey.</p><h2>How we use it</h2><p>We use your details and uploads solely to respond to your enquiry and provide our services. We do not sell your data.</p><h2>Retention &amp; contact</h2><p>We keep enquiry data and uploads only as long as needed for your project and our records. To access or delete your data, contact us via the details on the Contact page.</p>', "Privacy")

def page_terms():
    simple_page("terms.html", "Terms | Balcony Master", "Terms for Balcony Master — quotations, pricing, warranties and workmanship.", "Terms",
        '<p><em>Template only — review with a qualified adviser before publishing.</em></p><h2>Quotations &amp; pricing</h2><p>All prices shown on this website are indicative planning ranges. Final pricing is confirmed in a written, itemised quotation following a measured site survey. GST and minimum-order charges may apply.</p><h2>Warranties</h2><p>Warranty scope, inclusions and exclusions are stated in your quotation and on the Warranty page, and confirmed in writing before acceptance. The zip blind system warranty is 5 years, with the 1st and 2nd service visits free and the 3rd–5th visits at S$250 labour each; at least 4 weeks\u2019 notice is required to schedule a repair.</p><h2>Deposits &amp; MCST</h2><p>A booking deposit may be required to schedule works. Where a condominium requires a renovation/management deposit, this is arranged and paid by the home owner directly to the managing agent (MA) or MCST.</p><h2>Workmanship</h2><p>Installation is scheduled subject to site access, MCST approvals where relevant, and weather.</p>', "Terms")

def page_thankyou():
    body = f'<section class="section"><div class="container center" style="max-width:640px"><div class="form-success show" style="display:block"><div class="check">{CHECK}</div><h1 class="section-title" style="margin-top:1rem">Thank you — request received</h1><p class="lead" style="margin-inline:auto">We\'ll reach out within one business day to arrange your free site survey. For a faster response, send us photos on WhatsApp.</p><div class="hero-actions" style="justify-content:center;margin-top:1rem"><a data-wa class="btn btn-primary">Send photos on WhatsApp</a><a href="index.html" class="btn btn-ghost">Back to home</a></div></div></div></section>'
    write("thank-you.html", "Thank you | Balcony Master", "Thank you — your enquiry has been received.", body, trail=None)

def page_404():
    body = '<section class="section"><div class="container center" style="max-width:640px"><span class="eyebrow">404</span><h1 class="section-title">Page not found</h1><p class="lead" style="margin-inline:auto">The page you were looking for has moved or no longer exists. Try one of these instead.</p><div class="hero-actions" style="justify-content:center;margin-top:1rem"><a href="index.html" class="btn btn-primary">Home</a><a href="price-guide.html" class="btn btn-ghost">Price guide</a><a href="contact.html" class="btn btn-ghost">Contact</a></div></div></section>'
    write("404.html", "Page not found | Balcony Master", "404 — page not found.", body, trail=None)

def seo_files():
    pages = ["index.html","outdoor-decking-singapore.html","zip-blinds-singapore.html","invisible-grille-singapore.html",
             "complete-balcony-solution.html","projects.html","price-guide.html","warranty.html","about.html","contact.html","privacy.html","terms.html"]
    today = datetime.date.today().isoformat()
    urls = "".join(f"  <url><loc>{SITE}/{p}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>{'1.0' if p=='index.html' else '0.8'}</priority></url>\n" for p in pages)
    open(os.path.join(OUT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+urls+'</urlset>\n')
    open(os.path.join(OUT,"robots.txt"),"w").write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE)
    open(os.path.join(OUT,"site.webmanifest"),"w").write(json.dumps({
        "name":"Balcony Master","short_name":"BalconyMaster","start_url":"/index.html","display":"standalone",
        "background_color":"#ffffff","theme_color":"#1E4D3B","icons":[]}, indent=2))
    print("wrote sitemap.xml, robots.txt, site.webmanifest")

if __name__ == "__main__":
    home(); page_decking(); page_blinds(); page_grilles(); page_complete()
    page_projects(); page_price_guide(); page_warranty(); page_about(); page_contact()
    page_privacy(); page_terms(); page_thankyou(); page_404(); seo_files()
    print("ALL DONE")
