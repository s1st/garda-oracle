# Garda feasibility spike: Ora/Peler are predictable well beyond climatology — 2026-07-05

Question: does the Walchensee methodology generalize to Lake Garda — is there
day-ahead-grade weather signal for the two thermal regimes (Ora, Peler), using
only open data? Answer: **yes, with a wide margin.** This is the ML-first
ceiling check from the expansion plan; no rules were ported.

To keep the experiment independently reproducible, everything here uses
**openly reusable sources only**: Meteotrentino station T0193 for ground truth
and ERA5 fields from Open-Meteo for features.

## Ground truth

**Meteotrentino T0193 "Torbole (Belvedere)"** (90 m, in Torbole, 6 m mast),
10-min mean wind + direction, **2012-07-04 → today** (sensor installed at the
2012 station relocation; no gust channel in the archive; all values quality
code 145 "telemetry, not validated" + ~2 % code 140). Pulled via
`scripts/garda/fetch_torbole.py` — the Hydstra storico export is a plain GET
(one variable per request; the UI's silent one-variable msgBox and a confirm()
dialog make it *look* broken). 730k joined samples, coverage ≈100 % 2013–2025.
Data: `data/garda/torbole/raw/` (gitignored).

**Two-regime day labels** (`scripts/garda/build_labels.py` →
`data/garda/labels.csv`), Apr–Oct, n=2,973 days:

- **Ora** = S-sector (150–240°) 12–17h mean ≥ 8 kt → **69 %** of days
  (72–80 % Apr–Aug, 40 % Oct). Onset median 11:30, IQR 10:42–12:18.
- **Peler** = NE–E sector (**10–120°**, NOT north!) 04–09h mean ≥ 8 kt →
  **53 %** of days. Monte Brione steers the along-lake N flow to NE–E at
  Torbole; a naive 315–45° sector undercounts to 13 %.
- 37 % of days have both regimes (the classic double day).

