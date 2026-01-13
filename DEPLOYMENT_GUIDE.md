# 🚀 Smin-DECK Virtual - Deploy & Auto-Update

## Arquitetura de Atualização

```
[Local Machine] --deploy.py--> [VPS] --auto_updater.py--> [Client App]
     📦 Pacote               🖥️ Servidor              ✅ Atualiza automaticamente
```

---

## 📋 Pré-requisitos

### No seu PC (Local):
```bash
pip install requests
```

### No VPS:
```bash
pip install flask requests
```

---

## 🔧 Setup no VPS

### 1. Criar diretório de updates:
```bash
mkdir -p /root/smin_deck_updates
chmod 777 /root/smin_deck_updates
```

### 2. Copiar `vps_update_server.py` para o VPS:
```bash
scp vps_update_server.py root@72.60.244.240:/root/
```

### 3. Iniciar o servidor:
```bash
# SSH no VPS
ssh root@72.60.244.240

# Iniciar servidor (foreground para testes)
python3 /root/vps_update_server.py

# Ou usar PM2 para manter rodando:
pm2 start vps_update_server.py --name "smin-updates"
pm2 save
```

### 4. Verificar se está rodando:
```bash
curl http://72.60.244.240:8000/health
# Deve retornar: {"status": "ok", "service": "Smin-DECK Updates Server"}
```

---

## 📦 Fazer Deploy de Nova Versão

### 1. Atualizar versão local:
Editar `version.json`:
```json
{
  "version": "1.0.1",
  "app_name": "Smin-DECK Virtual",
  "release_date": "14/01/2026",
  "build": "Build 1.0.1 | Beta test"
}
```

### 2. Fazer as mudanças no código:
- Editar arquivos Python (.py)
- Testar localmente

### 3. Fazer deploy:
```bash
# Simples (changelog padrão)
python deploy.py

# Com changelog customizado
python deploy.py "Nova versão com bug fixes e melhorias"
```

### 4. Resultado esperado:
```
🚀 Iniciando deployment...
Versão: 1.0.1
📦 Criando pacote de atualização v1.0.1...
  ✅ deck_window.py
  ✅ bot.py
  ✅ auto_updater.py
  ...
✅ Pacote criado: smin_deck_v1.0.1.zip (45.23 MB)

📤 Fazendo upload para VPS...
✅ Upload concluído!
   URL: http://72.60.244.240:8000/download/smin_deck_v1.0.1.zip

✅ Deployment concluído com sucesso!
💡 Os clientes baixarão a atualização na próxima sincronização
```

---

## ✅ Como Funciona no Cliente

1. **Daemon inicia** ao abrir a aplicação (thread background)
2. **A cada 1 minuto** (configurável) verifica:
   ```
   GET http://72.60.244.240:8000/api/updates/check
   ```
3. **Se versão > local**, faz download:
   ```
   GET http://72.60.244.240:8000/download/smin_deck_vX.X.X.zip
   ```
4. **Extrai** no diretório de work
5. **Atualiza** arquivos Python
6. **Continua executando** sem reiniciar

---

## 🔍 Monitorar Updates no VPS

```bash
# Ver histórico de uploads
curl http://72.60.244.240:8000/api/updates/history

# Ver versão atual
curl http://72.60.244.240:8000/api/updates/check

# Listar arquivos
ls -lh /root/smin_deck_updates/
```

---

## ⚙️ Configurações

### Intervalo de Sincronização
Editar `main.py`, linha com `start_auto_update_daemon`:
- **Desenvolvimento**: 60 segundos (1 minuto)
- **Produção**: 3600 segundos (1 hora)

```python
# Desenvolvimento (testes rápidos)
update_thread = Thread(target=start_auto_update_daemon, args=(60,), daemon=True)

# Produção (sincronização a cada hora)
update_thread = Thread(target=start_auto_update_daemon, args=(3600,), daemon=True)
```

---

## 🐛 Troubleshooting

### Problema: "Connection refused"
```bash
# Verificar se servidor está rodando
curl http://72.60.244.240:8000/health

# Verificar porta 8000
netstat -tlnp | grep 8000
```

### Problema: Upload falha
```bash
# Verificar permissões
ls -la /root/smin_deck_updates/

# Dar permissão
chmod 777 /root/smin_deck_updates
```

### Problema: App não atualiza
```bash
# Verificar arquivo de versão local
cat version.json

# Verificar log do app (console)
# Procurar por "✅ Nova versão disponível" ou "⚠️ Erro ao verificar atualizações"
```

---

## 📝 Checklist de Deploy

- [ ] Atualizar `version.json` com novo número
- [ ] Testar mudanças localmente
- [ ] Executar `python deploy.py "descrição das mudanças"`
- [ ] Verificar upload: `curl http://72.60.244.240:8000/api/updates/history`
- [ ] Esperar 1-2 minutos (ou tempo de sincronização)
- [ ] Verificar se app baixou atualização

---

## 🎯 Próximos Passos

1. ✅ Setup do servidor no VPS
2. ✅ Deploy da primeira versão
3. ⏳ Monitorar em produção
4. ⏳ Coletar feedback de usuários
5. ⏳ Otimizar conforme necessário

