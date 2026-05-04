# V2 Content Brief: Turning USGS Septic Density Into Homeowner Answers

## Batch 1 Conclusion

The USGS data is useful for V2, but the page should not become a technical data dump. The best homeowner-facing value is to separate three ideas that homeowners can understand:

- High total exposure: large states can have many estimated septic systems even when statewide density is moderate.
- High density exposure: smaller or more developed states can have high septic density per square kilometer.
- Property-specific caution: a state average can hide rural, suburban-edge, private-well, or unincorporated pockets where septic locating still matters.

## Practical Questions V2 Can Answer

- Is my state historically septic-heavy and still showing a modern modeled septic signal?
- Is my state not a top historical septic state, but still full of localized septic pockets?
- Before a fence, landscaping, trench, pool, shed, or addition, should I treat septic location as a real planning issue?
- Should I start with local records, 811, or septic-specific locating?
- How much confidence should I place in the data if parcel coverage is incomplete?

## Strong User-Friendly Findings From Batch 1

### Big Total Septic Exposure

The medium USGS estimate shows the largest modeled septic counts in states such as Texas, North Carolina, Pennsylvania, Ohio, Michigan, Georgia, New York, Tennessee, Florida, and Alabama. This supports a plain-English point: total exposure is high in large states, even when statewide density does not always rank at the top.

### High Statewide Density Signal

The highest statewide modeled septic density signals include Connecticut, Rhode Island, Massachusetts, Delaware, Maryland, New Jersey, North Carolina, Ohio, Pennsylvania, New Hampshire, Tennessee, and South Carolina. This supports a different point: smaller states and dense suburban states can still have serious septic-location relevance before digging.

### Strong Septic-Block-Group Signal

The highest share of medium-predicted septic block groups includes Vermont, Maine, West Virginia, Mississippi, Arkansas, South Dakota, Alabama, New Hampshire, Kentucky, Montana, Wyoming, Iowa, North Dakota, South Carolina, and North Carolina. This supports the historic-rural signal and helps explain why state averages alone are not enough.

### Focus-State Notes

- Vermont: strongest medium-predicted septic block-group signal among summarized states; good fit for records-first and before-digging caution.
- Maine: very strong medium-predicted septic signal, but also the highest parcel-gap flag in this rollup, so confidence language matters.
- New Hampshire: strong modeled density and septic-block-group signal; good bridge between New England history and modern density.
- Kentucky: high septic-block-group signal and meaningful estimated count; useful for county-record guidance.
- Tennessee: top-10 estimated count and high density rank; strong V2 candidate for practical before-digging guidance.
- Alabama: top-10 estimated count and high septic-block-group signal; strong V2 candidate.
- Mississippi: high septic-block-group signal; good rural-records and incomplete-documentation angle.
- New Mexico: lower statewide density, but enough septic-block-group signal and missing parcel caution to support localized-risk framing rather than a top-ranking claim.

## Attribution Requirements

V2 must visibly credit the dataset creators and publisher:

- Brennon K. Peterson
- Stephanie E. Gordon
- Brianna M. Williams
- Rachel M. Atkins
- Labeeb Ahmed
- Serena M. Seawolf
- U.S. Geological Survey
- DOI: https://doi.org/10.5066/P1WCYDPB

V2 should also state that FindYourSepticBefore.com is interpreting the public dataset for homeowner education and that the analysis is not an official USGS ranking, endorsement, or property-level determination.

## Recommended V2 User Interface

- Keep the existing state selector, but add a "Modern USGS signal" line where we have analyzed output.
- Add a simple sortable state table with columns homeowners can understand:
  - State
  - Modern septic signal
  - Estimated exposure
  - Data confidence note
  - Best homeowner next step
- Add a short "Why your state average can mislead you" explainer.
- Add three mini-rankings:
  - High total estimated systems
  - High statewide density signal
  - High septic-block-group share
- Keep all caveats close to the numbers, not hidden at the bottom.

## Do Not Do

- Do not publish a giant raw table with unexplained columns.
- Do not call this exact current septic usage by state.
- Do not imply USGS endorses our interpretation.
- Do not over-weight a statewide ranking when property-level risk is the homeowner's real concern.
