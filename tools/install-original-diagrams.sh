#!/usr/bin/env bash
# Copies the original architecture diagrams from each repository into assets/architecture/.
# Run from the portfolio root with network access. Review what it reports before committing.
set -euo pipefail
tmp=$(mktemp -d); dest=assets/architecture
get() { # repo, source path glob, destination name
  git clone --depth 1 -q "https://github.com/viradidi/$1.git" "$tmp/$1"
  f=$(find "$tmp/$1" -path '*/.git' -prune -o -type f -ipath "$2" -print | head -n1)
  if [ -n "$f" ]; then cp "$f" "$dest/$3"; echo "ok   $3  <-  ${f#$tmp/}"; else echo "MISS $3 (look in $1/architecture)"; fi
}
get uber-eats-data-analytics-platform '*architecture/uber-eats-end-to-end-architecture.svg' uber-eats-architecture.svg
get 1NOVACART-CASE-STUDY '*overview*.svg' novacart-overview.svg
get 1NOVACART-CASE-STUDY '*detail*.svg' novacart-detailed.svg
get FLOWBRIDGE-SNOWFLAKE-PROJECT '*technical*architecture*.svg' flowbridge-technical-architecture.svg
get AtlasFlow '*architecture*.svg' atlasflow-architecture.svg
get healthgrid-data-platform '*architecture*overview*.png' healthgrid-architecture-overview.png
get CFPB-Consumer-Complaint-Analytics "*architecture/cfpb-consumer-complaint-analytics.webp" cfpb-consumer-complaint-analytics.webp
echo "If HealthGrid/CFPB files were copied as .png/.webp, update the two case pages and projects/index.html to point at them."
