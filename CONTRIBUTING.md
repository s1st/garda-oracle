# Contributing

Issues and feedback are welcome. Before submitting code, please open an issue
and wait for the maintainer to confirm that the contribution can be accepted.
The project currently has no contributor licence agreement. Forecast changes
need a higher evidence bar than copy or layout changes because a plausible
physical story is not enough to prove predictive value.

## Setup

```bash
uv sync --frozen --extra dev
uv run pytest -q
uv run ruff check src tests scripts
uv run mypy src
```

Add `--extra ml` only when working on training or research scripts.

## Change expectations

- Keep runtime scoring free of scikit-learn, pandas and NumPy.
- Build model features through the shared production feature path.
- Add tests for behaviour changes and retain all three UI languages.
- Do not commit downloaded weather data.
- Preserve source attribution and update `DATA_SOURCES.md` when adding data.
- Do not tune on a single recent day. Model or threshold changes need
  year-blocked evaluation and a documented comparison with the current model.
- Generated coefficient changes must be produced by
  `scripts/export_garda_coeffs.py`, reviewed as data and accompanied by an
  updated golden-vector test.

## Pull requests

Describe:

1. the user-visible or scientific problem;
2. the evidence supporting the change;
3. commands used to validate it; and
4. any effect on data licensing, model interpretation or deployment.

For vulnerabilities or accidentally exposed credentials, follow
[`SECURITY.md`](SECURITY.md) rather than opening a public issue.
