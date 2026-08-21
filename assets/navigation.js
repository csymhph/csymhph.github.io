(function () {
  "use strict";

  var historyApi = window.history;
  var navigationEntry = window.performance && window.performance.getEntriesByType
    ? window.performance.getEntriesByType("navigation")[0]
    : null;
  var isReload = navigationEntry
    ? navigationEntry.type === "reload"
    : Boolean(window.performance && window.performance.navigation
      && window.performance.navigation.type === 1);

  if ("scrollRestoration" in historyApi) {
    historyApi.scrollRestoration = "manual";
  }

  function cleanUrl() {
    if (!window.location.hash || !historyApi.replaceState) return;
    historyApi.replaceState(
      null,
      "",
      window.location.pathname + window.location.search
    );
  }

  function scrollToTop() {
    window.scrollTo(0, 0);
  }

  if (isReload) {
    cleanUrl();
    window.addEventListener("load", scrollToTop);
  }

  function initialize() {
    var links = document.querySelectorAll("[data-section-link]");

    Array.prototype.forEach.call(links, function (link) {
      link.addEventListener("click", function (event) {
        var target = document.getElementById(link.getAttribute("data-section-link"));
        if (!target) return;

        event.preventDefault();
        cleanUrl();
        target.scrollIntoView();
      });
    });

    if (isReload) {
      scrollToTop();
      return;
    }

    if (window.location.hash) {
      var id;
      try {
        id = decodeURIComponent(window.location.hash.slice(1));
      } catch (_error) {
        return;
      }
      var target = document.getElementById(id);
      if (target) {
        target.scrollIntoView();
        cleanUrl();
      }
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize);
  } else {
    initialize();
  }
})();
