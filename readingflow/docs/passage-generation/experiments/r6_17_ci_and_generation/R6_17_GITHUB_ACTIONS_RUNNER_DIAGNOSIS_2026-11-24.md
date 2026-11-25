# R6.17 GitHub Actions runner allocation failure / remediation status (2026-11-24)

Status: **GITHUB_ACTIONS_RUNNER_BLOCKED — NOT_RESOLVED**. Do not interpret as Python failing.

## Direct GitHub API evidence

- Branch: `feature/author-attribute-rng-audit-20261119` at `3af06e3c61a0dd15a9a02744e66cba3494b1ba0c` (before this mitigation commit).
- Latest catalog run: https://github.com/hotmoral/ReadingFlow/actions/runs/45308868142, 2026-11-24 01:57:53Z. Completed FAILURE in ~3 sec. GitHub API jobs record: `runner_id=0`, `runner_name=""`, `steps=[]`, 0 executed steps. Download-job-log returns BlobNotFound (404).
- Latest author run: https://github.com/hotmoral/ReadingFlow/actions/runs/45308868113, same minute, same `runner_id=0`, `steps=[]`.
- Re-ran failed catalog jobs via GitHub Actions API (run attempt **2**, 2026-11-24 02:04Z): success receipt for re-run request; latest job **138161808607** still FAILURE within 2 sec, `runner_id=0`, `steps=[]`. The re-run did not unblock runner allocation.
- Previously successful author workflow: https://github.com/hotmoral/ReadingFlow/actions/runs/44841838184 (2026-11-21 00:08Z). Thus the workflow structure was executable earlier; current failed jobs never reached checkout or Python.

## What was changed in this commit

The existing source tests and commands are **unchanged**. Only `push`/PR workflow path selection was narrowed:

- Author-attribute workflow: run on the author sampler / pools / planning / operations / directly referenced experiment sources / its own YAML changes; avoid triggering on arbitrary editorial report-only pushes.
- Passage catalog audit: run on Python test/validator code, JSON planning/catalog/revisions/experimental inputs, authoring canonical policy file and its own YAML. Avoid triggering on unrelated narrative-only reports.
- Both preserve `workflow_dispatch` for a manual full run. Catalog preserves PR triggers on relevant source changes.

This **reduces repeat billable jobs after runner access returns**, but does **not** repair an account-level quota, spending cap, runner policy, or GitHub outage. Treat future Actions as green only when runner_id>0, steps executed, and conclusion=success.

## Required account-level check (cannot be read or altered through this GitHub connector)

1. Open the failure run's summary page above and check the exact banner, particularly a billing/usage limit or payment issue.
2. GitHub account settings → Billing and licensing (or Billing and plans) → Usage and Budgets: check included Actions minutes, balance, and budget caps. Adjust only if the owner approves any charge.
3. Repository Settings → Actions → General: check Actions permissions and runner restrictions. If settings are normal and billing is not limiting, contact GitHub Support with the run IDs.
4. Re-run failed jobs only after confirming the blocker is cleared. Never classify a local Python PASS as an Actions PASS.

GitHub documentation: https://docs.github.com/en/actions/how-tos/troubleshoot-workflows
