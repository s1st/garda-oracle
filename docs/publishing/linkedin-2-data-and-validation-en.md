# LinkedIn draft 2: A good hindsight model is not yet a forecast

*Working draft · English*

In the first part, I explored whether the methodology behind a local thermal
wind forecast could be transferred from the Walchensee to Lake Garda.

The initial results for Ora and Peler looked very good. But this is exactly
where a weather model can easily appear better than it will be in everyday
use.

The reason is a classic problem: **reanalysis is not a forecast.**

Reanalysis data reconstruct past weather with a model that incorporates all
observations available after the event. It is excellent for building long
training datasets, but it knows the past more accurately than yesterday's
real forecast could have known the future.

For Garda Oracle, I therefore used two distinct data worlds:

- Meteotrentino T0193 in Torbole provides the observed wind regimes.
- Open-Meteo/ERA5 provides the long historical weather series.
- The Open-Meteo Previous Runs API provides fields from archived model runs:
  specifically, what did yesterday's run predict for today?

The ground truth is deliberately simple and reproducible:

- Peler: wind from the relevant direction between 04:00 and 09:00, averaging
  at least 8 knots.
- Ora: wind from the relevant direction between 12:00 and 17:00, also
  averaging at least 8 knots.

Two separate logistic models are trained on these labels. Their features
include pressure differences between the Alps and the Po Valley, solar
radiation, cloud cover, precipitation, humidity, and wind at 100 metres.

First, I held out each year in turn. This prevents weather patterns from the
same year appearing in both training and test data. Across roughly 2,972
complete seasonal days, Ora achieved a Peirce Skill Score of +0.54 and Peler
+0.39.

Then came the more important test. On 513 days, I evaluated the model trained
with ERA5 twice: once using reanalysis fields and once using the actual
forecast fields from the previous day.

| Regime | ERA5 hindsight | Previous day's forecast |
|---|---:|---:|
| Ora | +0.58 | **+0.59** |
| Peler | +0.38 | **+0.49** |

Moving to real forecast inputs therefore caused no visible loss of
discrimination. Peler actually performed better. One plausible explanation is
that the archived forecast fields have a higher regional resolution than ERA5
and capture the pressure distribution around the Alps more accurately.

There was still no reason to keep only the success story:

- Many Peler false alarms reached 6.7–7.8 knots, just below the chosen 8-knot
  threshold.
- On some days, Ora fails to develop despite apparently perfect conditions.
- A tested northerly-foehn override sounded physically plausible but did not
  improve the model robustly, so I left it out.
- A single station cannot represent the entire northern part of Lake Garda.

For me, these negative results are part of taking a hobby project seriously.
A model does not become trustworthy because every plausible idea is added. It
becomes trustworthy when attractive stories are allowed to fail against the
data.

In the third part, I will show how these experiments became a small public
application with explainable forecasts, three languages, and an open-source
training pipeline.

---

## Suggested media

- Main graphic: “ERA5 vs previous_day1” table or bar chart
- Second image: simplified data flow from station → labels → model → dashboard
- Optional: example of a narrowly missed Peler day
