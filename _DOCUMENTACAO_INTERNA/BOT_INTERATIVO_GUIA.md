# 🤖 Bot Interativo - Fluxo de Perguntas Passo-a-Passo

## 🎯 O que é novo?

O bot agora **pergunta passo-a-passo** para o cliente, ao invés de apenas mostrar instruções!

### ANTES (Estático)
```
Cliente clica: "🔗 Atualizar Link"
     ↓
Bot mostra: "Use: /atualizar_link [numero] [url]"
     ↓
Cliente tem que lembrar e digitar comando manual
```

### AGORA (Interativo) ✨
```
Cliente clica: "🔗 Atualizar Link"
     ↓
Bot abre Modal: "Em qual botão você quer atualizar?"
     ↓
Cliente digita: 5
     ↓
Bot abre Modal: "Qual é a nova URL?"
     ↓
Cliente cola: https://youtu.be/novo
     ↓
Bot confirma: "✅ Tudo prontinho! Em alguns minutos..."
     ↓
🎉 Pronto!
```

---

## 📋 Fluxo Completo por Categoria

### 🔗 ATUALIZAR LINK

```
Passo 1: Cliente clica botão "🔗 Atualizar Link"
    ↓
Modal abre com pergunta:
    ┌─────────────────────────────────┐
    │ Qual botão você quer atualizar? │
    │ Digite o número (1-12, ex: 5)   │
    │ [_______]                       │
    └─────────────────────────────────┘
    ↓
Passo 2: Cliente digita número (ex: 5)
    ↓
Modal abre com pergunta:
    ┌─────────────────────────────────┐
    │ 🔗 Qual é a Nova URL?            │
    │ (exemplo: https://youtu.be/...)  │
    │ [_______________________]        │
    └─────────────────────────────────┘
    ↓
Passo 3: Cliente cola URL
    ↓
Bot responde com confirmação:
    ╔════════════════════════════════╗
    ║ ✅ Tudo Prontinho!              ║
    ║                                ║
    ║ Em alguns minutos o Link       ║
    ║ do Botão 5 estará atualizado! ║
    ║                                ║
    ║ 🔗 Nova URL:                   ║
    ║ https://youtu.be/novo          ║
    ║                                ║
    ║ 🙏 Muito obrigado!              ║
    ╚════════════════════════════════╝
```

### 🎥 ATUALIZAR VÍDEO

```
Passo 1: Cliente clica botão "🎥 Atualizar Vídeo"
    ↓
Modal abre com pergunta:
    ┌─────────────────────────────────┐
    │ Qual botão você quer atualizar? │
    │ Digite o número (1-12, ex: 5)   │
    │ [_______]                       │
    └─────────────────────────────────┘
    ↓
Passo 2: Cliente digita número (ex: 3)
    ↓
Modal abre com pergunta:
    ┌──────────────────────────────────┐
    │ 🎥 Qual é o Novo Vídeo?          │
    │ (arquivo MP4, WebM ou link)      │
    │ [_______________________]        │
    └──────────────────────────────────┘
    ↓
Passo 3: Cliente envia arquivo ou link
    ↓
Bot responde com confirmação:
    ╔════════════════════════════════╗
    ║ ✅ Tudo Prontinho!              ║
    ║                                ║
    ║ Em alguns minutos o Vídeo      ║
    ║ do Botão 3 estará atualizado! ║
    ║                                ║
    ║ 🎥 Novo vídeo:                 ║
    ║ promo.mp4                      ║
    ║                                ║
    ║ 🙏 Muito obrigado!              ║
    ╚════════════════════════════════╝
```

### 🖼️ ATUALIZAR IMAGEM

```
Passo 1: Cliente clica botão "🖼️ Atualizar Imagem"
    ↓
Modal abre com pergunta:
    ┌─────────────────────────────────┐
    │ Qual botão você quer atualizar? │
    │ Digite o número (1-12, ex: 5)   │
    │ [_______]                       │
    └─────────────────────────────────┘
    ↓
Passo 2: Cliente digita número (ex: 7)
    ↓
Modal abre com pergunta:
    ┌──────────────────────────────────┐
    │ 🖼️ Qual é a Nova Imagem?         │
    │ (PNG, JPG, GIF, WebP ou link)   │
    │ [_______________________]        │
    └──────────────────────────────────┘
    ↓
Passo 3: Cliente envia arquivo ou link
    ↓
Bot responde com confirmação:
    ╔════════════════════════════════╗
    ║ ✅ Tudo Prontinho!              ║
    ║                                ║
    ║ Em alguns minutos a Imagem     ║
    ║ do Botão 7 estará atualizada! ║
    ║                                ║
    ║ 🖼️ Nova imagem:                ║
    ║ logo.png                       ║
    ║                                ║
    ║ 🙏 Muito obrigado!              ║
    ╚════════════════════════════════╝
```

---

