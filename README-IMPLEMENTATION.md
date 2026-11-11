# Portfolio implementation notes

This repository is a static GitHub Pages site built with HTML, CSS and a small progressive-enhancement JavaScript file. There is no build step.

## Site files

| Path | Purpose |
|---|---|
| `index.html` | Portfolio page, six project case studies, architecture diagrams and execution status |
| `css/style.css` | Responsive design system and project-diagram presentation |
| `js/main.js` | Accessible mobile navigation and active-section highlighting |
| `assets/favicon.svg`, `assets/og-image.png` | Favicon and social preview image |
| `assets/architecture/` | Portfolio-local architecture diagrams |
| `resume/Isaiah-Nyakundi-Data-Engineer-Resume.pdf` | Résumé PDF |

## Project inventory

The portfolio presents six project cards:

1. Uber Eats — Azure multi-source analytics platform.
2. NovaCart — incremental Databricks lakehouse.
3. HealthGrid — metadata-driven Azure data platform.
4. FlowBridge — Azure-to-Snowflake supply-chain analytics.
5. AtlasFlow — local real-time logistics control tower.
6. CFPB Consumer Complaint Analytics — Microsoft Fabric project currently in progress.

The first five projects are described as successfully executed end to end in their intended environments. The CFPB Microsoft Fabric project remains in progress and is not described as completed.

## Architecture assets

- Uber Eats and both NovaCart SVG diagrams are copied into the portfolio repository so the page does not depend on GitHub's file-rendering URLs.
- FlowBridge has a standalone technical SVG in its project repository and a portfolio-local copy. The README and architecture guide embed the standalone SVG alongside the Mermaid source diagram.
- AtlasFlow has a portfolio architecture SVG based on its README and manual runbook.
- HealthGrid continues to use its existing repository architecture image.
- The CFPB architecture image and project details will be incorporated as the Microsoft Fabric work progresses.

## Execution and documentation policy

The portfolio states the execution status of completed projects directly: each was successfully run end to end in its intended environment. Runtime screenshots are optional supporting material, not a prerequisite for presenting the completed work.

Repository CI statements remain scoped to what the corresponding workflow actually runs. Architecture diagrams explain system design; they are not described as runtime logs or benchmark results.

## Source-level verification

The source audit checks:

- all six project cards and repository links;
- local architecture asset paths;
- internal navigation targets;
- stylesheet and JavaScript references;
- responsive diagram styles and mobile navigation hooks.

A hosted browser review should still be performed after deployment at desktop and mobile widths to confirm rendering and live asset delivery. That review is separate from whether the completed data platforms ran end to end in their intended environments.
