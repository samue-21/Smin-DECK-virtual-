# 🧪 PLANO DE TESTE PRÁTICO - BOT INTERATIVO

## 📋 PRÉ-REQUISITOS

```
✅ Arquivo: bot_humanizado_interativo.py (criado)
✅ Arquivo: BOT_INTERATIVO_GUIA.md (criado)
✅ Arquivo: BOT_INTERATIVO_CLIENTE.md (criado)
✅ VPS: 72.60.244.240 (ativo)
✅ Discord: Servidor pronto para testes
✅ Usuario: root (acesso SSH)
```

---

## 🚀 PASSO 1: FAZER BACKUP DO BOT ANTIGO

```bash
# No VPS - Terminal PowerShell
plink -batch -pw "Amor180725###" -hostkey "ssh-ed25519 255 SHA256:qDiZjQytnIXPsyUf6AnkC65z2Oe5K+8WeAdFE/ae2GM" root@72.60.244.240 "cp /opt/smin-bot/bot_humanizado.py /opt/smin-bot/bot_humanizado.py.backup"

# Verificar
plink -batch -pw "Amor180725###" -hostkey "ssh-ed25519 255 SHA256:qDiZjQytnIXPsyUf6AnkC65z2Oe5K+8WeAdFE/ae2GM" root@72.60.244.240 "ls -la /opt/smin-bot/*.py"
```

---

## 📤 PASSO 2: COPIAR ARQUIVO NOVO PARA VPS

### Opção A: Via SCP (Recomendado)

```bash
# No seu PC - PowerShell
# Instalar WinSCP ou usar SCP

# Copiar arquivo
scp -P 22 "c:\Users\SAMUEL\Desktop\Smin-DECK virtual\bot_humanizado_interativo.py" root@72.60.244.240:/opt/smin-bot/

# Usar: Senha: Amor180725###
```

### Opção B: Via Base64 (Se SCP não funcionar)

```bash
# No seu PC - PowerShell
$filePath = "c:\Users\SAMUEL\Desktop\Smin-DECK virtual\bot_humanizado_interativo.py"
$fileContent = [System.IO.File]::ReadAllBytes($filePath)
$b64 = [System.Convert]::ToBase64String($fileContent)
Write-Host "Base64 length: $($b64.Length) chars"
# Copiar $b64 inteiro
```

```bash
# No VPS - via plink
plink -batch -pw "Amor180725###" -hostkey "ssh-ed25519 255 SHA256:qDiZjQytnIXPsyUf6AnkC65z2Oe5K+8WeAdFE/ae2GM" root@72.60.244.240 "echo '[COLAR BASE64 AQUI]' | base64 -d > /opt/smin-bot/bot_humanizado_interativo.py"

# Verificar
plink -batch -pw "Amor180725###" -hostkey "ssh-ed25519 255 SHA256:qDiZjQytnIXPsyUf6AnkC65z2Oe5K+8WeAdFE/ae2GM" root@72.60.244.240 "head -20 /opt/smin-bot/bot_humanizado_interativo.py"
```

---

## ⚙️ PASSO 3: ATUALIZAR ARQUIVO DE CARREGAMENTO DO BOT

### Localizar o arquivo principal do bot (discord_bot.py ou similar)

```bash
# Listar arquivos no VPS
plink -batch -pw "Amor180725###" -hostkey "ssh-ed25519 255 SHA256:qDiZjQytnIXPsyUf6AnkC65z2Oe5K+8WeAdFE/ae2GM" root@72.60.244.240 "ls -la /opt/smin-bot/*.py"
```

### Editar arquivo principal para carregar novo Cog

```bash
# Exemplo: Se arquivo é discord_bot.py
# Procurar por: from bot_humanizado import BotHumanizado
# Substituir por: from bot_humanizado_interativo import BotHumanizadoInterativo

# E procurar por: await bot.load_extension('bot_humanizado')
# Substituir por: await bot.load_extension('bot_humanizado_interativo')
```

---

## 🔄 PASSO 4: REINICIAR O BOT

```bash
# Reiniciar serviço
plink -batch -pw "Amor180725###" -hostkey "ssh-ed25519 255 SHA256:qDiZjQytnIXPsyUf6AnkC65z2Oe5K+8WeAdFE/ae2GM" root@72.60.244.240 "systemctl restart smin-bot"

# Verificar status
plink -batch -pw "Amor180725###" -hostkey "ssh-ed25519 255 SHA256:qDiZjQytnIXPsyUf6AnkC65z2Oe5K+8WeAdFE/ae2GM" root@72.60.244.240 "systemctl status smin-bot"

# Ver logs (últimas 20 linhas)
plink -batch -pw "Amor180725###" -hostkey "ssh-ed25519 255 SHA256:qDiZjQytnIXPsyUf6AnkC65z2Oe5K+8WeAdFE/ae2GM" root@72.60.244.240 "journalctl -u smin-bot -n 20 -f"
```

