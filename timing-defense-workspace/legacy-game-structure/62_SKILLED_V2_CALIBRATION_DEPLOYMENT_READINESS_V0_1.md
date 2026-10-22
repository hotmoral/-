# Timing Defense — SKILLED_V2 Calibration Deployment Readiness V0.1

Date: 2026-10-22 KST  
Status: **SEPARATE CALIBRATION DEPLOYMENT AUTHORIZED / CLOUDFLARE PROJECT CONNECTION PENDING**

## Authorization
The user has authorized proceeding with the calibration flow after clarifying that their own play should be treated above ordinary skilled rather than as `SKILLED_V2_CENTRAL`.

Authorized scope:
- deploy the isolated harness as a separate calibration Worker/project;
- run browser/device smoke;
- collect a small controlled H0–H5 pilot;
- treat the user's traces as `HIGH_MASTERY_STRESS_CANDIDATE` until reviewed.

Not authorized:
- production v0.45 gameplay changes;
- production balance freezes;
- treating the user's traces as ordinary-skilled center;
- broad public data collection.

## Source identities
Production baseline remains:
- branch `timing-defense-cloudflare-do-poc`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`

Calibration harness:
- branch `timing-defense-skilled-v2-harness-v01`
- reviewed deployment-ready HEAD `85396e7da53eee1d64769d76b2a0e9700577aa34`
- root `timing-defense-skilled-v2-harness`
- Worker name `timing-defense-skilled-v2-harness`

## Deployment route
Use Cloudflare Workers Builds + GitHub integration, matching the already validated Timing Defense deployment route.

Required Cloudflare project settings:
- repository: `hotmoral/-`
- branch: `timing-defense-skilled-v2-harness-v01`
- root directory: `timing-defense-skilled-v2-harness`
- Worker/project name: `timing-defense-skilled-v2-harness`
- build command: empty unless required
- deploy command: `npx wrangler deploy`

The calibration project MUST be separate from `timing-defense-do-poc`.

## External account blocker
Repository preparation is complete.
The remaining step requires Cloudflare account-side project creation/connection through the Cloudflare dashboard or an equivalent authorized Cloudflare control surface.
No Cloudflare connector is available in the current chat environment, so that account-side step cannot be performed here.

## Immediate smoke after connection
1. verify `/health` is calibration-only;
2. H0 real-device run;
3. H3 turnover run;
4. H4 stateful read run;
5. export sample JSONL;
6. canonical validator PASS;
7. verify production state unchanged;
8. patch only smoke-demonstrated instrumentation defects;
9. then small H0–H5 high-mastery-candidate pilot.

## Player-model interpretation
The first user's traces are an upper-tail stress anchor, not the central skilled population.
The non-T1 `<60%` difficulty gate remains attached to future fitted `SKILLED_V2_CENTRAL` only.
