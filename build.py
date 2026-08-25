#!/usr/bin/env python3
"""Balcony Master @ lionsin.com.sg — v9. Implements the senior-review action plan."""
import os, datetime, html, json

OUT=os.path.dirname(os.path.abspath(__file__))
SITE="https://www.lionsin.com.sg"; DOMAIN="www.lionsin.com.sg"
BRAND="Balcony Master"; TAGLINE="One Solution for All"; YEAR=2026
PHONE="+6583417888"; PHONE_D="+65 8341 7888"; WA="https://wa.me/6583417888"; EMAIL="bimprosg@outlook.com"
FORM=f"https://formsubmit.co/{EMAIL}"
WA_REL='rel="nofollow noopener noreferrer" target="_blank"'
OG_IMG="assets/images/social/og-home.jpg"; OG_ALT="Balcony Master — outdoor living solutions in Singapore"

NAV=[("Balcony Decking","balcony-decking-singapore.html"),("Zip Blinds","zip-blinds-singapore.html"),
     ("Invisible Grilles","invisible-grille-singapore.html"),("Retractable Roof","retractable-roof-singapore.html"),
     ("Projects","projects.html"),("Pricing","price-guide.html"),("Warranty","warranty.html")]
def nav_links(a): return "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h==a else ""}>{l}</a></li>' for l,h in NAV)
def mobile_links(a): return "".join(f'<a href="{h}"{" aria-current=\"page\"" if h==a else ""}>{l}</a>' for l,h in NAV)+'<a href="about.html">About</a><a href="contact.html" class="mm-cta">Get a quote →</a>'

CHECK='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>'
ARROW='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
PH='<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
PLAY='<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>'
LOGO=(f'<a href="./" class="brand" aria-label="{BRAND} — {TAGLINE}, home">'
      f'<span class="mark"><img src="assets/icons/favicon.svg" width="40" height="40" alt=""></span>'
      f'<span class="bt"><b>{BRAND}</b><span>{TAGLINE}</span></span></a>')

