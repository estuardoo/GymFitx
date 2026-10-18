@echo off
setlocal
title GYMFITX - Diagnostico de camara (sin Python, sin OpenCV)
cd /d "%~dp0"

echo ============================================================
echo  1) Camaras que WINDOWS reconoce como hardware
echo ============================================================
echo.
powershell -NoProfile -Command "Get-PnpDevice -Class Camera,Image -ErrorAction SilentlyContinue | Format-Table -AutoSize FriendlyName,Status,InstanceId"
echo.
echo  Si esta lista sale VACIA: Windows no ve ninguna camara conectada
echo  (cable/puerto USB, o el driver no quedo instalado). No es un
echo  problema de GYMFITX ni de Python.
echo.
echo  Si aparece pero "Status" dice algo distinto de "OK" (Error, Unknown,
echo  Degraded): el driver de esa camara tiene un problema. Se arregla desde
echo  el Administrador de dispositivos (click derecho - Actualizar driver),
echo  no desde GYMFITX.
echo.
pause

echo.
echo ============================================================
echo  2) Programas que podrian tener la camara ocupada ahora mismo
echo ============================================================
echo.
tasklist /FI "IMAGENAME eq Teams.exe" /FI "IMAGENAME eq ms-teams.exe" /FI "IMAGENAME eq Zoom.exe" /FI "IMAGENAME eq Skype.exe" /FI "IMAGENAME eq Discord.exe" /FI "IMAGENAME eq obs64.exe" /FI "IMAGENAME eq WhatsApp.exe" 2>nul | findstr /I "exe"
if errorlevel 1 echo   (ninguno de los sospechosos habituales esta corriendo)
echo.
echo  Si alguno de estos aparecio arriba y lo tenias abierto: cierralo del
echo  todo (no solo minimizado) y vuelve a probar GYMFITX.
echo.
pause

echo.
echo ============================================================
echo  3) Prueba de fuego: la app Camara de Windows (nada de GYMFITX aqui)
echo ============================================================
echo.
echo  Se va a abrir la app "Camara" de Windows. Si AHI TAMPOCO se ve imagen,
echo  el problema es 100%% de Windows/driver/permisos, no de este proyecto.
echo  Si en la app Camara SI se ve imagen, entonces el problema esta entre
echo  Python/OpenCV y la camara -- eso ya lo podemos arreglar en el codigo.
echo.
pause
start microsoft.windows.camera:
echo.
echo  (si no se abrio nada: es posible que tu Windows no tenga la app Camara
echo   instalada. En ese caso avisame y probamos otra cosa.)
echo.

echo ============================================================
echo  4) Recordatorio: permiso de camara para apps de escritorio
echo ============================================================
echo.
echo  Configuracion (Win+I) - Privacidad y seguridad - Camara
echo    - "Acceso a la camara" debe estar en ON
echo    - "Permitir que las aplicaciones de escritorio accedan a la camara"
echo      debe estar en ON  (esta es la que suele estar apagada)
echo.
echo  Python/GYMFITX cae en la categoria "aplicacion de escritorio", no en
echo  la lista de apps individuales de arriba -- por eso este interruptor
echo  especifico es el que casi siempre bloquea a OpenCV aunque la camara
echo  funcione perfecto en todo lo demas.
echo.
pause
