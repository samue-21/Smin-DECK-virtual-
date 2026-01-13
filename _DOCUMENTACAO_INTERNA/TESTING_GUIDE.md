# 🧪 Guia de Teste - Configuração Interativa do Token

## Verificação Rápida

### 1. Verificar se os arquivos foram gerados corretamente

```
dist/
✅ SminDeck.exe               - EXE principal
✅ SminDeck-Setup.exe         - Instalador principal  
✅ SminDeckBot-Setup.exe      - Instalador do bot

bot_installer/
✅ setup_token.exe            - Configurador interativo
✅ discord_bot.exe            - Bot Discord
✅ api_server.exe             - Servidor API
✅ start_bot.exe              - Launcher
✅ .env.template              - Template do .env
```

### 2. Testar SminDeckBot-Setup.exe em uma VM ou máquina limpa

```
1. Execute: dist\SminDeckBot-Setup.exe
2. Siga o instalador
3. Em "[Run] section" deve aparecer:
   - "Configurar Token Discord" (deve executar setup_token.exe)
   - "Iniciar o Bot agora"
```

### 3. Testar setup_token.exe diretamente

```
1. Execute: bot_installer\setup_token.exe
2. Deve aparecer uma janela pedindo o token
3. Instruções devem ser claras em português
4. Digite um token de teste (pode ser falso para teste)
5. Arquivo %APPDATA%\SminDeckBot\.env deve ser criado
6. Verificar conteúdo:
   DISCORD_TOKEN=token_que_foi_colado
```

### 4. Testar SminDeck-Setup.exe

```
1. Execute: dist\SminDeck-Setup.exe
2. Escolha "Instalar SminDeck + Bot Discord"
3. Siga as opções de instalação
4. Quando chegar em "Run" deve:
   ✅ Executar setup_token.exe (pedir token)
   ✅ Executar start_bot.exe (iniciar bot)
   ✅ Abrir SminDeck.exe (abertura final)
```

### 5. Verificar variáveis de ambiente

```
Token configurado:
- Arquivo: %APPDATA%\SminDeckBot\.env
- Conteúdo: DISCORD_TOKEN=seu_token_aqui

Banco de dados:
- Arquivo: %APPDATA%\SminDeckBot\smindeck_bot.db
- Contém: Configurações e histórico de comandos
```

## Checklist de Sucesso

- [ ] SminDeck.exe inicia sem erros
- [ ] SminDeckBot-Setup.exe executa sem erros
- [ ] setup_token.exe abre com interface gráfica
- [ ] Mensagens estão em português
- [ ] Token é salvo em %APPDATA%\SminDeckBot\.env
- [ ] Discord bot inicia após token configurado
- [ ] API server inicia após token configurado
- [ ] SminDeck consegue se conectar ao bot

## Troubleshooting

### setup_token.exe não abre
- Verificar se PyInstaller compilou corretamente
- Testar: `make_exe.bat` no SminDeck-Bot-Discord

### Token não é salvo
- Verificar permissões em %APPDATA%\SminDeckBot\
- Verificar se setup_token.py tem permissão de escrita

### Bot não inicia
- Verificar se DISCORD_TOKEN está no .env
- Verificar discord_bot.py para validação de token
- Checar console do start_bot.exe

## Próximos Passos

1. Testar instalação completa em VM Windows limpa
2. Validar fluxo desde token até bot online
3. Testar integração SminDeck ↔ Bot Discord
4. Preparar para distribuição
