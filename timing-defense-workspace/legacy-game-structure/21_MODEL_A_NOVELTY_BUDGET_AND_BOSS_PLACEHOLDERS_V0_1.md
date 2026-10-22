# Timing Defense — Model A Novelty Budget & Boss Placeholders V0.1

Date: 2026-10-22 KST  
Status: **STRUCTURAL CANDIDATE / NO BOSS OR NUMERIC FREEZE**

Depends on:
- `16_MASTER_CAMPAIGN_PROGRESSION_SPINE_V0_1.md`
- `17_MASTER_CAMPAIGN_MATRIX_V0_1.md`
- `19_MODEL_A_B_CLASS_ROLE_AND_VOLUME_AUDIT_V0_1.md`
- `20_LV31_MASTERY_PLAY_WINDOW_V0_1.md`

---

# 0. 목적

Model A(`T1..T4 + open-ended T5+`)가 단순히 몬스터를 3/2/2/2종으로 나눈 구조에 머물지 않도록, 각 Tier가 감당할 **전체 novelty budget**을 정의한다.

Novelty는 다음을 포함한다.
- new ordinary monster capability
- returning monster reinterpretation
- formation grammar
- cadence grammar
- boss-specific grammar
- run skill power spike
- first-time class-skill learning
- meta progression feedback

원칙:
> Tier는 새 요소가 있어야 하지만, 새 요소를 한 구간에 몰아서 읽을 수 없게 만들면 안 된다.

---

# 1. Novelty의 두 종류를 분리한다

## 1.1 Pedagogic novelty
플레이어가 **처음 배우는 규칙**.

예:
- 처음 만나는 CHARGER windup
- 처음 만나는 SPLITTER death→children
- 한 직업 T1에서 처음 경험하는 Lv11 skill

## 1.2 Power novelty
이미 아는 규칙이지만 이번 run에서 다시 unlock되어 전투력이 크게 변하는 순간.

예:
- 같은 직업 T3에서 Lv21이 다시 활성화
- Lv31 획득 후 후반 전투력이 상승

중요:
- T1에서 class skill milestones는 pedagogic novelty가 될 수 있다.
- T2+에서는 같은 skill milestone이 대부분 power novelty다.
- 따라서 `new monster + familiar skill unlock`은 자동으로 학습 과부하가 아니다.
- 하지만 power spike가 새 monster 난도를 가려버리는 calibration collision은 별도로 검사한다.

---

# 2. Model A novelty budget summary

| Tier | New ordinary | Primary new combat vocabulary | Formation/cadence novelty | Boss novelty allowance | Main risk |
|---|---:|---|---|---|---|
| T1 | 3 | baseline / sustained speed / raw durability | basic line/cluster/wave | LOW | class-skill learning + onboarding density |
| T2 | 2 | mitigation / vertical geometry | durable screen / air offset / stagger | LOW–MED | geometry attribution |
| T3 | 2 | telegraphed burst / population transform | burst / late insert / replication cluster | LOW–MED | two stateful mechanics |
| T4 | 2 | formation support / ranged objective pressure | screen-backline / escort / bounded overlap | LOW | highest learning-density risk |

`LOW/MED`는 boss difficulty가 아니라 **새 boss-only rule을 얼마나 허용할지**의 budget이다.

---

# 3. T1 novelty budget

Available ordinary:
- GRUNT
- RUNNER
- BRUTE

T1은 몬스터 수는 적지만 다른 의미의 학습량이 가장 크다.

## Pedagogic load
- core timing loop
- combo/heavy grammar
- class identity
- Lv6/11/16/21/26/31 first-time class skill understanding
- GRUNT baseline
- RUNNER tempo
- BRUTE durability/control-resistance
- basic formation/cadence reading
- first star-result experience

따라서 T1에 추가 boss-only mechanic을 많이 넣지 않는다.

### T1 boss budget
기본 후보:
- Stage10: checkpoint, boss 필수 아님
- Stage30: synthesis checkpoint, boss-specific 신규 규칙 없음이 기본
- Stage50: first Tier final / boss candidate

Stage50 boss가 존재하더라도 T1에서는:
- 이미 배운 movement/telegraph/formation grammar를 확대하여 사용
- 완전히 새로운 필수 해법을 요구하지 않음

T1 final은 `첫 boss라서 새 규칙 3개`가 아니라 `배운 것을 boss context에서 종합`하는 방향을 우선한다.

Verdict: **T1 novelty budget = PASS candidate, boss novelty intentionally low.**

---

# 4. T2 novelty budget

New ordinary:
- SHIELD
- FLYER

Primary novelty:
- mitigation과 raw durability의 구분
- authoritative Y/spatial geometry
- ground/air relationship

Returning reinterpretation:
- BRUTE + SHIELD durability contrast
- RUNNER + FLYER tempo/geometry contrast

Formation/cadence:
- durable-front line
- AIR_OFFSET
- STAGGER candidate

