@echo off
setlocal

echo Python fuggosegek ellenorzese es telepitese...
echo.

set "PYTHON_CMD="

py --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=py"
) else (
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON_CMD=python"
    )
)

if "%PYTHON_CMD%"=="" (
    echo HIBA: Nem talalhato Python telepites a gepen.
    echo Telepitsd a Python 3 verziot, majd futtasd ujra ezt a fajlt.
    pause
    exit /b 1
)

echo Python parancs megtalalva: %PYTHON_CMD%
echo Függőségek telepítése a requirements.txt alapján...

%PYTHON_CMD% -m pip install --upgrade pip
if errorlevel 1 (
    echo HIBA: A pip frissitese sikertelen volt.
    pause
    exit /b 1
)

%PYTHON_CMD% -m pip install -r requirements.txt
if errorlevel 1 (
    echo HIBA: A fuggosegek telepitese sikertelen volt.
    pause
    exit /b 1
)

echo.
echo Siker! Minden szukseges fuggoseg telepitve lett.
pause
endlocal