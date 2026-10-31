export const PRODUCT_SETTINGS_SCHEMA = 'LINKLINE_PRODUCT_SETTINGS';
export const PRODUCT_SETTINGS_VERSION = 1;
export const PRODUCT_SETTINGS_STORAGE_KEY = 'linkline.product.settings.v1';
export const PRODUCT_PROGRESS_STORAGE_KEY = 'linkline.product.progress.v3';

export function initialProductSettings() {
  return {
    schema: PRODUCT_SETTINGS_SCHEMA,
    version: PRODUCT_SETTINGS_VERSION,
    vibration: true,
    sound: true,
  };
}

function normalizeProductSettings(value) {
  const initial = initialProductSettings();
  if (!value || typeof value !== 'object') return initial;
  if (value.schema !== PRODUCT_SETTINGS_SCHEMA || value.version !== PRODUCT_SETTINGS_VERSION) return initial;
  return {
    ...initial,
    vibration: typeof value.vibration === 'boolean' ? value.vibration : initial.vibration,
    sound: typeof value.sound === 'boolean' ? value.sound : initial.sound,
  };
}

export function loadProductSettings(storage) {
  try {
    const raw = storage?.getItem?.(PRODUCT_SETTINGS_STORAGE_KEY);
    if (!raw) return initialProductSettings();
    return normalizeProductSettings(JSON.parse(raw));
  } catch {
    return initialProductSettings();
  }
}

export function saveProductSettings(storage, settings) {
  const next = normalizeProductSettings({
    ...initialProductSettings(),
    ...settings,
    schema: PRODUCT_SETTINGS_SCHEMA,
    version: PRODUCT_SETTINGS_VERSION,
  });
  try {
    storage?.setItem?.(PRODUCT_SETTINGS_STORAGE_KEY, JSON.stringify(next));
  } catch {}
  return next;
}

export function setProductSetting(storage, key, value) {
  if (!['vibration', 'sound'].includes(key)) throw new Error(`UNKNOWN_PRODUCT_SETTING:${key}`);
  const current = loadProductSettings(storage);
  return saveProductSettings(storage, { ...current, [key]: Boolean(value) });
}

export function summarizePerformanceRecords(progress) {
  const summary = { completed: 0, sPlus: 0, aPlus: 0, bPlus: 0 };
  if (!progress || typeof progress !== 'object' || Array.isArray(progress)) return summary;
  if (Number.isInteger(progress.highestCleared) && progress.highestCleared > 0) {
    summary.completed = progress.highestCleared;
  }
  if (!progress.performance || typeof progress.performance !== 'object' || Array.isArray(progress.performance)) return summary;
  for (const record of Object.values(progress.performance)) {
    if (!record || typeof record !== 'object' || Array.isArray(record)) continue;
    if (record.grade === 'S+') summary.sPlus += 1;
    if (record.grade === 'A+') summary.aPlus += 1;
    if (record.grade === 'B+') summary.bPlus += 1;
  }
  return summary;
}

export function loadPerformanceSummary(storage) {
  try {
    const raw = storage?.getItem?.(PRODUCT_PROGRESS_STORAGE_KEY);
    if (!raw) return summarizePerformanceRecords(null);
    const progress = JSON.parse(raw);
    if (progress?.schema !== 'LINKLINE_PRODUCT_PROGRESS' || progress?.version !== 3) {
      return summarizePerformanceRecords(null);
    }
    return summarizePerformanceRecords(progress);
  } catch {
    return summarizePerformanceRecords(null);
  }
}

let browserSettings = initialProductSettings();
let nativeVibrate = null;
let vibrationGateInstalled = false;
let audioContext = null;

function browserStorage() {
  try {
    return globalThis.localStorage ?? null;
  } catch {
    return null;
  }
}

function readBrowserSettings() {
  browserSettings = loadProductSettings(browserStorage());
  return browserSettings;
}

function installVibrationGate() {
  const nav = globalThis.navigator;
  if (!nav || typeof nav.vibrate !== 'function' || vibrationGateInstalled) return;
  nativeVibrate = nav.vibrate.bind(nav);
  const gatedVibrate = (pattern) => {
    if (!browserSettings.vibration) return false;
    return nativeVibrate(pattern);
  };

  try {
    Object.defineProperty(nav, 'vibrate', {
      configurable: true,
      writable: true,
      value: gatedVibrate,
    });
    vibrationGateInstalled = true;
    return;
  } catch {}

  try {
    const proto = Object.getPrototypeOf(nav);
    const descriptor = Object.getOwnPropertyDescriptor(proto, 'vibrate');
    if (!descriptor?.configurable || typeof descriptor.value !== 'function') return;
    Object.defineProperty(proto, 'vibrate', {
      ...descriptor,
      value: gatedVibrate,
    });
    vibrationGateInstalled = true;
  } catch {}
}

