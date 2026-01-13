# 📤 Sistema de Upload e Sincronização de Arquivos - SminDeck

## 🎯 Visão Geral

Sistema completo de upload, otimização e sincronização de mídia (vídeos e imagens) entre Discord Bot e aplicação desktop.

---

## 🔄 Fluxo de Funcionamento

### 1️⃣ **Cliente envia arquivo no Discord**
```
Cliente: "oi" → Seleciona "Botão 5" → Seleciona "Atualizar Vídeo" → Envia arquivo.mp4
```

### 2️⃣ **Bot processa e otimiza**
- Detecta o arquivo anexado
- Valida extensão (MP4, MKV, AVI, MOV para vídeo | JPG, PNG, WEBP para imagem)
- **Módulo `arquivo_processor.py`** otimiza:
  - **Vídeo**: Reduz para 720p, bitrate 2Mbps com ffmpeg
  - **Imagem**: Redimensiona para máx 1920x1080, comprime a 85% JPEG
- Salva em `/opt/smindeck-bot/uploads/` com nome: `video_botao_5.mp4`

### 3️⃣ **Bot registra no banco de dados**
```python
registrar_atualizacao(chave, 'video', 5, {'conteudo': 'video_botao_5.mp4'})
```
- Tipo: `'video'` ou `'imagem'`
- Dados: Nome do arquivo otimizado
- ID: Retornado para rastreamento

### 4️⃣ **API serve o arquivo (GET)**
```
GET /api/arquivo/video_botao_5.mp4 → Retorna arquivo binário
```

### 5️⃣ **App sincroniza (a cada 5 segundos)**
- `sincronizador.py` busca atualizações: `GET /api/atualizacoes`
- Detecta que é arquivo: `tipo='video'`
- **Faz download**: `GET /api/arquivo/video_botao_5.mp4`
- Salva em: `~/.smindeckbot/downloads/video_botao_5.mp4`
- Aplica na memória do app (não no arquivo JSON)
- Após 2 segundos, **deleta do VPS**: `DELETE /api/arquivo/video_botao_5.mp4`

### 6️⃣ **App mostra o vídeo no Botão 5**
- Botão 5 exibe: `"video_botao_5.mp4"`
- Quando fechar o app, salva tudo no `deck_config.sdk`

---

## 📁 Estrutura de Diretórios

### VPS (`/opt/smindeck-bot/`)
```
uploads/
  ├── video_botao_5.mp4       ← Arquivo otimizado
  ├── imagem_botao_3.jpg      ← Imagem comprimida
  └── ...
```

### Windows (`~/.smindeckbot/`)
```
downloads/
  ├── video_botao_5.mp4       ← Baixado do VPS
  ├── imagem_botao_3.jpg      ← Pronto para usar
  └── ...
```

---

## 📚 Módulos Criados/Modificados

### 1. `arquivo_processor.py` (NOVO)
**Função**: Otimizar mídia com ffmpeg e PIL

**Funções principais**:
- `processar_video(arquivo_path, output_filename)` → Reduz 720p + 2Mbps
- `processar_imagem(arquivo_path, output_filename)` → Redimensiona + 85% JPEG
- `processar_arquivo(arquivo_path, tipo, botao)` → Wrapper genérico
- `limpar_arquivo(filename)` → Deleta arquivo

**Requisitos**:
- `ffmpeg` instalado no VPS (`apt install ffmpeg`)
- Python PIL/Pillow (`pip install Pillow`)

---

### 2. `bot.py` (MODIFICADO)
**Adição**: Função `processar_arquivo_usuario()`

**O que faz**:
1. Detecta anexo (`message.attachments`)
2. Valida tipo (MP4, JPG, etc)
3. Faz download do servidor Discord
4. Chama `arquivo_processor.processar_arquivo()`
5. Registra no banco com nome do arquivo
6. Responde ao usuário com sucesso

**Fluxo**:
```python
if message.attachments:
    await processar_arquivo_usuario(message, user_id, opcao, botao)
```

---

### 3. `api_server.py` (MODIFICADO)
**Novos endpoints**:

#### GET `/api/arquivo/<filename>`
```
Serve arquivo binário do diretório uploads/
Retorna: 200 + arquivo binário (ou 404)
```

#### DELETE `/api/arquivo/<filename>`
```
Deleta arquivo após consumo
Retorna: 200 (sucesso) ou 404 (não encontrado)
```

**Métodos helpers**:
- `_servir_arquivo(filename)` → Lê e serve arquivo
- `_deletar_arquivo(filename)` → Remove do servidor

---

