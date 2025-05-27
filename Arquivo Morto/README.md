# Ferramenta para Execução de Política de Retenção Exchange Online

1. **Edite a variavel** `DOMINIO`
2. **Compile o programa**: 
pip install pyinstaller
pyinstaller --onefile ArquivoMorto.py
2. **Dê um duplo clique** sobre o arquivo para executar.

![Demonstração](menu-contexto-demo.gif)

**Importante:**  
- O executável pode demorar alguns segundos para abrir na primeira vez.
- Certifique-se de estar conectado ao domínio.

## O que a ferramenta faz?
- Solicita apenas o login da caixa desejada (sem precisar digitar o domínio).
- Exibe avisos em popup sobre a autenticação Microsoft.
- Executa os comandos necessários automaticamente.
- Mostra um popup informando o sucesso ou erro do processo.
- Registra um log das execuções para conferência posterior.

## Requisitos

- Permissão para executar scripts PowerShell e logar no Exchange Online

## Suporte

Em caso de dúvidas ou problemas, entre em contato com o **Pedro H. Netto**.

---
