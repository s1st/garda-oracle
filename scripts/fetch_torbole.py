"""Pull the full T0193 Torbole wind history (2012-07-04 .. today) from
storico.meteotrentino.it (Hydstra/WEB), one variable x one calendar year
per request, politely throttled.

Output: data/torbole/raw/<var>_<year>.csv
"""

import re
import sys
import time
import zipfile
import io
import argparse
from datetime import date
from pathlib import Path
from urllib.parse import quote

import httpx

BASE = "http://storico.meteotrentino.it"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "torbole" / "raw"
OUT.mkdir(parents=True, exist_ok=True)

UA = "garda-oracle/0.1 (+https://garda.simon-stieber.de/)"
COOKIES = {"username": "webuser", "userid": "980499266", "userclass": "anon", "is_admin": "0"}

VARS = {
    "515.00": "Veloc. vento media (metri/secondo)",
    "500.00": "Direzione vento media (gradi)",
}
FIRST = date(2012, 7, 4)

REDIRECT_RE = re.compile(r"location\.href=\\?'(?P<url>http[^']+\.zip[^']*)'")


def fetch_year(client: httpx.Client, var: str, vn: str, d1: str, d2: str) -> bytes:
    params = (
        f"co=t0193&v={var}_{var}&vn={quote(vn)}"
        f"&p=Altro,1,1,custom,1&o=Download,download"
        f"&i={quote('Tutte le misure')},Point,1&cat=rs&d1={d1}&d2={d2}"
    )
    r = client.get(f"{BASE}/cgi/webhyd.pl?{params}", timeout=180)
    r.raise_for_status()
    m = REDIRECT_RE.search(r.text)
    if not m:
        raise RuntimeError(f"no zip redirect in response ({r.text[:200]!r})")
    z = client.get(m.group("url"), timeout=180)
    z.raise_for_status()
    return z.content


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--end-date",
        default=date.today(),
        type=date.fromisoformat,
        help="Last observation date (YYYY-MM-DD).",
    )
    args = parser.parse_args()
    end_date = args.end_date
    if end_date < FIRST:
        raise ValueError(f"--end-date must be on or after {FIRST}")

    with httpx.Client(headers={"User-Agent": UA}, cookies=COOKIES) as client:
        for var, vn in VARS.items():
            for year in range(FIRST.year, end_date.year + 1):
                dest = OUT / f"{var.split('.')[0]}_{year}.csv"
                if dest.exists() and dest.stat().st_size > 1000 and year != end_date.year:
                    print(f"skip {dest.name} (exists)")
                    continue
                d1 = f"01/01/{year}" if year > FIRST.year else FIRST.strftime("%d/%m/%Y")
                d2 = f"31/12/{year}" if year < end_date.year else end_date.strftime("%d/%m/%Y")
                for attempt in (1, 2, 3):
                    try:
                        blob = fetch_year(client, var, vn, d1, d2)
                        with zipfile.ZipFile(io.BytesIO(blob)) as zf:
                            name = zf.namelist()[0]
                            dest.write_bytes(zf.read(name))
                        print(f"ok   {dest.name}  {dest.stat().st_size / 1e6:.2f} MB")
                        break
                    except Exception as exc:  # noqa: BLE001
                        print(f"fail {dest.name} attempt {attempt}: {exc}", file=sys.stderr)
                        time.sleep(20 * attempt)
                else:
                    print(f"GIVE UP {dest.name}", file=sys.stderr)
                time.sleep(8)  # politeness between year requests
    print("done")


if __name__ == "__main__":
    main()
