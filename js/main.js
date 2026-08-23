/* =====================================================================
   main.js — shared behaviour (nav, forms, uploads, pricing tabs,
   hero video, product-video boxes, shared lightbox, GA loader).
   Depends on config.js (window.SITE_CONFIG, window.waLink).
   Vanilla JS, no dependencies. Defensive against missing nodes.
   ===================================================================== */
(function () {
  "use strict";
  var C = window.SITE_CONFIG || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---- 1. Business details from config ---- */
  $$("[data-phone-text]").forEach(function (el) { el.textContent = C.phoneDisplay || ""; });
  $$("[data-tel]").forEach(function (a) { a.setAttribute("href", "tel:" + (C.phone || "")); });
  $$("[data-wa]").forEach(function (a) {
    a.setAttribute("href", window.waLink("Hi " + (C.brand || "") + ", I'd like to enquire about my balcony (decking / zip blind / grille)."));
    a.setAttribute("rel", "nofollow"); a.setAttribute("target", "_blank");
  });
  $$("[data-email]").forEach(function (a) {
    a.setAttribute("href", "mailto:" + (C.email || "")); if (!a.textContent.trim()) a.textContent = C.email || "";
  });
  $$("[data-site='legalName']").forEach(function (el) { el.textContent = C.legalName || ""; });
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---- 2. Mobile menu ---- */
  var toggle = $("#menuToggle"), menu = $("#mobileMenu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    $$("a", menu).forEach(function (a) { a.addEventListener("click", function () { menu.classList.remove("open"); }); });
  }

  /* ---- 3. Pricing tabs ---- */
  var toggler = $("[data-price-toggle]");
  if (toggler) {
    var btns = $$("button", toggler);
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) { x.setAttribute("aria-selected", "false"); });
        b.setAttribute("aria-selected", "true");
        var target = b.getAttribute("data-target");
        $$("[data-price-panel]").forEach(function (p) {
          p.hidden = (p.getAttribute("data-price-panel") !== target);
          p.style.display = p.hidden ? "none" : "";
        });
      });
    });
  }

  /* ---- 4. Reveal on scroll ---- */
  var reveals = $$(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    reveals.forEach(function (r) { io.observe(r); });
  } else { reveals.forEach(function (r) { r.classList.add("in"); }); }

  /* ---- 5. Hero video: reveal when ready, drop if missing ---- */
  $$("[data-hero-video]").forEach(function (v) {
    v.addEventListener("canplay", function () { v.classList.add("ready"); });
    v.addEventListener("error", function () { if (v.parentNode) v.parentNode.removeChild(v); });
  });

  /* ---- 6. Any element with data-video-box opens its video in lightbox ---- */
  $$("[data-video-box]").forEach(function (box) {
    var trigger = box.querySelector(".play, .pc-play") || box;
    var open = function () { window.openLightbox("video", box.getAttribute("data-src"), box.getAttribute("data-poster")); };
    trigger.addEventListener("click", open);
    trigger.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(); } });
  });

  /* ---- 7. File upload label ---- */
  $$(".upload").forEach(function (zone) {
    var input = $("input[type=file]", zone), out = $(".u-files", zone);
    if (!input) return;
    input.addEventListener("change", function () {
      out.textContent = input.files.length
        ? "Attached: " + Array.prototype.map.call(input.files, function (f) { return f.name; }).join(", ")
        : "";
    });
  });

  /* ---- 8. Quote form: validate + demo/endpoint submit ---- */
  $$("[data-quote-form]").forEach(function (form) {
    var card = form.closest(".form-card") || form.parentElement;
    var summary = $(".form-error-summary", form);
    var params = new URLSearchParams(location.search);
    var svc = params.get("service"), product = params.get("product");
    var hidS = $("[name='service_preselect']", form), hidP = $("[name='product']", form);
    if (hidS && svc) hidS.value = svc;
    if (hidP && product) hidP.value = product;
    if (svc) {
      var sel = $("select[name='service']", form);
      var map = { decking: "Decking", blinds: "Zip blinds", grilles: "Invisible grilles", all: "All three" };
      if (sel && map[svc]) sel.value = map[svc];
    }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (summary) summary.classList.remove("show");
      var ok = true;
      var hp = $("[name='company_website']", form); if (hp && hp.value) return; // bot
      $$("[required]", form).forEach(function (input) {
        var field = input.closest(".field") || input.closest(".checkbox");
        var valid = input.type === "checkbox" ? input.checked : !!input.value.trim();
        if (input.type === "tel" && valid) valid = /[0-9]{7,}/.test(input.value.replace(/\s/g, ""));
        if (field) field.classList.toggle("invalid", !valid);
        if (!valid) ok = false;
      });
      if (!ok) { if (summary) { summary.textContent = "Please complete the highlighted fields."; summary.classList.add("show"); } return; }
      var done = function () {
        var success = $(".form-success", card);
        if (success) {
          form.style.display = "none"; success.classList.add("show");
          var wa = $("[data-wa]", success);
          if (wa) wa.setAttribute("href", window.waLink("Hi " + (C.brand || "") + ", I just submitted a quote request. Here are my balcony photos / floor plan:"));
        }
      };
      if (C.formEndpoint) {
        fetch(C.formEndpoint, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
          .then(done).catch(done);
      } else { done(); }
    });
  });

  /* ---- 9. Shared lightbox ---- */
  var lb = document.createElement("div");
  lb.className = "lightbox"; lb.setAttribute("role", "dialog"); lb.setAttribute("aria-modal", "true");
  lb.innerHTML = '<button class="lb-close" aria-label="Close">&times;</button><div class="lb-inner"></div>';
  document.body.appendChild(lb);
  var inner = $(".lb-inner", lb);
  function close() { lb.classList.remove("open"); inner.innerHTML = ""; }
  lb.addEventListener("click", function (e) { if (e.target === lb || e.target.classList.contains("lb-close")) close(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
  window.openLightbox = function (kind, src, poster) {
    if (!src) return;
    inner.innerHTML = kind === "video"
      ? '<video controls autoplay playsinline ' + (poster ? 'poster="' + poster + '"' : '') + ' src="' + src + '"></video>'
      : '<img src="' + src + '" alt="Media">';
    lb.classList.add("open");
  };

  /* ---- 10. GA4 only if configured ---- */
  if (C.gaId) {
    var s = document.createElement("script"); s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + C.gaId;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag("js", new Date()); gtag("config", C.gaId);
  }
})();
