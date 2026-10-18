@echo off
rem  Una sola vez: deja DVC listo (punteros a los datos pesados). Despues: dvc remote add, dvc push, git add, git push.
cd /d "%~dp0\.."
call .venv\Scripts\activate.bat
pip install "setuptools<70" wheel
pip install "dvc>=3"
if not exist ".git" git init
if not exist ".dvc" dvc init
rem  Los datos pesados entran como punteros .dvc; los JSON chicos tambien (asi cada version queda fijada en git).
dvc add datos\clips datos\grabaciones datos\manifest.json datos\etiquetas.json datos\seleccion_entrenamiento.json
echo.
echo  Listo. Sigue con docs\GUIA_ETAPA3.md (seccion 2: elegir el remoto).
pause
