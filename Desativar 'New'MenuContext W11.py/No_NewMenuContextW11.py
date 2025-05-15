import os
import sys
import ctypes
import winreg as reg
from tkinter import messagebox

# Verifica se o script está sendo executado com privilégios de administrador
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Cria a chave do Registro para desativar o menu moderno do Windows 11
def desativar_menu_moderno():
    try:
        # Caminho da chave do CLSID que controla o menu moderno
        chave_base = r"Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32"

        # Cria a chave
        chave = reg.CreateKey(reg.HKEY_CURRENT_USER, chave_base)
        reg.SetValueEx(chave, "", 0, reg.REG_SZ, "")  # Define valor padrão vazio

        messagebox.showinfo("Sucesso", "Menu moderno do Windows 11 desativado com sucesso. Reinicie o Explorer para aplicar.")
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível alterar o registro: {e}")

# Reinicia o processo do Windows Explorer para aplicar a mudança
def reiniciar_explorer():
    os.system("taskkill /f /im explorer.exe")
    os.system("start explorer.exe")

if __name__ == "__main__":
    if not is_admin():
        # Reexecuta o script com permissão de administrador
        script = os.path.abspath(sys.argv[0])
        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
        sys.exit()

    desativar_menu_moderno()
    reiniciar_explorer()
