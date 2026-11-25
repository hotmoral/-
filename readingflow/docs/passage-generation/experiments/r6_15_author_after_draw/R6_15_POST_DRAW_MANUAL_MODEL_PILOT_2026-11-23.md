# R6.15 — 실제 필자 추첨 *이후* ChatGPT 원고 작성 실험 (비공식 API 주입)

2026-11-23 / feature/author-attribute-rng-audit-20261119

## 작업 의도와 명확한 범위
1. R6.12 기존 ‘문손잡이’ 지문·3문항, 동결된 30편·90문항은 수정하지 않음.
2. 같은 *주제*에 대해 **새로운 비교용 실험 원고**를 작성. R6.12 수정본이나 최종 승인 원고로 대체하지 않음.
3. Python `random.Random(202611232249)`로 저장소 24개 실제 후보 풀(172값)을 읽어 한 속성당 1회 선택. **문장 작성 전에 추첨 값을 확정**.
4. 추첨 값 확인 후 이 대화의 ChatGPT 모델이 실제 한국어 비문학 4문단(공백 제외 563자)과 서로 다른 독해 연산의 3문항·12개 선지·9개 오답 근거를 별도 원본으로 작성. **기존 `openai_new_passage_adapter.py`를 호출한 라이브 API 결과가 아니다.**
5. 24속성의 적용 상태를 AI 자체 사전 검토로 별도 기록. 엄밀한 독립 필자 스타일 평가, 17항목 Python 정본 QA 실행, 학습자 실측은 별개.

## 난수 추첨
- 방식: `python_mt19937_seeded_v1`의 실험용 재현 시드 (실제 서비스 CSPRNG 대신 재현 가능 시드).
- 풀: `docs/passage-generation/data/author_attribute_candidate_pools_proposal_v1.json` (상태: PROPOSAL_NOT_APPROVED).
- SHA-256(24개 풀 canonical serialization): `b98fba13edbcf91a5fc8295ee6816af10ed4b6d70b9c02ca0cd7b83c81662460`.
- `author_draw_and_application_v1.json`: 추첨 값 및 원본 `attribute_application_log`은 모두 `PENDING_INDEPENDENT_REVIEW`. 사용자가 승인하지 않은 12개 제안 후보 사용 없음.
- `style_application_ai_review_v1.json`: 문장 예시·충돌 이유 24개 기록, 사람 PASS 기록 없음. 예컨대 인문학 전문배경/긴 문단/삽입절/전문어 위주는 **초등 고학년 가독성·사실성 우선으로 제한**. 실제 사례 추첨도 교육용 가정 장면을 '검증된 실제 사건'으로 표시하지 않음.

## QA 및 사실
- 로컬 도구의 Python은 실제 후보 24속성 추첨 1회를 수행.
- 이 대화의 JavaScript 독립 검사로 정답 텍스트 매핑, 원문 연속 근거 3개, 오답 근거·배제 사유 9개, 고유 옵션, 정답 유일 길이 극단 여부 검증: **오류 0**. `test_r615_after_draw.py`는 실제 저장소 17항목 정본 Python 게이트로 같은 조건을 재현할 수 있게 제공하지만 이 커밋에서는 실행 통과를 아직 주장하지 않음.
- 후보 사실: UCSB Lecture Demonstration `https://web.physics.ucsb.edu/~lecturedemonstrations/Composer/Pages/28.18.html`, OpenStax University Physics `https://openstax.org/books/university-physics-volume-1/pages/10-6-torque`를 대조(독립 사람 확인 아님).
- `topic_id`는 R6.12과 같으며 의도적 동일 주제 실험임. 중복 콘텐츠로 출판 금지. 외부 사실 자료 본문 복제 없이 창작.
- 사용자 기준: 배경지식으로 지문 없이 풀 수 있는지 평가하지 않고 **지문과 정답/오답의 근거 관계만 검토**.

## 다시 검증할 항목
- 저장소 전체 원본 JSON + 전체 Stage5 Python 종단시험 통과(현재 파일의 JavaScript 정합성 대조와 구별).
- 실제 라이브 AI 제공자 입력에 24속성이 들어간 후 써지는지 확인(현재는 대화 모델이 추첨 뒤 작성한 원고).
- 사람 검수: 한국어 자연스러움·독해 목표/연령 적합·정답 유일성·오답 매력도, 미검증 출처 독립 확인, 독창성, 중복.
- `release_approved=false` / `can_publish=false` 유지. 테스트 파일 추가/문항 검사로 자동 승인하지 않음.
