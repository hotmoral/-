# Timing Defense — Monster Roster Extensibility Amendment

Date: 2026-10-22 KST  
Status: **USER-CONFIRMED STRUCTURAL AMENDMENT / V1 COMPATIBILITY CLARIFICATION**

Applies to interpretation of:
`MONSTER_CAPABILITY_CONTRACT_V1.md`

---

# 0. 문제

`MONSTER_CAPABILITY_CONTRACT_V1.md`는 V1에서 다음 9종 ordinary archetype membership을 frozen으로 기록한다.

- GRUNT
- RUNNER
- BRUTE
- SHIELD
- FLYER
- CHARGER
- SPLITTER
- SUPPORTER
- SIEGER

이 표현이 **게임 lifetime ordinary roster가 영구히 9종으로 제한된다**는 뜻으로 읽히면 현재 사용자 확정 방향과 충돌한다.

---

# 1. Clarified meaning

`roster membership: 9 ordinary archetypes`의 의미는:

> **Monster Capability Contract V1이 보장하는 initial mechanically-authoritative ordinary roster는 위 9종이다.**

의미하지 않는 것:

> Timing Defense의 lifetime/final roster가 반드시 9종으로 끝난다.

즉:

```text
V1 roster = fixed 9
lifetime roster cap = OPEN / EXTENSIBLE
```

기존 9종 ID/role/state-machine contract는 그대로 유지한다.

---

# 2. Future ordinary monster addition

새 monster archetype 추가는 허용한다.

추가 시 요구:
1. 기존 archetype과 다른 player decision을 만들어야 함
2. 단순 +HP / +speed 복제품 금지
3. no hard class lockout
4. current core targeting model을 몰래 변경하지 않음
5. gameplay state는 server authoritative
6. exceptional behavior는 readable telegraph 필요
7. uncontrolled recursion/buff stacking 금지
8. deterministic simulation 가능

필요 시:
- `Monster Capability Contract V2`
- 또는 별도 additive capability amendment
로 canonicalize한다.

---

# 3. Campaign introduction default

Future monster는 기본적으로 **새로운 higher Tier / expansion content**에서 도입하는 것을 우선한다.

이유:
- new Tier novelty 강화
- 기존 clear/star/title achievement 의미 보존
- 기존 campaign balance migration 비용 감소

Existing Tier retrofit은 금지하지 않지만 다음을 요구한다.
- campaign data version bump
- old/new progression semantics 검토
- star/title/achievement 의미 변화 검토
- deterministic regression simulation

---

# 4. Data-model requirement

금지:
```text
monsterCount = 9
array[9]
fixed columns GRUNT..SIEGER as lifetime schema
```

권장:
```text
MonsterRegistry(version)
Tier.availableMonsterIds[]
Tier.introducedMonsterIds[]
Encounter.composition[].monsterId
```

현재 9종은 registry initial set이다.

---

# 5. Pressure taxonomy extensibility

현재 pressure families:
BASELINE / FLOOD / RUSH / BULWARK / BREACH / AERIAL / REPLICATE / SUPPORT / SIEGE

Future monster를 억지로 기존 family에 넣지 않는다.

새 capability가 독립적인 player problem을 만들면:
- pressure taxonomy version-up
- new family or orthogonal axis 추가
를 허용한다.

---

# 6. Compatibility rule

이 amendment는 기존 V1 9종의 역할/상태기계/서버권위 contract를 변경하지 않는다.

변경하는 것은 단 하나다.

> **V1의 9종 고정을 lifetime roster cap으로 해석하지 않는다.**

Campaign authoring은 향후 monster/Tier expansion을 전제로 설계한다.
