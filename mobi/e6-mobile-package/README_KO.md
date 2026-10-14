# Samsung / One UI E6 모바일 단독 검증 패키지

이 패키지는 **PC 없이 Galaxy 한 대만으로** T0-3의 Samsung / One UI E6 검증을 실행하기 위한 것입니다.

구조는 다음과 같습니다.

`Termux → Android Wireless debugging → 같은 Galaxy의 adb shell → synthetic E6 probe`

실제 사용자 메시지, 문서, 클립보드, 알림 내용, 위치 정보는 읽지 않습니다. 테스트용 synthetic editor와 synthetic text만 사용합니다.

## 필요한 것

- Samsung Galaxy 실기기
- Samsung Keyboard가 기본 키보드로 선택된 상태
- Android 개발자 옵션 및 Wireless debugging 사용 가능 상태
- Termux
- 이 ZIP 파일

> Google Play의 오래된 Termux 빌드보다 공식 Termux 배포 경로(F-Droid 또는 Termux GitHub releases)를 사용하는 것을 권장합니다.

## 1. ZIP을 휴대폰에 받기

ZIP을 `Download` 폴더에 저장하고 압축을 풉니다.

Termux가 아직 저장소를 볼 수 없다면 Termux에서 한 번 실행합니다.

```bash
termux-setup-storage
```

Android가 파일 접근 권한을 요청하면 허용합니다.

## 2. 패키지를 Termux 홈으로 복사

압축을 푼 폴더 이름을 확인한 뒤 예를 들어 다음처럼 복사합니다.

```bash
cp -r ~/storage/downloads/mobi-samsung-e6-mobile-package ~/mobi-e6-mobile
cd ~/mobi-e6-mobile
```

파일 관리자에서 압축을 풀면서 폴더명이 달라졌다면 실제 이름에 맞게 바꾸면 됩니다.

공유 저장소에서 직접 실행하지 않고 Termux 홈으로 복사하는 이유는 Android 공유 저장소의 실행 제약을 피하기 위해서입니다.

## 3. Termux 준비

```bash
bash setup_termux.sh
```

이 스크립트는 `adb`, `zip`, `unzip`과 기본 shell 도구를 Termux에 설치합니다.

## 4. Galaxy의 Wireless debugging 켜기

Android 설정에서:

`설정 → 개발자 옵션 → 무선 디버깅`

을 켭니다.

개발자 옵션이 없다면:

`설정 → 휴대전화 정보 → 소프트웨어 정보 → 빌드번호`

를 여러 번 눌러 개발자 옵션을 활성화합니다.

## 5. 같은 Galaxy를 Termux adb와 페어링

Termux에서:

```bash
bash pair_connect.sh
```

스크립트가 두 종류의 주소를 차례로 물어봅니다.

### A. Pairing address

무선 디버깅 화면에서 **페어링 코드로 기기 페어링**을 누르면 표시되는:

- IP 주소
- pairing port
- 6자리 pairing code

를 입력합니다.

### B. Connection address

페어링 창을 닫고 무선 디버깅 메인 화면에 표시되는 일반 **IP 주소 및 포트**를 입력합니다.

페어링 포트와 연결 포트는 서로 다른 경우가 정상입니다.

성공하면 마지막에 대략 다음처럼 표시됩니다.

```text
ADB connected.
Target: ...
Device: samsung ...
Next: bash run.sh
```

## 6. Samsung Keyboard 확인

실행 전에 Android의 기본 키보드가 **Samsung Keyboard**인지 확인합니다.

다른 키보드가 기본이면 스크립트가 E6 증거로 인정하지 않고 중지합니다.

## 7. E6 테스트 실행

```bash
bash run.sh
```

실행 중에는:

- 휴대폰 잠금을 풀어 둡니다.
- Termux와 테스트 화면이 자동으로 전환될 수 있습니다.
- 화면이 회전할 수 있습니다.
- synthetic keyboard input이 자동 입력될 수 있습니다.
- 테스트가 끝날 때까지 다른 앱을 조작하지 않는 것이 좋습니다.

스크립트는 자동으로 다음을 검사합니다.

1. 실제 Samsung 기기인지
2. Samsung Keyboard가 기본 IME인지
3. synthetic APK 두 개 설치 및 overlay service 시작
4. 다른 UID의 synthetic editor가 focus를 갖는지
5. Samsung Keyboard 표시 상태를 host가 관찰하는지
6. overlay WindowContext / WindowMetrics가 동일한 docked IME geometry를 관찰하는지
7. Mode A overlap negative control
8. Mode B에서 editor focus와 synthetic typing이 유지되는지
9. 가능하면 One UI rotation / structural inset evidence

## 8. 결과 파일

실행 후 패키지 폴더에 다음과 같은 ZIP이 생성됩니다.

```text
mobi-samsung-e6-evidence-YYYYMMDD-HHMMSS.zip
```

**이 ZIP 하나를 ChatGPT의 Mobi 대화에 업로드하면 됩니다.**

성공뿐 아니라 실패한 실행의 ZIP도 버리지 마십시오. 실패 원인 분류에 필요합니다.

## 선택 옵션

회전을 하지 않으려면:

```bash
RUN_ROTATION=0 bash run.sh
```

테스트 종료 후 두 synthetic 앱까지 제거하려면:

```bash
CLEANUP_APPS=1 bash run.sh
```

## 주의

- Wireless debugging을 끄면 adb 연결이 끊길 수 있습니다.
- 휴대폰이 Wi-Fi 네트워크를 바꾸면 다시 `pair_connect.sh`가 필요할 수 있습니다.
- `adb pair` 성공 후에도 일반 connection port로 `adb connect`가 별도로 필요합니다.
- 같은 결과를 얻기 위해 무작정 여러 번 반복하지 마십시오. 첫 결과가 실패해도 evidence ZIP을 먼저 검토합니다.
- 이 패키지는 기술 검증용이며 production Mobi 앱이 아닙니다.
