# Asia Compass data methodology

## Trust rule

The application distinguishes catalog guidance from researched evidence. A current
cost requires a collection date, a defined traveler profile, and at least one
traceable source. When destination-level evidence is unavailable, the application
may use a named nearby-base or country proxy only when the scope is stored, displayed,
and assigned Low confidence. A proxy is never described as destination-level evidence.

## Daily ground-spending basket

A ground-spending estimate is per person/day and excludes accommodation and flights.
The primary source's published daily total includes accommodation, ordinary meals,
local transportation, and sightseeing. The stored ground estimate is the published
per-person daily total minus its published one-person accommodation amount.

This calculation avoids adding category figures that the source identifies as a
mixture of per-day and per-purchase averages. Food, transportation, and activity
figures are retained in the CSV as useful source context, but they are not summed for
Budget Your Trip records.

Users enter a total on-trip spending budget and trip length. The application divides
the total by the number of days and compares that daily amount with the sourced
ground-spending estimate.

At 125% or more of the sourced typical value, the UI says comfortably within budget;
at or above the typical value, within estimated budget; within 20% below it, stretch
budget; otherwise, above budget. This is a transparent project decision, not an
international standard.

## Representative accommodations

Accommodation records identify real properties in or near a destination. They do not
claim room availability or a current nightly price. Availability requires travel
dates and a live provider query. City and resort destinations prefer hotels or
resorts; remote parks, routes, and wilderness areas may instead show a lodge, hut,
camp, guesthouse, or another locally appropriate stay type.

Existing Myanmar pilot records use official property websites or government tourism
registries. Wider catalog coverage uses named accommodation features contributed to
OpenStreetMap. The project stores the exact OpenStreetMap feature URL, collection
date, selected nearby base, and approximate straight-line distance from that base.
An OpenStreetMap feature proves that a named mapped record existed when collected; it
does not independently prove that the business is operating. OpenStreetMap data is
© OpenStreetMap contributors and licensed under the ODbL. See
https://www.openstreetmap.org/copyright.

## Accommodation confidence

- High: a current official property/provider page directly supports the record.
- Medium: a current government registry supports it, or an OpenStreetMap record
  includes a property website that can be checked separately.
- Low: an OpenStreetMap identity has no property website, or the evidence is otherwise
  uncorroborated. The UI must clearly disclose this limitation.

Accommodation evidence should be reviewed at least every 6–12 months and immediately
when a source says a property suspended or closed.

## Cost evidence and confidence

The primary source is Budget Your Trip, which publishes traveler-reported destination
and country averages and permits referencing its costs with a link back. The exact
source URL is stored on every row.

- Medium: a complete destination page supplies a per-person daily total and a
  one-person accommodation value.
- Low: the value comes from a named nearby base, a country page, or a supplementary
  country model/breakdown. Strict affordability mode does not accept Low-confidence
  records.

Budget Your Trip does not provide a complete page for every catalog country. Brunei
uses a dated 2026 firsthand mid-range category breakdown from Never Ending Footsteps;
Timor-Leste uses a 2026 mid-range category breakdown from Explore Every Country; and
Turkmenistan uses an August 2026 standard-traveler model from Travel Cost Calculator.
These are stored as Low-confidence country proxies.

The current Goa and Kerala destination pages are excluded because their derived
ground-spending amounts are extreme outliers against the same source's India country
benchmark. Both use the India country proxy and disclose that decision in their notes.

All cost evidence should be reviewed at least every 6–12 months. Traveler averages
and country models are planning estimates, not live prices or guarantees.

## Coverage

Representative accommodation and cost-evidence coverage span the full 160-destination
catalog. Accommodation evidence mixes higher-confidence official/government Myanmar
records with reproducible OpenStreetMap records elsewhere. Cost evidence includes 58
destination-level records and 102 disclosed nearby-base/country proxies. These
evidence levels are not equivalent, so confidence and scope are displayed per record.

## Destination photos

The application stores one freely licensed Wikimedia Commons image for every catalog
destination under `assets/destinations`. The accompanying `manifest.json` records the
matched Wikipedia article, Commons file page, creator, license, license URL, source
image URL, and download timestamp. The UI links each local image back to its Commons
file page and displays its available creator and license attribution.

Run `python scripts/download_destination_images.py` to audit local coverage and fill
missing files. Use `--refresh` to replace existing valid files. The downloader uses
standard-width Wikimedia thumbnails, rate limiting, retries, and direct Commons
search when a Wikipedia article has no suitable free lead image. Maps, flags, logos,
route diagrams, and satellite imagery are rejected because this feature requires
destination photographs.
