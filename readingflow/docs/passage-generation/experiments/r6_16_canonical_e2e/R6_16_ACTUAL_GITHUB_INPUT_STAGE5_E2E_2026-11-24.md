# R6.16 — GitHub 원본 전체 데이터 Stage5 Python 종단시험

기준 브랜치: `feature/author-attribute-rng-audit-20261119`  
검증 기준 커밋: `e630723596f81409098efb8d5a0782ad476f08b5`  
로컬 실행일: 2026-11-24

## 결론

**문제 ② (실제 저장소 데이터에 대한 Stage5 종단시험)는 해결.** 비공개 GitHub 파일을 커넥터로 조회한 뒤 로컬 Python 실행환경에 복원. Python 원본 **10개**, Stage5 입력 원본 JSON **10개**를 `git hash-object`로 GitHub blob SHA와 **20/20 완전 일치** 확인. 대형 입력 JSON 4개는 전송 전 필드 추출본으로 일시 시험했으나, 마지막에는 누락 필드·키 순서·형식을 복원해 Git SHA가 일치한 **완전한 원본 파일로 교체한 다음 최종 재실행**했다. 최종 시험은 추출본이 아니다.

실행:
```bash
cd docs/passage-generation/tools
python -m unittest test_new_passage_generation_pipeline test_r616_canonical_stage5_end_to_end -v
```
**9개 테스트 전부 통과** (기존 6개 + 신규 3개). 원본 R6.11 테스트 모듈도 GitHub blob SHA `8b7073ad7df4d9b06c6e4ee9b961ed70288acd19`와 동일하게 복원해서 실행.

## 세부 종단 결과

| 단계 | 실제 확인 |
| --- | --- |
| 계획 자료 로드 | 원본 주제 분류 18개 영역·298개 하위분야, 필자 24개 풀·172개 선택지 |
| 과거 시범 | 기존 30편 원본과 대응표 30건 불일치 없이 로드 |
| 사전 통합 | 11개 단계 정상 수행; 단계 8 미작성 상태에서는 정상 차단 |
| 기본 사실 검증 차단 | `HOLD_SOURCE_VERIFICATION`; 생성 제공자 0회 호출 |
| 명시적 비검증 실험 | 제공자 정확히 1회 호출, `READY_FOR_EDITORIAL_REVIEW` |
| 필자 추첨 | 한 시도당 1회, 정확히 24개; 요청·Stage5 출력값 동일, 재추첨 없음 |
| 문항 구조검사 | 17항목, 오류 0건, **주의 경고 3건** |
| 의도적 오답 키 오류 | `REVISE`, `ANSWER_MAPPING_INVALID`, 추첨 1회 유지 |
| 입력·승인 | 입력 객체 불변, `release_approved=false`, `can_publish=false` |

## 주의 경고 3건의 의미

원본 테스트 제공자 `test_new_passage_generation_pipeline.response_for`가 생성하는 **합성 시범 문항** 3개 모두 정답이 혼자 유일하게 짧고, 비정답 중 절대적인 표현이 과다하다. QA는 각 문항에 `OPTION_SURFACE_CUE` 경고를 정상 발생시켰다. 구조검사 오류가 아니라 **문항 품질 개선 필요 사항**이다. 이 테스트 문항은 배포 품질 지문이 아니다. 원본 시범 30편·90문항이나 실제 R6.12/R6.15 원고를 바꾸지 않았다.

## 테스트 경계

- 이 실행은 **실제 Stage5/생성 래퍼/17QA 코드 + 실제 GitHub 원본 입력 JSON**을 사용했다.
- 제공자는 **시험용 Python 함수**로 주입. 실제 유료/실시간 AI API 호출은 아님. 생성기 인터페이스 및 반환 검증을 완료했다는 의미.
- 출처 실사, 문체 24속성의 실제 AI 반영, 내용 자연스러움, 문항 정답의 의미상 유일성, 독립 사람·학습자 평가를 통과했다는 뜻이 아니다. 이 항목은 문제 ③과 콘텐츠 검수 작업으로 별도 수행.
- 문제 ①: GitHub Actions 작업이 시작 단계 전에 실패하는 것은 이번 오프라인 Python 실행과 별개다. Actions 복구를 주장하지 않는다.
- 신규 회귀 `tools/test_r616_canonical_stage5_end_to_end.py`는 GitHub에서 저장소 전체를 체크아웃한 후 동일 조건을 재현한다. 이 파일의 테스트 통과 기록은 이번 로컬 Python 실행 결과이며 GitHub Actions 성공 결과가 아니다.
