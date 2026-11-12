export const PRODUCT_APP_NAME = 'Linkline';
export const PRODUCT_CAMPAIGN_STAGE_TOTAL = 1300;

export function productAboutInfo() {
  return {
    appName: PRODUCT_APP_NAME,
    campaignStages: PRODUCT_CAMPAIGN_STAGE_TOTAL,
  };
}

function renderSettingsAboutCard() {
  const screen = document.querySelector('#screen');
  if (!screen?.classList.contains('view-settings')) return;
  if (screen.querySelector('.settings-about-card')) return;

  const progressCard = [...screen.querySelectorAll('.settings-card')].find((card) =>
    !card.classList.contains('settings-preferences-card') &&
    !card.classList.contains('settings-about-card'));
  if (!progressCard) return;

  const info = productAboutInfo();
  const card = document.createElement('section');
  card.className = 'settings-card settings-about-card';
  card.setAttribute('aria-label', '앱 정보');

  const label = document.createElement('div');
  label.className = 'settings-label';
  label.textContent = 'ABOUT';

  const name = document.createElement('div');
  name.className = 'settings-value';
  name.textContent = info.appName;

  const copy = document.createElement('p');
  copy.className = 'settings-copy';
  copy.textContent = `정식 캠페인 · ${info.campaignStages.toLocaleString('en-US')} stages`;

  card.append(label, name, copy);
  progressCard.insertAdjacentElement('afterend', card);
}

function installSettingsAbout() {
  const screen = document.querySelector('#screen');
  if (!screen) return;
  const observer = new MutationObserver(renderSettingsAboutCard);
  observer.observe(screen, { childList: true, subtree: true, attributes: true, attributeFilter: ['class'] });
  queueMicrotask(renderSettingsAboutCard);
}

if (typeof document !== 'undefined') installSettingsAbout();
