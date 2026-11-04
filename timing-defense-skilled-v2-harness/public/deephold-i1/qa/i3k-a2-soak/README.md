# DeepHold I3K-A2 — protected 105+30 actor sustained-load QA (ISOLATED)

This is a diagnostic built from private source `hotmoral/DeepHold` branch `qa/i3k-a2-sustained-105-device-soak-v1` at source commit `bf9f95472b9c7d3f8a2c1b75fe4dcaccd53ff39f`.

- Automated GitHub run: https://github.com/hotmoral/DeepHold/actions/runs/41781211612 — PASS strict default/QA builds, original B1/B2 regressions, P1/P4/P5 attrition cases and P4/P5 SOAK, plus 120s Chromium actor-count integrity check.
- New SOAK scenarios: `p4-soak` = Common100 + Ferrix S3 Special5 + 30 real materialized QA Gnawers; `p5-soak` adds synthetic pulse VFX. This is NOT real projectile stress.
- SOAK is deliberately noncanonical: only during QA, Soulbound actor damage from monster hits is suppressed and QA hostile HP is clamped to at least 1. Real targeting, attack cadence, movement, hit VFX, damage-to-monster work, render objects and positions still execute. Original `p4/p5` retain normal combat deaths and recovery, for attrition comparison. Player death suppression is common to the A2 QA harness.
- Output: 5-second actor-count timeline, 1-second minimum checks, FPS/rAF p50/p95/p99/max, >=1000ms hitch count, touch-down-to-next-rAF scheduling proxy (not action latency), memory when available, manual heat observation, source commit and QA URL.
- Automated Chromium 120s verified 105+30 count retained with 26 timeline samples and no QA-hostile replacement, BUT virtualized headless Chromium FPS was about 0.6 and **cannot represent Android hardware performance**. Android Chrome/Samsung Internet device measurements still PENDING.
- Five Special actors are 5 different soulIds of one Ferrix S3 profile, not five distinct Special species. Hostile 5000HP and SOAK protection invalidate live game balance judgments.

**Open on Android in landscape:** https://timing-defense-skilled-v2-harness.sktjsek.workers.dev/deephold-i1/qa/i3k-a2-soak/?crowd-qa=1&case=p5-soak&seconds=120

Tap `측정 시작` and use joystick/skills during 120s. After completion choose heat observation, tap `JSON 복사` (or JSON save), and share the report. Do not mistake `loadMaintained=true` for performance PASS if frame intervals/hitch/heat are unacceptable.

Production main source, original hosted game `/deephold-i1/`, A2/B1/B2 QA, Cloudflare Worker script/config and other apps MUST remain unchanged.
