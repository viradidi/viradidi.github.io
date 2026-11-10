# Portfolio implementation notes

This repository is a static GitHub Pages site built with HTML, CSS and a small progressive-enhancement JavaScript file. There is no build step.

## Site files

| Path | Purpose |
|---|---|
| `index.html` | Portfolio page, project case-study summaries, diagram embeds and execution-evidence boundaries |
| `css/style.css` | Consolidated responsive stylesheet |
| `js/main.js` | Accessible mobile navigation and active-section highlighting |
| `assets/favicon.svg`, `assets/og-image.png` | Favicon and social preview image |
| `assets/architecture/` | Portfolio-local architecture diagrams |
| `resume/Isaiah-Nyakundi-Data-Engineer-Resume.pdf` | Existing résumé PDF |
| `docs/evidence/README.md` | Evidence capture and publication guide |

## Project inventory

The portfolio now presents six project cards:

1. Uber Eats — Azure multi-source analytics platform.
2. NovaCart — incremental Databricks lakehouse.
3. HealthGrid — metadata-driven Azure data platform.
4. FlowBridge — Azure-to-Snowflake supply-chain analytics.
5. AtlasFlow — local real-time logistics control tower.
6. CFPB Consumer Complaint Analytics — Microsoft Fabric project currently being finalized.

Execution statements are deliberately identified as owner-confirmed where that is the available basis. Architecture diagrams are design documentation, not proof of runtime execution.

## Architecture assets

- Uber Eats and both NovaCart SVG diagrams are copied into the portfolio repository so the page does not depend on GitHub's file-rendering URLs.
- FlowBridge now has a standalone technical SVG in its project repository and a portfolio-local copy. The README and architecture guide embed the standalone SVG alongside the Mermaid source diagram.
- AtlasFlow has a portfolio architecture SVG derived from its README and manual runbook.
- HealthGrid continues to use its existing repository architecture image.
- The original CFPB Microsoft Fabric image supplied by the project owner is to be placed at `assets/architecture/cfpb-consumer-complaint-analytics.png`. The portfolio currently shows an explicit asset-placement note rather than a broken image or a replacement diagram.

## Execution evidence

No runtime screenshots or query records have been fabricated. The FlowBridge and AtlasFlow cards contain explicit capture checklists for authentic artifacts from the owner's environments:

- FlowBridge: Snowflake Query History, serving-view results, relevant object status and dashboard.
- AtlasFlow: Docker Compose service health, three Flink job states, Trino Gold query results and Superset dashboard.

See `docs/evidence/README.md` for capture guidance and recommended filenames.

## Important evidence distinction

- Owner-confirmed execution means the project owner reports successful execution in the intended environment.
- Repository CI demonstrates only the checks actually run by the workflow.
- An architecture image explains design.
- A runtime screenshot or exported query record is published execution evidence only when it comes from the actual environment and is dated and described accurately.

## Verification still required before calling the portfolio release fully reviewed

The source has been updated, but a real browser check on GitHub Pages remains outstanding. Before public sign-off, inspect the page at desktop and mobile widths, verify all six project links, check each diagram loads, open the résumé link, and confirm the mobile navigation and keyboard controls. Add the real runtime evidence after capturing it from the corresponding environments.
