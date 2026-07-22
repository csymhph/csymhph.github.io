(function () {
  "use strict";

  var storageKey = "csymhph-color-theme";

  function storedTheme() {
    try {
      var value = window.localStorage.getItem(storageKey);
      return value === "light" || value === "dark" ? value : null;
    } catch (_error) {
      return null;
    }
  }

  function systemTheme() {
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  function activeTheme() {
    return document.documentElement.dataset.theme || systemTheme();
  }

  function updateButton(button) {
    var dark = activeTheme() === "dark";
    button.setAttribute(
      "aria-label",
      dark ? "Switch to light appearance" : "Switch to dark appearance"
    );
    button.setAttribute("title", button.getAttribute("aria-label"));
    button.querySelector(".theme-icon").textContent = dark ? "☀" : "☾";
  }

  var saved = storedTheme();
  if (saved) {
    document.documentElement.dataset.theme = saved;
  }

  document.addEventListener("DOMContentLoaded", function () {
    var button = document.querySelector("[data-theme-toggle]");
    if (!button) return;

    updateButton(button);
    button.addEventListener("click", function () {
      var next = activeTheme() === "dark" ? "light" : "dark";
      document.documentElement.dataset.theme = next;
      try {
        window.localStorage.setItem(storageKey, next);
      } catch (_error) {
        // The visual preference still works for the current page.
      }
      updateButton(button);
    });
  });
})();
