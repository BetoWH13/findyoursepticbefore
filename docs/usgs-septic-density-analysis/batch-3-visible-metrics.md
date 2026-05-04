# Batch 3: Visible Metrics and UI Rules

## Rule

Only show metrics that help a homeowner decide what to check before digging. Keep technical fields out of the main UI unless they are translated into plain-English labels.

## Recommended Public Metrics

### Good To Show

- Modern USGS signal label.
- Estimated septic exposure rank, if phrased as "among the higher modeled counts" or "top 10 by modeled count."
- Density signal rank, if phrased as "high modeled density signal."
- Predicted septic-supported block group share, rounded to one decimal or simplified into a category.
- Parcel-data caution, only when it affects confidence.

### Use Sparingly

- Estimated septic count. This can be useful for rankings, but it should be called a modeled medium estimate and not an exact current count.
- Septic tanks per square kilometer. This is useful for methodology and rankings, but many homeowners will not understand it without explanation.

### Do Not Show In Main UI

- `HS_SepCnt`
- `MS_SepCnt`
- `LS_SepCnt`
- `HS_SepDn`
- `MS_SepDn`
- `LS_SepDn`
- raw `MedSewer`, `HighSewer`, or `LowSewer` flags
- raw block group counts unless needed in methodology

## Public Label Mapping

- `MS_SepCnt` -> "modeled medium-estimate septic count"
- `MS_SepDn` -> "modeled septic density"
- `med_predicted_septic_bg_pct` -> "share of block groups with a septic-supported signal"
- `missing_parcel_bg_pct` -> "parcel-data confidence caution"
- `rank_ms_count` -> "modeled count rank"
- `rank_ms_density` -> "modeled density rank"

## UI Recommendation

For the state selector, show compact fields:

- Modern signal: `Urban/suburban hidden-septic signal`
- What it means: one plain-English sentence
- Confidence: one sentence
- Best next step: one action-oriented sentence

Avoid more than two numeric values in the selector result. If numbers are included, use:

- modeled count rank
- septic-supported block group share

## Mini-Ranking Recommendation

Use three small rankings instead of a giant table:

- High total estimated systems
- High statewide density signal
- High septic-supported block group share

Each ranking should include a one-sentence "why this matters before digging" explanation.

## Methodology Placement

Detailed numbers and caveats should live below the useful sections, near attribution. The methodology can mention that the analysis used the medium USGS estimate as the main homeowner-facing signal and retained high/low estimate fields for internal comparison.
