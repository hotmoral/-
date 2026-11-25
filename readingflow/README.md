# ReadingFlow — 공동 개발 작업공간

**공용 저장소:** [hotmoral/-](https://github.com/hotmoral/-) 의 `readingflow/`  
**현재 작업:** R6.17 신규 한국어 비문학/독해 문항 자동 생성기 및 검수 시스템.

## 이전 상태

- 원본 비공개 저장소 `hotmoral/ReadingFlow`, 브랜치 `feature/author-attribute-rng-audit-20261119`, 커밋 `60b52baa9fe21095d880d8804d5e98787acf2ecc`에서 **선별 파일 68개를 그대로 복사**했습니다.
- **Git 객체 SHA 68개 일치**, 누락·변형 0건. 전체 목록은 `MIGRATION_MANIFEST.json`.
- **공용 GitHub Actions 실제 성공:** [ReadingFlow Stage5 Generator CI](https://github.com/hotmoral/-/actions/runs/45551005100) — Python 회귀 16개 모두 통과, R6.17 Stage5/17 QA 실행 완료.
- 이 작업공간에서는 앞으로 **`readingflow/` 하위만 수정**하고 다른 공용 프로젝트 폴더는 건드리지 않습니다.
- 비공개 원본 저장소는 보존합니다. 기존 30편·90문항의 원고 본문/대량 수정 이력은 복사하지 않고, 구조검사용 30편 **메타데이터**만 가져왔습니다.

## 폴더

- `docs/passage-generation/tools/` — 실제 Stage5 생성/검수 코드와 Python 테스트
- `docs/passage-generation/planning/`, `data/`, `operations/` — 읽기 목표, 사실, 무작위 필자 속성, 검수 계약
- `docs/passage-generation/experiments/` — R6.12~R6.17 원고 및 재현 실험 자료
- `MIGRATION_STATUS.md`, `MIGRATION_MANIFEST.json` — 검증/이전 근거
- `AGENTS.md` — 공동 작업 규칙

## 실행

공용 저장소 루트에서:

```bash
python -m unittest discover -s readingflow/docs/passage-generation/tools -p 'test_new_passage_generation_pipeline.py' -v
python -m unittest discover -s readingflow/docs/passage-generation/tools -p 'test_r616*.py' -v
python -m unittest discover -s readingflow/docs/passage-generation/tools -p 'test_r617*.py' -v
python readingflow/docs/passage-generation/experiments/r6_17_ci_and_generation/run_trial.py
```

**범위:** 자동 Python 구조 검증과 실험용 모델 작성 후보입니다. 실제 실시간 OpenAI API 호출, 독립 사실 확인, 사람의 문항 의미·문체 검수, 학습자 실측 및 배포 승인은 아직 별개입니다. 비밀 키·유료 API 출력·보호된 외부 저작물은 공개 저장소에 저장하지 않습니다.
