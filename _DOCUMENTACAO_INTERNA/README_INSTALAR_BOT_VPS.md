📖 INSTALAR BOT NO VPS
═════════════════════════════════════════

🎯 OBJETIVO
───────────
Colocar o bot rodando 24/7 no VPS (72.60.244.240) para que:
✅ Cliente autoriza no Discord
✅ Bot (no VPS) detecta automaticamente
✅ Bot cria o canal #smindeck
✅ Cliente usa o SminDeck com integração Discord


📋 PRÉ-REQUISITOS
────────────────
✅ Acesso SSH ao VPS (72.60.244.240)
✅ Arquivo bot.py criado
✅ Token do Discord Bot (ID: 1457841504893538385)


🚀 INSTALAÇÃO - OPÇÃO 1 (AUTOMÁTICA - Recomendado)
──────────────────────────────────────────────────

1. Certifique-se que você está no diretório:
   C:\Users\SAMUEL\Desktop\Smin-DECK virtual

2. Execute o script de deploy:
   python deploy_bot_vps.py

3. O script vai:
   ✅ Enviar bot.py para o VPS
   ✅ Instalar Python e dependências
   ✅ Pedir seu DISCORD_TOKEN
   ✅ Criar arquivo .env
   ✅ Iniciar o bot como serviço permanente

4. Pronto! Bot está online no VPS!


🔧 INSTALAÇÃO - OPÇÃO 2 (MANUAL)
────────────────────────────────

1. Conecte no VPS via SSH:
   ssh root@72.60.244.240

2. Copie o arquivo bot.py para o VPS:
   # No seu computador:
   scp bot.py root@72.60.244.240:/opt/smindeck-bot/

3. No VPS, execute o script:
   bash instalar_bot_vps.sh

4. Coloque seu DISCORD_TOKEN quando pedir

5. Pronto!


📊 VERIFICAR STATUS
───────────────────

Ver se o bot está rodando:
   ssh root@72.60.244.240 "systemctl status smindeck-bot"

Ver logs em tempo real:
   ssh root@72.60.244.240 "journalctl -u smindeck-bot -f"

Parar o bot:
   ssh root@72.60.244.240 "systemctl stop smindeck-bot"

Reiniciar o bot:
   ssh root@72.60.244.240 "systemctl restart smindeck-bot"


🔑 ONDE CONSEGUIR O TOKEN
──────────────────────────

1. Acesse: https://discord.com/developers/applications
2. Clique em sua aplicação
3. Vá em "Bot" (menu à esquerda)
4. Clique em "Copy" embaixo de TOKEN
5. Cole o token no script


✅ FLUXO DO CLIENTE APÓS INSTALAÇÃO
────────────────────────────────────

1. Cliente abre SminDeck.exe
2. Clica em "Conectar com Discord Bot"
3. Clica em "Sim"
4. Navegador abre link de autorização
5. Seleciona o servidor
6. Clica "Autorizar"
7. Bot (no VPS) detecta automaticamente
8. Bot cria o canal #smindeck
9. Bot envia mensagem de boas-vindas
10. Cliente recebe a chave via DM
11. Cliente cola a chave no SminDeck
12. ✅ Integração completa!


⚙️ COMO FUNCIONA
────────────────

O bot roda como serviço systemd no VPS:
✅ Inicia automaticamente quando VPS reinicia
✅ Reinicia automaticamente se cair
✅ Roda 24/7 sem parar
✅ Detecta novos servidores
✅ Cria canais automaticamente


🐛 TROUBLESHOOTING
──────────────────

Se o bot não estiver online:
1. Verifique o token: ssh root@72.60.244.240 "cat /opt/smindeck-bot/.env"
2. Verifique os logs: journalctl -u smindeck-bot -f
3. Reinicie: systemctl restart smindeck-bot

Se o canal não é criado:
1. Verifique permissões do bot no Discord
2. O bot precisa de permissão "manage_channels"
3. Tente comando: /criar-canal

Se há erro "DISCORD_TOKEN not found":
1. Edite o arquivo .env no VPS
2. Adicione: DISCORD_TOKEN=seu_token_aqui
3. Salve e reinicie


📞 SUPORTE
──────────

Comandos úteis do bot:
  /ajuda      - Ver todos os comandos
  /status     - Status do bot
  /info       - Informações do servidor
  /criar-canal - Cria o canal #smindeck


════════════════════════════════════════

✅ Você está pronto! Execute:
   python deploy_bot_vps.py
