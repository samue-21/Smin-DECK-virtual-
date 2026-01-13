# Interface PyQt6 para adicionar chaves do Bot Discord

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QLabel, QCheckBox, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
import time
import requests
import subprocess
import os
import json
from pathlib import Path
from database_client import DatabaseClient


class BotConnectionThread(QThread):
    """Thread para conectar com bot sem travar UI"""
    progress = pyqtSignal(str)  # Emite status
    finished = pyqtSignal(bool, str)  # Emite (sucesso, mensagem)
    
    def __init__(self, connector, connection_key):
        super().__init__()
        self.connector = connector
        self.connection_key = connection_key
        self.db_client = DatabaseClient()
    
    def run(self):
        """Executa em thread separada"""
        try:
            self.progress.emit("🔍 Validando chave...")
            time.sleep(0.5)
            
            self.progress.emit("🔐 Conectando com bot...")
            time.sleep(0.5)
            
            # Obter info da chave do Bot via API
            user_id = None
            guild_id = None
            channel_id = None
            
            try:
                # Tenta na API nova (porta 5001)
                info = self.db_client.obter_info_chave(self.connection_key)
                if info:
                    user_id = info.get('user_id')
                    guild_id = info.get('guild_id')
                    channel_id = info.get('channel_id')
            except Exception as e:
                print(f"⚠️ Aviso: Não conseguiu obter dados da chave: {e}")
            
            # Validar chave no banco de dados
            if user_id and guild_id and channel_id:
                self.progress.emit("✓ Ativando chave no banco...")
                sucesso, msg = self.db_client.validar_chave(
                    self.connection_key.upper(),
                    user_id,
                    guild_id,
                    channel_id
                )
                
                if sucesso:
                    self.progress.emit("✓ Conectado!")
                    time.sleep(0.5)
                    self.finished.emit(True, msg)
                else:
                    self.finished.emit(False, msg)
            else:
                self.finished.emit(False, "❌ Chave não encontrada no servidor")
        except Exception as e:
            self.finished.emit(False, f"❌ Erro: {str(e)}")


