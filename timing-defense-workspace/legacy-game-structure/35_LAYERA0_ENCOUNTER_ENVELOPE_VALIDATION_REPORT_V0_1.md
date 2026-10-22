# Timing Defense — Layer-A0 Encounter Envelope Validation Report V0.1

Date: 2026-10-22 KST  
Status: **VALIDATION REPORT / AUTHORING ENVELOPE ONLY**

Inputs:
- `data/model_a_encounter_envelope_v0_1.yaml`
- `tools/validate_encounter_envelope.py`
- `32_MODEL_A_TIER_ENCOUNTER_AVAILABILITY_V0_1.md`
- `33_MODEL_A_FORMATION_CADENCE_VOCABULARY_V0_1.md`
- `34_MODEL_A_FREQUENCY_RANGE_ENVELOPE_V0_1.md`

---

# 0. 목적

Model A encounter envelope가 Tier별 roster unlock, formation/cadence progression, complexity/frequency bounds와 정합적인지 machine-readable constraint로 확인한다.

---

# 1. 검사 범위

- legal archetype cumulative availability
- archetype earliest Tier violation
- unknown archetype/formations/cadences
- formation/cadence regression warning
- pressure label validity
- Stage-dominant complexity range가 50 Stage를 채울 수 있는지
- T4가 current E01–E20 library 전체를 수용하는지
- Lv31 Ascension window Stage41–45 consistency

---

# 2. Initial modeling issue found

초기 validator 가설은 다음을 암묵적으로 동일시했다.

```text
Encounter archetype complexity == Stage dominant complexity
```

이것은 잘못된 모델링이었다.

예:
- E02 C1과 E03 C1을 한 Stage에서 순차/overlap하여 target-order/tempo interaction을 만들면 Stage 전체는 C2로 판정될 수 있다.
- 따라서 T1 legal archetype에 C2 ID가 없어도 T1 Stage dominant C2는 구조적으로 가능하다.

조치:
- encounter-level complexity와 Stage-level dominant complexity를 명시적으로 분리
- exact same complexity archetype 존재 여부를 Stage distribution validation 조건에서 제거

이 수정은 난도를 낮추거나 규칙을 우회한 것이 아니라 **모델 계층을 올바르게 분리한 것**이다.

---

# 3. Revised validation result

Corrected validator 기준:

```text
RESULT=PASS errors=0 warnings=0
```

현재 확인된 사항:
- T1 legal: E01–E03
- T2 legal: 7 archetypes
- T3 legal: 13 archetypes
- T4 legal: current E01–E20 full library
- formation/cadence vocabulary cumulative progression intact
- pressure labels valid
- all Tier complexity ranges feasible for 50 Stage
- Lv31 Ascension Stage41–45 consistent

---

# 4. PASS 의미

PASS는:
- representative deterministic recipe authoring으로 내려갈 수 있음을 뜻함
- Tier unlock 전 archetype leakage를 machine-check할 수 있음을 뜻함

PASS가 뜻하지 않는 것:
- exact encounter frequency production freeze
- exact monster counts freeze
- exact cadence milliseconds freeze
- actual readability PASS
- actual class balance PASS

이들은 representative recipe/static density/Layer-A simulation에서 검증한다.

---

# 5. Next boundary

1. representative recipe set 작성
2. deterministic candidate spawn schedule 부여
3. authored/effective entity count 계산
4. 4s/6s burst density 계산
5. SPLITTER child-volume stress
6. SUPPORTER/SIEGER screened uptime simulation input 생성
7. CHARGER telegraph concurrency 검사
8. Layer-A micro-sim

---

# 6. Verdict

**LAYER-A0 ENCOUNTER ENVELOPE VALIDATION = PASS**

Model A encounter envelope is admitted for representative deterministic recipe authoring.
