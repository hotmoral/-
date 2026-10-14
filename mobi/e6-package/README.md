# Samsung / One UI E6 Probe Package

This is a synthetic Android technical-evidence package. It contains no Mobi product source, private assets, user data, or semantic screen-reading logic.

## Purpose

Run the already-proven generic environment probe on one real Samsung Galaxy with Samsung Keyboard active, using ADB. The same package can be used with:

- Samsung Remote Test Lab + Remote Debug Bridge (RDB), or
- a physical Galaxy connected through normal ADB / wireless debugging.

## Preconditions

- real Samsung Galaxy device
- Samsung Keyboard selected as the active default keyboard
- ADB connection authorized
- device unlocked for the duration of the test
- two debug APKs in `apks/`

The script does **not** use Accessibility, Usage Stats, location, screenshots as a product input, clipboard reading, notification-content access, or real user content. The host app contains only synthetic text.

## Run

Linux / macOS / Git Bash:

```bash
bash run.sh
```

The package installs the two synthetic debug apps, grants the test overlay app-op over ADB, runs the controlled Samsung Keyboard scenarios, captures structural evidence, restores rotation settings, and stops the test apps.

Set `RUN_ROTATION=0` if rotation must not be changed:

```bash
RUN_ROTATION=0 bash run.sh
```

Set `CLEANUP_APPS=1` to uninstall both synthetic apps at the end:

```bash
CLEANUP_APPS=1 bash run.sh
```

## Evidence

A timestamped `evidence/` directory is created beside the script. Keep the whole directory. Do not select only screenshots; the WindowMetrics, host control, WindowManager, input-method, logcat, identity, and SHA-256 files are part of the evidence chain.

## Critical gates

The run checks:

1. the connected device is Samsung;
2. the default IME is Samsung-family;
3. the two APKs install and the overlay foreground service starts;
4. another UID owns the focused synthetic editor;
5. Samsung Keyboard is visible to the host control;
6. overlay WindowContext / WindowMetrics reports the same positive docked IME bottom geometry;
7. Mode A overlap is retained as a negative coexistence control;
8. Mode B keeps the editor focused and accepts synthetic text input;
9. optional rotation evidence is captured and prior rotation settings are restored.

A script SUCCESS is evidence only for that exact device/build/keyboard state. It does not prove all Samsung devices or all One UI versions.