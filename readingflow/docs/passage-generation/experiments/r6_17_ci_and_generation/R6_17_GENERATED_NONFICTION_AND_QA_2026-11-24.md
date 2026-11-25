# R6.17 — 신규 비문학 원고 실제 ChatGPT 집필 + Stage5/17QA 검증

기준일: 2026-11-24 / 미승인 실험. 본 보고서의 **AI 자체 평가와 독립 사람 검수는 다름**.

## 1. 작업 범위와 출처

- 대상: `RF-R617-SECONDARY-L4-001` / `r6-17-generated-v1` / 중·고등학생 L4.
- 주제: **검색어가 가장 많이 나오는 글이 가장 적절한 글일까** (`정보·컴퓨터` → `데이터 처리·정보 검색`).
- 독해목표는 (1) 단어 출현 횟수와 정보 요구 충족 **비교**, (2) 서로 다른 검색 결과 **추론**, (3) 질문 변경에 따른 관련성 **근거 평가**로 분리.
- 기존 30편에는 자료 검색 *방식과 검색 결과의 정보 요구*를 직접 설명하는 동일 제목/중심 구조가 없음. 다만 내용과 논증에 대한 독립 의미 중복 검수는 **NOT_RUN**.
- `trial_inputs_v1.json`으로 목표·사실 후보·출처 3개가 아닌 **2개 원 출처**(Stanford IR, NIST TREC)를 준비하고, 편집 승인하지 않은 상태로 유지했다. 예시에 등장하는 달의 위상 원리는 NASA 별도 공공 설명과 모델이 대조했으나, 인용문을 재사용하지 않고 가상의 검색 상황에 적용했다. 사실·저작권의 독립 검수는 아직 아님.
- 공식 확인 출처(원문 복제 금지):
  - Stanford *Introduction to Information Retrieval*: https://nlp.stanford.edu/IR-book/ (검색어 빈도와 정보 요구 관련성의 구분)
  - NIST TREC relevance judgments: https://trec.nist.gov/data/reljudge_eng.html (정보 요구에 비추어 문서 관련성 판단)
  - NASA Moon Phases: https://science.nasa.gov/moon/moon-phases/ (달에서 밝게 보이는 부분의 변화)
- 사실 레지스트리의 source/fact 검수 상태는 **PENDING_EXTERNAL_REVIEW**로 유지한다. ChatGPT가 웹 자료를 확인했다고 `REVIEWED_BY_HUMAN`으로 올리지 않는다.

## 2. 실제 집필과 24개 필자 속성

1. 문서 작성 **전에** 주제·목표·근거 계획을 먼저 확정하고 `Stage5.integrate(..., seed=2026112405)`로 24개 속성 1회 추첨, `author_draw_v1.json` 저장. 후보 풀 24개·총 172값, 원본 SHA-256 `b98fba13edbcf91a5fc8295ee6816af10ed4b6d70b9c02ca0cd7b83c81662460`.
2. **그 뒤** 이 대화의 ChatGPT 모델이 4문단, 공백 제외 **613자**, 신규 질문 3개·A–D 선지 12개·오답별 반박 근거 9개를 집필했다. `model_authored_output_v1.json` 참조. 실제 OpenAI Responses **API는 호출하지 않았다**.
3. 지문은 가상 학생의 검색 상황임을 `검색했다고 하자`라고 명시. 24개 속성의 `구체화=실제 사례`는 실제 기록된 사례라고 가장하지 않고 제한. 전문적 배경 등이 연령 가독성을 손상시키지 않도록 관리했다.
4. `author_style_self_review_v1.json`: **AI 자체 관찰** 16개, 부분/제한 적용 7개, 독립 확인 불가 1개. 사람에 의한 24속성 구현·차별성 검수는 0개.

## 3. 수정한 실제 코드 결함

기존 `tools/new_passage_generation_pipeline.py`의 `generate_experimental_candidate`는 원고 작성 전에 생성한 속성을 입력으로 받을 수 없어, 실행할 때마다 `integrate(seed=...)`를 다시 호출했다. 재현 시드가 같은 결과를 만든다고 해서 원고 제작시의 **원래 추첨**을 재사용한 것과 같지는 않다.

