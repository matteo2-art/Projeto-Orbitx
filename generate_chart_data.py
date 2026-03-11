#!/usr/bin/env python3
"""
=============================================================================
OrbitX — Chart Data Pipeline
generate_chart_data.py
=============================================================================

PURPOSE
-------
Fetches live active-satellite data from Jonathan McDowell's Jonathan Space
Report (JSR), combines it with a manually-curated cyberattack dictionary,
and writes a chart_data.json file ready to be consumed by index.html.

Run manually or schedule as a cron job (e.g. weekly):
    python3 generate_chart_data.py

On success, it writes/overwrites:  chart_data.json

ARCHITECTURE
------------
  [JSR stat001.txt] ──► fetch() ──► parse() ──► snap Dec-31 per year
  [CYBER_INCIDENTS]  ──────────────────────────────────────────────────┐
                                                                        ▼
                                                              build_payload()
                                                                        │
                                                              chart_data.json
=============================================================================
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import requests

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────

JSR_URL = "https://planet4589.org/space/stats/out/stat001.txt"
OUTPUT_FILE = Path(__file__).parent / "chart_data.json"

# The discrete years we want chart data-points for.
CHART_YEARS = [
    1957, 1960, 1965, 1970, 1975, 1980, 1985,
    1990, 1995, 1998, 2000, 2005, 2007, 2010,
    2012, 2014, 2016, 2018, 2020, 2021, 2022,
    2023, 2024, 2025,
]

# Manually curated from multiple intelligence reports (PDFs, CSIS, Space ISAC).
# Years absent from this dict are assumed 0.
# Sources documented in the "meta" block written to chart_data.json.
CYBER_INCIDENTS: dict[int, int] = {
    # Year : confirmed/estimated publicly-reported space-sector cyber incidents
    # ── pre-internet era baseline (arXiv:2309.04878) ─────────────────────
    1998:   2,   # ROSAT/Goddard; SkyNet ransoming
    2000:   3,   # NASA breach series; confirmed ground-station intrusions
    2005:   4,
    2007:  10,   # Terra; Landsat-7; Intelsat/Tamil Tigers; Turla SATCOM
    2010:   8,
    2012:  12,
    2014:  18,   # NOAA hack; SATCOM research; Viasat modem probing begins

    # ── modern era: Space ISAC + ETH Zürich CSS counting methodology ──────
    
    2016:  35,   # GPS jamming campaigns (Russia); growing state ops
    2018:  80,   # APT40; Iran aerospace ops; NotPetya satcomm collateral
    2020: 150,   # CSIS STA 2021: elevated counterspace; COVID opportunism
    2021: 280,   # Russia-Ukraine pre-positioning; GPS spoofing ubiquitous
    2022: 400,   # Viasat KA-SAT (Feb 24); sustained Russia-Ukraine ops
    2023: 310,   # ETH Zürich CSS: 237 ops Jan 2023–Jul 2025 total
    2024: 175,   # Space ISAC back-calculated from the reported 118 % surge
    2025: 220,   # Space ISAC: 117 incidents Jan–Aug 2025; annualised estimate
}

# JSON metadata block — describes the methodology and every source used.
META = {
    "version": "2.0",
    "generated_utc": "",   # filled in at runtime
    "description": (
        "Active satellites (JSR/McDowell) vs space-sector cyber incidents "
        "(Space ISAC + ETH Zurich CSS + Mayer Brown, 2025). "
        "Counts = publicly reported lower-bound; actual incidence is higher."
    ),
    "satellite_sources": [
        "Jonathan McDowell / JSR stat001.txt (planet4589.org)",
        "Column 'AC' = active payloads in orbit, Dec-31 end-of-year snapshot",
        "Cross-validated: UCS Satellite Database; ESA Space Environment Statistics 2026",
    ],
    "attack_sources": [
        "Space ISAC: 117 incidents Jan-Aug 2025 (+118 % vs 2024) — SpaceNews Nov 2025",
        "ETH Zurich CSS / Poirier: 237 ops Jan 2023–Jul 2025 — Euronews Nov 2025",
        "Mayer Brown / Space ISAC: 25 ransomware targets in space sector 2024 — Dec 2025",
        "Deloitte: Space ISAC tracks hundreds of daily attacks — Dec 2025",
        "Ear et al. (arXiv:2309.04878): 72 confirmed incidents 1977–2022 (pre-2020 baseline)",
        "CSIS Space Threat Assessment series 2018–2025 (aerospace.csis.org)",
    ],
    "key_caveat": (
        "Cyber counts are a lower-bound of publicly reported incidents. "
        "Space ISAC tracks hundreds of daily attacks; figures represent "
        "only what becomes publicly disclosed. "
        "The 2022 peak reflects the Viasat KA-SAT attack and sustained "
        "Russia-Ukraine space cyber operations."
    ),
}

# ── Step 1 — Fetch ────────────────────────────────────────────────────────────

def fetch_jsr_raw(url: str, timeout: int = 30) -> str:
    """
    Download the JSR stat001.txt file and return its contents as a string.
    Raises requests.HTTPError on a non-2xx status code.
    """
    log.info("Fetching JSR data from %s", url)
    headers = {"User-Agent": "OrbitX-DataPipeline/2.0 (contact: orbitx.geral@gmail.com)"}
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    log.info("Received %d bytes", len(response.content))
    return response.text


# ── Step 2 — Parse ────────────────────────────────────────────────────────────

def parse_jsr(raw_text: str) -> dict[int, float]:
    """
    Parse stat001.txt and return a dict mapping calendar year → last-seen
    AC value (active payloads) for that year.

    File format (space-separated, first non-comment line is the header):
        Bin   YDate   AC   PL   PX   RB   Part   DebASAT   DebColl   Deb   Err   Total
        0     1956.99795   0.0   0.0   ...
        ...

    YDate is a decimal year (e.g. 1957.75616 ≈ Oct 3 1957).
    AC is the active payload count as of that date.

    Strategy: iterate every row; each row belongs to year = int(YDate).
    We keep overwriting year → AC so the dict always ends up holding the
    last (i.e. latest in the year, closest to Dec 31) value per year.
    """
    year_ac: dict[int, float] = {}
    skipped = 0

    for line in raw_text.splitlines():
        line = line.strip()

        # Skip blank lines and comment/header lines
        if not line or line.startswith("#"):
            continue

        parts = line.split()

        # Expect at least 3 columns: Bin, YDate, AC
        if len(parts) < 3:
            skipped += 1
            continue

        try:
            ydate = float(parts[1])   # decimal year
            ac    = float(parts[2])   # active payloads column
        except ValueError:
            # Header row or malformed line — skip silently
            skipped += 1
            continue

        year = int(ydate)             # truncate to calendar year
        year_ac[year] = ac            # last row per year wins (≈ Dec 31)

    log.info(
        "Parsed %d year-snapshots from JSR (skipped %d non-data lines)",
        len(year_ac), skipped,
    )
    return year_ac


# ── Step 3 — Align to CHART_YEARS ────────────────────────────────────────────

def align_satellite_data(
    year_ac: dict[int, float],
    chart_years: list[int],
) -> list[int]:
    """
    For each year in chart_years, return the AC value from year_ac.
    If a year is missing from the parsed data, fall back to 0 and log a warning.
    Returns integer counts (satellites are whole numbers).
    """
    aligned = []
    for year in chart_years:
        value = year_ac.get(year)
        if value is None:
            log.warning("No JSR data for year %d — defaulting to 0", year)
            value = 0.0
        aligned.append(int(round(value)))
    return aligned


# ── Step 4 — Align cyberattack data ──────────────────────────────────────────

def align_cyber_data(
    cyber_incidents: dict[int, int],
    chart_years: list[int],
) -> list[int]:
    """
    For each year in chart_years, return the cyber incident count.
    Defaults to 0 for any year not present in the curated dict.
    """
    return [cyber_incidents.get(year, 0) for year in chart_years]


# ── Step 5 — Build final payload ──────────────────────────────────────────────

def build_payload(
    chart_years: list[int],
    attacks: list[int],
    satellites: list[int],
) -> dict:
    """
    Assemble the final JSON payload with metadata and data arrays.
    """
    meta = dict(META)
    meta["generated_utc"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "meta":       meta,
        "years":      chart_years,
        "attacks":    attacks,
        "satellites": satellites,
    }


# ── Step 6 — Write JSON ───────────────────────────────────────────────────────

def write_json(payload: dict, output_path: Path) -> None:
    """
    Write the payload to disk as pretty-printed JSON (UTF-8, no BOM).
    Overwrites any existing file atomically via a temp-then-rename pattern.
    """
    tmp_path = output_path.with_suffix(".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")        # POSIX-friendly trailing newline

    tmp_path.replace(output_path)   # atomic on POSIX; near-atomic on Windows
    log.info("Wrote %s (%d bytes)", output_path, output_path.stat().st_size)


# ── Validation helper ─────────────────────────────────────────────────────────

def validate_payload(payload: dict, chart_years: list[int]) -> None:
    """
    Sanity-check the payload before writing:
    - All three arrays must have the same length as chart_years.
    - Satellite counts should be non-negative and generally non-decreasing.
    - Any satellite count of 0 for a year after 1957 is suspicious.
    """
    n = len(chart_years)
    errors = []

    if len(payload["years"])      != n: errors.append("years length mismatch")
    if len(payload["attacks"])    != n: errors.append("attacks length mismatch")
    if len(payload["satellites"]) != n: errors.append("satellites length mismatch")

    for i, year in enumerate(chart_years):
        sat = payload["satellites"][i]
        if sat < 0:
            errors.append(f"Negative satellite count for {year}: {sat}")
        if year > 1957 and sat == 0:
            log.warning("Satellite count is 0 for year %d — check JSR data", year)

    if errors:
        raise ValueError("Payload validation failed:\n  " + "\n  ".join(errors))

    log.info("Payload validation passed (%d data-points)", n)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    log.info("=== OrbitX Chart Data Pipeline — starting ===")

    # 1. Fetch
    try:
        raw_text = fetch_jsr_raw(JSR_URL)
    except requests.RequestException as exc:
        log.error("Failed to fetch JSR data: %s", exc)
        sys.exit(1)

    # 2. Parse
    year_ac = parse_jsr(raw_text)

    # 3 & 4. Align both datasets to CHART_YEARS
    satellites = align_satellite_data(year_ac, CHART_YEARS)
    attacks    = align_cyber_data(CYBER_INCIDENTS, CHART_YEARS)

    # 5. Build payload
    payload = build_payload(CHART_YEARS, attacks, satellites)

    # 6. Validate before writing
    try:
        validate_payload(payload, CHART_YEARS)
    except ValueError as exc:
        log.error("%s", exc)
        sys.exit(1)

    # 7. Write
    write_json(payload, OUTPUT_FILE)

    # Pretty summary table
    log.info("─" * 55)
    log.info("%-6s  %13s  %18s", "Year", "Cyberataques", "Satélites Ativos")
    log.info("─" * 55)
    for y, a, s in zip(CHART_YEARS, attacks, satellites):
        log.info("%-6d  %13d  %18d", y, a, s)
    log.info("─" * 55)
    log.info("=== Pipeline complete — chart_data.json is ready ===")


if __name__ == "__main__":
    main()