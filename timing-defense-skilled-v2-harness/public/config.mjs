export const HUMAN_COLLECTION_ENABLED = false;
export const RUNTIME_MODE = 'PRE_HUMAN_VALIDATION';
export const EXPORT_ELIGIBILITY = 'TECHNICAL_VALIDATION_ONLY';
export const PROTOCOL_VERSION = '0.1';
export const PRESENTATION_VERSION = 'A3P_HUMAN_CANDIDATE_0_3';
export const EVENT_SCHEMA_VERSION = '1.0.0';
export const ORDER_PLAN_VERSION = '0.1.0';
export const MECHANIC_BASELINE = 'a2-v1.0.0';
export const CALIBRATION_MANIFEST_FINGERPRINT = '2c3615516ad5caea431ec98bc1ec985a1dd6996d17c013c8e0fabe047932c2b1';
export const ORDER_PLAN_FINGERPRINT = 'd6a47992395e0afb654b1c5d6eaa0a42b1ee52dba46becb5ec35d0c9051f6667';
export const PILOT_BUNDLE_FINGERPRINT = 'e57112fcf2ebef769883dfa7369862c4d6be8cdba7bf11d30bc5c21dc7da26ec';
export const WARMUP_CONTRACT = 'LINKLINE_A3_PRE_HUMAN_WARMUP_GOLDEN@0.1.0';

export const WARMUPS = Object.freeze([
  Object.freeze({
    id:'WARMUP-1', n:3, length:3,
    initial:Object.freeze([0,1,2]), targets:Object.freeze([1,3]),
    guidedEndpointCell:0, guidedDestination:3,
    label:'연습 1/3 — 왼쪽 끝을 잡고 표시되는 목표 칸 쪽으로 끌어 보세요.'
  }),
  Object.freeze({
    id:'WARMUP-2', n:3, length:3,
    initial:Object.freeze([0,1,2]), targets:Object.freeze([1,5]),
    guidedEndpointCell:2, guidedDestination:5,
    label:'연습 2/3 — 이번에는 반대쪽 끝을 잡고 목표 칸 쪽으로 끌어 보세요.'
  }),
  Object.freeze({
    id:'WARMUP-3', n:3, length:3,
    initial:Object.freeze([0,1,2]), targets:Object.freeze([0,6]),
    guidedEndpointCell:null, guidedDestination:null,
    label:'연습 3/3 — 안내 없이 끝점을 잡아 끌어 두 끝을 목표 칸에 놓아 보세요.'
  })
]);

export const PARTICIPANT_COPY = Object.freeze({
  goalTitle:'목표',
  goal:'연결된 줄의 두 끝을 두 목표 칸에 하나씩 놓으면 문제가 해결됩니다. 어느 끝이 어느 목표 칸에 들어가도 됩니다.',
  howTitle:'움직이는 방법',
  how:'줄의 두 끝 중 하나를 손가락으로 잡고 원하는 방향으로 끌어 보세요. 인접한 빈칸을 지나갈 때마다 줄 전체가 한 칸씩 따라 움직입니다. 손을 떼지 않고 방향을 꺾어 계속 움직일 수 있습니다. 끝을 누른 뒤 표시된 칸을 다시 누르는 방식도 사용할 수 있습니다. 목표 칸은 지나가도 됩니다.',
  toolsTitle:'사용할 수 있는 기능',
  tools:'필요하면 처음부터 다시 시작할 수 있습니다. 한 수만 되돌리는 기능은 없습니다. 원하면 현재 문제를 끝내고 다음 단계로 넘어갈 수 있습니다.'
});
