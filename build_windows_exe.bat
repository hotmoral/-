@echo off
setlocal

echo [1/3] PyInstaller 설치 중...
python -m pip install --upgrade pip
python -m pip install pyinstaller
if errorlevel 1 (
  echo PyInstaller 설치 실패. Python 설치/인터넷 연결을 확인하세요.
  pause
  exit /b 1
)

echo [2/3] exe 빌드 중...
pyinstaller --noconfirm --clean --onefile --windowed --name WordToImageGUI launch_gui.py
if errorlevel 1 (
  echo 빌드 실패. 오류 메시지를 확인하세요.
  pause
  exit /b 1
)

echo [3/3] 완료!
echo 실행파일 경로: dist\WordToImageGUI.exe
echo.
echo 이제 dist\WordToImageGUI.exe 를 더블클릭하면 윈도우 창이 실행됩니다.
pause
