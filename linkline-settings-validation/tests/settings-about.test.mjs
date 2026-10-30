import assert from 'node:assert/strict';
import {
  PRODUCT_APP_NAME,
  PRODUCT_CAMPAIGN_STAGE_TOTAL,
  productAboutInfo,
} from '../src/settings-about.mjs';

assert.equal(PRODUCT_APP_NAME, 'Linkline');
assert.equal(PRODUCT_CAMPAIGN_STAGE_TOTAL, 1300);
assert.deepEqual(productAboutInfo(), {
  appName: 'Linkline',
  campaignStages: 1300,
});

console.log('PASS Settings about metadata matches the canonical Linkline launch campaign');
