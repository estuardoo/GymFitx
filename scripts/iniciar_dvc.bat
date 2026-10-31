@echo off
rem  Una sola vez por equipo: deja DVC listo (punteros a los datos pesados). La carpeta .dvc ya viene en el repo con el remoto
rem  compartido (.dvc/config); la credencial NO viaja: queda en .dvc/config.local (ver docs/GUIA_ETAPA3.md).
cd /d "%~dp0\.."
call .venv\Scripts\activate.bat
pip install "setuptools<70" wheel
pip install "dvc>=3"
if not exist ".git" git init
if not exist ".dvc" dvc init
rem  Los datos pesados entran como punteros .dvc; los JSON chicos tambien (asi cada version queda fijada en git).
dvc add input\raw input\bronze
dvc repro
echo.
echo  Listo. Publicar es en DOS pasos y en este orden (primero el contenido, luego el historial):
echo    GITHUB_LOADER2 (programa aparte) hace los dos pasos en orden: dvc push y despues git push.
echo  Detalle en docs\GUIA_ETAPA3.md.
pause
