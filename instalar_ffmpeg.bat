@echo off
echo ========================================
echo  Instalando FFmpeg para maxima calidad
echo ========================================
echo.

REM Verificar si FFmpeg ya existe
if exist "ffmpeg.exe" if exist "ffprobe.exe" (
    echo ✅ FFmpeg ya esta instalado
    goto :fin
)

echo 📥 Descargando FFmpeg...
echo.
echo Intentando descargar desde GitHub...
curl -L -o ffmpeg.zip "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"

if errorlevel 1 (
    echo ❌ ERROR: No se pudo descargar desde GitHub
    echo 📥 Intentando método alternativo...
    powershell -Command "& {try { Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile 'ffmpeg.zip' -ErrorAction Stop; Write-Host '✅ Descarga completada' } catch { Write-Host '❌ Error en descarga alternativa'; exit 1 }}"
    
    if errorlevel 1 (
        echo ❌ ERROR: Falló la descarga desde ambas fuentes
        echo.
        echo 💡 Soluciones posibles:
        echo   1. Verificar conexión a Internet
        echo   2. Descargar manualmente desde: https://ffmpeg.org/download.html
        echo   3. Colocar ffmpeg.exe y ffprobe.exe en esta carpeta
        echo.
        pause
        exit /b 1
    )
)

echo.
echo Extrayendo FFmpeg...
powershell -Command "& {Expand-Archive -Path 'ffmpeg.zip' -DestinationPath '.' -Force}"

echo.
echo Configurando FFmpeg...
if exist "ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe" (
    copy "ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe" "ffmpeg.exe"
    copy "ffmpeg-master-latest-win64-gpl\bin\ffprobe.exe" "ffprobe.exe"
    rmdir /s /q "ffmpeg-master-latest-win64-gpl"
) else if exist "ffmpeg-*\bin\ffmpeg.exe" (
    for /d %%i in (ffmpeg-*) do (
        copy "%%i\bin\ffmpeg.exe" "ffmpeg.exe"
        copy "%%i\bin\ffprobe.exe" "ffprobe.exe"
        rmdir /s /q "%%i"
    )
)

echo.
echo 🧹 Limpiando archivos temporales...
if exist "ffmpeg.zip" del "ffmpeg.zip"

REM Verificar que la instalación fue exitosa
if exist "ffmpeg.exe" if exist "ffprobe.exe" (
    echo.
    echo ========================================
    echo  ✅ FFmpeg instalado correctamente!
    echo ========================================
    echo.
    echo Archivos instalados:
    echo   - ffmpeg.exe
    echo   - ffprobe.exe
    echo.
) else (
    echo.
    echo ❌ ERROR: La instalación no se completó correctamente
    echo.
    echo Verifica que los archivos ffmpeg.exe y ffprobe.exe estén presentes.
    pause
    exit /b 1
)

:fin
echo Ahora puedes usar el descargador con maxima calidad:
echo   🎨 GUI: gui_v2.bat
echo   💻 CLI: audio_v2.bat
echo.
pause 