# Isaiah Nyakundi: portfolio site

Personal portfolio of a data engineer, hosted on GitHub Pages at https://viradidi.github.io/

A plain static site: HTML, one stylesheet and a small script for the project filter. No build step, no framework.

## Pages

`/` home, `/projects/` catalogue, `/projects/<name>/` six case studies, `/about.html`, `/blog.html` with three posts, `/cv.html`, `/404.html`. See `README-IMPLEMENTATION.md`.

## Folders

```
css/style.css          all styling
js/main.js             project filter
assets/architecture/   the original architecture diagrams (SVG and PNG), used unchanged
resume/                CV PDF linked from the site
```

## Content rules

- Every project carries a status that says how it was run.
- Every architecture diagram is the original file from its project, loaded from `assets/architecture/` and never redrawn.
- These are portfolio projects. No client engagements are listed.

## Run locally

```
python -m http.server 8000
```

## Hardening

- **Content Security Policy** (meta tag on every page): scripts, styles, images and fonts only from this site, no network connections, no plugins, no forms. The pages contain no inline scripts or styles.
- **Referrer policy** `strict-origin-when-cross-origin`, and every external link uses `rel="noopener noreferrer"`.
- **No third-party requests**: no analytics, fonts, CDNs or embeds.
- **`.nojekyll`** so GitHub Pages serves the files exactly as they are.
- **Accessibility**: skip link, landmarks, keyboard-operable diagram lightbox with focus return, visible focus rings, reduced-motion support, and text colours that meet WCAG AA contrast (4.5:1).
- **SEO and sharing**: canonical URLs, sitemap, social-share image (`assets/og-image.png`), structured data for the person and for each blog post.
- **Print styles** for a clean CV.

GitHub Pages cannot send HTTP headers, so `frame-ancestors`, `X-Frame-Options` and HSTS cannot be set from the repository.
Turn on "Enforce HTTPS" in Settings > Pages.


## Development and deployment

- Static HTML, CSS and JS. No build step. Preview locally with `python3 -m http.server 8000` and open http://localhost:8000.
- Deploy: push to the `main` branch of `viradidi/viradidi.github.io` (Settings > Pages > Deploy from branch). `.nojekyll` is included.
- Internal links are root-absolute, so the site must be served from the domain root.

## Architecture diagrams: action needed

The upload did not include the original diagrams. Every file in `assets/architecture/` is currently a **generated fallback** drawn from each README's component list (each carries a visible note saying so). They are not the original diagrams.

To use the originals, run `tools/install-original-diagrams.sh` (needs network), or copy the files by hand using the same filenames. For HealthGrid (`.png`) and CFPB (`.webp`), also change the image paths in their case pages and `projects/index.html`. `tools/make_diagrams.py` regenerates the fallbacks.

## Content notes

- CFPB is labelled Completed, per the project owner. The case study states that deployment is manual DEV-to-PROD promotion, not Git-triggered CI/CD. The repo README still has a placeholder for the exact Kaggle dataset URL.
- AtlasFlow's case study mentions Prometheus, Grafana, Kafka UI and the Flink dashboard. Confirm against the repo.
