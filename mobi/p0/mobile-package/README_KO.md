# P0 Galaxy 실기기 검증 패키지 — ABOVE_IME v2

이 패키지는 **PC 없이 Galaxy에서 직접 설치하고 수동 검증**하기 위한 P0 기술 프로토타입입니다.

이번 v2의 핵심은 고양이 placeholder가 Samsung Keyboard **위(ABOVE_IME)** 에 실제로 존재할 수 있는지 확인하는 것입니다. `UNDER_IME`는 안전 fallback 비교용으로 남겨둡니다.

## 준비

- 실제 Samsung Galaxy
- 기본 키보드: Samsung Keyboard 권장
- `cat-presence-p0-debug.apk`

이 APK는 최종 Mobi 앱이 아닙니다. P0 Cat Presence Foundation의 bounded overlay / 이동 / 터치 / 키보드 표면 존재 / lifecycle을 확인하기 위한 임시 기술 빌드입니다.

## 설치

1. ZIP을 풀고 `cat-presence-p0-debug.apk`를 누릅니다.
2. Android가 요청하면 이 출처의 앱 설치를 이번에만 허용합니다.
3. 기존 P0 앱이 설치되어 있으면 업데이트 설치해도 됩니다.
4. 앱을 실행합니다.
5. `Grant / inspect overlay permission`을 눌러 **다른 앱 위에 표시** 권한을 허용합니다.
6. 앱으로 돌아와 `Start Presence`를 누릅니다.

기본 keyboard layer는 `ABOVE_IME`입니다.

## 실기기 체크 순서

1. **다른 앱 위 존재**
   - 설정, 브라우저, ChatGPT 등 다른 앱으로 이동합니다.
   - placeholder가 계속 떠 있는지 확인합니다.

2. **비간섭**
   - placeholder 사각형 바깥의 버튼/스크롤을 여러 번 조작합니다.
   - 평범하게 조작되어야 합니다.
   - placeholder의 투명한 여백도 실제 Window 내부이므로 그 부분은 터치를 받을 수 있습니다. 이것은 현재 P0에서 숨기지 않는 기술 특성입니다.

3. **고양이 직접 터치 / 드래그**
   - placeholder를 한 번 탭합니다.
   - placeholder를 손가락으로 다른 위치로 끌어봅니다.
   - 이동이 화면 밖으로 무제한 빠져나가면 안 됩니다.

4. **A → B 기술 이동**
   - P0 앱으로 돌아갑니다.
   - `Move A → B`를 누릅니다.
   - placeholder가 반대쪽 유효 위치로 이동하는지 확인합니다.

5. **Samsung Keyboard ABOVE_IME**
   - 입력 가능한 다른 앱에서 Samsung Keyboard를 띄웁니다.
   - placeholder를 키보드 영역 위로 직접 끌어봅니다.
   - **고양이가 키보드 뒤로 가려지지 않고 키보드 위에 보여야 합니다.**
   - 고양이 Window가 덮지 않은 키를 눌러 짧은 테스트 문자열을 입력합니다.
   - 입력 focus와 Samsung Keyboard가 계속 정상 동작해야 합니다.
   - 고양이 Window가 직접 덮은 키는 현재 P0에서 터치가 막힐 수 있습니다. 이것은 실제 rectangular Window footprint 제약이며 숨기지 않습니다.

6. **IME geometry 기반 비키기 substrate**
   - 고양이가 키보드 위에 겹쳐 있는 상태에서 고양이를 **한 번 탭**합니다.
   - v2의 QA-only 동작으로 고양이가 키보드 바로 위쪽으로 이동해야 합니다.
   - 이것은 최종 고양이 행동이 아니라, 키보드 geometry만으로 방해 영역에서 이동할 수 있음을 증명하는 기술 동작입니다.

7. **UNDER_IME fallback 비교(선택)**
   - P0 앱의 `Keyboard layer: UNDER IME (fallback)`을 누르면 예전처럼 키보드가 고양이 위에 놓입니다.
   - 다시 `Keyboard layer: ABOVE IME (Mobi default)`을 누르면 Mobi 방향으로 복귀합니다.

8. **회전**
   - 가로 방향으로 한 번 회전했다가 세로로 돌아옵니다.
   - placeholder가 비정상적으로 사라지거나 화면 밖에 영구 고정되지 않는지 확인합니다.

9. **화면 끄기 → 켜기**
   - 전원 버튼으로 화면을 끕니다.
   - 잠시 후 다시 켜고 잠금을 해제합니다.
   - 앱 프로세스가 유지된 일반 조건에서 placeholder가 계속 존재하는지 확인합니다.

10. **QA 보고서 확보**
   - P0 앱으로 돌아갑니다.
   - `Refresh QA State` → `Copy QA Report`를 누릅니다.
   - 이 채팅에 그대로 붙여 넣습니다.

11. **명시적 종료**
   - `Stop Presence`를 누릅니다.
   - placeholder가 즉시 사라지는지 확인합니다.

## 중요 관찰값

QA Report에서 특히 다음을 확인합니다.

- `prototype=P0_PROTO_V2_ABOVE_IME`
- `imeLayerMode=ABOVE_IME`
- `imeEverVisible=true`
- `maxImeBottomObserved`가 0보다 큰지
- keyboard overlap 중 `windowOverlapsImeNow=true`가 관찰되는지
- tap-to-clear 후 `imeClearCount>=1`
- `lastMove=IME_CLEAR_TAP ... errorPx=0` 여부

## 같이 보내면 좋은 증거

- 일반 다른 앱 위에 placeholder가 떠 있는 화면
- Samsung Keyboard **위에** placeholder가 보이면서 synthetic text 입력도 보이는 화면
- 가능하면 tap-to-clear 직전/직후 화면

개인 메시지나 개인정보가 보이지 않도록 synthetic text만 사용하세요.

## 테스트 종료 후

P0 검증이 끝나면 이 임시 앱은 삭제해도 됩니다.

이 패키지는 Accessibility, Usage Stats, 알림 내용 접근, 화면 캡처/OCR, 위치 권한을 요구하지 않습니다.
