import os
import sys
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox
import winreg as reg

# Verifica se o script está sendo executado com privilégios de administrador
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Abre um seletor de arquivo para o usuário escolher o executável do VS Code
def solicitar_code_exe():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter
    caminho = filedialog.askopenfilename(
        title="Selecione o executável Code.exe",
        filetypes=[("Executável", "*.exe")],
    )
    return caminho

# Cria a entrada no Registro do Windows para adicionar o atalho no menu de contexto
def criar_entrada_registro(code_path):
    nome_atalho = "Abrir com Visual Studio Code"  # Nome que aparecerá no menu
    icone = code_path  # O próprio executável será usado como ícone
    chave_pai = r"Directory\Background\shell"  # Caminho da chave onde o atalho será criado
    caminho_completo = chave_pai + "\\" + nome_atalho

    try:
        # Cria a chave principal do atalho
        chave_atalho = reg.CreateKey(reg.HKEY_CLASSES_ROOT, caminho_completo)
        reg.SetValueEx(chave_atalho, "", 0, reg.REG_SZ, nome_atalho)  # Define o nome exibido
        reg.SetValueEx(chave_atalho, "Icon", 0, reg.REG_SZ, icone)  # Define o ícone

        # Cria a subchave 'command' e define o comando a ser executado
        chave_command = reg.CreateKey(chave_atalho, "command")
        comando = f'"{code_path}" "%V"'  # "%V" representa o diretório atual clicado
        reg.SetValueEx(chave_command, "", 0, reg.REG_SZ, comando)

        # Exibe mensagem de sucesso
        messagebox.showinfo("Sucesso", f"O atalho '{nome_atalho}' foi criado com sucesso!")
    except Exception as e:
        # Em caso de erro, exibe uma mensagem informando o problema
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    # Se o script não estiver sendo executado como admin, reinicia com elevação
    if not is_admin():
        script = os.path.abspath(sys.argv[0])  # Caminho completo do script atual
        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
        sys.exit()

    # Solicita que o usuário selecione o executável do VS Code
    caminho = solicitar_code_exe()
    if caminho:
        caminho = caminho.replace('/', '\\')  # Corrige barras para formato Windows
        criar_entrada_registro(caminho)  # Cria o atalho no registro
    else:
        print("Nenhum arquivo selecionado.")
