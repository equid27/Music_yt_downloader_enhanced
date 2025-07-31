#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audio Downloader V2 - GUI
Interfaz gráfica moderna para el descargador de audio mejorado
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import os
from pathlib import Path
import yt_dlp
from colorama import init, Fore, Style
import time

# Inicializar colorama
init(autoreset=True)

class AudioGUIV2:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Audio Downloader V2 - SOLO AUDIO")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Configurar estilo moderno
        style = ttk.Style()
        style.theme_use('clam')
        
        # Variables
        self.output_dir = tk.StringVar(value=str(Path.cwd() / "audio_downloads"))
        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar(value="flac")
        self.is_downloading = False
        self.download_queue = queue.Queue()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="🎵 Audio Downloader V2", 
                               font=("Arial", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, text="SOLO AUDIO - Máxima Calidad - Versión Mejorada", 
                                  font=("Arial", 12), foreground="blue")
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Frame de información
        info_frame = ttk.LabelFrame(main_frame, text="🔧 Información del Sistema", padding="10")
        info_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        info_frame.columnconfigure(1, weight=1)
        
        # Verificar versiones
        try:
            import yt_dlp
            yt_version = yt_dlp.version.__version__
            yt_status = f"✅ yt-dlp v{yt_version}"
            yt_color = "green"
        except:
            yt_status = "❌ yt-dlp no disponible"
            yt_color = "red"
            
        try:
            import subprocess
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            ff_status = "✅ FFmpeg disponible"
            ff_color = "green"
        except:
            ff_status = "❌ FFmpeg no disponible"
            ff_color = "red"
        
        ttk.Label(info_frame, text=yt_status, foreground=yt_color).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(info_frame, text=ff_status, foreground=ff_color).grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        
        # URL Input
        url_frame = ttk.LabelFrame(main_frame, text="🔗 URL de YouTube", padding="10")
        url_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        url_frame.columnconfigure(0, weight=1)
        
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=80, font=("Arial", 11))
        url_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        paste_btn = ttk.Button(url_frame, text="📋 Pegar", command=self.paste_url, width=8)
        paste_btn.grid(row=0, column=1)
        
        # Frame de configuración
        config_frame = ttk.LabelFrame(main_frame, text="⚙️ Configuración", padding="10")
        config_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        config_frame.columnconfigure(1, weight=1)
        
        # Formato de audio
        ttk.Label(config_frame, text="📁 Formato de audio:").grid(row=0, column=0, sticky=tk.W, pady=5)
        format_frame = ttk.Frame(config_frame)
        format_frame.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        flac_radio = ttk.Radiobutton(format_frame, text="🎵 FLAC (Sin pérdida)", 
                                    variable=self.format_var, value="flac")
        flac_radio.pack(side=tk.LEFT, padx=(0, 15))
        
        wav_radio = ttk.Radiobutton(format_frame, text="🎼 WAV (Profesional)", 
                                   variable=self.format_var, value="wav")
        wav_radio.pack(side=tk.LEFT, padx=(0, 15))
        
        mp3_radio = ttk.Radiobutton(format_frame, text="🎧 MP3 (320kbps)", 
                                   variable=self.format_var, value="mp3")
        mp3_radio.pack(side=tk.LEFT)
        
        # Directorio de salida
        ttk.Label(config_frame, text="📂 Directorio de salida:").grid(row=1, column=0, sticky=tk.W, pady=5)
        output_frame = ttk.Frame(config_frame)
        output_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        output_frame.columnconfigure(0, weight=1)
        
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir, width=60)
        output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        browse_btn = ttk.Button(output_frame, text="📁 Examinar", command=self.browse_directory, width=12)
        browse_btn.grid(row=0, column=1)
        
        # Botones de descarga
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        self.download_btn = ttk.Button(button_frame, text="🎵 Descargar Audio", 
                                      command=self.download_single, width=20)
        self.download_btn.pack(side=tk.LEFT, padx=10)
        
        self.playlist_btn = ttk.Button(button_frame, text="🎼 Descargar Playlist", 
                                      command=self.download_playlist, width=20)
        self.playlist_btn.pack(side=tk.LEFT, padx=10)
        
        self.stop_btn = ttk.Button(button_frame, text="⏹️ Detener", 
                                  command=self.stop_download, state=tk.DISABLED, width=15)
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        
        # Barra de progreso
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.status_label = ttk.Label(progress_frame, text="Listo para descargar", foreground="green")
        self.status_label.grid(row=0, column=1)
        
        # Área de log
        log_frame = ttk.LabelFrame(main_frame, text="📋 Log de Descarga", padding="10")
        log_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, width=90, 
                                                 font=("Consolas", 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar expansión
        main_frame.rowconfigure(7, weight=1)
        
        # Configurar eventos
        url_entry.bind('<Return>', lambda e: self.download_single())
        url_entry.bind('<Control-v>', lambda e: self.paste_url())
        
        # Log inicial
        self.log_message("🎵 Audio Downloader V2 iniciado")
        self.log_message("✅ Solo se descargará AUDIO en máxima calidad")
        self.log_message("🔧 Versión mejorada con mejor manejo de errores")
        self.log_message("💡 Pega una URL de YouTube y selecciona el formato deseado")
        
    def paste_url(self):
        """Pega la URL del portapapeles"""
        try:
            clipboard_content = self.root.clipboard_get()
            if clipboard_content and ('youtube.com' in clipboard_content or 'youtu.be' in clipboard_content):
                self.url_var.set(clipboard_content.strip())
                self.log_message(f"📋 URL pegada: {clipboard_content[:50]}...")
            else:
                self.log_message("⚠️ No se encontró una URL válida de YouTube en el portapapeles")
        except tk.TclError:
            self.log_message("❌ Error al acceder al portapapeles")
    
    def browse_directory(self):
        directory = filedialog.askdirectory(initialdir=self.output_dir.get())
        if directory:
            self.output_dir.set(directory)
            self.log_message(f"📂 Directorio cambiado a: {directory}")
    
    def log_message(self, message):
        """Agrega un mensaje al log con timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.log_text.insert(tk.END, formatted_message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_status(self, message, color="blue"):
        """Actualiza el label de estado"""
        self.status_label.config(text=message, foreground=color)
    
    def download_single(self):
        """Descarga un solo audio"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Por favor ingresa una URL de YouTube")
            return
        
        if not ('youtube.com' in url or 'youtu.be' in url):
            messagebox.showerror("Error", "Por favor ingresa una URL válida de YouTube")
            return
        
        self.start_download(url, is_playlist=False)
    
    def download_playlist(self):
        """Descarga una playlist"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Por favor ingresa una URL de YouTube")
            return
        
        if not ('youtube.com' in url or 'youtu.be' in url):
            messagebox.showerror("Error", "Por favor ingresa una URL válida de YouTube")
            return
        
        self.start_download(url, is_playlist=True)
    
    def start_download(self, url, is_playlist=False):
        """Inicia el proceso de descarga en un hilo separado"""
        if self.is_downloading:
            return
        
        self.is_downloading = True
        self.download_btn.config(state=tk.DISABLED)
        self.playlist_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress.start()
        
        if is_playlist:
            self.update_status("Descargando playlist...", "orange")
        else:
            self.update_status("Descargando audio...", "orange")
        
        # Limpiar log anterior
        self.log_text.delete(1.0, tk.END)
        self.log_message("🚀 Iniciando descarga...")
        
        # Iniciar hilo de descarga
        download_thread = threading.Thread(
            target=self.download_worker, 
            args=(url, is_playlist)
        )
        download_thread.daemon = True
        download_thread.start()
    
    def stop_download(self):
        """Detiene la descarga actual"""
        self.is_downloading = False
        self.progress.stop()
        self.download_btn.config(state=tk.NORMAL)
        self.playlist_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.update_status("Descarga detenida", "red")
        self.log_message("⏹️ Descarga detenida por el usuario")
    
    def download_worker(self, url, is_playlist=False):
        """Trabajador de descarga que se ejecuta en un hilo separado"""
        try:
            format_type = self.format_var.get()
            output_dir = Path(self.output_dir.get())
            output_dir.mkdir(exist_ok=True)
            
            self.log_message(f"📁 Formato: {format_type.upper()}")
            self.log_message(f"📂 Directorio: {output_dir.absolute()}")
            
            # Configuración mejorada
            base_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(output_dir / '%(title)s.%(ext)s'),
                'writethumbnail': False,
                'writesubtitles': False,
                'writeautomaticsub': False,
                'writedescription': False,
                'writeinfojson': False,
                'writeannotations': False,
                'keepvideo': False,
                'ignoreerrors': True,
                'no_warnings': False,
                'extractaudio': True,
                'audioformat': format_type,
                'prefer_ffmpeg': True,
                'noplaylist': not is_playlist,
                'nocheckcertificate': True,
                'geo_bypass': True,
                'extractor_retries': 3,
                'fragment_retries': 3,
            }
            
            # Configurar postprocesador según el formato
            if format_type == "flac":
                base_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'flac',
                    'preferredquality': '0',
                }]
            elif format_type == "wav":
                base_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                    'preferredquality': '0',
                }]
            else:  # mp3
                base_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }]
            
            # Callback para progreso
            def progress_hook(d):
                if not self.is_downloading:
                    return
                    
                if d['status'] == 'downloading':
                    if 'total_bytes' in d and d['total_bytes']:
                        percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                        filename = d.get('filename', 'Unknown')
                        title = filename.split('/')[-1] if '/' in filename else filename
                        self.log_message(f"⬇️ Descargando: {title} - {percent:.1f}%")
                    else:
                        filename = d.get('filename', 'Unknown')
                        self.log_message(f"⬇️ Descargando: {filename}")
                elif d['status'] == 'finished':
                    filename = d.get('filename', 'Unknown')
                    title = filename.split('/')[-1] if '/' in filename else filename
                    self.log_message(f"✅ Descargado: {title}")
                elif d['status'] == 'error':
                    self.log_message(f"❌ Error: {d.get('error', 'Unknown error')}")
            
            base_opts['progress_hooks'] = [progress_hook]
            
            with yt_dlp.YoutubeDL(base_opts) as ydl:
                self.log_message(f"🎵 Procesando: {url}")
                
                try:
                    info = ydl.extract_info(url, download=True)
                    
                    if is_playlist and 'entries' in info:
                        total_videos = len([e for e in info['entries'] if e is not None])
                        self.log_message(f"🎼 Playlist completada. Total: {total_videos} audios")
                    else:
                        title = info.get('title', 'Unknown')
                        self.log_message(f"✅ Audio completado: {title}")
                    
                    self.root.after(0, lambda: self.update_status("✅ Descarga completada", "green"))
                    
                except yt_dlp.utils.DownloadError as e:
                    error_msg = str(e)
                    if "only images are available" in error_msg.lower():
                        self.log_message("❌ Error: Este contenido no tiene audio")
                        self.log_message("💡 Intenta con un video que tenga audio")
                    else:
                        self.log_message(f"❌ Error de descarga: {error_msg}")
                    
                    self.root.after(0, lambda: self.update_status("❌ Error en descarga", "red"))
                
        except Exception as e:
            self.log_message(f"❌ Error inesperado: {str(e)}")
            self.root.after(0, lambda: self.update_status("❌ Error inesperado", "red"))
        finally:
            # Restaurar UI
            self.root.after(0, self.download_finished)
    
    def download_finished(self):
        """Llamado cuando termina la descarga"""
        self.is_downloading = False
        self.progress.stop()
        self.download_btn.config(state=tk.NORMAL)
        self.playlist_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.log_message("🏁 Proceso finalizado")

def main():
    # Verificar dependencias básicas
    try:
        import yt_dlp
    except ImportError:
        messagebox.showerror("Error", 
                           "yt-dlp no está instalado.\n"
                           "Ejecuta: pip install --upgrade yt-dlp")
        return
    
    # Crear ventana principal
    root = tk.Tk()
    app = AudioGUIV2(root)
    
    # Centrar ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Iniciar aplicación
    root.mainloop()

if __name__ == "__main__":
    main() 