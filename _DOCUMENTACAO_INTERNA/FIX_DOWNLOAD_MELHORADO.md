# 🔧 FIX - Sistema de Download Melhorado

## ✅ O que foi corrigido:

### 1️⃣ **Retry Automático (Multi-tentativas)**
- O bot agora tenta fazer download com **4 diferentes User-Agents**
- Se falhar com um, tenta com outro automaticamente
- Melhor compatibilidade com servidores

### 2️⃣ **Melhor Tratamento de Erros**
- HTTP 404 → Para de tentar (arquivo não encontrado)
- HTTP 403/401 → Para de tentar (acesso negado)
- HTTP 5xx → Tenta novamente com outro User-Agent
- Timeout → Tenta novamente
- Erros de conexão → Tenta novamente

### 3️⃣ **Suporte a BackBlaze B2**
- Adicionado suporte oficial para `f000.backblazeb2.com`
- Headers configurados corretamente
- Timeout aumentado para downloads grandes

### 4️⃣ **Melhor Tratamento de Nomes**
- Remove acentos e caracteres especiais
- `provaí-e-vede` → `prova-e-vede`
- Limita tamanho do nome (máx 50 caracteres)
- Preserva extensão corretamente

### 5️⃣ **Logs Mais Detalhados**
- Mostra qual User-Agent funcionou
- Mostra qual tentativa está sendo feita
- Mostra erros específicos (404, 403, timeout, etc)

## 🧪 Teste com seu arquivo:

### Opção 1: Envie a URL de novo
```
Discord: "oi"
Menu: "🎥 Atualizar Vídeo"
Botão: Escolha um botão
URL: https://f000.backblazeb2.com/file/deptos/mordomia/provaí-e-vede/2026/episódios/01-10-26_%20primícias-de-fe.mp4
```

Bot agora vai tentar com múltiplos User-Agents!

### Opção 2: Ver logs em tempo real
```bash
ssh root@72.60.244.240
tail -f /opt/smindeck-bot/debug.log | grep -E "Tentativa|User-Agent|Downloaded|Progresso"
```

Procure por:
```
⏳ Tentativa 1/4...
⏳ Tentativa 2/4...
✅ Download concluído: prova-e-vede.mp4
```

## 📊 User-Agents Usados (em ordem):

1. **Mozilla (Windows)** - Firefox padrão
2. **Mozilla (Linux)** - Chrome padrão
3. **VLC** - Para servidores que bloqueiam bots
4. **ffmpeg** - Para servidores específicos

## 🔍 Se ainda não funcionar:

### Debug da URL:

```bash
# No seu PC, teste manualmente:
curl -I "https://f000.backblazeb2.com/file/deptos/mordomia/provaí-e-vede/2026/episódios/01-10-26_%20primícias-de-fe.mp4"

# Ou no VPS:
ssh root@72.60.244.240
curl -I "https://seu-url-aqui"
```

### Possíveis causas:

❌ **URL com acentos** → Tente URL-encodeada
   Isso: `prova%C3%AD-e-vede`
   
❌ **Servidor bloqueia bots** → Tente com VLC User-Agent
   ✅ Agora feito automaticamente!

❌ **Arquivo temporariamente indisponível** → Aguarde e tente de novo

❌ **Servidor tem rate limiting** → Tente de novo em alguns minutos

## 📈 Melhorias implementadas:

```
ANTES:
- ❌ 1 tentativa apenas
- ❌ 1 User-Agent
- ❌ Poucas informações de erro
- ❌ Falha em URLs com acentos

DEPOIS:
- ✅ 4 tentativas automáticas
- ✅ 4 User-Agents diferentes
- ✅ Logs detalhados de cada tentativa
- ✅ Remove acentos de nomes
- ✅ Melhor tratamento de erros HTTP
```

## 🚀 Deploy Realizado:

```
✅ download_manager.py atualizado
✅ Bot reiniciado (PID 38969)
✅ Pronto para teste!
```

## 📞 Teste Agora:

1. Vá ao Discord
2. Envie a URL de novo
3. Veja os logs:
   ```bash
   tail -f /opt/smindeck-bot/debug.log
   ```
4. Aguarde as tentativas automáticas
5. Se funcionar: 🎉
6. Se não: Veja qual tentativa funcionou melhor

---

**Versão:** 2.0 (com retry automático)
**Data:** 07/01/2026 18:30:52 UTC
**Status:** ✅ DEPLOYADO
