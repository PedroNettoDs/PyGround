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
        # Solicitar o link do vídeo ao usuário
        video_link = input("Informe o Link do vídeo:").strip()
        
        # Validar o link (precisa começar com http ou https)
        if video_link.startswith("http://") or video_link.startswith("https://"):
            # Abrir o explorador de arquivos para escolher o diretório
            root = tk.Tk()
            root.withdraw()  # Ocultar a janela principal do Tkinter
            download_path = filedialog.askdirectory(title="Escolha a pasta de destino")  # Abrir o explorador de arquivos
            
            # Validar se o usuário escolheu um diretório
            if not download_path:
                put_text("Nenhum diretório foi selecionado. Tente novamente.").style('color: red; font-size: 20px')
                continue  # Se nenhum diretório for selecionado, solicita novamente

            try:
                put_text("Fazendo Download do vídeo...").style('color: red; font-size: 20px')
                
                # Configurar opções para o yt-dlp
                download_options = {
                    'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),  # Usar o diretório escolhido
                    'format': 'bestvideo+bestaudio/best',  # Melhor qualidade de vídeo e áudio
                    'merge_output_format': 'mp4',  # Formato final do arquivo
                    'ffmpeg_location': r'C:\Users\mrped\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1-full_build\bin',  # Caminho global do FFmpeg
                }
                
                # Tentar baixar o vídeo
                with YoutubeDL(download_options) as ydl:
                    ydl.download([video_link])
                
                # Mensagem de sucesso
                put_text("Vídeo baixado com sucesso!").style('color: green; font-size: 20px')
                
                # Abrir a pasta de downloads
                startfile(download_path)  # Abre o local escolhido
                break  # Sair do loop após o download bem-sucedido

            except Exception as e:
                put_text(f"Erro: {e}").style('color: red; font-size: 20px')
        else:
            put_text("URL inválida. Por favor, insira um link válido do YouTube.").style('color: orange; font-size: 20px')

if __name__ == "__main__":
    # Configurar o endereço do servidor
    host = "http://127.0.0.1:8080/"  # Localhost com a porta 8080
    
    # Abrir o navegador automaticamente
    webbrowser.open(host)
    
    # Inicia o servidor PyWebIO
    start_server(video_download, port=8080, open_browser=False)  # open_browser=False porque estamos abrindo manualmente