## 📊 Mensagens Personalizadas

### Pergunta 1: Qual Botão? (Para todas as categorias)
```
Modal: "Qual botão você quer atualizar?"
├─ Placeholder: "Digite o número (1-12, ex: 5)"
├─ Validação: Apenas números 1-12
└─ Se errado: "❌ Número inválido! Escolha entre 1 e 12"
```

### Pergunta 2: Qual Arquivo/URL? (Varia por categoria)

#### Para Link:
```
Modal: "🔗 Qual é a Nova URL?"
├─ Descrição: "Você escolheu o Botão X"
├─ Placeholder: "https://youtu.be/..."
├─ Exemplos: YouTube, links, sites
└─ Validação: Deve começar com http:// ou https://
```

#### Para Vídeo:
```
Modal: "🎥 Qual é o Novo Vídeo?"
├─ Descrição: "Você escolheu o Botão X"
├─ Placeholder: "arquivo.mp4 ou https://..."
├─ Formatos: MP4, WebM, AVI, MOV
└─ Links: YouTube, Vimeo, Twitch
```

#### Para Imagem:
```
Modal: "🖼️ Qual é a Nova Imagem?"
├─ Descrição: "Você escolhido o Botão X"
├─ Placeholder: "imagem.png ou https://..."
├─ Formatos: PNG, JPG, JPEG, GIF, WebP
└─ Links: Qualquer link de imagem
```

### Confirmação Final

```
╔════════════════════════════════╗
║ ✅ Tudo Prontinho!              ║
║                                ║
║ Em alguns minutos o [TIPO]     ║
║ do Botão [X] estará           ║
║ atualizado!                     ║
║                                ║
║ [TIPO] [CONTEÚDO]:             ║
║ [ARQUIVO/URL ENVIADO]          ║
║                                ║
║ 🎯 O que foi feito?             ║
║ • Botão escolhido: X ✅        ║
║ • Tipo: LINK/VÍDEO/IMAGEM ✅  ║
║ • Status: Em processamento ⏳  ║
║                                ║
║ 🙏 Obrigado!                    ║
║ Muito obrigado por usar o bot! ║
║ Seu arquivo será atualizado    ║
║ em breve! ⚡                    ║
╚════════════════════════════════╝
```

---

## 💻 Classes Criadas

### 1. `BotHumanizadoInterativo(commands.Cog)`
- Menu principal com `/help`
- Listener para cumprimentos
- Integração com modals

### 2. `ModalEscolherBotao(discord.ui.Modal)`
- **Primeira pergunta:** "Em qual botão?"
- Valida 1-12
- Direciona para próximo modal conforme categoria

### 3. `ModalPerguntaURL(discord.ui.Modal)`
- **Segunda pergunta (Link):** "Qual URL?"
- Valida formato http/https
- Mostra confirmação

### 4. `ModalPerguntaVideo(discord.ui.Modal)`
- **Segunda pergunta (Vídeo):** "Qual vídeo?"
- Valida extensões MP4, WebM, etc
- Mostra confirmação

### 5. `ModalPerguntaImagem(discord.ui.Modal)`
- **Segunda pergunta (Imagem):** "Qual imagem?"
- Valida extensões PNG, JPG, GIF, WebP
- Mostra confirmação

### 6. `MenuPrincipal(discord.ui.View)`
- 4 botões principais
- Cada botão abre modal correspondente
- Dinâmico e interativo

---

## 🎮 Como Funciona Tecnicamente

### Fluxo de Execução

```
1. Cliente clica botão
   │
   ├─ atualizar_link()
   │  ├─ Cria: ModalEscolherBotao("Link", self)
   │  └─ Abre modal
   │
   ├─ atualizar_video()
   │  ├─ Cria: ModalEscolherBotao("Vídeo", self)
   │  └─ Abre modal
   │
   └─ atualizar_imagem()
      ├─ Cria: ModalEscolherBotao("Imagem", self)
      └─ Abre modal

2. Cliente responde primeira pergunta (botão)
   │
   └─ ModalEscolherBotao.on_submit()
      ├─ Valida número (1-12)
      ├─ Armazena: self.parent_view.botao_escolhido = numero
      └─ Chama método conforme tipo:
         ├─ _pergunta_url()
         ├─ _pergunta_video()
         └─ _pergunta_imagem()

3. Método abre segundo modal
   │
   ├─ ModalPerguntaURL(numero, self.parent_view)
   ├─ ModalPerguntaVideo(numero, self.parent_view)
   └─ ModalPerguntaImagem(numero, self.parent_view)

4. Cliente responde segunda pergunta (arquivo/URL)
   │
   └─ ModalPergunta*.on_submit()
      ├─ Valida entrada
      └─ _confirmar(interaction, conteudo)

5. Confirmação final
   └─ Embed com mensagem de sucesso + agradecimento
```

---

## ✨ Validações Implementadas

