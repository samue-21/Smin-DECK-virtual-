# 📂 Arquivos Gerais - Integração Completa

## 🎯 Visão Geral

**Objetivo:** Sincronizar automaticamente arquivos enviados no Discord com a pasta local `Arquivos Gerais` do app.

**Resultado:** Cliente envia arquivo no Discord → Salva automático na pasta local → Acessa no app!

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    SINCRONIZAÇÃO AUTOMÁTICA                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Discord Server              ↔️          Windows/Mac/Linux  │
│   ┌──────────────────┐                   ┌────────────────┐ │
│   │ Cliente envia    │                   │  SminDeck App  │ │
│   │ arquivo para bot │    bot_file_sync  │                │ │
│   │                  │─────────→─────────│  Pasta Local   │ │
│   │ (attachment)     │                   │  ~/.smindeckbot│ │
│   │                  │                   │  /arquivos_    │ │
│   │ @bot upload      │                   │   gerais/      │ │
│   │ [PDF/IMG/VID]    │                   │                │ │
│   └──────────────────┘                   └────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Fluxo Completo

### Passo 1: Cliente no Discord

```
Cliente Discord:
1. Clica "/help"
   ↓
2. Vê menu com 4 botões
   [🔗 Link] [🎥 Vídeo] [🖼️ Imagem] [💾 Arquivo]
   ↓
3. Clica "💾 Enviar Arquivo"
   ↓
4. Bot responde com instruções:
   "Como enviar?
    1. Clique em [+] ao lado do campo
    2. Escolha "Enviar arquivo"
    3. Selecione o arquivo
    4. Envie aqui no Discord
    
    ✨ Será salvo automaticamente em Arquivos Gerais!"
```

### Passo 2: Cliente Envia Arquivo

```
Cliente Discord:
1. Clica [+] do lado da msg
2. Seleciona "Enviar arquivo"
3. Escolhe arquivo (PDF, IMG, VID, etc)
4. Clica em "Enviar"
   ↓
Discord: Arquivo enviado para canal
   ↓
Bot detecta: "on_message() triggered"
   ↓
Checar: message.attachments exists?
   ↓
SIM! → Download automático
   ↓
Bot confirma: "✅ Arquivo recebido!"
             "📂 Salvo em Arquivos Gerais!"
```

### Passo 3: Bot Processa (BotFileSync)

```
BotFileSync.on_message() triggered:
   ↓
1. Verificar se tem attachment
   ✓ Sim = prosseguir
   ✗ Não = ignorar
   ↓
2. Para cada arquivo:
   ↓
   _baixar_arquivo(attachment, username):
   ├─ Criar timestamp: 20260106_143000
   ├─ Preservar extensão: arquivo.pdf
   ├─ Nome final: 20260106_143000_arquivo.pdf
   ├─ Caminho: ~/.smindeckbot/arquivos_gerais/
   ├─ Download HTTP do Discord
   ├─ Salvar no disco
   └─ Log: "✅ Arquivo baixado: 20260106_143000_arquivo.pdf"
   ↓
3. Confirmar no Discord:
   "✅ 1 arquivo recebido!
    📂 Salvo em Arquivos Gerais!
    
    Você pode:
    • Abrir pasta no app
    • Arrastar em botões (drag-drop)
    • Adicionar como mídia"
```

### Passo 4: App Acessa Arquivo

```
No SminDeck App:
1. Menu → Arquivos Gerais
   ↓
2. Vê arquivo recém-salvo:
   "20260106_143000_documento.pdf"
   ↓
3. Opções:
   A) Abrir arquivo
   B) Drag-drop em botão para atualizar
   C) Adicionar como mídia (vídeo/imagem)
   ↓
4. Pronto! Arquivo no app
```

---

## 🗂️ Estrutura de Pastas

### Criar a Pasta

A pasta é criada **automaticamente** quando o bot inicia:

```python
# bot_file_sync.py - __init__
os.makedirs(self.arquivos_gerais_path, exist_ok=True)
```

### Localização

**Windows:**
```
C:\Users\[SEU_USUÁRIO]\.smindeckbot\arquivos_gerais\
```

**Linux/Mac:**
```
~/.smindeckbot/arquivos_gerais/
```

### Conteúdo

