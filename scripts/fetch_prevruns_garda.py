"""Fetch previous_day1 (yesterday's run for today) hourly data, 4 Garda points, 2024-01-01..2026-07-03."""

import argparse
import time
from datetime import date
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "prevruns"

BASE_VARS = "pressure_msl,temperature_2m"
TOR_VARS = (
    "pressure_msl,cloud_cover,shortwave_radiation,temperature_2m,"
    "precipitation,relative_humidity_2m,wind_speed_100m,wind_direction_100m"
)
POINTS = {
    "torbole": (45.87, 10.877, TOR_VARS),
    "verona": (45.44, 10.99, BASE_VARS),
    "bolzano": (46.50, 11.35, BASE_VARS),
    "innsbruck": (47.27, 11.39, BASE_VARS),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-date", default="2024-01-01", type=date.fromisoformat)
    parser.add_argument("--end-date", default=date.today(), type=date.fromisoformat)
    parser.add_argument("--replace", action="store_true", help="Replace existing downloads.")
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    with httpx.Client(timeout=300) as client:
        for name, (lat, lon, hourly) in POINTS.items():
            dest = OUT / f"{name}.json"
            if not args.replace and dest.exists() and dest.stat().st_size > 10000:
                print(f"skip {name}")
                continue
            hourly_previous_day1 = ",".join(f"{variable}_previous_day1" for variable in hourly.split(","))
            response = client.get(
                "https://previous-runs-api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "hourly": hourly_previous_day1,
                    "start_date": args.start_date.isoformat(),
                    "end_date": args.end_date.isoformat(),
                    "timezone": "Europe/Berlin",
                },
            )
            response.raise_for_status()
            dest.write_bytes(response.content)
            print(f"ok {name}: {dest.stat().st_size / 1e6:.1f} MB")
            time.sleep(15)
    print("done")


if __name__ == "__main__":
    main()
