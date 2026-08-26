@echo off
setlocal enabledelayedexpansion
title GYMFITX
cd /d "%~dp0"

rem ------------------------------------------------------------------
rem  Primer uso: crea el entorno virtual e instala dependencias.
rem  Siguientes usos: esto se salta y arranca directo.
rem ------------------------------------------------------------------
rem ------------------------------------------------------------------
rem  Version de Python pedida desde el panel (boton "Cambiar version" en
rem  Sistema). Vacio o ausente = comportamiento de siempre (3.11, luego 3.12).
rem ------------------------------------------------------------------
set "PYVER="
if exist "python_version.txt" set /p PYVER=<python_version.txt

if not exist ".venv\Scripts\python.exe" (
    echo.
    echo   Primera vez: preparando GYMFITX, un momento...
    echo.

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

rem ------------------------------------------------------------------
rem  Instala/actualiza dependencias en CADA arranque, no solo la primera
rem  vez: si el requirements.txt gana una libreria nueva (p.ej. pygrabber),
rem  un venv que ya existia la recibe solo sin que haya que borrar .venv a
rem  mano. Con todo ya instalado, pip lo confirma en 1-2 segundos.
rem ------------------------------------------------------------------
echo   Verificando dependencias...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
if !errorlevel! neq 0 (
    echo.
    echo   [ERROR] Fallo la instalacion de dependencias. Revisa el mensaje de arriba.
    echo.
    pause
    exit /b 1
)

rem ------------------------------------------------------------------
rem  Si quedo una instancia de GYMFITX corriendo de una vez anterior (p.ej.
rem  se cerro la ventana sin Ctrl+C), la apaga primero: si no, la camara
rem  queda bloqueada por ese proceso viejo y el nuevo arranque falla.
rem ------------------------------------------------------------------
echo   Verificando si GYMFITX ya esta corriendo...
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":8000" ^| findstr "LISTENING"') do (
    echo   Deteniendo instancia anterior (PID %%p^)...
    taskkill /F /PID %%p >nul 2>nul
)
timeout /t 1 /nobreak >nul

rem ------------------------------------------------------------------
rem  Abre el navegador un par de segundos despues de lanzar el servidor,
rem  dandole tiempo a levantar antes de que la pestana intente cargar.
rem ------------------------------------------------------------------
start "" cmd /c "timeout /t 3 /nobreak >nul && start http://127.0.0.1:8000"

echo   Panel GYMFITX en http://127.0.0.1:8000
echo   Deja esta ventana abierta mientras entrenas.
echo   Para cerrar: Ctrl+C, o simplemente cierra esta ventana.
echo.

python apps\serve.py

rem ------------------------------------------------------------------
rem  Si el servidor termino limpio (p.ej. "Apagar panel" desde el navegador,
rem  que sale con codigo 0), esta ventana se cierra sola. Si termino por un
rem  error o un crash, se queda abierta con el mensaje para poder leerlo.
rem ------------------------------------------------------------------
echo.
if !errorlevel! equ 0 (
    echo   GYMFITX se detuvo.
) else (
    echo   GYMFITX se detuvo con un error ^(codigo !errorlevel!^).
    pause
)
