# Portfolio execution evidence guide

This folder documents how to add genuine runtime evidence to the AtlasFlow and FlowBridge portfolio entries. It does not contain mock screenshots.

## Evidence rules

- Capture directly from the actual local or cloud environment.
- Keep the original timestamp visible where possible.
- Do not alter query results, job states, service health indicators or execution dates.
- Crop only to remove irrelevant browser chrome or sensitive fields; do not change the technical content.
- Redact credentials, tokens, account identifiers, personal data, email addresses and private hostnames.
- Add a short caption stating the environment, date and what the image proves.
- Architecture diagrams and conceptual illustrations must not be presented as runtime evidence.
- An owner-confirmed run can be stated as such even before screenshots are available.

## AtlasFlow

Recommended destination: `assets/evidence/atlasflow/`

| Filename | Capture | What it demonstrates |
|---|---|---|
| `01-docker-compose-status.png` | `docker compose ps` or Docker Desktop service view | Local containers and health state at capture time |
| `02-flink-running-jobs.png` | Flink dashboard | Bronze, Silver and Gold streaming jobs and their actual states |
| `03-trino-gold-query.png` | Trino query and returned rows | A real query against `atlasflow.gold.shipment_control_tower` |
| `04-superset-control-tower.png` | Superset dashboard | Gold-backed shipment and risk analytics |

Suggested caption: "AtlasFlow local integration run — captured [actual date]. This image shows [specific state/result]."

## FlowBridge

Recommended destination: `assets/evidence/flowbridge/`

| Filename | Capture | What it demonstrates |
|---|---|---|
| `01-snowflake-query-history.png` | Snowsight Query History | Successful SQL execution and actual execution timestamps |
| `02-serving-view-results.png` | Query result for `FLOWBRIDGE_PROD_DB.SERVING_SCH.VW_SUPPLY_CHAIN_OVERVIEW` | Real rows returned by the governed serving view |
| `03-pipeline-object-status.png` | Relevant Snowpipe, Task or Dynamic Table status | The actual object state or refresh evidence available in the account |
| `04-streamlit-dashboard.png` | FlowBridge Streamlit app | A dashboard view backed by the Snowflake serving objects |

The owner has confirmed a successful end-to-end Snowflake rerun on 8 November 2026. Use that date only for artifacts genuinely captured from that run. Any later validation must be labelled with its actual date.

## Publish sequence

1. Place the original screenshots in the corresponding folder.
2. Add a short Markdown caption beside each image or link it from the relevant project card.
3. Confirm that no sensitive values are visible.
4. Check that each image is readable on mobile.
5. Keep the source files unchanged; do not replace them with generated mockups.

## Status

The portfolio currently records the successful runs as owner-confirmed and leaves runtime screenshot slots pending capture. This is intentional and honest.
