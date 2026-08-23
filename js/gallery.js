/* =====================================================================
   gallery.js — renders managed project galleries from window.PROJECTS.
   Uses window.openLightbox (main.js). Loads only on projects.html.
   ===================================================================== */
(function () {
  "use strict";
  var DATA = window.PROJECTS || {};
  var PLAY = '<span><svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span>';
  function box(item, cat) {
    var el = document.createElement("div");
    el.className = "media-box";
    if (!item || item.type === "empty") {
      el.classList.add("empty");
      el.innerHTML = '<div class="drop"><span class="plus">+</span><b>Add photo or video</b><code>assets/\u2026/projects/' + cat + '/</code></div>';
      return el;
    }
    var cap = '<div class="mcap"><h4>' + (item.title || "") + '</h4>' + (item.meta ? '<p>' + item.meta + '</p>' : '') + '</div>';
    if (item.type === "video") {
      var poster = item.poster ? ' poster="' + item.poster + '"' : '';
      el.innerHTML = '<span class="mtag">Video</span><video preload="none"' + poster + ' playsinline src="' + item.src + '"></video>' +
        '<button class="play" aria-label="Play video">' + PLAY + '</button>' + cap;
      el.querySelector(".play").addEventListener("click", function () { window.openLightbox("video", item.src, item.poster); });
    } else {
      el.innerHTML = '<img loading="lazy" src="' + item.src + '" alt="' + (item.title || "Project photo") + '">' + cap;
      el.style.cursor = "zoom-in";
      el.addEventListener("click", function () { window.openLightbox("image", item.src); });
    }
    return el;
  }
  Object.keys(DATA).forEach(function (cat) {
    var host = document.querySelector('[data-gallery="' + cat + '"]');
    if (!host) return;
    DATA[cat].forEach(function (item) { host.appendChild(box(item, cat)); });
  });
})();
