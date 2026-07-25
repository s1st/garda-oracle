# Model card

## Summary

Garda Oracle contains two independent binary logistic-regression models:

- **Peler:** whether a directed morning wind establishes at Torbole;
- **Ora:** whether a directed afternoon wind establishes at Torbole.

The models produce calibrated probabilities. Product verdicts are `GO`,
`MAYBE` and `NO GO`; `MAYBE` is an uncertainty band below the fitted GO
threshold rather than a separately trained class.

## Intended use

The models are a day-ahead and same-day decision aid for wind-sport planning
at the northern end of Lake Garda, with a Torbole/east-shore focus.

They are not intended for:

- official weather warnings or safety-critical decisions;
- predicting exact wind speed, gusts or start/end times;
- representing every shoreline location; or
- replacing current observations and local judgement.

## Targets

Labels come from 10-minute Meteotrentino T0193 observations in local time.

| Regime | Window | Direction sector | Positive label |
|---|---|---|---|
| Peler | 04:00–09:00 | 10–120° | Mean directed wind ≥ 8 kt with at least 12 samples |
| Ora | 12:00–17:00 | 150–240° | Mean directed wind ≥ 8 kt with at least 15 samples |

The Peler sector is deliberately NE–E rather than due north: local steering
around Monte Brione rotates the along-lake flow at the Torbole station.

## Data

- Label period: July 2012 through July 2026, April–October season days.
- Label station: Meteotrentino T0193, Torbole (Belvedere), approximately
  90 metres above sea level and a 6-metre mast.
- Training features: Open-Meteo ERA5 reanalysis at Torbole, Verona, Bolzano
  and Innsbruck.
- Transfer/calibration features: Open-Meteo `previous_day1` model-run fields
  from 2024 onward.

Raw downloads are not distributed in the repository. See
[`DATA_SOURCES.md`](../DATA_SOURCES.md) and
[`docs/reproducibility.md`](reproducibility.md).

## Features

The Ora model has 12 features covering:

- morning Bozen/Verona and Innsbruck/Verona pressure contrasts;
- morning-to-midday pressure evolution;
- Po Valley–Alps heating contrast;
- morning solar radiation, cloud and humidity;
- daytime precipitation and Torbole maximum temperature; and
- 100-metre wind speed and vector components.

The Peler model has nine features covering:

- overnight pressure contrasts;
- overnight cloud, precipitation, humidity and 100-metre wind;
- previous-afternoon solar radiation; and
- morning pressure and heating contrasts.

Feature contributions shown in the dashboard are signed terms in the linear
logit. They explain what moved this model prediction, but do not prove a
single physical cause.

## Training and calibration

Each target uses `LogisticRegression(class_weight="balanced")` on standardised
features. The long model fit uses ERA5. A second logistic fit performs Platt
calibration on the previous-run feature distribution.

The committed operating points are:

| Regime | MAYBE threshold | GO threshold |
|---|---:|---:|
| Ora | 0.539 | 0.689 |
| Peler | 0.412 | 0.562 |

All serving parameters are frozen in `src/garda/coeffs.py`.

## Evaluation

### Leave-one-year-out validation

Approximately 2,972 complete season days were pooled after holding out each
year in turn.

| Regime | Base rate | AUC | Peirce | Monthly-climatology Peirce |
|---|---:|---:|---:|---:|
| Ora | 69% | 0.841 | **+0.544** | +0.218 |
| Peler | 53% | 0.757 | **+0.388** | +0.195 |

### 2026 re-forecast

Training through 2025 and evaluating 94 days in 2026 produced:

| Regime | AUC | Peirce | Accuracy |
|---|---:|---:|---:|
| Ora | 0.837 | +0.526 | 84% |
| Peler | 0.706 | +0.340 | 67% |

### Reanalysis-to-forecast transfer

On the same 513 days from 2024–2026, the ERA5-trained model was scored once
with ERA5 fields and once with the previous day's real forecast fields:

| Regime | ERA5 best-threshold Peirce | Previous-day forecast Peirce |
|---|---:|---:|
| Ora | +0.581 | **+0.590** |
| Peler | +0.383 | **+0.494** |

An honest threshold split—calibration on 2024, evaluation on 2025–2026—gave
+0.519 for Ora and +0.471 for Peler. This is the central evidence that the
signal is deployable rather than only visible in hindsight.

## Known limitations

1. **One label station.** T0193 represents Torbole, not the whole lake.
   Limone observations differ substantially and their representativeness is
   still under investigation.
2. **A binary 8-kt threshold.** Marginal Peler false alarms often measured
   6.7–7.8 kt; the circulation may have existed while missing the product
   threshold.
3. **Dead-Ora days.** Some high-confidence setups remain calm or mixed. True
   northerly suppression explains only a minority, and tested ERA5-derived
   override features did not improve the model significantly.
4. **No gust or session-quality target.** Historical T0193 labels use mean
   speed and direction, not ride duration, gustiness or subjective quality.
5. **Provider revisions.** Reanalysis and station archives can be corrected
   after the training snapshot.
6. **Season scope.** Evaluation covers April–October; winter behaviour is not
   established.
7. **Spatial model limits.** Global and regional grid fields do not resolve
   all shoreline effects, valley jets or local shadows.

## Monitoring

The public 30-day history compares a stable day-ahead (`previous_day1`)
hindcast with observations. It is useful for recent face validity but is too
small for retuning. Model changes should be justified with multi-year,
year-blocked evaluation and reflected by a changed coefficient golden vector.
