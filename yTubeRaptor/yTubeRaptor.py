import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from urllib.request import urlopen
from yt_dlp import YoutubeDL
from os import startfile
from PIL import Image, ImageTk
import io

# OBS: Este script requer o FFmpeg instalado no sistema para unir vídeo e áudio.
# Para instalar o FFmpeg via pip, use este comando:
# pip install imageio[ffmpeg]

# Função que extrai a miniatura do vídeo a partir do link do YouTube
# Utiliza yt_dlp para pegar apenas os metadados do vídeo (sem baixar)
def obter_thumbnail(video_url):
    try:
        ydl_opts = {'quiet': True, 'skip_download': True, 'force_generic_extractor': False}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            thumbnail_url = info.get('thumbnail')

        if thumbnail_url:
            response = urlopen(thumbnail_url)  # Requisição da imagem pela URL
            raw_data = response.read()  # Lê os bytes da imagem
            image = Image.open(io.BytesIO(raw_data))  # Abre a imagem a partir dos bytes
            image = image.resize((320, 180))  # Redimensiona para se encaixar na janela
            return ImageTk.PhotoImage(image)
    except Exception:
        return None

# Função que abre uma janela para o usuário escolher a pasta de destino
def selecionar_pasta():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal
    pasta = filedialog.askdirectory(title="Escolha a pasta de destino")
    root.destroy()
    return pasta

# Função principal que lida com o processo de download
def iniciar_download():
    url = entrada_url.get().strip()  # Obtém o link digitado pelo usuário
    tipo = formato_var.get()  # Verifica se usuário escolheu MP4 ou MP3

    # Valida a URL
    if not url.startswith("http://") and not url.startswith("https://"):
        messagebox.showerror("Erro", "URL inválida. Por favor, insira um link válido do YouTube.")
        return

    # Abre seletor de pasta
    pasta = selecionar_pasta()
    if not pasta:
        messagebox.showwarning("Atenção", "Nenhuma pasta selecionada.")
        return

    # Atualiza status
    status_label.config(text="Iniciando download...", fg="#0052cc")
    janela.update()

    try:
        # Obtém e exibe a miniatura do vídeo
        thumb = obter_thumbnail(url)
        if thumb:
            thumbnail_label.config(image=thumb)
            thumbnail_label.image = thumb
        else:
            thumbnail_label.config(image='')

        # Função hook usada para atualizar o progresso de download
        def hook(d):
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded = d.get('downloaded_bytes', 0)
                if total:
                    percent = int(downloaded / total * 100)
                    status_label.config(text=f"Baixando: {percent}%", fg="#0052cc")
                else:
                    status_label.config(text="Baixando...", fg="#0052cc")
                janela.update()

        # Define as opções do yt_dlp com base no formato escolhido
        if tipo == "MP3":
            download_options = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(pasta, '%(title)s.%(ext)s'),
                'progress_hooks': [hook],
                'noplaylist': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            }
        else:  # Se for MP4
            download_options = {
                'outtmpl': os.path.join(pasta, '%(title)s.%(ext)s'),
                'format': 'bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/best[ext=mp4][vcodec^=avc1]',
                'merge_output_format': 'mp4',
                'progress_hooks': [hook],
                'noplaylist': True,
            }

        # Executa o download com as opções definidas
        with YoutubeDL(download_options) as ydl:
            ydl.download([url])

        # Atualiza status ao finalizar
        status_label.config(text="Download concluído com sucesso!", fg="green")

        # Tenta abrir a pasta automaticamente
        try:
            startfile(pasta)
        except Exception:
            pass
    except Exception as e:
        # Mostra o erro na interface
        status_label.config(text=f"Erro: {e}", fg="red")

# Configuração da janela principal
janela = tk.Tk()
janela.title("YouTube Downloader")
janela.geometry("540x460")
janela.configure(bg="#f5f5f5")

# Definição de fontes usadas nos widgets
fonte_padrao = ("Segoe UI", 10)
fonte_titulo = ("Segoe UI", 11, "bold")

# Campo de instrução
label_instrucao = tk.Label(janela, text="Informe o link do vídeo do YouTube:", font=fonte_titulo, bg="#f5f5f5")
label_instrucao.pack(pady=(20, 5))

# Campo de entrada de URL
entrada_url = tk.Entry(janela, width=58, font=fonte_padrao, relief="groove", bd=2)
entrada_url.pack(pady=5)

# Campo de seleção do formato (MP3 ou MP4)
formato_var = tk.StringVar(value="MP4")
formato_label = tk.Label(janela, text="Formato desejado:", font=fonte_padrao, bg="#f5f5f5")
formato_label.pack(pady=(10, 0))
formato_menu = ttk.Combobox(janela, textvariable=formato_var, values=["MP4", "MP3"], state="readonly", width=10)
formato_menu.pack(pady=5)

# Botão para iniciar o download
botao_download = tk.Button(
    janela,
    text="Baixar",
    font=fonte_padrao,
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    relief="flat",
    width=20,
    command=lambda: threading.Thread(target=iniciar_download).start()  # Usa thread para não travar a UI
)
botao_download.pack(pady=10)

# Espaço para mostrar miniatura do vídeo
thumbnail_label = tk.Label(janela, bg="#f5f5f5")
thumbnail_label.pack(pady=10)

# Label de status (progresso ou erro)
status_label = tk.Label(janela, text="", font=fonte_padrao, bg="#f5f5f5")
status_label.pack(pady=(10, 5))

# Inicia o loop principal da interface
janela.mainloop()
