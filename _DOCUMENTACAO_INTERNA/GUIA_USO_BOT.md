# 🚀 SminDeck Bot - Guia de Uso

## ⭐ Discord é OPCIONAL!

**O app funciona 100% normal SEM Discord.**

Se você quiser integrar Discord, siga este guia.

---

## 🎯 Fluxo Completo

### Para o Cliente (Usuário Final)

#### 1️⃣ **Abrir SminDeck**
- Executar `main.py` ou `SminDeck.exe`
- App funciona normalmente, COM OU SEM Discord
- Clicar no botão **`🤖 BOT`** (parte inferior) quando quiser integrar

#### 2️⃣ **Escolher Como Integrar**
Uma janela pergunta: "Como você quer integrar?"

**Opção A: 🎮 Discord Automático** (RECOMENDADO)
- Clica SIM
- App abre Discord automaticamente
- Vai para o Passo 3A

**Opção B: 📝 Manual**
- Clica NÃO
- Vai para o Passo 3B

---

### 🎮 Opção A: Discord Automático

#### 3️⃣A **App abre Discord**
- Navegador abre `discord.com`
- Você entra/cria conta
- Cria ou entra em um servidor (público ou pessoal)

#### 4️⃣A **Adicionar Bot ao Servidor**
- Bot aparece pedindo permissão
- Você clica "Sim, adicionar"
- Bot entra no servidor

#### 5️⃣A **Bot Cria Tudo Automaticamente**
O app mostra:
- `1️⃣ Abrindo Discord...`
- `2️⃣ Aguardando... (crie/entre em um servidor)`
- `3️⃣ Solicitando adição do bot`
- `4️⃣ Bot criando sala`
- `5️⃣ Gerando sua chave`

Bot faz automaticamente:
- ✓ Detecta novo servidor
- ✓ Cria sala `#sminbot`
- ✓ Gera chave única
- ✓ Retorna para app

#### 6️⃣A **Pronto!**
- App mostra: "Chave: ABC12345"
- Chave salva automaticamente
- ✅ **Sem mais nenhuma configuração!**

---

### 📝 Opção B: Manual (Tradicional)

#### 3️⃣B **Ir ao Discord e Executar Comando**
No servidor onde quer integrar:
```
/setup botao:1
```
(ou outro número de botão)

#### 4️⃣B **Bot Envia Chave via DM**
Bot envia mensagem privada:
```
✓ Sua chave de conexão:
   ABC12345

Cole esta chave no SminDeck quando solicitado
```

#### 5️⃣B **Colar Chave no App**
- App mostra dialog: "Cole a chave recebida"
- Você cola: `ABC12345`
- Clica `✓ Conectar`

#### 6️⃣B **Aguardar Conexão**
- Checkbox aparece: `☐ Conectando com o bot... Aguarde`
- App faz automaticamente:
  - ✓ Valida a chave
  - ✓ Conecta ao bot no VPS
  - ✓ Baixa as URLs cadastradas

#### 7️⃣B **Pronto!**
- Checkbox muda para: `☑ Conectado!`
- URLs aparecem nos botões (1-12)
- Sala já criada no Discord
- Sala do bot criada e pronta no servidor Discord do cliente
- **SEM NENHUMA CONFIGURAÇÃO EXTRA!**

---

## 🤖 Para o Bot (Servidor Discord)

### Comandos Disponíveis

#### `/setup`
Gera uma chave de conexão para o usuário
```
/setup botao:3
```
**Resposta (DM):**
```
✓ Sua chave de conexão: ABC12345

Cole esta chave no SminDeck quando solicitado
```

#### `ola` (mensagem)
Usuário pode dizer "ola" no canal dedicado
```
Usuario: ola
Bot: Qual número do botão (1-12)?
Usuario: 3
Bot: Cole a URL do vídeo
Usuario: https://youtu.be/dQw4w9WgXcQ
Bot: ✓ Botão 3 atualizado!
```

---

## 📊 Arquivos Criados

```
SminDeck/
├── bot_connector.py          # Gerencia conexões
├── bot_key_ui.py             # Interface gráfica
├── bot_client_remote.py      # Cliente de teste
├── test_integration.py       # Script de teste
├── VPS_STATUS.md             # Guia VPS
└── main.py                   # [MODIFICADO] Adicionado botão 🤖 BOT
```

---

## 🔧 Arquitetura

```
Cliente (Windows)          VPS (Linux)
┌──────────────┐         ┌──────────────┐
│  SminDeck.py │◄────────┤  Discord Bot │
│ + bot_conn.. │         │  + API Flask │
│ + bot_key_ui │         │  + SQLite DB │
└──────────────┘         └──────────────┘
      ▲                         ▲
      │                         │
      └─────────► HTTP/5000 ◄───┘
              (conexão automática)
```

---

## ✅ Checklist de Implementação

- ✅ Bot Discord rodando no VPS (72.60.244.240:5000)
- ✅ API Flask funcional
- ✅ `bot_connector.py` - Gerenciador de chaves
- ✅ `bot_key_ui.py` - Interface amigável com checkbox
- ✅ `deck_window.py` modificado - Botão 🤖 BOT adicionado
- ✅ Sincronização automática de URLs
- ✅ Criação de sala automática no Discord
- ✅ Sistema de teste integrado

---

## 🎯 Fluxo de Dados

### 1. Cliente adiciona chave:
```
Cliente → [Chave: ABC12345] → VPS API
```

### 2. API valida e retorna URLs:
```
VPS API → [URLs: {1: "url1", 2: "url2", ...}] → Cliente
```

### 3. Cliente atualiza botões:
```
Cliente → [Atualiza BTN 1-12 com URLs] → Interface Visual
```

### 4. Bot cria sala automática:
```
VPS Bot → [Cria sala no Discord] → Servidor do Cliente
```

---

## 🐛 Troubleshooting

### ❌ "Bot não está respondendo"
```bash
# Verificar status no VPS
ssh root@72.60.244.240
systemctl status smin-bot.service
systemctl status smin-api.service
```

### ❌ "Chave inválida"
- Copiar chave exatamente como recebida (sensível a maiúsculas)
- Aguardar 30 segundos antes de tentar novamente

### ❌ "URLs não aparecem"
- Verificar internet
- Clicar novamente no botão 🤖 BOT
- Se persistir, desconectar e reconectar

---

## 📞 Suporte Técnico

**VPS:** `72.60.244.240`  
**API:** `http://72.60.244.240:5000`  
**Status:** ✅ Online e pronto

---

## 🎉 Pronto para Usar!

O sistema está 100% operacional e pronto para o cliente usar!

**Última atualização:** 06/01/2026 15:50 UTC