```
arquivos_gerais/
├─ 20260106_143000_video.mp4         ← Vídeo enviado 14:30:00
├─ 20260106_150530_imagem.png        ← Imagem enviada 15:05:30
├─ 20260106_161200_documento.pdf     ← PDF enviado 16:12:00
├─ 20260107_091545_musica.mp3        ← MP3 enviado 07/01 09:15:45
└─ 20260107_102000_arquivo.zip       ← ZIP enviado 07/01 10:20:00
```

**Padrão do Nome:**
```
[AAAAMMDD]_[HHMMSS]_[nome_original]
│          │         │
│          │         └─ Nome do arquivo original
│          └─ Hora do envio (HH:MM:SS)
└─ Data do envio (YYYY:MM:DD)
```

---

## 🤖 Cogs Necessários

### 1️⃣ BotHumanizado (Já Pronto)

**Arquivo:** `bot_humanizado.py`

**Funcionalidade:**
- Menu `/help` com botões
- 4 botões: Link, Vídeo, Imagem, Enviar Arquivo
- Mensagens amigáveis
- Greetings automáticos

**Classes:**
```python
class BotHumanizado(commands.Cog):
    - help_humanized() → Mostra menu
    - on_message() → Responde cumprimentos

class MenuPrincipal(discord.ui.View):
    - atualizar_link() → Botão 1
    - atualizar_video() → Botão 2
    - atualizar_imagem() → Botão 3
    - enviar_arquivo() → Botão 4
```

### 2️⃣ BotFileSync (Novo!)

**Arquivo:** `bot_file_sync.py`

**Funcionalidade:**
- Detecta arquivo enviado
- Download automático
- Salva na pasta local
- Comandos auxiliares

**Classes:**
```python
class BotFileSync(commands.Cog):
    - on_message() → Detecta attachment
    - listar_arquivos() → Comando /listar_arquivos
    - limpar_arquivos() → Comando /limpar_arquivos
    - _baixar_arquivo() → Método auxiliar
```

---

## 🔌 Integração no Bot

### Arquivo: `discord_bot.py` (ou similar)

Adicionar imports:

```python
from bot_humanizado import BotHumanizado
from bot_file_sync import BotFileSync
```

Adicionar em `on_ready()`:

```python
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    
    # Carregar Cogs humanizados
    await bot.load_extension('bot_humanizado')
    await bot.load_extension('bot_file_sync')
    
    # Opcional: especificar caminho customizado
    # await BotFileSync.setup(bot, '/caminho/customizado')
```

### Ou em Main Loop:

```python
async def main():
    async with bot:
        # Carregar extensões
        await bot.load_extension('bot_humanizado')
        await bot.load_extension('bot_file_sync')
        
        # Conectar
        await bot.start(DISCORD_TOKEN)

# Rodar
asyncio.run(main())
```

---

## 📊 Comandos Disponíveis

### `/help` (Menu Principal)
```
Mostra: Menu com 4 botões
Acesso: Qualquer usuário
Resultado: Escolhe opção ou envia arquivo
```

### `/listar_arquivos` (Ver Arquivos)
```
Mostra: Lista de todos os arquivos na pasta
Acesso: Qualquer usuário
Resultado: Embed com:
   - Nome do arquivo
   - Tamanho
   - Total de arquivos
   - Total de espaço
```

### `/limpar_arquivos` (Remover Tudo)
```
Remove: Todos os arquivos
Acesso: Apenas ADMINISTRADOR
Resultado: Confirmação de quantos arquivos foram apagados
```

---

## 🎯 Casos de Uso

### Caso 1: Cliente Quer Atualizar Imagem

```
Cliente Discord: "Clica /help → 💾 Enviar Arquivo"
       ↓
Bot: "Como enviar? [instruções]"
       ↓
Cliente: Upload imagem.png
       ↓
Bot: "✅ Imagem salva em Arquivos Gerais!"
       ↓
Cliente App: Abre Arquivos Gerais
       ↓
Vê: "20260106_143000_imagem.png"
       ↓
Arrasta para botão (drag-drop)
       ↓
Botão atualizado! ✅
```

### Caso 2: Cliente Quer Compartilhar PDF

