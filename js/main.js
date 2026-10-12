/*
 * Minimal enhancement only. In-page links are plain #anchors handled natively by the
 * browser (smooth scrolling and header offset are done in CSS), so navigation works
 * without this file. This script adds: the mobile menu and the active-section marker.
 */
(function () {
    "use strict";

    var toggle = document.querySelector(".nav-toggle");
    var menu = document.getElementById("nav-menu");
    var links = Array.prototype.slice.call(document.querySelectorAll(".nav-links a"));

    /* ---- mobile menu ---- */
    function setMenu(open) {
        if (!toggle || !menu) return;
        toggle.setAttribute("aria-expanded", String(open));
        menu.classList.toggle("is-open", open);
    }

    if (toggle && menu) {
        toggle.addEventListener("click", function () {
            setMenu(toggle.getAttribute("aria-expanded") !== "true");
        });

        // Close after choosing a destination (the browser still performs the anchor jump).
        menu.addEventListener("click", function (event) {
            if (event.target.closest("a")) setMenu(false);
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
                setMenu(false);
                toggle.focus();
            }
        });

        // Leaving the mobile breakpoint resets the menu state.
        window.matchMedia("(min-width: 861px)").addEventListener("change", function (e) {
            if (e.matches) setMenu(false);
        });
    }

    /* ---- active section marker ---- */
    if (!("IntersectionObserver" in window) || !links.length) return;

    var byId = {};
    links.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });

    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            links.forEach(function (a) { a.removeAttribute("aria-current"); });
            var active = byId[entry.target.id];
            if (active) active.setAttribute("aria-current", "location");
        });
    }, { rootMargin: "-30% 0px -60% 0px" });

    Object.keys(byId).forEach(function (id) {
        var section = document.getElementById(id);
        if (section) observer.observe(section);
    });

    // At the very top (hero) nothing is highlighted.
    window.addEventListener("scroll", function () {
        if (window.scrollY < 120) links.forEach(function (a) { a.removeAttribute("aria-current"); });
    }, { passive: true });
})();
