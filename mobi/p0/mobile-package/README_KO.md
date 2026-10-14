# P0 Galaxy 실기기 검증 패키지

이 패키지는 **PC 없이 Galaxy에서 직접 설치하고 수동 검증**하기 위한 P0 기술 프로토타입입니다.

## 준비

- 실제 Samsung Galaxy
- 기본 키보드: Samsung Keyboard 권장
- `cat-presence-p0-debug.apk`

이 APK는 최종 Mobi 앱이 아닙니다. P0 Cat Presence Foundation의 bounded overlay / 이동 / 터치 / 키보드 공존 / lifecycle을 확인하기 위한 임시 기술 빌드입니다.

## 설치

1. ZIP을 풀고 `cat-presence-p0-debug.apk`를 누릅니다.
2. Android가 요청하면 이 출처의 앱 설치를 이번에만 허용합니다.
3. 앱을 실행합니다.
4. `Grant / inspect overlay permission`을 눌러 **다른 앱 위에 표시** 권한을 허용합니다.
5. 앱으로 돌아와 `Start Presence`를 누릅니다.

화면에 작은 고양이 형태의 기술 placeholder가 떠야 합니다.

## 실기기 체크 순서

아래를 순서대로 수행합니다.

1. **다른 앱 위 존재**
   - 설정, 브라우저 등 다른 앱으로 이동합니다.
   - placeholder가 계속 떠 있는지 확인합니다.

2. **비간섭**
   - placeholder 사각형 바깥의 버튼/스크롤을 여러 번 조작합니다.
   - 평범하게 조작되어야 합니다.
   - placeholder의 투명한 여백도 실제 Window 내부이므로 그 부분은 터치를 받을 수 있습니다. 이것은 현재 P0에서 숨기지 않는 의도된 기술 특성입니다.

3. **고양이 직접 터치 / 드래그**
   - placeholder를 한 번 탭합니다.
   - placeholder를 손가락으로 다른 위치로 끌어봅니다.
   - 이동이 화면 밖으로 무제한 빠져나가면 안 됩니다.

4. **A → B 기술 이동**
   - P0 앱으로 돌아갑니다.
   - `Move A → B`를 누릅니다.
   - placeholder가 반대쪽 유효 위치로 이동하는지 확인합니다.

5. **Samsung Keyboard 공존**
   - 메모/검색창처럼 입력 가능한 다른 앱을 엽니다.
   - Samsung Keyboard를 띄우고 실제로 짧은 테스트 문자를 입력합니다.
   - 키보드 입력이 정상 동작해야 합니다.
   - placeholder와 키보드가 겹치는 위치에서는 키보드가 사용 가능한 상태를 유지해야 합니다.

6. **회전**
   - 자동 회전 또는 수동 회전을 이용해 화면을 한 번 가로 방향으로 바꿨다가 세로로 돌아옵니다.
   - placeholder가 비정상적으로 사라지거나 화면 밖에 영구 고정되지 않는지 확인합니다.

7. **화면 끄기 → 켜기**
   - 전원 버튼으로 화면을 끕니다.
   - 잠시 후 다시 켜고 잠금을 해제합니다.
   - 앱 프로세스가 유지된 일반 조건에서 placeholder가 계속 존재하는지 확인합니다.

8. **QA 보고서 확보**
   - P0 앱으로 돌아갑니다.
   - `Refresh QA State`를 누릅니다.
   - `Copy QA Report`를 누릅니다.
   - 이 채팅에 그대로 붙여 넣습니다.

9. **명시적 종료**
   - `Stop Presence`를 누릅니다.
   - placeholder가 즉시 사라지는지 확인합니다.

## 같이 보내면 좋은 증거

가능하면 아래 스크린샷 2장을 함께 올려주세요.

- 일반 다른 앱 위에 placeholder가 떠 있는 화면 1장
- Samsung Keyboard가 열린 상태에서 placeholder가 같이 보이는 화면 1장

스크린샷에는 개인 메시지나 개인정보가 보이지 않도록 빈 메모/검색 화면을 사용하세요.

## 테스트 종료 후

P0 검증이 끝나면 이 임시 앱은 삭제해도 됩니다.

이 패키지는 Accessibility, Usage Stats, 알림 내용 접근, 화면 캡처/OCR, 위치 권한을 요구하지 않습니다.
