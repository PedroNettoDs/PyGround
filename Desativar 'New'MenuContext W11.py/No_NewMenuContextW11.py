import os
import sys
import ctypes
import winreg as reg
import tkinter as tk
from tkinter import messagebox, simpledialog

# Verifica se o script está sendo executado com privilégios de administrador
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Cria a chave do Registro para desativar o menu moderno do Windows 11
def desativar_menu_moderno():
    try:
        chave_base = r"Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32"
        chave = reg.CreateKey(reg.HKEY_CURRENT_USER, chave_base)
        reg.SetValueEx(chave, "", 0, reg.REG_SZ, "")
        messagebox.showinfo("Sucesso", "Menu moderno do Windows 11 desativado com sucesso. Reinicie o Explorer para aplicar.")
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível alterar o registro: {e}")

# Remove a chave para restaurar o menu moderno do Windows 11
def restaurar_menu_moderno():
    try:
        chave_pai = r"Software\Classes\CLSID"
        reg.DeleteKey(reg.HKEY_CURRENT_USER, chave_pai + r"\\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\\InprocServer32")
        reg.DeleteKey(reg.HKEY_CURRENT_USER, chave_pai + r"\\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}")
        messagebox.showinfo("Sucesso", "Menu moderno do Windows 11 restaurado com sucesso. Reinicie o Explorer para aplicar.")
    except FileNotFoundError:
        messagebox.showinfo("Aviso", "A chave do menu moderno já está ausente.")
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível restaurar o menu moderno: {e}")

# Reinicia o processo do Windows Explorer para aplicar a mudança
def reiniciar_explorer():
    os.system("taskkill /f /im explorer.exe")
    os.system("start explorer.exe")

if __name__ == "__main__":
    if not is_admin():
        script = os.path.abspath(sys.argv[0])
        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
        sys.exit()

    root = tk.Tk()
    root.withdraw()

    escolha = messagebox.askquestion("Menu do Windows 11", "Deseja desativar o menu moderno do Windows 11?\nClique em 'Não' para restaurar o menu moderno.")

    if escolha == 'yes':
        desativar_menu_moderno()
    else:
        restaurar_menu_moderno()

    reiniciar_explorer()
