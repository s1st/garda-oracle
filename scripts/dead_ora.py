"""Dead-Ora autopsy: what happens on high-probability Ora false-alarm days,
and does a north-foehn override feature fix them?

Part 1: LOYO probs for all days -> classify FA afternoons from the measured
        Torbole curves (N-suppression vs calm vs gap).
Part 2: extended feature set (northerly-aloft magnitude + measured morning
        Peler) -> LOYO rerun -> Peirce delta + what happens to the dead days.
"""

import csv
import json
import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
GARDA = ROOT / "data"
KT = 1.94384


# ---------- measured afternoon character per day (from raw curves) ----------
def load_var(var):
    out = {}
    for f in sorted((GARDA / "torbole" / "raw").glob(f"{var}_*.csv")):
        with f.open(encoding="latin-1") as fh:
            for row in csv.reader(fh):
                if len(row) < 3:
                    continue
                try:
                    ts = datetime.strptime(row[0].strip(), "%H:%M:%S %d/%m/%Y")
                    out[ts] = float(row[1])
                except ValueError:
                    continue
    return out


spd, drn = load_var("515"), load_var("500")
bydate = defaultdict(list)
for ts, v in spd.items():
    d = drn.get(ts)
    if d is not None:
        bydate[ts.date()].append((ts, v * KT, d))


def afternoon_character(day):
    ss = [(ts, v, d) for ts, v, d in bydate.get(day, []) if 12 <= ts.hour < 17]
    if len(ss) < 15:
        return dict(pm_kind="gap", pm_speed=np.nan, pm_nshare=np.nan)
    speeds = [v for _, v, _ in ss]
    nshare = sum(1 for _, v, d in ss if (d >= 315 or d <= 90)) / len(ss)
    mean = sum(speeds) / len(speeds)
    if mean >= 8 and nshare >= 0.5:
        kind = "N-WIND (suppressed)"
    elif mean < 5:
        kind = "calm"
    else:
        kind = "weak/mixed"
    return dict(pm_kind=kind, pm_speed=mean, pm_nshare=nshare)


def morning_peler_kt(day):
    ss = [v for ts, v, d in bydate.get(day, []) if 6 <= ts.hour < 10 and 10 <= d <= 120]
    return sum(ss) / len(ss) if len(ss) >= 6 else 0.0


# ---------- features (same as spike) + override candidates ----------
def load_point(name):
    d = json.loads((GARDA / "era5" / f"{name}.json").read_text())["hourly"]
    df = pd.DataFrame(d)
    df["time"] = pd.to_datetime(df["time"])
    return df.set_index("time")


tor, ver, bz, ib = (load_point(n) for n in ("torbole", "verona", "bolzano", "innsbruck"))
dp_bz = bz["pressure_msl"] - ver["pressure_msl"]
dp_ib = ib["pressure_msl"] - ver["pressure_msl"]


def win(s, day, h1, h2, fn):
    w = s.loc[pd.Timestamp(day) + pd.Timedelta(hours=h1) : pd.Timestamp(day) + pd.Timedelta(hours=h2)]
    return getattr(w, fn)() if not w.empty and not w.isna().all() else np.nan


labels = pd.read_csv(GARDA / "labels.csv", parse_dates=["date"])
rows = []
for _, r in labels.iterrows():
    day = r["date"].date()
    f = dict(
        date=day,
        year=day.year,
        month=day.month,
        ora=r["ora"],
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
    )
    wd = win(tor["wind_direction_100m"], day, 11, 15, "mean")
    ws = f["w100_noon"]
    ok = not (pd.isna(wd) or pd.isna(ws))
    f["w100_u"] = -ws * math.sin(math.radians(wd)) if ok else np.nan
    f["w100_v"] = -ws * math.cos(math.radians(wd)) if ok else np.nan
    # --- override candidates ---
    # northerly-aloft magnitude (km/h from N, floor 0) + its square
    f["north_aloft"] = max(0.0, -f["w100_v"]) if ok else np.nan
    f["north_aloft_sq"] = f["north_aloft"] ** 2 if ok else np.nan
    # measured morning Peler strength (available by ~09:30 for a same-morning verdict)
    f["peler_meas_morn"] = morning_peler_kt(day)
    # morning northerly aloft (already blowing before noon)
    wdm = win(tor["wind_direction_100m"], day, 6, 10, "mean")
    wsm = win(tor["wind_speed_100m"], day, 6, 10, "mean")
    okm = not (pd.isna(wdm) or pd.isna(wsm))
    f["north_aloft_morn"] = max(0.0, wsm * -math.cos(math.radians(wdm))) if okm else np.nan
    rows.append(f)

