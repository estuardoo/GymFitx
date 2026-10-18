@echo off
setlocal
title Subir a GitHub - GYMFITX
cd /d "%~dp0"
rem  Ventana para subir el codigo actual a GitHub. Solo necesita Python 3.9+ (con tkinter, viene en el instalador normal) y git.
where py >nul 2>nul && (py -3 subir_github.py & goto :fin)
where python >nul 2>nul && (python subir_github.py & goto :fin)
echo.
echo   No se encontro Python. Instalalo desde https://www.python.org/downloads/ (marca "Add python.exe to PATH").
echo.
pause
:fin
endlocal
