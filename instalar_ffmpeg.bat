@echo off
echo ========================================
echo  Instalando FFmpeg para maxima calidad
echo ========================================
echo.

echo Descargando FFmpeg...
curl -L -o ffmpeg.zip "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"

if errorlevel 1 (
    echo ERROR: No se pudo descargar FFmpeg
    echo Intentando metodo alternativo...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile 'ffmpeg.zip'}"
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
echo Limpiando archivos temporales...
del "ffmpeg.zip"

echo.
echo ========================================
echo  FFmpeg instalado correctamente!
echo ========================================
echo.
echo Ahora puedes usar el descargador con maxima calidad:
echo   python youtube_music_downloader.py --interactive
echo.
pause 