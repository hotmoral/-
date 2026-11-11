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
