# ✅ CHECKLIST DE TESTE: Auto-Renomear Botões

## 🚀 ANTES DE COMEÇAR

- [ ] Bot rodando na VPS (verificar: `/opt/smindeck-bot`)
- [ ] API respondendo (verificar: `curl http://72.60.244.240:5001/api/health`)
- [ ] APP sincronizador.py e deck_window.py atualizados
- [ ] Chave de autenticação gerada e validada no APP

---

## 🧪 TESTE 1: Registrar Arquivo com Nome Customizado

### Pré-requisitos
- [ ] Bot conectado e respondendo
- [ ] Usuario autenticado no Discord com SminDeck

### Passos
1. [ ] No Discord, envie: `/oi`
2. [ ] Bot responde com menu de 4 opções
3. [ ] Clique em: "🎥 Atualizar Vídeo"
4. [ ] Bot pergunta: "Em qual botão você deseja atualizar?"
5. [ ] Escolha: "Botão 7"
6. [ ] Bot pergunta: "Envie o link para o Botão 7:"
7. [ ] Envie um link de vídeo (ex: YouTube, Google Drive, Direct URL)
8. [ ] Bot pergunta: "Digite o nome customizado" (ou automático se vazio)
9. [ ] Responda: "primicias-de-fe" (sem caracteres especiais)
10. [ ] Bot responde: "✅ PRONTO!" com informações do arquivo

### Esperado
- ✅ Bot mostra tamanho do arquivo baixado (MB)
- ✅ Status: "Sincronizado!" 
- ✅ Sem erros

---

## 🧪 TESTE 2: Verificar Dados no Banco de Dados

### Acesso ao VPS
```bash
ssh root@72.60.244.240
cd /root/.smindeckbot
sqlite3 smindeckbot.db
```

### Verificar Registros
```sql
SELECT 
    botao,
    tipo,
    dados,
    timestamp
FROM atualizacoes 
WHERE botao = 7
ORDER BY timestamp DESC 
LIMIT 1;
```

### Esperado
```
| botao | tipo  | dados                                                  | timestamp |
|-------|-------|--------------------------------------------------------|-----------|
| 7     | video | {"arquivo": "video_botao_7.bin", "nome": "primicias-de-fe"} | 2025-01-07 21:46:XX |
```

### Validação
- [ ] Campo `arquivo` contém nome padronizado (video_botao_7.bin)
- [ ] Campo `nome` contém nome customizado (primicias-de-fe)
- [ ] Ambos os campos presentes no JSON
- [ ] Timestamp recente (últimos minutos)

---

## 🧪 TESTE 3: Sincronização no APP

### Preparação
- [ ] APP está aberto
- [ ] APP conectado à VPS (verificar status)
- [ ] Chave de autenticação validada

### Verificar Sincronização
1. [ ] Abrir APP
2. [ ] Aguardar 5 segundos (ciclo de sincronização)
3. [ ] Verificar logs do APP (deve mostrar "Atualização(ões) encontrada(s)")
4. [ ] Verificar se botão 7 mostra: "primicias-de-fe"

### Esperado nos Logs
```
⏰ 1 atualização(ões) encontrada(s)! Aplicando na memória...
📝 Atualização Botão 7 (índice 6): video
   🔹 Arquivo: video_botao_7.bin
   🔹 Nome botão: primicias-de-fe
📥 Baixando arquivo do VPS: video_botao_7.bin
✅ Download concluído: /home/user/.smindeckbot/downloads/video_botao_7.mp4
✅ Botão 7: primicias-de-fe (arquivo: video_botao_7.mp4...)
```

### Validação
- [ ] Arquivo baixado com sucesso (HTTP 200)
- [ ] Tamanho do arquivo correto (não 2.4KB!)
- [ ] Botão exibe nome customizado: "primicias-de-fe"
- [ ] Nenhum erro 404

---

## 🧪 TESTE 4: Verificar Arquivo Deletado

### Após Download no APP
1. [ ] Verificar se arquivo foi deletado do VPS

```bash
ls -lah /opt/smindeck-bot/uploads/ | grep video_botao_7
```

### Esperado
- [ ] Arquivo NÃO aparece na listagem (foi deletado)
- [ ] Espaço liberado no servidor

### Se arquivo ainda estiver lá
```bash
# Verificar logs da API
tail -f /opt/smindeck-bot/api_server.log | grep "DELETE"
```

---

## 🧪 TESTE 5: Persistência do Nome

### Teste de Reinício
1. [ ] Feche o APP completamente
2. [ ] Aguarde 10 segundos
3. [ ] Reabra o APP
4. [ ] Verifique se botão 7 ainda exibe: "primicias-de-fe"

### Esperado
- [ ] Nome persiste após reinício
- [ ] Arquivo continua sincronizado

### Se não persistir
```bash
# Verificar arquivo de configuração
cat ~/.smindeckbot/deck_config.json | grep -A 20 "botao_7"
```

---

