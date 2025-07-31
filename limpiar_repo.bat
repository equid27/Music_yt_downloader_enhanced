@echo off
echo ========================================
echo  PREPARANDO REPOSITORIO PARA GITHUB
echo ========================================
echo.

echo 🗑️  Removiendo archivos .exe del repositorio...

REM Remover archivos del índice de git si ya están trackeados
git rm --cached ffmpeg.exe 2>nul
git rm --cached ffprobe.exe 2>nul

echo ✅ Archivos .exe removidos del repositorio
echo.

echo 📝 Agregando cambios al repositorio...
git add .gitignore
git add README.md
git add instalar_ffmpeg.bat

echo.
echo ✅ Preparación completada!
echo.
echo 📋 Próximos pasos:
echo   1. git commit -m "feat: Add automatic FFmpeg download, remove exe files from repo"
echo   2. git push origin main
echo.
echo 💡 Los archivos .exe ahora se descargarán automáticamente durante la instalación
echo    y no ocuparán espacio en GitHub.
echo.
pause