#!/usr/bin/env python3
"""Create controlled state-level summaries from the USGS septic-density CSVs."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import median


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "datausgsseptic-density"
OUT_DIR = ROOT / "docs" / "usgs-septic-density-analysis"

DENSITY_FILE = DATA_DIR / "BG2021_SepticDensities.csv"
SEWER_FILE = DATA_DIR / "BG2021_SewerEstimates.csv"
MISSING_FILE = DATA_DIR / "BG2021_PotMissing_Parcels.csv"

STATE_FIPS = {
    "01": ("AL", "Alabama"),
    "04": ("AZ", "Arizona"),
    "05": ("AR", "Arkansas"),
    "06": ("CA", "California"),
    "08": ("CO", "Colorado"),
    "09": ("CT", "Connecticut"),
    "10": ("DE", "Delaware"),
    "11": ("DC", "District of Columbia"),
    "12": ("FL", "Florida"),
    "13": ("GA", "Georgia"),
    "16": ("ID", "Idaho"),
    "17": ("IL", "Illinois"),
    "18": ("IN", "Indiana"),
    "19": ("IA", "Iowa"),
    "20": ("KS", "Kansas"),
    "21": ("KY", "Kentucky"),
    "22": ("LA", "Louisiana"),
    "23": ("ME", "Maine"),
    "24": ("MD", "Maryland"),
    "25": ("MA", "Massachusetts"),
    "26": ("MI", "Michigan"),
    "27": ("MN", "Minnesota"),
    "28": ("MS", "Mississippi"),
    "29": ("MO", "Missouri"),
    "30": ("MT", "Montana"),
    "31": ("NE", "Nebraska"),
    "32": ("NV", "Nevada"),
    "33": ("NH", "New Hampshire"),
    "34": ("NJ", "New Jersey"),
    "35": ("NM", "New Mexico"),
    "36": ("NY", "New York"),
    "37": ("NC", "North Carolina"),
    "38": ("ND", "North Dakota"),
    "39": ("OH", "Ohio"),
    "40": ("OK", "Oklahoma"),
    "41": ("OR", "Oregon"),
    "42": ("PA", "Pennsylvania"),
    "44": ("RI", "Rhode Island"),
    "45": ("SC", "South Carolina"),
    "46": ("SD", "South Dakota"),
    "47": ("TN", "Tennessee"),
    "48": ("TX", "Texas"),
    "49": ("UT", "Utah"),
    "50": ("VT", "Vermont"),
    "51": ("VA", "Virginia"),
    "53": ("WA", "Washington"),
    "54": ("WV", "West Virginia"),
    "55": ("WI", "Wisconsin"),
    "56": ("WY", "Wyoming"),
}


def clean_geoid(value: str) -> str:
    return value.strip().strip('"').lstrip("'")


def as_int(value: str) -> int:
    if value == "":
        return 0
    return int(float(value))


def as_float(value: str) -> float:
    if value == "":
        return 0.0
    return float(value)


def pct(part: float, whole: float) -> float:
    if whole == 0:
        return 0.0
    return round((part / whole) * 100, 2)


def load_sewer_flags() -> dict[str, dict[str, str]]:
    flags: dict[str, dict[str, str]] = {}
    with SEWER_FILE.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            geoid = clean_geoid(row["GEOID"])
            flags[geoid] = {
                "HighSewer": row["HighSewer"],
                "MedSewer": row["MedSewer"],
                "LowSewer": row["LowSewer"],
            }
    return flags


def load_missing_geoids() -> set[str]:
    missing: set[str] = set()
    with MISSING_FILE.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            missing.add(clean_geoid(row["GEOID"]))
    return missing


def classify_signal(row: dict[str, object]) -> str:
    density_rank = int(row["rank_ms_density"])
    count_rank = int(row["rank_ms_count"])
    septic_bg_pct = float(row["med_predicted_septic_bg_pct"])
    missing_pct = float(row["missing_parcel_bg_pct"])

    if density_rank <= 10 and septic_bg_pct >= 35:
        return "Very high modern density signal"
    if density_rank <= 15 or count_rank <= 10 or septic_bg_pct >= 45:
        return "High modern or localized signal"
    if missing_pct >= 8:
        return "Useful signal, but parcel gaps need caution"
    if septic_bg_pct >= 25:
        return "Moderate property-specific signal"
    return "Lower statewide signal, still property-specific"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    sewer_flags = load_sewer_flags()
    missing_geoids = load_missing_geoids()
    states = defaultdict(
        lambda: {
            "bg_count": 0,
            "area_sqkm": 0.0,
            "hs_count": 0,
            "ms_count": 0,
            "ls_count": 0,
            "positive_ms_bg": 0,
            "high_density_ms_bg": 0,
            "missing_bg": 0,
            "med_predicted_septic_bg": 0,
            "med_predicted_sewer_bg": 0,
            "ms_density_values": [],
        }
    )

    density_rows = 0
    unknown_fips = defaultdict(int)

    with DENSITY_FILE.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            density_rows += 1
            geoid = clean_geoid(row["GEOID"])
            fips = geoid[:2]
            if fips not in STATE_FIPS:
                unknown_fips[fips] += 1
                continue

            state = states[fips]
            ms_count = as_int(row["MS_SepCnt"])
            ms_density = as_float(row["MS_SepDn"])
            area = as_float(row["AREA_SQKM"])

            state["bg_count"] += 1
            state["area_sqkm"] += area
            state["hs_count"] += as_int(row["HS_SepCnt"])
            state["ms_count"] += ms_count
            state["ls_count"] += as_int(row["LS_SepCnt"])
            state["ms_density_values"].append(ms_density)

            if ms_count > 0:
                state["positive_ms_bg"] += 1
            if ms_density >= 25:
                state["high_density_ms_bg"] += 1
            if geoid in missing_geoids:
                state["missing_bg"] += 1

            flags = sewer_flags.get(geoid)
            if flags:
                if flags["MedSewer"] == "NO":
                    state["med_predicted_septic_bg"] += 1
                elif flags["MedSewer"] == "YES":
                    state["med_predicted_sewer_bg"] += 1

    rows = []
    for fips, values in states.items():
        abbr, name = STATE_FIPS[fips]
        bg_count = values["bg_count"]
        area_sqkm = values["area_sqkm"]
        ms_count = values["ms_count"]
        density_values = values["ms_density_values"]
        positive_density_values = [v for v in density_values if v > 0]

        rows.append(
            {
                "state_fips": fips,
                "state_abbr": abbr,
                "state_name": name,
                "block_groups": bg_count,
                "area_sqkm": round(area_sqkm, 3),
                "hs_septic_count": values["hs_count"],
                "ms_septic_count": ms_count,
                "ls_septic_count": values["ls_count"],
                "ms_density_per_sqkm_statewide": round(ms_count / area_sqkm, 3) if area_sqkm else 0.0,
                "ms_median_bg_density": round(median(density_values), 3) if density_values else 0.0,
                "ms_median_positive_bg_density": round(median(positive_density_values), 3)
                if positive_density_values
                else 0.0,
                "positive_ms_bg_pct": pct(values["positive_ms_bg"], bg_count),
                "high_density_ms_bg_pct": pct(values["high_density_ms_bg"], bg_count),
                "med_predicted_septic_bg_pct": pct(values["med_predicted_septic_bg"], bg_count),
                "missing_parcel_bg_pct": pct(values["missing_bg"], bg_count),
            }
        )

    by_density = sorted(rows, key=lambda r: r["ms_density_per_sqkm_statewide"], reverse=True)
    by_count = sorted(rows, key=lambda r: r["ms_septic_count"], reverse=True)

    for idx, row in enumerate(by_density, start=1):
        row["rank_ms_density"] = idx
    density_rank_by_state = {row["state_fips"]: row["rank_ms_density"] for row in by_density}

    for idx, row in enumerate(by_count, start=1):
        row["rank_ms_count"] = idx
    count_rank_by_state = {row["state_fips"]: row["rank_ms_count"] for row in by_count}

    for row in rows:
        row["rank_ms_density"] = density_rank_by_state[row["state_fips"]]
        row["rank_ms_count"] = count_rank_by_state[row["state_fips"]]
        row["homeowner_signal"] = classify_signal(row)

    fieldnames = [
        "state_fips",
        "state_abbr",
        "state_name",
        "block_groups",
        "area_sqkm",
        "hs_septic_count",
        "ms_septic_count",
        "ls_septic_count",
        "rank_ms_count",
        "ms_density_per_sqkm_statewide",
        "rank_ms_density",
        "ms_median_bg_density",
        "ms_median_positive_bg_density",
        "positive_ms_bg_pct",
        "high_density_ms_bg_pct",
        "med_predicted_septic_bg_pct",
        "missing_parcel_bg_pct",
        "homeowner_signal",
    ]

    csv_path = OUT_DIR / "state-summary.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda r: r["state_name"]))

    summary = {
        "source_files": {
            "densities": str(DENSITY_FILE.relative_to(ROOT)),
            "sewer_estimates": str(SEWER_FILE.relative_to(ROOT)),
            "missing_parcels": str(MISSING_FILE.relative_to(ROOT)),
        },
        "density_rows": density_rows,
        "sewer_rows": len(sewer_flags),
        "missing_parcel_rows": len(missing_geoids),
        "state_count": len(rows),
        "unknown_fips": dict(sorted(unknown_fips.items())),
        "top_by_medium_septic_count": by_count[:15],
        "top_by_medium_statewide_density": by_density[:15],
        "notes": [
            "Statewide density is calculated as total medium-estimate septic count divided by total block-group area in square kilometers.",
            "This is a modeled state-level rollup for editorial interpretation, not an official USGS state ranking.",
            "High density block groups are defined here as MS_SepDn >= 25 septic tanks per square kilometer for screening only.",
        ],
    }

    json_path = OUT_DIR / "audit-summary.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    md_path = OUT_DIR / "batch-1-findings.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Batch 1 Findings: USGS Septic Density Rollup\n\n")
        f.write("## Files Audited\n\n")
        f.write(f"- `{DENSITY_FILE.relative_to(ROOT)}`\n")
        f.write(f"- `{SEWER_FILE.relative_to(ROOT)}`\n")
        f.write(f"- `{MISSING_FILE.relative_to(ROOT)}`\n\n")
        f.write("## Row Counts\n\n")
        f.write(f"- Density rows: {density_rows:,}\n")
        f.write(f"- Sewer estimate rows: {len(sewer_flags):,}\n")
        f.write(f"- Potential missing parcel rows: {len(missing_geoids):,}\n")
        f.write(f"- States or districts summarized: {len(rows)}\n\n")
        f.write("## Top 10 By Medium-Estimate Septic Count\n\n")
        for row in by_count[:10]:
            f.write(
                f"- {row['state_name']}: {row['ms_septic_count']:,} estimated septic tanks; "
                f"{row['med_predicted_septic_bg_pct']}% medium-predicted septic block groups\n"
            )
        f.write("\n## Top 10 By Statewide Medium-Estimate Density\n\n")
        for row in by_density[:10]:
            f.write(
                f"- {row['state_name']}: {row['ms_density_per_sqkm_statewide']} estimated septic tanks/sq km; "
                f"{row['high_density_ms_bg_pct']}% high-density block groups\n"
            )
        f.write("\n## Interpretation Guardrails\n\n")
        f.write("- Use this as a modern modeled density signal, not exact current septic usage by state.\n")
        f.write("- Do not present this as an official USGS ranking.\n")
        f.write("- Convert the numbers into homeowner questions: records, 811 limits, digging risk, and when septic-specific locating matters.\n")

    print(f"Wrote {csv_path.relative_to(ROOT)}")
    print(f"Wrote {json_path.relative_to(ROOT)}")
    print(f"Wrote {md_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
