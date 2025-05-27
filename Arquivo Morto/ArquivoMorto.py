import getpass
import subprocess
import datetime
import os
import tkinter as tk
from tkinter import messagebox

DOMINIO = "dominio.com"  # Substitua pelo domínio correto

def mostrar_popup_aviso(msg, titulo="Atenção"):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(titulo, msg)
    root.destroy()

def mostrar_popup_erro(msg, titulo="Erro"):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(titulo, msg)
    root.destroy()

def mostrar_popup_sucesso(msg, titulo="Sucesso"):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(titulo, msg)
    root.destroy()

# 1. Descobre o usuário local do Windows
usuario_local = getpass.getuser()
print(f"Usuário local detectado: {usuario_local}")

# 2. Monta o e-mail para conexão (C.I.)
email_conexao = f"{usuario_local}@{DOMINIO}"
print(f"E-mail de conexão a ser utilizado: {email_conexao}")

# 3. Pergunta apenas o login da caixa (sem o domínio)
login_caixa = input("Digite o login da caixa que será startada (apenas o usuário, sem @domínio): ")
email_caixa = f"{login_caixa}@{DOMINIO}"
print(f"E-mail da caixa: {email_caixa}")

# 4. Mostra popup destacado antes da autenticação
mostrar_popup_aviso(
    "\nA tela de autenticação da Microsoft será exibida agora!\n\n"
    "Por favor, realize o login normalmente para continuar.",
    titulo="Autenticação Microsoft"
)

# 5. Monta comandos PowerShell, testando se o módulo já está instalado
comandos = f"""
if (-not (Get-Module -ListAvailable -Name ExchangeOnlineManagement)) {{
    Install-Module ExchangeOnlineManagement
}}
Import-Module ExchangeOnlineManagement
Connect-ExchangeOnline -UserPrincipalName {email_conexao}
Get-Mailbox {email_caixa} | FL RetentionPolicy
Start-ManagedFolderAssistant {email_caixa}
"""

# 6. Salva comandos em arquivo .ps1
ps1_file = "comando_exchange.ps1"
with open(ps1_file, 'w', encoding='utf-8') as f:
    f.write(comandos)

# Função para registrar log
def registrar_log(email_conexao, email_caixa, status):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('registro_comandos.log', 'a', encoding='utf-8') as f:
        f.write(f"[{now}] Conexão: {email_conexao} | Caixa: {email_caixa} | Status: {status}\n")

# 7. Executa o script PowerShell
try:
    print("Executando comandos no PowerShell...")
    resultado = subprocess.run(
        ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", ps1_file],
        capture_output=True,
        text=True
    )
    print("Saída do PowerShell:\n", resultado.stdout)
    if resultado.stderr:
        print("Erros:\n", resultado.stderr)
        mostrar_popup_erro(
            f"Ocorreu um erro na execução:\n\n{resultado.stderr.strip()}",
            titulo="Erro no Processo"
        )
        registrar_log(email_conexao, email_caixa, f"ERRO: {resultado.stderr.strip()}")
    else:
        mostrar_popup_sucesso(
            "Processo executado com sucesso!\nA política de retenção foi processada.",
            titulo="Sucesso"
        )
        registrar_log(email_conexao, email_caixa, "Executado com sucesso")
except Exception as e:
    print("Erro ao executar o PowerShell:", e)
    mostrar_popup_erro(
        f"Exceção ao executar o PowerShell:\n\n{str(e)}",
        titulo="Erro Crítico"
    )
    registrar_log(email_conexao, email_caixa, f"EXCEPTION: {str(e)}")

# 8. Aguarda o usuário antes de fechar o terminal
input("\nPressione ENTER para sair...")
