# Atalho para Abrir Pastas com Visual Studio Code via Menu de Contexto (Windows)

Este projeto adiciona uma opção chamada **"Abrir com Visual Studio Code"** ao menu de contexto do Windows, acessível ao clicar com o botão direito no fundo de qualquer pasta. Ele facilita a abertura do VS Code diretamente no diretório desejado.

![Demonstração](docs/menu-contexto-demo.gif)


## 🧩 Funcionalidades

- Adiciona um atalho ao menu de contexto do Explorer.
- Usa o caminho selecionado pelo usuário para `Code.exe` (VS Code).
- Corrige o caminho para o formato adequado (`\`).
- Suporta elevação automática de privilégios (UAC).
- Interface gráfica para seleção do executável.

## ⚙️ Requisitos

- Python 3.x instalado
- Sistema Operacional: **Windows**
- Permissão de Administrador (o script solicita automaticamente se necessário)
- Biblioteca `tkinter` (já vem com Python na maioria das instalações)

## ▶️ Como usar

1. **Execute o script `atalho_vscode.py` como administrador.**
   - Se não for executado como administrador, o próprio script solicitará elevação de privilégios.
2. Uma janela será exibida pedindo para selecionar o arquivo `Code.exe` (executável do VS Code).
   - Caminho padrão no Windows:
     ```
     C:\Users\SEU_USUARIO\AppData\Local\Programs\Microsoft VS Code\Code.exe
     ```
3. Após a seleção, será criado um atalho no menu de contexto de diretórios.

## 📁 Onde o atalho será adicionado?

O atalho aparecerá ao clicar com o botão direito **no fundo de uma pasta**, ou seja, não sobre um arquivo ou a pasta em si. Ele corresponde ao seguinte caminho no Regedit:

```
HKEY_CLASSES_ROOT\Directory\Background\shell\Abrir com Visual Studio Code
```

## 🧹 Como remover o atalho

Para remover, abra o **Editor do Registro (regedit.exe)** e delete a chave:

```
HKEY_CLASSES_ROOT\Directory\Background\shell\Abrir com Visual Studio Code
```

## 📜 Licença

Este projeto é de uso livre e educativo. Modifique à vontade para seu ambiente de trabalho ou produtividade pessoal.
