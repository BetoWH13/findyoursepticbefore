# Batch 2: V2 Page Blueprint

## Strategic Angle

V2 should not be framed only as "rural states use septic." That is obvious and less useful.

The stronger angle is:

**Septic risk is easiest to notice in rural areas, but easiest to overlook in urban-edge, suburban, older, coastal, lake, and formerly rural neighborhoods.**

This lets the page serve both obvious rural users and the more valuable user who assumes "I probably have sewer" because the area looks developed.

## Core User Concern

The V2 page should answer:

"If I live in a developed or suburban area where septic is not obvious, what should I check before digging?"

The practical answer:

- Do not assume sewer just because the neighborhood looks urban.
- Check whether the home has a sewer bill or municipal sewer connection record.
- Look for septic permits, old inspection records, transfer documents, and health department files.
- Call 811 before digging, but do not assume 811 marks private septic tanks, septic lines, or drain fields.
- Be extra careful before fence posts, landscaping, trenching, pools, sheds, additions, grading, or driveway work.
- Use septic-specific locating when records are missing and the work area is near the likely tank, line, or drain field path.

## Why The USGS Data Supports This Angle

The Batch 1 rollup showed states with high modeled statewide septic density even where many residents may think of the area as urban or suburban:

- Connecticut
- Rhode Island
- Massachusetts
- Delaware
- Maryland
- New Jersey
- Ohio
- Pennsylvania
- New York

These states do not all fit the simple "remote rural septic" stereotype. That supports a practical homeowner message: septic risk can be concentrated in older suburbs, small towns, coastal communities, lake areas, unincorporated pockets, and development edges.

## Recommended V2 Page Structure

### 1. Short Answer

Explain that septic use is not only a rural issue. Rural properties are more obvious, but developed-looking neighborhoods can still have private septic systems, older onsite systems, or mixed sewer/septic patterns.

### 2. State Lookup Tool

Keep the state selector, but add a "Modern USGS modeled signal" field:

- Estimated exposure: high total count / high density / localized signal
- Data confidence: strong, moderate, parcel gaps possible
- Best next step: records, 811, septic-specific locating

### 3. Three Ways To Read Septic Risk

- Historical reliance: Census 1990 shows where septic was common.
- Modern modeled density: USGS shows where septic density may still be concentrated.
- Property-level uncertainty: a single address still needs records or locating.

### 4. Urban and Suburban Septic Trap

This should become a major V2 section.

Suggested heading:

"Why septic can still matter in developed-looking neighborhoods"

Suggested content points:

- Some neighborhoods were built before sewer expansion.
- Some homes remain on septic even after nearby sewer became available.
- City mailing addresses can include unincorporated or partially sewered areas.
- Older homes, private wells, lake communities, coastal areas, and large-lot suburbs can still use septic.
- A sewer line in the street does not prove the house is connected.

### 5. What Urban/Suburban Homeowners Should Do Before Digging

Turn this into a simple checklist:

- Check for a sewer bill or municipal wastewater account.
- Check the property disclosure, inspection report, and closing documents.
- Search local health department or county septic records.
- Call 811 before digging.
- Do not treat absent 811 septic marks as proof that no septic system exists.
- If records are missing, locate the tank, line, and drain field before posts, trenches, trees, patios, pools, or additions.

### 6. Modern USGS Findings In Plain English

Use three mini-rankings:

- High total estimated systems: useful for big-state exposure.
- High density signal: useful for developed/suburban states.
- High septic-block-group share: useful for rural/historical signal.

Each ranking should have a plain-language explanation and a caveat.

### 7. Practical Next-Step Cards

Link to:

- Fence installation guide
- Landscaping guide
- 811 vs septic guide
- Septic records by state
- Property records guide
- Private utility locator guide

### 8. Attribution and Methodology

Credit the USGS creators visibly:

- Brennon K. Peterson
- Stephanie E. Gordon
- Brianna M. Williams
- Rachel M. Atkins
- Labeeb Ahmed
- Serena M. Seawolf
- U.S. Geological Survey
- DOI: https://doi.org/10.5066/P1WCYDPB

Include non-endorsement language:

"FindYourSepticBefore.com interpreted the public USGS dataset for homeowner education. This page is not an official USGS ranking, endorsement, or property-level septic determination."

## Recommended User-Friendly Labels

Avoid raw technical labels in the public UI.

- `MS_SepCnt` -> "Modeled septic exposure"
- `MS_SepDn` -> "Modeled septic density"
- `MedSewer = NO` -> "Block groups more likely septic-supported"
- `missing parcel rows` -> "Data confidence caution"
- `rank_ms_density` -> "Density signal rank"

## Content Rule

Every number shown on V2 must answer a homeowner question. If a metric does not help someone decide what to check before digging, it should stay in the methodology or not appear on the page.
