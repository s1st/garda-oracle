"""Live 30-day Verlauf: day-1 hindcast vs. observed Ora/Peler days.

Observed side: the Meteotrentino storico (Hydstra) export for T0193 —
one GET per variable (speed 515.00, direction 500.00), zip -> CSV,
labelled with the same sectors/thresholds as the training labels.

Hindcast side: the Open-Meteo previous-runs archive (``previous_day1`` =
what yesterday's model run said about each day), scored through the same
frozen model the live page uses. So the strip shows what the dashboard
WOULD have displayed the evening before, against what actually happened.

Both fetches are slow-ish (seconds) and cached by the caller for hours.
"""
from __future__ import annotations

import csv
import io
import re
import zipfile
from datetime import date, datetime, timedelta
from urllib.parse import quote

import httpx

from .features import POINTS, PointSeries, build_day_features
from .model import classify

KT = 1.94384
_HYDSTRA_BASE = "http://storico.meteotrentino.it/cgi/webhyd.pl"
_REDIRECT_RE = re.compile(r"location\.href=\\?'(?P<url>http[^']+\.zip[^']*)'")
_HY_COOKIES = {"username": "webuser", "userid": "980499266", "userclass": "anon", "is_admin": "0"}
_HY_VARS = {
    "515.00": "Veloc. vento media (metri/secondo)",
    "500.00": "Direzione vento media (gradi)",
}

# label definition — keep identical to scripts/garda/build_labels.py
PELER_HOURS = (4, 9)
PELER_SECTOR = (10, 120)
ORA_HOURS = (12, 17)
ORA_SECTOR = (150, 240)
FIRE_KT = 8.0


async def _fetch_hydstra_var(client: httpx.AsyncClient, var: str, d1: date, d2: date) -> dict[datetime, float]:
    params = (
        f"co=t0193&v={var}_{var}&vn={quote(_HY_VARS[var])}"
        f"&p=Altro,1,1,custom,1&o=Download,download"
        f"&i={quote('Tutte le misure')},Point,1&cat=rs"
        f"&d1={d1:%d/%m/%Y}&d2={d2:%d/%m/%Y}"
    )
    r = await client.get(f"{_HYDSTRA_BASE}?{params}", cookies=_HY_COOKIES, timeout=120)
    r.raise_for_status()
    m = _REDIRECT_RE.search(r.text)
    if not m:
        raise RuntimeError("no zip redirect from storico export")
    z = await client.get(m.group("url"), timeout=120)
    z.raise_for_status()
    out: dict[datetime, float] = {}
    with zipfile.ZipFile(io.BytesIO(z.content)) as zf:
        text = zf.read(zf.namelist()[0]).decode("latin-1")
    for row in csv.reader(io.StringIO(text)):
        if len(row) < 2:
            continue
        try:
            ts = datetime.strptime(row[0].strip(), "%H:%M:%S %d/%m/%Y")
            out[ts] = float(row[1])
        except ValueError:
            continue
    return out


def label_day(samples: list[tuple[datetime, float, float]]) -> dict:
    """Observed Ora/Peler flags for one day's (ts, kt, deg) samples."""
    if len(samples) < 100:
        return {"ora": None, "peler": None}
    peler_w = [v for ts, v, d in samples
               if PELER_HOURS[0] <= ts.hour < PELER_HOURS[1] and PELER_SECTOR[0] <= d <= PELER_SECTOR[1]]
    ora_w = [v for ts, v, d in samples
             if ORA_HOURS[0] <= ts.hour < ORA_HOURS[1] and ORA_SECTOR[0] <= d <= ORA_SECTOR[1]]
    peler = int(len(peler_w) >= 12 and sum(peler_w) / len(peler_w) >= FIRE_KT)
    ora = int(len(ora_w) >= 15 and sum(ora_w) / len(ora_w) >= FIRE_KT)
    return {"ora": ora, "peler": peler}


async def observed_labels(days: int = 30) -> dict[date, dict]:
    """Observed labels for the last `days` full days (yesterday backwards)."""
    end = date.today()
    start = end - timedelta(days=days)
    async with httpx.AsyncClient() as client:
        speed = await _fetch_hydstra_var(client, "515.00", start, end)
        dirn = await _fetch_hydstra_var(client, "500.00", start, end)
    bydate: dict[date, list[tuple[datetime, float, float]]] = {}
    for ts, v in speed.items():
        d = dirn.get(ts)
        if d is not None:
            bydate.setdefault(ts.date(), []).append((ts, v * KT, d))
    return {day: label_day(sorted(ss)) for day, ss in bydate.items()}


async def hindcast_verdicts(days: int = 30) -> dict[date, dict]:
    """Day-1 hindcast: score each past day from yesterday's-run features."""
    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=days)
    points: dict[str, PointSeries] = {}
    async with httpx.AsyncClient(timeout=120) as client:
        for name, (lat, lon, hourly) in POINTS.items():
            hv = ",".join(f"{v}_previous_day1" for v in hourly.split(","))
            r = await client.get(
                "https://previous-runs-api.open-meteo.com/v1/forecast",
                params={"latitude": lat, "longitude": lon, "hourly": hv,
                        # one day earlier for the prev-evening windows
                        "start_date": (start - timedelta(days=1)).isoformat(),
                        "end_date": end.isoformat(), "timezone": "Europe/Berlin"},
            )
            r.raise_for_status()
            points[name] = PointSeries(r.json()["hourly"])
    out: dict[date, dict] = {}
    day = start
    while day <= end:
        f = build_day_features(points, day)
        if f is not None:
            out[day] = {"ora": classify("ora", f), "peler": classify("peler", f)}
        day += timedelta(days=1)
    return out


def build_strip(days: int, observed: dict[date, dict], hindcast: dict[date, dict]) -> dict:
    """Rows for the template: oldest -> newest, last `days` full days."""
    end = date.today() - timedelta(days=1)
    cells = []
    hits = {"ora": [0, 0], "peler": [0, 0]}  # [correct, decided]
    for i in range(days - 1, -1, -1):
        day = end - timedelta(days=i)
        obs = observed.get(day, {"ora": None, "peler": None})
        hc = hindcast.get(day)
        cell = {"date": day, "label": day.strftime("%d.%m.")}
        for regime in ("ora", "peler"):
            verdict = hc[regime]["verdict"].lower() if hc else None
            fired = obs[regime]
            cell[f"{regime}_model"] = verdict or "empty"
            cell[f"{regime}_obs"] = ("go" if fired else "no_go") if fired is not None else "empty"
            if verdict in ("go", "no_go") and fired is not None:
                hits[regime][1] += 1
                if (verdict == "go") == bool(fired):
                    hits[regime][0] += 1
        cells.append(cell)
    summary = {r: {"correct": c, "decided": n} for r, (c, n) in hits.items()}
    return {"cells": cells, "summary": summary}
