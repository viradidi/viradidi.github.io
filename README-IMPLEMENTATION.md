# Portfolio update: change notes

Static site (HTML, CSS, one small JS file) for GitHub Pages. No build step, no dependencies.

## Files
| Path | Purpose |
|---|---|
| `index.html` | Single page: hero, about, services, 4 projects, practices, stack, resume, contact |
| `css/style.css` | One consolidated stylesheet (replaces ~3,500 lines of stacked patches) |
| `js/main.js` | Mobile menu + active-section marker only. Anchor links are native, so navigation works without JS |
| `assets/favicon.svg`, `assets/og-image.png` | Favicon and 1200x630 social-share image |
| `resume/Isaiah-Nyakundi-Data-Engineer-Resume.pdf` | One-page, text-selectable, ATS-friendly resume |

Removed: `assets/architecture/*.svg` (fixed-size images that became unreadable on phones; the diagrams are now HTML/CSS in `index.html`), dead project-toggle JS, the "Writing" section.

## What was wrong, and the fix
- **Navigation / in-page anchors:** the hero section made the page wider than the viewport (1452px on a 1280px screen, 621px on a 390px phone) and the nav had no mobile layout, so its links wrapped and overflowed. `overflow-x: hidden` on `body` hid the symptom. Fixed by removing the overflow source, using `overflow-x: clip`, `scroll-padding-top` for the sticky header, a real mobile menu button, and smooth scrolling only when reduced-motion is not requested.
- **Unverifiable claims removed:** Kafka/streaming, "Cloud Engineer", fake terminal output (`PASS analytical_models`), and a "Writing" section that linked repos as if they were articles.
- **Project cards** now state problem, flow, decisions, what is verified in the repo, and what is not there yet.

## Verification run (headless Chromium, 207 checks, 0 failures)
Widths 1440/1280/820/390: no horizontal overflow; no duplicate IDs; no dangling anchors; each nav link lands with its heading visible under the sticky header, from the top and from other sections; hash is set; back/forward work; mobile menu opens, closes after navigation and on Escape; direct `/#practices` load lands correctly; exactly 4 project cards, each button pointing at its own repo; external links have `rel="noopener"`; no console errors or failed requests; resume, favicon and share image return 200. Contrast: all text/button pairs >= 5.2:1.

Also verified against the repos: E-Commerce's 6 pytest tests all pass (run with a minimal stand-in for `pytest.raises`, because the pytest package could not be installed offline).

## Not verified / limitations
- PySpark and Databricks code was read, not executed.
- No real screenshots exist for these projects, so none are shown (no mock-ups are passed off as screenshots).
- LinkedIn URL (`.../limbaga-undefined-752bab429/`) looks auto-generated; please confirm it opens your profile.
- "Final-year" BSc and "2+ years freelance" are carried over from your existing site/resume; update if they have changed.
- `og:image` and canonical URLs assume the site is served at `https://viradidi.github.io/`.

## Repo issues found while auditing (outside this site)
1. **FlowBridge:** all nine `sql/*.sql` files and `docs/data-model.md`, `deployment.md`, `governance.md` are 0 bytes; no generator or Streamlit code. Commit the real files, then change the card status to a working-project badge.
2. **E-Commerce:** `dbt/profiles.yml` has a database password committed, and `docker-compose.env` is tracked. Move both to environment variables / an untracked `.env` and rotate the password.
3. **Novacart:** `upsert_to_gold` builds its merge condition as `target.{target_table} = source.{join_key}`, which will fail once the Gold table exists; the Bronze control table is created twice with different schemas; the README is one line.
4. **Retail:** README's "Running the Project" ends mid-command (`docker compose up -d`, no `spark-submit`).
