# Portfolio implementation notes

Static HTML, CSS and JavaScript for GitHub Pages. No framework, no build step, no backend.
Live site: https://viradidi.github.io/

## Site map

| URL | Purpose |
|---|---|
| `/` | Home: introduction, stats, four featured projects, tools, writing, and a link to the full catalogue |
| `/projects/` | Engineering Projects catalogue: search, discipline filters, technology filters |
| `/projects/atlasflow/` | Case study 1 |
| `/projects/healthgrid/` | Case study 2 |
| `/projects/uber-eats/` | Case study 3 |
| `/projects/novacart/` | Case study 4 |
| `/projects/flowbridge/` | Case study 5 |
| `/projects/cfpb/` | Case study 6 |
| `/about.html`, `/cv.html` | Background and CV |
| `/blog.html` and `/post-*.html` | Blog index and three posts |
| `/404.html` | Not-found page |

All internal links are root-absolute (`/projects/...`), which is correct for a user site served from the domain root.

## Project inventory

| Project | Disciplines | Status | Repository | Architecture asset |
|---|---|---|---|---|
| AtlasFlow | Streaming and real-time; Data platform architecture | Completed, local Docker Compose | `AtlasFlow` | `assets/architecture/atlasflow-architecture.svg` |
| HealthGrid | Cloud and lakehouse; Data platform architecture | Completed, run in Azure | `healthgrid-data-platform` | `assets/architecture/healthgrid-architecture-overview.png` |
| Uber Eats | Cloud and lakehouse; Data platform architecture; Warehouse and analytics | Completed, run in Azure | `uber-eats-data-analytics-platform` | `assets/architecture/uber-eats-architecture.svg` |
| NovaCart | Cloud and lakehouse; Warehouse and analytics | Completed, run in Azure Databricks | `1NOVACART-CASE-STUDY` | `assets/architecture/novacart-overview.svg`, `novacart-detailed.svg` |
| FlowBridge | Warehouse and analytics; Data platform architecture | Completed, latest version rerun in Snowflake on 8 November 2026 | `FLOWBRIDGE-SNOWFLAKE-PROJECT` | `assets/architecture/flowbridge-technical-architecture.svg` |
| CFPB | Warehouse and analytics; Cloud and lakehouse | Completed, Microsoft Fabric | `CFPB-Consumer-Complaint-Analytics` | `assets/architecture/cfpb-consumer-complaint-analytics.webp` |

A project can appear under several disciplines. It still has one case-study page.

## Assets that must exist

The diagrams are the original files from each project and are never redrawn. They live in `assets/architecture/`:

- `atlasflow-architecture.svg`, `uber-eats-architecture.svg`, `novacart-overview.svg`, `novacart-detailed.svg`, `flowbridge-technical-architecture.svg`
- `cfpb-consumer-complaint-analytics.webp` (copy it from the CFPB repository's `architecture/` folder)
- `healthgrid-architecture-overview.png` (included)

`assets/og-image.png` is the social-share image. `resume/Isaiah-Nyakundi-Data-Engineer-Resume.pdf` is the CV download.

## How the pages work

- **Catalogue:** each `.project-card` carries `data-cats`, `data-tech` and `data-search`. `js/main.js` filters on all three at once. Without JavaScript every card is shown and the controls are hidden.
- **Case studies:** nine sections in a fixed order (hero, business problem, architecture, how it works, engineering decisions, reliability and testing, deployment, evidence and boundaries, documentation), then previous and next project links.
- **Diagrams:** each opens in a native `<dialog>` lightbox. Without JavaScript the link opens the image in a new tab. On phones the image keeps a readable minimum width and scrolls inside its frame.

## Adding a project

1. Copy a folder under `projects/` to `projects/<name>/` and edit the sections.
2. Add a card to `projects/index.html` with the `data-cats`, `data-tech` and `data-search` attributes.
3. Add the diagram to `assets/architecture/`.
4. Add the URL to `sitemap.xml`, and the previous and next links on the neighbouring case studies.

## Security and quality

A Content Security Policy meta tag on every page (own-site scripts, styles and images only), a referrer policy, `rel="noopener noreferrer"` on external links, no inline scripts or styles, no third-party requests, AA text contrast, a skip link, keyboard-operable filters and lightbox, reduced-motion support, print styles and structured data. `.nojekyll` makes GitHub Pages serve the files as they are.

## Verification boundaries stated on the case studies

Each case study separates repository checks (static validation and unit tests) from execution in the cloud or local environment. Some Azure environments were decommissioned after a successful run to control cost, and the pages state this plainly.