Cross-check Limone (ARPA Lombardia sensor 14065/14066, Apr–Jul 2026 via the
live Socrata API): the west-shore village station **barely sees the Peler**
(15 % vs Torbole's 55 % on common days; mornings are W katabatic drainage) and
is sheltered for Ora strength (39 % vs 72 % ≥ 8 kt at peak hour). Limone =
independent Ora *direction* witness + gusts (gust/mean median 1.54), not a
label source. Torbole carries both labels alone.

## Features & model

ERA5 reanalysis (open-meteo archive API, `scripts/garda/fetch_era5_garda.py`),
4 points: Torbole (cloud, solar, temp, precip, RH, 100 m wind), Verona,
Bolzano, Innsbruck (MSL pressure, temp). Per-regime logistic regression
(standardized, class_weight=balanced), **leave-one-year-out** over 2012–2026,
n=2,972 days with full features. Baseline: month-of-year climatology fit on
train years. `scripts/garda/spike_model.py`.

## Results (LOYO, pooled)

| regime | base rate | model AUC | model Peirce | climatology AUC | climatology Peirce |
|---|---|---|---|---|---|
| **Ora** | 69 % | **0.841** | **+0.544** | 0.613 | +0.218 |
| **Peler** | 53 % | **0.757** | **+0.388** | 0.596 | +0.195 |

Both regimes ≈ **double the climatology skill**. For scale: the Walchensee
14-rule system scores Peirce +0.107 on its thermal label, the ML ceiling there
+0.14–0.22 — the Garda Ora signal (+0.544) is *much* stronger, consistent with
a larger, synoptically-driven valley-wind system.

Top drivers are textbook physics, which raises confidence this is signal, not
artifact:

- **Ora**: southerly 100 m flow component (+0.82), daytime precip (−0.63),
  Bolzano−Verona morning pressure delta (−0.59: mountain thermal low vs plain
  → valley wind), morning solar (+0.50), morning cloud (−0.45).
- **Peler**: **Bolzano−Verona night pressure delta (+1.29)** — the classic
  north-gradient nocturnal drive — plus Innsbruck-delta terms, night RH,
  night precip (−0.28).

## Caveats

- **ERA5 = lead-time-0 reanalysis → this is a ceiling, not forecast skill.**
  A deployable model must ride the same drivers from a forecast run
  (day-ahead ICON/ECMWF); synoptic-scale pressure/flow features usually
  survive that transfer well, but it must be measured (same caveat the
  Walchensee replay carried).
- Single ground-truth station, unvalidated telemetry, one sector/threshold
  choice per regime (not sensitivity-swept).
- 8 kt mean-wind threshold is a first guess at "rideable"; per-rider
  cost/threshold tuning would follow the Walchensee shadow-classifier pattern.

## Addendum: 2026 re-forecast (train ≤2025, predict Apr–Jul 2026, 94 days)

| regime | base rate | AUC | Peirce | accuracy | hits / correct-no / miss / false-alarm |
|---|---|---|---|---|---|
| Ora | 70 % | 0.837 | +0.526 | 84 % | 63 / 16 / **3** / 12 |
| Peler | 55 % | 0.706 | +0.340 | 67 % | 35 / 28 / 17 / 14 |

Matches the pooled LOYO numbers — no degradation on the current season. Error
anatomy (from the per-day table, `ora_mean_kt`/`peler_mean_kt` on error days):

- **Peler false alarms are mostly threshold-straddles**: 11 of 14 had actual
  NE-morning wind of 6.7–7.8 kt — just under the 8 kt label line. The regime
  call was right, the strength call marginal. Misses are less flattering
  (several real 9–12 kt Peler mornings missed, clustered early April).
- **Ora false alarms are the interesting failure**: ~11 days with p ≥ 0.7 and
  actual 0.0 kt S-wind — "perfect setup, lake stayed dead" days (e.g.
  2026-05-11 p=0.94, actual 0). Candidate causes worth a look before
  productizing: north-foehn override, label gaps, or a suppression regime the
  feature set lacks (the Walchensee `foehn_override` analog).
- Only **3 missed Ora days** all season — including one painful one
  (2026-04-02, 19.4 kt at p=0.37).

## Addendum 2: forecast-transfer test — the lead time costs nothing

Features rebuilt from Open-Meteo **Previous Runs API** (`*_previous_day1` =
what yesterday's run predicted for today; archive reaches back to early 2024,
so 3 test seasons). Same ERA5-trained models (≤2023), same 513 test days
2024–2026, scored with both feature sources (`scripts/garda/transfer_test.py`
in scratchpad; fetch: `fetch_prevruns_garda.py`):

| regime | ERA5 ceiling (best-thr Peirce) | day-1 forecast (best-thr) | honest split* |
|---|---|---|---|
| Ora | +0.581 | **+0.590** | **+0.519** |
| Peler | +0.383 | **+0.494** | **+0.471** |

*threshold calibrated on 2024 only, evaluated on 2025–26 (n=308).

**The day-ahead forecast features are as good as — for Peler clearly better
than — the reanalysis ceiling.** Plausible cause: ICON previous-day fields are
finer-resolved than ERA5's ~31 km grid, which sharpens the city pressure
deltas. The only transfer cost is **probability calibration**: the ERA5-trained
logistic's 0.5 threshold sits wrong on forecast-feature distributions
(Peler@0.5 collapses to +0.166 while its AUC *rises* to 0.823) — so the
production model must either be trained on forecast features directly or have
its threshold calibrated on them (one season sufficed above).

Product-shape note (mirrors Walchensee's single 08:00 run covering today+2):
an Ora verdict issued same-morning has only ~4–8 h lead (easier than tested
here); a **Peler verdict must ship the previous evening** (04–09 h regime) —
`previous_day1` is exactly that case, and it holds +0.47.

## Addendum 3: dead-Ora autopsy — north-foehn feature is a no-build (for now)

Autopsy of all **105 high-confidence Ora false alarms** (LOYO p ≥ 0.7, no Ora)
across 2012–2026, classified by what Torbole actually measured that afternoon
(`scripts/garda/dead_ora.py`):

| afternoon character | days |
|---|---|
| weak/mixed (5–8 kt or wrong sector) | 44 |
| calm (< 5 kt) | 41 |
| **N-wind ≥ 8 kt (true foehn suppression)** | **20** |

So the folklore mode ("Nordföhn kills the Ora") is real but only ~1/5 of the
dead days — the dominant failure is *"perfect setup, thermal just doesn't
fire"*. Three further negative results, all worth remembering:

1. **ERA5's 100 m wind is blind to the suppression**: northerly-aloft
   component ≈ 0.0 even on the 20 measured-N afternoons (31 km grid doesn't
   resolve the along-lake flow). Feature candidates built from it fix **0** of
   105 dead days and cost skill (Peirce +0.544 → +0.526).
2. **Measured morning Peler doesn't discriminate** (8.0–8.8 kt on FA days vs
   7.8 kt on true-Ora days) — a strong Peler morning precedes a good Ora as
   often as a dead one.
3. The suppression *does* show in the **Innsbruck−Verona gradient**, as a
   hump: Ora rate climbs 41 %→77 % up to Δ 4–6 hPa, holds to 8, then
   **collapses to 37 % above 8 hPa** (n=151). But a hinge feature
   (`max(0, Δ−4)`) yields only +0.010 Peirce, fixed 65 / broke 50,
   **McNemar p = 0.19**, and only 2 of 40 collapse-zone errors repaired —
   within noise by the project's own standard. Not shipped.

Next lever candidates for the dead-Ora problem: pressure-level winds
(700/850 hPa) from the forecast models instead of ERA5 100 m (the
previous-runs archive has them 2024+), lake temperature, or upstream
(Sarca valley) stations.

## Verdict / next

The methodology generalizes; Garda is, if anything, the *easier* forecasting
problem. If this becomes a product: (1) re-run the feature build from
historical *forecast* data to measure the reanalysis→forecast drop, (2)
sector/threshold sensitivity on the labels, and (3) two verdicts/day product
shape (Peler morning / Ora afternoon).
