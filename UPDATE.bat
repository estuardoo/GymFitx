@echo off
setlocal enabledelayedexpansion
title GYMFITX - actualizar
cd /d "%~dp0"

rem ------------------------------------------------------------------
rem  Prepara o actualiza el entorno. Correlo UNA vez (primer uso) y cada
rem  vez que cambie requirements.txt o quieras actualizar librerias. Al terminar abre GYMFITX.bat.
rem  Para usar la app a diario: GYMFITX.bat (no instala nada, arranca directo).
rem ------------------------------------------------------------------
set "PYVER="
if exist "python_version.txt" set /p PYVER=<python_version.txt

rem  Si la carpeta se copio o se movio (p.ej. de C:\ a D:\), el .venv viejo apunta
rem  a la ruta anterior: se descarta y se vuelve a crear aqui.
if exist ".venv\Scripts\activate.bat" (
    find /i "%CD%\.venv" ".venv\Scripts\activate.bat" >nul || (
        echo.
        echo   La carpeta cambio de lugar: se rehace el entorno virtual...
        rmdir /s /q ".venv"
    )
)

if not exist ".venv\Scripts\python.exe" (
    echo.
    echo   Creando el entorno virtual...
    where py >nul 2>nul
    if !errorlevel! equ 0 (
        if not "!PYVER!"=="" (
            echo   Usando Python !PYVER! ^(elegido desde el panel^)...
            py -!PYVER! -m venv .venv 2>nul
        )
        if not exist ".venv\Scripts\python.exe" py -3.11 -m venv .venv 2>nul
        if not exist ".venv\Scripts\python.exe" py -3.12 -m venv .venv 2>nul
        if not exist ".venv\Scripts\python.exe" py -3 -m venv .venv
    ) else (
        python -m venv .venv
    )
    if not exist ".venv\Scripts\python.exe" (
        echo.
        echo   [ERROR] No se pudo crear el entorno virtual.
        if not "!PYVER!"=="" echo   Verifica que Python !PYVER! este instalado y en el PATH.
        if "!PYVER!"=="" echo   Verifica que Python 3.11 o 3.12 este instalado y en el PATH.
        echo.
        pause
        exit /b 1
    )
)

call ".venv\Scripts\activate.bat"

echo   Instalando / actualizando dependencias...
rem  (versiones anteriores instalaban el codigo como paquete; ya no: corre desde esta carpeta)
pip uninstall -y gymfitx --quiet >nul 2>nul
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
if !errorlevel! neq 0 (
    echo.
    echo   [ERROR] Fallo la instalacion de dependencias. Revisa el mensaje de arriba.
    echo.
    pause
    exit /b 1
)

rem  Termino bien: abre GYMFITX.bat (que solo ejecuta). "--lanzar" (lo usa el panel al cambiar
rem  de version de Python) ya no hace falta: siempre se abre. Si algo fallo arriba, se queda con el error.
echo.
echo   Listo. Abriendo GYMFITX...
start "" "%~dp0GYMFITX.bat"
timeout /t 2 /nobreak >nul
exit /b 0
