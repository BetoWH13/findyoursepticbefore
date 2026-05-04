#!/usr/bin/env python3
"""Build a small homeowner-facing V2 state payload from the USGS rollup."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_DIR = ROOT / "docs" / "usgs-septic-density-analysis"
SOURCE = ANALYSIS_DIR / "state-summary.csv"
OUT_JSON = ANALYSIS_DIR / "v2-state-payload.json"
OUT_CSV = ANALYSIS_DIR / "v2-state-payload.csv"

URBAN_SURPRISE_STATES = {"CT", "RI", "MA", "DE", "MD", "NJ", "OH", "PA", "NY"}
RURAL_HISTORY_STATES = {"VT", "ME", "WV", "MS", "AR", "SD", "AL", "NH", "KY", "MT", "WY", "IA", "ND", "SC", "NC"}
HIGH_TOTAL_STATES = {"TX", "NC", "PA", "OH", "MI", "GA", "NY", "TN", "FL", "AL"}


def as_int(value: str) -> int:
    return int(float(value or 0))


def as_float(value: str) -> float:
    return float(value or 0)


def exposure_label(row: dict[str, str]) -> str:
    abbr = row["state_abbr"]
    count_rank = as_int(row["rank_ms_count"])
    density_rank = as_int(row["rank_ms_density"])
    septic_bg_pct = as_float(row["med_predicted_septic_bg_pct"])

    if abbr in URBAN_SURPRISE_STATES:
        return "Urban/suburban hidden-septic signal"
    if density_rank <= 12 and septic_bg_pct >= 45:
        return "High density and strong local septic signal"
    if count_rank <= 10 and density_rank <= 15:
        return "High total and high density signal"
    if count_rank <= 10:
        return "High total exposure signal"
    if density_rank <= 12:
        return "High density signal"
    if septic_bg_pct >= 45:
        return "Strong rural or county-level signal"
    if septic_bg_pct >= 25:
        return "Moderate localized signal"
    return "Lower statewide signal, still property-specific"


def confidence_note(row: dict[str, str]) -> str:
    missing_pct = as_float(row["missing_parcel_bg_pct"])
    abbr = row["state_abbr"]

    if missing_pct >= 8:
        return "Use extra caution: parcel-data gaps may undercount septic systems in parts of this state."
    if missing_pct >= 3:
        return "Moderate confidence: some parcel-data gaps may affect local estimates."
    if abbr in {"AK", "HI"}:
        return "Not summarized in this conterminous-U.S. dataset."
    return "Good planning signal, but property records are still needed for an address-level answer."


def urban_caution(row: dict[str, str]) -> str:
    abbr = row["state_abbr"]
    name = row["state_name"]

    if abbr in URBAN_SURPRISE_STATES:
        return (
            f"{name} has developed-looking areas where septic can still be overlooked, especially older suburbs, "
            "coastal or lake communities, large-lot neighborhoods, and sewer-edge streets."
        )
    if abbr in HIGH_TOTAL_STATES:
        return (
            f"{name} has enough modeled septic exposure that city edges, fast-growing suburbs, and older subdivisions "
            "should still be checked before digging."
        )
    if abbr in RURAL_HISTORY_STATES:
        return (
            f"{name} has a strong rural or historical septic signal, but the same records-first logic also applies "
            "near town edges and partially sewered communities."
        )
    return (
        f"In {name}, a lower statewide signal does not rule out septic on a specific property, especially outside "
        "confirmed municipal sewer service."
    )


def best_next_step(row: dict[str, str]) -> str:
    label = exposure_label(row)
    missing_pct = as_float(row["missing_parcel_bg_pct"])

    if "Urban/suburban" in label:
        return (
            "Confirm the home has a municipal sewer account or connection record, then check local records before "
            "digging. Call 811, but do not assume 811 marks private septic components."
        )
    if missing_pct >= 8:
        return (
            "Start with local health department or county records because the modeled data may undercount some areas. "
            "Use septic-specific locating if records do not show the tank, lines, or field."
        )
    if "High" in label or "Strong" in label:
        return (
            "Treat septic location as a real planning issue before posts, trenches, grading, pools, sheds, additions, "
            "or landscaping. Check records, call 811, and locate private septic components when layout is unclear."
        )
    return (
        "Do not rely on the state average. Verify the property through sewer billing, local records, disclosures, "
        "811, and septic-specific locating when the work area is uncertain."
    )


def visible_metrics(row: dict[str, str]) -> dict[str, object]:
    return {
        "estimated_septic_count_medium": as_int(row["ms_septic_count"]),
        "count_rank": as_int(row["rank_ms_count"]),
        "density_rank": as_int(row["rank_ms_density"]),
        "modeled_density_per_sqkm": round(as_float(row["ms_density_per_sqkm_statewide"]), 2),
        "predicted_septic_block_group_pct": round(as_float(row["med_predicted_septic_bg_pct"]), 1),
        "parcel_gap_pct": round(as_float(row["missing_parcel_bg_pct"]), 1),
    }


def main() -> int:
    records = []
    with SOURCE.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            record = {
                "state": row["state_name"],
                "abbr": row["state_abbr"],
                "modern_signal": exposure_label(row),
                "confidence_note": confidence_note(row),
                "urban_suburban_caution": urban_caution(row),
                "best_next_step": best_next_step(row),
                "metrics": visible_metrics(row),
            }
            records.append(record)

    records = sorted(records, key=lambda item: item["state"])

    with OUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "source": "Derived from docs/usgs-septic-density-analysis/state-summary.csv",
                "use": "Homeowner-facing V2 labels, not official USGS rankings.",
                "states": records,
            },
            f,
            indent=2,
        )

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "state",
            "abbr",
            "modern_signal",
            "estimated_septic_count_medium",
            "count_rank",
            "density_rank",
            "modeled_density_per_sqkm",
            "predicted_septic_block_group_pct",
            "parcel_gap_pct",
            "confidence_note",
            "urban_suburban_caution",
            "best_next_step",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    "state": record["state"],
                    "abbr": record["abbr"],
                    "modern_signal": record["modern_signal"],
                    **record["metrics"],
                    "confidence_note": record["confidence_note"],
                    "urban_suburban_caution": record["urban_suburban_caution"],
                    "best_next_step": record["best_next_step"],
                }
            )

    print(f"Wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"Wrote {OUT_CSV.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
