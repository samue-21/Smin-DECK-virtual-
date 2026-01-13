#!/usr/bin/env python3
"""
INSTRUÇÕES PARA TESTE REAL COM BOT DISCORD
"""

print("""
╔══════════════════════════════════════════════════════════════════╗
║              🎯 TESTE REAL - BOT DISCORD + APP                  ║
╚══════════════════════════════════════════════════════════════════╝

✅ PRÉ-REQUISITOS:
   □ Bot Discord online e conectado
   □ API rodando na VPS (porta 5001)
   □ APP pronto com database_client integrado
   □ Database.py sincronizado em ambos

📋 PASSOS DO TESTE:

PASSO 1️⃣ - GERAR CHAVE NO BOT
═══════════════════════════════════════════════════════════════════
1. Abra Discord e acesse o servidor do bot
2. No canal #smindeck, envie: "oi"
3. ✅ Bot vai responder com chave de 8 caracteres
   Ex: K5O66FHQ
4. COPIE ESTA CHAVE (você vai precisar)

⏱️ Timeout: Chave expira em 5 minutos


PASSO 2️⃣ - INICIAR APP SMINDECK
═══════════════════════════════════════════════════════════════════
1. Execute: python main.py
2. ✅ Você vai ver:
   - Tela "Atualizando seu app..."
   - Barra de progresso
   - "Conectando ao banco remoto..."
   - "Processando atualizações..."
   - "Sincronização concluída!"
3. APP vai abrir normalmente


PASSO 3️⃣ - CONECTAR COM CHAVE DO BOT
═══════════════════════════════════════════════════════════════════
1. No APP, clique no botão "🤖 BOT" (canto inferior)
2. Clique em "Tenho chave"
3. Cole a chave que copiou do Discord
4. ✅ Você vai ver:
   - "🔍 Validando chave..."
   - "🔐 Conectando com bot..."
   - "✓ Conectado!"
5. Diálogo vai fechar


PASSO 4️⃣ - BOT VAI RESPONDER AUTOMATICAMENTE
═══════════════════════════════════════════════════════════════════
1. Volte ao Discord
2. ✅ Bot DEVE enviar:
   - "✅ SUCESSO!" 
   - "Sua autenticação foi confirmada!"
   - Menu com 4 opções:
     🔗 Atualizar Link
     🎥 Atualizar Vídeo
     🖼️ Atualizar Imagem
     📁 Menu de Conteúdo
3. ✨ Se não receber, verifique logs da VPS:
   ssh root@72.60.244.240
   cd /opt/smindeck-bot
   tail -f api_server.log


PASSO 5️⃣ - INTERAGIR COM MENU
═══════════════════════════════════════════════════════════════════
1. No menu do Discord, clique em "🔗 Atualizar Link"
2. ✅ Bot vai pedir:
   "Em qual botão você deseja atualizar?"
3. Clique em qualquer botão (ex: "Botão 1")
4. ✅ Bot vai pedir:
   "Envie o link para o Botão 1:"
5. Envie uma URL qualquer: https://example.com
6. ✅ Bot deve responder:
   "✅ SUCESSO!"
   "Seus dados foram atualizados no Botão 1!"
   "Tudo pronto! ✨"


╔══════════════════════════════════════════════════════════════════╗
║                    ✨ CHECKLIST DE SUCESSO                      ║
╚══════════════════════════════════════════════════════════════════╝

□ APP inicia com tela de sincronização
□ Barra de progresso atualiza (Conectando... → Processando... → Concluído)
□ APP abre sem erros
□ Botão "🤖 BOT" está funcional
□ Dialog "Tenho chave" aparece
□ Chave é validada com sucesso
□ Bot responde com menu no Discord
□ Menu tem 4 botões funcionais
□ Clicando em um botão, bot pede dados
□ Enviando dados, bot confirma sucesso
□ Novo menu aparece automaticamente


╔══════════════════════════════════════════════════════════════════╗
║                   🔍 TROUBLESHOOTING                            ║
╚══════════════════════════════════════════════════════════════════╝

❌ APP não abre:
   → Verifique se API está online: curl http://72.60.244.240:5001/api/health
   → Verifique erro na tela de sincronização

❌ Chave inválida no APP:
   → Verifique se copiou corretamente
   → Verifique se não expirou (5 minutos)
   → Solicite nova chave ao bot

❌ Bot não responde após autenticação:
   → Verifique bot está online: systemctl status smindeck-bot
   → Verifique API: curl http://72.60.244.240:5001/api/health
   → Verifique logs: tail -100 /opt/smindeck-bot/api_server.log

❌ Menu não aparece:
   → Verifique channel_id está correto
   → Verifique bot tem permissão de enviar mensagens
   → Verifique guild_id está correto

❌ Dados não são salvos:
   → Verifique banco: sqlite3 ~/.smindeckbot/smindeckbot.db
   → Execute: SELECT * FROM chaves_ativas; SELECT * FROM atualizacoes;


════════════════════════════════════════════════════════════════════
             📝 PRÓXIMA ETAPA: Implementar sincronização
             de updates do Discord para o APP via polling
════════════════════════════════════════════════════════════════════
""")

input("\n👉 Pressione ENTER para começar o teste...")
