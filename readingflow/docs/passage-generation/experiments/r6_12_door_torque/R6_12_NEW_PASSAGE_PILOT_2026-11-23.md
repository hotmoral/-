# R6.12 신규 비문학 1편 종단 시험 — 원고와 오프라인 주입 제공자
작성일 2026-11-23 / 작업 브랜치 feature/author-attribute-rng-audit-20261119

## 실제로 확보한 결과
- 독립 신규 한국어 비문학 1편 **「문손잡이는 왜 경첩에서 멀리 있을까」**, 초등 고학년 L4, 문항 3개/선지 12개/오답 근거 기록 9개를 별도 신규 파일로 제작.
- 글은 이 세션의 대화 AI가 원본으로 작성했다. **OpenAI Responses 실시간 API 호출 결과가 아니다.** 원고를 미리 만든 뒤 오프라인 제공자에서 반환하도록 하여 R6.11 Stage5 -> 생성기 제공자 -> 17 QA의 종단 연결을 확인할 **실행 코드를 추가**했다.
- 세 문항은 **인과 / 비교·조건 / 근거 평가**를 서로 다른 지문 근거로 설계. 정답이 유일 최단 또는 최장인 문항이 없도록 선지 길이 단서를 별도 사전검사해 Q2의 일방적인 길이 단서를 교정했다. Q2는 거리와 방향의 효과가 상충하므로 명시된 수치 없이 어느 쪽 돌림힘이 더 크다고 단정할 수 없다는 결론. 각 오답에 지문 연속 구절과 배제 이유 기록.
- 검증 근거: University of California, Santa Barbara 물리학 시연 소개자료 `https://web.physics.ucsb.edu/~lecturedemonstrations/Composer/Pages/28.18.html`, 설명 본문 단락 1~8. AI가 2026-11-23 웹 대조로 기본 사실 관계를 확인했지만, 사실/출처 레지스트리는 **PENDING_EXTERNAL_REVIEW/NOT_CHECKED_IN_THIS_STAGE** 유지. 독립 사람 검수로 승격 금지.
- 기존 30편·90문항 원고/문항 파일 수정 없음. 신규 원고는 실험 자료로 격리.
- 24속성은 **생성기 진입 시 1회 추출 후 같은 기록을 재사용하도록 기존 코드를 호출**한다. 이번 원고가 해당 추출 속성을 실제 글에 충실히 반영하는지는 검증하지 않았다(정적 제공자 초안이기 때문). 사용자 지정 재추첨 없음.
- 배포/승인/학습자 실측 전부 미완료. 정답 유일성·한국어 어감은 AI 사전 검토일 뿐 독립 검수 승인 아님.

## 파일
- `trial_inputs_v1.json`: 신규 주제/3개 목표/7개 후보 사실/출처 레지스트리. 기존 30편과 주제/근거 의미 중복은 추가 검수.
- `model_authored_output_v1.json`: **원고·3문항·12선지·9오답 근거**. 원고/문항 정본 및 승인 상태와 분리.
- `run_trial.py`: 실제 구현된 R6.11 메서드를 재사용하는 **오프라인 종단 시험 실행 코드**, 먼저 기본 미검증 HOLD, 명시 실험 모드에서 새 원고·문항 주입/17 QA.
- `test_r612_trial.py`: 회귀 검사 5개. 코드만 기록했으며 **GitHub Actions 실패 환경에서 Python 실행 완료를 주장하지 않는다**.

## 재현 명령
```bash
python docs/passage-generation/experiments/r6_12_door_torque/run_trial.py --output /tmp/r612_trial_result.json
cd docs/passage-generation/experiments/r6_12_door_torque
python -m unittest test_r612_trial -v
```

기대 결과는 첫 기본 호출 `HOLD_SOURCE_VERIFICATION`, 다음 명시적 실험 호출 `READY_FOR_EDITORIAL_REVIEW` 또는 구조 결함 시 `REVISE`. 이는 실제 테스트 통과 판정이 아니며 결과와 Python 테스트를 실행해서 확인해야 한다.

## 다음 작업
1. 독립 실행환경에서 위 Python 회귀/실험을 실제 실행하고 오류 시 최소 수정.
2. 생성 직전 추출한 **필자 24속성을 입력으로 실제 생성하는 단계**를 직접 확인. 정적 fixture는 그 속성의 문체 충실도를 입증할 수 없다.
3. 사실 근거 사람 검증/글의 자연스러움/문항 유일성/오답 매력도/중복 검토. 문제가 있으면 **신규 초안 범위에서만** 수정.
4. 사람 승인이 끝나기 전에는 release false, 신규 원고 생산 확대 금지.


## R6.12 추가 검수 (2026-11-23)

[Python QA 실제 실행 및 오답 교정 보고](R6_12_PYTHON_QA_AND_EDITORIAL_RECHECK_2026-11-23.md). 기존 원고/정답 불변, Q1-D/Q2-C 오답만 근거 중심으로 수정, 문항 세트 버전 r6-12-mcq-v2. Python 로컬 15개 검사 통과(9 QA 직접 + 6 생성 래퍼/Stage5 mock). **실제 Stage5 전체 통합 실행/실제 라이브 AI/API 호출/사람 검수·배포 승인 미완료.**
