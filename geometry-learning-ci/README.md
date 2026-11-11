# Public synthetic CI space — Geometry Learning

This branch exists solely to run **public-safe, independently written**
validation of generic learning/transfer design rules on GitHub's standard
public hosted runners.

- Workflow: `.github/workflows/geometry-learning-ci.yml`
- Sandbox folder: `geometry-learning-ci/`
- No external secrets, credentials, private checkout, private bank files,
  student progress data, unpublished source, Golden vectors or real IDs.
- All sample skill IDs (S1, S2), stimuli and representations here are synthetic.
- Only tests **generic logic** (three distinguishable practice observations,
  two genuine representations, held-out unseen probes, stage-update exclusion).
- A green status here is **NOT** a private GeometryLearningProgram regression
  or validated educational outcome.
- To run private tests: use authorized local isolated environment or an
  explicitly approved private workflow, and keep private artifacts private.
- No upload-artifact action; log-only output minimizes storage usage.
- Changes on this branch must remain confined to this workflow and folder.
- This branch is separate from all other games and projects in `hotmoral/-`.

## Fresh-example educational prototype (public synthetic)

`generic_newform.py` defines an independently written toy model for:
- Distinguishing first-try independent training success from assisted success,
- Requiring multiple stimuli and distinct representations,
- Keeping a new unseen assessment probe separate from training,
- Requiring an additional fresh and verified delayed probe for maintenance,
- Rejecting already-seen examples as evidence of being unseen.

These generic results are **not** authoritative current V1 `TransferConfidence`
outputs and never establish a learner's spatial competence. The private repo
alone owns the side-by-side reference vectors and real schema mapping.

## Responsive learning-player mock (R1A-2-3)

- File: [mock/index.html](mock/index.html) — download or open as a local HTML file in a browser
- Purpose: mobile-first geometry viewport, clear tool separation, synthetic rotation/reflection/placement interactions
- All shapes and choices are fabricated UI samples: **no canonical problem bank, no scorer, no account storage, no student information**
- Browser smoke: `python3 mock/browser_smoke.py` (Python Playwright + system Chrome)
- Real public hosted Actions example: https://github.com/hotmoral/-/actions/runs/42972369928 (40 unit tests + five viewport browser smoke, SUCCESS)
- Five browser sizes: 320×568, 360×800, 823×384, 768×1024, 1280×850
- Primary action is visible without scrolling on the three phone layouts; no canvas/controls overlay or horizontal overflow
- Actual V1 source integration and authoritative correctness must only happen in the **private** GeometryLearningProgram repository

Open the GitHub file, select **Raw**, and save it as `index.html` if your browser shows source instead of rendering. It contains all CSS and JavaScript inline and does not require network access.
