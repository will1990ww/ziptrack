/* config.js — SINGLE SOURCE OF TRUTH for business details.
   Edit these placeholders once verified; every page reads from here. */
window.SITE_CONFIG = {
  legalName: "Balcony Master",
  brand: "Balcony Master",
  tagline: "One Solution for All",
  phone: "+6583417888",
  phoneDisplay: "+65 8341 7888",
  whatsapp: "658341888",
  email: "bimprosg@outlook.com",
  address: "Singapore",
  uen: "TBC",
  hours: "Mon\u2013Sat, 9am\u20136pm",
  formEndpoint: "",   // empty = DEMO mode (no data sent)
  gaId: ""            // e.g. "G-XXXXXXXXXX"
};
window.waLink = function (msg) {
  var c = window.SITE_CONFIG, base = "https://wa.me/" + c.whatsapp;
  return msg ? base + "?text=" + encodeURIComponent(msg) : base;
};
