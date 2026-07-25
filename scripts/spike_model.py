"""Garda spike: logistic per regime (Ora/Peler) on ERA5 features vs climatology.

Labels: data/labels.csv (from Torbole T0193 curves).
Features: ERA5 reanalysis (lead-time-0 ceiling check, NOT forecast skill).
Validation: leave-one-year-out. Metric: Peirce (TPR-FPR) + AUC.
"""

import json
import math
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
GARDA = ROOT / "data"


def load_point(name: str) -> pd.DataFrame:
    d = json.loads((GARDA / "era5" / f"{name}.json").read_text())["hourly"]
    df = pd.DataFrame(d)
    df["time"] = pd.to_datetime(df["time"])
    return df.set_index("time")


tor = load_point("torbole")
ver = load_point("verona")
bz = load_point("bolzano")
ib = load_point("innsbruck")

dp_bz = (bz["pressure_msl"] - ver["pressure_msl"]).rename("dp_bz")
dp_ib = (ib["pressure_msl"] - ver["pressure_msl"]).rename("dp_ib")


def win(s: pd.Series, day: date, h1: int, h2: int, fn: str):
    lo = pd.Timestamp(day) + pd.Timedelta(hours=h1)
    hi = pd.Timestamp(day) + pd.Timedelta(hours=h2)
    w = s.loc[lo:hi]
    if w.empty or w.isna().all():
        return np.nan
    return getattr(w, fn)()


labels = pd.read_csv(GARDA / "labels.csv", parse_dates=["date"])
rows = []
for _, r in labels.iterrows():
    day = r["date"].date()
    prev = day - timedelta(days=1)
    f = {
        "date": day,
        "year": day.year,
        "month": day.month,
        "ora": r["ora"],
        "peler": r["peler"],
        # --- Ora drivers (morning state -> afternoon wind)
        "dp_bz_morn": win(dp_bz, day, 6, 10, "mean"),
        "dp_ib_morn": win(dp_ib, day, 6, 10, "mean"),
        "dp_ib_trend": win(dp_ib, day, 11, 13, "mean") - win(dp_ib, day, 5, 7, "mean"),
        "dtmax_ve_ib": win(ver["temperature_2m"], day, 6, 16, "max")
        - win(ib["temperature_2m"], day, 6, 16, "max"),
        "solar_morn": win(tor["shortwave_radiation"], day, 8, 12, "max"),
        "cloud_morn": win(tor["cloud_cover"], day, 6, 12, "mean"),
        "rh_morn": win(tor["relative_humidity_2m"], day, 6, 10, "mean"),
        "precip_day": win(tor["precipitation"], day, 6, 18, "sum"),
        "w100_noon": win(tor["wind_speed_100m"], day, 11, 15, "mean"),
        "tmax_tor": win(tor["temperature_2m"], day, 6, 18, "max"),
        # --- Peler drivers (overnight state -> early-morning wind)
        "dp_ib_night": win(dp_ib, day, 1, 5, "mean"),
        "dp_bz_night": win(dp_bz, day, 1, 5, "mean"),
        "cloud_night": win(tor["cloud_cover"], day, 0, 6, "mean"),
        "precip_night": (win(tor["precipitation"], prev, 18, 23, "sum") or 0)
        + (win(tor["precipitation"], day, 0, 4, "sum") or 0),
        "w100_night": win(tor["wind_speed_100m"], day, 1, 5, "mean"),
        "solar_prev_pm": win(tor["shortwave_radiation"], prev, 12, 18, "max"),
        "rh_night": win(tor["relative_humidity_2m"], day, 0, 5, "mean"),
    }
    # 100m wind vector components at noon (direction = meteorological "from")
    wd = win(tor["wind_direction_100m"], day, 11, 15, "mean")
    ws = f["w100_noon"]
    if not (math.isnan(wd) if isinstance(wd, float) else False) and not pd.isna(ws):
        f["w100_u"] = -ws * math.sin(math.radians(wd))
        f["w100_v"] = -ws * math.cos(math.radians(wd))
    else:
        f["w100_u"] = f["w100_v"] = np.nan
    rows.append(f)

df = pd.DataFrame(rows).dropna()
print(f"days with full features: {len(df)}  ({df.year.min()}-{df.year.max()})")

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


def peirce(y, yhat):
    tp = ((y == 1) & (yhat == 1)).sum()
    fn = ((y == 1) & (yhat == 0)).sum()
    fp = ((y == 0) & (yhat == 1)).sum()
    tn = ((y == 0) & (yhat == 0)).sum()
    tpr = tp / (tp + fn) if tp + fn else 0.0
    fpr = fp / (fp + tn) if fp + tn else 0.0
    return tpr - fpr


for target in ("ora", "peler"):
    X_cols = FEATS[target]
    ys, ps, base_ps = [], [], []
    for yr in sorted(df.year.unique()):
        tr, te = df[df.year != yr], df[df.year == yr]
        if len(te) < 30:
            continue
        m = make_pipeline(StandardScaler(), LogisticRegression(class_weight="balanced", max_iter=2000))
        m.fit(tr[X_cols], tr[target])
        ys.append(te[target].to_numpy())
        ps.append(m.predict_proba(te[X_cols])[:, 1])
        # climatology baseline: month fire-rate from TRAIN years
        rate = tr.groupby("month")[target].mean()
        base_ps.append(te["month"].map(rate).to_numpy())
    y = np.concatenate(ys)
    p = np.concatenate(ps)
    bp = np.concatenate(base_ps)
    print(f"\n=== {target.upper()}  (n={len(y)}, base rate {y.mean():.0%}) ===")
    print(f"model  AUC {roc_auc_score(y, p):.3f} | Peirce@0.5 {peirce(y, (p >= 0.5).astype(int)):+.3f}")
    # best-threshold Peirce for both (fair comparison)
    for nm, pr in (("model", p), ("climatology", bp)):
        best = max(peirce(y, (pr >= t).astype(int)) for t in np.quantile(pr, np.linspace(0.05, 0.95, 37)))
        auc = roc_auc_score(y, pr)
        print(f"{nm:12s} AUC {auc:.3f} | best-threshold Peirce {best:+.3f}")
    # coefficients on full data (direction of drivers)
    m = make_pipeline(StandardScaler(), LogisticRegression(class_weight="balanced", max_iter=2000))
    m.fit(df[X_cols], df[target])
    coefs = sorted(zip(X_cols, m[-1].coef_[0]), key=lambda t: -abs(t[1]))
    print("top drivers:", ", ".join(f"{n}={c:+.2f}" for n, c in coefs[:6]))
