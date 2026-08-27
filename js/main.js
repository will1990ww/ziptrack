/* main.js — progressive enhancement: nav, accessible tabs, reveal, hero-video
   guards, product-video lightbox, form validation (aria-invalid + error summary),
   GA4 + events, PRICE ESTIMATOR, BEFORE/AFTER SLIDER, TESTIMONIALS renderer. */
(function () {
  "use strict";
  var C = window.SITE_CONFIG || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var saveData = navigator.connection && navigator.connection.saveData;

  /* GA4 */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;
  window.track = function (n, p) { try { window.gtag("event", n, p || {}); } catch (e) {} };
  if (C.gaId) {
    var ga = document.createElement("script"); ga.async = true;
    ga.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(C.gaId);
    document.head.appendChild(ga); gtag("js", new Date()); gtag("config", C.gaId, { anonymize_ip: true });
  }

  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
  if (C.whatsapp) {
    $$("[data-wa]").forEach(function (a) {
      a.setAttribute("href", "https://wa.me/" + C.whatsapp + "?text=" +
        encodeURIComponent("Hi " + (C.brand || "Balcony Master") + ", I'd like to enquire about my balcony (decking / zip blind / grille / retractable roof)."));
    });
  }
  $$('a[href^="tel:"]').forEach(function (a) { a.addEventListener("click", function () { window.track("contact_call", {}); }); });
  $$('[data-wa]').forEach(function (a) { a.addEventListener("click", function () { window.track("contact_whatsapp", {}); }); });
  $$('a[href^="mailto:"]').forEach(function (a) { a.addEventListener("click", function () { window.track("contact_email", {}); }); });
  $$('a[href="contact.html"], a[href^="contact.html?"]').forEach(function (a) { a.addEventListener("click", function () { window.track("quote_cta_click", { location: location.pathname }); }); });

  /* mobile menu */
  var toggle = $("#menuToggle"), menu = $("#mobileMenu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () { var o = menu.classList.toggle("open"); toggle.setAttribute("aria-expanded", o ? "true" : "false"); });
    $$("a", menu).forEach(function (a) { a.addEventListener("click", function () { menu.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); }); });
  }

  /* accessible tabs */
  var tablist = $("[data-price-toggle]");
  if (tablist) {
    var tabs = $$('[role="tab"]', tablist), panels = $$("[data-price-panel]");
    function selectTab(tab, focus) {
      tabs.forEach(function (t) { var s = t === tab; t.setAttribute("aria-selected", s ? "true" : "false"); t.tabIndex = s ? 0 : -1; });
      var target = tab.getAttribute("data-target");
      panels.forEach(function (p) { var on = p.getAttribute("data-price-panel") === target; p.classList.toggle("is-hidden", !on); p.hidden = !on; });
      if (focus) tab.focus(); window.track("pricing_tab", { service: target });
    }
    tabs.forEach(function (tab, i) {
      tab.addEventListener("click", function () { selectTab(tab, false); });
      tab.addEventListener("keydown", function (e) {
        var k = e.key, idx = null;
        if (k === "ArrowRight" || k === "ArrowDown") idx = (i + 1) % tabs.length;
        else if (k === "ArrowLeft" || k === "ArrowUp") idx = (i - 1 + tabs.length) % tabs.length;
        else if (k === "Home") idx = 0; else if (k === "End") idx = tabs.length - 1;
        if (idx !== null) { e.preventDefault(); selectTab(tabs[idx], true); }
      });
    });
  }

  /* reveal */
  var reveals = $$(".reveal");
  if (!reduce && "IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }); }, { threshold: 0.12 });
    reveals.forEach(function (r) { io.observe(r); });
  } else { reveals.forEach(function (r) { r.classList.add("in"); }); }

  /* hero video */
  $$("[data-hero-video]").forEach(function (v) {
    if (reduce || saveData) { if (v.parentNode) v.parentNode.removeChild(v); return; }
    var started = false;
    function begin() {
      if (started) return; started = true;
      v.addEventListener("canplay", function () { v.classList.add("ready"); });
      v.addEventListener("error", function () { if (v.parentNode) v.parentNode.removeChild(v); });
      var p = v.play && v.play(); if (p && p.catch) p.catch(function () {});
      if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) v.play && v.play().catch(function(){}); else v.pause && v.pause(); }); }, { threshold: 0.1 }).observe(v);
      document.addEventListener("visibilitychange", function () { if (document.hidden) v.pause(); else v.play && v.play().catch(function(){}); });
    }
    if ("requestIdleCallback" in window) requestIdleCallback(begin, { timeout: 2500 }); else window.addEventListener("load", function () { setTimeout(begin, 800); });
  });

  /* product video boxes */
  $$("[data-video-box]").forEach(function (box) {
    var trigger = box.querySelector(".play, .pc-play") || box;
    var open = function () { window.openLightbox("video", box.getAttribute("data-src"), box.getAttribute("data-poster")); window.track("video_play", {}); };
    trigger.addEventListener("click", open);
    trigger.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(); } });
  });

  /* upload label */
  $$(".upload").forEach(function (zone) {
    var input = $("input[type=file]", zone), out = $(".u-files", zone);
    if (!input || !out) return;
    input.addEventListener("change", function () { out.textContent = input.files.length ? "Attached: " + Array.prototype.map.call(input.files, function (f) { return f.name; }).join(", ") : ""; });
  });

  /* ---------- PRICE ESTIMATOR ---------- */
  $$("[data-estimator]").forEach(function (root) {
    var unit = root.getAttribute("data-unit") || "ft2";      // ft2 or project
    var lo = parseFloat(root.getAttribute("data-lo"));
    var hi = parseFloat(root.getAttribute("data-hi"));
    var minFt = parseFloat(root.getAttribute("data-min") || "0");
    var svc = root.getAttribute("data-service") || "";
    var out = $(".est-out", root), area = $("#est-area", root), unitSel = $("#est-unit", root);
    function fmt(n) { return "S$" + Math.round(n).toLocaleString("en-SG"); }
    function calc() {
      if (unit === "project") { out.innerHTML = '<span class="est-range">' + fmt(lo) + ' – ' + fmt(hi) + '</span><span class="est-sub">per project (indicative)</span>'; return; }
      var a = parseFloat(area.value); if (!a || a <= 0) { out.innerHTML = '<span class="est-sub">Enter your balcony size to see an estimate.</span>'; return; }
      var ft = unitSel && unitSel.value === "m2" ? a * 10.7639 : a;
      var billFt = Math.max(ft, minFt);
      out.innerHTML = '<span class="est-range">' + fmt(billFt * lo) + ' – ' + fmt(billFt * hi) + '</span>' +
        '<span class="est-sub">≈ ' + Math.round(ft) + ' ft²' + (billFt > ft ? ' (min ' + minFt + ' ft² applies)' : '') + ' · indicative, before survey</span>';
    }
    if (area) area.addEventListener("input", calc);
    if (unitSel) unitSel.addEventListener("change", calc);
    var cta = $(".est-cta", root);
    if (cta) cta.addEventListener("click", function () { window.track("estimator_use", { service: svc }); });
    calc();
  });

  /* ---------- BEFORE / AFTER SLIDER ---------- */
  $$("[data-ba]").forEach(function (root) {
    var range = $(".ba-range", root), after = $(".ba-after", root), handle = $(".ba-handle", root);
    function set(v) { after.style.clipPath = "inset(0 0 0 " + v + "%)"; if (handle) handle.style.left = v + "%"; }
    if (range) { range.addEventListener("input", function () { set(range.value); }); set(range.value); }
  });

  /* ---------- TESTIMONIALS ---------- */
  var revHost = $("[data-reviews]");
  if (revHost && window.REVIEWS && window.REVIEWS.length) {
    var star = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2l3 6.9 7.5.6-5.7 4.9 1.8 7.3L12 17.8 5.1 21.7l1.8-7.3L1.2 9.5 8.7 8.9z"/></svg>';
    window.REVIEWS.forEach(function (r) {
      var d = document.createElement("figure"); d.className = "review reveal in";
      var stars = ""; for (var i = 0; i < (r.stars || 5); i++) stars += star;
      d.innerHTML = '<div class="r-stars" aria-label="' + (r.stars || 5) + ' out of 5">' + stars + '</div>' +
        '<blockquote>' + r.text + '</blockquote>' +
        '<figcaption><b>' + (r.name || "") + '</b><span>' + (r.area || "") + '</span></figcaption>';
      revHost.appendChild(d);
    });
  }

  /* ---------- FORM validation + error summary ---------- */
  $$("[data-quote-form]").forEach(function (form) {
    var card = form.closest(".form-card") || form.parentElement;
    var summary = $(".form-error-summary", form);
    var params = new URLSearchParams(location.search);
    var svc = params.get("service");
    var hidS = $("[name='service_preselect']", form); if (hidS && svc) hidS.value = svc;
    if (svc) { var sel = $("select[name='service']", form); var map = { decking: "Decking", blinds: "Zip blinds", grilles: "Invisible grilles", roof: "Retractable roof", all: "Multiple / all" }; if (sel && map[svc]) sel.value = map[svc]; }
    var actionReal = form.getAttribute("action") && form.getAttribute("action") !== "#";
    $$("[required]", form).forEach(function (input) {
      var ev = input.tagName === "SELECT" || input.type === "checkbox" ? "change" : "input";
      input.addEventListener(ev, function () {
        var ok = input.type === "checkbox" ? input.checked : !!input.value.trim();
        if (input.type === "tel" && ok) ok = /[0-9]{7,}/.test(input.value.replace(/\s/g, ""));
        input.setAttribute("aria-invalid", ok ? "false" : "true");
        var field = input.closest(".field") || input.closest(".checkbox"); if (field) field.classList.toggle("invalid", !ok);
      });
    });
    function labelFor(i) { var l = i.id ? form.querySelector("label[for='" + i.id + "']") : null; var t = l ? l.textContent.replace(/\*/g, "").trim() : (i.name || "this field"); return t.split("(")[0].trim(); }
    form.addEventListener("submit", function (e) {
      var invalids = [];
      $$("[required]", form).forEach(function (input) {
        var ok = input.type === "checkbox" ? input.checked : !!input.value.trim();
        if (input.type === "tel" && ok) ok = /[0-9]{7,}/.test(input.value.replace(/\s/g, ""));
        input.setAttribute("aria-invalid", ok ? "false" : "true");
        var field = input.closest(".field") || input.closest(".checkbox"); if (field) field.classList.toggle("invalid", !ok);
        if (!ok) invalids.push(input);
      });
      var hp = $("[name='company_website']", form); if (hp && hp.value) { e.preventDefault(); return; }
      if (invalids.length) {
        e.preventDefault();
        if (summary) {
          summary.innerHTML = "<p>Please correct the following:</p><ul>" + invalids.map(function (i) { return '<li><a href="#' + i.id + '">' + labelFor(i) + '</a></li>'; }).join("") + "</ul>";
          summary.classList.add("show"); summary.setAttribute("tabindex", "-1"); summary.focus();
          $$("a", summary).forEach(function (a) { a.addEventListener("click", function (ev) { ev.preventDefault(); var t = document.getElementById(a.getAttribute("href").slice(1)); if (t) t.focus(); }); });
        } else { invalids[0].focus(); }
        return;
      }
      var svcSel = $("select[name='service']", form), propSel = $("select[name='property']", form);
      window.track("generate_lead", { service: svcSel ? svcSel.value : "", property_type: propSel ? propSel.value : "", page: location.pathname });

      var endpoint = C.formEndpoint;
      if (endpoint) {
        /* ---- Wired to your Cloudflare Worker: submit via fetch with a graceful fallback ---- */
        e.preventDefault();
        var btn = $("button[type=submit]", form);
        if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = "Sending…"; }
        function showSuccess() {
          var ok = $(".form-success", card);
          if (ok) { form.hidden = true; ok.classList.add("show"); var h = ok.querySelector("h1,h2,h3"); if (h) { h.setAttribute("tabindex", "-1"); h.focus(); } }
          else { location.href = C.thankYouUrl || "thank-you.html"; }
        }
        function whatsappFallback() {
          if (!(C.fallbackToWhatsApp && C.whatsapp)) { restore(); if (summary) { summary.innerHTML = "<p>Sorry, sending failed. Please call or WhatsApp us and we'll help right away.</p>"; summary.classList.add("show"); } return; }
          var msg = "Hi " + (C.brand || "Balcony Master") + ", I'd like a balcony quote.\n" +
            "Property: " + (propSel ? propSel.value : "-") + "\nService: " + (svcSel ? svcSel.value : "-") +
            "\nMobile: " + (($("[name='mobile']", form) || {}).value || "-") + "\nName: " + (($("[name='name']", form) || {}).value || "-") +
            "\n(My photos didn't upload — I'll attach them here.)";
          window.track("lead_whatsapp_fallback", {});
          window.open("https://wa.me/" + C.whatsapp + "?text=" + encodeURIComponent(msg), "_blank", "noopener");
          restore();
        }
        function restore() { if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label || "Request my quote"; } }
        var ctrl = ("AbortController" in window) ? new AbortController() : null;
        var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 15000);
        fetch(endpoint, { method: "POST", body: new FormData(form), headers: { "X-BM-Ajax": "1" }, signal: ctrl ? ctrl.signal : undefined })
          .then(function (r) { clearTimeout(timer); if (r.ok || r.status === 303 || r.type === "opaqueredirect") { showSuccess(); } else { whatsappFallback(); } })
          .catch(function () { clearTimeout(timer); whatsappFallback(); });
      } else if (!actionReal) {
        /* Demo mode (no endpoint, no real action): show inline success */
        e.preventDefault();
        var ok = $(".form-success", card);
        if (ok) { form.hidden = true; ok.classList.add("show"); var h = ok.querySelector("h1,h2,h3"); if (h) { h.setAttribute("tabindex", "-1"); h.focus(); } }
      }
      /* else: a real <form action> (e.g. FormSubmit) is present -> allow native POST */
    });
  });

  /* lightbox */
  var lb = document.createElement("div");
  lb.className = "lightbox"; lb.setAttribute("role", "dialog"); lb.setAttribute("aria-modal", "true"); lb.setAttribute("aria-label", "Media viewer");
  lb.innerHTML = '<button class="lb-close" type="button" aria-label="Close">&times;</button><div class="lb-inner"></div>';
  document.body.appendChild(lb);
  var inner = $(".lb-inner", lb), lastFocus = null;
  function close() { lb.classList.remove("open"); inner.innerHTML = ""; if (lastFocus) lastFocus.focus(); }
  lb.addEventListener("click", function (e) { if (e.target === lb || e.target.classList.contains("lb-close")) close(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && lb.classList.contains("open")) close(); });
  window.openLightbox = function (kind, src, poster) {
    if (!src) return; lastFocus = document.activeElement;
    inner.innerHTML = kind === "video" ? '<video controls autoplay playsinline ' + (poster ? 'poster="' + poster + '"' : '') + ' src="' + src + '"></video>' : '<img src="' + src + '" alt="Project media">';
    lb.classList.add("open"); var c = $(".lb-close", lb); if (c) c.focus();
  };
})();
