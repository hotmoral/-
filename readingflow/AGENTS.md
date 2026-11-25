# ReadingFlow 공동 작업 규칙

## 수정 범위
- 공용 저장소 `hotmoral/-`의 **`readingflow/` 하위만** 수정한다. 다른 AI의 프로젝트 폴더, 공용 루트 README, 무관한 workflow를 변경하지 않는다.
- 자동 테스트 workflow는 **`.github/workflows/readingflow-validation.yml`**만 사용한다.
- 비공개 원본 `hotmoral/ReadingFlow`을 실수로 수정/공개하거나 과거 파일을 대량 미러링하지 않는다.
- Git 커밋에는 변경 이유·실행한 실제 테스트·결과를 남긴다. 실험 원고와 코드 변경을 구분한다.

## 작업 근거와 불변조건
- 기준: `docs/passage-generation/NEW_PASSAGE_AUTHORING_AND_MCQ_CANONICAL_2026-11-22.md` 및 그 하위 계약. 최근 사용자 결정이 구버전 제안보다 우선한다.
- 읽기 연령군: 초등 저학년/초등 고학년/중·고등학생/성인/고령층, 각각 L1–L6. 비문학만.
- 주제→목표→사실 확인→24 필자 속성 1회 독립 추첨→본문→문항/정답/오답 근거→17 QA 순서.
- 필자 속성은 QA 실패를 이유로 재추첨하지 않는다. 충돌/부분 적용/미적용은 로그에 남긴다.
- 신규 원고는 지문 근거와 정답 1개를 확인한다. 오답 3개마다 관련 원문 인용 및 배제 이유를 제공한다. 엉뚱한 조합·비문·노골적인 절대 단정·정답 길이 단서를 점검한다.
- 단순 배경지식으로 정답을 예상할 수 있음은 오류 판정 사유가 아니다.
- 기존 30편·90문항은 **변경 금지**, 기존 원고 본문/대량 revisions는 공용 저장소로 가져오지 않는다.

## 검증 및 승인
- `python -m unittest discover -s readingflow/docs/passage-generation/tools -p 'test_new_passage_generation_pipeline.py' -v`
- `python -m unittest discover -s readingflow/docs/passage-generation/tools -p 'test_r616*.py' -v`
- `python -m unittest discover -s readingflow/docs/passage-generation/tools -p 'test_r617*.py' -v`
- `python readingflow/docs/passage-generation/experiments/r6_17_ci_and_generation/run_trial.py`
- 최소 실제 CI 증거: `https://github.com/hotmoral/-/actions/runs/45551005100` (16회귀 PASS).
- `HOLD_SOURCE_VERIFICATION` 차단을 우회해 실험할 경우 `EXPERIMENT_ONLY` 명시, `can_publish=false` / `release_approved=false` 유지.
- 코드 통과 ≠ 실제 AI 실시간 API 생성 검증 ≠ 문항 의미·사실·독창성 사람 검수 ≠ 학습자 검증 ≠ 배포 승인.
- 공개 저장소에 API 키, 로그인 정보, 원본 외부 저작물, 무단 복제 원고·보호된 텍스트를 넣지 않는다.

## 상태
- `MIGRATION_STATUS.md` / `MIGRATION_MANIFEST.json`에서 원본 기준 SHA와 이전 결과 확인.
- 후속 작업은 공용 경로에서 이어가고, 별도 사용자 지시 없이 이전 비공개 저장소 동기화를 주장하지 않는다.