function ensureAudioContext() {
  if (!browserSettings.sound) return null;
  const AudioContextCtor = globalThis.AudioContext ?? globalThis.webkitAudioContext;
  if (typeof AudioContextCtor !== 'function') return null;
  try {
    audioContext ??= new AudioContextCtor();
    if (audioContext.state === 'suspended') audioContext.resume?.();
    return audioContext;
  } catch {
    return null;
  }
}

function playClearSound() {
  if (!browserSettings.sound) return false;
  const context = ensureAudioContext();
  if (!context) return false;

  try {
    const now = context.currentTime;
    const oscillator = context.createOscillator();
    const gain = context.createGain();
    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(560, now);
    oscillator.frequency.exponentialRampToValueAtTime(760, now + 0.07);
    oscillator.frequency.exponentialRampToValueAtTime(920, now + 0.15);
    gain.gain.setValueAtTime(0.0001, now);
    gain.gain.exponentialRampToValueAtTime(0.045, now + 0.012);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.18);
    oscillator.connect(gain);
    gain.connect(context.destination);
    oscillator.start(now);
    oscillator.stop(now + 0.19);
    return true;
  } catch {
    return false;
  }
}

function ensureStyles() {
  if (document.querySelector('#linkline-settings-preferences-style')) return;
  const style = document.createElement('style');
  style.id = 'linkline-settings-preferences-style';
  style.textContent = `
.settings-preferences-card{display:grid}
.settings-preference-block{display:grid}
.settings-preference-block+.settings-preference-block{margin-top:24px;padding-top:24px;border-top:1px solid rgba(23,23,22,.12)}
.settings-preference-title{margin-top:9px;font-size:24px;font-weight:430;letter-spacing:0}
.settings-preference-help{margin:16px 0 22px;color:#77736d;font-size:13px;line-height:1.65}
.settings-toggle-outline{width:100%;min-height:50px;border-radius:999px;background:transparent;border:1px solid rgba(23,23,22,.30);color:#625f59;font-size:11px;font-weight:560;letter-spacing:.14em;touch-action:manipulation}
.settings-toggle-outline[aria-checked="true"]{border-color:rgba(18,104,255,.52);color:var(--blue)}
.settings-toggle-outline:active{background:rgba(23,23,22,.035)}
.settings-toggle-outline[aria-checked="true"]:active{background:rgba(18,104,255,.045)}
.settings-record-summary{display:grid;grid-template-columns:repeat(3,1fr);margin:18px 0 4px;border-top:1px solid rgba(23,23,22,.12);border-bottom:1px solid rgba(23,23,22,.12)}
.settings-record-stat{min-width:0;padding:16px 8px 15px;text-align:center}
.settings-record-stat+.settings-record-stat{border-left:1px solid rgba(23,23,22,.12)}
.settings-record-grade{font-size:10px;font-weight:620;letter-spacing:.16em;color:#77736d}
.settings-record-count{margin-top:7px;font-size:22px;font-weight:430;font-variant-numeric:tabular-nums}
.settings-record-stat[data-grade="S+"] .settings-record-grade{color:#a88424}
.settings-record-stat[data-grade="A+"] .settings-record-grade{color:#818890}
.settings-record-stat[data-grade="B+"] .settings-record-grade{color:#9e653f}
`;
  document.head.append(style);
}

function syncSettingToggle(toggle, key, label) {
  const enabled = Boolean(browserSettings[key]);
  toggle.setAttribute('aria-checked', enabled ? 'true' : 'false');
  toggle.textContent = `${label} ${enabled ? 'ON' : 'OFF'}`;
}

