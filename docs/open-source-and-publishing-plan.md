# Open-source and publishing plan

## Goal

Prepare Garda Oracle as a clean, reproducible open-source hobby project and
use the release as the basis for a short series of two or three LinkedIn
articles.

The public story should focus on:

- the local wind-forecasting problem at Lake Garda;
- building and validating a useful model from openly reusable data;
- turning the experiment into a small, explainable public product; and
- what transferred from the earlier Walchensee Oracle project.

Walchensee Oracle is relevant as the starting point for the transfer question,
but it is not the main subject. The Garda project should be presented
positively as an open-data-first implementation without dwelling on the
licensing constraints of the earlier project.

## Working branch

Do the release preparation on a dedicated branch from the current public-site
baseline:

```text
codex/open-source-release
```

Keep the current production site deployable throughout the work. Merge only
after the repository audit and the reproducibility checks are complete.

## Implementation status

The release work is implemented on `codex/open-source-release`. The branch
contains the repository audit, explicit licensing and data provenance,
reproducibility and model documentation, public-facing project metadata, CI,
contributor/security guidance, a mobile README screenshot and three LinkedIn
drafts.

Before making the GitHub repository public, the maintainer still needs to:

- decide whether to preserve the existing short Git history or publish a
  squashed public history;
- merge the branch after review;
- change the GitHub repository visibility; and
- create the first release/tag when the merged CI run is green.

## Phase 1: repository and history audit

- Inspect the full Git history for credentials, private URLs, personal data,
  proprietary data and large generated artefacts.
- Review tracked and ignored datasets. No raw observation or training data
  should be published unless its licence clearly permits redistribution.
- Verify that configuration and examples contain no deploy credentials,
  Cloudflare secrets or reusable access tokens.
- Decide whether deployment-specific project and service names should remain
  as examples or be replaced with neutral placeholders.
- Remove stale private-beta and experimental wording from package metadata,
  comments and documentation.
- Decide whether to commit a dependency lock file and make that choice
  consistent in the development instructions.

## Phase 2: licensing and data provenance

- Select and add a code licence.
- Add a clear data-source and attribution document covering:
  - Meteotrentino / Provincia Autonoma di Trento, including the applicable
    CC BY terms and required attribution;
  - Open-Meteo and the underlying forecast/reanalysis datasets;
  - which data is fetched by scripts and which artefacts are distributed in
    the repository;
  - whether the frozen model coefficients are covered by the code licence.
- Record the distinction between permission to access data, permission to
  automate retrieval and permission to redistribute downloaded data.
- Make all attribution shown by the site consistent with the repository
  documentation.

## Phase 3: reproducibility and technical documentation

- Verify a clean setup from a fresh checkout.
- Document the complete path from public observations and forecast data to:
  1. daily Ora/Peler labels;
  2. training features;
  3. model fitting and calibration;
  4. exported pure-Python coefficients; and
  5. live scoring.
- Make explicit which large or fetched inputs are intentionally not committed
  and how another developer can recreate them.
- Add a compact architecture/data-flow diagram.
- Add a model card describing:
  - prediction targets and time windows;
  - training and validation periods;
  - performance against climatology;
  - the previous-run forecast-transfer test;
  - known limitations, especially the single Torbole label station,
    marginal Peler days and high-confidence dead-Ora cases; and
  - the difference between statistical association and physical causation.
- Document the relationship to Walchensee Oracle: the forecasting methodology
  transferred, while the Garda models, labels and data sources are independent.

## Phase 4: public repository quality

- Rewrite the README for a first-time external visitor: problem, screenshot,
  live demo, how it works, results, local setup and licence.
- Add contribution and security-reporting guidance if useful for the intended
  level of outside participation.
- Run tests, linting and type checks from a fresh environment.
- Add or verify CI for those checks on pull requests.
- Verify the Docker build and local dashboard without production secrets.
- Review accessibility, mobile rendering and all German, English and Italian
  pages.
- Prepare a first public release/tag only after the audit is complete.

## Phase 5: LinkedIn series

### Article 1 — Can a local wind model transfer to another lake?

- Start with Walchensee Oracle as the earlier hobby project.
- Introduce the question of transferring the method rather than copying the
  model.
- Explain Ora and Peler and why standard weather apps do not directly answer
  the session question.
- End with the discovery that both regimes contain a strong forecastable
  signal.

### Article 2 — Fourteen years of open data to an honest forecast

- Explain the Torbole observations, wind-sector labels and open forecast data.
- Show the leave-one-year-out result against monthly climatology.
- Make the reanalysis-versus-previous-run transfer test the centrepiece: the
  useful result survives contact with real day-ahead forecast inputs.
- Include the negative findings and limitations rather than presenting only a
  success metric.

### Article 3 — Turning the model into a public product

- Show the pure-Python scorer, three-day dashboard and factor explanations.
- Cover multilingual UI, caching, deployment and open-data attribution.
- Explain why the project is being published as open source.
- Link the live site and repository and invite technically specific feedback.

If the material is too thin for three articles, combine Articles 2 and 3 into
one technical build-and-release article.

## Release criteria

The repository is ready to make public when:

- the history and current tree have passed the privacy/secret/licence audit;
- the code and data-source licences are explicit;
- a fresh checkout can run the tests and local site from documented commands;
- the training/export path is reproducible from documented public inputs;
- the model's performance and limitations are stated accurately;
- the website and repository attributions agree; and
- the README makes sense without access to private notes or prior project
  context.