## 🧪 TESTE 6: Múltiplos Botões

### Teste com Diferentes Tipos

#### Botão 1: Link
1. [ ] Enviar: `/atualizar_link`
2. [ ] Botão: 1
3. [ ] Link: https://google.com
4. [ ] Nome: "Google"
5. [ ] Verificar APP: Botão exibe "Google"

#### Botão 2: Imagem  
1. [ ] Enviar: `/atualizar_imagem`
2. [ ] Botão: 2
3. [ ] Link: [URL de imagem PNG/JPG]
4. [ ] Nome: "Galeria"
5. [ ] Verificar APP: Botão exibe "Galeria"

#### Botão 3: Vídeo
1. [ ] Enviar: `/atualizar_video`
2. [ ] Botão: 3
3. [ ] Link: [URL de vídeo MP4]
4. [ ] Nome: "Aula de Hoje"
5. [ ] Verificar APP: Botão exibe "Aula de Hoje"

### Esperado
- [ ] Todos os 3 botões exibem nomes customizados
- [ ] Todos sincronizam corretamente
- [ ] Nenhum erro

---

## 🧪 TESTE 7: Compatibilidade com Dados Antigos

### Simular Dado Antigo (Opcional)

No banco de dados, inserir um registro com formato antigo:
```sql
INSERT INTO atualizacoes (chave, tipo, botao, dados)
VALUES ('XXXX1234', 'link', 5, '{"conteudo": "https://example.com"}');
```

### Verificar APP
1. [ ] APP sincroniza
2. [ ] Botão 5 mostra: "https://example.com"
3. [ ] Sem erro, funciona normalmente

### Esperado
- [ ] Dados antigos continuam funcionando
- [ ] Retro-compatibilidade ✅

---

## ❌ TROUBLESHOOTING

### Problema: "Botão não atualiza com nome customizado"
**Possíveis Causas:**
- [ ] APP não está sincronizando (verificar conexão VPS)
- [ ] Banco não tem o novo formato (verificar SQL)
- [ ] APP não recebeu atualização de code

**Solução:**
1. Verificar logs do APP: `python main.py` (no terminal)
2. Verificar API: `curl http://72.60.244.240:5001/api/atualizacoes`
3. Verificar banco: `sqlite3 /root/.smindeckbot/smindeckbot.db`

---

### Problema: "HTTP 404 ao baixar arquivo"
**Possíveis Causas:**
- [ ] Arquivo não existe no VPS (`/opt/smindeck-bot/uploads/`)
- [ ] Nome do arquivo errado na API
- [ ] API retornando nome customizado ao invés do real

**Solução:**
1. Verificar arquivo existe: `ls -la /opt/smindeck-bot/uploads/video_botao_7.bin`
2. Verificar logs API: `tail -f /opt/smindeck-bot/api_server.log`
3. Verificar banco: `SELECT dados FROM atualizacoes WHERE botao = 7`

---

### Problema: "Arquivo não é deletado do VPS"
**Possíveis Causas:**
- [ ] APP não tem permissão DELETE
- [ ] API não implementou DELETE endpoint
- [ ] Arquivo não foi baixado com sucesso

**Solução:**
1. Verificar permissões: `chmod 755 /opt/smindeck-bot/uploads/`
2. Verificar API code: `grep -n "DELETE" /opt/smindeck-bot/api_server.py`
3. Verificar logs: `tail -f /opt/smindeck-bot/api_server.log`

---

## ✅ SUCESSO!

Se TODOS os testes passaram:

```
✅ TESTE 1: Registrar com nome customizado
✅ TESTE 2: Banco contém ambos os campos
✅ TESTE 3: APP sincroniza e botão atualiza
✅ TESTE 4: Arquivo deletado do VPS
✅ TESTE 5: Nome persiste após reinício
✅ TESTE 6: Múltiplos botões funcionam
✅ TESTE 7: Compatibilidade com dados antigos
```

**🎉 SISTEMA FUNCIONANDO PERFEITAMENTE! 🎉**

---

## 📊 Relatório de Teste

**Data de Teste:** ________________
**Tester:** ________________
**Tempo Total:** ________________

| Teste | Status | Observações |
|-------|--------|-------------|
| Registrar com Nome | ✅ / ❌ | |
| Banco de Dados | ✅ / ❌ | |
| Sincronização APP | ✅ / ❌ | |
| Arquivo Deletado | ✅ / ❌ | |
| Persistência | ✅ / ❌ | |
| Múltiplos Botões | ✅ / ❌ | |
| Compatibilidade | ✅ / ❌ | |

**Status Geral:** ✅ PASSOU / ⚠️ PARCIAL / ❌ FALHOU

**Comentários:**
```


```

---

## 📞 Contato

Se encontrar problemas fora deste checklist, recolha:
1. Logs do APP
2. Logs do VPS (bot.log, api_server.log)
3. Query do banco de dados
4. Prints de tela do erro
5. Hora exata que o erro ocorreu