function createPreferenceBlock({ key, title, help, ariaLabel, buttonLabel }) {
  const block = document.createElement('div');
  block.className = 'settings-preference-block';

  const titleNode = document.createElement('div');
  titleNode.className = 'settings-preference-title';
  titleNode.textContent = title;

  const helpNode = document.createElement('p');
  helpNode.className = 'settings-preference-help';
  helpNode.textContent = help;

  const toggle = document.createElement('button');
  toggle.type = 'button';
  toggle.className = 'settings-toggle-outline';
  toggle.dataset.settingKey = key;
  toggle.setAttribute('role', 'switch');
  toggle.setAttribute('aria-label', ariaLabel);
  toggle.addEventListener('click', () => {
    browserSettings = setProductSetting(browserStorage(), key, !browserSettings[key]);
    syncSettingToggle(toggle, key, buttonLabel);
    if (key === 'vibration' && browserSettings.vibration) {
      try { globalThis.navigator?.vibrate?.(18); } catch {}
    }
    if (key === 'sound' && browserSettings.sound) playClearSound();
  });

  block.append(titleNode, helpNode, toggle);
  return block;
}

function createRecordStat(grade, count) {
  const stat = document.createElement('div');
  stat.className = 'settings-record-stat';
  stat.dataset.grade = grade;
  const label = document.createElement('div');
  label.className = 'settings-record-grade';
  label.textContent = grade;
  const value = document.createElement('div');
  value.className = 'settings-record-count';
  value.textContent = String(count);
  stat.append(label, value);
  return stat;
}

function decorateProgressSummary(progressCard) {
  let summaryNode = progressCard.querySelector('.settings-record-summary');
  if (!summaryNode) {
    summaryNode = document.createElement('div');
    summaryNode.className = 'settings-record-summary';
    summaryNode.setAttribute('aria-label', '최고 등급 기록 요약');
    const copy = progressCard.querySelector('.settings-copy');
    progressCard.insertBefore(summaryNode, copy ?? progressCard.querySelector('.danger-outline'));
  }

  const summary = loadPerformanceSummary(browserStorage());
  summaryNode.replaceChildren(
    createRecordStat('S+', summary.sPlus),
    createRecordStat('A+', summary.aPlus),
    createRecordStat('B+', summary.bPlus),
  );
}

function renderSettingsPreferenceCard() {
  const screen = document.querySelector('#screen');
  if (!screen?.classList.contains('view-settings')) return;
  ensureStyles();

  const progressCard = screen.querySelector('.settings-card:not(.settings-preferences-card)');
  if (!progressCard) return;
  decorateProgressSummary(progressCard);

  let card = screen.querySelector('.settings-preferences-card');
  if (!card) {
    card = document.createElement('section');
    card.className = 'settings-card settings-preferences-card';
    card.dataset.settingsPreferences = 'true';

    const label = document.createElement('div');
    label.className = 'settings-label';
    label.textContent = 'FEEDBACK';

    const vibration = createPreferenceBlock({
      key: 'vibration',
      title: 'Vibration',
      help: '스테이지 클리어 시 진동 피드백을 사용합니다.',
      ariaLabel: '진동',
      buttonLabel: 'VIBRATION',
    });

    const sound = createPreferenceBlock({
      key: 'sound',
      title: 'Sound',
      help: '스테이지 클리어 시 짧은 효과음을 재생합니다.',
      ariaLabel: '효과음',
      buttonLabel: 'SOUND',
    });

    card.append(label, vibration, sound);
    screen.insertBefore(card, progressCard);
  }

  for (const toggle of card.querySelectorAll('.settings-toggle-outline')) {
    const key = toggle.dataset.settingKey;
    if (key === 'vibration') syncSettingToggle(toggle, key, 'VIBRATION');
    if (key === 'sound') syncSettingToggle(toggle, key, 'SOUND');
  }
}

function maybePlayClearSound(event) {
  if (!event.target.closest?.('.cell')) return;
  const success = document.querySelector('#screen .success-panel');
  if (!success || success.dataset.linklineSoundPlayed === 'true') return;
  success.dataset.linklineSoundPlayed = 'true';
  playClearSound();
}

function installBrowserSettings() {
  readBrowserSettings();
  installVibrationGate();
  const screen = document.querySelector('#screen');
  if (!screen) return;
  const observer = new MutationObserver(renderSettingsPreferenceCard);
  observer.observe(screen, { childList: true, attributes: true, attributeFilter: ['class'] });
  document.addEventListener('pointerdown', () => { if (browserSettings.sound) ensureAudioContext(); }, { passive: true });
  document.addEventListener('keydown', () => { if (browserSettings.sound) ensureAudioContext(); });
  document.addEventListener('click', maybePlayClearSound);
  queueMicrotask(renderSettingsPreferenceCard);
}

if (typeof document !== 'undefined') installBrowserSettings();
