(function () {
  "use strict";

  var storageKey = "csymhph-color-theme";
  var root = document.documentElement;
  var media = window.matchMedia("(prefers-color-scheme: dark)");

  function savedTheme() {
    try {
      var value = window.localStorage.getItem(storageKey);
      return value === "light" || value === "dark" ? value : null;
    } catch (_error) {
      return null;
    }
  }

  function resolvedTheme() {
    return root.getAttribute("data-theme") || (media.matches ? "dark" : "light");
  }

  function updateControl(button) {
    var current = resolvedTheme();
    var next = current === "dark" ? "light" : "dark";
    var label = "Use " + next + " appearance";
    var icon = button.querySelector("[data-theme-icon]");

    button.setAttribute("aria-label", label);
    button.setAttribute("title", label);
    if (icon) icon.textContent = current === "dark" ? "☀︎" : "☾";
  }

  var initial = savedTheme();
  if (initial) root.setAttribute("data-theme", initial);

  function initialize() {
    var button = document.querySelector("[data-theme-toggle]");
    if (!button) return;

    updateControl(button);
    button.addEventListener("click", function () {
      var next = resolvedTheme() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try {
        window.localStorage.setItem(storageKey, next);
      } catch (_error) {
        // The selected appearance still applies for the current page.
      }
      updateControl(button);
    });

    var handleSystemChange = function () {
      if (!savedTheme()) updateControl(button);
    };
    if (media.addEventListener) {
      media.addEventListener("change", handleSystemChange);
    } else {
      media.addListener(handleSystemChange);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize);
  } else {
    initialize();
  }
})();