class BotKeyDialog(QDialog):
    """Diálogo para adicionar chave do bot"""
    
    def __init__(self, connector, parent=None):
        super().__init__(parent)
        self.connector = connector
        self.connection_thread = None
        self.init_ui()
    
    def init_ui(self):
        """Cria interface"""
        self.setWindowTitle("Adicionar Chave - SminDeck Bot")
        self.setGeometry(100, 100, 450, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QLineEdit {
                background-color: #2d2d2d;
                color: #00ff00;
                border: 1px solid #00ff00;
                border-radius: 4px;
                padding: 8px;
                font-family: Courier;
                font-size: 12px;
            }
            QPushButton {
                background-color: #00ff00;
                color: #000000;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #00dd00;
            }
            QPushButton:pressed {
                background-color: #00aa00;
            }
            QLabel {
                color: #ffffff;
                font-size: 11px;
            }
            QCheckBox {
                color: #ffffff;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title = QLabel("🤖 Conectar com SminDeck Bot")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Instrução
        info = QLabel("Cole a chave recebida no Discord:")
        layout.addWidget(info)
        
        # Campo de entrada
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Ex: ABC12345")
        self.key_input.returnPressed.connect(self.connect_bot)
        layout.addWidget(self.key_input)
        
        # Status com checkbox
        status_layout = QHBoxLayout()
        self.status_checkbox = QCheckBox("Conectando com o bot...")
        self.status_checkbox.setEnabled(False)
        status_layout.addWidget(self.status_checkbox)
        status_layout.addStretch()
        layout.addLayout(status_layout)
        
        # Label de status detalhado
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #00ff00; font-size: 10px;")
        layout.addWidget(self.status_label)
        
        # Botões
        button_layout = QHBoxLayout()
        
        self.connect_btn = QPushButton("✓ Conectar")
        self.connect_btn.clicked.connect(self.connect_bot)
        button_layout.addWidget(self.connect_btn)
        
        cancel_btn = QPushButton("✗ Cancelar")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff0000;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #dd0000;
            }
        """)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def connect_bot(self):
        """Conecta com bot em thread separada"""
        chave = self.key_input.text().strip()
        
        if not chave:
            QMessageBox.warning(self, "Erro", "Cole uma chave válida!")
            return
        
        # Desabilitar interação
        self.key_input.setEnabled(False)
        self.connect_btn.setEnabled(False)
        self.status_checkbox.setChecked(False)
        self.status_checkbox.setEnabled(False)
        
        # Iniciar thread de conexão
        self.connection_thread = BotConnectionThread(self.connector, chave)
        self.connection_thread.progress.connect(self.update_progress)
        self.connection_thread.finished.connect(self.on_connection_finished)
        self.connection_thread.start()
    
    def update_progress(self, message):
        """Atualiza status durante conexão"""
        self.status_label.setText(message)
        self.status_checkbox.setCheckState(Qt.CheckState.Checked if "✓" in message else Qt.CheckState.Unchecked)
    
    def on_connection_finished(self, success, message):
        """Chamado quando conexão termina"""
        self.key_input.setEnabled(True)
        self.connect_btn.setEnabled(True)
        
        if success:
            self.status_label.setText("✓ Conectado com sucesso!")
            self.status_checkbox.setCheckState(Qt.CheckState.Checked)
            self.status_checkbox.setEnabled(False)
            
            # Fechar diálogo após 2 segundos
            self.connect_btn.setText("✓ Pronto!")
            self.connect_btn.setEnabled(False)
            
            # Esperar 2 segundos e fechar
            QThread.msleep(2000)
            self.accept()
        else:
            self.status_label.setText(message)
            self.status_checkbox.setCheckState(Qt.CheckState.Unchecked)
            QMessageBox.critical(self, "Erro de Conexão", message)


class BotKeysListDialog(QDialog):
    """Diálogo para gerenciar chaves conectadas"""
    
    def __init__(self, connector, parent=None):
        super().__init__(parent)
        self.connector = connector
        self.init_ui()
        self.load_keys()
    
    def init_ui(self):
        """Cria interface"""
        self.setWindowTitle("Gerenciar Chaves - SminDeck Bot")
        self.setGeometry(100, 100, 500, 350)
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QListWidget {
                background-color: #2d2d2d;
                color: #00ff00;
                border: 1px solid #00ff00;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #00ff00;
                color: #000000;
            }
            QPushButton {
                background-color: #00ff00;
                color: #000000;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00dd00;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title = QLabel("📋 Suas Conexões com o Bot")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Lista de chaves
        self.keys_list = QListWidget()
        layout.addWidget(self.keys_list)
        
        # Botões
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ Adicionar Nova Chave")
        add_btn.clicked.connect(lambda: BotKeyDialog(self.connector, self).exec())
        button_layout.addWidget(add_btn)
        
        remove_btn = QPushButton("➖ Remover")
        remove_btn.clicked.connect(self.remove_selected)
        button_layout.addWidget(remove_btn)
        
        close_btn = QPushButton("✓ Fechar")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def load_keys(self):
        """Carrega lista de chaves"""
        self.keys_list.clear()
        keys = self.connector.list_keys()
        
        if not keys:
            item = QListWidgetItem("Nenhuma chave adicionada")
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
            self.keys_list.addItem(item)
        else:
            for key, data in keys.items():
                text = f"✓ {key} - {data.get('name', 'SminDeck')}"
                self.keys_list.addItem(text)
    
    def remove_selected(self):
        """Remove chave selecionada"""
        item = self.keys_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Aviso", "Selecione uma chave para remover")
            return
        
        chave = item.text().split(" - ")[0].replace("✓ ", "")
        
        if QMessageBox.question(self, "Confirmar", f"Remover chave {chave}?") == QMessageBox.StandardButton.Yes:
            self.connector.remove_key(chave)
            self.load_keys()


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from bot_connector import connector
    
    app = QApplication([])
    dialog = BotKeyDialog(connector)
    dialog.exec()
