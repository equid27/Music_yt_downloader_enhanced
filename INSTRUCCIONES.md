# 🎵 Audio Downloader V2 - Instrucciones Completas

## 📋 Pasos de Instalación

### 1. 📥 Verificar Python
```bash
python --version
```
**Requisito**: Python 3.7 o superior
- Si no tienes Python: Descarga desde [python.org](https://python.org)

### 2. 🔧 Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. ⚡ Instalar FFmpeg (OBLIGATORIO)
```bash
.\instalar_ffmpeg.bat
```
**O manualmente**: Descargar FFmpeg desde [ffmpeg.org](https://ffmpeg.org)

### 4. ✅ Verificar Instalación
```bash
ffmpeg -version
```

## 🚀 Cómo Usar

### Opción 1: Interfaz Gráfica (Recomendado)
```bash
python audio_gui_v2.py
```
**O ejecutar**: `gui_v2.bat`

### Opción 2: Línea de Comandos
```bash
python audio_downloader_v2.py --interactive
```
**O ejecutar**: `audio_v2.bat`

## 📁 Formatos Disponibles

| Formato | Calidad | Tamaño | Uso Recomendado |
|---------|---------|--------|-----------------|
| **FLAC** | Sin pérdida | Grande | Producción, DJ profesional |
| **WAV** | Sin compresión | Muy grande | Estudios, máxima calidad |
| **MP3** | 320kbps | Mediano | Uso general, compatibilidad |

## 🎯 Ejemplos de Uso

### Línea de Comandos
```bash
# Modo interactivo
python audio_downloader_v2.py --interactive

# Descargar en FLAC
python audio_downloader_v2.py "URL_DE_YOUTUBE" --format flac

# Descargar playlist en WAV
python audio_downloader_v2.py "URL_DE_PLAYLIST" --format wav

# Cambiar directorio de salida
python audio_downloader_v2.py "URL" --output "mi_musica" --format mp3
```

### Interfaz Gráfica
1. Ejecuta `gui_v2.bat`
2. Pega la URL de YouTube
3. Selecciona formato (FLAC, WAV, MP3)
4. Elige directorio de salida
5. Haz clic en "Descargar Audio" o "Descargar Playlist"

## 📂 Estructura del Proyecto

```
descargador music/
├── audio_downloader_v2.py    # Línea de comandos
├── audio_gui_v2.py           # Interfaz gráfica
├── gui_v2.bat                # Inicio rápido GUI
├── audio_v2.bat              # Inicio rápido CLI
├── instalar_ffmpeg.bat       # Instalador FFmpeg
├── requirements.txt          # Dependencias
├── ffmpeg.exe                # Conversor de audio
├── ffprobe.exe               # Analizador de audio
└── audio_downloads/          # Carpeta de descargas
```

## 🔧 Solución de Problemas

### Error: "yt-dlp no está instalado"
```bash
pip install --upgrade yt-dlp
```

### Error: "FFmpeg no encontrado"
```bash
.\instalar_ffmpeg.bat
```

### Error: "Contenido no tiene audio"
- Verifica que la URL sea de un video con audio
- Algunos videos pueden estar restringidos por región

### Error de red
- Verifica tu conexión a internet
- Algunos videos pueden estar bloqueados

## ⚙️ Configuración Avanzada

### Cambiar Calidad de Audio
Edita `audio_downloader_v2.py` línea de postprocesadores:
```python
'preferredquality': '0',  # Para FLAC/WAV (máxima)
'preferredquality': '320',  # Para MP3 (320kbps)
```

### Cambiar Formato de Salida
Modifica el postprocesador:
```python
'preferredcodec': 'flac',  # o 'wav', 'mp3'
```

## 📊 Comparación de Calidades

| Formato | Bitrate | Tamaño (4 min) | Calidad |
|---------|---------|----------------|---------|
| FLAC | Variable | ~25-40 MB | Perfecta |
| WAV | 1411 kbps | ~40-50 MB | Perfecta |
| MP3 320 | 320 kbps | ~10 MB | Muy alta |

## 🎵 Tipos de URLs Soportadas

- Videos individuales: `https://www.youtube.com/watch?v=VIDEO_ID`
- Playlists: `https://www.youtube.com/playlist?list=PLAYLIST_ID`
- URLs cortas: `https://youtu.be/VIDEO_ID`
- Videos en canales con playlists

## 💡 Consejos

- **Para DJ**: Usa FLAC o WAV
- **Para escuchar**: MP3 320kbps es suficiente
- **Playlists grandes**: Usa la interfaz gráfica para mejor seguimiento
- **Contenido restringido**: Algunos videos no están disponibles por región

## 🆘 Soporte

Si tienes problemas:
1. Verifica que Python y FFmpeg estén instalados
2. Actualiza yt-dlp: `pip install --upgrade yt-dlp`
3. Verifica que la URL sea válida
4. Revisa los logs para más detalles

---

**Nota**: Este software es para uso personal y educativo. Respeta los derechos de autor. 