### 4. `sincronizador.py` (MODIFICADO)
**Novas funções**:

#### `baixar_arquivo(filename: str) -> str`
```python
# Faz download de http://API/api/arquivo/video_botao_5.mp4
# Salva em ~/.smindeckbot/downloads/video_botao_5.mp4
# Retorna caminho ou None
```

#### `deletar_arquivo_vps(filename: str) -> bool`
```python
# Chama DELETE /api/arquivo/video_botao_5.mp4
# Limpa VPS após app consumir
```

#### `processar_atualizacoes()` (ATUALIZADO)
```python
# Agora retorna também:
{
    'botao_idx': 5,
    'file': '/home/samuel/.smindeckbot/downloads/video_botao_5.mp4',
    'tipo': 'video',
    'nome_arquivo': 'video_botao_5.mp4',  # Para deletar depois
    ...
}
```

---

### 5. `deck_window.py` (MODIFICADO)
**Atualização**: `sincronizar_atualizacoes()`

**Novo fluxo**:
1. Recebe `mudancas` do sincronizador
2. Para cada mudança:
   - Verifica se arquivo existe
   - Atualiza `self.button_files[idx]`
   - Atualiza visual do botão
3. Agenda deleção do VPS após 2 segundos

**Novo método**:
```python
def _deletar_arquivo_vps(self, filename: str):
    # Chama DELETE /api/arquivo/filename
    # Limpa VPS automaticamente
```

---

## 🚀 Deploy no VPS

### Pré-requisitos
```bash
# No VPS, instalar:
apt update
apt install ffmpeg
pip install Pillow aiohttp
```

### Passos
```bash
# 1. Enviar arquivos
python deploy_vps.py

# 2. Reiniciar serviços
ssh root@72.60.244.240
systemctl restart smindeck-bot
systemctl restart smindeck-api

# 3. Verificar logs
tail -f /opt/smindeck-bot/debug.log
```

---

## 🧪 Testando

### Teste manual
```
1. Abre app local
2. No Discord: "oi"
3. Seleciona "Botão 5"
4. Seleciona "Atualizar Vídeo"
5. Envia arquivo.mp4

Resultado esperado:
✅ Bot processa e otimiza
✅ Bot mostra: "ARQUIVO PROCESSADO! Botão 5 | 3.2MB"
✅ App sincroniza em 5 segundos
✅ Botão 5 mostra: "video_botao_5.mp4"
✅ Arquivo deletado do VPS
```

---

## 🔐 Segurança

### Proteções implementadas
- ✅ Validação de extensão (whitelist)
- ✅ Sanitização de filename (previne path traversal)
- ✅ Limite de tamanho implícito (Discord: 8MB free, 100MB nitro)
- ✅ Autenticação via chave (só usuário autenticado pode enviar)

---

## 📊 Tamanhos antes/depois

### Vídeo
```
Antes: 50MB (1080p, 8Mbps)
Depois: ~10MB (720p, 2Mbps)
Compressão: 80%
```

### Imagem
```
Antes: 5MB (PNG com alpha)
Depois: ~200KB (JPEG 85%)
Compressão: 96%
```

---

## ⚠️ Limitações

1. **Tamanho**: Discord limita a 8MB (free) ou 100MB (nitro)
2. **Tipos**: Apenas MP4, MKV, AVI, MOV (vídeo) e JPG, PNG, WEBP (imagem)
3. **Qualidade vídeo**: 720p é máximo para manter tamanho pequeno
4. **Espaço VPS**: Arquivos são deletados após consumo, mas considerar limite de disco

---

## 🐛 Troubleshooting

### "ffmpeg not found"
```bash
apt install ffmpeg
```

### "Erro ao processar arquivo"
Verificar:
- ✅ ffmpeg instalado
- ✅ Permissões em `/opt/smindeck-bot/uploads/`
- ✅ Espaço disco (100GB+)

### Arquivo não baixa no app
Verificar:
- ✅ API rodando (`http://72.60.244.240:5001/api/health`)
- ✅ Arquivo existe no VPS: `ls /opt/smindeck-bot/uploads/`
- ✅ Pasta downloads existe: `~/.smindeckbot/downloads/`

---

## 📝 Resumo

| Componente | Função | Status |
|-----------|--------|--------|
| Bot | Recebe arquivo, otimiza | ✅ Pronto |
| VPS uploads | Armazena arquivo | ✅ Pronto |
| API | Serve e deleta arquivo | ✅ Pronto |
| App | Baixa e sincroniza | ✅ Pronto |
| Cleanup | Deleta automático | ✅ Pronto |

Sistema completo e funcional! 🎉
