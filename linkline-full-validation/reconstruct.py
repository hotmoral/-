from pathlib import Path
import hashlib
import os

app = Path(os.environ['APP'])

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()

part1 = Path('linkline-full-validation/chunks/clear-result-ui.01').read_bytes()
part2 = Path('linkline-full-validation/chunks/clear-result-ui.02').read_bytes()
expected_clear = 'c9235254d396661d26fc793e74c1d68282af2790'
candidates = [part1 + b'\n' + part2, part1 + b'\n' + part2 + b'\n', part1 + part2, part1 + part2 + b'\n']
for candidate in candidates:
    if git_blob_sha(candidate) == expected_clear:
        (app / 'src/clear-result-ui.mjs').write_bytes(candidate)
        break
else:
    raise SystemExit('CLEAR_RESULT_RECONSTRUCTION_SHA_MISMATCH')

p = app / 'src/app.mjs'
text = p.read_text(encoding='utf-8')
old = 'let stagePageAnchor = 1;\n'
new = 'let stagePageAnchor = 1;\nlet persistentRetry = null;\n'
if text.count(old) != 1:
    raise SystemExit('APP_STAGE_ANCHOR_REPLACEMENT_COUNT')
text = text.replace(old, new, 1)

anchor = "function resetPuzzle() {\n  runtime = createPuzzleRuntime(current);\n  renderGame();\n}\n\n"
helper = "function gameRetryControl() {\n  if (persistentRetry) return persistentRetry;\n  const retry = button('secondary round-action', '↻', resetPuzzle);\n  retry.setAttribute('aria-label', '현재 스테이지 다시 도전');\n  const label = el('span', 'round-action-label', 'RETRY');\n  const wrap = el('div', 'game-retry-control');\n  Object.assign(wrap.style, {\n    display: 'flex',\n    flexDirection: 'column',\n    alignItems: 'center',\n    gap: '8px',\n  });\n  wrap.append(retry, label);\n  persistentRetry = wrap;\n  return persistentRetry;\n}\n\n"
if text.count(anchor) != 1:
    raise SystemExit('APP_RETRY_ANCHOR_REPLACEMENT_COUNT')
text = text.replace(anchor, anchor + helper, 1)

old = '  screen.append(nav, renderBoard());'
new = '  screen.append(nav, renderBoard(), gameRetryControl());'
if text.count(old) != 1:
    raise SystemExit('APP_RENDER_GAME_REPLACEMENT_COUNT')
text = text.replace(old, new, 1)

old = "  const hint = el('div', 'play-hint', '끝점을 끌어 두 목표에 연결하세요.');\n  const restart = button('secondary round-action', '↻', resetPuzzle);\n  const label = el('span', 'round-action-label', 'RESTART');\n  const restartWrap = el('div', 'round-action-wrap');\n  restartWrap.append(restart, label);\n  screen.append(hint, restartWrap);"
new = "  screen.append(el('div', 'play-hint', '끝점을 끌어 두 목표에 연결하세요.'));"
if text.count(old) != 1:
    raise SystemExit('APP_RESTART_BLOCK_REPLACEMENT_COUNT')
text = text.replace(old, new, 1)
p.write_text(text, encoding='utf-8')

p = app / 'src/polish.mjs'
text = p.read_text(encoding='utf-8')
old = '.linkline-incoming-ui{opacity:0;transform:translateY(4px);pointer-events:none;will-change:opacity,transform}\n.linkline-incoming-ui.is-visible{opacity:1;transform:translateY(0);pointer-events:auto;transition:opacity .22s .04s ease,transform .26s .04s cubic-bezier(.18,.76,.22,1)}'
new = '.linkline-incoming-ui{opacity:0;pointer-events:none;will-change:opacity}\n.linkline-incoming-ui.is-visible{opacity:1;pointer-events:auto;transition:opacity .22s .04s ease}'
if text.count(old) != 1:
    raise SystemExit('POLISH_UI_REPLACEMENT_COUNT')
text = text.replace(old, new, 1)
old = '// Linkline polish v4.3 Stage Select grade rings + smoother NEXT crossfade + one-shot clear celebration + native NEXT + stage-select swipe.'
new = '// Linkline polish v4.4 fixed-position lower UI fade + Stage Select grade rings + smoother NEXT crossfade + one-shot clear celebration + native NEXT + stage-select swipe.'
if text.count(old) != 1:
    raise SystemExit('POLISH_VERSION_REPLACEMENT_COUNT')
text = text.replace(old, new, 1)
if not text.endswith('\n'):
    text += '\n'
p.write_text(text, encoding='utf-8')
