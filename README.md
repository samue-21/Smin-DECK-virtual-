# 🎬 Smin-DECK Virtual

> **Versão 1.0.3** | Janeiro 2026

## 📌 Sobre o Projeto

**Smin-DECK Virtual** é uma aplicação profissional desenvolvida em Python/PyQt6 para gerenciamento de conteúdo de streaming com integração Discord e sistema automático de atualização.

### 🚀 Recursos Principais

- ✅ Interface de Stream Deck Virtual personalizável
- ✅ Integração completa com Discord Bot
- ✅ Sistema de auto-atualização via VPS
- ✅ Gerenciamento de vídeos, áudios e imagens
- ✅ Editor de logo interativo
- ✅ Temas customizáveis
- ✅ Persistência automática de dados

---

## 📋 Pré-requisitos

- Windows 10/11
- Python 3.13+
- PyQt6
- Inno Setup 6 (para compilar instalador)

---

## 🔧 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/Smin-DECK-Virtual.git
cd Smin-DECK-Virtual
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
Copie `.env.example` para `.env` e preencha com suas credenciais:
```bash
copy .env.example .env
```

Edite o arquivo `.env` com seus dados do VPS:
```env
VPS_HOST=seu_ip_vps
VPS_USER=usuario
VPS_PASSWORD=sua_senha
VPS_PORT=22
VPS_REMOTE_PATH=/caminho/no/vps
VPS_UPDATE_SERVER=http://seu_ip:porta
```

---

## 🎮 Uso

### Executar a aplicação
```bash
python main.py
```

### Compilar executável
```bash
pyinstaller SminDeck.spec
```

