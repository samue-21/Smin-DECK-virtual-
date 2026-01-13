# 📖 Instruções de Instalação - SminDeck + Bot Discord

## Para o Cliente Final

Parabéns! Agora é muito simples instalar e configurar o SminDeck com o Bot Discord.

### Opção 1: Instalação Simples (Sem Bot)

Apenas para usar localmente:

1. Baixe `SminDeck-Setup.exe`
2. Execute o arquivo
3. Na instalação, **desmarque** a opção "Bot Discord (modo remoto)"
4. Clique em instalar
5. Pronto! O SminDeck está instalado

### Opção 2: Instalação com Bot Discord (Recomendado)

Para controlar o SminDeck remotamente via Discord:

1. Baixe `SminDeck-Setup.exe`
2. Execute o arquivo
3. Na instalação, **marque** a opção "Bot Discord (modo remoto)"
4. Siga as instruções de instalação normalmente
5. Quando chegar a parte do Bot Discord:
   - Uma janela vai pedir seu **Token do Discord**
   - Não se preocupe! As instruções vão aparecer na tela

### Como Obter o Token do Discord

Quando a janela de configuração aparecer, ela vai mostrar:

1. Acesse: https://discord.com/developers/applications
2. Clique em "New Application" e crie uma app
3. Vá para a aba "Bot"
4. Copie o token (clique em "Copy")
5. Cole no campo da janela
6. Clique "Confirmar"

### Pronto! 🎉

- O bot será inicializado automaticamente
- Você pode fechar a janela
- O SminDeck vai abrir
- O bot está pronto para receber comandos no Discord

## Primeiro Uso

### Passo 1: Obter a Chave de Conexão

No Discord, no canal do bot, envie:
```
/setup
```

O bot vai responder com uma **chave de conexão**

### Passo 2: Configurar no SminDeck

No SminDeck:
1. Clique em "Configurar Bot Discord" (ou ⚙️)
2. Cole a chave que recebeu do Discord
3. Pronto! Agora pode controlar via Discord

## Dúvidas Frequentes

**P: Onde meu token fica armazenado?**
R: Em `C:\Users\[SeuUsuario]\AppData\Local\SminDeckBot\.env`  
R: Não se preocupe, o arquivo é protegido

**P: Posso desinstalar e reinstalar?**
R: Sim! Se desinstalar, o token é removido. Na próxima instalação você precisa fornecer novamente.

**P: E se esquecer o token?**
R: Sem problema! Vá no Discord Developer Portal e gere um novo.

**P: O bot ficará rodando todo tempo?**
R: Sim, ele roda em background. Você pode fechar as janelas normalmente.

**P: Posso usar em outro PC?**
R: Sim! Instale em quantos computadores quiser.

## Suporte

Se encontrar problemas:

1. Verifique se a chave está correta
2. Verifique se seu Discord bot tem permissões
3. Reinicie o SminDeck
4. Reinstale se necessário

---

**Versão**: 1.2  
**Última atualização**: 2025  
**Suporte**: Contate o desenvolvedor
