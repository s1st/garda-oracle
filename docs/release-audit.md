# Open-source release audit

Audit date: 25 July 2026.

## Repository status at audit start

- GitHub repository: `s1st/garda-oracle`
- Visibility: **private**
- Default branch: `main`
- Release-preparation branch: `codex/open-source-release`
- History size: 12 commits before release-preparation work

Repository visibility was only inspected. Making the repository public is an
explicit maintainer action and is not part of this branch.

## History and secret review

The complete reachable history was checked for:

- common GitHub, Google and AWS key formats;
- private-key headers;
- credentials embedded in URLs;
- assignments and references containing secret/token/password terminology;
- tracked file sizes and generated datasets.

Result:

- no typical credential, access-token or private-key value was found;
- environment-variable names such as `GARDA_GATE_SECRET` and
  `CF_BEACON_TOKEN` are present, but no values are committed;
- no raw Meteotrentino or Open-Meteo download is tracked;
- the largest pre-release tracked file was below 40 KB; and
- Git author metadata contains the maintainer's name and email address, as is
  normal for a Git history. The maintainer should confirm that this identity
  may become public.

The scan was a repository-specific pattern audit, not a substitute for
GitHub's secret scanning or a dedicated scanner such as Gitleaks. Enable
secret scanning when repository visibility and account features permit it.

## Historical narrative

Earlier commits contain private-beta terminology and brief references to the
data-licensing constraints that motivated an open-data-only Garda project.
They do not contain third-party datasets or credentials.

Before changing visibility, two publication modes were considered:

1. **Preserve history:** make the repository public with the existing compact
   development history.
2. **Clean public baseline:** publish a squashed snapshot if the historical
   wording or author email should not be public.

The maintainer selected a **clean public baseline**. The public repository is
created from the audited current tree with one new AGPL-3.0-only root commit.
The earlier development history remains private in a separate shadow
repository and is not part of the public repository.

The clean baseline is present in two repositories with the same `main`
commit: a private shadow repository for staging and the canonical repository,
which remains private until the maintainer performs the final visibility
change.

## Data boundary

- `data/*` is ignored except for documentation and the placeholder.
- Fetch scripts now resolve paths from the repository rather than a personal
  workstation path.
- Raw source data remain outside the version-controlled project.
- Source-specific licence and attribution details are in
  [`DATA_SOURCES.md`](../DATA_SOURCES.md).

## Deployment configuration

`cloudbuild.yaml` contains the maintainer's GCP project, registry, image,
service and region names. These identifiers are not credentials and are
retained because the file is also the real deployment definition. Forks must
replace them.

The origin secret and analytics token are environment-injected. Neither value
is needed for local operation or the Docker build.

## Release controls added

- AGPL-3.0-only licence for project-authored code and artefacts;
- locked dependencies and pinned Python version;
- CI for lint, type checks, tests and package build;
- data provenance and source-licence documentation;
- reproducible fetch/train/export instructions;
- architecture and model card;
- contribution and security guidance; and
- explicit model safety and limitation statements.

The final container check completed successfully with Docker Desktop 4.83.0:
`docker build` produced `garda-oracle:open-source-check`, and a container
started without secrets returned HTTP 200 with the expected dashboard HTML.

The existing Cloud Build trigger was also verified against the clean canonical
repository: it built and deployed the new root commit successfully.
Dependency-graph processing, vulnerability alerts and automated security
updates are enabled.

## Remaining maintainer actions

- change GitHub visibility to public;
- enable secret scanning, push protection and branch protection once available
  for the public repository; and
- create the first release tag after CI passes on `main`.
