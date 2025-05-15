import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from yt_dlp import YoutubeDL
from os import startfile

# OBS: Este script requer o FFmpeg instalado no sistema para unir vídeo e áudio.
# Para instalar o FFmpeg via pip, use este comando:
# pip install imageio[ffmpeg]
# Isso instala uma versão funcional do FFmpeg embutida para uso com bibliotecas compatíveis.

def selecionar_pasta():
    # Abre uma janela oculta do Tkinter apenas para usar o seletor de diretórios
    root = tk.Tk()
    root.withdraw()
    pasta = filedialog.askdirectory(title="Escolha a pasta de destino")  # Mostra o seletor de pastas
    root.destroy()
    return pasta

def iniciar_download():
    # Captura a URL fornecida pelo usuário
    url = entrada_url.get().strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        # Verifica se é uma URL válida
        messagebox.showerror("Erro", "URL inválida. Por favor, insira um link válido do YouTube.")
        return

    # Abre o seletor de pastas para o usuário escolher o local de destino
    pasta = selecionar_pasta()
    if not pasta:
        messagebox.showwarning("Atenção", "Nenhuma pasta selecionada.")
        return

    # Atualiza o status para o usuário saber que o download está em andamento
    status_label.config(text="Baixando vídeo...", fg="#0052cc")
    janela.update()

    try:
        # Hook de progresso que é chamado durante o download
        def hook(d):
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded = d.get('downloaded_bytes', 0)
                if total:
                    percent = int(downloaded / total * 100)  # Calcula porcentagem
                    status_label.config(text=f"Baixando: {percent}%", fg="#0052cc")
                else:
                    status_label.config(text="Baixando...", fg="#0052cc")
                janela.update()

        # Configurações de download para o yt_dlp
        download_options = {
            'outtmpl': os.path.join(pasta, '%(title)s.%(ext)s'),  # Define o nome do arquivo de saída
            'format': 'bestvideo+bestaudio/best',  # Baixa a melhor qualidade de vídeo e áudio
            'merge_output_format': 'mp4',  # Une os arquivos baixados em .mp4
            'progress_hooks': [hook],  # Função para acompanhar o progresso
            'noplaylist': True,  # Evita baixar playlists inteiras
        }

        # Executa o download com as opções fornecidas
        with YoutubeDL(download_options) as ydl:
            ydl.download([url])

        # Atualiza o status ao finalizar o download
        status_label.config(text="Vídeo baixado com sucesso!", fg="green")

        # Tenta abrir a pasta automaticamente após o download
        try:
            startfile(pasta)
        except Exception:
            pass
    except Exception as e:
        # Mostra mensagem de erro caso algo falhe
        status_label.config(text=f"Erro: {e}", fg="red")

# Cria a janela principal da aplicação
janela = tk.Tk()
janela.title("YouTube Downloader")
janela.geometry("520x240")  # Define tamanho da janela
janela.configure(bg="#f5f5f5")  # Define cor de fundo

# Define estilos de fonte para elementos
fonte_padrao = ("Segoe UI", 10)
fonte_titulo = ("Segoe UI", 11, "bold")

# Label de instrução
label_instrucao = tk.Label(janela, text="Informe o link do vídeo do YouTube:", font=fonte_titulo, bg="#f5f5f5")
label_instrucao.pack(pady=(20, 5))

# Campo de entrada de texto para a URL
entrada_url = tk.Entry(janela, width=58, font=fonte_padrao, relief="groove", bd=2)
entrada_url.pack(pady=5)

# Botão que inicia o download em uma thread separada
botao_download = tk.Button(
    janela,
    text="Baixar",
    font=fonte_padrao,
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    relief="flat",
    width=20,
    command=lambda: threading.Thread(target=iniciar_download).start()  # Roda o download em thread para não travar a interface
)
botao_download.pack(pady=10)

# Label para mostrar mensagens de status (ex: progresso ou erros)
status_label = tk.Label(janela, text="", font=fonte_padrao, bg="#f5f5f5")
status_label.pack(pady=(10, 5))

# Inicia o loop principal da interface
janela.mainloop()