### Modal 1 - Número do Botão
```
✅ Deve ser número (1-12)
❌ Rejeita: letras, símbolos, 0, 13+, vazio
```

### Modal 2 - URL (Link)
```
✅ Deve começar com: http:// ou https://
✅ Aceita: YouTube, sites, links gerais
❌ Rejeita: URLs sem protocolo, vazio
```

### Modal 3 - Vídeo
```
✅ Deve ter extensão: .mp4, .webm, .avi, .mov
✅ OU ser link: youtube, youtu.be, vimeo, twitch
✅ OU começar com: http:// ou https://
❌ Rejeita: extensões inválidas, vazio
```

### Modal 4 - Imagem
```
✅ Deve ter extensão: .png, .jpg, .jpeg, .gif, .webp
✅ OU começar com: http:// ou https://
❌ Rejeita: extensões inválidas, vazio
```

---

## 🎨 Mensagens Personalizadas por Tipo

| Tipo | Cor | Pergunta | Validação | Confirmação |
|------|-----|----------|-----------|-------------|
| Link | 🟢 Green | "Qual URL?" | http/https | "Link atualizado!" |
| Vídeo | 🟢 Green | "Qual vídeo?" | MP4/WebM/link | "Vídeo atualizado!" |
| Imagem | 🟢 Green | "Qual imagem?" | PNG/JPG/GIF | "Imagem atualizada!" |

---

## 📱 User Experience

### Cliente Vê:

**Passo 1:**
```
Clica em: 🔗 Atualizar Link

Modal abre automaticamente:
┌─────────────────────┐
│ Qual botão?         │
│ [Digite aqui]       │
└─────────────────────┘
```

**Passo 2:**
```
Digita: 5

Modal abre automaticamente:
┌──────────────────────────────┐
│ Qual é a Nova URL?           │
│ Você escolheu o Botão 5       │
│ [Cola a URL aqui]            │
└──────────────────────────────┘
```

**Passo 3:**
```
Cola: https://youtu.be/novo

Bot responde:
✅ Tudo Prontinho!
Em alguns minutos o Link do
Botão 5 estará atualizado!
🙏 Muito obrigado!
```

---

## 🔄 Como Integrar

### No `discord_bot.py`:

```python
from bot_humanizado_interativo import BotHumanizadoInterativo

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    
    # Carregar cogs
    await bot.load_extension('bot_humanizado_interativo')
    await bot.load_extension('bot_file_sync')

bot.run(TOKEN)
```

---

## 🎯 Benefícios

✅ **Mais Intuitivo** - Cliente não precisa lembrar comando
✅ **Conversacional** - Bot pergunta, cliente responde
✅ **Seguro** - Valida todas as entradas
✅ **Educado** - Mensagens de erro amigáveis
✅ **Agradecido** - Mensagem de obrigado no final
✅ **Organizado** - Tudo passo-a-passo
✅ **Dinâmico** - Perguntas mudam conforme categoria

---

## 📝 Exemplos Reais

### Exemplo 1: Atualizar Link do Botão 1
```
Cliente: /help
         [Clica 🔗 Atualizar Link]
         
Bot: Modal - "Em qual botão?"
Cliente: 1

Bot: Modal - "Qual URL?"
Cliente: https://youtu.be/dQw4w9WgXcQ

Bot: ✅ Tudo prontinho!
     Link do Botão 1 será atualizado!
     Obrigado por usar o bot! 🤖
```

### Exemplo 2: Atualizar Vídeo do Botão 8
```
Cliente: /help
         [Clica 🎥 Atualizar Vídeo]
         
Bot: Modal - "Em qual botão?"
Cliente: 8

Bot: Modal - "Qual vídeo?"
Cliente: promo_novo.mp4

Bot: ✅ Tudo prontinho!
     Vídeo do Botão 8 será atualizado!
     Obrigado por usar o bot! 🤖
```

### Exemplo 3: Atualizar Imagem do Botão 12
```
Cliente: /help
         [Clica 🖼️ Atualizar Imagem]
         
Bot: Modal - "Em qual botão?"
Cliente: 12

Bot: Modal - "Qual imagem?"
Cliente: logo_novo.png

Bot: ✅ Tudo prontinho!
     Imagem do Botão 12 será atualizada!
     Obrigado por usar o bot! 🤖
```

---

## 🚀 Status

✅ **Arquivo:** `bot_humanizado_interativo.py`
✅ **Linhas:** 450+ linhas
✅ **Classes:** 6 classes (1 Cog + 5 Modals)
✅ **Validações:** Completas
✅ **Mensagens:** Personalizadas por tipo
✅ **Pronto para:** Deploy no VPS

---

**Arquivo:** [bot_humanizado_interativo.py](bot_humanizado_interativo.py)

Próximo passo: Substituir `bot_humanizado.py` por `bot_humanizado_interativo.py` no VPS!
