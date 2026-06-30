(function () {
  "use strict";

  /* ---------- mobile sidebar toggle ---------- */

  var menuToggle = document.getElementById("pookiedocs-menu-toggle");
  var sidebar = document.getElementById("pookiedocs-sidebar");

  if (menuToggle && sidebar) {
    menuToggle.addEventListener("click", function () {
      document.body.classList.toggle("pookiedocs-sidebar-open");
    });

    document.addEventListener("click", function (event) {
      if (!document.body.classList.contains("pookiedocs-sidebar-open")) return;
      if (!sidebar.contains(event.target) && event.target !== menuToggle && !menuToggle.contains(event.target)) {
        document.body.classList.remove("pookiedocs-sidebar-open");
      }
    });

    var navLinks = sidebar.querySelectorAll(".pookiedocs-nav-link");
    navLinks.forEach(function (link) {
      link.addEventListener("click", function () {
        document.body.classList.remove("pookiedocs-sidebar-open");
      });
    });
  }

  /* ---------- active nav link (client-side supplement to server-side marking) ---------- */

  var currentPath = window.location.pathname;
  var allNavLinks = document.querySelectorAll(".pookiedocs-nav-link");
  allNavLinks.forEach(function (link) {
    if (link.getAttribute("href") === currentPath) {
      link.classList.add("pookiedocs-nav-active");
    }
  });

  /* ---------- code copy buttons ---------- */

  var codeBlocks = document.querySelectorAll(".pookiedocs-content-inner pre");
  codeBlocks.forEach(function (pre) {
    var wrapper = document.createElement("div");
    wrapper.className = "pookiedocs-pre-wrapper";
    pre.parentNode.insertBefore(wrapper, pre);
    wrapper.appendChild(pre);

    var btn = document.createElement("button");
    btn.className = "pookiedocs-copy-btn";
    btn.setAttribute("aria-label", "Copy code");
    btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';

    var copyIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';
    var checkIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';

    btn.addEventListener("click", function () {
      var codeEl = pre.querySelector("code");
      var text = codeEl ? codeEl.textContent : pre.textContent;

      function markCopied() {
        btn.innerHTML = checkIcon;
        btn.classList.add("pookiedocs-copied");
        setTimeout(function () {
          btn.innerHTML = copyIcon;
          btn.classList.remove("pookiedocs-copied");
        }, 2000);
      }

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(markCopied).catch(function () {
          fallbackCopy(text, markCopied);
        });
      } else {
        fallbackCopy(text, markCopied);
      }
    });

    wrapper.appendChild(btn);
  });

  function fallbackCopy(text, callback) {
    var textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.style.cssText = "position:fixed;opacity:0;pointer-events:none;";
    document.body.appendChild(textarea);
    textarea.select();
    try { document.execCommand("copy"); callback(); } catch (e) {}
    document.body.removeChild(textarea);
  }

  /* ---------- search modal ---------- */

  var searchTrigger = document.getElementById("pookiedocs-search-trigger");
  var modalOverlay = document.getElementById("pookiedocs-modal-overlay");
  var modal = document.getElementById("pookiedocs-modal");
  var modalInput = document.getElementById("pookiedocs-modal-input");
  var modalResults = document.getElementById("pookiedocs-modal-results");
  var modalClose = document.getElementById("pookiedocs-modal-close");
  var searchIndex = null;
  var focusedIndex = -1;

  function openModal() {
    if (!modal) return;
    modal.removeAttribute("hidden");
    modalOverlay.removeAttribute("hidden");
    document.body.style.overflow = "hidden";
    focusedIndex = -1;
    modalInput.focus();
  }

  function closeModal() {
    if (!modal) return;
    modal.setAttribute("hidden", "");
    modalOverlay.setAttribute("hidden", "");
    document.body.style.overflow = "";
    modalResults.innerHTML = "";
    modalInput.value = "";
    focusedIndex = -1;
  }

  function ensureIndexLoaded(callback) {
    if (searchIndex !== null) {
      callback();
      return;
    }
    fetch("/search-index.json")
      .then(function (response) {
        if (!response.ok) throw new Error("Search index returned " + response.status);
        return response.json();
      })
      .then(function (data) {
        searchIndex = data;
        callback();
      })
      .catch(function () {
        searchIndex = [];
      });
  }

  if (searchTrigger) {
    searchTrigger.addEventListener("click", function () {
      document.body.classList.remove("pookiedocs-sidebar-open");
      ensureIndexLoaded(function () {});
      openModal();
    });
  }

  if (modalClose) {
    modalClose.addEventListener("click", closeModal);
  }

  if (modalOverlay) {
    modalOverlay.addEventListener("click", closeModal);
  }

  // Ctrl+K / Cmd+K to open, Escape to close
  document.addEventListener("keydown", function (event) {
    if ((event.ctrlKey || event.metaKey) && event.key === "k") {
      event.preventDefault();
      if (modal && !modal.hasAttribute("hidden")) {
        closeModal();
      } else {
        ensureIndexLoaded(function () {});
        openModal();
      }
      return;
    }

    if (event.key === "Escape" && modal && !modal.hasAttribute("hidden")) {
      closeModal();
      return;
    }

    // arrow key navigation through results
    if (modal && !modal.hasAttribute("hidden") && (event.key === "ArrowDown" || event.key === "ArrowUp")) {
      event.preventDefault();
      var items = modalResults.querySelectorAll(".pookiedocs-modal-result");
      if (!items.length) return;
      items[focusedIndex] && items[focusedIndex].classList.remove("pookiedocs-modal-result--focused");
      if (event.key === "ArrowDown") {
        focusedIndex = Math.min(focusedIndex + 1, items.length - 1);
      } else {
        focusedIndex = Math.max(focusedIndex - 1, 0);
      }
      items[focusedIndex].classList.add("pookiedocs-modal-result--focused");
      items[focusedIndex].scrollIntoView({ block: "nearest" });
    }

    // Enter navigates to focused result
    if (modal && !modal.hasAttribute("hidden") && event.key === "Enter" && focusedIndex >= 0) {
      var items = modalResults.querySelectorAll(".pookiedocs-modal-result");
      if (items[focusedIndex]) {
        items[focusedIndex].click();
      }
    }
  });

  if (modalInput) {
    modalInput.addEventListener("input", function () {
      var query = modalInput.value.trim().toLowerCase();
      focusedIndex = -1;

      if (!query) {
        modalResults.innerHTML = "";
        return;
      }

      ensureIndexLoaded(function () {
        var matches = (searchIndex || []).filter(function (page) {
          return (
            page.title.toLowerCase().indexOf(query) !== -1 ||
            page.excerpt.toLowerCase().indexOf(query) !== -1
          );
        });
        renderModalResults(matches, query);
      });
    });
  }

  function renderModalResults(matches, query) {
    modalResults.innerHTML = "";

    if (matches.length === 0) {
      var noResults = document.createElement("p");
      noResults.className = "pookiedocs-modal-no-results";
      noResults.textContent = "No results found for \"" + query + "\".";
      modalResults.appendChild(noResults);
      return;
    }

    matches.slice(0, 10).forEach(function (page) {
      var link = document.createElement("a");
      link.className = "pookiedocs-modal-result";
      link.href = page.url;

      var titleEl = document.createElement("span");
      titleEl.className = "pookiedocs-modal-result-title";
      titleEl.textContent = page.title;

      var excerptEl = document.createElement("span");
      excerptEl.className = "pookiedocs-modal-result-excerpt";
      excerptEl.textContent = page.excerpt;

      link.appendChild(titleEl);
      link.appendChild(excerptEl);

      link.addEventListener("click", function () {
        closeModal();
      });

      modalResults.appendChild(link);
    });
  }
})();
