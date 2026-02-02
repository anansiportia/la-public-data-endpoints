# LA Public Data Endpoints Catalog

This repo contains a tested catalog of public government data endpoints across Los Angeles County and nearby cities. Each entry includes a working sample query URL.

## Files
- **la_public_data_endpoints_catalog.json** — structured catalog (machine‑readable)
- **la_public_data_endpoints_catalog.md** — readable catalog for quick browsing

## Fields (per entry)
- **Source** — Portal or system name
- **Jurisdiction** — City/County
- **Dataset/Service** — Name of dataset or service
- **Endpoint URL** — Base API endpoint
- **Sample Query URL** — Minimal query to verify working access
- **Data Type** — Socrata / ArcGIS REST / OpenDataSoft / etc.
- **Notes** — Any important details

## Data Integrity
- Endpoints are tested with minimal queries (usually 1 record) to confirm they respond.
- No scraping of gated pages; only public APIs and official datasets.

## Contributing / Expanding
If you know of additional public portals in LA‑area cities, open an issue or PR.
