from yt_dlp import YoutubeDL
from os import startfile
from pywebio.input import input
from pywebio.output import put_text
from pywebio import start_server
import webbrowser
import os
import tkinter as tk
from tkinter import filedialog

def video_download():
    while True:
        video_link = input("Informe o Link do vídeo:").strip()
        
        if video_link.startswith("http://") or video_link.startswith("https://"):
        
            # Abrir o explorador de arquivos para escolher o diretório
            root = tk.Tk()
            root.withdraw()  
            download_path = filedialog.askdirectory(title="Escolha a pasta de destino")  
            
            if not download_path:
                put_text("Nenhum diretório foi selecionado. Tente novamente.").style('color: red; font-size: 20px')
                continue

            try:
                put_text("Fazendo Download do vídeo...").style('color: red; font-size: 20px')
                
                download_options = {
                    'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                    'format': 'bestvideo+bestaudio/best',
                    'merge_output_format': 'mp4',
                    'ffmpeg_location': r'C:\Users\ffmpeg\bin',  # Caminho do FFmpeg
                }
                with YoutubeDL(download_options) as ydl:
                    ydl.download([video_link])
                
                put_text("Vídeo baixado com sucesso!").style('color: green; font-size: 20px')
                
                startfile(download_path)
                break

            except Exception as e:
                put_text(f"Erro: {e}").style('color: red; font-size: 20px')
        else:
            put_text("URL inválida. Por favor, insira um link válido do YouTube.").style('color: orange; font-size: 20px')

if __name__ == "__main__":
    host = "http://127.0.0.1:8080/"
    
    webbrowser.open(host)
    
    start_server(video_download, port=8080, open_browser=False)  # open_browser=False porque estamos abrindo manualmente
