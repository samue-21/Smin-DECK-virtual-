# 📂 Integração Arquivos Gerais - No App

## 🎯 Objetivo

Adicionar um menu no app para **acessar a pasta "Arquivos Gerais"** onde os arquivos do Discord são salvos automaticamente.

---

## 📐 Estrutura

### Menu do App (deck_window.py)

```
┌──────────────────────────────────┐
│  🎮 SminDeck                     │
├──────────────────────────────────┤
│ Menu:                            │
│ ├─ 📚 Botões                    │
│ ├─ 🎮 Gerenciar Controles      │
│ ├─ ⚙️ Configurações             │
│ ├─ 🤖 Conexão Bot              │
│ └─ 📂 Arquivos Gerais ← NOVO   │
│    └─ Abre pasta local         │
│       com arquivos sincronizados│
└──────────────────────────────────┘
```

---

## 💻 Implementação (Python)

### Opção 1: Adicionar no Menu Principal

```python
# Em deck_window.py

def adicionar_menu_arquivos_gerais(self):
    """Adiciona opção de Arquivos Gerais no menu"""
    
    # Criar ação
    self.action_arquivos_gerais = QAction("📂 Arquivos Gerais")
    self.action_arquivos_gerais.triggered.connect(self.abrir_arquivos_gerais)
    self.menu_principal.addAction(self.action_arquivos_gerais)

def abrir_arquivos_gerais(self):
    """Abre a pasta Arquivos Gerais"""
    
    import os
    import platform
    from pathlib import Path
    
    # Determinar caminho da pasta
    home = str(Path.home())
    pasta_arquivos = os.path.join(home, '.smindeckbot', 'arquivos_gerais')
    
    # Criar pasta se não existir
    os.makedirs(pasta_arquivos, exist_ok=True)
    
    # Abrir pasta
    if platform.system() == 'Windows':
        os.startfile(pasta_arquivos)
    elif platform.system() == 'Darwin':  # macOS
        os.system(f'open "{pasta_arquivos}"')
    else:  # Linux
        os.system(f'xdg-open "{pasta_arquivos}"')
```

### Opção 2: Adicionar Atalho na Toolbar

```python
# Em deck_window.py - __init__

# Botão na toolbar
btn_arquivos = QPushButton("📂 Arquivos Gerais")
btn_arquivos.clicked.connect(self.abrir_arquivos_gerais)
self.toolbar.addWidget(btn_arquivos)

# Mesmo método anterior
def abrir_arquivos_gerais(self):
    # ... código igual ...
```

### Opção 3: Criar Dialog com Preview

```python
# Em deck_window.py ou em novo arquivo: arquivo_gerais_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget, 
    QListWidgetItem, QPushButton, QLabel
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import os
from pathlib import Path

class ArquivosGeraisDialog(QDialog):
    """Dialog para visualizar e gerenciar arquivos"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📂 Arquivos Gerais")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QListWidget {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
            }
            QPushButton {
                background-color: #0d7377;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #14919b;
            }
        """)
        
        self.init_ui()
    
    def init_ui(self):
        """Interface"""
        layout = QVBoxLayout()
        
        # Info
        info = QLabel("📂 Arquivos sincronizados do Discord")
        layout.addWidget(info)
        
        # Lista de arquivos
        self.lista = QListWidget()
        self.carregar_arquivos()
        layout.addWidget(self.lista)
        
        # Botões
        btn_layout = QHBoxLayout()
        
        btn_abrir = QPushButton("🔓 Abrir Pasta")
        btn_abrir.clicked.connect(self.abrir_pasta)
        btn_layout.addWidget(btn_abrir)
        
        btn_recarregar = QPushButton("🔄 Recarregar")
        btn_recarregar.clicked.connect(self.carregar_arquivos)
        btn_layout.addWidget(btn_recarregar)
        
        btn_deletar = QPushButton("🗑️ Deletar")
        btn_deletar.clicked.connect(self.deletar_selecionado)
        btn_layout.addWidget(btn_deletar)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def carregar_arquivos(self):
        """Carrega lista de arquivos"""
        self.lista.clear()
        
        home = str(Path.home())
        pasta = os.path.join(home, '.smindeckbot', 'arquivos_gerais')
        
        # Criar pasta se não existir
        os.makedirs(pasta, exist_ok=True)
        
        try:
            arquivos = os.listdir(pasta)
            
            if not arquivos:
                item = QListWidgetItem("Nenhum arquivo ainda...")
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                self.lista.addItem(item)
                return
            
            for arquivo in sorted(arquivos, reverse=True):
                arquivo_path = os.path.join(pasta, arquivo)
                
                if os.path.isfile(arquivo_path):
                    # Info do arquivo
                    tamanho = os.path.getsize(arquivo_path)
                    tamanho_mb = f"{tamanho / (1024*1024):.2f} MB"
                    
                    texto = f"{arquivo} ({tamanho_mb})"
                    item = QListWidgetItem(texto)
                    item.setData(Qt.ItemDataRole.UserRole, arquivo_path)
                    self.lista.addItem(item)
        
        except Exception as e:
            print(f"Erro ao carregar arquivos: {e}")
    
    def abrir_pasta(self):
        """Abre a pasta no explorador"""
        import platform
        
        home = str(Path.home())
        pasta = os.path.join(home, '.smindeckbot', 'arquivos_gerais')
        
        if platform.system() == 'Windows':
            os.startfile(pasta)
        elif platform.system() == 'Darwin':
            os.system(f'open "{pasta}"')
        else:
            os.system(f'xdg-open "{pasta}"')
    
    def deletar_selecionado(self):
        """Deleta arquivo selecionado"""
        item = self.lista.currentItem()
        
        if not item:
            return
        
        arquivo_path = item.data(Qt.ItemDataRole.UserRole)
        
        if arquivo_path and os.path.exists(arquivo_path):
            os.remove(arquivo_path)
            self.carregar_arquivos()


# Usar no deck_window.py:
def abrir_arquivos_gerais(self):
    dialog = ArquivosGeraisDialog(self)
    dialog.exec()
```

