/* =====================================================================
   main.js — progressive enhancement. Site is fully usable without JS.
   Implements review priorities: accessible tabs (arrows/Home/End),
   robust form validation (aria-invalid toggling + error summary with
   links to invalid fields), hero-video performance guards (reduced
   motion, Save-Data, viewport & page-visibility pausing, deferred load),
   product-video lightbox, GA4 + conversion events.
   ===================================================================== */
(function () {
  "use strict";
  var C = window.SITE_CONFIG || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var saveData = navigator.connection && navigator.connection.saveData;

  /* ---- GA4 (loads only if a Measurement ID is set) ---- */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;
  window.track = function (name, params) { try { window.gtag("event", name, params || {}); } catch (e) {} };
  if (C.gaId) {
    var ga = document.createElement("script"); ga.async = true;
    ga.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(C.gaId);
    document.head.appendChild(ga);
    gtag("js", new Date()); gtag("config", C.gaId, { anonymize_ip: true });
  }

  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  if (C.whatsapp) {
    $$("[data-wa]").forEach(function (a) {
      a.setAttribute("href", "https://wa.me/" + C.whatsapp + "?text=" +
        encodeURIComponent("Hi " + (C.brand || "Balcony Master") + ", I'd like to enquire about my balcony (decking / zip blind / grille / retractable roof)."));
    });
  }

  /* GA conversion events */
  $$('a[href^="tel:"]').forEach(function (a) { a.addEventListener("click", function () { window.track("contact_call", { method: "phone" }); }); });
  $$('[data-wa]').forEach(function (a) { a.addEventListener("click", function () { window.track("contact_whatsapp", { method: "whatsapp" }); }); });
  $$('a[href^="mailto:"]').forEach(function (a) { a.addEventListener("click", function () { window.track("contact_email", { method: "email" }); }); });
  $$('a[href="./"], a[href="contact.html"], a[href^="contact.html?"]').forEach(function (a) {
    if (a.getAttribute("href") !== "./") a.addEventListener("click", function () { window.track("quote_cta_click", { location: location.pathname }); });
  });

  /* Mobile menu */
  var toggle = $("#menuToggle"), menu = $("#mobileMenu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    $$("a", menu).forEach(function (a) { a.addEventListener("click", function () { menu.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); }); });
  }

  /* Accessible tabs (WAI-ARIA) */
  var tablist = $("[data-price-toggle]");
  if (tablist) {
    var tabs = $$('[role="tab"]', tablist), panels = $$("[data-price-panel]");
    function selectTab(tab, focus) {
      tabs.forEach(function (t) { var sel = t === tab; t.setAttribute("aria-selected", sel ? "true" : "false"); t.tabIndex = sel ? 0 : -1; });
      var target = tab.getAttribute("data-target");
      panels.forEach(function (p) { var on = p.getAttribute("data-price-panel") === target; p.classList.toggle("is-hidden", !on); p.hidden = !on; });
      if (focus) tab.focus();
      window.track("pricing_tab", { service: target });
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

  /* Reveal on scroll */
  var reveals = $$(".reveal");
  if (!reduce && "IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    reveals.forEach(function (r) { io.observe(r); });
  } else { reveals.forEach(function (r) { r.classList.add("in"); }); }

  /* Hero video — performance & accessibility guards */
  $$("[data-hero-video]").forEach(function (v) {
    if (reduce || saveData) { if (v.parentNode) v.parentNode.removeChild(v); return; }
    var started = false;
    function begin() {
      if (started) return; started = true;
      v.addEventListener("canplay", function () { v.classList.add("ready"); });
      v.addEventListener("error", function () { if (v.parentNode) v.parentNode.removeChild(v); });
      var p = v.play && v.play(); if (p && p.catch) p.catch(function () {});
      // pause when off-screen or tab hidden
      if ("IntersectionObserver" in window) {
        new IntersectionObserver(function (es) {
          es.forEach(function (e) { if (e.isIntersecting) { v.play && v.play().catch(function(){}); } else { v.pause && v.pause(); } });
        }, { threshold: 0.1 }).observe(v);
      }
      document.addEventListener("visibilitychange", function () { if (document.hidden) v.pause(); else v.play && v.play().catch(function(){}); });
    }
    // defer until the page has settled so it can't delay LCP
    if ("requestIdleCallback" in window) requestIdleCallback(begin, { timeout: 2500 });
    else window.addEventListener("load", function () { setTimeout(begin, 800); });
  });

  /* Product-video boxes -> lightbox */
  $$("[data-video-box]").forEach(function (box) {
    var trigger = box.querySelector(".play, .pc-play") || box;
    var open = function () { window.openLightbox("video", box.getAttribute("data-src"), box.getAttribute("data-poster")); window.track("video_play", { src: box.getAttribute("data-src") }); };
    trigger.addEventListener("click", open);
    trigger.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(); } });
  });

  /* Upload label */
  $$(".upload").forEach(function (zone) {
    var input = $("input[type=file]", zone), out = $(".u-files", zone);
    if (!input || !out) return;
    input.addEventListener("change", function () {
      out.textContent = input.files.length ? "Attached: " + Array.prototype.map.call(input.files, function (f) { return f.name; }).join(", ") : "";
    });
  });

  /* Forms: validation + focus management + error summary with links */
  $$("[data-quote-form]").forEach(function (form) {
    var card = form.closest(".form-card") || form.parentElement;
    var summary = $(".form-error-summary", form);
    var params = new URLSearchParams(location.search);
    var svc = params.get("service");
    var hidS = $("[name='service_preselect']", form); if (hidS && svc) hidS.value = svc;
    if (svc) {
      var sel = $("select[name='service']", form);
      var map = { decking: "Decking", blinds: "Zip blinds", grilles: "Invisible grilles", roof: "Retractable roof", all: "Multiple / all" };
      if (sel && map[svc]) sel.value = map[svc];
    }
    var actionReal = form.getAttribute("action") && form.getAttribute("action") !== "#";

    // clear invalid state as the user fixes fields
    $$("[required]", form).forEach(function (input) {
      var ev = input.tagName === "SELECT" || input.type === "checkbox" ? "change" : "input";
      input.addEventListener(ev, function () {
        var ok = input.type === "checkbox" ? input.checked : !!input.value.trim();
        if (input.type === "tel" && ok) ok = /[0-9]{7,}/.test(input.value.replace(/\s/g, ""));
        input.setAttribute("aria-invalid", ok ? "false" : "true");
        var field = input.closest(".field") || input.closest(".checkbox"); if (field) field.classList.toggle("invalid", !ok);
      });
    });

    function labelFor(input) {
      var id = input.id;
      var lab = id ? form.querySelector("label[for='" + id + "']") : null;
      var t = lab ? lab.textContent.replace(/\*/g, "").trim() : (input.name || "this field");
      return t.split("(")[0].trim();
    }

    form.addEventListener("submit", function (e) {
      var invalids = [];
      $$("[required]", form).forEach(function (input) {
        var ok = input.type === "checkbox" ? input.checked : !!input.value.trim();
        if (input.type === "tel" && ok) ok = /[0-9]{7,}/.test(input.value.replace(/\s/g, ""));
        input.setAttribute("aria-invalid", ok ? "false" : "true");
        var field = input.closest(".field") || input.closest(".checkbox"); if (field) field.classList.toggle("invalid", !ok);
        if (!ok) invalids.push(input);
      });
      var hp = $("[name='company_website']", form);
      if (hp && hp.value) { e.preventDefault(); return; } // bot

      if (invalids.length) {
        e.preventDefault();
        if (summary) {
          summary.innerHTML = "<p>Please correct the following:</p><ul>" +
            invalids.map(function (i) { return '<li><a href="#' + i.id + '">' + labelFor(i) + '</a></li>'; }).join("") + "</ul>";
          summary.classList.add("show");
          summary.setAttribute("tabindex", "-1"); summary.focus();
          $$("a", summary).forEach(function (a) {
            a.addEventListener("click", function (ev) { ev.preventDefault(); var t = document.getElementById(a.getAttribute("href").slice(1)); if (t) t.focus(); });
          });
        } else { invalids[0].focus(); }
        return;
      }
      var svcSel = $("select[name='service']", form), propSel = $("select[name='property']", form);
      window.track("generate_lead", { service: svcSel ? svcSel.value : "", property_type: propSel ? propSel.value : "", page: location.pathname });
      if (!actionReal) {
        e.preventDefault();
        var success = $(".form-success", card);
        if (success) { form.hidden = true; success.classList.add("show"); var h = success.querySelector("h1,h2,h3"); if (h) { h.setAttribute("tabindex", "-1"); h.focus(); } }
      }
    });
  });

  /* Shared lightbox */
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
    inner.innerHTML = kind === "video"
      ? '<video controls autoplay playsinline ' + (poster ? 'poster="' + poster + '"' : '') + ' src="' + src + '"></video>'
      : '<img src="' + src + '" alt="Project media">';
    lb.classList.add("open"); var c = $(".lb-close", lb); if (c) c.focus();
  };
})();
