# Surplus Crown

[Open Surplus Crown](https://coolcode.ca/surplus-crown/)

Follow federal sale listings, land identified for housing and Nova Scotia’s recorded land disposals. See which source supports each status and price.

<!-- coolcode:guide -->
Search Upper Tantallon to compare the Nova Scotia disposal files and the contract prices recorded for different parcels. Choose Federal sale listing to see asking prices separately. Provincial files have no parcel coordinates.
<!-- /coolcode:guide -->

## Using the records

The three collections represent different events. Federal listings use published asking prices and are mapped only if an exact DFRP property number yields one coordinate-bearing parcel. The Public Land Bank layer includes the statuses actually returned by its service, including completed cases. Housing suitability does not establish vacancy, sale terms or transfer of title. Nova Scotia disposals have fiscal years and prices as filed. Recipients and mailing addresses are excluded. That table has no coordinates, and county-level locations do not identify a parcel. The weekly job preserves the first observed date of each changed federal listing status or asking price, with a separate label if the item disappears. Historical events before the first capture need other evidence. The same underlying property can appear in two source collections.

Search, filter and download every matching record. Selecting a result exposes a shareable record URL. The local Natural Earth backdrop and zoomable point groups work from the deployed files. The optional street-map switch requests tiles from OpenStreetMap. Sources without coordinates still appear in the list and export.

## Sources and verification

- [Federal real estate for sale](https://open.canada.ca/data/en/dataset/e7a3accb-d419-4d8a-b612-0a601ba4540c)
- [Canada Public Land Bank](https://www.canada.ca/en/public-services-procurement/services/infrastructure-buildings/public-lands-homes/bank-mapping-tool.html)
- [Nova Scotia real property disposals](https://data.novascotia.ca/d/2kw3-tjdw)

Contains information licensed under the [Open Government Licence – Canada](https://open.canada.ca/en/open-government-licence-canada). Nova Scotia records are licensed under the [Nova Scotia Open Government Licence](https://novascotia.ca/opendata/licence.asp). Housing locations, identifiers and public project-stage facts are attributed to PSPC’s Canada Public Land Bank. The ArcGIS publisher describes this layer as a reference. Province and state outlines derive from the [Natural Earth 1:50m admin-1 with lakes](https://www.naturalearthdata.com/) public-domain dataset. The bundled [Leaflet](https://leafletjs.com/) license is in web/vendor/LICENSE. The street layer contains © OpenStreetMap contributors.

The site derives dates and counts from each successfully retrieved edition. A weekly GitHub Actions job fetches and validates the source files, checks the app and commits the resulting snapshot. A failed refresh leaves the last working deployment available. The static build expands checked-in regional gzip files. No registration or API key is required.

Run `python scripts/refresh.py` to retrieve sources, `python -m unittest discover -s tests` and `node --test tests/*.test.mjs` for validation, and `python scripts/build.py` to build the site. For local preview run `python -m http.server --directory dist`.

<!-- schedule-reliability -->
## Schedule reliability

Public GitHub repositories can have scheduled workflows disabled after 60 days of inactivity. A separate weekly [schedule guard](.github/workflows/schedule-guard.yml) calls GitHub's enable-workflow API for an explicit list of refresh workflows and itself. It can restore workflows disabled for inactivity, preserves manually disabled workflows, and runs independently of collection failures.

This is an interim mitigation, not a scheduling guarantee: GitHub does not document active-workflow renewal as a permanent exemption, and scheduled runs can be delayed or dropped. A scheduler on our own Linux server is the planned independent trigger. The guard does not collect data, create dummy commits, or change source/check timestamps; successful collection and published data freshness still need monitoring.
<!-- /schedule-reliability -->