---

## 🎨 Interface Visual

### Opção 1: Simples (Menu)
```
Menu: File / Edit / ... / 📂 Arquivos Gerais
                         └─ Clica
                            └─ Abre pasta no Windows Explorer / Finder / Nautilus
```

### Opção 2: Com Dialog (Melhor)
```
┌─────────────────────────────────────┐
│ 📂 Arquivos Gerais          [X]     │
├─────────────────────────────────────┤
│ 📂 Arquivos sincronizados do Discord│
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ 20260106_143000_video.mp4 (45M) │ │
│ │ 20260106_150530_imagem.png (2M) │ │
│ │ 20260106_161200_documento.pdf   │ │
│ │ 20260107_091545_musica.mp3 (8M) │ │
│ └─────────────────────────────────┘ │
│                                     │
│ [🔓 Abrir Pasta] [🔄 Recarregar]  │
│ [🗑️ Deletar]                       │
└─────────────────────────────────────┘
```

---

## 🔄 Fluxo Completo com App

```
USUÁRIO NO DISCORD
│
└─ Clica /help
   └─ Botão "💾 Enviar Arquivo"
      └─ Upload arquivo
         └─ Bot detecta + salva
            │
            ↓
         USUÁRIO NO APP
         │
         └─ Menu: Arquivos Gerais
            └─ Abre dialog/pasta
               └─ Vê arquivo
                  ├─ Opção 1: Abrir arquivo
                  ├─ Opção 2: Copiar arquivo
                  └─ Opção 3: Usar em botão
                     ├─ Drag-drop → Botão
                     │  └─ Atualiza botão ✅
                     │
                     └─ Add como mídia
                        └─ Em biblioteca ✅
```

---

## 🛠️ Integração Completa

### No deck_window.py

```python
# 1. Imports no topo
from pathlib import Path
import os
import platform

# 2. No __init__, adicionar:
self.setup_arquivos_gerais_menu()

# 3. Novo método:
def setup_arquivos_gerais_menu(self):
    """Configura menu de Arquivos Gerais"""
    
    # Adicionar ao menu principal
    action = QAction("📂 Arquivos Gerais", self)
    action.triggered.connect(self.abrir_arquivos_gerais)
    self.menu_ferramentas.addAction(action)
    
    # Ou adicionar ao toolbar
    btn = QPushButton("📂")
    btn.setToolTip("Arquivos Gerais")
    btn.clicked.connect(self.abrir_arquivos_gerais)
    self.toolbar.addWidget(btn)

def abrir_arquivos_gerais(self):
    """Abre dialog ou pasta"""
    
    # Opção A: Dialog com preview
    # dialog = ArquivosGeraisDialog(self)
    # dialog.exec()
    
    # Opção B: Abrir pasta direto
    home = str(Path.home())
    pasta = os.path.join(home, '.smindeckbot', 'arquivos_gerais')
    os.makedirs(pasta, exist_ok=True)
    
    if platform.system() == 'Windows':
        os.startfile(pasta)
    elif platform.system() == 'Darwin':
        os.system(f'open "{pasta}"')
    else:
        os.system(f'xdg-open "{pasta}"')
```

---

## ✨ Funcionalidades Adicionais (Futuro)

### 1. Drag-Drop de Arquivo para Botão
```python
# Permitir arrastar arquivo para botão
def drag_drop_arquivo_para_botao(self, arquivo_path, botao_id):
    """Arrasta arquivo para atualizar botão"""
    
    # Copiar arquivo para a pasta de mídia do botão
    # Atualizar config do botão
    # Recarregar interface
```