---

## ✅ PASSO 5: TESTES NO DISCORD

### TESTE 1: Bot Responde a Saudação

```
LOCAL: Canal do Discord (sala do bot)

1. Você digita: "oi"
2. Bot deve responder com:
   ✅ Saudação (Oi! / Olá! / E aí! etc)
   ✅ Título: "Bem-vindo ao SminBot!"
   ✅ Subtítulo: "Que tal eu te ajudar agora?"
   ✅ Opções Disponíveis (com 4 itens)
   ✅ 4 Botões: 🔗 🎥 🖼️ 💾

Se tudo aparecer: ✅ PASSOU
```

### TESTE 2: Atualizar Link (Fluxo Completo)

```
LOCAL: Canal do Discord

1. Digita: "oi"
2. Bot mostra menu
3. Clica botão: 🔗 Atualizar Link
4. Modal abre: "Qual botão você quer atualizar?"
   └─ Digita: 5
5. Modal abre: "Qual é a Nova URL?"
   └─ Cola: https://youtu.be/testelink
6. Bot responde:
   ✅ "Tudo Prontinho!"
   ✅ Mostra URL que foi enviada
   ✅ Mostra Botão 5
   ✅ Mostra Tipo: Link
   ✅ Mensagem de agradecimento

Se tudo aparece: ✅ PASSOU
```

### TESTE 3: Validação de Número Inválido

```
LOCAL: Canal do Discord

1. Digita: "oi"
2. Bot mostra menu
3. Clica botão: 🔗 Atualizar Link
4. Modal abre: "Qual botão você quer atualizar?"
   └─ Digita: 15 (INVÁLIDO - maior que 12)
5. Bot deve rejeitar com erro
6. Modal reabre para tentar novamente
   └─ Digita: 5 (VÁLIDO)
7. Continua fluxo normalmente

Se modal reabre: ✅ PASSOU
```

### TESTE 4: Validação de URL Inválida

```
LOCAL: Canal do Discord

1. Digita: "oi"
2. Bot mostra menu
3. Clica botão: 🔗 Atualizar Link
4. Modal abre: "Qual botão você quer atualizar?"
   └─ Digita: 5
5. Modal abre: "Qual é a Nova URL?"
   └─ Cola: www.youtube.com/teste (SEM http/https)
6. Bot deve rejeitar com erro
7. Modal reabre
   └─ Cola: https://www.youtube.com/teste (COM https)
8. Continua fluxo normalmente

Se valida URL: ✅ PASSOU
```

### TESTE 5: Atualizar Vídeo

```
LOCAL: Canal do Discord

1. Digita: "oi"
2. Bot mostra menu
3. Clica botão: 🎥 Atualizar Vídeo
4. Modal abre: "Qual botão você quer atualizar?"
   └─ Digita: 3
5. Modal abre: "Qual é o Novo Vídeo?"
   └─ Digita: promocao.mp4
6. Bot responde:
   ✅ "Tudo Prontinho!"
   ✅ Mostra vídeo enviado
   ✅ Mostra Botão 3
   ✅ Mostra Tipo: Vídeo

Se tudo aparece: ✅ PASSOU
```

### TESTE 6: Atualizar Imagem

```
LOCAL: Canal do Discord

1. Digita: "oi"
2. Bot mostra menu
3. Clica botão: 🖼️ Atualizar Imagem
4. Modal abre: "Qual botão você quer atualizar?"
   └─ Digita: 7
5. Modal abre: "Qual é a Nova Imagem?"
   └─ Digita: logo.png
6. Bot responde:
   ✅ "Tudo Prontinho!"
   ✅ Mostra imagem enviada
   ✅ Mostra Botão 7
   ✅ Mostra Tipo: Imagem

Se tudo aparece: ✅ PASSOU
```

### TESTE 7: Múltiplas Saudações

```
LOCAL: Canal do Discord

Digita cada uma (em mensagens separadas):
1. "oi" → Bot responde com menu
2. "ola" → Bot responde com menu
3. "olá" → Bot responde com menu
4. "e aí" → Bot responde com menu
5. "salve" → Bot responde com menu

Se todos geram menu: ✅ PASSOU
```

---

## 📊 CHECKLIST DE TESTES

