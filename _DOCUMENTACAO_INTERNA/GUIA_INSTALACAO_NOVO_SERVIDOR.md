# 🚀 GUIA DE INSTALAÇÃO E INTEGRAÇÃO - NOVO SERVIDOR DISCORD

**Data**: 06/01/2026  
**Objetivo**: Instalar SminDeck e integrar bot em novo servidor Discord  

---

## 📋 PRÉ-REQUISITOS

- [x] SminDeck.exe compilado (46.6 MB)
- [x] Bot Discord em VPS (72.60.244.240) ativo
- [ ] Novo servidor Discord criado
- [ ] Token Discord Bot obtido
- [ ] Permissões configuradas

---

## FASE 1: PREPARAR NOVO SERVIDOR DISCORD

### Passo 1.1: Criar Novo Servidor (se não tiver)
```
1. Abra Discord
2. Clique em "+" → "Criar um servidor"
3. Nomeie como: "SminDeck Test" (ou seu nome)
4. Selecione "Para um clube ou comunidade pequena"
5. Crie o servidor
```

### Passo 1.2: Obter Permissões de Admin
```
1. Vá para Configurações do Servidor
2. Abra "Membros"
3. Encontre seu nome e confirme que é "Proprietário"
```

---

## FASE 2: REGISTRAR BOT DISCORD

### Passo 2.1: Ir ao Discord Developer Portal
```
https://discord.com/developers/applications
```

### Passo 2.2: Criar Nova Aplicação
```
1. Clique em "New Application"
2. Nomeie: "SminDeck Bot"
3. Clique em "Create"
```

### Passo 2.3: Criar Bot User
```
1. Vá para "Bot" no menu esquerdo
2. Clique em "Add Bot"
3. Você verá um token → COPIE E GUARDE SEGURO
```

### Passo 2.4: Configurar Intents (IMPORTANTE!)
```
Em "Bot" → "Intents", ative:
[x] PRESENCE INTENT
[x] SERVER MEMBERS INTENT
[x] MESSAGE CONTENT INTENT
```

### Passo 2.5: Gerar URL de Convite
```
1. Vá para "OAuth2" → "URL Generator"
2. Selecione scopes: "bot"
3. Selecione permissões:
   [x] Send Messages
   [x] Embed Links
   [x] Read Messages/View Channels
   [x] Read Message History
4. Copie a URL gerada
```

---

## FASE 3: ADICIONAR BOT AO SERVIDOR

### Passo 3.1: Convite do Bot
```
1. Cole a URL do passo anterior em nova aba
2. Selecione seu novo servidor
3. Clique em "Autorizar"
4. Complete o CAPTCHA
```

### Passo 3.2: Verificar Bot no Servidor
```
1. Volte ao Discord
2. Vá para seu novo servidor
3. Você deve ver "SminDeck Bot" na lista de membros
4. Status deve ser ONLINE ✅
```

---

## FASE 4: INSTALAR SMINDECK NO WINDOWS

### Passo 4.1: Escolher Local de Instalação
```
Opção A: Pasta simples
C:\Users\SEU_USUARIO\SminDeck\

Opção B: Program Files
C:\Program Files\SminDeck\

Opção C: Área de Trabalho
C:\Users\SEU_USUARIO\Desktop\SminDeck\
```

### Passo 4.2: Copiar Executável
```powershell
# Abra PowerShell como Admin

# Opção A - Pasta simples:
New-Item -ItemType Directory "C:\Users\SAMUEL\SminDeck" -Force
Copy-Item "C:\Users\SAMUEL\Desktop\Smin-DECK virtual\dist\SminDeck.exe" "C:\Users\SAMUEL\SminDeck\"
Copy-Item "C:\Users\SAMUEL\Desktop\Smin-DECK virtual\assets" "C:\Users\SAMUEL\SminDeck\" -Recurse -Force

# Verificar
Get-Item "C:\Users\SAMUEL\SminDeck\SminDeck.exe"
```

### Passo 4.3: Criar Atalho (Opcional)
```powershell
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut("C:\Users\SAMUEL\Desktop\SminDeck.lnk")
$shortcut.TargetPath = "C:\Users\SAMUEL\SminDeck\SminDeck.exe"
$shortcut.WorkingDirectory = "C:\Users\SAMUEL\SminDeck"
$shortcut.Save()
```

---

## FASE 5: CONFIGURAR BOT NO VPS

### Passo 5.1: Conectar ao VPS via SSH
```bash
# No PowerShell ou Terminal
ssh root@72.60.244.240
# Senha: [sua senha]
```

### Passo 5.2: Localizar Bot
```bash
cd /opt/smin-bot/
ls -la
# Deve mostrar: bot_humanizado_interativo.py
```