df = pd.DataFrame(rows).dropna()

BASE = [
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
]
EXT = BASE + ["north_aloft", "north_aloft_sq", "north_aloft_morn", "peler_meas_morn"]


def peirce(y, yh):
    tp = ((y == 1) & (yh == 1)).sum()
    fn = ((y == 1) & (yh == 0)).sum()
    fp = ((y == 0) & (yh == 1)).sum()
    tn = ((y == 0) & (yh == 0)).sum()
    return (tp / (tp + fn) if tp + fn else 0) - (fp / (fp + tn) if fp + tn else 0)


def loyo(feats):
    out = pd.DataFrame(index=df.index, columns=["p"], dtype=float)
    for yr in sorted(df.year.unique()):
        tr, te = df[df.year != yr], df[df.year == yr]
        if len(te) < 30:
            continue
        m = make_pipeline(StandardScaler(), LogisticRegression(class_weight="balanced", max_iter=3000))
        m.fit(tr[feats], tr["ora"])
        out.loc[te.index, "p"] = m.predict_proba(te[feats])[:, 1]
    return out["p"]


p_base = loyo(BASE)
mask = p_base.notna()
d = df[mask].copy()
d["p_base"] = p_base[mask]

# ---------- Part 1: autopsy ----------
fa = d[(d.p_base >= 0.7) & (d.ora == 0)].copy()
ch = fa["date"].apply(afternoon_character).apply(pd.Series)
fa = pd.concat([fa.reset_index(drop=True), ch.reset_index(drop=True)], axis=1)
print(f"high-confidence Ora false alarms (p>=0.7, actual no-Ora): {len(fa)} of {len(d)} days")
print("\nafternoon character of those days:")
print(fa.pm_kind.value_counts().to_string())
print("\nmean northerly-aloft on FA days by kind:")
print(fa.groupby("pm_kind")[["north_aloft", "peler_meas_morn", "dp_ib_morn"]].mean().round(1).to_string())
ref = d[d.ora == 1]
print(
    f"\nreference true-Ora days: north_aloft {ref.north_aloft.mean():.1f} km/h | peler_meas {ref.peler_meas_morn.mean():.1f} kt"
)

# ---------- Part 2: extended model ----------
p_ext = loyo(EXT)
d["p_ext"] = p_ext[mask]
y = d.ora.to_numpy()
for nm, p in (("BASE", d.p_base), ("+override feats", d.p_ext)):
    yh = (p >= 0.5).astype(int)
    fp = int(((y == 0) & (yh == 1)).sum())
    fn = int(((y == 1) & (yh == 0)).sum())
    print(f"\n{nm:16s} AUC {roc_auc_score(y, p):.3f} | Peirce@0.5 {peirce(y, yh):+.3f} | FA {fp} | miss {fn}")

# what happened to the dead days specifically?
dead = d[(d.p_base >= 0.7) & (d.ora == 0)]
fixed = (dead.p_ext < 0.5).sum()
print(f"\nof the {len(dead)} dead-Ora days: {fixed} now correctly below 0.5 ({fixed / len(dead):.0%})")
# and did we break true Ora days?
strong = d[(d.p_base >= 0.7) & (d.ora == 1)]
broken = (strong.p_ext < 0.5).sum()
print(
    f"of {len(strong)} previously-confident TRUE Ora days: {broken} newly lost ({broken / len(strong):.0%})"
)
# McNemar-ish discordant counts at 0.5
b2e = int(((d.p_base >= 0.5) != (y == 1)).sum())
e2 = int(((d.p_ext >= 0.5) != (y == 1)).sum())
fixed_n = int((((d.p_base >= 0.5).astype(int) != y) & ((d.p_ext >= 0.5).astype(int) == y)).sum())
broke_n = int((((d.p_base >= 0.5).astype(int) == y) & ((d.p_ext >= 0.5).astype(int) != y)).sum())
print(f"\noverall errors {b2e} -> {e2} | fixed {fixed_n}, broke {broke_n}")
# coefficient check on full fit
m = make_pipeline(StandardScaler(), LogisticRegression(class_weight="balanced", max_iter=3000))
m.fit(df[EXT], df["ora"])
coefs = sorted(zip(EXT, m[-1].coef_[0]), key=lambda t: -abs(t[1]))
print("\ntop coefficients (extended):", ", ".join(f"{n}={c:+.2f}" for n, c in coefs[:8]))
