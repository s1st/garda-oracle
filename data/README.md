# Local data workspace

This directory is intentionally empty in Git. The public fetch and processing
scripts create:

```text
data/
├── torbole/raw/       # Meteotrentino historical wind and direction CSVs
├── labels.csv         # derived Ora/Peler day labels
├── era5/              # Open-Meteo historical/reanalysis JSON
└── prevruns/          # Open-Meteo previous-run forecast JSON
```

See [`../DATA_SOURCES.md`](../DATA_SOURCES.md) for licences and
[`../docs/reproducibility.md`](../docs/reproducibility.md) for exact commands.

Do not force-add downloaded data without reviewing both redistribution rights
and repository size.