### Boss allowance
T2부터 boss-specific signature를 하나 둘 수 있으나:
- Stage50에서 처음 공개하지 않는다.
- unique signature가 실제 decision을 바꾼다면 Stage30 전후의 preview/elite slot에서 낮은 강도로 먼저 노출한다.

Candidate grammar:
```text
Stage30: BOSS_SIGNATURE_PREVIEW (optional)
Stage50: BOSS_SIGNATURE_MASTERY
```

정확한 boss 유형/수치는 OPEN.

Verdict: **PASS candidate.**

---

# 5. T3 novelty budget

New ordinary:
- CHARGER
- SPLITTER

Primary novelty:
- telegraph → interruptible burst
- death → deterministic population transformation

둘 다 stateful mechanic이므로 T2보다 학습비용이 높다.

Formation/cadence:
- burst window
- late insert
- replication cluster
- target-order reset after split

### Boss allowance
T3는 ordinary novelty가 이미 높다.
Boss가 새로운 복잡 state machine을 추가하는 것을 기본값으로 하지 않는다.

허용 candidate:
- known telegraph grammar의 boss-scale 변형
- Stage30에서 preview 가능한 한 개의 signature

금지 candidate:
- Stage50에서만 처음 보는 다단계 boss rule 여러 개
- CHARGER/SPLITTER 학습과 무관한 별도 puzzle layer를 final에 갑자기 추가

Verdict: **PASS/WATCH — stateful novelty separation required.**

---

# 6. T4 novelty budget

New ordinary:
- SUPPORTER
- SIEGER

Primary novelty:
- screened formation amplification
- ranged objective/wall pressure

둘 다:
- backline-oriented
- target-order sensitive
- uptime-based difficulty

이므로 Model A의 가장 큰 novelty risk다.

## Required separation
```text
early/first half: SUPPORTER isolated teach/mix
later/second half: SIEGER isolated teach/mix
31+: combined formation/objective pressure
```

### T4 boss novelty budget
**LOW by default.**

이유:
- SUPPORTER + SIEGER synergy 자체가 충분한 late-campaign novelty다.
- Stage41~45에는 Lv31 acquisition이 겹친다.

T4 final boss는:
- completely new boss-only rule보다
- 이미 배운 support/siege/screen/objective vocabulary의 composition mastery
를 우선한다.

필요한 boss signature가 있다면 Stage30 이전/부근에 반드시 preview한다.

Verdict: **WATCH but structurally viable.**

---

# 7. Boss placeholder contract V0.1

Boss cadence 자체는 아직 freeze하지 않는다.
다만 campaign authoring이 사용할 placeholder semantics를 정의한다.

## CHECKPOINT_A — Stage10
- boss optional
- 1~9 학습 확인
- boss novelty introduction 금지에 가까운 기본값

## BOSS_PREVIEW_SLOT — around Stage30
- optional
- Stage50 boss가 unique decision grammar를 가진다면 여기서 낮은 강도로 preview
- preview 없이 Stage50에서 필수 boss grammar를 처음 던지는 것을 경고

## TIER_FINAL_SLOT — Stage50
- boss candidate / final composition
- Tier identity 종합
- Lv31은 이미 익숙한 상태를 전제
- 처음 보는 core ordinary capability 금지
- unpreviewed mandatory boss-only mechanic 금지

---

# 8. Boss novelty와 monster novelty의 관계

Boss는 ordinary roster를 대체하는 `10번째 ordinary monster`가 아니다.
Boss-specific grammar는 별도 layer다.

원칙:
1. Tier의 ordinary novelty가 높을수록 boss-only novelty budget은 낮춘다.
2. boss novelty가 실제 판단 규칙을 바꾸면 preview를 제공한다.
3. final boss는 난도가 높을 수 있지만 낯선 규칙 때문에만 어려워서는 안 된다.
4. boss visual spectacle과 gameplay novelty를 구분한다. 시각적 새로움은 높아도 gameplay rule novelty는 낮게 유지할 수 있다.

---

# 9. Novelty overload warning rules

다음은 static warning:
- 같은 3-Stage window에서 두 개 이상의 unpreviewed major mechanics 최초 도입
- new stateful monster first-teach와 new boss-only mechanic 동시 도입
- T1에서 new monster + first-time major class skill + boss rule이 같은 짧은 window에 중첩
- T4 Stage41~45에서 SUPPORTER/SIEGER first-teach + Lv31 first acquisition 동시 발생

T4에서는 SUPPORTER/SIEGER first-teach를 Stage30 이전에 끝내는 것이 기본 guardrail이다.

---

# 10. Model A 결과

Static novelty verdict:
- T1: PASS with low boss novelty
- T2: PASS
- T3: PASS/WATCH
- T4: WATCH, not FAIL

Model A는 novelty budget 관점에서 폐기할 이유가 없다.
다음 검증은:
- exact skill reach window
- skill/monster collision audit
- SKILLED_V2 measurement
- meta/star progression envelope
와 함께 수행한다.
