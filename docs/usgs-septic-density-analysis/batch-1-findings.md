# Batch 1 Findings: USGS Septic Density Rollup

## Files Audited

- `datausgsseptic-density\BG2021_SepticDensities.csv`
- `datausgsseptic-density\BG2021_SewerEstimates.csv`
- `datausgsseptic-density\BG2021_PotMissing_Parcels.csv`

## Row Counts

- Density rows: 237,900
- Sewer estimate rows: 237,900
- Potential missing parcel rows: 1,344
- States or districts summarized: 49

## Top 10 By Medium-Estimate Septic Count

- Texas: 2,563,936 estimated septic tanks; 21.83% medium-predicted septic block groups
- North Carolina: 1,919,660 estimated septic tanks; 45.32% medium-predicted septic block groups
- Pennsylvania: 1,543,260 estimated septic tanks; 27.98% medium-predicted septic block groups
- Ohio: 1,470,026 estimated septic tanks; 27.38% medium-predicted septic block groups
- Michigan: 1,409,157 estimated septic tanks; 30.82% medium-predicted septic block groups
- Georgia: 1,370,984 estimated septic tanks; 34.58% medium-predicted septic block groups
- New York: 1,300,573 estimated septic tanks; 17.57% medium-predicted septic block groups
- Tennessee: 1,243,491 estimated septic tanks; 42.83% medium-predicted septic block groups
- Florida: 1,173,660 estimated septic tanks; 14.49% medium-predicted septic block groups
- Alabama: 1,161,532 estimated septic tanks; 52.8% medium-predicted septic block groups

## Top 10 By Statewide Medium-Estimate Density

- Connecticut: 21.782 estimated septic tanks/sq km; 16.67% high-density block groups
- Rhode Island: 19.468 estimated septic tanks/sq km; 8.72% high-density block groups
- Massachusetts: 18.924 estimated septic tanks/sq km; 10.45% high-density block groups
- Delaware: 18.326 estimated septic tanks/sq km; 13.37% high-density block groups
- Maryland: 15.771 estimated septic tanks/sq km; 10.27% high-density block groups
- New Jersey: 14.983 estimated septic tanks/sq km; 5.64% high-density block groups
- North Carolina: 14.928 estimated septic tanks/sq km; 22.97% high-density block groups
- Ohio: 13.757 estimated septic tanks/sq km; 11.49% high-density block groups
- Pennsylvania: 13.152 estimated septic tanks/sq km; 12.56% high-density block groups
- New Hampshire: 11.679 estimated septic tanks/sq km; 23.09% high-density block groups

## Interpretation Guardrails

- Use this as a modern modeled density signal, not exact current septic usage by state.
- Do not present this as an official USGS ranking.
- Convert the numbers into homeowner questions: records, 811 limits, digging risk, and when septic-specific locating matters.
