@echo off
setlocal enabledelayedexpansion
title GYMFITX
cd /d "%~dp0"

rem ------------------------------------------------------------------
rem  Solo ejecuta la app (no instala nada). Primer uso o cambio de
rem  librerias / de carpeta: corre antes UPDATE.bat.
rem ------------------------------------------------------------------
if not exist ".venv\Scripts\activate.bat" (
    echo.
    echo   Falta el entorno virtual: ejecuta primero UPDATE.bat
    echo.
    pause
    exit /b 1
)

rem  Si la carpeta se movio, el .venv apunta a la ruta vieja: hay que rehacerlo.
find /i "%CD%\.venv" ".venv\Scripts\activate.bat" >nul || (
    echo.
    echo   La carpeta cambio de lugar: ejecuta UPDATE.bat para rehacer el entorno.
    echo.
    pause
    exit /b 1
)

call ".venv\Scripts\activate.bat"

rem ------------------------------------------------------------------
rem  Si quedo una instancia de GYMFITX corriendo de una vez anterior (p.ej.
rem  se cerro la ventana sin Ctrl+C), la apaga primero: si no, la camara
rem  queda bloqueada por ese proceso viejo y el nuevo arranque falla.
rem ------------------------------------------------------------------
set "MATADO="
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":8000" ^| findstr "LISTENING"') do (
    echo   Deteniendo instancia anterior ^(PID %%p^)...
    taskkill /F /PID %%p >nul 2>nul
    set "MATADO=1"
)
if defined MATADO timeout /t 1 /nobreak >nul

rem  Abre el navegador unos segundos despues de lanzar el servidor.
start "" cmd /c "timeout /t 3 /nobreak >nul && start http://127.0.0.1:8000"

echo   Panel GYMFITX en http://127.0.0.1:8000
echo   Deja esta ventana abierta mientras entrenas.
echo   Para cerrar: Ctrl+C, o simplemente cierra esta ventana.
echo   Tiempos por proceso: http://127.0.0.1:8000/api/tiempos  (y datos\logs\tiempos_*.log)
echo.

rem Primera vez: copia los datos del proyecto viejo (..\GYMFITX) sin tocarlo.
python -m src.nucleo.migrar

python -m src.interfaz

rem  Si el servidor termino limpio (p.ej. "Apagar panel"), la ventana se cierra sola.
rem  Si termino por un error o un crash, se queda abierta con el mensaje.
echo.
if !errorlevel! equ 0 (
    echo   GYMFITX se detuvo.
) else (
    echo   GYMFITX se detuvo con un error ^(codigo !errorlevel!^).
    pause
)
