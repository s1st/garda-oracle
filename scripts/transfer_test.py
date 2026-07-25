"""Forecast-transfer test: how much skill survives when features come from
yesterday's forecast run (previous_day1) instead of ERA5 reanalysis?

Train: ERA5 features, season days <=2023.
Test:  season days 2024..2026 present in BOTH sources, scored twice —
       (a) ERA5 features (ceiling), (b) previous_day1 features (deployable).
"""

import json
import math
from datetime import timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
GARDA = ROOT / "data"


def load_point(subdir: str, name: str, suffix: str) -> pd.DataFrame:
    d = json.loads((GARDA / subdir / f"{name}.json").read_text())["hourly"]
    df = pd.DataFrame(d)
    df["time"] = pd.to_datetime(df["time"])
    df = df.set_index("time")
    if suffix:
        df.columns = [c.replace(suffix, "") for c in df.columns]
    return df


def build_features(subdir: str, suffix: str, labels: pd.DataFrame) -> pd.DataFrame:
    tor = load_point(subdir, "torbole", suffix)
    ver = load_point(subdir, "verona", suffix)
    bz = load_point(subdir, "bolzano", suffix)
    ib = load_point(subdir, "innsbruck", suffix)
    dp_bz = bz["pressure_msl"] - ver["pressure_msl"]
    dp_ib = ib["pressure_msl"] - ver["pressure_msl"]

    def win(s, day, h1, h2, fn):
        w = s.loc[pd.Timestamp(day) + pd.Timedelta(hours=h1) : pd.Timestamp(day) + pd.Timedelta(hours=h2)]
        return getattr(w, fn)() if not w.empty and not w.isna().all() else np.nan

    rows = []
    for _, r in labels.iterrows():
        day = r["date"].date()
        prev = day - timedelta(days=1)
        f = dict(
            date=day,
            year=day.year,
            month=day.month,
            ora=r["ora"],
            peler=r["peler"],
            dp_bz_morn=win(dp_bz, day, 6, 10, "mean"),
            dp_ib_morn=win(dp_ib, day, 6, 10, "mean"),
            dp_ib_trend=win(dp_ib, day, 11, 13, "mean") - win(dp_ib, day, 5, 7, "mean"),
            dtmax_ve_ib=win(ver["temperature_2m"], day, 6, 16, "max")
            - win(ib["temperature_2m"], day, 6, 16, "max"),
            solar_morn=win(tor["shortwave_radiation"], day, 8, 12, "max"),
            cloud_morn=win(tor["cloud_cover"], day, 6, 12, "mean"),
            rh_morn=win(tor["relative_humidity_2m"], day, 6, 10, "mean"),
            precip_day=win(tor["precipitation"], day, 6, 18, "sum"),
            w100_noon=win(tor["wind_speed_100m"], day, 11, 15, "mean"),
            tmax_tor=win(tor["temperature_2m"], day, 6, 18, "max"),
            dp_ib_night=win(dp_ib, day, 1, 5, "mean"),
            dp_bz_night=win(dp_bz, day, 1, 5, "mean"),
            cloud_night=win(tor["cloud_cover"], day, 0, 6, "mean"),
            precip_night=(win(tor["precipitation"], prev, 18, 23, "sum") or 0)
            + (win(tor["precipitation"], day, 0, 4, "sum") or 0),
            w100_night=win(tor["wind_speed_100m"], day, 1, 5, "mean"),
            solar_prev_pm=win(tor["shortwave_radiation"], prev, 12, 18, "max"),
            rh_night=win(tor["relative_humidity_2m"], day, 0, 5, "mean"),
        )
        wd = win(tor["wind_direction_100m"], day, 11, 15, "mean")
        ws = f["w100_noon"]
        ok = not (pd.isna(wd) or pd.isna(ws))
        f["w100_u"] = -ws * math.sin(math.radians(wd)) if ok else np.nan
        f["w100_v"] = -ws * math.cos(math.radians(wd)) if ok else np.nan
        rows.append(f)
    return pd.DataFrame(rows).dropna()


FEATS = {
    "ora": [
        "dp_bz_morn",
        "dp_ib_morn",
        "dp_ib_trend",
        "dtmax_ve_ib",
        "solar_morn",
        "cloud_morn",
        "rh_morn",
        "precip_day",
        "w100_noon",
        "w100_u",
        "w100_v",
        "tmax_tor",
    ],
    "peler": [
        "dp_ib_night",
        "dp_bz_night",
        "cloud_night",
        "precip_night",
        "w100_night",
        "solar_prev_pm",
        "rh_night",
        "dp_ib_morn",
        "dtmax_ve_ib",
    ],
}


def peirce(y, yh):
    tp = ((y == 1) & (yh == 1)).sum()
    fn = ((y == 1) & (yh == 0)).sum()
    fp = ((y == 0) & (yh == 1)).sum()
    tn = ((y == 0) & (yh == 0)).sum()
    return (tp / (tp + fn) if tp + fn else 0) - (fp / (fp + tn) if fp + tn else 0)


labels = pd.read_csv(GARDA / "labels.csv", parse_dates=["date"])
era = build_features("era5", "", labels)
fc = build_features("prevruns", "_previous_day1", labels)

train = era[era.year <= 2023]
test_dates = sorted(set(era[era.year >= 2024].date) & set(fc.date))
era_te = era[era.date.isin(test_dates)].sort_values("date")
fc_te = fc[fc.date.isin(test_dates)].sort_values("date")
print(f"train {len(train)} days (<=2023) | test {len(test_dates)} days 2024-2026 (both sources)")

for target in ("ora", "peler"):
    m = make_pipeline(StandardScaler(), LogisticRegression(class_weight="balanced", max_iter=2000))
    m.fit(train[FEATS[target]], train[target])
    y = era_te[target].to_numpy()
    rate = train.groupby("month")[target].mean()
    print(f"\n=== {target.upper()} (n={len(y)}, base {y.mean():.0%}) ===")
    for nm, X in (("ERA5 (ceiling)", era_te), ("day-1 forecast", fc_te)):
        p = m.predict_proba(X[FEATS[target]])[:, 1]
        print(f"{nm:16s} AUC {roc_auc_score(y, p):.3f} | Peirce@0.5 {peirce(y, (p >= 0.5).astype(int)):+.3f}")
    bp = era_te["month"].map(rate).to_numpy()
    best = max(peirce(y, (bp >= t).astype(int)) for t in np.quantile(bp, np.linspace(0.05, 0.95, 37)))
    print(f"{'climatology':16s} AUC {roc_auc_score(y, bp):.3f} | best-thr Peirce {best:+.3f}")