def org_node():
    return {"@type":"HomeAndConstructionBusiness","@id":f"{SITE}/#business","name":BRAND,
        "alternateName":["Balcony Master Singapore","Lionsin"],"slogan":TAGLINE,"url":f"{SITE}/",
        "image":f"{SITE}/{OG_IMG}","logo":f"{SITE}/assets/icons/icon-512.png","telephone":PHONE,"email":EMAIL,
        "priceRange":"$$","areaServed":{"@type":"Country","name":"Singapore"},
        "address":{"@type":"PostalAddress","addressLocality":"Singapore","addressCountry":"SG"},
        "description":"Singapore balcony specialist — balcony decking, zip blinds, invisible grilles and motorised retractable roofs. Supply and installation for HDB, condo and landed homes.",
        "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"09:00","closes":"18:00"}]}
def website_node():
    return {"@type":"WebSite","@id":f"{SITE}/#website","url":f"{SITE}/","name":BRAND,"publisher":{"@id":f"{SITE}/#business"},"inLanguage":"en-SG"}

def page_graph(canonical,title,desc,trail,faqs=None,service=None):
    nodes=[org_node(),website_node(),
        {"@type":"WebPage","@id":canonical+"#webpage","url":canonical,"name":title,"description":desc,
         "isPartOf":{"@id":f"{SITE}/#website"},"about":{"@id":f"{SITE}/#business"},
         "inLanguage":"en-SG","primaryImageOfPage":f"{SITE}/{OG_IMG}"}]
    if trail:
        items=[]
        for i,(label,href) in enumerate(trail):
            it={"@type":"ListItem","position":i+1,"name":label}
            if href: it["item"]=f"{SITE}/" if href in("./","index.html") else f"{SITE}/{href}"
            items.append(it)
        nodes.append({"@type":"BreadcrumbList","@id":canonical+"#breadcrumb","itemListElement":items})
    if faqs:
        nodes.append({"@type":"FAQPage","@id":canonical+"#faq","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]})
    if service:
        nodes.append(service)
    return '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@graph":nodes})+'</script>'

def service_node(name,desc,offers,url):
    return {"@type":"Service","@id":f"{SITE}/{url}#service","serviceType":name,"provider":{"@id":f"{SITE}/#business"},
        "areaServed":"Singapore","url":f"{SITE}/{url}","description":desc,
        "hasOfferCatalog":{"@type":"OfferCatalog","name":name,"itemListElement":[{"@type":"Offer","name":n,"priceCurrency":"SGD","price":str(p)} for n,p in offers]}}

def head(title,desc,path,trail=None,faqs=None,service=None,active="",home=False):
    canonical=f"{SITE}/" if home else f"{SITE}/{path}"
    return f'''<!DOCTYPE html>
<html lang="en-SG"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#1E4D3B"><meta name="geo.region" content="SG"><meta name="geo.placename" content="Singapore">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="assets/icons/favicon.svg" type="image/svg+xml">
<link rel="alternate icon" href="assets/icons/favicon-32.png">
<link rel="apple-touch-icon" href="assets/icons/apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/{OG_IMG}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{OG_ALT}"><meta property="og:locale" content="en_SG">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}"><meta name="twitter:image" content="{SITE}/{OG_IMG}">
<meta name="twitter:image:alt" content="{OG_ALT}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="css/styles.css"><link rel="manifest" href="site.webmanifest">
<script src="js/config.js" defer></script><script src="js/main.js" defer></script>
{page_graph(canonical,title,desc,trail,faqs,service)}
</head><body>
<a href="#main" class="skip-link">Skip to content</a>
<header class="site-header"><div class="container nav">
    {LOGO}
    <nav aria-label="Primary"><ul class="nav-links">{nav_links(active)}</ul></nav>
    <div class="nav-cta">
      <a class="nav-phone" href="tel:{PHONE}">{PH}<span>{PHONE_D}</span></a>
      <a href="contact.html" class="btn btn-primary">Get a quote</a>
      <button class="menu-toggle" id="menuToggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      </button>
    </div></div>
  <div class="container mobile-menu" id="mobileMenu">{mobile_links(active)}</div>
</header>
<main id="main">'''

def breadcrumb(trail):
    parts=[]
    for label,href in trail:
        if href: parts.append(f'<a href="{href}">{label}</a>')
        else: parts.append(f'<span aria-current="page">{label}</span>')
    return f'<nav class="breadcrumbs container" aria-label="Breadcrumb">{"<span aria-hidden=\"true\">›</span>".join(parts)}</nav>'

def footer(extra_js=""):
    return f'''</main>
<footer class="site-footer"><div class="container">
  <h2 class="visually-hidden">Site footer</h2>
  <div class="footer-grid">
    <div class="footer-brand">{LOGO}<p>Singapore's balcony specialist — balcony decking, zip blinds, invisible grilles and retractable roofs. Call <a href="tel:{PHONE}">{PHONE_D}</a>.</p></div>
    <div class="footer-col"><h3>Services</h3><ul>
      <li><a href="balcony-decking-singapore.html">Balcony decking</a></li>
      <li><a href="zip-blinds-singapore.html">Zip blinds</a></li>
      <li><a href="invisible-grille-singapore.html">Invisible grilles</a></li>
      <li><a href="retractable-roof-singapore.html">Retractable roof</a></li>
      <li><a href="complete-balcony-solution.html">All-in-1 bundle</a></li></ul></div>
    <div class="footer-col"><h3>Explore</h3><ul>
      <li><a href="price-guide.html">Price guide</a></li>
      <li><a href="projects.html">Projects</a></li>
      <li><a href="warranty.html">Warranty</a></li>
      <li><a href="about.html">About</a></li></ul></div>
    <div class="footer-col"><h3>Get in touch</h3><ul>
      <li><a href="tel:{PHONE}">{PHONE_D}</a></li>
      <li><a data-wa href="{WA}" {WA_REL}>WhatsApp us</a></li>
      <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li><a href="contact.html">Book a site survey</a></li>
      <li><a href="privacy.html">Privacy</a> · <a href="terms.html">Terms</a></li></ul></div>
  </div>
  <div class="footer-bottom"><span>© {YEAR} {BRAND} · lionsin.com.sg. All rights reserved.</span>
    <span>Prices are indicative planning ranges. Final pricing follows a measured site survey. GST may apply.</span></div>
</div></footer>
<div class="mobile-bar">
  <a href="tel:{PHONE}" class="call">📞<span>Call</span></a>
  <a data-wa href="{WA}" class="wa" {WA_REL}>💬<span>WhatsApp</span></a>
  <a href="contact.html" class="quote">✏️<span>Get quote</span></a>
</div>
{extra_js}
</body></html>'''

def upload_field():
    return ('<div class="field"><label for="qf-files">Floor plan or balcony photos <span class="u-sub">(optional)</span></label>'
            '<label class="upload" for="qf-files"><span class="u-ic" aria-hidden="true">📎</span>'
            '<b>Tap to attach your floor plan or balcony photos</b>'
            '<span class="u-sub">JPG, PNG or PDF. For large files, you can also send them on WhatsApp.</span>'
            '<input id="qf-files" type="file" name="attachments" accept="image/*,.pdf" multiple>'
            '<span class="u-files" aria-live="polite"></span></label></div>')

def quote_form(service="",with_name=False):
    name=('<div class="field"><label for="qf-name">Name <span class="req" aria-hidden="true">*</span></label>'
          '<input id="qf-name" name="name" type="text" autocomplete="name" required aria-required="true" aria-invalid="false" aria-describedby="qf-name-err">'
          '<span class="err" id="qf-name-err">Please enter your name.</span></div>') if with_name else ""
    return f'''<form data-quote-form action="{FORM}" method="POST" enctype="multipart/form-data" novalidate>
      <h2>Tell us the basics</h2><p class="sub">Add your floor plan or balcony photos for a faster, more accurate quote.</p>
      <div class="form-error-summary" role="alert" aria-live="assertive"></div>
      <input type="hidden" name="_subject" value="New balcony enquiry — lionsin.com.sg">
      <input type="hidden" name="_next" value="{SITE}/thank-you.html">
      <input type="hidden" name="_template" value="table">
      <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div class="hp" aria-hidden="true"><label>Company website<input type="text" name="company_website" tabindex="-1" autocomplete="off"></label></div>
      <input type="hidden" name="service_preselect" value="{service}">
      <fieldset class="form-fieldset"><legend class="visually-hidden">Project details</legend>
        <div class="field-row">
          <div class="field"><label for="qf-prop">Property type <span class="req" aria-hidden="true">*</span></label>
            <select id="qf-prop" name="property" required aria-required="true" aria-invalid="false" aria-describedby="qf-prop-err"><option value="" disabled selected>Select…</option><option>Condominium</option><option>Landed</option><option>HDB</option><option>Commercial</option></select>
            <span class="err" id="qf-prop-err">Please select a property type.</span></div>
          <div class="field"><label for="qf-svc">Service needed</label>
            <select id="qf-svc" name="service"><option value="" disabled selected>Select…</option><option>Decking</option><option>Zip blinds</option><option>Invisible grilles</option><option>Retractable roof</option><option>Multiple / all</option></select></div>
        </div>
        {name}
        <div class="field"><label for="qf-mob">Mobile number <span class="req" aria-hidden="true">*</span></label>
          <input id="qf-mob" name="mobile" type="tel" inputmode="tel" placeholder="+65 8XXX XXXX" autocomplete="tel" required aria-required="true" aria-invalid="false" aria-describedby="qf-mob-err">
          <span class="err" id="qf-mob-err">Please enter a valid mobile number.</span></div>
        {upload_field()}
      </fieldset>
      <label class="checkbox"><input type="checkbox" id="qf-consent" name="consent" required aria-required="true" aria-invalid="false" aria-describedby="qf-consent-err"> I agree to be contacted and to the storing of these details per the <a href="privacy.html">Privacy Notice</a>. <span class="req" aria-hidden="true">*</span></label>
      <span class="consent-err" id="qf-consent-err">Please tick the box to continue.</span>
      <button type="submit" class="btn btn-primary btn-block">Request my quote</button>
      <p class="form-note">We aim to reply within one business day. Your details are kept private and never sold.</p>
    </form>
    <div class="form-success" role="status"><div class="check">{CHECK}</div><h3>Thank you — request received</h3>
      <p class="sub mt-1">We'll be in touch to arrange your free site survey.</p>
      <a data-wa href="{WA}" {WA_REL} class="btn btn-primary mt-1">Send photos on WhatsApp</a></div>'''

def quote_section(service=""):
    return f'''<section id="quote" class="quote section"><div class="container quote-grid">
  <div class="quote-copy reveal"><span class="eyebrow">Start your project</span>
    <h2 class="section-title">Request a measured, itemised quote</h2>
    <p>Share a few details — and upload your floor plan or balcony photos — to begin. Or call us now at <a href="tel:{PHONE}">{PHONE_D}</a>.</p>
    <ul><li>Free site survey &amp; measurement</li><li>Honest recommendation for your property</li><li>Transparent, itemised pricing with GST stated</li></ul></div>
  <div class="form-card reveal">{quote_form(service)}</div>
</div></section>'''

def write(path,title,desc,body,trail=None,faqs=None,service=None,active="",home=False,extra_js=""):
    doc=head(title,desc,path,trail,faqs,service,active,home)+(breadcrumb(trail) if trail else "")+body+footer(extra_js)
    open(os.path.join(OUT,path),"w",encoding="utf-8").write(doc); print("wrote",path,f"({len(doc)}b)")

def faq_section(qas):
    items="".join(f'<details class="qa"{" open" if i==0 else ""}><summary>{q}<span class="plus" aria-hidden="true"></span></summary><div class="ans">{a}</div></details>' for i,(q,a) in enumerate(qas))
    return f'<section class="section alt"><div class="container"><span class="eyebrow reveal">Common questions</span><h2 class="section-title reveal">Answers before you commit</h2><div class="faq reveal mt-2">{items}</div></div></section>'
def table(headers,rows):
    th="".join(f'<th scope="col">{h}</th>' for h in headers)
    tr="".join("<tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>" for r in rows)
    return f'<table class="spec"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'
def plain(t):
    import re; return re.sub("<[^>]+>","",t).replace("&amp;","&")
def related(title,links):
    return f'<section class="section"><div class="container"><span class="eyebrow reveal">{title}</span><div class="reveal chips">{"".join(f"<a href=\"{h}\">{l}</a>" for l,h in links)}</div></div></section>'

def price_card(name,amt,who,bullets,cta,featured=False,ribbon=None,photo=None,alt=None,badge=None,video=None,poster=None):
    lis="".join(f"<li>{b}</li>" for b in bullets); rib=f'<span class="ribbon">{ribbon}</span>' if ribbon else ""
    btn="btn-primary" if featured else "btn-ghost"; media=""; a=alt or name
    if video:
        b=f'<span class="pc-badge">{badge}</span>' if badge else ""
        media=(f'<div class="pc-photo is-video" data-video-box data-src="{video}" data-poster="{poster}">'
               f'<img src="{poster}" width="900" height="640" alt="{a}" loading="lazy">{b}'
               f'<span class="pc-vtag">▶ Video</span><button class="pc-play" type="button" aria-label="Play {name} video"><span>{PLAY}</span></button></div>')
    elif photo:
        b=f'<span class="pc-badge">{badge}</span>' if badge else ""
        media=f'<div class="pc-photo"><img src="{photo}" width="900" height="640" alt="{a}" loading="lazy">{b}</div>'
    return (f'<div class="price-card {"featured" if featured else ""} reveal">{media}'
            f'<div class="pc-body">{rib}<h3>{name}</h3><p class="who">{who}</p><div class="amt">{amt}</div>'
            f'<ul>{lis}</ul><a href="{cta}" class="btn {btn}">Plan this</a></div></div>')

def panel_wrap(pid,active,title,cards,hint):
    hid=pid!=active; cls="price-panel is-hidden" if hid else "price-panel"; ha=" hidden" if hid else ""
    return (f'<div class="{cls}" data-price-panel="{pid}" id="panel-{pid}" role="tabpanel" aria-labelledby="tab-{pid}" tabindex="0"{ha}>'
            f'<h3 class="panel-title">{title}</h3><div class="grid price-grid">{cards}</div><p class="lead price-hint">{hint}</p></div>')

def deck_cards():
    return (price_card("Entry composite / WPC",'S$18–23<small>per ft² supply &amp; install</small>',"Price-conscious, straightforward installs",
              ["Entry-grade capped WPC","Standard colours &amp; detailing","Standard corrosion-resistant fixings"],"contact.html?service=decking&tier=essential",photo="assets/images/decking/product-wpc.webp",alt="Capped composite WPC decking boards",badge="Value")+
            price_card("Mid-range capped WPC",'S$24–32<small>per ft² supply &amp; install</small>',"Most homeowners seeking durability &amp; value",
              ["Upgraded capped WPC &amp; finish","Concealed / upgraded fixings","Better edge &amp; drainage detailing"],"contact.html?service=decking&tier=performance",featured=True,ribbon="Popular",photo="assets/images/decking/product-chengal.webp",alt="Warm-toned capped WPC decking",badge="Popular")+
            price_card("Premium / marble, tiles &amp; stone",'S$33–45+<small>per ft² supply &amp; install</small>',"Design-led, hardwood or stone finishes",
              ["Premium boards, Chengal, marble, tiles or stone","Aluminium subframe, complex edges &amp; steps","Upgraded hardware"],"contact.html?service=decking&tier=premium",photo="assets/images/decking/product-stone.webp",alt="Stone-look outdoor flooring",badge="Premium"))
def blind_cards():
    return (price_card("Manual zip blind",'S$18–28<small>per ft² supply &amp; install</small>',"Simple, reliable, budget-friendly",
              ["Manual side-track (zip-lock) operation","Solar-mesh fabric options","Standard track colours"],"contact.html?service=blinds&tier=manual",video="assets/videos/blinds/zipblind-manual.mp4",poster="assets/images/blinds/product-manual.webp",alt="Manual zip blind on a balcony",badge="Value")+
            price_card("Motorised zip blind",'S$25–35<small>per ft² supply &amp; install</small>',"Convenient daily use",
              ["Tubular motor &amp; remote","Solar-mesh or denser fabric","Electrical point coordinated"],"contact.html?service=blinds&tier=motorised",featured=True,ribbon="Popular",video="assets/videos/blinds/zipblind-motorised.mp4",poster="assets/images/blinds/product-motorised.webp",alt="Motorised zip blind lowering on a balcony",badge="Popular")+
            price_card("Premium / smart zip blind",'S$30–45+<small>per ft² supply &amp; install</small>',"Branded systems, app &amp; voice control",
              ["Premium branded system","Smart-home / app control","Premium fabric options"],"contact.html?service=blinds&tier=premium",video="assets/videos/blinds/zipblind-smart.mp4",poster="assets/images/blinds/product-smart.webp",alt="Smart zip blind with app control",badge="Premium"))
def grille_cards():
    return (price_card("Nylon fixed grille",'from S$8<small>per ft² · 3-year warranty</small>',"Indoor-facing balconies, value option",
              ["Stainless-steel core, nylon coating","Vertical cables · 50 mm or 100 mm","Physical sample provided"],"contact.html?service=grilles&product=nylon",photo="assets/images/grilles/product-nylon.webp",alt="Close view of a nylon-coated vertical cable grille",badge="Entry")+
            price_card("PTFE-coated fixed grille",'from S$10<small>per ft² · 5-year warranty</small>',"Most homes &amp; higher floors",
              ["Non-stick, UV-stable PTFE coating","Vertical cables · 50 mm or 100 mm","Physical sample provided"],"contact.html?service=grilles&product=ptfe",featured=True,ribbon="Popular",photo="assets/images/grilles/product-ptfe.webp",alt="Close view of a PTFE-coated vertical cable grille",badge="Most popular")+
            price_card("Nano all-weather grille",'from S$16<small>per ft² · 10-year warranty</small>',"Exposed / coastal balconies (premium)",
              ["Premium coating with supplier data sheet","Vertical cables · 50 mm or 100 mm","Longest warranty period"],"contact.html?service=grilles&product=nano",photo="assets/images/grilles/product-nano.webp",alt="Nano-coated stainless steel grille cables",badge="Top tier"))
def roof_cards():
    return (price_card("Manual retractable awning",'from S$800<small>per project (folding-arm)</small>',"Small balconies &amp; windows, budget",
              ["Hand-crank folding-arm awning","Acrylic or PVC-coated fabric","Powder-coated aluminium frame"],"contact.html?service=roof&tier=manual",photo="assets/images/roof/product-manual.webp",alt="Retractable fabric awning over an outdoor terrace",badge="Value")+
            price_card("Motorised retractable roof",'from S$2,500<small>per project (motor incl.)</small>',"Patios &amp; balconies, everyday use",
              ["Tubular motor &amp; remote","Shade, plus rain &amp; UV reduction","Optional wind / rain sensor"],"contact.html?service=roof&tier=motorised",featured=True,ribbon="Popular",video="assets/videos/roof/roof-motorised.mp4",poster="assets/images/roof/product-motorised.webp",alt="Hand using a remote to operate a motorised retractable roof",badge="Popular")+
            price_card("Premium cassette / louvered",'from S$6,000<small>per project</small>',"Landed patios, large spans, commercial",
              ["Full-cassette fabric roof or louvered pergola","Premium motor &amp; technical fabric (subject to selection)","Integrated LED &amp; concealed drainage options"],"contact.html?service=roof&tier=premium",photo="assets/images/roof/product-premium.webp",alt="Aluminium louvered pergola roof over an outdoor lounge",badge="Top tier"))

DECK_HINT="Complex raised decks, steps, aluminium subframes, difficult access or marble/tile/stone finishes are priced after survey."
BLIND_HINT='Tap ▶ on any card to watch that zip blind in action. Every zip blind carries our <a class="link-green" href="warranty.html">5-year warranty</a>. Standard condo balcony ≈ S$1,200–2,000 manual or S$1,800–2,800 motorised. Minimum panel ~30–32 ft². Electrical work quoted separately.'
GRILLE_HINT="Openable grilles, 50 mm spacing surcharge and the minimum-order value are confirmed after measurement. Physical cable samples provided on request."
ROOF_HINT=('Retractable roofs are quoted <strong>per project</strong> (span, projection, motor and fabric), not per ft². '
           'Indicative bands (Singapore, 2026): manual awning ≈ S$800–3,000; motorised roof ≈ S$2,500–6,000; premium cassette or louvered ≈ S$6,000–20,000+. '
           'Add-ons such as a wind/rain sensor, electrical point, scaffolding, PE endorsement and MCST/HDB approvals may apply.')

def tabs(active,label):
    T=[("decking","Balcony Decking"),("blinds","Zip Blinds"),("grilles","Invisible Grilles"),("roof","Retractable Roof")]
    btns="".join(f'<button type="button" role="tab" id="tab-{p}" aria-selected="{"true" if p==active else "false"}" aria-controls="panel-{p}" tabindex="{"0" if p==active else "-1"}" data-target="{p}">{l}</button>' for p,l in T)
    panels=(panel_wrap("decking",active,"Balcony decking planning packages",deck_cards(),DECK_HINT)+
            panel_wrap("blinds",active,"Zip blind planning packages",blind_cards(),BLIND_HINT)+
            panel_wrap("grilles",active,"Invisible-grille systems",grille_cards(),GRILLE_HINT)+
            panel_wrap("roof",active,"Retractable roof &amp; awning packages",roof_cards(),ROOF_HINT))
    return f'<div class="svc-toggle reveal" role="tablist" aria-label="{label}" data-price-toggle>{btns}</div>{panels}'

def rates_note():
    return ('<div class="price-note reveal"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 8h.01M11 12h1v4h1"/></svg>'
            '<span><strong>How to read these rates:</strong> decking, zip blinds and grilles are indicative supply-and-install ranges above the minimum order size; retractable roofs are quoted per project. Electrical work, restricted access, complex shapes, approvals and GST may be additional. Your exact price is confirmed at a free site survey.</span></div>')

def bundle():
    return f'''<div class="bundle reveal"><div>
    <span class="b-tag">★ All-in-1 · One Solution for All</span>
    <h2>Do it all together and save</h2>
    <p>Combine balcony decking, zip blinds, invisible grilles and a retractable roof in one project: one site survey, one schedule, one coordinated team and one warranty conversation — often at a better combined price than separate contractors.</p>
    <ul class="b-list"><li>Single itemised quote across every service</li><li>Details that align — deck height, blind tracks, grille anchors &amp; roof fixings planned together</li><li>One accountable team from survey to handover</li></ul></div>
    <div class="b-cta"><div class="b-save">Save up to 10%*</div><a href="contact.html?service=all" class="btn btn-gold">Get my All-in-1 quote</a><a href="complete-balcony-solution.html" class="btn btn-light">How it works</a></div></div>
    <p class="lead fineprint">*Indicative combined saving versus commissioning services separately; the exact saving is confirmed in your itemised quotation after a free site survey.</p>'''

def trust():
    items=[("Written warranties","Product, workmanship and manufacturer coverage — defined scope and claim process."),
           ("Real specifications","Product systems, coatings, fabrics, motors and fixings published — not vague claims."),
           ("Condo approval help","Guidance on MCST/HDB approved colours, working hours and paperwork."),
           ("Itemised quotes","Inclusions, exclusions and GST stated up front — no surprises.")]
    return f'<section class="section"><div class="container"><span class="eyebrow reveal">Why homeowners choose us</span><h2 class="section-title reveal">Specified properly. Installed carefully. Supported after.</h2><div class="grid feature-grid mt-2">'+"".join(f'<div class="feature-item reveal"><div class="ic">{CHECK}</div><h3>{t}</h3><p>{d}</p></div>' for t,d in items)+'</div></div></section>'

# --------- claims-safe FAQ answers ---------
FAQ_MCST=("Do you help with condo (MCST) or HDB approval?","Yes. We provide guidance on approved colours, working-hour restrictions and the documentation your management usually requests. Many condominiums require a <strong>renovation/management deposit paid by the home owner</strong> to the managing agent (MA) before work starts — typically refunded after inspection. We help prepare the submission; the <strong>MA deposit is arranged directly by the home owner</strong>.")
FAQ_5010=("What's the difference between 50 mm and 100 mm cable spacing?","<strong>100 mm</strong> spacing provides a more open appearance, while <strong>50 mm</strong> spacing provides a denser cable arrangement. The right choice depends on the opening, installation method, property requirements and your household's needs — we recommend a suitable option at the site survey and confirm the specification in your quotation.")
FAQ_ZIPWARR=("What does the zip blind warranty cover?","Our zip blind systems carry a <strong>5-year warranty</strong> on the scope described on our <a href='warranty.html'>Warranty page</a>. Servicing is <strong>free for the 1st and 2nd visits</strong>; the <strong>3rd, 4th and 5th visits carry a labour charge of S$250 each</strong>. Please give at least <strong>4 weeks' advance notice</strong> to schedule a repair or service.")
FAQ_ZIPTRAK=("Are zip blinds the same as ziptrak or zip-track?","These terms are commonly used when searching for side-retained outdoor blind systems, where the fabric edge runs inside side tracks. Specifications, components and branded systems differ. <em>Ziptrak® is a trademark of its owner; Balcony Master is independent and is not affiliated with third-party brands unless expressly stated.</em>")
FAQ_ROOFTM=("Is this the same as a “Skyline®” retractable roof or “smart awning”?","These names are commonly used when searching for motorised retractable awning and roof systems. Product design, specifications, components, motors, fabrics and performance vary by supplier and system. <em>Skyline® and other brand names are trademarks of their respective owners; Balcony Master is independent and is not affiliated with those brands unless expressly stated.</em>")

# ================= HOME (simplified pricing) =================
def home():
    faqs=[("How much does a balcony makeover cost in Singapore?","As indicative planning ranges: balcony decking S$18–45+/ft², zip blinds S$18–45+/ft², invisible grilles from S$8/ft², and a motorised retractable roof from about S$2,500 per project. Combining services is often cheaper than separate contractors. Final pricing follows a free site survey."),
        FAQ_ROOFTM, FAQ_ZIPTRAK, FAQ_5010, FAQ_MCST]
    from_grid=('<div class="from-grid reveal">'
        '<div class="from-card"><span class="fc-tag">Flooring</span><h3>Balcony decking</h3><div class="fc-amt">from S$18<small>per ft²</small></div></div>'
        '<div class="from-card"><span class="fc-tag">Weather</span><h3>Zip blinds</h3><div class="fc-amt">from S$18<small>per ft²</small></div></div>'
        '<div class="from-card"><span class="fc-tag">Safety</span><h3>Invisible grilles</h3><div class="fc-amt">from S$8<small>per ft²</small></div></div>'
        '<div class="from-card"><span class="fc-tag">Shade &amp; rain</span><h3>Retractable roof</h3><div class="fc-amt">from S$800<small>per project</small></div></div>'
        '</div>')
    body=f'''
<section class="hero" aria-label="Introduction"><div class="hero-media">
    <img src="assets/images/hero-1536.webp" srcset="assets/images/hero-768.webp 768w, assets/images/hero-1200.webp 1200w, assets/images/hero-1536.webp 1536w" sizes="100vw" width="1536" height="1024" alt="Singapore balcony with composite decking, motorised zip blinds, an invisible grille railing and a retractable roof at golden hour" fetchpriority="high">
    <video data-hero-video muted loop playsinline preload="none" poster="assets/images/hero-poster.webp" src="assets/videos/hero.mp4" aria-hidden="true"></video></div>
  <div class="container hero-inner"><span class="eyebrow">Decking · Zip Blinds · Invisible Grilles · Retractable Roof</span>
    <h1>Balcony Decking, Zip Blinds, Grilles<br>&amp; Retractable Roofs</h1>
    <p>Balcony Master is your one solution for all — supplied and installed across HDB, condo and landed homes in Singapore, with clear specs, honest prices and dependable warranties.</p>
    <div class="hero-actions"><a href="contact.html" class="btn btn-primary">Get a site-measured quote</a><a href="projects.html" class="btn btn-light">See completed work</a></div>
    <div class="hero-trust"><div>{CHECK} Four services, one team</div><div>{CHECK} 5-year zip blind warranty</div><div>{CHECK} Call {PHONE_D}</div></div>
  </div></section>

<section class="section"><div class="container">
  <span class="eyebrow reveal">One specialist, four layers</span>
  <h2 class="section-title reveal">Everything your outdoor space needs, under one roof</h2>
  <p class="lead reveal">Balcony decking for the floor, zip blinds for weather control, invisible grilles for safety, and a motorised retractable roof for shade and rain cover — planned together so every detail works as a system.</p>
  <div class="grid services-grid">
    <article class="service-card reveal"><a href="balcony-decking-singapore.html" class="thumb"><img src="assets/images/decking/service-decking-small.webp" width="900" height="600" alt="Capped composite WPC decking boards on a sunny Singapore balcony" loading="lazy"><span class="badge">Flooring</span></a>
      <div class="service-body"><span class="service-tag">Flooring</span><h3>Balcony Decking</h3><p>Capped WPC / composite, Chengal, and outdoor marble, tiles and stone on detailed subframes.</p><a class="service-link" href="balcony-decking-singapore.html">Explore decking {ARROW}</a></div></article>
    <article class="service-card reveal"><a href="zip-blinds-singapore.html" class="thumb"><img src="assets/images/blinds/service-blinds-small.webp" width="900" height="600" alt="Motorised zip blinds enclosing a Singapore condo balcony" loading="lazy"><span class="badge">Weather</span></a>
      <div class="service-body"><span class="service-tag">Weather control</span><h3>Zip Blinds</h3><p>Manual &amp; motorised zip blinds — reduce heat, glare &amp; wind-driven rain. 5-year warranty.</p><a class="service-link" href="zip-blinds-singapore.html">Explore zip blinds {ARROW}</a></div></article>
    <article class="service-card reveal"><a href="invisible-grille-singapore.html" class="thumb"><img src="assets/images/grilles/service-grilles-small.webp" width="900" height="600" alt="Vertical stainless steel invisible grille cables on a Singapore balcony" loading="lazy"><span class="badge">Safety</span></a>
      <div class="service-body"><span class="service-tag">Safety</span><h3>Invisible Grilles</h3><p>Vertical-cable Nylon, PTFE and Nano invisible grilles in 50 or 100&nbsp;mm spacing.</p><a class="service-link" href="invisible-grille-singapore.html">Explore grilles {ARROW}</a></div></article>
    <article class="service-card reveal"><a href="retractable-roof-singapore.html" class="thumb"><img src="assets/images/roof/service-roof-small.webp" width="900" height="600" alt="Motorised retractable roof over a Singapore landed patio, half-retracted showing blue sky" loading="lazy"><span class="badge">Shade &amp; rain</span></a>
      <div class="service-body"><span class="service-tag">Roofing</span><h3>Retractable Roof</h3><p>Motorised retractable roofs &amp; awnings — fully retractable outdoor roofing for shade and rain cover.</p><a class="service-link" href="retractable-roof-singapore.html">Explore retractable roof {ARROW}</a></div></article>
  </div>
</div></section>

<section class="section alt"><div class="container">
  <span class="eyebrow reveal">A look at the finished result</span><h2 class="section-title reveal">See the work</h2>
  <p class="lead reveal">A selection of completed outdoor spaces — the systems and details we specify for homes like yours.</p>
  <div class="grid projects-grid">
    <a class="project big reveal" href="projects.html"><img src="assets/images/projects/condo-balcony-wpc-01.webp" width="1200" height="800" alt="Condo balcony with decking, zip blinds and an invisible grille, skyline view" loading="lazy"><div class="project-meta"><span class="t">Condo · All-in-1</span><h3>Skyline balcony</h3><p>Decking · zip blinds · grille</p></div></a>
    <a class="project reveal" href="projects.html"><img src="assets/images/projects/retractable-roof-01.webp" width="1200" height="800" alt="Landed patio with a motorised retractable roof" loading="lazy"><div class="project-meta"><span class="t">Landed · Roof</span><h3>Retractable patio roof</h3><p>Motorised · folding fabric</p></div></a>
    <a class="project reveal" href="projects.html"><img src="assets/images/projects/motorised-zip-blinds-01.webp" width="1200" height="800" alt="Balcony enclosed with motorised zip blinds" loading="lazy"><div class="project-meta"><span class="t">Condo · Zip blinds</span><h3>Motorised enclosure</h3><p>2 panels · solar mesh</p></div></a>
    <a class="project reveal" href="projects.html"><img src="assets/images/projects/nano-grille-01.webp" width="1200" height="800" alt="Vertical invisible grille cables on a balcony" loading="lazy"><div class="project-meta"><span class="t">Safety</span><h3>Invisible grille</h3><p>50 / 100 mm spacing</p></div></a>
  </div>
  <div class="center mt-2"><a href="projects.html" class="btn btn-ghost">Browse the full gallery {ARROW}</a></div>
</div></section>

<section class="section"><div class="container">
  <span class="eyebrow reveal">Transparent starting prices</span><h2 class="section-title reveal">Indicative starting prices</h2>
  <p class="lead reveal">A quick view of where each service starts. Every rate is a planning starting point; final pricing follows a free site survey.</p>
  {from_grid}
  <div class="center mt-2"><a href="price-guide.html" class="btn btn-primary">Compare all packages {ARROW}</a></div>
  {bundle()}
  {rates_note()}
</div></section>

{trust()}
{faq_section(faqs)}
{quote_section()}
'''
    write("index.html","Balcony Decking, Zip Blinds, Grilles & Retractable Roof Singapore | Balcony Master",
          "Balcony Master (lionsin.com.sg) — balcony decking, zip blinds, invisible grilles and motorised retractable roofs in Singapore for HDB, condo & landed. Transparent prices. Call 8341 7888.",
          body,trail=[("Home","./")],faqs=[(q,plain(a)) for q,a in faqs],active="",home=True)

# ============ service pages ============
def service_page(path,title,desc,eyebrow,h1,hero_p,intro,spec,active_pid,faqs,service_key,trail_label,svc_node,rel):
    body=f'''
<section class="page-hero"><div class="container"><span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p>{hero_p}</p>
  <div class="hero-actions mt-1"><a href="contact.html?service={service_key}" class="btn btn-primary">Get a quote for this</a><a href="price-guide.html" class="btn btn-light">See full price guide</a></div></div></section>
<section class="section"><div class="container"><div class="prose reveal">{intro}</div></div></section>
<section class="section alt"><div class="container"><span class="eyebrow reveal">Specifications</span><h2 class="section-title reveal">Compare the options</h2><div class="table-wrap reveal mt-2">{spec}</div></div></section>
<section class="section"><div class="container"><span class="eyebrow reveal">Planning ranges</span><h2 class="section-title reveal">Indicative pricing</h2><p class="lead reveal">Planning starting points — confirmed at a free site survey.</p>{tabs(active_pid,"Choose a service")}{rates_note()}</div></section>
{faq_section(faqs)}
{rel}
{quote_section(service_key)}
'''
    write(path,title,desc,body,trail=[("Home","./"),(trail_label,None)],faqs=[(q,plain(a)) for q,a in faqs],service=svc_node,active=path)

def page_decking():
    intro='''
<h2>Balcony decking in Singapore</h2>
<p><strong>Balcony decking</strong> turns bare tiles or screed into a warm, usable outdoor room. We supply and install <strong>capped WPC (composite) decking</strong>, natural <strong>Chengal and Balau hardwood</strong>, and outdoor <strong>marble, porcelain tiles and stone</strong> on detailed subframes — with drainage falls, corrosion-resistant fixings and clean edge trims.</p>
<p>Installed balcony decking runs from roughly <strong>S$18 per ft²</strong> for entry composite (market average near S$27) to above <strong>S$45 per ft²</strong> for premium hardwood or stone.</p>
<h3>Composite (WPC) vs Chengal vs marble &amp; stone</h3>
<ul><li><strong>Capped WPC / composite:</strong> low-maintenance, colour-stable, resistant to rot and termites.</li>
<li><strong>Chengal &amp; Balau hardwood:</strong> dense tropical timbers, warm grain; weather to silver-grey unless oiled.</li>
<li><strong>Outdoor marble, porcelain tiles &amp; stone:</strong> cool underfoot, easy to clean — suited to pool surrounds.</li></ul>
<div class="callout">Substructure, drainage, access and complex shapes affect price. An itemised quotation after survey is more useful than a board-only rate.</div>'''
    spec=table(["Option","Feel & look","Upkeep","Best for","Planning from"],[
        ["Entry composite / WPC","Uniform, modern","Low","Value balconies","S$18–23 / ft²"],
        ["Mid-range capped WPC","Richer texture, colour-stable","Low","Most homeowners","S$24–32 / ft²"],
        ["Premium composite / Chengal","Natural grain, premium","Medium","Landed patios","S$33–45+ / ft²"],
        ["Marble, tiles &amp; stone","Stone-like, cool","Low","Pool surrounds","Price on survey"]])
    faqs=[("How much does balcony decking cost in Singapore?","Installed balcony decking commonly starts around S$18 per ft² for entry composite and can exceed S$45 per ft² for premium hardwood or stone, depending on finish, subframe, drainage and access."),
        ("Composite or Chengal — which is better?","Capped WPC is lower-maintenance and colour-stable; Chengal is a premium hardwood that can be oiled to retain colour. Both perform well on a ventilated subframe with drainage. We recommend based on your exposure, look and budget."),FAQ_MCST]
    rel=related("Related searches we cover",[("Balcony decking Singapore","balcony-decking-singapore.html"),("Composite / WPC decking","balcony-decking-singapore.html"),("Chengal decking","balcony-decking-singapore.html"),("Balcony decking price","price-guide.html"),("Decking + roof + blinds bundle","complete-balcony-solution.html")])
    svc=service_node("Balcony decking supply and installation","Supply and installation of composite (WPC), Chengal hardwood, and marble/tile/stone balcony decking in Singapore.",[("Entry composite / WPC decking","18"),("Mid-range capped WPC decking","24"),("Premium / marble, tiles & stone decking","33")],"balcony-decking-singapore.html")
    service_page("balcony-decking-singapore.html","Balcony Decking Singapore | Composite, Chengal, Marble & Stone | Balcony Master",
        "Balcony decking in Singapore — capped WPC/composite, Chengal & Balau hardwood, and outdoor marble, tiles and stone. From S$18/ft². Free site survey. Call 8341 7888.",
        "Balcony decking","Balcony Decking in Singapore","Capped WPC/composite, Chengal, and outdoor marble, tiles and stone — on detailed subframes with drainage and corrosion-resistant fixings.",
        intro,spec,"decking",faqs,"decking","Balcony decking",svc,rel)

def page_blinds():
    intro='''
<h2>Zip blinds in Singapore</h2>
<p><strong>Zip blinds</strong> are side-retained outdoor blinds: the fabric edge runs inside side tracks so the screen stays taut and greatly reduces heat, glare, wind and wind-driven rain. Choose <strong>manual or motorised</strong>, with solar-mesh or blockout fabrics. Every zip blind we install carries our <strong>5-year warranty</strong> (see the <a href="warranty.html">Warranty page</a> for scope).</p>
<p><em>The terms “zipblind” and “ziptrak / zip-track” are commonly used when searching for this product category. Ziptrak® is a trademark of its owner; Balcony Master is independent and is not affiliated with third-party brands unless expressly stated.</em></p>
<p>Guide prices: manual ≈ <strong>S$18–28/ft²</strong>, motorised ≈ <strong>S$25–35/ft²</strong>, premium/smart ≈ <strong>S$30–45+/ft²</strong>, minimum panel ~30–32 ft².</p>
<div class="callout">Zip blinds reduce glare, heat and wind-driven rain — subject to site exposure and operating conditions. We do not describe a blind as fully "waterproof" without test reports covering the exact product.</div>'''
    spec=table(["Openness","Light control","Outward view","Best for","Planning"],[
        ["0–1% Blackout","Highest","Low","Privacy, west sun","S$18–35+ / ft²"],
        ["5% ScreenView","High","Balanced","Everyday balconies","S$18–35+ / ft²"],
        ["10% Ventilation","Medium","Good","Airflow with shade","S$18–35+ / ft²"],
        ["30% Insect screen","Low","Highest","Ventilation","S$18–35+ / ft²"]])
    faqs=[FAQ_ZIPTRAK,("How much do zip blinds cost in Singapore?","About S$18–28/ft² manual, S$25–35/ft² motorised, S$30–45+/ft² premium/smart, minimum panel ~30–32 ft². A standard condo balcony is often S$1,200–2,000 manual or S$1,800–2,800 motorised."),FAQ_ZIPWARR,("Can zip blinds stop rain completely?","They dramatically reduce wind-driven rain, heat and glare and make a balcony usable in most weather. No zip blind system is fully watertight in every wind-driven-rain condition — we match fabric density and detailing to your exposure."),FAQ_MCST]
    rel=related("Related searches we cover",[("Zip blinds Singapore","zip-blinds-singapore.html"),("Zipblind / ziptrak","zip-blinds-singapore.html"),("Motorised outdoor blinds","zip-blinds-singapore.html"),("Balcony blinds price","price-guide.html"),("Zip blinds + roof bundle","complete-balcony-solution.html")])
    svc=service_node("Zip blind supply and installation","Supply and installation of manual and motorised zip blinds (side-retained outdoor blinds) for HDB, condo and landed balconies. 5-year warranty on the described scope.",[("Manual zip blind","18"),("Motorised zip blind","25"),("Premium / smart zip blind","30")],"zip-blinds-singapore.html")
    service_page("zip-blinds-singapore.html","Zip Blinds Singapore (Zipblind / Ziptrak-style) | Balcony Master",
        "Zip blinds in Singapore — manual & motorised side-retained outdoor blinds (also searched as zipblind or ziptrak). S$18–45+/ft², 5-year warranty. Call 8341 7888.",
        "Zip blinds","Zip Blinds in Singapore","Manual and motorised side-retained outdoor blinds — reduce heat, glare, wind and wind-driven rain. 5-year warranty on the described scope.",
        intro,spec,"blinds",faqs,"blinds","Zip blinds",svc,rel)

def page_grilles():
    intro='''
<h2>Invisible grille in Singapore</h2>
<p><strong>Invisible grilles</strong> use fine, tensioned stainless-steel cables — laid <strong>vertically</strong> between slim aluminium tracks — a near-invisible barrier that keeps your view, light and airflow. Available in 50&nbsp;mm or 100&nbsp;mm spacing, in three coatings.</p>
<p>Standard fixed installations commonly run <strong>S$8–10 per ft²</strong> (some guides S$7–15), with promotions from about <strong>S$4.90/ft²</strong>; a fixed balcony ranges roughly S$480–3,000.</p>
<h3>Nylon vs PTFE vs Nano</h3>
<ul><li><strong>Nylon — from S$8/ft², 3-year.</strong> Value option.</li><li><strong>PTFE-coated — from S$10/ft², 5-year.</strong> Non-stick, UV-stable. (PTFE is also commonly known as Teflon™.)</li><li><strong>Nano all-weather — from S$16/ft², 10-year.</strong> Premium; supplier data on request.</li></ul>
<div class="callout">We confirm the stainless grade, cable diameter, track spec and written warranty scope in your quotation. Cable spacing changes the appearance and density; suitability for any household is assessed at the survey rather than stated as a general safety assurance.</div>'''
    spec=table(["Coating","Core","Warranty","Best for","Planning from"],[
        ["Nylon-coated","Stainless-steel wire","3-year","Value","S$8 / ft²"],
        ["PTFE-coated","304/316 stainless","5-year","Higher floors","S$10 / ft²"],
        ["Nano all-weather","Premium 316","10-year","Coastal","S$16 / ft²"],
        ["Openable system","As specified","As specified","Cleaning access","On survey"]])
    faqs=[("How much does an invisible grille cost in Singapore?","Standard fixed invisible grilles commonly fall around S$8–10 per ft² (some guides S$7–15), promotions from ~S$4.90/ft². A fixed balcony ranges roughly S$480–3,000; openable systems cost more."),FAQ_5010,("Which coating should I choose — Nylon, PTFE or Nano?","Nylon is the value option (3-year); PTFE is non-stick and UV-stable (5-year); Nano is a premium all-weather coating (10-year). We provide physical samples and confirm the stainless grade, cable diameter and warranty scope in your quotation."),FAQ_MCST]
    rel=related("Related searches we cover",[("Invisible grille Singapore","invisible-grille-singapore.html"),("Invisible grille price","price-guide.html"),("Invisible grille HDB","invisible-grille-singapore.html"),("Balcony invisible grille","invisible-grille-singapore.html"),("Grille + roof bundle","complete-balcony-solution.html")])
    svc=service_node("Invisible grille supply and installation","Supply and installation of vertical-cable invisible grilles (Nylon, PTFE, Nano) for HDB, condo and landed balconies in 50 mm or 100 mm spacing.",[("Nylon fixed grille","8"),("PTFE-coated fixed grille","10"),("Nano all-weather fixed grille","16")],"invisible-grille-singapore.html")
    service_page("invisible-grille-singapore.html","Invisible Grille Singapore | Nylon, PTFE & Nano (Vertical) | Balcony Master",
        "Invisible grille in Singapore — vertical-cable Nylon (from S$8/ft²), PTFE (from S$10/ft²) & Nano (from S$16/ft²), 50mm or 100mm. Free site survey. Call 8341 7888.",
        "Invisible grilles","Invisible Grille in Singapore","Vertical-cable Nylon, PTFE and Nano invisible grilles in 50 mm or 100 mm spacing — verified specs and written warranties.",
        intro,spec,"grilles",faqs,"grilles","Invisible grilles",svc,rel)

def page_roof():
    intro='''
<h2>Retractable roof &amp; motorised awning in Singapore</h2>
<p>A <strong>retractable roof</strong> (also called a <strong>motorised retractable awning</strong>, <strong>smart awning</strong> or <strong>fully retractable outdoor roofing</strong>) turns a balcony, patio, pool deck or rooftop into a more usable space. At the touch of a button the fabric or louvered roof extends for shade and rain cover, or retracts for open sky and breeze.</p>
<p><em>“Skyline®”, “smart awning” and similar names are commonly used when searching for this product category. Product design, specifications, components, motors, fabrics and performance vary by supplier and system. Skyline® and other brand names are trademarks of their respective owners; Balcony Master is independent and is not affiliated with those brands unless expressly stated.</em></p>
<h3>Types we install</h3>
<ul><li><strong>Manual retractable awning (folding-arm):</strong> hand-crank shade for smaller balconies and windows — the most budget-friendly option.</li>
<li><strong>Motorised retractable roof:</strong> tubular motor and remote; optional wind/rain sensors that can auto-retract in windy conditions. A popular all-rounder for patios and balconies.</li>
<li><strong>Premium full-cassette fabric roof or louvered pergola:</strong> an aluminium cassette that protects the fabric, or adjustable aluminium louvers, with integrated LED and concealed drainage options — for larger spans, landed homes and commercial spaces.</li></ul>
<h3>What you're paying for</h3>
<ul><li><strong>Fabric:</strong> solution-dyed acrylic, micro-perforated technical fabric, or PVC-coated; fire-retardant options are available where SCDF/MCST submission is required. Specific brands are confirmed by selection at quotation.</li>
<li><strong>Frame:</strong> powder-coated aluminium; marine-grade specification for coastal homes.</li>
<li><strong>Motor &amp; controls:</strong> premium or standard motors, with optional wind/rain/sun sensors and smart-home control. Specific motor and fabric brands are subject to selection and availability.</li></ul>
<div class="callout">Retractable roofs are quoted <strong>per project</strong> — span, projection, motor, fabric and site access all matter. The system provides <strong>shade and helps reduce rain and UV</strong>; the degree of weather protection depends on the specific system, pitch, drainage and exposure, and is confirmed in writing in your quotation.</div>
<h3>Regulations &amp; hidden costs</h3>
<ul><li><strong>HDB:</strong> engage an HDB-registered contractor; fixings and boundary rules apply.</li>
<li><strong>Condo:</strong> MCST approval and design-guide colours; a renovation deposit is paid by the home owner to the MA.</li>
<li><strong>Landed:</strong> larger permanent structures may require a Professional Engineer (PE) endorsement for BCA/URA.</li>
<li>Common add-ons: electrical point, scaffolding for high installs, a wind/rain sensor, and disposal of any old unit.</li></ul>'''
    spec=table(["Type","Operation","Roof","Best for","Planning from"],[
        ["Manual retractable awning","Hand crank","Folding-arm fabric","Small balconies, windows","S$800 / project"],
        ["Motorised retractable roof","Motor + remote","Folding fabric, sensors optional","Patios &amp; balconies","S$2,500 / project"],
        ["Full-cassette fabric roof","Motor + remote","Cassette-protected fabric","Landed, larger spans","S$6,000 / project"],
        ["Louvered pergola","Motor + app","Adjustable aluminium louvers","Premium / commercial","Quotation on survey"]])
    faqs=[FAQ_ROOFTM,
        ("How much does a retractable roof cost in Singapore?","As indicative bands (2026): a manual folding-arm awning is roughly S$800–3,000; a motorised retractable roof about S$2,500–6,000; and a premium full-cassette fabric roof or louvered pergola from about S$6,000 to S$20,000+. Final price depends on span, projection, motor, fabric and site access."),
        ("Is a retractable roof waterproof?","It provides shade and helps reduce rain and UV, and premium fabric or louvered systems shed rain effectively with the right pitch and drainage. No retractable roof is described as fully watertight in every wind-driven-rain condition — we confirm the system, pitch and drainage for your exposure in writing."),
        ("Manual, motorised or louvered — which should I choose?","Manual suits small balconies and tight budgets; motorised suits everyday patio use and can auto-retract with a wind/rain sensor; a louvered pergola gives adjustable slats, ventilation and the most premium, permanent finish. We advise based on span, exposure and budget."),
        FAQ_MCST]
    rel=related("Related searches we cover",[("Retractable roof Singapore","retractable-roof-singapore.html"),("Motorised retractable awning","retractable-roof-singapore.html"),("Outdoor roofing / smart awning","retractable-roof-singapore.html"),("Louvered pergola roof","retractable-roof-singapore.html"),("Retractable roof price","price-guide.html"),("Roof + decking + blinds bundle","complete-balcony-solution.html")])
    svc=service_node("Retractable roof and awning supply and installation","Supply and installation of manual and motorised retractable roofs and awnings — fully retractable outdoor roofing for balconies, patios, pool decks and rooftops in Singapore.",[("Manual retractable awning","800"),("Motorised retractable roof","2500"),("Premium cassette / louvered pergola","6000")],"retractable-roof-singapore.html")
    service_page("retractable-roof-singapore.html","Retractable Roof Singapore | Motorised Retractable Awning & Outdoor Roofing | Balcony Master",
        "Retractable roof in Singapore — motorised retractable awnings & fully retractable outdoor roofing for balconies, patios & rooftops. From S$800 per project. Call 8341 7888.",
        "Retractable roof","Retractable Roof &amp; Motorised Awning in Singapore","Motorised retractable roofs and awnings — fully retractable outdoor roofing for shade and rain cover on balconies, patios, pool decks and rooftops.",
        intro,spec,"roof",faqs,"roof","Retractable roof",svc,rel)

# ============ other pages ============
def page_complete():
    body=f'''
<section class="page-hero"><div class="container"><span class="eyebrow">All-in-1 · One Solution for All</span><h1>The Complete Balcony Solution</h1>
  <p>Balcony decking, zip blinds, invisible grilles and a retractable roof — surveyed once, specified together, installed in the right sequence, and often priced better as a bundle.</p>
  <div class="hero-actions mt-1"><a href="contact.html?service=all" class="btn btn-primary">Plan my All-in-1 balcony</a><a href="projects.html" class="btn btn-light">See projects</a></div></div></section>
<section class="section"><div class="container">{bundle()}</div></section>
<section class="section alt"><div class="container"><div class="prose reveal"><h2>Why plan them together</h2>
  <p>Decking height, blind tracks, grille anchors and roof fixings all compete for the same edges. Coordinating them avoids clashes, reduces rework and keeps one team accountable — and it often costs less than hiring separate contractors.</p><h3>The right installation sequence</h3></div>
  <div class="grid steps mt-2">
    <div class="step reveal"><div class="n">1</div><h3>Survey &amp; design</h3><p>Measure floor, enclosure, safety line and roof span together; confirm MCST/HDB needs.</p></div>
    <div class="step reveal"><div class="n">2</div><h3>Roof &amp; grilles</h3><p>Fix roof structure and vertical cable anchors while access is clear.</p></div>
    <div class="step reveal"><div class="n">3</div><h3>Decking</h3><p>Set subframe, drainage falls and boards to the correct finished height.</p></div>
    <div class="step reveal"><div class="n">4</div><h3>Zip blinds</h3><p>Install tracks, fabric and any motor/electrical last, aligned to the deck and roof.</p></div>
  </div></div></section>
{quote_section("all")}'''
    write("complete-balcony-solution.html","All-in-1 Balcony Package Singapore | Decking + Blinds + Grilles + Roof | Balcony Master",
        "Balcony Master All-in-1: balcony decking, zip blinds, invisible grilles and a retractable roof surveyed once and installed together — one itemised quote, often at a better bundled price. Call 8341 7888.",
        body,trail=[("Home","./"),("All-in-1",None)],active="complete-balcony-solution.html")

def gcat(cat,icon,title,blurb):
    return f'<div class="gallery-cat reveal"><div class="gallery-cat-head"><div class="gc-ic" aria-hidden="true">{icon}</div><h2>{title}</h2><p>{blurb}</p></div><div class="media-grid" data-gallery="{cat}"></div></div>'
def page_projects():
    body=f'''
<section class="page-hero"><div class="container"><span class="eyebrow">A look at the finished result</span><h1>Completed installations</h1>
  <p>Balcony decking, zip blind, invisible grille and retractable roof installations for HDB, condo and landed homes. Tap any photo or video to view it larger.</p></div></section>
<section class="section"><div class="container">
  {gcat("decking","🪵","Balcony decking","Composite (WPC), Chengal hardwood, and marble/tile/stone finishes.")}
  {gcat("blinds","🌧️","Zip blinds","Manual and motorised zip blind enclosures with solar-mesh fabrics.")}
  {gcat("grilles","🛡️","Invisible grilles","Vertical-cable Nylon, PTFE and Nano systems in 50 mm or 100 mm spacing.")}
  {gcat("roof","☂️","Retractable roofs","Motorised retractable roofs, cassette awnings and louvered pergolas.")}
</div></section>
{quote_section()}'''
    write("projects.html","Projects | Decking, Zip Blinds, Grilles & Retractable Roof Singapore | Balcony Master",
        "Completed Singapore projects by Balcony Master — balcony decking, zip blinds, invisible grilles and retractable roofs, with photo and video galleries.",
        body,trail=[("Home","./"),("Projects",None)],active="projects.html",
        extra_js='<script src="data/projects.js" defer></script>\n<script src="js/gallery.js" defer></script>')

def page_price():
    body=f'''
<section class="page-hero"><div class="container"><span class="eyebrow">Transparent planning ranges</span><h1>Singapore price guide 2026</h1>
  <p>Indicative supply-and-install planning ranges. Decking, zip blinds and grilles are priced per ft²; retractable roofs are quoted per project. Bundle and save.</p></div></section>
<section class="section"><div class="container">
  {tabs("decking","Choose a service")}
  {bundle()}
  {rates_note()}
  <div class="prose reveal mt-2"><h2>What changes your final price</h2>
    <ul><li><strong>Balcony decking:</strong> finish (WPC, Chengal, marble/tile/stone), subframe, drainage, access and complex shapes.</li>
    <li><strong>Zip blinds:</strong> opening size, panels, motor, fabric openness, electrical work, minimum panel (~30–32 ft²).</li>
    <li><strong>Invisible grilles:</strong> stainless grade, cable diameter, track, 50 vs 100 mm, fixed vs openable, install height.</li>
    <li><strong>Retractable roof:</strong> span &amp; projection, manual/motorised/louvered, motor &amp; fabric grade, sensors, electrical work, scaffolding, PE endorsement and approvals.</li></ul></div>
</div></section>
{quote_section()}'''
    write("price-guide.html","Price Guide 2026 | Decking, Zip Blinds, Grilles & Retractable Roof Singapore",
        "2026 Singapore price guide — balcony decking (from S$18/ft²), zip blinds (S$18–45+/ft²), invisible grilles (from S$8/ft²) and retractable roofs (from S$800/project). Call 8341 7888.",
        body,trail=[("Home","./"),("Price guide",None)],active="price-guide.html")

# ---- Warranty (seller-protective) ----
def warr_card(name,term,cov,exc,extra=None,hl=False,sched=""):
    c="".join(f"<li>{x}</li>" for x in cov); e="".join(f"<li>{x}</li>" for x in exc)
    ex=f'<h4>Conditions</h4><ul>{"".join(f"<li>{x}</li>" for x in extra)}</ul>' if extra else ""
    return f'<div class="warr-card{" hl" if hl else ""} reveal"><div class="wh"><h3>{name}</h3><span class="term">{term}</span></div>{sched}<h4>What is covered</h4><ul>{c}</ul><h4>What is NOT covered</h4><ul class="excl">{e}</ul>{ex}</div>'
def page_warranty():
    ce=["Damage from misuse, accident, alteration, relocation, or work by anyone not authorised by us",
        "Normal wear, weathering, fading, patina and colour change over time",
        "Damage from extreme weather, storms, wind above the product's stated limits, falling objects, pests, vandalism or force majeure",
        "Movement, cracking or water ingress originating from the building structure, tiling or existing waterproofing",
        "Cosmetic marks, minor tonal variation and characteristics inherent to natural or outdoor materials",
        "Any consequential, incidental or indirect loss, including loss of use, of any kind"]
    cc=["Warranty is non-transferable and applies to the original paying customer at the installed address",
        "Valid only when the invoice is paid in full and the product is used and maintained as advised",
        "Defects must be reported to us in writing; we must be given access to inspect before any remedy is attempted",
        "Our sole obligation, and your exclusive remedy, is repair or replacement of the defective part, at our option, using the same or an equivalent component",
        "Repairs or parts supplied under warranty do not extend or restart the original warranty period",
        "A call-out/inspection fee applies to no-fault visits and to issues found to be outside the warranty scope"]
    liability=["To the maximum extent permitted by law, our total aggregate liability for any claim is limited to the price paid for the affected product",
        "Warranties are limited to the specific defects and periods stated here and in your quotation; no other warranty, condition or representation (including fitness for a particular purpose) is given except as required by law",
        "Nothing in this warranty excludes rights that cannot be excluded under applicable Singapore law"]
    sched=('<h4>Service visits during the 5-year warranty</h4><table class="svc-sched"><thead><tr><th scope="col">Service visit</th><th scope="col">Labour charge</th></tr></thead><tbody>'
           '<tr><td>1st visit</td><td class="free">FREE</td></tr><tr><td>2nd visit</td><td class="free">FREE</td></tr>'
           '<tr><td>3rd visit</td><td class="paid">S$250</td></tr><tr><td>4th visit</td><td class="paid">S$250</td></tr><tr><td>5th visit</td><td class="paid">S$250</td></tr></tbody></table>'
           '<p class="warr-note">Please give at least <strong>4 weeks\u2019 advance notice</strong> to schedule any repair or service visit. Parts/materials, motor/electrical faults and out-of-scope items are quoted separately.</p>')
    cards=(warr_card("Zip Blind System","5-year",
              ["Fabric, tracks, bottom bar and side-lock components against manufacturing defects for 5 years","Workmanship of our installation (fixings, alignment, tensioning) for 5 years","Re-tensioning and adjustment arising from our installation, within the service schedule"],
              ce+["Wind damage when the blind is left down in strong wind against our advice","Water ingress in wind-driven rain (zip blinds reduce, but do not eliminate, rain)","Fabric soiling, mould from lack of cleaning, and pet damage"],
              cc+["The blind must be raised in stormy / high-wind conditions as advised","Motor, remote and smart-control electronics follow the manufacturer's own warranty","At least 4 weeks' notice is required to schedule any service or repair visit"],hl=True,sched=sched)+
           warr_card("Retractable Roof / Awning","Frame per maker · 1-yr workmanship",
              ["Frame, arms, cassette and fabric against manufacturing defects per the maker's terms","Workmanship of our installation (brackets, fixings, alignment) for 12 months","Re-alignment arising from our installation within 12 months"],
              ce+["Fabric stretch, minor ripple and colour change inherent to outdoor fabric","Water ingress in wind-driven rain (a retractable roof reduces, but does not eliminate, rain)","Damage from operating in wind above the product's stated limit, or from leaves/debris/pooled water left on the fabric"],
              cc+["The roof must be retracted in strong-wind / storm conditions as advised, or the wind sensor used where fitted","Motor, sensors, remote and smart controls follow the manufacturer's own warranty","Periodic cleaning of fabric, gutters and drainage is the owner's responsibility"])+
           warr_card("Retractable Roof — motor & sensors (if selected)","Motor per manufacturer",
              ["Tubular motor, receiver and wind/rain sensor defects per the manufacturer's warranty","Remote pairing/setup issues reported within the workmanship period"],
              ce+["Damage from incorrect power supply, power surges or unauthorised electrical work","Batteries, remotes and third-party smart-home integration issues","Water damage from exposure beyond the motor's IP rating"],
              cc+["Electrical supply must comply with our specification and be installed by a licensed electrician"])+
           warr_card("Balcony Decking (WPC / Chengal / stone)","Product + 1-yr workmanship",
              ["Manufacturing defects in supplied boards/tiles per the maker's terms","Workmanship defects in our subframe &amp; fixings for 12 months","Re-securing of any board that lifts due to our installation within 12 months"],
              ce+["Oiling/sealing of natural timber and routine cleaning","Heat build-up, minor expansion/contraction and natural timber movement","Furniture, planter, footfall scratching or staining"],cc)+
           warr_card("Invisible Grille — Nylon","3-year limited",["Cable, coating and track defects under normal residential use for 3 years","One complimentary re-tensioning within the first 12 months","Anchor/fixing workmanship for the warranty period"],ce+["Coating wear from abrasion, cleaning chemicals or pets","Corrosion where cables are cut, drilled or modified after install","Sagging caused by hanging objects or loads on the cables"],cc)+
           warr_card("Invisible Grille — PTFE","5-year limited",["Cable, PTFE coating and track defects under normal use for 5 years","One complimentary re-tensioning within the first 18 months","Anchor/fixing workmanship for the warranty period"],ce+["Coating wear from abrasion, cleaning chemicals or pets","Corrosion where cables are cut, drilled or modified after install","Sagging caused by hanging objects or loads on the cables"],cc)+
           warr_card("Invisible Grille — Nano","10-year limited",["Cable, nano-coating and track defects under normal use for 10 years","Annual courtesy tension check on request for the first 3 years","Anchor/fixing workmanship for the warranty period"],ce+["Coating wear from abrasion, cleaning chemicals or pets","Corrosion where cables are cut, drilled or modified after install","Sagging caused by hanging objects or loads on the cables"],cc+["Supplier data sheet defines the coating performance; claims are assessed against it"]))
    body=f'''
<section class="page-hero"><div class="container"><span class="eyebrow">After-sales</span><h1>Warranty &amp; support</h1>
  <p>Every product carries a clear, written warranty with a defined scope and claim process. Our headline <strong>Zip Blind System warranty is 5 years</strong>, with the first two service visits free. Retractable-roof motors and grille coatings follow their own product terms below.</p></div></section>
<section class="section"><div class="container"><div class="warr-grid">{cards}</div>
  <div class="prose reveal mt-2"><h2>General warranty terms</h2>
    <ol><li><strong>Zip blind service schedule.</strong> Within the 5-year warranty the <strong>1st and 2nd visits are free</strong>; the <strong>3rd–5th visits carry S$250 labour each</strong>. Parts and out-of-scope work are quoted separately.</li>
      <li><strong>Advance notice.</strong> Please provide at least <strong>4 weeks' notice</strong> to schedule any repair or service visit.</li>
      <li><strong>Coverage &amp; remedy.</strong> Warranties cover genuine manufacturing or workmanship defects only. Our sole obligation, and your exclusive remedy, is repair or replacement of the defective part at our option, using the same or an equivalent component.</li>
      <li><strong>Registration &amp; payment.</strong> Cover starts on installation completion and is valid only when the invoice is paid in full. Warranty is non-transferable and does not restart after a repair.</li>
      <li><strong>Maintenance &amp; use.</strong> Products must be cleaned and used as advised; zip blinds must be raised, and retractable roofs retracted, in stormy or high-wind conditions as advised. Failure to do so, or use outside the intended purpose, voids cover.</li>
      <li><strong>Safety statements.</strong> Descriptions of products (including cable spacing options) describe physical characteristics and are not a guarantee of safety performance in any particular situation. Suitability is assessed at survey and confirmed in your quotation.</li>
      <li><strong>Exclusions.</strong> Wear, weathering, misuse, third-party work, structural/waterproofing issues, weather events beyond stated limits, and consequential loss are excluded.</li>
      <li><strong>Limitation of liability.</strong> {'; '.join(liability)}.</li>
      <li><strong>Whole agreement.</strong> The warranty scope, inclusions and exclusions stated here and in your written quotation and invoice form the entire warranty; earlier discussions or marketing statements do not add to it.</li></ol>
    <p>Full warranty terms are provided with your written quotation and invoice.</p></div>
</div></section>
{quote_section()}'''
    write("warranty.html","Warranty & Support | 5-Year Zip Blind Warranty | Balcony Master Singapore",
        "Balcony Master warranties — 5-year zip blind (1st & 2nd service free, 3rd–5th S$250, 4 weeks' notice), retractable roof (frame + motor per maker), decking, and grilles (Nylon 3-yr, PTFE 5-yr, Nano 10-yr). Clear scope, exclusions and liability limit.",
        body,trail=[("Home","./"),("Warranty",None)],active="warranty.html")

def page_about():
    body=f'''
<section class="page-hero"><div class="container"><span class="eyebrow">About us</span><h1>Balcony Master — one solution for all</h1>
  <p>We coordinate balcony decking, zip blinds, invisible grilles and retractable roofs so the finish, drainage, safety and shade all work together. Call us at <a href="tel:{PHONE}">{PHONE_D}</a>.</p></div></section>
<section class="section"><div class="container"><div class="prose reveal">
  <h2>How we work</h2><p>We start with a free site survey, recommend the right system for your property and exposure, and prepare a single itemised quotation with inclusions, exclusions and GST stated up front. Installation follows a sensible sequence so nothing has to be undone.</p>
  <h2>What we stand for</h2><ul><li>One accountable team across every service</li><li>Transparent planning-price ranges, not one misleading "from" figure</li><li>Written warranties with a defined scope and claim process</li><li>Genuine project evidence and real reviews only</li></ul></div></div></section>
{quote_section()}'''
    write("about.html","About | Balcony Master — Decking, Zip Blinds, Grilles & Retractable Roof",
        "About Balcony Master (lionsin.com.sg) — Singapore's one-solution specialist for balcony decking, zip blinds, invisible grilles and retractable roofs. Call 8341 7888.",
        body,trail=[("Home","./"),("About",None)],active="")

def page_contact():
    body=f'''
<section class="page-hero"><div class="container"><span class="eyebrow">Get in touch</span><h1>Request a free, measured quote</h1>
  <p>Tell us the basics and upload your floor plan or balcony photos — or call/WhatsApp <a href="tel:{PHONE}">{PHONE_D}</a>. We'll arrange a free site survey and itemised quotation, no obligation.</p></div></section>
<section class="section"><div class="container two-col">
  <div class="prose reveal"><h2>Talk to us</h2><p>Fastest response is on WhatsApp with a couple of photos or your floor plan.</p>
    <ul><li>Phone: <a href="tel:{PHONE}">{PHONE_D}</a></li><li>WhatsApp: <a data-wa href="{WA}" {WA_REL}>message us</a></li><li>Email: <a href="mailto:{EMAIL}">{EMAIL}</a></li></ul>
    <p>Hours: Mon–Sat, 9am–6pm. Serving HDB, condo and landed properties islandwide.</p></div>
  <div class="form-card reveal">{quote_form("",with_name=True)}</div>
</div></section>'''
    write("contact.html","Contact | Free Site Survey & Quote | Balcony Master (8341 7888)",
        "Contact Balcony Master for a free site survey and itemised quote on balcony decking, zip blinds, invisible grilles and retractable roofs in Singapore. Call/WhatsApp 8341 7888.",
        body,trail=[("Home","./"),("Contact",None)],active="")

def simple(path,title,desc,h1,prose,label):
    write(path,title,desc,f'<section class="page-hero"><div class="container"><span class="eyebrow">Legal</span><h1>{h1}</h1></div></section><section class="section"><div class="container"><div class="prose reveal">{prose}</div></div></section>',trail=[("Home","./"),(label,None)])
def page_privacy():
    simple("privacy.html","Privacy Notice | Balcony Master","Privacy notice for Balcony Master (lionsin.com.sg) — what we collect, how enquiries and uploads are processed.","Privacy Notice",
        f'<h2>What we collect</h2><p>When you submit an enquiry we collect the details you provide (name, mobile number, property type) and any files you upload (floor plans or balcony photos) to prepare a quotation and arrange a site survey.</p>'
        f'<h2>How your enquiry is processed</h2><p>Our web form is delivered using a third-party form-to-email service (<strong>FormSubmit</strong>). When you submit the form, your details and any attachments are transmitted through that service to our business email in order to reach us. The service processes the submission only to deliver it; we do not use it to build marketing profiles. Depending on the provider, processing may occur on servers outside Singapore. You can avoid the online form entirely by contacting us directly by phone, WhatsApp or email.</p>'
        f'<h2>How we use it</h2><p>We use your details and uploads solely to respond to your enquiry, prepare a quotation and provide our services. We do not sell your data.</p>'
        f'<h2>Retention &amp; your choices</h2><p>We keep enquiry data and uploads only as long as needed for your project and our records, then delete them. To ask what we hold, or to request deletion, contact us at <a href="tel:{PHONE}">{PHONE_D}</a> or <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>'
        f'<h2>Sensitive files</h2><p>Floor plans and home photographs can be sensitive. Please share only what is needed for a quotation. If you prefer, you can describe your balcony and send photos later over WhatsApp.</p>','Privacy')
def page_terms():
    simple("terms.html","Terms | Balcony Master","Terms for Balcony Master (lionsin.com.sg) — quotations, pricing, warranties, trademarks and workmanship.","Terms",
        '<h2>Quotations &amp; pricing</h2><p>All prices shown on this website are indicative planning ranges, not a contractual quotation. Final pricing is confirmed in a written, itemised quotation following a measured site survey. GST and minimum-order charges may apply.</p>'
        '<h2>Warranties</h2><p>Warranty scope, inclusions, exclusions and the limitation of liability are stated on the Warranty page and in your quotation and invoice, which together form the entire warranty. The zip blind system warranty is 5 years (1st &amp; 2nd service free, 3rd–5th at S$250 labour each; at least 4 weeks\u2019 notice required to schedule a repair).</p>'
        '<h2>Product descriptions &amp; safety</h2><p>Product descriptions state physical characteristics and intended use. They are not a guarantee of performance or safety in any particular situation; suitability is assessed at survey and confirmed in writing.</p>'
        '<h2>Trademarks &amp; independence</h2><p>Ziptrak®, Skyline®, Teflon™ and other names are trademarks of their respective owners and are used only to describe product categories or coatings. Balcony Master is an independent supplier and installer and is not affiliated with, endorsed by, or an authorised dealer of any third-party brand unless expressly stated in writing.</p>'
        '<h2>Deposits &amp; approvals</h2><p>A booking deposit may be required. Where a condominium requires a renovation/management deposit, this is arranged and paid by the home owner directly to the MA/MCST. Retractable roofs and certain works may require MCST/HDB approval or PE endorsement, which are the home owner\u2019s responsibility unless agreed otherwise.</p>'
        '<h2>Workmanship</h2><p>Installation is scheduled subject to site access, approvals and weather.</p>','Terms')
def page_thankyou():
    write("thank-you.html","Thank you | Balcony Master","Thank you — your enquiry has been received.",
        f'<section class="section"><div class="container maxw-narrow"><div class="form-success static"><div class="check">{CHECK}</div><h1>Thank you — request received</h1><p class="lead center">We\'ll be in touch to arrange your free site survey. For a faster response, call or WhatsApp <a class="link-green" href="tel:{PHONE}">{PHONE_D}</a>.</p><div class="hero-actions center mt-1"><a data-wa href="{WA}" {WA_REL} class="btn btn-primary">Send photos on WhatsApp</a><a href="./" class="btn btn-ghost">Back to home</a></div></div></div></section>',trail=None)
def page_404():
    write("404.html","Page not found | Balcony Master","404 — page not found.",
        '<section class="section"><div class="container center maxw-narrow"><span class="eyebrow">404</span><h1 class="section-title">Page not found</h1><p class="lead">The page you were looking for has moved or no longer exists.</p><div class="hero-actions center mt-1"><a href="./" class="btn btn-primary">Home</a><a href="price-guide.html" class="btn btn-ghost">Price guide</a><a href="contact.html" class="btn btn-ghost">Contact</a></div></div></section>',trail=None)

def seo_files():
    pages=["","balcony-decking-singapore.html","zip-blinds-singapore.html","invisible-grille-singapore.html","retractable-roof-singapore.html","complete-balcony-solution.html","projects.html","price-guide.html","warranty.html","about.html","contact.html","privacy.html","terms.html"]
    today=datetime.date.today().isoformat()
    urls="".join(f"  <url><loc>{SITE}/{p}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>{'1.0' if p=='' else '0.8'}</priority></url>\n" for p in pages)
    open(os.path.join(OUT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+urls+'</urlset>\n')
    open(os.path.join(OUT,"robots.txt"),"w").write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n"%SITE)
    open(os.path.join(OUT,"site.webmanifest"),"w").write(json.dumps({"name":"Balcony Master","short_name":"BalconyMaster","start_url":"/","display":"standalone","background_color":"#ffffff","theme_color":"#1E4D3B","icons":[{"src":"assets/icons/icon-192.png","sizes":"192x192","type":"image/png","purpose":"any maskable"},{"src":"assets/icons/icon-512.png","sizes":"512x512","type":"image/png","purpose":"any maskable"}]},indent=2))
    open(os.path.join(OUT,"CNAME"),"w").write(DOMAIN+"\n"); open(os.path.join(OUT,".nojekyll"),"w").write("")
    print("wrote sitemap.xml, robots.txt, site.webmanifest, CNAME, .nojekyll")

if __name__=="__main__":
    home(); page_decking(); page_blinds(); page_grilles(); page_roof(); page_complete()
    page_projects(); page_price(); page_warranty(); page_about(); page_contact()
    page_privacy(); page_terms(); page_thankyou(); page_404(); seo_files()
    print("ALL DONE")
