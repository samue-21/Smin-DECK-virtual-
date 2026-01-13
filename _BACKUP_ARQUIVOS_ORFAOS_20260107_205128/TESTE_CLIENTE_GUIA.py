#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 GUIA DE TESTE - CLIENTE SMINDECK
Siga os passos para testar todo o fluxo
"""

print("""
╔════════════════════════════════════════════════════════════════════╗
║                   🎯 TESTE COMO CLIENTE                           ║
║                                                                    ║
║         Sistema de Banco Centralizado - SminDeck                  ║
╚════════════════════════════════════════════════════════════════════╝


📝 PRÉ-REQUISITOS CHECADOS:
════════════════════════════════════════════════════════════════════

✅ Banco de dados local: LIMPO (vazio)
✅ Bot Discord: ONLINE (em 72.60.244.240:5001)
✅ API REST: RESPONDENDO (http://72.60.244.240:5001/api/health)
✅ APP: RODANDO (em sua máquina local)


🎮 PASSO 1: ABRIR DISCORD
════════════════════════════════════════════════════════════════════

1. Abra Discord
2. Vá para o servidor do SminDeck Bot
3. Acesse o canal #smindeck (ou qualquer canal onde o bot está)


🔐 PASSO 2: GERAR CHAVE NO BOT
════════════════════════════════════════════════════════════════════

1. No Discord, envie: "oi"
2. ✅ Bot vai responder com uma mensagem
3. Copie a CHAVE (8 caracteres em MAIÚSCULAS)

   Exemplo de chave: ABCD1234

   ⏰ Timeout: A chave expira em 5 minutos


🔑 PASSO 3: CONECTAR CHAVE NO APP
════════════════════════════════════════════════════════════════════

1. No APP SminDeck que está rodando:
   └─ Clique no botão "🤖 BOT" (canto inferior)

2. Clique em "Tenho chave"
   └─ Vai abrir um dialog para inserir a chave

3. Cole a chave que copiou do Discord
   └─ Exemplo: ABCD1234

4. Aguarde:
   ├─ "🔍 Validando chave..." (amarelo)
   ├─ "🔐 Conectando com bot..." (amarelo)
   ├─ "✓ Conectado!" (verde)
   └─> Dialog fecha automaticamente


✨ PASSO 4: VERIFICAR BOT NO DISCORD
════════════════════════════════════════════════════════════════════

Volte ao Discord e verifique:

✅ Bot enviou:
   ├─ "✅ SUCESSO!"
   ├─ "Sua autenticação foi confirmada!"
   └─ Menu com 4 botões:
      ├─ 🔗 Atualizar Link
      ├─ 🎥 Atualizar Vídeo
      ├─ 🖼️ Atualizar Imagem
      └─ 📁 Menu de Conteúdo


🎨 PASSO 5: FAZER PRIMEIRA ATUALIZAÇÃO
════════════════════════════════════════════════════════════════════

1. No menu do Discord, clique em: "🔗 Atualizar Link"

2. Bot vai pedir:
   └─ "Em qual botão você deseja atualizar?"

3. Clique em: "Botão 1"

4. Bot vai pedir:
   └─ "Envie o link para o Botão 1:"

5. Você envia qualquer link, exemplo:
   └─ "https://example.com"

6. ✅ Bot confirma:
   ├─ "✅ SUCESSO!"
   ├─ "Seus dados foram atualizados no Botão 1!"
   └─ "Tudo pronto! ✨"


📊 PASSO 6: SINCRONIZAR NO APP
════════════════════════════════════════════════════════════════════

1. Volte ao APP SminDeck

2. FECHE e ABRA novamente:
   ├─ Ctrl+Q (ou fechar a janela)
   └─ python main.py (ou clique para abrir novamente)

3. ✅ Deve aparecer LOADING DIALOG:
   ├─ "Atualizando seu app..."
   ├─ [████████░░░░░░░░░░░] Barra de progresso
   ├─ "Conectando ao banco remoto..." (10%)
   ├─ "Processando atualizações..." (50%)
   └─ "✓ Sincronização concluída!" (100%)

4. 🎉 APP abre com dados sincronizados
   └─ Botão 1 agora contém: https://example.com


🔄 PASSO 7: FAZER MAIS ATUALIZAÇÕES
════════════════════════════════════════════════════════════════════

Repita os PASSOS 5-6 para cada tipo:

1. Atualizar Vídeo:
   ├─ Escolha um botão (ex: Botão 2)
   ├─ Envie um link de vídeo
   └─ Sincronize no APP

2. Atualizar Imagem:
   ├─ Escolha um botão (ex: Botão 3)
   ├─ Envie um link de imagem
   └─ Sincronize no APP

3. Menu de Conteúdo:
   ├─ Escolha um botão
   ├─ Envie dados personalizados
   └─ Sincronize no APP


✅ CHECKLIST DE SUCESSO
════════════════════════════════════════════════════════════════════

Marque conforme avança:

□ Gerei chave no Discord (/oi)
□ Copiei corretamente a chave
□ Colei a chave no APP
□ APP conectou com sucesso
□ Bot enviou confirmação no Discord
□ Bot mostrou menu com 4 opções
□ Enviei primeira atualização (link)
□ Bot confirmou atualização
□ Fechei e reabrui APP
□ Loading Dialog apareceu
□ APP sincronizou dados
□ Botão 1 tem os dados da primeira atualização
□ Fiz mais atualizações nos outros botões
□ Todas as sincronizações funcionaram


🐛 TROUBLESHOOTING
════════════════════════════════════════════════════════════════════

❌ "API offline"
   └─> Verifique se VPS está rodando:
       curl http://72.60.244.240:5001/api/health

❌ "Chave inválida"
   └─> Copie novamente (exatamente como o bot mostrou)
   └─> Verifique se não expirou (5 min)

❌ "Bot não responde após autenticação"
   └─> Verifique logs do bot:
       ssh root@72.60.244.240
       tail -100 /opt/smindeck-bot/api_server.log

❌ "Loading não aparece ao abrir APP"
   └─> Normal! Só aparece se há atualizações pendentes
   └─> Faça uma atualização no Discord primeiro

❌ "Dados não sincronizam"
   └─> Feche e abra APP novamente
   └─> Verifique conexão com internet


📊 O QUE ESTÁ SENDO TESTADO
════════════════════════════════════════════════════════════════════

FLUXO COMPLETO:
  1. ✓ Geração de chaves no bot (5 min timeout)
  2. ✓ Validação de chaves via API
  3. ✓ Autenticação no banco de dados
  4. ✓ Registro de atualizações
  5. ✓ Loading dialog condicional
  6. ✓ Sincronização incremental
  7. ✓ Persistência de dados

TECNOLOGIAS:
  • Discord.py (Bot)
  • SQLite (Banco)
  • HTTP REST (API)
  • PyQt6 (UI)


════════════════════════════════════════════════════════════════════

💡 DICA: Se tudo funcionar, parabéns! 🎉

O sistema está pronto para PRODUÇÃO!

════════════════════════════════════════════════════════════════════
""")

input("\n👉 Pressione ENTER quando quiser começar...")
