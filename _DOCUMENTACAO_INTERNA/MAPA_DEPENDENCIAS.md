# 📋 MAPA DE DEPENDÊNCIAS - SMIN-DECK

**Status:** ✅ Gerado após limpeza  
**Arquivos Analisados:** 24 Python files  
**Data:** 7 de janeiro de 2026

---

## 🎯 ENTRYPOINTS PRINCIPAIS

### 1️⃣ Aplicação Desktop
```
main.py (ENTRADA)
    ↓
    ├─→ deck_window.py (Janela principal)
    │   ├─→ background_controller.py
    │   ├─→ loading_dialog.py
    │   ├─→ playback_window.py
    │   ├─→ app_paths.py
    │   └─→ theme.py
    │
    ├─→ theme.py (Estilos)
    ├─→ beta_warning.py (Dialog)
    └─→ background_controller.py (Threads)
```

### 2️⃣ Bot Discord (VPS)
```
bot.py (ENTRADA)
    ↓
    ├─→ bot_humanizado.py (Cog - Personalidade)
    ├─→ bot_connector.py (Conector)
    ├─→ bot_key_ui.py (UI Chaves)
    ├─→ bot_file_sync.py (Sincronização)
    ├─→ database.py (BD SQLite)
    ├─→ download_manager.py (Downloads)
    └─→ vps_config.py (Configuração)
```

### 3️⃣ API Server (VPS)
```
api_server.py (ENTRADA)
    ↓
    ├─→ database.py (BD)
    ├─→ database_client.py (Cliente BD Remoto)
    ├─→ download_manager.py (Downloads)
    ├─→ sincronizador.py (Sincronização)
    ├─→ arquivo_processor.py (Processamento)
    └─→ vps_config.py (Configuração)
```

---

## 📦 AGRUPAMENTO POR FUNCIONALIDADE

### 🎨 Apresentação (UI/Frontend)
```
deck_window.py
├── Imports internos:
│   ├── background_controller.py
│   ├── loading_dialog.py
│   ├── playback_window.py
│   ├── app_paths.py
│   └── theme.py
│
├── Imports externos:
│   ├── PyQt6 (UI Framework)
│   ├── PIL (Imagens)
│   ├── requests (HTTP)
│   └── webbrowser (Links)
```

### 🤖 Lógica de Bot
```
bot.py
├── Imports internos:
│   ├── database.py
│   ├── download_manager.py
│   └── bot_humanizado.py
│
├── Imports externos:
│   ├── discord (Bot Framework)
│   ├── aiohttp (HTTP Assíncrono)
│   └── logging (Logs)
```

### 🗄️ Dados (Database)
```
database.py
├── Imports internos:
│   └── (Nenhum - Module base)
│
└── Imports externos:
    ├── sqlite3 (BD)
    └── json (Serialização)

database_client.py
├── Imports internos:
│   └── vps_config.py
│
└── Imports externos:
    ├── requests (HTTP)
    ├── paramiko (SSH)
    └── sqlite3 (BD Local)
```

### 📥 Download/Sincronização
```
download_manager.py
├── Imports internos:
│   └── (Nenhum - Module base)
│
└── Imports externos:
    ├── aiohttp (Async HTTP)
    ├── requests (HTTP)
    └── pathlib (Arquivos)

sincronizador.py
├── Imports internos:
│   ├── database_client.py
│   └── app_paths.py
│
└── Imports externos:
    ├── requests (HTTP)
    └── pathlib (Arquivos)

arquivo_processor.py
├── Imports internos:
│   └── (Nenhum - Module base)
│
└── Imports externos:
    ├── pathlib
    ├── json
    └── PIL
```

### ⚙️ Configuração
```
app_paths.py
├── Propósito: Definir caminhos globais
└── Imports externos: pathlib

vps_config.py
├── Propósito: Configuração VPS
├── Imports internos: (Nenhum)
└── Imports externos: os, json, dotenv
```

---

## 🔗 DIAGRAMA DE FLUXO DE DADOS

```
┌─────────────────────────────────────────────────────────┐
│         USUÁRIO DESKTOP (main.py)                       │
└─────────────┬───────────────────────────────────────────┘
              │
              ▼
      ┌───────────────┐
      │  deck_window  │ ◄────────────────┐
      └───┬───────────┘                  │
          │                              │
          ├─►background_controller       │
          ├─►loading_dialog              │
          ├─►playback_window             │
          ├─►theme                       │
          └─►app_paths                   │
              │                          │
              ▼                          │
      ┌───────────────────┐             │
      │  API_SERVER       │             │
      │  (VPS REMOTA)     │             │
      └─┬─────────────────┘             │
        │                               │
        ├─►database                     │
        ├─►download_manager            │
        ├─►sincronizador               │
        └─►arquivo_processor           │
            │                          │
            ▼                          │
    ┌────────────────────┐             │
    │  DISCORD BOT       │             │
    │  (VPS)             │             │
    └─┬──────────────────┘             │
      │                                │
      ├─►bot_humanizado               │
      ├─►bot_connector                │
      ├─►bot_key_ui                   │
      ├─►bot_file_sync                │
      └─►database ────────────────────►
```