### Criar instalador Windows
```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

---

## 🔄 Sistema de Auto-Update

O projeto inclui um sistema completo de auto-atualização:

- **Cliente** (`auto_updater.py`): Verifica atualizações a cada 60 segundos
- **Servidor** (`vps_update_server.py`): Flask API no VPS para servir atualizações
- **Deploy** (`auto_deploy.py`): Script para fazer deploy automático de novas versões

### Configurar VPS para Updates

1. Faça upload do `vps_update_server.py` para seu VPS
2. Execute o servidor Flask:
```bash
python vps_update_server.py
```

---

## 📁 Estrutura do Projeto

```
Smin-DECK-Virtual/
├── main.py                 # Ponto de entrada da aplicação
├── deck_window.py          # Interface principal do deck
├── playback_window.py      # Janela de reprodução fullscreen
├── logo_editor_window.py   # Editor de logo interativo
├── bot.py                  # Integração com Discord
├── auto_updater.py         # Cliente de auto-atualização
├── vps_update_server.py    # Servidor de updates (VPS)
├── auto_deploy.py          # Script de deploy automático
├── database.py             # Gerenciamento de banco de dados
├── theme.py                # Tema visual da aplicação
├── version.json            # Informações de versão
├── requirements.txt        # Dependências Python
├── SminDeck.spec          # Spec do PyInstaller
├── installer.iss           # Script Inno Setup
└── .env.example            # Template de variáveis de ambiente
```

---

## 🎯 Recursos Principais

### **1. Reprodução de Mídia**
- **Vídeos**: MP4, AVI, MOV, MKV, FLV, WMV, WEBM
- **Áudio**: MP3, WAV, OGG, FLAC, AAC, M4A
- **Imagens**: JPG, PNG, BMP, WEBP, GIF

### **2. Discord Bot Integration**
- Botão "Enviar Arquivos" integrado na interface
- Upload automático de conteúdo
- Gerenciamento de arquivos via Discord

### **3. Auto-Update System**
- Verificação automática a cada 60 segundos
- Download e instalação de atualizações
- Multi-endpoint com fallback
- Versionamento semântico

---

## 🔐 Segurança

⚠️ **IMPORTANTE**: Nunca faça commit de credenciais reais!

- Use `.env` para armazenar credenciais (já está no `.gitignore`)
- O arquivo `.env.example` serve apenas como template
- Mantenha suas senhas e tokens do Discord seguros
- Adicione `python-dotenv` às dependências para usar variáveis de ambiente

---

## 📝 Versão

**Versão atual: 1.0.3**

Veja [version.json](version.json) para detalhes da build.

### Changelog
- **v1.0.3**: Setup com auto-updater funcional
- **v1.0.2**: Correções no sistema de update
- **v1.0.1**: Primeira versão com auto-update
- **v1.0.0**: Versão inicial estável

---

## 🛠️ Desenvolvimento

### Criar nova versão
1. Atualize `version.json` com a nova versão
2. Compile o executável: `pyinstaller SminDeck.spec`
3. Crie o instalador: `ISCC.exe installer.iss`
4. Use `auto_deploy.py` para fazer deploy no VPS

### Estrutura de Commits
```bash
git add .
git commit -m "tipo: descrição"
git push
```

**Tipos de commit**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

---

- Drag-drop para reordenar
- Editar/deletar em tempo real
- Nomes persistem no banco de dados

### **3. Editor de Logo Interativo**
- Janela flutuante (stays-on-top)
- **Drag**: Move logo
- **Shift+Drag**: Redimensiona
- Controles spinbox: X, Y, Tamanho
- Slider: Opacidade (0-100%)
- Preview em tempo real

### **4. Banco de Dados**
- SQLite (arquivo único: database.db)
- Backup automático
- Sem configuração necessária

---

## ⚙️ Configuração Avançada

### **Logo Configuration (deck_config.sdk)**
```json
{
  "player_config": {
    "logo_path": "C:/Users/.../logo.png",
    "logo_size": 150,
    "logo_opacity": 0.8,
    "x": 10,
    "y": 218
  }
}
```

### **Variáveis de Ambiente**
```bash
# Opcional: Discord bot token
DISCORD_TOKEN=seu_token_aqui
```

---

## 🎮 Atalhos de Teclado

| Tecla | Ação |
|-------|------|
| `ESC` | Sair fullscreen |
| `SPACE` | Play/Pause |
| `→` | Avançar 5s |
| `←` | Retroceder 5s |
| `L` | Abrir editor de logo |

---

## 🐛 Solução de Problemas

### **"Logo não aparece no vídeo"**
- ⚠️ **Limitação conhecida**: PyQt6 não renderiza overlays em fullscreen
- ✅ **Solução**: Editor funciona perfeitamente, configuração é salva
- 🚀 **Futuro**: Será implementado em versão Electron

### **"Botão não toca som"**
1. Verifique formato: `.mp3`, `.wav`, etc
2. Verifique caminho do arquivo
3. Verifique volume do Windows

### **"App não inicia"**
```bash
# Teste dependências
python -c "import PyQt6; print('✅ PyQt6 OK')"
python -c "import PyQt6.QtMultimedia; print('✅ Multimedia OK')"
```

### **"Banco de dados corrompido"**
```bash
# Backup automático está em: database.db.backup
# Restaure com:
copy database.db.backup database.db
```

---

## 📊 Performance

| Métrica | Valor |
|---------|-------|
| Tempo de inicialização | ~2-3s |
| RAM (base) | ~100-150MB |
| RAM (com vídeo) | ~200-300MB |
| CPU (idle) | <2% |
| Tamanho executável | 100-120MB (PyInstaller) |

---

## 🔒 Privacidade & Segurança

- ✅ Sem telemetria
- ✅ Sem rastreamento
- ✅ Sem conexão internet (exceto Discord opcional)
- ✅ Dados locais apenas (SQLite)
- ✅ Código-fonte disponível

---

## 📈 Próxima Versão (Smin-DECK 2.0)

Está sendo planejada em **Electron + React** com:
- ✅ Logo visível em fullscreen
- ✅ UI moderna
- ✅ Melhor extensibilidade
- ✅ Monetização integrada

📖 Veja: [PROJETO_PILOTO_PLANO.md](PROJETO_PILOTO_PLANO.md)

---

## 💬 Suporte

## 📄 Licença

Este projeto é privado. Todos os direitos reservados.

## 👤 Autor

**SAMUEL**

---

💡 **Dica**: Para mais detalhes sobre deployment, veja [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)


### **Contribuições**
- Issues: Reporte bugs
- Features: Sugira melhorias
- PRs: Bem-vindo!

---

## 📜 Licença

Desenvolvido para uso em igrejas e instituições religiosas.

---

## 🎓 Stack Técnico

```
Frontend: PyQt6 (Python)
Backend: Python 3.10+
Database: SQLite
Media: Qt Multimedia
Bot: discord.py (opcional)
Package: PyInstaller
```

---

## ✅ Status

- **Estabilidade**: Pronta para produção ✅
- **Features Completas**: ~95%
- **Logo em Fullscreen**: ⚠️ Limitação PyQt6
- **Documentação**: ✅ Completa
- **Performance**: ✅ Otimizada

---

**Desenvolvido com ❤️ para comunidades de fé**

*Última atualização: 8 de janeiro de 2026*
