"""Build per-day Ora/Peler labels from the T0193 Torbole 10-min curves."""

import argparse
import csv
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "torbole" / "raw"
OUT = ROOT / "data" / "labels.csv"
KT = 1.94384


def load(var: str) -> dict:
    out = {}
    for f in sorted(RAW.glob(f"{var}_*.csv")):
        with f.open(encoding="latin-1") as fh:
            for row in csv.reader(fh):
                if len(row) < 3:
                    continue
                try:
                    ts = datetime.strptime(row[0].strip(), "%H:%M:%S %d/%m/%Y")
                except ValueError:
                    continue
                try:
                    out[ts] = float(row[1])
                except ValueError:
                    continue
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--end-date",
        type=date.fromisoformat,
        help="Last label date (YYYY-MM-DD); defaults to all downloaded observations.",
    )
    args = parser.parse_args()

    speed, dirn = load("515"), load("500")
    days = defaultdict(list)
    for ts, value in speed.items():
        direction = dirn.get(ts)
        if direction is not None:
            days[ts.date()].append((ts, value * KT, direction))

    rows = []
    for day in sorted(days):
        if args.end_date and day > args.end_date:
            continue
        samples = days[day]
        if not (4 <= day.month <= 10) or len(samples) < 100:
            continue
        peler_w = [v for ts, v, d in samples if 4 <= ts.hour < 9 and 10 <= d <= 120]
        ora_w = [v for ts, v, d in samples if 12 <= ts.hour < 17 and 150 <= d <= 240]
        peler_mean = sum(peler_w) / len(peler_w) if len(peler_w) >= 12 else 0.0
        ora_mean = sum(ora_w) / len(ora_w) if len(ora_w) >= 15 else 0.0
        rows.append(
            {
                "date": day.isoformat(),
                "peler": int(peler_mean >= 8),
                "ora": int(ora_mean >= 8),
                "peler_mean_kt": round(peler_mean, 2),
                "ora_mean_kt": round(ora_mean, 2),
                "n_samples": len(samples),
            }
        )

    if not rows:
        raise RuntimeError(f"no usable observations found under {RAW}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    n = len(rows)
    print(f"{n} season days -> {OUT}")
    print(
        f"ora rate {sum(r['ora'] for r in rows) / n:.0%} | peler rate {sum(r['peler'] for r in rows) / n:.0%}"
    )


if __name__ == "__main__":
    main()
