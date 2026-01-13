# Plano de Testes de Integração - SminDeck + Bot VPS

**Data**: 01/06/2026  
**Escopo**: Validar integração entre SminDeck (desktop) e Bot Discord (VPS)

---

## 🎯 OBJETIVO

Validar que o SminDeck compilado pode se conectar ao bot Discord em execução na VPS (72.60.244.240) e executar comandos de controle de mídia e background.

---

## 📋 CHECKLIST DE TESTES

### FASE 1: Ambiente VPS ✅ (JÁ TESTADO)
- [x] Bot está online em 72.60.244.240
- [x] Bot conectado ao Discord
- [x] Bot respondendo a comandos
- [x] Sistema de modais funcionando

**Comprovante**: 
- Bot rodando: `/opt/smin-bot/bot_humanizado_interativo.py`
- Status: Active (running)
- Gateway: Connected

---

### FASE 2: Compilação Desktop ✅ (CONCLUÍDO)
- [x] SminDeck.exe compilado com sucesso
- [x] Arquivo de 46.6 MB criado
- [x] Executável rodando sem erros
- [x] Interface PyQt6 carregando

---

### FASE 3: Teste de Integração (EM ANDAMENTO)

#### 3.1: Verificação de Conectividade
```
[ ] Teste 1: Verificar se SminDeck pode acessar 72.60.244.240:8000 (porta padrão)
[ ] Teste 2: Verificar se há firewall bloqueando a conexão
[ ] Teste 3: Testar comunicação HTTP com VPS
```

#### 3.2: Teste de Fluxo de Comando
```
[ ] Teste 4: Usuário insere URL do servidor no SminDeck
[ ] Teste 5: SminDeck envia comando "play" ao bot
[ ] Teste 6: Bot recebe comando e responde
[ ] Teste 7: SminDeck recebe resposta do bot
```

#### 3.3: Teste de Modais Discord
```
[ ] Teste 8: Bot exibe modal de seleção de botão
[ ] Teste 9: Usuário seleciona opção no modal
[ ] Teste 10: Bot processa e confirma seleção
```

#### 3.4: Teste de Mídia
```
[ ] Teste 11: SminDeck envia URL de vídeo
[ ] Teste 12: Bot processa URL e valida
[ ] Teste 13: Mídia é iniciada com sucesso
[ ] Teste 14: Usuário pode pausar/resumir
```

---

### FASE 4: Testes de Carga
```
[ ] Teste 15: Múltiplas instâncias do SminDeck
[ ] Teste 16: Requests simultâneos ao bot VPS
[ ] Teste 17: Uso de memória após 10 minutos
[ ] Teste 18: Shutdown gracioso em caso de erro
```

---

### FASE 5: Testes de Erro
```
[ ] Teste 19: VPS indisponível → erro gracioso no SminDeck
[ ] Teste 20: URL inválida → mensagem de erro clara
[ ] Teste 21: Timeout na conexão → retry automático
[ ] Teste 22: Entrada malformada → validação na interface
```

---

## 🔍 PROCEDIMENTO DE TESTE

### Teste 1-3: Conectividade
```powershell
# Terminal PowerShell
Test-NetConnection -ComputerName 72.60.244.240 -Port 8000
Test-NetConnection -ComputerName 72.60.244.240 -Port 80
curl -Uri "http://72.60.244.240:8000/status" -Method Get
```

### Teste 4-7: Fluxo de Comando
1. Iniciar SminDeck.exe
2. Inserir endereço VPS: `72.60.244.240`
3. Clicar em "Conectar"
4. Verificar se status muda para "Conectado"
5. Executar comando de teste
6. Validar resposta no log

### Teste 8-10: Modais Discord
1. Ter Discord aberto em segundo plano
2. Enviar comando via SminDeck
3. Aguardar aparecimento do modal no Discord
4. Selecionar uma opção
5. Validar confirmação no SminDeck

### Teste 11-14: Mídia
1. Inserir URL de vídeo válida no SminDeck
2. Selecionar modo "reproduzir"
3. Enviar ao bot
4. Verificar se vídeo inicia em background
5. Testar controles (pause, resume, stop)

---

## 📊 MÉTRICAS DE SUCESSO

| Métrica | Alvo | Status |
|---------|------|--------|
| Taxa de sucesso de conexão | 100% | ⏳ |
| Tempo de resposta (cmd→response) | < 2s | ⏳ |
| Memória máxima | < 100 MB | ⏳ |
| Uptime sem erros | 10+ min | ⏳ |
| Taxa de erro | 0% | ⏳ |

---

## 🛠️ FERRAMENTAS NECESSÁRIAS

- SminDeck.exe (compilado) ✅
- Bot Discord em 72.60.244.240 ✅
- Discord client (para testes de modais)
- PowerShell ou cmd para testes de rede
- Task Manager para monitoramento de recursos

---

## 📝 LOG DE TESTES

### Sessão 1 - 01/06/2026

**Horário**: 14:09 - 14:17

**Testes Executados**:
- ✅ SminDeck.exe inicia com sucesso
- ✅ Interface PyQt6 carrega corretamente
- ✅ Memória cresce de 7.88MB (inicial) para 34.75MB (com GUI)
- ✅ Processo encerra sem erros

**Resultado**: **PASSOU** - Build operacional

**Próximos Passos**: Testes de conectividade com VPS

---

## 📞 CONTATOS

- **Bot VPS**: 72.60.244.240
- **Porta Bot**: 8000 (assumido)
- **Discord Server**: [Seu servidor aqui]
- **Token Discord**: [Configurado em VPS]

---

**Status Geral**: 🟡 **EM TESTE** - Build operacional, aguardando testes de integração

