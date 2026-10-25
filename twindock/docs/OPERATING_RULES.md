# Operating Rules

1. Preserve V8 as the immutable fallback baseline.
2. Work in bounded slices. One slice should answer one product question.
3. Do not rerun expensive build/AI workflows when deterministic local checks are sufficient.
4. Use Codex only for implementation batches large enough to justify delegation; provide frozen constants and acceptance tests up front.
5. Use public GitHub Actions only when a repeatable build/test lane materially reduces manual work.
6. Do not move to Android packaging until a 3–5 minute Mission 01 loop, input stability, and replay intent are validated.
7. Prefer web-native static architecture until a concrete platform requirement justifies additional tooling.
8. Each completed slice updates `PROJECT_STATUS.md` before the next slice begins.
9. Refactor and tuning are separate changes: no silent gameplay-value changes during structural cleanup.
10. Device feel overrides synthetic parity checks for input/camera behavior; deterministic tests protect math and contracts, not tactile judgment.
