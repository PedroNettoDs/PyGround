import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from urllib.request import urlopen
from yt_dlp import YoutubeDL
from os import startfile
from PIL import Image, ImageTk
import io

# OBS: Este script requer o FFmpeg instalado no sistema para unir vídeo e áudio.
# Para instalar o FFmpeg via pip, use este comando:
# pip install imageio[ffmpeg]
# Isso instala uma versão funcional do FFmpeg embutida para uso com bibliotecas compatíveis.

# Função para buscar a miniatura (thumbnail) do vídeo a partir da URL
# Utiliza yt_dlp apenas para extrair metadados do vídeo (sem baixá-lo)
def obter_thumbnail(video_url):
    try:
        ydl_opts = {'quiet': True, 'skip_download': True, 'force_generic_extractor': False}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            thumbnail_url = info.get('thumbnail')

        if thumbnail_url:
            response = urlopen(thumbnail_url)  # Abre a URL da miniatura
            raw_data = response.read()  # Lê os dados da imagem
            image = Image.open(io.BytesIO(raw_data))  # Abre a imagem a partir dos bytes
            image = image.resize((320, 180))  # Redimensiona para caber na janela
            return ImageTk.PhotoImage(image)
    except Exception:
        return None

# Abre seletor de pasta usando Tkinter (em modo oculto)
def selecionar_pasta():
    root = tk.Tk()
    root.withdraw()
    pasta = filedialog.askdirectory(title="Escolha a pasta de destino")
    root.destroy()
    return pasta

# Função principal que é executada ao clicar no botão "Baixar"
def iniciar_download():
    url = entrada_url.get().strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        messagebox.showerror("Erro", "URL inválida. Por favor, insira um link válido do YouTube.")
        return

    pasta = selecionar_pasta()
    if not pasta:
        messagebox.showwarning("Atenção", "Nenhuma pasta selecionada.")
        return

    status_label.config(text="Baixando vídeo...", fg="#0052cc")
    janela.update()

    try:
        # Mostra a miniatura do vídeo se for possível carregá-la
        thumb = obter_thumbnail(url)
        if thumb:
            thumbnail_label.config(image=thumb)
            thumbnail_label.image = thumb
        else:
            thumbnail_label.config(image='')

        # Função que exibe progresso em tempo real na interface
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

        # Opções de configuração para yt_dlp
        download_options = {
            'outtmpl': os.path.join(pasta, '%(title)s.%(ext)s'),  # Nome do arquivo de saída
            'format': 'bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/best[ext=mp4][vcodec^=avc1]',  # Melhores streams de vídeo e áudio
            'merge_output_format': 'mp4',  # Formato final de saída
            'progress_hooks': [hook],  # Atualiza a interface com o progresso
            'noplaylist': True,  # Garante que apenas o vídeo individual seja baixado
        }

        with YoutubeDL(download_options) as ydl:
            ydl.download([url])  # Inicia o download

        status_label.config(text="Vídeo baixado com sucesso!", fg="green")

        # Tenta abrir a pasta de destino automaticamente
        try:
            startfile(pasta)
        except Exception:
            pass
    except Exception as e:
        # Mostra qualquer erro ocorrido durante o processo
        status_label.config(text=f"Erro: {e}", fg="red")

# Cria a janela principal da interface gráfica
janela = tk.Tk()
janela.title("YouTube Downloader")
janela.geometry("540x400")  # Tamanho da janela
janela.configure(bg="#f5f5f5")  # Cor de fundo clara

# Define fontes usadas nos widgets
fonte_padrao = ("Segoe UI", 10)
fonte_titulo = ("Segoe UI", 11, "bold")

# Label de instrução para o campo de entrada
label_instrucao = tk.Label(janela, text="Informe o link do vídeo do YouTube:", font=fonte_titulo, bg="#f5f5f5")
label_instrucao.pack(pady=(20, 5))

# Campo onde o usuário digita a URL do vídeo
entrada_url = tk.Entry(janela, width=58, font=fonte_padrao, relief="groove", bd=2)
entrada_url.pack(pady=5)

# Botão que dispara o processo de download (em uma thread separada)
botao_download = tk.Button(
    janela,
    text="Baixar",
    font=fonte_padrao,
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    relief="flat",
    width=20,
    command=lambda: threading.Thread(target=iniciar_download).start()
)
botao_download.pack(pady=10)

# Label que exibe a miniatura do vídeo (caso carregada)
thumbnail_label = tk.Label(janela, bg="#f5f5f5")
thumbnail_label.pack(pady=10)

# Label para mensagens de status (erro, sucesso, progresso)
status_label = tk.Label(janela, text="", font=fonte_padrao, bg="#f5f5f5")
status_label.pack(pady=(10, 5))

# Inicia o loop principal da interface gráfica
janela.mainloop()
