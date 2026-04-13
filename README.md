# Word to Image (픽셀 아트 BMP) - 초보자용 가이드

입력한 단어/문장을 **픽셀 아트 스타일 BMP 이미지**로 만들어주는 프로그램입니다.
외부 라이브러리 없이 실행되며, GUI 창에서 입력 후 버튼 클릭으로 이미지를 만들 수 있습니다.

---

## 0) 가장 쉬운 목표

당신이 원하는 형태:
- exe 파일 더블클릭
- 윈도우 창 열림
- 텍스트 입력
- 이미지 생성

이 저장소는 그걸 위해 아래 파일을 제공합니다.
- `launch_gui.py`: GUI만 바로 실행하는 파일
- `build_windows_exe.bat`: exe 자동 빌드 스크립트

---

## 1) 지금 바로 GUI 실행 (설치 테스트)

1. 프로젝트 폴더를 엽니다.
2. 터미널(명령 프롬프트/PowerShell)에서 아래 실행:

```bash
python launch_gui.py
```

창이 뜨면 정상입니다.

---

## 2) Windows 실행파일(.exe) 만들기 (초보자용)

### 방법 A: 자동 스크립트(추천)

프로젝트 폴더에서 `build_windows_exe.bat`를 **더블클릭**하세요.

스크립트가 자동으로:
1. PyInstaller 설치
2. exe 빌드
3. 결과 경로 안내

완료 후 실행파일:
- `dist\\WordToImageGUI.exe`

이 파일을 더블클릭하면 GUI 창이 실행됩니다.

### 방법 B: 수동 명령어

```bash
python -m pip install pyinstaller
pyinstaller --onefile --windowed --name WordToImageGUI launch_gui.py
```

---

## 3) GUI 사용법

1. 텍스트 입력
2. 출력 경로(.bmp) 지정
3. 배율/여백/색상 값 입력
4. `이미지 생성` 버튼 클릭

---

## 4) CLI도 가능(선택)

GUI 말고 명령어 방식도 됩니다.

```bash
python word_to_image.py "안녕하세요" --output hello.bmp
```

---

## 5) 자주 막히는 문제

- **Python이 없다고 나옴**: python.org에서 설치 후 "Add Python to PATH" 체크
- **GUI가 안 뜸**: 원격/서버 환경이면 화면이 없어 GUI 실행 불가
- **exe가 안 만들어짐**: 보안 프로그램에서 빌드 차단하는지 확인

---

## 6) 내부 동작 참고

- `word_to_image.py`는 CLI/GUI 둘 다 지원합니다.
- A-Z, 0-9, 공백은 5x7 폰트로 표시됩니다.
- 한글 등은 문자 코드 기반 픽셀 패턴으로 변환됩니다.
