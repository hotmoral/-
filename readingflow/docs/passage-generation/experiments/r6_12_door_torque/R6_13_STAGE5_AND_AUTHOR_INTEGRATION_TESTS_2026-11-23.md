# R6.13 — 실제 Stage5 통합·필자 추출 검증 강화
작성일: 2026-11-23. 기준 브랜치: feature/author-attribute-rng-audit-20261119.

## 수정 목적
기존 15개 로컬 Python 검사는 정본 QA 17항목과 R6.11 생성기 래퍼까지 검증했지만 Stage5는 테스트 대역이었음. 이번 커밋은 **실제 저장소 Stage5 구현을 호출하는 기존 `run_trial.py`의 자체 단언 및 `test_r612_trial.py`의 회귀 테스트**를 강화한다. 기존 30편/90문항 원본과 새 시범 원고의 내용·정답/오답은 건드리지 않는다.

## 추가 실행 검사
- 미검증 사실 기본 HOLD -> provider 호출 0회.
- 명시적 실험은 제공자 1회 호출, 요청 당시 필자 24개 값과 Stage5 생성 후 값 일치.
- **실제 Stage5 11단계 기록** 및 8단계 `AI_GENERATED_EXPERIMENTAL_DRAFT`.
- **기존 시범 30편 기준선**, 독립 속성 이름 집합 24개, `verify_selection` 풀 검증, 시드 보존, 후보 풀 SHA 일치.
- `author_selection_override`와 `seed` 동시 사용 금지, 재사용 시 원본 선택기록 동일.
- Stage5 입력 객체 비변경 및 `release_approved=false`, `can_publish=false`.
- 모든 17개 검사 `editorial_state=NOT_REVIEWED`; 필자 속성의 원고 표현 반영 `False`.
- 기존 5개 테스트에 통합 관련 테스트 3개 추가 → **총 8개 테스트 정의**. 테스트 정의 수는 실행 통과 수가 아니다.

## 검증 상태
- GitHub 코드 연결과 테스트 작성은 반영.
- **이 커밋에서 실제 저장소 Stage5 원본을 Python으로 실행한 결과는 아직 확보하지 못했다.** 이전 15개 로컬 성공은 Stage5 테스트 대역을 사용한 결과임.
- 모델이 필자 속성을 실제 문장·문단에 구현했는지 알 수 없다. 현재 제공자는 속성 추첨 전에 작성된 고정 원고를 반환하므로 전달/재사용 검증만 가능.
- 실제 모델 API 미호출, 사실·저작권/의미/난도/사람 검수 및 배포 승인 전부 미완료. 기본 source gate HOLD 유지.

## 재현
```bash
python docs/passage-generation/experiments/r6_12_door_torque/run_trial.py --output /tmp/r612_stage5_full_run.json
cd docs/passage-generation/experiments/r6_12_door_torque
python -m unittest test_r612_trial -v
```
`run_trial.py`는 실제 `tools/passage_stage5_integration.py`와 기존 저장소 입력 JSON을 읽는다. 정상 종료 시 오프라인 생성·검수 데이터와 필자 추첨 증거가 결과 JSON에 남는다. 결과 파일은 덮어쓰지 않는다.

## 이어서 해결할 점
1. 실제 Stage5 Python 실행 통과 확인과 CI 실패 원인 분리.
2. **24속성 추첨 이후 모델이 원고를 작성하는 실시간 생성 테스트**와 속성 적용 로그/문장 증거 별도 검수 (고정 원고 주입과 혼동 금지).
3. 독립 의미 검수·실측 전 자동 승인/생산 확대 금지.