```
Cliente Discord: "Clica /help → 💾 Enviar Arquivo"
       ↓
Bot: "Como enviar? [instruções]"
       ↓
Cliente: Upload documento.pdf
       ↓
Bot: "✅ PDF salvo em Arquivos Gerais!"
       ↓
Cliente App: Abre Arquivos Gerais
       ↓
Vê: "20260106_150000_documento.pdf"
       ↓
Clica para abrir (lerá PDF)
       ↓
Visualiza conteúdo ✅
```

### Caso 3: Admin Quer Limpar Pasta

```
Admin Discord: "/limpar_arquivos"
       ↓
Bot: "⚠️ Remover todos? (admin only)"
       ↓
Bot: "🗑️ 5 arquivo(s) removido(s)!"
       ↓
Pasta vazia novamente
```

---

## 🔐 Permissões

| Comando | Qualquer Um | Admin |
|---------|-------------|-------|
| `/help` | ✅ | ✅ |
| Enviar arquivo | ✅ | ✅ |
| `/listar_arquivos` | ✅ | ✅ |
| `/limpar_arquivos` | ❌ | ✅ |

---

## ⚙️ Configuração Avançada

### Caminho Customizado

Se quiser salvar em outro lugar:

```python
# No discord_bot.py
import os
from bot_file_sync import BotFileSync

caminho_custom = os.path.expanduser('/pasta/customizada')

@bot.event
async def on_ready():
    await bot.load_extension('bot_humanizado')
    # Passar caminho customizado
    await BotFileSync.setup(bot, caminho_custom)
```

### Tamanho Máximo de Arquivo

Discord permite até 25MB por arquivo (limite nativo).

Se quiser adicionar validação:

```python
# Em bot_file_sync.py - _baixar_arquivo()
MAX_SIZE = 25 * 1024 * 1024  # 25MB

if attachment.size > MAX_SIZE:
    await message.reply(f"❌ Arquivo muito grande! (máx {MAX_SIZE/1024/1024}MB)")
    return
```

### Filtrar Extensões

Se quiser permitir apenas certos tipos:

```python
ALLOWED_EXTENSIONS = {'.pdf', '.png', '.jpg', '.mp4', '.mp3', '.xlsx'}

extension = os.path.splitext(attachment.filename)[1].lower()

if extension not in ALLOWED_EXTENSIONS:
    await message.reply(f"❌ Tipo de arquivo não permitido!")
    return
```

---

## 🧪 Testes

### Teste 1: Verificar Criação de Pasta

```bash
# Windows PowerShell
Test-Path "$env:userprofile\.smindeckbot\arquivos_gerais"

# Linux/Mac
[ -d ~/.smindeckbot/arquivos_gerais ] && echo "OK" || echo "Falha"
```

### Teste 2: Enviar Arquivo Pequeno

1. No Discord: `/help`
2. Clica `💾 Enviar Arquivo`
3. Upload pequeno (1MB)
4. Verifica pasta local

**Esperado:** Arquivo salvo com timestamp

### Teste 3: Listar Arquivos

1. No Discord: `/listar_arquivos`
2. Verifica se aparecem os arquivos

**Esperado:** Embed com lista completa

### Teste 4: Drag-Drop no App

1. Abre SminDeck → Arquivos Gerais
2. Arrasta arquivo para um botão
3. Atualiza botão

**Esperado:** Botão com novo arquivo

---

## 🚀 Próximos Passos

1. ✅ **Copiar `bot_humanizado.py` para VPS**
2. ✅ **Copiar `bot_file_sync.py` para VPS**
3. ✅ **Integrar imports em `discord_bot.py`**
4. ✅ **Adicionar `load_extension()` em `on_ready()`**
5. ✅ **Restart bot service**
6. ✅ **Testar `/help` no Discord**
7. ✅ **Testar envio de arquivo**
8. ✅ **Verificar pasta local**
9. ✅ **Testar drag-drop no app**

---

## 📝 Resumo

| Aspecto | Detalhe |
|--------|---------|
| **O quê?** | Sincronizar arquivos Discord → App |
| **Como?** | Bot detecta upload → Salva local |
| **Onde?** | `~/.smindeckbot/arquivos_gerais/` |
| **Quem?** | Qualquer usuário pode enviar |
| **Quando?** | Tempo real (imediato) |
| **Por quê?** | Facilita gerenciamento de mídia |
| **Resultado** | Cliente usa arquivo no app direto |

---

**Status: PRONTO PARA DEPLOY! 🚀**
