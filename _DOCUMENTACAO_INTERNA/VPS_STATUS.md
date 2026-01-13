# 🎯 SminDeck Bot - Arquitetura Remota

## Status: ✅ PRONTO PARA USAR

---

## 🖥️ Infraestrutura VPS

**Servidor:** Hostinger Linux VPS  
**IP:** `72.60.244.240`  
**SO:** Ubuntu 22.04 LTS  
**Python:** 3.10.6

### Serviços Rodando

#### 1️⃣ Discord Bot (`smin-bot.service`)
- **Status:** ✅ Active (running)
- **Componente:** `discord_bot.py`
- **Porta:** Conecta ao Discord API
- **Auto-restart:** Habilitado

```bash
# Verificar status
systemctl status smin-bot.service

# Ver logs
journalctl -u smin-bot.service -f

# Reiniciar
systemctl restart smin-bot.service
```

#### 2️⃣ API Flask (`smin-api.service`)
- **Status:** ✅ Active (running)
- **Componente:** `api_server.py`
- **Porta:** 5000
- **Acesso:** http://72.60.244.240:5000
- **Auto-restart:** Habilitado

```bash
# Verificar status
systemctl status smin-api.service

# Ver logs
journalctl -u smin-api.service -f

# Reiniciar
systemctl restart smin-api.service
```

---

## 📡 Arquivos no VPS

```
/opt/smin-bot/
├── discord_bot.py      # Bot Discord principal
├── api_server.py       # API Flask (endpoints)
├── db.py              # Banco de dados SQLite
├── requirements.txt   # Dependências
├── .env              # Variáveis de ambiente (TOKEN)
└── venv/             # Ambiente Python virtual
    └── lib/python3.10/site-packages/
        ├── discord.py
        ├── flask
        ├── flask_cors
        └── python_dotenv
```

---

## 🔌 Endpoints da API

### 1. Health Check
```
GET /api/health
Response: {
  "status": "online",
  "message": "API SminDeck Bot está funcionando!"
}
```

### 2. Buscar URLs
```
GET /api/deck/{connection_key}
Response: {
  "connection_key": "ABC12345",
  "urls": {
    1: "https://youtube.com/watch?v=...",
    2: "https://youtube.com/watch?v=...",
    ...
  }
}
```

### 3. Verificar Chave
```
GET /api/verify/{connection_key}
Response: {
  "connection_key": "ABC12345",
  "valid": true
}
```

---

## 💻 Client (SminDeck Local)

### Arquivo: `bot_client_remote.py`

```python
from bot_client_remote import bot

# Verificar se está online
if bot.health_check():
    print("✓ Bot está online!")

# Obter URLs
urls = bot.get_urls("ABC12345")
print(urls)

# Verificar chave
if bot.verify_key("ABC12345"):
    print("✓ Chave válida")
```

---

## 🔐 Token Discord

**Localização:** `/opt/smin-bot/.env`

```env
DISCORD_TOKEN=SEU_TOKEN_AQUI
API_PORT=5000
```

**Para trocar o token:**
```bash
ssh root@72.60.244.240

# Editar arquivo
nano /opt/smin-bot/.env

# Salvar (Ctrl+X, Y, Enter)

# Reiniciar bot
systemctl restart smin-bot.service
```

---

## 📊 Banco de Dados

**Localização:** `/root/.smindeckbot/smindeck_bot.db`

**Tabelas:**
- `connection_keys` - Chaves de conexão por servidor Discord
- `urls` - URLs dos botões (1-12)
- `server_settings` - Configurações por servidor

---

## 🐛 Troubleshooting

### Bot não responde
```bash
# Verificar se está rodando
systemctl status smin-bot.service

# Ver últimos 50 logs
journalctl -u smin-bot.service -n 50 --no-pager

# Reiniciar
systemctl restart smin-bot.service
```

### API retorna erro
```bash
# Testar conexão
curl http://72.60.244.240:5000/api/health

# Ver logs
journalctl -u smin-api.service -n 50 --no-pager

# Verificar porta
ss -tlnp | grep 5000
```

### Conexão SSH para editar arquivos
```bash
ssh root@72.60.244.240
# Senha: Amor180725###

# Entrar na pasta do bot
cd /opt/smin-bot

# Editar arquivos
nano api_server.py
nano discord_bot.py
nano .env

# Salvar (Ctrl+X, Y, Enter)
```

---

## 🚀 Inicialização Automática

Ambos os serviços são habilitados para iniciar automaticamente após reboot:

```bash
# Verificar habilitação
systemctl is-enabled smin-bot.service   # Deve retornar 'enabled'
systemctl is-enabled smin-api.service   # Deve retornar 'enabled'
```

---

## 📈 Próximos Passos

1. **Integrar ao SminDeck.py**: Usar `bot_client_remote.py` para conectar
2. **Configurar HTTPS**: Usar certificado SSL (para produção)
3. **Adicionar Nginx reverse proxy**: Para melhor performance
4. **Backup automático**: Configurar backup do banco de dados

---

## 📞 Informações Úteis

- **VPS IP:** 72.60.244.240
- **API Base URL:** http://72.60.244.240:5000
- **SSH Port:** 22
- **SSH User:** root
- **SSH Pass:** Amor180725###

---

**Status Geral:** ✅ **SISTEMA OPERACIONAL E PRONTO PARA USO**

Última atualização: 06/01/2026 15:42 UTC
