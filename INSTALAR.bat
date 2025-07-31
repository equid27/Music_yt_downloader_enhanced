@echo off
title Audio Downloader V2 - Instalador
color 0A

echo.
echo ========================================
echo   AUDIO DOWNLOADER V2 - INSTALADOR
echo ========================================
echo.
echo Este script instalara todo lo necesario:
echo  - Dependencias de Python
echo  - FFmpeg para conversion de audio
echo.

pause

echo.
echo [1/3] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no encontrado
    echo.
    echo Por favor instala Python desde: https://python.org
    echo Asegurate de marcar "Add to PATH" durante la instalacion
    pause
    exit /b 1
)
echo ✅ Python encontrado

echo.
echo [2/3] Instalando dependencias de Python...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ ERROR: No se pudieron instalar las dependencias
    echo.
    echo Intentando con pip alternativo...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ ERROR: Fallo la instalacion de dependencias
        pause
        exit /b 1
    )
)
echo ✅ Dependencias instaladas

echo.
echo [3/3] Instalando FFmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo FFmpeg no encontrado. Instalando...
    call instalar_ffmpeg.bat
) else (
    echo ✅ FFmpeg ya esta instalado
)

echo.
echo ========================================
echo   INSTALACION COMPLETADA EXITOSAMENTE
echo ========================================
echo.
echo Para usar el descargador:
echo.
echo  🎨 INTERFAZ GRAFICA (Recomendado):
echo     gui_v2.bat
echo.
echo  💻 LINEA DE COMANDOS:
echo     audio_v2.bat
echo.
echo  📋 INSTRUCCIONES COMPLETAS:
echo     INSTRUCCIONES.md
echo.
pause 