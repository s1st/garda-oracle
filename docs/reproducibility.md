# Reproducing the Garda models

## Scope

The repository contains the complete fetch, label, validation, training and
coefficient-export code. It does not redistribute raw weather data.

The committed model was built from a data cutoff of **2026-07-03**. Pinning the
cutoff controls sample membership; it cannot prevent a provider from later
correcting an older observation or reanalysis value.

## Environment

Install the locked development and ML environment:

```bash
uv sync --frozen --extra dev --extra ml
```

All commands below run from the repository root.

## 1. Fetch observations

```bash
uv run python scripts/fetch_torbole.py --end-date 2026-07-03
```

This downloads wind speed (`515.00`) and direction (`500.00`) one year at a
time into:

```text
data/torbole/raw/515_YYYY.csv
data/torbole/raw/500_YYYY.csv
```

The cookies in the script are anonymous Hydstra UI values, not user
credentials. Requests are throttled deliberately.

## 2. Build labels

```bash
uv run python scripts/build_labels.py --end-date 2026-07-03
```

Output:

```text
data/labels.csv
```

The label definitions are recorded in the [model card](model-card.md) and
shared conceptually with the recent-history implementation.

## 3. Fetch training and transfer fields

```bash
uv run python scripts/fetch_era5_garda.py --end-date 2026-07-03
uv run python scripts/fetch_prevruns_garda.py --end-date 2026-07-03
```

Outputs:

```text
data/era5/{torbole,verona,bolzano,innsbruck}.json
data/prevruns/{torbole,verona,bolzano,innsbruck}.json
```

Existing downloads are skipped. Pass `--replace` to refresh them
intentionally.

## 4. Re-run the validation

```bash
uv run python scripts/spike_model.py
uv run python scripts/transfer_test.py
uv run python scripts/dead_ora.py
```

- `spike_model.py` performs leave-one-year-out validation against monthly
  climatology.
- `transfer_test.py` compares ERA5 and previous-run fields on identical dates.
- `dead_ora.py` analyses high-confidence Ora false alarms and documents why a
  tested northerly-override extension was not shipped.

The expected headline results are recorded in
[`docs/model-card.md`](model-card.md).

## 5. Export the serving artefact

```bash
uv run python scripts/export_garda_coeffs.py
git diff -- src/garda/coeffs.py
uv run pytest -q
```

The exporter:

1. builds both training and calibration features through
   `garda.features.build_day_features`, the production feature path;
2. fits one balanced logistic model per regime;
3. performs Platt calibration on previous-run fields;
4. selects the maximum-Peirce GO threshold in calibrated probability space;
5. writes the complete pure-Python artefact to `src/garda/coeffs.py`.

Any intentional model change should update both the generated file and the
golden-vector expectation in `tests/test_garda.py` in the same review.

## Data hygiene

`data/*` is ignored except for `data/README.md`. Before committing, verify:

```bash
git status --short
git ls-files data
```

Only `data/README.md` and the placeholder may be tracked. Do not commit raw
station downloads or Open-Meteo responses without a separate redistribution
and repository-size decision.
