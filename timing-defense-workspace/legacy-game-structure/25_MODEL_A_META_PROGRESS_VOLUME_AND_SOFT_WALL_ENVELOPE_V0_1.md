# Timing Defense — Model A Meta Progression Volume & Soft-Wall Envelope V0.1

Date: 2026-10-22 KST  
Status: **STRUCTURAL/SENSITIVITY ANALYSIS / NO STAR VALUE FREEZE**

Depends on:
- `01_META_PROGRESSION.md`
- `17_MASTER_CAMPAIGN_MATRIX_V0_1.md`
- `24_SKILLED_V2_MEASUREMENT_PROTOCOL_V0_1.md`

---

# 0. 목적

Model A(4 initial Tiers)에서 desired difficulty(`<60% skilled full clear`)와 별 기반 cross-class progression이 서로 충돌하지 않는지 구조적으로 검토한다.

핵심:
> full-clear probability 하나만 보면 안 된다. **어디서 실패하는지**가 별 획득과 다음 직업 성장에 직접 영향을 준다.

---

# 1. Model A fixed volume floor

4 initial Tiers × 5 classes × 50 Stages:

```text
20 class×Tier records
1000 successful Stage clears minimum if every record clears once
Max stars = 60★
```

실제 play volume은 실패/retry 때문에 더 크다.

---

# 2. Full-clear sensitivity recap

단순 geometric comparison:

| Full-clear q | Expected full attempts for 20 clears |
|---:|---:|
| .59 | 33.9 |
| .55 | 36.4 |
| .50 | 40.0 |
| .45 | 44.4 |
| .40 | 50.0 |

이 값은 실제 Stage play volume이 아니라 full-attempt count 비교용이다.

---

# 3. Failure location matters more than q alone

Outcome buckets:
- p0 = fail Stage1–19 = 0★
- p1 = fail Stage20–39 = 1★
- p2 = fail Stage40–49 = 2★
- p3 = Stage50 clear = 3★

```text
p0+p1+p2+p3=1
```

같은 p3라도 p0/p1/p2 분포가 다르면:
- first-attempt stars
- retry motivation
- cross-class permanent growth
- blocked-class recovery
가 완전히 달라진다.

---

# 4. Sensitivity examples — NOT production targets

아래는 구조 이해를 위한 synthetic distributions이다.

## LATE_WALL
```text
p0=.05 / p1=.15 / p2=.35 / p3=.45
```

## BALANCED_HARD
```text
p0=.10 / p1=.20 / p2=.25 / p3=.45
```

## EARLY_WALL
```text
p0=.25 / p1=.30 / p2=.25 / p3=.20
```

이 값들은 production target이 아니다.

---

# 5. Expected best-stars after repeated attempts

한 class×Tier에서 best star는 max record이므로 n attempts 후:

```text
E[bestStars_n]
= P(max>=1)+P(max>=2)+P(max>=3)
= 3 - p0^n - (p0+p1)^n - (1-p3)^n
```

Sensitivity result:

| Scenario | attempt1 | attempt2 | attempt3 | attempt4 |
|---|---:|---:|---:|---:|
| LATE_WALL | 2.20★ | 2.66★ | 2.83★ | 2.91★ |
| BALANCED_HARD | 2.05★ | 2.60★ | 2.81★ | 2.90★ |
| EARLY_WALL | 1.40★ | 2.00★ | 2.31★ | 2.49★ |

해석:
- 동일하게 어렵더라도 `late wall`은 실패 자체가 account progression에 기여한다.
- early wall은 blocked class가 별도 거의 못 만들고 죽은 경로가 될 수 있다.

---

# 6. Rough Stage-play sensitivity

단순 비교를 위해 failure bucket 평균 도달 Stage를:
- 0★ fail ≈10
- 1★ fail ≈30
- 2★ fail ≈45
- clear=50
으로 놓은 synthetic estimate.

### q=.45 LATE_WALL
- expected fail length ≈37.7 Stages
- expected Stage plays to first clear ≈96.1 per class×Tier

### q=.45 BALANCED_HARD
- expected fail length ≈33.2
- expected Stage plays to first clear ≈90.6

### q=.20 EARLY_WALL
- expected fail length ≈28.4
- expected Stage plays to first clear ≈163.8