### 2. Preview Rápido
```python
# Ver preview do arquivo antes de usar
def preview_arquivo(self, arquivo_path):
    """Mostra preview do arquivo"""
    
    extensao = os.path.splitext(arquivo_path)[1]
    
    if extensao in ['.png', '.jpg', '.gif']:
        # Mostrar imagem
    elif extensao in ['.mp4', '.webm']:
        # Reproduzir vídeo
    elif extensao == '.pdf':
        # Abrir PDF
```

### 3. Organizar por Tipo
```python
# Filtrar por tipo de arquivo
def filtrar_por_tipo(self, tipo):
    """Filtra: Imagens, Vídeos, PDFs, etc"""
    
    tipos = {
        'imagens': ['.png', '.jpg', '.gif', '.webp'],
        'videos': ['.mp4', '.webm', '.avi'],
        'audio': ['.mp3', '.wav', '.ogg'],
        'docs': ['.pdf', '.docx', '.txt']
    }
```

---

## 📝 Código Pronto para Copiar

### Arquivo: `arquivo_gerais_dialog.py`

```python
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget, 
    QListWidgetItem, QPushButton, QLabel, QMessageBox
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import os
from pathlib import Path

class ArquivosGeraisDialog(QDialog):
    """Dialog para gerenciar Arquivos Gerais"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📂 Arquivos Gerais")
        self.setGeometry(100, 100, 600, 400)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Info
        info = QLabel("📂 Arquivos sincronizados do Discord\n"
                      "Você pode arrastar para botões ou adicionar como mídia")
        layout.addWidget(info)
        
        # Lista
        self.lista = QListWidget()
        self.carregar_arquivos()
        layout.addWidget(self.lista)
        
        # Botões
        btn_layout = QHBoxLayout()
        
        btn_abrir = QPushButton("🔓 Abrir Pasta")
        btn_abrir.clicked.connect(self.abrir_pasta)
        btn_layout.addWidget(btn_abrir)
        
        btn_recarregar = QPushButton("🔄 Recarregar")
        btn_recarregar.clicked.connect(self.carregar_arquivos)
        btn_layout.addWidget(btn_recarregar)
        
        btn_deletar = QPushButton("🗑️ Deletar")
        btn_deletar.clicked.connect(self.deletar_selecionado)
        btn_layout.addWidget(btn_deletar)
        
        btn_fechar = QPushButton("✖️ Fechar")
        btn_fechar.clicked.connect(self.close)
        btn_layout.addWidget(btn_fechar)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def carregar_arquivos(self):
        self.lista.clear()
        home = str(Path.home())
        pasta = os.path.join(home, '.smindeckbot', 'arquivos_gerais')
        os.makedirs(pasta, exist_ok=True)
        
        try:
            arquivos = os.listdir(pasta)
            if not arquivos:
                item = QListWidgetItem("Nenhum arquivo ainda...")
                self.lista.addItem(item)
                return
            
            for arquivo in sorted(arquivos, reverse=True):
                path = os.path.join(pasta, arquivo)
                if os.path.isfile(path):
                    tamanho = os.path.getsize(path) / (1024*1024)
                    texto = f"{arquivo} ({tamanho:.2f} MB)"
                    item = QListWidgetItem(texto)
                    item.setData(Qt.ItemDataRole.UserRole, path)
                    self.lista.addItem(item)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar: {e}")
    
    def abrir_pasta(self):
        import platform
        home = str(Path.home())
        pasta = os.path.join(home, '.smindeckbot', 'arquivos_gerais')
        
        if platform.system() == 'Windows':
            os.startfile(pasta)
        elif platform.system() == 'Darwin':
            os.system(f'open "{pasta}"')
        else:
            os.system(f'xdg-open "{pasta}"')
    
    def deletar_selecionado(self):
        item = self.lista.currentItem()
        if item:
            path = item.data(Qt.ItemDataRole.UserRole)
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                    self.carregar_arquivos()
                    QMessageBox.information(self, "Sucesso", "Arquivo deletado!")
                except Exception as e:
                    QMessageBox.critical(self, "Erro", f"Erro ao deletar: {e}")
```

### Usar em deck_window.py:

```python
# No topo:
from arquivo_gerais_dialog import ArquivosGeraisDialog

# No __init__:
action = QAction("📂 Arquivos Gerais", self)
action.triggered.connect(self.abrir_arquivos_gerais)
self.menu_principal.addAction(action)

# Novo método:
def abrir_arquivos_gerais(self):
    dialog = ArquivosGeraisDialog(self)
    dialog.exec()
```

---

## 🎯 Resumo

| Item | Descrição |
|------|-----------|
| **Função** | Acessar arquivos sincronizados do Discord |
| **Local** | Menu principal do app |
| **Atalho** | "📂 Arquivos Gerais" |
| **Pasta** | `~/.smindeckbot/arquivos_gerais/` |
| **Ações** | Abrir, Recarregar, Deletar |
| **Uso** | Drag-drop em botões, adicionar como mídia |

---

**PRONTO PARA INTEGRAR! 🚀**