---

## 🔄 Fluxo de Importações

### Nível 1 - Entrypoints
```
main.py (nenhuma dependência local)
bot.py (importa: database, download_manager, bot_humanizado)
api_server.py (importa: database, download_manager, sincronizador)
```

### Nível 2 - Core Modules
```
database.py (nenhuma dependência local)
database_client.py (importa: vps_config)
download_manager.py (nenhuma dependência local)
```

### Nível 3 - Support Modules
```
deck_window.py (importa: background_controller, loading_dialog, playback_window, app_paths)
bot_humanizado.py (nenhuma dependência local)
sincronizador.py (importa: database_client)
arquivo_processor.py (nenhuma dependência local)
```

### Nível 4 - Utility Modules
```
theme.py (nenhuma dependência local)
beta_warning.py (nenhuma dependência local)
app_paths.py (nenhuma dependência local)
vps_config.py (nenhuma dependência local)
```

---

## 📊 Análise de Acoplamento

### Arquivos mais utilizados (Highest Coupling)
```
✅ database.py           - Importado por: bot, api_server, sincronizador (3)
✅ download_manager.py   - Importado por: bot, api_server (2)
✅ app_paths.py          - Importado por: deck_window, sincronizador (2)
✅ vps_config.py         - Importado por: database_client (1)
```

### Arquivos isolados (Low Coupling - Bom!)
```
✅ theme.py              - Não é importado por ninguém (UI Pura)
✅ beta_warning.py       - Não é importado por ninguém (Dialog Isolado)
✅ background_controller.py - Não é importado por ninguém (Thread Manager)
✅ browser_downloader.py - Não é importado por ninguém (Standalone)
```

---

## 🎯 Matriz de Dependências

| From \ To | database | dwnld_mgr | vps_cfg | db_client | sincro | arquivo | app_paths |
|-----------|----------|-----------|---------|-----------|--------|---------|-----------|
| bot.py | ✅ | ✅ | | | | | |
| api_srv.py | ✅ | ✅ | | ✅ | ✅ | ✅ | |
| bot_human.py | | | | | | | |
| db_client.py | | | ✅ | | | | |
| sincro.py | | | | ✅ | | | ✅ |
| arquivo_proc.py | | | | | | | |
| deck_window.py | | | | | | | ✅ |

---

## 🏗️ Arquitetura Resumida

```
┌─────────────────────────────────────────────────┐
│              TIER 0: ENTRYPOINTS                │
├─────────────────────────────────────────────────┤
│  main.py (Desktop) | bot.py (Discord) | api_server.py (API) │
└──────┬──────────────────────┬──────────────────┬┘
       │                      │                  │
       └──────────┬───────────┴──────────────────┘
                  │
       ┌──────────▼─────────────┐
       │  TIER 1: CORE MODULES  │
       ├────────────────────────┤
       │ database.py            │
       │ download_manager.py    │
       │ sincronizador.py       │
       │ arquivo_processor.py   │
       │ database_client.py     │
       └──────────┬─────────────┘
                  │
       ┌──────────▼──────────────┐
       │ TIER 2: SUPPORT MODULES │
       ├───────────────────────────┤
       │ bot_humanizado.py       │
       │ bot_connector.py        │
       │ bot_key_ui.py          │
       │ bot_file_sync.py       │
       │ background_controller   │
       │ loading_dialog.py       │
       │ playback_window.py      │
       └──────────┬──────────────┘
                  │
       ┌──────────▼──────────────┐
       │ TIER 3: CONFIG/UTILS    │
       ├───────────────────────────┤
       │ vps_config.py          │
       │ app_paths.py           │
       │ theme.py               │
       │ beta_warning.py        │
       │ browser_downloader.py  │
       └───────────────────────┘
```

---

## 🧪 Testes Recomendados por Função

### Import Order
```python
# ✅ Ordem correta de importação
import database           # Core
import download_manager   # Core
import app_paths         # Config
import bot_humanizado    # Feature
```

### Dependency Chain
```python
# ✅ Validar cadeia de importação
main.py
  → deck_window.py
    → background_controller.py ✅ (sem ciclos)
    → app_paths.py ✅ (sem ciclos)
```

---

## 📝 Notas de Manutenção

1. **Evitar Imports Cíclicos**: A estrutura atual não tem ciclos ✅
2. **Manter Separação de Concerns**: Core, UI, Config bem definidos ✅
3. **Facilitar Testes**: Modules podem ser testados independentemente ✅
4. **Documentar Novos Imports**: Adicionar ao gráfico quando novo arquivo for criado

---

**Estrutura validada e documentada** ✅  
**Pronto para produção** 🚀
