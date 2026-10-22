# Timing Defense SKILLED_V2 Harness — Workers Builds Deployment

Status: **CALIBRATION-ONLY / SEPARATE WORKER / PRODUCTION ISOLATED**

## Fixed source
- Repository: `hotmoral/-`
- Branch: `timing-defense-skilled-v2-harness-v01`
- Root directory: `timing-defense-skilled-v2-harness`
- Worker/project name: `timing-defense-skilled-v2-harness`
- Wrangler config: `wrangler.jsonc`
- Deploy command: `npx wrangler deploy`
- Build command: leave empty unless Cloudflare requires one

## Required isolation
This project MUST be created as a separate Cloudflare Worker/Workers Builds project.
Do not repoint or reuse `timing-defense-do-poc`.

The calibration Worker has no authority over:
- production Durable Objects
- production room/session state
- campaign progression
- stars/Tier records
- achievements/titles
- campaign EXP/coin/shop state

## Cloudflare Workers Builds setup
1. Cloudflare Dashboard -> Workers & Pages -> Create application.
2. Choose GitHub repository source.
3. Select repository `hotmoral/-`.
4. Select production branch `timing-defense-skilled-v2-harness-v01` for this calibration project only.
5. Root directory: `timing-defense-skilled-v2-harness`.
6. Project/Worker name: `timing-defense-skilled-v2-harness`.
7. Build command: empty unless required.
8. Deploy command: `npx wrangler deploy`.
9. Save and Deploy.

Do not paste Cloudflare API credentials into repository files.

## First smoke order
After Cloudflare provides the separate `*.workers.dev` URL:

1. `GET /health` -> HTTP 200 and calibration service identity.
2. root `/` loads the harness selector.
3. mobile browser H0 run starts and input responds.
4. H0 produces >=40 ACTION records and JSONL export/copy works.
5. H3 shows NO_TARGET_START -> NO_TARGET_END -> TARGET_REORDER and post-turnover ACTION.
6. H4 shows WINDUP_START and subsequent response/full-activation evidence.
7. exported sample traces pass the canonical dataset validator.
8. confirm production `timing-defense-do-poc` state is unaffected.

## Player classification for first pilot
The primary user's first traces are interpreted as `HIGH_MASTERY_STRESS_CANDIDATE`, not `SKILLED_V2_CENTRAL`.
This is an analysis label only; do not bias the input surface or lower/raise difficulty to force that classification.

## Deployment boundary
A successful calibration deployment authorizes browser/device smoke and a small controlled H0–H5 pilot only.
It does NOT authorize production gameplay changes or production balance freezes.
