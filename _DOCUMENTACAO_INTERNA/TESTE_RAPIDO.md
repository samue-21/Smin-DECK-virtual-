# 🎯 Guia Rápido de Teste - Sistema de Download de URLs

## ⚡ Teste em 5 Minutos

### 1️⃣ Preparar um Arquivo no Google Drive

```
1. Abra https://drive.google.com
2. Clique em "+ Novo" → "Fazer upload de arquivo"
3. Escolha um vídeo (MP4) ou imagem (JPG/PNG)
4. Clique com direito no arquivo → "Compartilhar"
5. Mude para "Qualquer pessoa com o link"
6. Copie o link (algo assim):
   https://drive.google.com/file/d/1A2B3C4D5E6F7G8H9I0J/view?usp=sharing
```

### 2️⃣ Autenticar no Discord

```
No Discord, canal #smindeck:

Você: "oi"

Bot responde com:
🔐 CHAVE DE AUTENTICAÇÃO
Sua chave é: ABCD-EFGH-IJKL-MNOP

E mostra menu:
🎯 O QUE VOCÊ PRECISA?
  🔗 Atualizar Link
  🎥 Atualizar Vídeo ← CLIQUE AQUI
  🖼️ Atualizar Imagem
  📁 Menu de Conteúdo
```

### 3️⃣ Selecionar Vídeo

```
Você: Clica em "🎥 Atualizar Vídeo"

Bot responde:
📍 EM QUAL BOTÃO VOCÊ DESEJA ATUALIZAR?
Escolha o botão que deseja modificar:

[Botão 1] [Botão 2] ... [Botão 5] ← CLIQUE AQUI
```

### 4️⃣ Enviar a URL

```
Você: Copia e envia a URL do Drive:
https://drive.google.com/file/d/1A2B3C4D5E6F7G8H9I0J/view?usp=sharing

Bot começa a processar:

Mensagem 1: 📥 INICIANDO DOWNLOAD
🔗 URL: https://drive.google.com/file/d/1A2B3C4D5E6F7...
⏳ Fazendo download...

Mensagem 2: ⚙️ PROCESSANDO
Otimizando arquivo...

Mensagem 3 (final): ✅ PRONTO!
Botão 5
📁 video_botao_4.mp4
📊 8.5MB
✨ Sincronizado!
```

### 5️⃣ Verificar no App

```
1. Abra o app SminDeck local
2. Aguarde sincronização automática (5 segundos)
3. Clique no botão 5
4. Veja o vídeo/imagem aparecer!
```

## 🧪 Teste com Arquivo Pequeno

Para teste RÁPIDO, use um arquivo MÍNIMO:

```
Google Drive:
- Faça upload de uma imagem pequena (100KB) em PNG ou JPG
- Compartilhe com "Qualquer pessoa"
- Envie a URL ao bot
- Resultado em segundos!
```

## 🔍 Monitorando o Processamento

### Opção 1: Logs do Bot (VPS)
```bash
ssh root@72.60.244.240
tail -f /opt/smindeck-bot/debug.log

# Procure por:
📥 URL detectada para botão 4
📥 Iniciando download
⏳ Progresso: 2.5MB / 50.0MB
✅ Download concluído
⚙️ Processando arquivo
✅ URL processada com sucesso
```

### Opção 2: Logs Locais
```
Na pasta do projeto, abra: bot_debug.log
Verifique as mesmas mensagens
```

### Opção 3: Verificar Arquivo no VPS
```bash
ssh root@72.60.244.240
ls -lah /opt/smindeck-bot/uploads/

# Deve aparecer:
-rw-r--r-- 1 root root 8.5M Jan  7 18:20 video_botao_4.mp4
```

## ❌ Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| "Bot não responde a 'oi'" | Autentique no app primeiro (copie a chave gerada) |
| "URL não funciona" | Tente com Drive (mais fácil que MediaFire) |
| "Download travado" | Arquivo muito grande? Use < 100MB para teste |
| "Tipo não permitido" | Use .mp4 para vídeos, .jpg para imagens |
| "Erro de timeout" | Verifique conexão de internet |

## 📋 Checklist de Teste

- [ ] Bot respondendo no Discord
- [ ] Menu principal exibindo
- [ ] Botões funcionando
- [ ] Consegue escolher tipo (Vídeo/Imagem)
- [ ] Consegue escolher número do botão (1-12)
- [ ] URL é detectada (aparece "📥 INICIANDO DOWNLOAD")
- [ ] Download está progredindo (aparece "⏳ Progresso")
- [ ] Processamento funcionando (aparece "⚙️ PROCESSANDO")
- [ ] Mensagem final mostra "✅ PRONTO!"
- [ ] Arquivo aparece no app após sincronização

## 🎬 Vídeo do Fluxo Completo

```
1. Discord: "oi" ──→ Bot envia chave
2. App: Coloca chave ──→ Autentifica
3. Discord: "🎥 Atualizar Vídeo" ──→ Mostra botões
4. Discord: Clica "Botão 5" ──→ Aguarda URL
5. Discord: Envia URL Drive ──→ Bot faz download
6. Bot: 📥 🔄 ⚙️ ✅ ──→ Processa e registra
7. App: Sincroniza (5s) ──→ Aparece o vídeo
8. App: Clica botão 5 ──→ Toca o vídeo!
```

## 🚀 Teste Avançado (Opcional)

Se o teste básico funcionar, tente com:

- **MediaFire**: https://www.mediafire.com/file/ABC123/video.mp4
- **Link Direto**: Um arquivo em seu próprio servidor HTTP
- **Dropbox**: Um arquivo compartilhado com permissão pública
- **Imagem Grande**: Uma foto de 5MB para testar compressão

## ✅ Sucesso!

Se viu:
1. Download iniciando no Discord
2. Arquivo sendo processado
3. Mensagem "✅ PRONTO!" com tamanho final
4. Arquivo aparecendo no app após sincronizar

**PARABÉNS! O sistema está funcionando! 🎉**

---

**Tempo esperado de teste:** 3-5 minutos
**Tamanho recomendado:** < 100MB (teste rápido)
**Melhor para testar:** Google Drive (automático)

