
/*
 * Portfolio progressive enhancements
 *
 * Features:
 * - Accessible mobile navigation
 * - Outside-click and Escape-to-close behavior
 * - Active navigation section highlighting
 * - Graceful handling of optional browser APIs
 *
 * Navigation links remain ordinary HTML anchors, so the site remains
 * navigable if JavaScript or IntersectionObserver is unavailable.
 */
(function () {
    "use strict";

    function initNavigation() {
        var toggle = document.querySelector(".nav-toggle");
        var menu = document.getElementById("nav-menu");
        var links = Array.prototype.slice.call(
            document.querySelectorAll(".nav-links a[href^='#']")
        );

        /* Mobile navigation */
        function setMenu(open) {
            if (!toggle || !menu) {
                return;
            }

            toggle.setAttribute("aria-expanded", String(open));
            menu.classList.toggle("is-open", open);
        }

        if (toggle && menu) {
            toggle.addEventListener("click", function () {
                var isOpen =
                    toggle.getAttribute("aria-expanded") === "true";

                setMenu(!isOpen);
            });

            menu.addEventListener("click", function (event) {
                var target = event.target;

                if (
                    target &&
                    typeof target.closest === "function" &&
                    target.closest("a[href]")
                ) {
                    setMenu(false);
                }
            });

            document.addEventListener("click", function (event) {
                var isOpen =
                    toggle.getAttribute("aria-expanded") === "true";

                if (
                    isOpen &&
                    !menu.contains(event.target) &&
                    !toggle.contains(event.target)
                ) {
                    setMenu(false);
                }
            });

            document.addEventListener("keydown", function (event) {
                if (
                    event.key === "Escape" &&
                    toggle.getAttribute("aria-expanded") === "true"
                ) {
                    setMenu(false);
                    toggle.focus();
                }
            });

            /*
             * Reset the mobile menu when the desktop breakpoint is reached.
             * Support older browsers that expose addListener instead.
             */
            if (typeof window.matchMedia === "function") {
                var desktopQuery = window.matchMedia("(min-width: 861px)");

                var handleBreakpointChange = function (event) {
                    if (event.matches) {
                        setMenu(false);
                    }
                };

                if (typeof desktopQuery.addEventListener === "function") {
                    desktopQuery.addEventListener(
                        "change",
                        handleBreakpointChange
                    );
                } else if (
                    typeof desktopQuery.addListener === "function"
                ) {
                    desktopQuery.addListener(handleBreakpointChange);
                }

                handleBreakpointChange(desktopQuery);
            }
        }

        /* Active section highlighting */
        if (
            !links.length ||
            !("IntersectionObserver" in window)
        ) {
            return;
        }

        var sections = [];
        var activeLink = null;

        links.forEach(function (link) {
            var href = link.getAttribute("href");

            if (!href || href.length < 2) {
                return;
            }

            var id = href.slice(1);

            /*
             * Only observe real sections that correspond to navigation links.
             */
            var section = document.getElementById(id);

            if (!section) {
                return;
            }

            var alreadyRegistered = sections.some(function (item) {
                return item.section === section;
            });

            if (!alreadyRegistered) {
                sections.push({
                    section: section,
                    link: link
                });
            }
        });

        if (!sections.length) {
            return;
        }

        function clearActiveLink() {
            links.forEach(function (link) {
                link.removeAttribute("aria-current");
            });

            activeLink = null;
        }

        function setActiveLink(link) {
            if (!link || activeLink === link) {
                return;
            }

            clearActiveLink();

            link.setAttribute("aria-current", "location");
            activeLink = link;
        }

        var observer = new IntersectionObserver(
            function () {
                /*
                 * Choose the section nearest the activation line rather than
                 * relying on the order of entries in the observer callback.
                 */
                if (window.scrollY < 120) {
                    clearActiveLink();
                    return;
                }

                var activationLine = window.innerHeight * 0.35;
                var bestSection = null;
                var bestDistance = Infinity;

                sections.forEach(function (item) {
                    var rect = item.section.getBoundingClientRect();

                    if (
                        rect.top <= activationLine &&
                        rect.bottom > activationLine
                    ) {
                        bestSection = item;
                        bestDistance = 0;
                        return;
                    }

                    if (bestDistance === 0) {
                        return;
                    }

                    var distance = Math.abs(rect.top - activationLine);

                    if (distance < bestDistance) {
                        bestDistance = distance;
                        bestSection = item;
                    }
                });

                if (bestSection) {
                    setActiveLink(bestSection.link);
                }
            },
            {
                rootMargin: "-30% 0px -60% 0px",
                threshold: 0
            }
        );

        sections.forEach(function (item) {
            observer.observe(item.section);
        });

        window.addEventListener(
            "scroll",
            function () {
                if (window.scrollY < 120) {
                    clearActiveLink();
                }
            },
            { passive: true }
        );
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initNavigation);
    } else {
        initNavigation();
    }
})();
