# 📥 Sistema de Download de URLs - SminDeck Bot

## 🎯 Visão Geral

O bot agora suporta fazer download de arquivos a partir de URLs, não apenas anexos diretos do Discord. Isso permite que o cliente envie arquivos grandes por serviços de hospedagem como:

- **Google Drive** 
- **MediaFire**
- **Dropbox**
- **OneDrive**
- **Links diretos** (HTTP/HTTPS)
- Qualquer servidor com suporte a downloads

## 📋 Características

### ✅ O que o Sistema Faz

1. **Detecta URLs automaticamente** na mensagem do usuário
2. **Processa URLs especiais**:
   - Google Drive: Extrai FILE_ID e converte para link direto de exportação
   - MediaFire: Faz parsing do HTML e extrai link de download
   - Outros: Faz download direto via HTTP
3. **Faz download do arquivo** com progress tracking
4. **Valida o arquivo**:
   - Verifica extensão (mp4, jpg, png, etc)
   - Verifica tamanho (máx 500MB)
   - Verifica se é acessível
5. **Processa o arquivo**:
   - Vídeos: Otimiza para 720p @ 2Mbps com ffmpeg
   - Imagens: Comprime com PIL (JPEG 85%)
6. **Registra no banco de dados** para sincronização
7. **Notifica o cliente** com embeds visuais

### 🚫 Limitações

- **Tamanho máximo**: 500MB
- **Timeout**: 5 minutos por download
- **Extensões permitidas**:
  - Vídeos: `.mp4, .mkv, .avi, .mov, .webm`
  - Imagens: `.jpg, .jpeg, .png, .webp, .bmp`
  - Áudio: `.mp3, .wav, .aac, .flac, .m4a, .ogg`

## 🔄 Fluxo de Uso

### 1️⃣ Autenticação (mesmo de antes)
```
Usuário: "oi"
Bot: Gera chave e mostra menu
```

### 2️⃣ Escolher Tipo (Vídeo/Imagem)
```
Usuário: Clica em "🎥 Atualizar Vídeo"
Bot: Pede para escolher botão
```

### 3️⃣ Escolher Botão (1-12)
```
Usuário: Clica em "Botão 5"
Bot: Aguarda arquivo/URL
```

### 4️⃣ Enviar URL (NOVO!)
```
Usuário: "https://drive.google.com/file/d/ABC123/view"
Bot: 
  📥 INICIANDO DOWNLOAD
  🔗 URL: https://drive.google.com/file/d/ABC123/view
  ⏳ Fazendo download...
  
  ⚙️ PROCESSANDO
  Otimizando arquivo...
  
  ✅ PRONTO!
  Botão 5
  📁 video_botao_4.mp4
  📊 8.5MB
  ✨ Sincronizado!
```

## 🔗 URLs Suportadas

### Google Drive
```
https://drive.google.com/file/d/{FILE_ID}/view
https://drive.google.com/file/d/{FILE_ID}/view?usp=sharing
```
✅ Funciona automaticamente - não precisa fazer nada especial!

### MediaFire
```
https://www.mediafire.com/file/{KEY}/filename
```
✅ Funciona automaticamente!

### Links Diretos
```
https://servidor.com/video.mp4
https://servidor.com/imagem.jpg
```
✅ Qualquer servidor HTTP/HTTPS funciona!

### Dropbox
```
https://www.dropbox.com/s/{PATH}/arquivo.mp4?dl=1
```
⚠️ Use `?dl=1` no final para garantir download direto

### OneDrive
```
https://1drv.ms/v/s!ABC123/embed
```
✅ Geralmente funciona

## 📊 Módulos Envolvidos

### `download_manager.py` (NOVO)
```python
async def download_arquivo(url, filename, index)
  - Faz download com timeout e validação
  - Suporta Google Drive e MediaFire automaticamente
  - Log de progresso

async def download_google_drive(url)
  - Extrai FILE_ID da URL
  - Retorna link direto de exportação

async def download_mediafire(url)
  - Faz parsing do HTML
  - Extrai link de download direto

def validar_extensao(filename)
  - Verifica se extensão é permitida
```

### `bot.py` (MODIFICADO)
```python
async def processar_arquivo_usuario(message, user_id, opcao, botao)
  - Detecta se é anexo ou URL
  - Chama função apropriada

async def processar_url_usuario(message, user_id, opcao, botao, url)
  - Faz download
  - Valida
  - Processa
  - Registra no banco
```

### `arquivo_processor.py` (sem mudanças)
```python
processar_arquivo(path, tipo, botao)
  - Comprime vídeos e imagens
  - Salva em /opt/smindeck-bot/uploads/
```

## 🛠️ Tratamento de Erros

| Erro | Mensagem | Solução |
|------|----------|---------|
| URL inválida | "❌ URL inválida" | Use `http://` ou `https://` |
| Arquivo grande | "❌ Arquivo muito grande: XXX MB" | Use arquivo menor que 500MB |
| Tipo não permitido | "❌ Tipo não permitido: .exe" | Use mp4, jpg, png, etc |
| Drive não acessível | "❌ Erro no download" | Verifique se link é público |
| Timeout | "❌ Timeout ao fazer download" | Tente de novo ou arquivo menor |
| MediaFire inválido | "❌ Não foi possível extrair link" | Use link direto do MediaFire |

## 📝 Logs

Os logs são salvos em:
- **VPS**: `/opt/smindeck-bot/debug.log`
- **Local**: `bot_debug.log`

Procure por:
```
📥 URL detectada para botão X
📥 Iniciando download de: https://...
⏳ Progresso: 5.2MB / 50.0MB (10.4%)
✅ Download concluído
⚙️ Processando arquivo
✅ URL processada com sucesso
```

## 🧪 Teste Rápido

1. Autentique-se: envie "oi"
2. Escolha "🎥 Atualizar Vídeo"
3. Escolha "Botão 1"
4. Envie uma URL:
   ```
   https://drive.google.com/file/d/1A2B3C4D5E6F7G8H9I0J/view
   ```
5. Aguarde o processamento
6. Veja a mensagem "✅ PRONTO!" com os detalhes

## 🔒 Segurança

- Validação de extensão (whitelist)
- Limite de tamanho (500MB)
- Timeout de 5 minutos
- User-Agent padrão para bypass de proteções
- SSL bypass para servidores problemáticos (ssl=False)

## 🚀 Deploy

Para usar o novo sistema no VPS:

```bash
# 1. Upload do download_manager.py
scp download_manager.py user@host:/opt/smindeck-bot/

# 2. Atualizar bot.py
scp bot.py user@host:/opt/smindeck-bot/

# 3. Reiniciar bot
ssh user@host "systemctl restart smindeck-bot"
```

Ou execute o `deploy_vps_auto.py` que já cuida de tudo!

## 📞 Suporte

Se tiver problemas:
1. Verifique se a URL é pública
2. Veja os logs em `/opt/smindeck-bot/debug.log`
3. Teste com um link direto primeiro
4. Verifique o tamanho do arquivo (< 500MB)
