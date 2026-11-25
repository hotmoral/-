# ReadingFlow — 공동 개발 작업공간

ReadingFlow 속독·독해 학습 프로그램의 **신규 한국어 비문학 지문/문항 생성기** 작업공간입니다.

- 위치: `hotmoral/-/readingflow/` (공개 공용 저장소)
- 원본: `hotmoral/ReadingFlow` (Private), `feature/author-attribute-rng-audit-20261119` at `60b52baa9fe21095d880d8804d5e98787acf2ecc`
- 범위: R6.17의 생성기·Stage5·17항목 QA, 필자 속성 24개 추첨·재사용, 신규 실험 원고
- 원본 Private 저장소는 보존합니다. **기존 30편 지문·90문항의 본문과 대량 수정 이력은 이 공간으로 복사하지 않습니다.** 회귀검사를 위해 필요한 읽기 전용 지문 *메타데이터*만 이전합니다.
- 현재 자료는 개발·검수 후보이며 배포 승인과 독립 사람/학습자 검증을 의미하지 않습니다.
- 외부 자료의 저작권 및 유료 API 키는 공개 저장소에 저장하지 않습니다.

## 실무 위치

`docs/passage-generation/tools/`: Stage5, 생성 인터페이스, 필자 난수추첨, QA 테스트

`docs/passage-generation/planning/`, `data/`, `operations/`: 규칙 및 검수용 계약·메타데이터

`docs/passage-generation/experiments/`: R6.12~R6.17 실험과 검증 증거

## 실행

작업공간 루트를 기준으로:

```bash
python -m unittest discover -s readingflow/docs/passage-generation/tools -p 'test_r617_*.py' -v
python -m unittest discover -s readingflow/docs/passage-generation/tools -p 'test_new_passage_generation_pipeline.py' -v
python readingflow/docs/passage-generation/experiments/r6_17_ci_and_generation/run_trial.py
```

이 코드는 시험용 생성 함수로 실행되며, 인증·모델을 직접 설정하지 않으면 유료 OpenAI API는 호출하지 않습니다. `README` 작성 당시의 경로이며 파일 동기화 완료 상태는 `MIGRATION_STATUS.md`에서 확인하세요.