20 records 단순 환산은 약:
- 1922
- 1811
- 3275
Stage-play units.

이것은 production prediction이 아니다.
핵심은 **초기 실패율을 높게 만드는 방식으로 난도를 올리면 campaign grind가 폭증할 수 있다**는 점이다.

---

# 7. Soft-wall design principle

원하는 soft wall:
```text
현재 power에서는 Stage40대에서 자주 막힘
 -> 2★ 확보
 -> 다른 class도 진행
 -> global stars / achievements 획득
 -> 다시 돌아옴
 -> Stage50 clear 가능성 상승
```

덜 바람직한 기본형:
```text
특정 class가 매번 Stage12에서 막힘
 -> 0★
 -> 그 class play가 account progression에 기여하지 못함
 -> 다른 class 플레이가 사실상 강제
```

Stage1–19 fail 자체를 금지하는 것은 아니다.
하지만 ordinary soft-wall design의 기본 위치로 쓰지 않는다.

---

# 8. Star-band target philosophy

Exact probability target은 아직 freeze하지 않는다.

그러나 non-T1 intended-entry SKILLED_V2에서 구조적으로 원하는 형태:
- 0★ fail이 압도적 다수가 되지 않음
- 1★ 도달은 의미 있는 baseline progression
- 2★는 숙련/성장으로 자주 보이지만 자동은 아님
- 3★ full clear는 <60%

Soft-wall class는:
- 3★ rate가 다른 class보다 낮아도 됨
- 그러나 reasonable 1★/2★ path가 있어야 함

---

# 9. Tier unlock policy sensitivity — Gate G1

아직 USER-CONFIRMED가 아니므로 두 후보를 분리한다.

## U0 CLEAR_LOCK
```text
Class X Tn Stage50 clear required -> Class X T(n+1) unlock
```

Pros:
- “Tier clear” 의미가 선명
- blocked class로 돌아올 이유 강함
- cross-class permanent growth의 목적과 잘 맞음
- 3★의 의미가 progression과 일치

Cons:
- soft wall이 너무 강하면 해당 class lane 정체

## U1 TWO_STAR_UNLOCK
```text
Class X Tn reaches Stage40+ / 2★ -> next Tier unlock
```

Pros:
- lane deadlock 완화

Cons:
- Stage50/3★를 건너뛰고 다음 Tier로 갈 수 있음
- “막힌 직업을 다른 직업 성장으로 다시 밀어 clear”하는 핵심 루프가 약해질 수 있음
- higher Tier farming으로 lower Tier를 trivialize할 우려

### Current structural recommendation
**U0 CLEAR_LOCK을 first simulation hypothesis로 우선 사용.**

이는 final freeze가 아니다.
Simulation에서 class-lane deadlock이 과하면 U1/other policy를 비교한다.

---

# 10. Cross-class recovery acceptance

Account simulation은 다음 사건을 명시적으로 찾아야 한다.

```text
SOFT_WALL_RECOVERY_EVENT
sourceClass = A
blockedTier = Tn
beforeMeta: fail distribution
otherClassProgress: stars/achievements gained
returnAttempt: clear probability improved
```

성공적인 구조는:
- 다른 직업 진행이 실제로 A를 돕고
- A가 이전 wall을 넘을 확률이 체감되게 상승하며
- 완전히 자동 clear가 되지는 않음
을 만족한다.

---

# 11. Snowball guardrail

반대 극단도 위험하다.

```text
2★/3★ 획득
 -> huge permanent boost
 -> next class trivial
 -> more stars
 -> rest of campaign collapses
```

따라서 permanent reward는:
- 한 wall을 이동시키는 bridge 역할
- 여러 Tier를 통째로 무력화하는 skip 역할 금지

으로 calibration한다.

---

# 12. Model A verdict from meta-volume lens

Model A는 4 Tier만으로도 충분히 큰 base volume을 가진다.
Desired skilled difficulty와 결합할 때 5/6 Tier로 늘리기 전에:
- fail histogram
- star-band distribution
- soft-wall recovery
- retry Stage volume
을 먼저 확인해야 한다.

현재 verdict:
**MODEL A = PASS for bounded simulation / WATCH permanent-reward snowball and unlock policy.**
