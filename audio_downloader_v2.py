#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audio Downloader V2 - SOLO AUDIO en Máxima Calidad
Versión mejorada con mejor manejo de errores y compatibilidad actualizada
"""

import os
import sys
import argparse
from pathlib import Path
import yt_dlp
from colorama import init, Fore, Style
import time

# Inicializar colorama para colores en Windows
init(autoreset=True)

class AudioDownloaderV2:
    def __init__(self, output_dir="audio_downloads", format_type="flac"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.format_type = format_type
        
        # Configuración mejorada SOLO AUDIO
        base_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            
            # SOLO AUDIO
            'writethumbnail': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'writedescription': False,
            'writeinfojson': False,
            'writeannotations': False,
            'keepvideo': False,
            
            # CONFIGURACIONES MEJORADAS
            'ignoreerrors': True,  # Continuar si hay errores en algunos videos
            'no_warnings': False,
            'extractaudio': True,
            'audioformat': format_type,
            'prefer_ffmpeg': True,
            'noplaylist': False,
            
            # CONFIGURACIONES ADICIONALES PARA MEJOR COMPATIBILIDAD
            'nocheckcertificate': True,
            'geo_bypass': True,
            'age_limit': None,
            'cookiesfrombrowser': None,
            
            # CONFIGURACIONES PARA EVITAR ERRORES DE YOUTUBE
            'extractor_retries': 3,
            'fragment_retries': 3,
            'retry_sleep_functions': {
                'http': lambda n: min(4 ** n, 30),
                'fragment': lambda n: min(4 ** n, 30),
                'extractor': lambda n: min(4 ** n, 30),
            },
        }
        
        # Configurar postprocesador según el formato
        if format_type == "flac":
            base_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'flac',
                'preferredquality': '0',  # Máxima calidad sin compresión
            }]
        elif format_type == "wav":
            base_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '0',  # Máxima calidad sin compresión
            }]
        else:  # mp3
            base_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',  # Máxima calidad MP3
            }]
        
        self.ydl_opts = base_opts
    
    def download_audio(self, url):
        """Descarga SOLO el audio de una URL con manejo mejorado de errores"""
        try:
            print(f"{Fore.CYAN}🎵 Descargando SOLO AUDIO: {url}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}📁 Formato: {self.format_type.upper()}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}📂 Directorio: {self.output_dir.absolute()}{Style.RESET_ALL}")
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                try:
                    # Intentar descargar directamente primero
                    print(f"{Fore.BLUE}⬇️ Iniciando descarga...{Style.RESET_ALL}")
                    ydl.download([url])
                    print(f"{Fore.GREEN}✅ Descarga completada exitosamente{Style.RESET_ALL}")
                    return True
                    
                except yt_dlp.utils.DownloadError as e:
                    error_msg = str(e).lower()
                    
                    if "only images are available" in error_msg:
                        print(f"{Fore.RED}❌ Error: Este video solo tiene imágenes disponibles{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}💡 Sugerencia: Intenta con otro video que tenga audio{Style.RESET_ALL}")
                        return False
                    
                    elif "precondition check failed" in error_msg:
                        print(f"{Fore.YELLOW}⚠️ Error de YouTube API, reintentando con configuración alternativa...{Style.RESET_ALL}")
                        return self.download_with_fallback(url)
                    
                    elif "private video" in error_msg:
                        print(f"{Fore.RED}❌ Error: Video privado o no disponible{Style.RESET_ALL}")
                        return False
                    
                    else:
                        print(f"{Fore.RED}❌ Error de descarga: {e}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}🔄 Intentando con configuración alternativa...{Style.RESET_ALL}")
                        return self.download_with_fallback(url)
                
        except Exception as e:
            print(f"{Fore.RED}❌ Error inesperado: {e}{Style.RESET_ALL}")
            return False
    
    def download_with_fallback(self, url):
        """Descarga con configuración alternativa para casos problemáticos"""
        try:
            print(f"{Fore.BLUE}🔄 Intentando descarga con configuración alternativa...{Style.RESET_ALL}")
            
            # Configuración alternativa más simple
            fallback_opts = {
                'format': 'worst[ext=m4a]/worst[ext=webm]/worst',  # Usar peor calidad si es necesario
                'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
                'writethumbnail': False,
                'writesubtitles': False,
                'writeautomaticsub': False,
                'ignoreerrors': True,
                'no_warnings': True,
                'extractaudio': True,
                'prefer_ffmpeg': True,
                'nocheckcertificate': True,
                'postprocessors': self.ydl_opts['postprocessors'],
            }
            
            with yt_dlp.YoutubeDL(fallback_opts) as ydl:
                ydl.download([url])
                print(f"{Fore.GREEN}✅ Descarga completada con configuración alternativa{Style.RESET_ALL}")
                return True
                
        except Exception as e:
            print(f"{Fore.RED}❌ Error en descarga alternativa: {e}{Style.RESET_ALL}")
            return False
    
    def download_playlist(self, url):
        """Descarga una playlist con manejo individual de errores"""
        try:
            print(f"{Fore.CYAN}🎼 Procesando playlist...{Style.RESET_ALL}")
            
            # Obtener información de la playlist
            with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
                playlist_info = ydl.extract_info(url, download=False)
                
                if 'entries' not in playlist_info:
                    print(f"{Fore.RED}❌ No se pudo procesar la playlist{Style.RESET_ALL}")
                    return False
                
                entries = playlist_info['entries']
                total = len(entries)
                successful = 0
                failed = 0
                
                print(f"{Fore.CYAN}📋 Encontrados {total} videos en la playlist{Style.RESET_ALL}")
                
                for i, entry in enumerate(entries, 1):
                    if entry is None:
                        continue
                    
                    video_url = entry.get('url') or f"https://www.youtube.com/watch?v={entry['id']}"
                    title = entry.get('title', 'Unknown')
                    
                    print(f"\n{Fore.BLUE}[{i}/{total}] {title}{Style.RESET_ALL}")
                    
                    if self.download_audio(video_url):
                        successful += 1
                    else:
                        failed += 1
                        print(f"{Fore.YELLOW}⏭️ Continuando con el siguiente video...{Style.RESET_ALL}")
                    
                    # Pequeña pausa entre descargas
                    time.sleep(1)
                
                print(f"\n{Fore.GREEN}🎯 RESUMEN DE PLAYLIST:{Style.RESET_ALL}")
                print(f"{Fore.GREEN}✅ Exitosos: {successful}{Style.RESET_ALL}")
                print(f"{Fore.RED}❌ Fallidos: {failed}{Style.RESET_ALL}")
                
                return successful > 0
                
        except Exception as e:
            print(f"{Fore.RED}❌ Error procesando playlist: {e}{Style.RESET_ALL}")
            return False

def main():
    parser = argparse.ArgumentParser(
        description="🎵 Audio Downloader V2 - SOLO AUDIO en Máxima Calidad",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🎵 Ejemplos de uso:
  python audio_downloader_v2.py --interactive
  python audio_downloader_v2.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --format flac
  python audio_downloader_v2.py "https://www.youtube.com/playlist?list=PLxxxxxxxx" --format wav

📁 Formatos disponibles:
  flac  - Formato sin pérdida (máxima calidad)
  wav   - Formato sin compresión (calidad profesional)
  mp3   - MP3 320kbps (alta calidad comprimida)
        """
    )
    
    parser.add_argument('url', nargs='?', help='URL de YouTube (video o playlist)')
    parser.add_argument('-o', '--output', default='audio_downloads', 
                       help='Directorio de salida (default: audio_downloads)')
    parser.add_argument('-f', '--format', choices=['flac', 'wav', 'mp3'], 
                       default='flac', help='Formato de audio (default: flac)')
    parser.add_argument('--interactive', action='store_true',
                       help='Modo interactivo')
    
    args = parser.parse_args()
    
    # Verificar dependencias
    try:
        import yt_dlp
        print(f"{Fore.GREEN}✅ yt-dlp versión: {yt_dlp.version.__version__}{Style.RESET_ALL}")
    except ImportError:
        print(f"{Fore.RED}❌ Error: yt-dlp no está instalado.{Style.RESET_ALL}")
        print("Ejecuta: pip install --upgrade yt-dlp")
        sys.exit(1)
    
    # Verificar FFmpeg
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print(f"{Fore.GREEN}✅ FFmpeg disponible{Style.RESET_ALL}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Fore.RED}❌ Error: FFmpeg no está instalado.{Style.RESET_ALL}")
        print("Ejecuta: .\\instalar_ffmpeg.bat")
        sys.exit(1)
    
    # Crear descargador
    downloader = AudioDownloaderV2(args.output, args.format)
    
    print(f"{Fore.CYAN}🎚️ === AUDIO DOWNLOADER V2 - SOLO AUDIO ==={Style.RESET_ALL}")
    print(f"{Fore.GREEN}✅ GARANTIZADO: Solo se descarga AUDIO{Style.RESET_ALL}")
    print(f"{Fore.GREEN}🔧 Versión mejorada con mejor manejo de errores{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📁 Formato: {args.format.upper()}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📂 Directorio: {downloader.output_dir.absolute()}{Style.RESET_ALL}")
    
    if args.interactive or not args.url:
        print(f"\n{Fore.YELLOW}🎵 Modo interactivo - Solo AUDIO{Style.RESET_ALL}")
        
        while True:
            url = input(f"\n{Fore.YELLOW}🎵 URL de YouTube (o 'quit' para salir): {Style.RESET_ALL}")
            
            if url.lower() in ['quit', 'exit', 'salir', 'q']:
                break
            
            if not url.strip():
                continue
            
            print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            
            # Detectar si es playlist
            if 'playlist' in url or 'list=' in url:
                downloader.download_playlist(url.strip())
            else:
                downloader.download_audio(url.strip())
            
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    else:
        # Modo no interactivo
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        if 'playlist' in args.url or 'list=' in args.url:
            downloader.download_playlist(args.url)
        else:
            downloader.download_audio(args.url)
            
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}🎵 Proceso completado!{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 