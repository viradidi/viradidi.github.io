/*
 * Portfolio enhancements (progressive: every page works without JavaScript).
 *  - Projects catalogue: search plus discipline and technology filters.
 *  - Diagram lightbox: opens the original image in a native <dialog>.
 */
(function () {
    "use strict";

    document.documentElement.classList.add("js");

    function initCatalogue() {
        var cards = Array.prototype.slice.call(document.querySelectorAll(".project-card"));
        var chips = Array.prototype.slice.call(document.querySelectorAll(".chip[data-group]"));
        var input = document.getElementById("project-search");
        var count = document.getElementById("catalog-count");
        var status = document.getElementById("filter-status");
        var none = document.getElementById("no-results");
        var state = { cat: "all", tech: "all", terms: [] };

        if (!cards.length) {
            return;
        }

        var grid = document.querySelector(".catalog-grid");
        var groupsEl = null;
        var labels = {};
        chips.forEach(function (c) {
            if (c.getAttribute("data-group") === "cat") { labels[c.getAttribute("data-filter")] = c.textContent; }
        });
        var order = Object.keys(labels).filter(function (k) { return k !== "all"; });

        // Default view: projects grouped under their primary discipline. Any filter or search switches to the flat grid.
        function regroup(grouped) {
            if (!grid) { return; }
            if (!grouped) {
                if (groupsEl) { groupsEl.hidden = true; }
                grid.hidden = false;
                cards.forEach(function (card) { grid.appendChild(card); });
                return;
            }
            if (!groupsEl) {
                groupsEl = document.createElement("div");
                groupsEl.className = "catalog-groups";
                grid.parentNode.insertBefore(groupsEl, grid);
            }
            groupsEl.innerHTML = "";
            order.forEach(function (key) {
                var members = cards.filter(function (card) { return card.getAttribute("data-cats").split("|")[0] === key; });
                if (!members.length) { return; }
                var section = document.createElement("section");
                section.className = "catalog-group";
                var h = document.createElement("h2");
                h.textContent = labels[key];
                var g = document.createElement("div");
                g.className = "catalog-grid";
                members.forEach(function (card) { g.appendChild(card); });
                section.appendChild(h);
                section.appendChild(g);
                groupsEl.appendChild(section);
            });
            groupsEl.hidden = false;
            grid.hidden = true;
        }

        function apply() {
            var shown = 0;
            regroup(state.cat === "all" && state.tech === "all" && !state.terms.length);

            cards.forEach(function (card) {
                var cats = card.getAttribute("data-cats").split("|");
                var tech = card.getAttribute("data-tech").split("|");
                var text = card.getAttribute("data-search");
                var ok =
                    (state.cat === "all" || cats.indexOf(state.cat) !== -1) &&
                    (state.tech === "all" || tech.indexOf(state.tech) !== -1) &&
                    state.terms.every(function (term) { return text.indexOf(term) !== -1; });

                card.hidden = !ok;

                if (ok) {
                    shown += 1;
                }
            });

            var message = "Showing " + shown + " of " + cards.length + " projects";

            if (count) { count.textContent = message; }
            if (status) { status.textContent = message; }
            if (none) { none.hidden = shown !== 0; }
        }

        apply();

        chips.forEach(function (chip) {
            chip.addEventListener("click", function () {
                var group = chip.getAttribute("data-group");

                state[group] = chip.getAttribute("data-filter");

                chips.forEach(function (other) {
                    if (other.getAttribute("data-group") === group) {
                        other.setAttribute("aria-pressed", String(other === chip));
                    }
                });

                apply();
            });
        });

        if (input) {
            input.addEventListener("input", function () {
                state.terms = input.value.toLowerCase().split(/\s+/).filter(Boolean);
                apply();
            });
        }
    }

    function initLightbox() {
        var links = document.querySelectorAll(".frame > a");
        var dialog, view, caption, closeBtn, opener;

        if (!links.length || typeof HTMLDialogElement === "undefined") {
            return;
        }

        function build() {
            if (dialog) { return; }
            dialog = document.createElement("dialog");
            dialog.className = "lightbox";
            dialog.setAttribute("aria-label", "Enlarged diagram");
            dialog.innerHTML =
                '<button type="button" class="lightbox-close" aria-label="Close enlarged diagram">Close</button>' +
                '<div class="lightbox-scroll"><img class="lightbox-img" alt=""></div>' +
                '<p class="lightbox-caption"></p>';
            document.body.appendChild(dialog);
            view = dialog.querySelector(".lightbox-img");
            caption = dialog.querySelector(".lightbox-caption");
            closeBtn = dialog.querySelector(".lightbox-close");
            closeBtn.addEventListener("click", function () { dialog.close(); });
            dialog.addEventListener("click", function (event) {
                if (event.target === dialog) { dialog.close(); }
            });
            dialog.addEventListener("close", function () {
                if (opener) { opener.focus(); }
            });
        }

        Array.prototype.forEach.call(links, function (link) {
            link.addEventListener("click", function (event) {
                var img = link.querySelector("img");
                var figcaption = link.parentNode.querySelector("figcaption");

                if (!img) { return; }
                event.preventDefault();
                build();
                opener = link;
                view.src = img.currentSrc || img.src;
                view.alt = img.alt;
                caption.textContent = figcaption ? figcaption.textContent : "";
                dialog.showModal();
                closeBtn.focus();
            });
        });
    }

    function initNav() {
        var btn = document.querySelector(".nav-toggle");
        var nav = document.getElementById("site-nav");
        if (!btn || !nav) { return; }
        btn.addEventListener("click", function () {
            var open = nav.classList.toggle("open");
            btn.setAttribute("aria-expanded", String(open));
        });
        document.addEventListener("keydown", function (e) {
            if (e.key === "Escape" && nav.classList.contains("open")) {
                nav.classList.remove("open");
                btn.setAttribute("aria-expanded", "false");
                btn.focus();
            }
        });
    }

    function init() {
        initNav();
        initCatalogue();
        initLightbox();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
