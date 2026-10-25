# Operating Rules

1. Preserve V8 as the immutable fallback baseline until a later baseline is explicitly accepted and documented.
2. Work in bounded slices. One slice should answer one product question.
3. Do not rerun expensive build/AI workflows when deterministic local checks are sufficient.
4. Use Codex only for implementation batches large enough to justify delegation; provide frozen constants, scope, non-goals, and acceptance tests up front.
5. Use public GitHub Actions only when a repeatable build/test lane materially reduces manual work.
6. Android packaging is authorized only after the web gameplay/presentation milestone it depends on is device-validated and closed. As of P3 closure, P1 Mission 01, P2 world-readable feedback, and P3 game-feel/presentation are accepted, so the Android lane may begin. Do not invent a measured 3–5 minute run duration; exact Mission 01 duration was not separately instrumented.
7. Prefer web-native/static architecture and faithful wrapper packaging until a concrete native-only requirement justifies additional tooling or a native rewrite.
8. Refactor and tuning are separate changes: no silent gameplay-value changes during structural cleanup.
9. Device feel overrides synthetic parity checks for input/camera behavior; deterministic tests protect math and contracts, not tactile judgment.
10. Live repository state is authoritative. Past chats, memory, copied SHAs, and handoff text are navigation aids only when they agree with live canonical files.
11. New sessions must recover state through the read order in `START_HERE.md` before implementation, delegation, or broad revalidation.
12. Do not revalidate frozen/accepted work merely because a chat restarted. Revalidation requires relevant source change, new relevant commit, explicit contract need, or concrete mismatch.
13. Full free rotation remains available from first play. Do not remove/stage-gate it as a tutorial shortcut without a new controlled design decision.
14. Keep visible docking geometry and internal docking geometry aligned. UI success indicators and actual success thresholds must not disagree.
15. Keep the world/background deterministic unless a deliberate gameplay feature requires change. Resize/fullscreen/reset must not appear to regenerate the universe.
16. Preserve recovery gameplay: mistakes should normally create a recoverable unstable state rather than immediate reset.
17. UI/graphics/mission/platform work must not silently change the accepted control baseline.
18. Android/platform fixes must be separated from gameplay tuning. Prefer packaging the accepted web implementation first; do not rewrite physics/input/docking/camera natively merely to create an APK.
19. At every large-group closure, update `PROJECT_STATUS.md` and `SESSION_HANDOFF.md` together before starting the next group.
20. The handoff package must contain game structure/direction, frozen and accepted decisions, repository/document read order, architecture, development/validation/build pipeline, usage-efficiency policy, known risks, and the exact next execution boundary.
21. After each large-group closure, verify `START_HERE.md`, README, and other canonical documents reflect the current milestone and do not contradict live canonical state.