해결: `author_selection_override` 인자를 추가하고 원본 Stage5의 기존 재사용·검증 로직에 그대로 전달. `seed`와 동시 지정은 거부. 다른 내용이나 품질 점수에 따른 재추첨 **불가**. 별도 회귀 테스트에서 `draw_author_attributes`를 호출하면 예외가 발생하도록 감시하며 Stage5 전 단계를 실행했다.

## 4. 재현 가능한 검증

실행:

```bash
cd docs/passage-generation
python experiments/r6_17_ci_and_generation/run_trial.py
python -m unittest discover -s tools -p 'test_r617*.py' -v
python -m unittest discover -s tools -p 'test_new_passage_generation_pipeline.py' -v
python -m unittest discover -s tools -p 'test_r616*.py' -v
```

- 신규 R6.17 회귀: **7/7 통과** (필자 선추첨 4개, 가상 HTTP Responses 연결 3개).
- 기존 R6.11/R6.16 회귀: **9/9 통과**. 이 범위의 합계 **16/16**; GitHub Actions 전체 CI 통과가 아님.
- 원본 Stage5 단계 **11/11**, 원본 30편 보존, 필자 추첨 재호출 **0회**, 생성기 호출 **1회**.
- 기본 출처 차단 `HOLD_SOURCE_VERIFICATION`; **명시적 실험**에서만 `READY_FOR_EDITORIAL_REVIEW`.
- 신규 문항 3개 정답 슬롯 **C/B/A**. 17개 구조검사 항목 중 오류 **0**, 경고 **0**. 정확한 정답 근거 3개, 오답 9개 각각 원문 인용과 반박 이유 연결. 정답 유일 길이 최단·최장, 절대적 단정 편향 경고 없음.
- 초안에서 Q3 오답 근거 인용이 `첫 번째 글은`이라고 적혀 원문의 `첫 번째 결과는`과 일치하지 않아 검사가 `REVISE` 처리했고, 근거 인용만 수정해 재검사 통과. **정답·정답 슬롯은 바꾸지 않았다.**
- `test_r617_mocked_live_adapter_contract.py`는 키/모델 미설정에 대한 방어, `store=false`, Responses JSON 파싱, 실제 Stage5 연결을 **모의 HTTP 응답**으로 검증한다. 네트워크/유료 API 호출은 0회.

## 5. AI의 별도 문항 내용 검토 (사람 PASS 아님)

| 문항 | 독해 연산 | 정답 | 오답 배제 논거 |
| --- | --- | --- | --- |
| Q1 | 비교 | C | A: 검색어 적어도 관련 가능; B: 단어 반복이 답 보장 못함; D: 단어 횟수와 뜻의 동일성 혼동 |
| Q2 | 추론 | B | A: 사진은 원인 충분 증거 아님; C: 빈도가 설명의 충실성 뜻하지 않음; D: 원리 설명과 사진의 양 혼동 |
| Q3 | 근거 평가 | A | B: 달라진 목적에 맞지 않게 원리 글 고정; C: 정보 요구 변화 무시; D: 같은 개념 설명과 날짜별 사진 제공을 혼동 |

발문은 중·고등학생 독서 문항의 정중한 문어체. 같은 물음을 3회 반복하지 않았고, 배경지식만으로 추측 가능한지 여부는 품질 감점에서 제외한다. **최종 AI 자체 판단**: 원고와 문항의 의미 관계가 일관된 편집 검토 후보이나, 실제 학습자 변별도/독립 답지 검증이 없다.

## 6. 검수/배포 경계

`human_validated=false`, `learner_validated=false`, `semantic_uniqueness_validated=false`, `release_approved=false`, `can_publish=false`.

검사에서 요구한 **공식 승인 조건**: 외부 사실·근거 출처 독립 확인 → 지문/선지 한국어·연령별 난도·정답 유일성 및 3개 오답 반박 독립 검수 → 24속성 표현 차이 검토 → 학습자 사용성/변별도 실험 → 출판/저작권 승인.

① GitHub Actions 실행기 배정 실패는 별도 기록 `R6_17_GITHUB_ACTIONS_RUNNER_DIAGNOSIS_2026-11-24.md` 참조; 실제 OpenAI API 키와 모델 환경변수도 없으므로 라이브 제공자 구간은 **NOT_RUN**.
