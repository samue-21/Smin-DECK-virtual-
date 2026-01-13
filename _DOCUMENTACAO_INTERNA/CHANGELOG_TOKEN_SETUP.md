# 📝 CHANGELOG - Configuração Interativa do Token

## [1.2] - 2025 - Token Setup Interativo

### ✨ Novo
- **Configurador de Token Interativo** (`setup_token.exe`)
  - Interface gráfica em PyQt6
  - Instruções claras em português
  - Detecta arquivo .env existente
  - Valida formato do token
  
- **Novo Instalador do Bot** com fluxo integrado
  - Pede token automaticamente durante instalação
  - Executa setup_token.exe antes de iniciar bot
  - Salva .env em local correto (%APPDATA%)
  - Mostra mensagem de sucesso ao final

- **Build Pipeline Completo**
  - `make_exe.bat` atualizado
  - Gera 4 EXEs: discord_bot, api_server, start_bot, setup_token
  - PyInstaller com flags --windowed para setup_token
  - Inno Setup compilação automática

### 🐛 Corrigido
- **Permissões de Banco de Dados**
  - Movido de `Program Files` para `%APPDATA%\SminDeckBot`
  - Usuário não-admin agora pode escrever no banco
  - Banco criado automaticamente se não existir

- **Validação de Token**
  - `discord_bot.py` valida token antes de conectar
  - Mensagem clara se token está faltando
  - Instruções de como obter token

- **Inicialização do Bot**
  - `start_bot.exe` não mostra console
  - Inicia discord_bot.exe e api_server.exe em background
  - Mensagem amigável "Ativando seu bot Discord, aguarde..."

### 📦 Empacotamento
- Novo `SminDeckBot-Setup.exe` com setup_token integrado
- Atualizado `SminDeck-Setup.exe` com bot component
- Bot installer em `dist\` para fácil acesso
- Arquivos de template (.env.template) para referência

### 📚 Documentação
- `SETUP_TOKEN_SUMMARY.md` - Resumo técnico
- `INSTALLATION_GUIDE.md` - Guia para cliente final
- `TESTING_GUIDE.md` - Checklist de testes
- `README.md` atualizado em bot com instruções token

### 🔄 Fluxo de Instalação
```
SminDeck-Setup.exe
    ↓
[Marcar "Bot Discord"]
    ↓
SminDeckBot-Setup.exe
    ↓
setup_token.exe [INTERATIVO - pede token]
    ↓
Salva .env automaticamente
    ↓
Inicia bot (discord_bot.exe + api_server.exe)
    ↓
SminDeck pronto!
```

### 🎯 Resultado Final
**Cliente NÃO precisa mais:**
- Editar arquivo .env manualmente
- Entender onde tokens vão
- Lidar com variáveis de ambiente
- Executar scripts

**Cliente APENAS:**
- Executa SminDeck-Setup.exe
- Marca "Bot Discord"
- Segue prompt interativo
- Pronto!

## Detalhes Técnicos

### Arquivos Modificados
- `setup_token.py` (NEW) - Configurador interativo
- `discord_bot.py` - Adicionada validação de token
- `make_exe.bat` - Step [6/6] para setup_token.exe
- `installer\SminDeckBot.iss` - Integração do setup_token
- `deck_window.py` - Referências ao novo instalador
- `installer.iss` - Atualizado para integrar bot

### Arquivos Criados
- `SminDeckBot-Setup.exe` - Novo instalador do bot
- `setup_token.exe` - Configurador de token
- `SminDeck-Setup.exe` - Atualizado com bot integrado
- `.env.template` - Template de configuração

### Dependências Adicionadas
- PyQt6 (já está no requirements do bot)
- pathlib (built-in)
- python-dotenv (já estava)

## Versão Anterior (1.1) Tinha

- Bot Discord funcionando
- Database em AppData (corrigido em 1.1)
- API Server funcionando
- YouTube fullscreen
- Token validation básico

## Próximas Versões

### Planejado para 1.3
- [ ] Suporte a múltiplos bots (tokens diferentes)
- [ ] Atualização automática de token
- [ ] Recovery de token perdido
- [ ] Dashboard web do bot

### Considerações Futuras
- Autenticação OAuth2 no Discord
- Sincronização em nuvem
- Interface web para gerenciamento remoto

---

**Desenvolvido com ❤️ para melhor experiência do usuário**
