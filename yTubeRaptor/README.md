# YouTube Downloader com Interface Gráfica (Tkinter)

Este projeto é uma aplicação de desktop simples e moderna que permite ao usuário baixar vídeos do YouTube com as seguintes funcionalidades integradas:

## 🚀 Funcionalidades

- ✅ Interface gráfica moderna com Tkinter
- 🎞️ Visualização automática da miniatura (thumbnail) do vídeo
- 🔁 Download apenas do vídeo (evita playlists inteiras)
- 📂 Escolha do diretório de destino via seletor de pastas
- 🎚️ Exibição em tempo real do progresso do download
- 🔄 Mesclagem automática de vídeo + áudio em um único arquivo `.mp4`
- 📼 Compatibilidade com editores como Adobe Premiere (evita o codec VP9)
- 📁 Abertura automática da pasta após o download

---

## 🛠️ Requisitos

- Python 3.7+
- `yt-dlp` para download dos vídeos
- `Pillow` para exibir imagens
- `imageio[ffmpeg]` para garantir fusão de streams
- Internet ativa (obviamente)

Instale com:

```bash
pip install yt-dlp Pillow imageio[ffmpeg]
```

---

## 💻 Como usar

1. Execute o script `youtube_downloader.py`.
2. Insira a URL do vídeo do YouTube.
3. Uma miniatura será exibida automaticamente.
4. Escolha a pasta onde deseja salvar o vídeo.
5. O progresso será mostrado e a pasta será aberta ao final.

---

## 🧩 Compatibilidade com o Adobe Premiere

O script está configurado para evitar o uso do codec `vp09` (VP9), que não é suportado por padrão pelo Premiere. Ele força o uso do codec `avc1` (H.264), amplamente compatível com softwares de edição de vídeo.

---

## ✨ Screenshot

(Opcional: adicionar uma captura de tela aqui mostrando a interface)

---

## 📜 Licença

Este projeto é livre para uso pessoal, estudo e modificação.