```
FUNCIONALIDADE
[ ] Bot responde a saudações
[ ] Menu aparece corretamente
[ ] Botões funcionam (4 botões)

FLUXO LINK
[ ] Modal 1 abre (qual botão?)
[ ] Aceita números 1-12
[ ] Rejeita números < 1 ou > 12
[ ] Modal 2 abre (qual URL?)
[ ] Valida http/https
[ ] Confirmação aparece
[ ] Mensagem de agradecimento

FLUXO VÍDEO
[ ] Modal 1 abre
[ ] Modal 2 abre (qual vídeo?)
[ ] Valida extensões MP4/WebM/etc
[ ] Confirmação aparece
[ ] Mensagem de agradecimento

FLUXO IMAGEM
[ ] Modal 1 abre
[ ] Modal 2 abre (qual imagem?)
[ ] Valida extensões PNG/JPG/etc
[ ] Confirmação aparece
[ ] Mensagem de agradecimento

VALIDAÇÕES
[ ] Rejeita números inválidos
[ ] Rejeita URLs sem protocolo
[ ] Rejeita extensões inválidas
[ ] Modal reabre após erro
[ ] Mensagens de erro amigáveis

MENSAGENS
[ ] Saudações variadas (aleatórias)
[ ] "Tudo Prontinho!" aparece
[ ] Mostra dados corretos
[ ] Emoji aparecem corretamente
[ ] Agradecimentos personalizados

PERFORMANCE
[ ] Sem atrasos nas modais
[ ] Validações rápidas
[ ] Sem erros no console
[ ] Serviço não trava
```

---

## 🐛 TROUBLESHOOTING

### Bot não responde

```bash
# Verificar se serviço está rodando
plink -batch -pw "Amor180725###" -hostkey "ssh-ed25519 255 SHA256:qDiZjQytnIXPsyUf6AnkC65z2Oe5K+8WeAdFE/ae2GM" root@72.60.244.240 "systemctl status smin-bot"

# Verificar logs
plink -batch -pw "Amor180725###" -hostkey "ssh-ed25519 255 SHA256:qDiZjQytnIXPsyUf6AnkC65z2Oe5K+8WeAdFE/ae2GM" root@72.60.244.240 "journalctl -u smin-bot -n 50"
```

### Erro de sintaxe

```bash
# Verificar arquivo
plink -batch -pw "Amor180725###" -hostkey "ssh-ed25519 255 SHA256:qDiZjQytnIXPsyUf6AnkC65z2Oe5K+8WeAdFE/ae2GM" root@72.60.244.240 "python3 -m py_compile /opt/smin-bot/bot_humanizado_interativo.py"

# Se OK: nenhuma saída
# Se erro: mostra a linha
```

### Modal não abre

```
Verificar:
- Discord.py versão é 2.0+? (precisa de Modal)
- Arquivo foi copiado corretamente?
- Serviço foi reiniciado?
- Permissões no VPS? (ls -la /opt/smin-bot/)
```

### Validação não funciona

```
Verificar:
- Números 1-12 são aceitos?
- URL com http/https é aceita?
- Extensões de arquivo são reconhecidas?
- Modal reabre após erro?
```

---

## 📝 RESUMO DA EXECUÇÃO

### Ordem Recomendada:

```
1️⃣  Fazer backup do bot antigo (PASSO 1)
2️⃣  Copiar arquivo novo para VPS (PASSO 2)
3️⃣  Atualizar carregamento do Cog (PASSO 3)
4️⃣  Reiniciar serviço (PASSO 4)
5️⃣  Executar testes no Discord (PASSO 5)
6️⃣  Preencher checklist
7️⃣  Documentar resultados
```

---

## 🎯 OBJETIVO FINAL

```
Quando todos os testes passarem: ✅

✅ Bot responde automaticamente a saudações
✅ Menu com 4 botões aparece
✅ Fluxo de perguntas funciona (botão → conteúdo)
✅ Validações rejeitam entradas inválidas
✅ Confirmações aparecem corretamente
✅ Mensagens de agradecimento funcionam
✅ Sem erros ou travamentos
✅ Pronto para uso em produção!
```

---

## 📞 PRÓXIMAS ETAPAS (APÓS TESTES)

Se tudo passar:
- [ ] Integrar com banco de dados
- [ ] Processar atualizações reais
- [ ] Testar com clientes reais
- [ ] Manter backup do código

---

**Status:** 🔴 Aguardando Execução
**Data:** 6 de janeiro de 2026
**Próximo:** PASSO 1 - Fazer backup