### Passo 5.3: Atualizar Token (SE NECESSÁRIO)
```bash
# Editar arquivo do bot
nano bot_humanizado_interativo.py

# Procure por: TOKEN = "seu_token_aqui"
# Substitua pelo novo token do Discord
# Ctrl+O → Enter (salvar)
# Ctrl+X (sair)
```

### Passo 5.4: Reiniciar Bot
```bash
# Parar bot atual
systemctl stop smin-bot

# Verificar parada
systemctl status smin-bot

# Iniciar novamente
systemctl start smin-bot

# Verificar se está rodando
systemctl status smin-bot
# Deve mostrar: active (running) ✅
```

---

## FASE 6: TESTAR INTEGRAÇÃO

### Teste 6.1: Bot Respondendo
```
1. Vá para seu servidor Discord
2. No canal #general ou qualquer canal
3. Digite: "oi" ou "olá"
4. Bot deve responder com:
   "Opa! 👋 Como você está? Qual é a parada?"
5. Deve mostrar menu com 4 botões
```

### Teste 6.2: Teste de Modal
```
1. Clique em um dos botões (ex: "Botão 1")
2. Deve aparecer modal: "Qual botão deseja?"
3. Selecione uma opção (1-12)
4. Bot deve confirmar: "OK! Configurado para o Botão X"
```

### Teste 6.3: Verificar Logs VPS
```bash
# Conectar via SSH
ssh root@72.60.244.240

# Ver logs do bot
journalctl -u smin-bot -f
# (Ctrl+C para sair)

# Ou verificar se processo está rodando
ps aux | grep bot_humanizado
```

---

## FASE 7: INICIAR SMINDECK

### Passo 7.1: Executar Aplicação
```powershell
# Opção 1: Clique no atalho na desktop
# Opção 2: Via PowerShell
C:\Users\SAMUEL\SminDeck\SminDeck.exe

# Opção 3: Via botão iniciar
# Procure por "SminDeck"
```

### Passo 7.2: Verificar Interface
```
1. Janela SminDeck deve abrir
2. Deve mostrar interface PyQt6
3. Verifique logo no título e taskbar
4. Sem erros ou crashes
```

### Passo 7.3: Conectar ao Bot (Se Necessário)
```
Se a interface tiver campo para URL/Token:
1. Insira: 72.60.244.240
2. Insira seu novo token (se solicitado)
3. Clique em "Conectar"
4. Aguarde confirmação
```

---

## ⚠️ TROUBLESHOOTING

### Problema: Bot não aparece online
```
Solução:
1. Verifique token no VPS está correto
2. Verifique intents no Discord Developer Portal
3. Reinicie o bot: systemctl restart smin-bot
4. Aguarde 30 segundos
```

### Problema: Bot não responde a mensagens
```
Solução:
1. Verifique MESSAGE CONTENT INTENT está ativo
2. Verifique permissões do bot no servidor
3. Verifique se bot tem acesso ao canal
4. Reinicie bot e Discord
```

### Problema: SminDeck não abre
```
Solução:
1. Tente executar como Administrador
2. Verifique se arquivo existe: SminDeck.exe
3. Verifique espaço em disco
4. Desative antivírus temporariamente
5. Tente em outro computador
```

### Problema: Conexão VPS recusada
```
Solução:
1. Verifique se VPS está online: ping 72.60.244.240
2. Verifique firewall Windows
3. Verifique configuração firewall do VPS
4. Tente conexão SSH para confirmar
```

---

## 📊 CHECKLIST DE VALIDAÇÃO

- [ ] Novo servidor Discord criado
- [ ] Bot Discord registrado no portal
- [ ] Token obtido e guardado
- [ ] Intents ativados
- [ ] Bot adicionado ao servidor
- [ ] Bot online no servidor
- [ ] SminDeck.exe instalado
- [ ] SminDeck executando sem erros
- [ ] Bot responde a "oi"/"olá"
- [ ] Modais funcionam
- [ ] Logs VPS mostram atividade

---

## 🎯 RESUMO DO FLUXO

```
┌─────────────────────────────────────┐
│   1. Novo Servidor Discord          │
│      ✓ Criado e configurado        │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   2. Bot Registrado                 │
│      ✓ Token obtido                │
│      ✓ Intents ativados            │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   3. Bot Adicionado ao Servidor     │
│      ✓ Online e respondendo        │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   4. SminDeck Instalado             │
│      ✓ Pronto para usar            │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   5. Integração Validada            │
│      ✓ Tudo funcionando            │
└─────────────────────────────────────┘
```

---

## 📞 SUPORTE

Se encontrar problemas:
1. Consulte TROUBLESHOOTING acima
2. Verifique logs do bot em VPS
3. Valide permissões no Discord
4. Teste com servidor de teste primeiro

---

**Status**: Pronto para instalação  
**Próximo passo**: Comece pela FASE 1

**Data**: 06/01/2026  
**Versão**: SminDeck v1.2
