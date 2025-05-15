# Desativar o Menu de Contexto Moderno do Windows 11

Este script modifica o Registro do Windows para desativar o menu de contexto moderno introduzido no Windows 11 e restaurar diretamente o menu clássico (o mesmo exibido ao clicar em “Mostrar mais opções”).

## 🧩 Funcionalidades

- Desativa o menu moderno do botão direito do mouse no Windows 11.
- Restaura o menu clássico automaticamente.
- Reinicia o Windows Explorer para aplicar as mudanças imediatamente.
- Solicita permissão de administrador automaticamente se necessário.

## ⚙️ Requisitos

- Python 3.x instalado
- Sistema Operacional: **Windows 11**
- Permissão de Administrador

## ▶️ Como usar

1. **Execute o script `desativar_menu_moderno.py` como administrador.**
   - O script solicitará elevação de privilégios se necessário.
2. O script criará a chave necessária no Registro do Windows:
   ```
   HKEY_CURRENT_USER\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32
   ```
   Com valor padrão vazio (`""`).
3. O Windows Explorer será reiniciado automaticamente para aplicar a alteração.

## 🧹 Como restaurar o menu moderno

Para reativar o menu moderno, basta excluir a chave criada. Você pode fazer isso manualmente pelo **Editor de Registro (regedit.exe)** ou criar um script para removê-la:

Caminho da chave a ser removida:
```
HKEY_CURRENT_USER\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}
```

## 📜 Licença

Este projeto é de uso livre e educativo. Sinta-se à vontade para modificá-lo conforme suas necessidades.
