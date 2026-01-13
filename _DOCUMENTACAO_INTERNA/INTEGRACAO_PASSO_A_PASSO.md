# 🎯 INTEGRAÇÃO PASSO-A-PASSO - NOVO SERVIDOR DISCORD

**Objetivo Final**: Ter o bot funcionando no seu novo servidor Discord  
**Tempo Estimado**: 15-20 minutos  
**Dificuldade**: ⭐ Fácil

---

## ✨ RESULTADO ESPERADO

Quando terminar, você terá:
- ✅ Um novo servidor Discord (privado ou público)
- ✅ Um bot Discord funcionando nele
- ✅ SminDeck instalado no Windows
- ✅ Tudo integrado e comunicando

---

## 🔴 PASSO 1: CRIAR NOVO SERVIDOR DISCORD (3 min)

### 1.1 - Abra Discord
```
1. Abra Discord (desktop ou web: discord.com)
2. Você deve estar logado
```

### 1.2 - Clique no "+"
```
1. No lado esquerdo, veja a lista de servidores
2. No final, tem um ícone "+" 
3. Clique nele
```

### 1.3 - Crie um Servidor
```
1. Clique em "Criar um servidor"
2. Escolha um template (pode deixar padrão)
3. Nomeie seu servidor:
   Exemplo: "SminDeck Test"
4. Clique em "Criar"
```

### 1.4 - Você Está no Novo Servidor!
```
✅ Pronto! Seu novo servidor foi criado
✅ Você é o proprietário automaticamente
```

---

## 🔵 PASSO 2: REGISTRAR BOT NO DISCORD DEVELOPER (5 min)

### 2.1 - Vá ao Discord Developer Portal
```
Abra em navegador:
https://discord.com/developers/applications
```

### 2.2 - Crie Nova Aplicação
```
1. Clique no botão "New Application"
2. Nomeie: "SminDeck Bot"
3. Leia os termos (opcional)
4. Clique em "Create"
```

### 2.3 - Abra a Aba "Bot"
```
1. No menu esquerdo, veja "Bot"
2. Clique em "Add Bot"
3. Uma nova página carregar
```

### 2.4 - COPIE O TOKEN (⚠️ IMPORTANTE!)
```
Você vê um campo com "TOKEN" com um botão "Copy"

1. Clique em "Copy" para copiar o token
2. GUARDE SEGURO em um lugar:
   - Bloco de notas
   - Password manager
   - Arquivo de texto

⚠️ NÃO COMPARTILHE COM NINGUÉM!
```

---

## 🟣 PASSO 3: ATIVAR INTENTS (2 min)

### 3.1 - Ainda na Aba "Bot"
```
Scroll down até ver "INTENTS"
```

### 3.2 - Ative Estes Intents
```
☑ Presence Intent
☑ Server Members Intent
☑ Message Content Intent

(Os outros podem ficar desativados)
```

### 3.3 - Clique em "Save Changes"
```
Um botão verde deve aparecer
```

---

## 🟢 PASSO 4: GERAR LINK DE CONVITE (3 min)

### 4.1 - Vá para "OAuth2" → "URL Generator"
```
1. Menu esquerdo → "OAuth2"
2. Vá para "URL Generator"
```

### 4.2 - Selecione Escopos
```
Em "SCOPES", selecione:
☑ bot
```

### 4.3 - Selecione Permissões
```
Em "PERMISSIONS", selecione:
☑ Send Messages
☑ Embed Links
☑ Read Messages/View Channels
☑ Read Message History

(Você pode selecionar mais se quiser)
```

### 4.4 - Copie a URL
```
No final da página, vê a URL gerada
Clique em "Copy" para copiar
```

---

## 🟡 PASSO 5: ADICIONAR BOT AO SERVIDOR (2 min)

### 5.1 - Cole a URL em Novo Navegador
```
1. Abra uma nova aba
2. Cole a URL que copiou
3. Enter
```

### 5.2 - Selecione o Servidor
```
1. Você vê um dropdown "Select a server"
2. Clique nele
3. Selecione seu novo servidor
4. "SminDeck Test" (ou seu nome)
```

### 5.3 - Autorize o Bot
```
1. Clique em "Autorizar"
2. Se pedir CAPTCHA, complete
3. Pronto! Bot foi adicionado
```

