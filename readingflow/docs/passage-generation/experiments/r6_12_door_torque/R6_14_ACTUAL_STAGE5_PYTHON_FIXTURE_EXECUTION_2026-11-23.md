# R6.14 — 실제 Stage5 Python 실행 및 24속성 단일 추첨 계측

작업일: 2026-11-23
브랜치: `feature/author-attribute-rng-audit-20261119`

## 이번에 실제 실행한 범위

GitHub 작업 브랜치에서 받은 **원본 Python 소스 10종**을 로컬 실행환경에 복원하였다. Git 객체 SHA-1과 원격 blob SHA의 일치를 비교했다. 다음 모듈을 수정 없이 실행하였다.

- `passage_stage5_integration.py`
- `new_passage_generation_pipeline.py`, `new_passage_qa_gate.py`
- `author_attribute_sampler.py`
- `passage_goal_contract.py`, `passage_evidence_contract.py`, `passage_planning_contract.py`
- `topic_taxonomy_v2_contract.py`, `passage_quality_gate.py`, `passage_duplication_diversity.py`

**중요한 범위 제한:** 실행에 사용된 주제·목표·출처·품질 정책·30편 기준선 입력 JSON은 실제 원본 데이터를 모두 재현한 것이 아니라 계약을 만족하도록 만든 **독립적인 합성 시험 데이터**였다. 24개 필자 속성의 명칭과 각 후보 값(총 172개)은 저장소의 후보 풀과 대조했다. 기존 R6.12 손잡이 지문과 문항 세트는 작성 완료된 정적 제공자 응답을 사용했다. 이 시험이 원본 저장소의 전체 입력 JSON, 실제 실시간 AI 호출, 필자 스타일 구현을 검증했다고 주장하지 않는다.

## 로컬 실측

- 실제 Stage5/생성 래퍼/검수 모듈을 사용하는 Python 독립 테스트 **10/10 통과**.
- Stage5 11개 단계 수행, 24속성/172후보 추출 기록, 검증전 사실 기본 `HOLD_SOURCE_VERIFICATION`(생성 제공자 호출 없음).
- 실험 허용 시 한 번의 제공자 호출, `READY_FOR_EDITORIAL_REVIEW`, 17항목 구조검사 **오류 0 / 경고 0**.
- `unittest.mock.patch.object(stage5, 'draw_author_attributes', ...)` 로 실제 Stage5 추첨 함수를 계측한 추가 시나리오 3개:
  1. 정상 후보: 추첨 1회·제공자 1회·`READY_FOR_EDITORIAL_REVIEW`.
  2. 정답 레이블 오표기: 추첨 1회·제공자 1회·`REVISE` (품질 문제로 재추첨 안 함).
  3. 미검증 사실 기본차단: 추첨 1회·제공자 0회·`HOLD_SOURCE_VERIFICATION`.
- 원고·문항·필자 풀을 바꾸거나, 배포 승인을 변경하지 않았다.

## GitHub 재현 검사 추가

`test_r614_real_stage5_draw_spy.py`를 추가했다. 이 회귀 테스트 파일은 **체크아웃한 저장소의 원본 입력 JSON**을 `run_trial.load_trial()`로 로드하며, 원본 Stage5에서 24속성을 정말 한 번만 뽑는지 3개 시나리오로 계측하도록 작성했다. **해당 GitHub 원본 입력형 테스트는 이 커밋에서 실행 통과했다고 주장하지 않는다.** 위 10+3 로컬 결과는 합성 입력으로 얻은 것이다.

재현 명령:
```bash
cd docs/passage-generation/experiments/r6_12_door_torque
python -m unittest test_r614_real_stage5_draw_spy -v
python -m unittest test_r612_trial -v
python run_trial.py --output /tmp/r612_stage5_real_inputs_result.json
```

## 판정

- 실제 원본 구현의 Stage5 **동작·결합 자체는 합성 입력을 이용한 실행으로 통과**.
- **아직 검증 전**: GitHub 원본 입력 JSON 종단시험, 실제 추첨된 속성을 전달받은 모델의 신규 원고 작성, 각 속성의 문장·문단 발현, 사실 검증, 의미 품질/문항 변별력 독립 검수, 학습자 실측, 배포 승인.
- 고정 원고가 필자 추첨보다 먼저 작성되었으므로 24속성의 문체 반영을 입증할 수 없다.
- 이전 GitHub Actions 2개가 조기 실패하고 있어 자동 CI는 별도 조사 대상.

다음 우선 작업: 원본 입력 JSON 전체를 사용해 위 회귀를 실행하고, 실제 모델 생성으로 넘기기 전에 출처 검증 HOLD를 유지한다. 기존 30편·90문항 수정 금지.
