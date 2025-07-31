# 🎵 Music YouTube Downloader Enhanced V2

Un descargador de música de YouTube mejorado con interfaz gráfica y soporte para alta calidad de audio.

## ✨ Características

- 🎨 **Interfaz gráfica amigable** para uso fácil
- 💻 **Modo línea de comandos** para usuarios avanzados
- 🔊 **Alta calidad de audio** con soporte FFmpeg
- 📋 **Descarga por lotes** desde archivos de texto
- 🎯 **Múltiples formatos** de salida (MP3, WAV, FLAC, etc.)
- 🚀 **Instalación automática** de dependencias

## 🚀 Instalación Rápida

### Opción 1: Instalación Automática (Recomendada)

1. **Clona o descarga** este repositorio
2. **Ejecuta** `INSTALAR.bat` como administrador
3. **¡Listo!** El instalador descargará automáticamente:
   - Dependencias de Python
   - FFmpeg (para conversión de audio)

### Opción 2: Instalación Manual

```bash
# 1. Instalar dependencias de Python
pip install -r requirements.txt

# 2. Instalar FFmpeg
# Ejecutar: instalar_ffmpeg.bat
# O descargar manualmente desde: https://ffmpeg.org/download.html
```

## 📖 Uso

### 🎨 Interfaz Gráfica (Recomendada)
```bash
gui_v2.bat
```

### 💻 Línea de Comandos
```bash
audio_v2.bat
```

### 🐍 Python Directo
```bash
# GUI
python audio_gui_v2.py

# CLI
python audio_downloader_v2.py
```

## 📋 Instrucciones Detalladas

Para instrucciones completas y resolución de problemas, consulta: `INSTRUCCIONES.md`

## ⚙️ Requisitos del Sistema

- **Windows** 10/11
- **Python** 3.7+ (con pip)
- **Conexión a Internet** (para descargar FFmpeg automáticamente)

## 🔧 Archivos Importantes

- `ffmpeg.exe` y `ffprobe.exe` - Se descargan automáticamente
- No es necesario incluirlos en el repositorio
- El instalador los obtiene de fuentes oficiales

## 📝 Notas para Desarrolladores

Este proyecto utiliza descarga automática de FFmpeg para evitar incluir archivos ejecutables grandes en el repositorio. Los archivos `.exe` están excluidos en `.gitignore` y se descargan durante la instalación.