### 5.4 - Verifique no Discord
```
1. Volte ao Discord
2. Vá para seu novo servidor
3. Vá para "Membros" (ícone de pessoas)
4. Deve ver "SminDeck Bot" na lista
5. Status deve ser ONLINE ✅
```

---

## 🟠 PASSO 6: ATUALIZAR BOT NO VPS (OPCIONAL - se novo token)

### 6.1 - Se Você Está Usando Novo Token
```
Você precisa atualizar no VPS
Se estiver usando o mesmo token, PULE esta parte
```

### 6.2 - Conecte via SSH
```powershell
# No PowerShell
ssh root@72.60.244.240
# Digite sua senha
```

### 6.3 - Edite o Arquivo do Bot
```bash
nano /opt/smin-bot/bot_humanizado_interativo.py
```

### 6.4 - Procure por TOKEN
```
Ctrl+W e procure por: TOKEN = "
Você verá algo como: TOKEN = "seu_token_antigo"
```

### 6.5 - Substitua o Token
```
1. Delete o token antigo
2. Digite seu novo token
3. Ctrl+O e Enter para salvar
4. Ctrl+X para sair
```

### 6.6 - Reinicie o Bot
```bash
systemctl restart smin-bot
systemctl status smin-bot
# Deve mostrar: active (running) ✅
```

---

## ⚪ PASSO 7: TESTAR BOT NO DISCORD (2 min)

### 7.1 - Vá para Seu Servidor
```
Discord → Seu novo servidor
```

### 7.2 - Vá para Um Canal (ex: #general)
```
1. Clique em #general (ou outro canal)
2. Na caixa de mensagem, escreva: oi
```

### 7.3 - Envie a Mensagem
```
Pressione Enter
```

### 7.4 - Bot Deve Responder!
```
Você verá algo como:
"Opa! 👋 Como você está? Qual é a parada?"

Com 4 botões abaixo:
- Botão 1
- Botão 2
- Botão 3
- Botão 4
```

### 7.5 - Teste um Modal
```
1. Clique em "Botão 1"
2. Um popup (modal) deve aparecer
3. Pergunta: "Qual botão deseja?"
4. Selecione um número (1-12)
5. Clique "Submit"
6. Bot deve confirmar
```

---

## 🔘 PASSO 8: INSTALAR E RODAR SMINDECK (3 min)

### 8.1 - Abra PowerShell
```
Pressione: Win + X
Selecione: "PowerShell"
```

### 8.2 - Rode SminDeck
```powershell
C:\Users\SAMUEL\SminDeck_v1.2\SminDeck.exe
```

### 8.3 - Janela Deve Abrir
```
✅ SminDeck interface aparece
✅ Logo visível
✅ Sem erros
```

---

## 🎉 PRONTO!

**Você completou a integração!**

```
✅ Novo servidor Discord criado
✅ Bot Discord configurado
✅ Bot online e respondendo
✅ SminDeck instalado
✅ Tudo funcionando integrado
```

---

## 🆘 PROBLEMAS?

### Bot não aparece online
```
1. Verifique token está correto no VPS
2. Verifique intents no Discord portal
3. Reinicie: systemctl restart smin-bot
4. Aguarde 30 segundos
5. Refreshe Discord (F5)
```

### Bot não responde a mensagens
```
1. Verifique se tem permissão no canal
2. Verifique MESSAGE CONTENT INTENT está ativo
3. Reinicie bot no VPS
4. Teste novamente
```

### SminDeck não abre
```
1. Tente rodar como Admin
2. Tente duplo clique em SminDeck.exe
3. Desative antivírus temporariamente
4. Verifique espaço em disco
```

---

## 📝 CHECKLIST

- [ ] Servidor Discord criado
- [ ] Bot registrado no portal
- [ ] Token copiado e guardado
- [ ] Intents ativados
- [ ] URL de convite gerada
- [ ] Bot adicionado ao servidor
- [ ] Bot online no Discord
- [ ] Token atualizado em VPS (se novo)
- [ ] Bot testado com "oi"
- [ ] Modal testado
- [ ] SminDeck instalado
- [ ] Tudo funcionando! 🎉

---

**Tempo Total**: ~15-20 minutos  
**Resultado**: Sistema completo integrado e funcional  
**Próximo Passo**: Aproveite! 🚀

Gerado: 06/01/2026
