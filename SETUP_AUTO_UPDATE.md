# 🚀 Setup do Auto-Update - Guia Completo

## 📋 Opções Disponíveis

O sistema de auto-update agora suporta **múltiplos endpoints** em ordem de prioridade:

### 1. **VPS Principal** (72.60.244.240:8000)
- Status: ❌ Indisponível
- Quando ficar online, será usado automaticamente

### 2. **VPS do Bot**
- Status: ⏳ Aguardando configuração
- **IP/URL**: Você precisa informar
- Melhor opção para seu caso

### 3. **Servidor Local** (para testes)
- Status: ⏳ Disponível
- Rodando em `http://localhost:8000`

---

## 🔧 Configuração

### Editar `update_config.py`

```python
"bot_vps": {
    "name": "VPS do Bot",
    "api_url": "http://SEU_IP_VPS:8000",  # ⚠️ ALTERAR AQUI
    "check_endpoint": "/api/updates/check",
    "download_base": "/download",
    "active": True  # ✅ ATIVAR AQUI
}
```

---

## 📦 Deploy no VPS do Bot

### 1. Copiar servidor para o VPS:
```bash
scp vps_update_server.py root@seu_ip_vps:/root/
scp setup_vps_bot.sh root@seu_ip_vps:/root/
```

### 2. Executar setup (SSH no VPS):
```bash
ssh root@seu_ip_vps
chmod +x setup_vps_bot.sh
./setup_vps_bot.sh
```

### 3. Verificar status:
```bash
systemctl status smin-updates
journalctl -u smin-updates -f  # Ver logs em tempo real
```

### 4. Fazer deploy de atualização:
```bash
# No seu PC local
python deploy.py "Descrição das mudanças"
```

---

## ✅ Fluxo Completo

```
┌─────────────────────────────────────────┐
│     Seu PC Local                         │
│  1. Editar código                        │
│  2. python deploy.py "mudanças"         │
│  3. Pacote ZIP criado e enviado         │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│     VPS do Bot (Servidor de Updates)    │
│  /root/smin_deck_updates/               │
│  - smin_deck_v1.0.1.zip                 │
│  - current_version.json                 │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│     App Instalado (Cliente)             │
│  A cada 1 minuto (testes):              │
│  GET /api/updates/check                 │
│  ↓ (se houver novo)                     │
│  GET /download/smin_deck_v1.0.1.zip     │
│  ↓ Extrai e atualiza                    │
│  ✅ Pronto!                             │
└─────────────────────────────────────────┘
```

---

## 🔄 Processo de Atualização (Cliente)

1. **Daemon inicia** ao abrir o app (thread background)
2. **A cada 1 minuto** tenta cada endpoint ativo em ordem:
   - VPS Principal (se ativo)
   - VPS do Bot (se ativo)
   - Servidor Local (se ativo)
   - GitHub (fallback)
3. **Se encontrar nova versão**, faz download e atualiza
4. **App continua rodando** sem reiniciar

---

## 🧪 Testar Localmente

### 1. Iniciar servidor local:
```bash
# Terminal 1
python vps_update_server.py
```

### 2. Ativar servidor local em `update_config.py`:
```python
"local": {
    ...
    "active": True
}
```

### 3. Fazer deploy local:
```bash
# Terminal 2
python deploy_local.py "Teste local"
```

### 4. Ver app atualizando:
```bash
# Terminal 3
python main.py
# Observe os logs de atualização
```

---

## 📊 Status Atual

✅ Sistema de deploy criado
✅ Suporte a múltiplos endpoints
✅ Auto-update funcionando a cada 1 minuto (testes)
⏳ Aguardando configuração do VPS do Bot

---

## 🎯 Próximos Passos

1. [ ] Informar IP/URL do VPS do Bot
2. [ ] Copiar arquivos para o VPS
3. [ ] Executar `setup_vps_bot.sh`
4. [ ] Atualizar `update_config.py` com novo IP
5. [ ] Testar com `python deploy.py "teste"`
6. [ ] Verificar atualização no app (esperar 1-2 min)

