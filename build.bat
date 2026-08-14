@echo off
chcp 65001 > nul
REM ==========================================================
REM  Go/No-Go 한국어판 - exe 빌드 스크립트
REM  프로젝트 폴더에서 실행:  build.bat
REM ==========================================================

setlocal
cd /d "%~dp0"

echo.
echo [1/5] 가상환경 확인
if not exist ".venv\Scripts\python.exe" (
    echo    .venv 를 찾을 수 없습니다. 먼저 환경을 구축하세요.
    goto :fail
)
call .venv\Scripts\activate.bat

echo.
echo [2/5] 버전 검증
python -c "import numpy,pyglet,psychopy;assert numpy.__version__.startswith('1.26'),'numpy '+numpy.__version__+' <- 1.26.4 여야 합니다';assert pyglet.version=='1.4.11','pyglet '+pyglet.version+' <- 1.4.11 이어야 합니다';assert psychopy.__version__=='2023.2.3','psychopy '+psychopy.__version__;print('   numpy',numpy.__version__,'/ pyglet',pyglet.version,'/ psychopy',psychopy.__version__)"
if errorlevel 1 goto :fail

echo.
echo [3/5] 스크립트 존재 확인
if not exist "gng_ko.py" (
    if exist "main.py" (
        echo    main.py 를 gng_ko.py 로 복사합니다.
        copy /y main.py gng_ko.py > nul
    ) else (
        echo    gng_ko.py 도 main.py 도 없습니다.
        goto :fail
    )
)

echo.
echo [4/5] PyInstaller 빌드 (수 분 소요)
python -m pip install "pyinstaller==6.10.0" --quiet
pyinstaller gng_ko.spec --noconfirm --clean
if errorlevel 1 goto :fail

echo.
echo [5/5] 자산 파일 복사
copy /y conditions.xlsx  dist\GoNoGo\ > nul
copy /y go.png           dist\GoNoGo\ > nul
copy /y nogo.png         dist\GoNoGo\ > nul
if exist NanumGothic.ttf copy /y NanumGothic.ttf dist\GoNoGo\ > nul
if exist gng.psyexp      copy /y gng.psyexp      dist\GoNoGo\ > nul
mkdir dist\GoNoGo\data 2> nul

echo.
echo ==========================================================
echo  빌드 완료
echo.
echo   실행 파일 : dist\GoNoGo\GoNoGo.exe
echo   결과 저장 : dist\GoNoGo\data\
echo.
echo  dist\GoNoGo 폴더를 통째로 옮겨야 동작합니다.
echo  exe 파일 하나만 떼어내면 실행되지 않습니다.
echo ==========================================================
goto :end

:fail
echo.
echo  *** 빌드 실패 ***
exit /b 1

:end
endlocal
pause
