/* =====================================================================
   config.js — business + form settings (progressive enhancement).
   Contact links are hard-coded in HTML, so the site works without JS.
   ---------------------------------------------------------------------
   FORM ENDPOINT SWITCH (this is the "wiring"):
     - Leave formEndpoint = ""   -> forms use the built-in FormSubmit action
                                    (works today, no setup).
     - Set  formEndpoint = "https://form.lionsin.com.sg"  (your Cloudflare
       Worker URL) -> forms POST there instead, with secure upload checks.
     If the Worker is unreachable, the site auto-falls back to WhatsApp so a
     lead is never lost (toggle with fallbackToWhatsApp).
   ===================================================================== */
window.SITE_CONFIG = {
  brand: "Balcony Master",
  whatsapp: "6583417888",
  gaId: "",                       // GA4 id e.g. "G-XXXXXXXXXX"
  formEndpoint: "",               // <- paste your Worker URL here to switch on
  fallbackToWhatsApp: true,       // if the endpoint fails, open WhatsApp with details
  thankYouUrl: "thank-you.html"   // where to send visitors after a JS submit
};
