# Timing Defense — Layer-0 Model A Validation Report V0.1

Date: 2026-10-22 KST  
Status: **VALIDATION REPORT / STRUCTURE ONLY**

Inputs:
- `data/model_a_campaign_spine_v0_1.yaml`
- `tools/validate_campaign_spine.py`

---

# 0. 목적

Model A의 상위 campaign spine이 문서 간 정성 검토뿐 아니라 machine-readable constraint에서도 모순 없는지 확인한다.

---

# 1. Validation scope

검사 항목:
- initial Tier count
- skill reach window order/range
- Lv31 Stage41–45 contract
- late-band ordering
- cumulative monster availability
- duplicate/unknown monster introduction
- future monster extensibility
- firstTeach/firstMixed/firstHighPressure ordering
- Stage40+ first-teach 금지
- first-high-pressure vs skill-power attribution collision warning
- skilled clear upper-bound configuration
- star outcome contract
- Stage50 unpreviewed mandatory boss mechanic policy
- future pressure-taxonomy versioning

게임 수치/실제 clear rate는 이 검사의 범위가 아니다.

---

# 2. Initial precheck

최초 machine-readable candidate에서 structural ERROR는 없었으나 다음 attribution WATCH가 검출됐다.

- T1 BRUTE first-high-pressure가 Lv21 reach window에 너무 근접
- T4 SUPPORTER first-high-pressure가 Lv26 reach window에 너무 근접
- GRUNT baseline pressure는 capability novelty가 아니므로 generic collision rule의 false positive

조치:
- T1 BRUTE firstHighPressure `24–29 -> 21–23`
- T4 SUPPORTER firstHighPressure `31–33 -> 29–31`
- GRUNT baseline은 capability-attribution collision 검사에서 exempt

이 변경은 exact Stage recipe freeze가 아니라 simulation window refinement다.

---

# 3. Revised validation result

Current local validation result against the revised candidate:

```text
RESULT=PASS errors=0 warnings=0
```

즉 현재 Layer-0 규칙에서:
- hard structural contradiction 없음
- known attribution warning 없음

---

# 4. What PASS means

PASS는 다음을 뜻한다.
- Model A가 deterministic campaign simulation input으로 내려갈 수 있음
- 상위 구조가 machine-readable 형태로 일관됨

PASS가 뜻하지 않는 것:
- Model A production freeze
- 4 Tier final 확정
- monster count/HP 확정
- exact Stage recipe 확정
- skill EXP formula 확정
- boss design 확정
- star/achievement reward 확정

---

# 5. Current machine-readable contract summary

```text
Initial candidate: T1..T4
Lifetime tiers: open-ended
T1: G/R/B
T2: +SH/F
T3: +C/SP
T4: +SUP/SI
T5+: future expansion

Lv6  5–7
Lv11 11–14
Lv16 18–21
Lv21 25–28
Lv26 32–36
Lv31 41–45

40     2★ gate
41–45  Lv31 Ascension
46–49  post-Lv31 mastery
50     Tier Final

non-T1 SKILLED_V2_CENTRAL full-clear <60%
```

---

# 6. Remaining simulation-only risks

Layer-0 cannot resolve:
- T4 SUPPORTER/SIEGER actual readability
- actual skilled clear probabilities
- Lv31 power cliff
- class-specific soft walls
- Stage fail histogram
- stars/permanent-stat snowball
- SPLITTER effective entity volume
- SIEGER/SUPPORTER uptime
- actual boss difficulty

These move to lower simulation layers.

---

# 7. Verdict

**LAYER-0 MODEL A STRUCTURE VALIDATION = PASS**

Model A is admitted as the current default bounded simulation spine.
Model B remains fallback if T4 lower-layer testing fails.
