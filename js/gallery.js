/* gallery.js — renders project galleries from window.PROJECTS. */
(function () {
  "use strict";
  var DATA = window.PROJECTS || {};
  var PLAY = '<span><svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></span>';
  function box(item) {
    var el = document.createElement("div"); el.className = "media-box";
    if (!item || item.type === "empty") {
      el.classList.add("empty");
      el.innerHTML = '<div class="drop"><b>More coming soon</b><span>New installations added regularly</span></div>'; return el;
    }
    var cap = '<div class="mcap"><h4>' + (item.title || "") + '</h4>' + (item.meta ? '<p>' + item.meta + '</p>' : '') + '</div>';
    if (item.type === "video") {
      var poster = item.poster ? ' poster="' + item.poster + '"' : '';
      el.innerHTML = '<span class="mtag">Video</span><video preload="none"' + poster + ' playsinline src="' + item.src + '"></video>' +
        '<button class="play" type="button" aria-label="Play video: ' + (item.title || "") + '">' + PLAY + '</button>' + cap;
      el.querySelector(".play").addEventListener("click", function () { window.openLightbox("video", item.src, item.poster); });
    } else {
      el.innerHTML = '<img loading="lazy" src="' + item.src + '" alt="' + (item.alt || item.title || "Project photo") + '">' + cap;
      el.setAttribute("role", "button"); el.setAttribute("tabindex", "0"); el.setAttribute("aria-label", "View photo: " + (item.title || ""));
      var open = function () { window.openLightbox("image", item.src); };
      el.addEventListener("click", open);
      el.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(); } });
    }
    return el;
  }
  Object.keys(DATA).forEach(function (cat) {
    var host = document.querySelector('[data-gallery="' + cat + '"]');
    if (!host) return; DATA[cat].forEach(function (item) { host.appendChild(box(item)); });
  });
})();
