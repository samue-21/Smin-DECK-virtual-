#!/usr/bin/env python3
"""
Setup Completo do Cliente SminDeck
Configura tokens, credenciais e testa integração com o bot Discord.
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

try:
    from PyQt6.QtWidgets import (
        QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
        QLineEdit, QPushButton, QMessageBox, QTabWidget, QTextEdit,
        QGroupBox, QComboBox, QCheckBox
    )
    from PyQt6.QtCore import Qt, QThread, pyqtSignal
    from PyQt6.QtGui import QFont
except ImportError:
    print("❌ Erro: PyQt6 não instalado")
    sys.exit(1)


class TestadorBotSignals(QThread):
    """Thread para testar conexão com o bot"""
    resultado = pyqtSignal(str)
    erro = pyqtSignal(str)
    
    def __init__(self, token, bot_url):
        super().__init__()
        self.token = token
        self.bot_url = bot_url
    
    def run(self):
        try:
            import requests
            
            # Testar conexão com Discord API
            self.resultado.emit("🔍 Testando token com Discord API...")
            
            headers = {"Authorization": f"Bot {self.token}"}
            response = requests.get(
                "https://discord.com/api/v10/users/@me",
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                bot_info = response.json()
                self.resultado.emit(f"✅ Bot conectado: {bot_info['username']}#{bot_info['discriminator']}")
            else:
                self.erro.emit(f"❌ Token inválido ou expirado (Status: {response.status_code})")
                return
            
            # Testar conexão com bot local/remoto
            if self.bot_url and self.bot_url.startswith("http"):
                self.resultado.emit(f"🔍 Testando conexão com {self.bot_url}...")
                response = requests.get(f"{self.bot_url}/health", timeout=5)
                
                if response.status_code == 200:
                    self.resultado.emit(f"✅ Bot local/remoto respondendo corretamente")
                else:
                    self.resultado.emit(f"⚠️ Bot local/remoto não respondeu (Status: {response.status_code})")
            
            self.resultado.emit("\n✅ Testes concluídos com sucesso!")
            
        except Exception as e:
            self.erro.emit(f"❌ Erro durante testes: {str(e)}")


class SetupClienteCompleto(QDialog):
    """Interface de setup completo do cliente"""
    
    def __init__(self):
        super().__init__()
        self.env_file = Path.cwd() / ".env"
        self.config_file = Path.cwd() / "client_config.json"
        self.testador = None
        self.init_ui()
        self.carregar_configs()
    
    def init_ui(self):
        """Criar interface gráfica"""
        self.setWindowTitle("🎮 Setup Completo - SminDeck Cliente")
        self.setGeometry(50, 50, 900, 700)
        
        layout = QVBoxLayout()
        
        # Título
        titulo = QLabel("⚙️ Configuração Completa do Cliente SminDeck")
        fonte_titulo = QFont()
        fonte_titulo.setPointSize(14)
        fonte_titulo.setBold(True)
        titulo.setFont(fonte_titulo)
        layout.addWidget(titulo)
        
        # Abas
        abas = QTabWidget()
        
        # Aba 1: Credenciais Discord
        aba_discord = self.criar_aba_discord()
        abas.addTab(aba_discord, "🤖 Discord Bot")
        
        # Aba 2: Configurações de Conexão
        aba_conexao = self.criar_aba_conexao()
        abas.addTab(aba_conexao, "🔌 Conexão")
        
        # Aba 3: Testes
        aba_testes = self.criar_aba_testes()
        abas.addTab(aba_testes, "✅ Testes")
        
        # Aba 4: Status
        aba_status = self.criar_aba_status()
        abas.addTab(aba_status, "📊 Status")
        
        layout.addWidget(abas)
        
        # Botões de ação
        botoes_layout = QHBoxLayout()
        
        btn_salvar = QPushButton("💾 Salvar Configurações")
        btn_salvar.clicked.connect(self.salvar_configuracoes)
        botoes_layout.addWidget(btn_salvar)
        
        btn_testar = QPushButton("🧪 Testar Tudo")
        btn_testar.clicked.connect(self.testar_tudo)
        botoes_layout.addWidget(btn_testar)
        
        btn_fechar = QPushButton("❌ Fechar")
        btn_fechar.clicked.connect(self.accept)
        botoes_layout.addWidget(btn_fechar)
        
        layout.addLayout(botoes_layout)
        
        self.setLayout(layout)
    
    def criar_aba_discord(self):
        """Aba para configurar credenciais Discord"""
        widget = QDialog()
        layout = QVBoxLayout()
        
        # Grupo de Token
        grupo_token = QGroupBox("🔑 Token do Bot Discord")
        grupo_layout = QVBoxLayout()
        
        label_token = QLabel(
            "1. Acesse: https://discord.com/developers/applications\n"
            "2. Crie um 'New Application'\n"
            "3. Vá para 'Bot' → 'Add Bot'\n"
            "4. Clique em 'Copy' embaixo de TOKEN\n"
            "5. Cole seu token abaixo:"
        )
        label_token.setStyleSheet("color: #666; font-size: 10px;")
        grupo_layout.addWidget(label_token)
        
        self.input_token = QLineEdit()
        self.input_token.setPlaceholderText("Cole seu DISCORD_TOKEN aqui...")
        self.input_token.setEchoMode(QLineEdit.EchoMode.Password)
        grupo_layout.addWidget(self.input_token)
        
        grupo_token.setLayout(grupo_layout)
        layout.addWidget(grupo_token)
        
        # Grupo de IDs
        grupo_ids = QGroupBox("📍 IDs do Discord")
        grupo_ids_layout = QVBoxLayout()
        
        # Server ID
        label_server_id = QLabel("ID do Servidor Discord:")
        grupo_ids_layout.addWidget(label_server_id)
        self.input_server_id = QLineEdit()
        self.input_server_id.setPlaceholderText("Encontre em Server Settings → Widget")
        grupo_ids_layout.addWidget(self.input_server_id)
        
        # Channel ID
        label_channel_id = QLabel("ID do Canal (opcional):")
        grupo_ids_layout.addWidget(label_channel_id)
        self.input_channel_id = QLineEdit()
        self.input_channel_id.setPlaceholderText("ID do canal para enviar mensagens")
        grupo_ids_layout.addWidget(self.input_channel_id)
        
        # User ID
        label_user_id = QLabel("Seu ID do Discord (opcional):")
        grupo_ids_layout.addWidget(label_user_id)
        self.input_user_id = QLineEdit()
        self.input_user_id.setPlaceholderText("Seu ID de usuário")
        grupo_ids_layout.addWidget(self.input_user_id)
        
        grupo_ids.setLayout(grupo_ids_layout)
        layout.addWidget(grupo_ids)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def criar_aba_conexao(self):
        """Aba para configurar conexão"""
        widget = QDialog()
        layout = QVBoxLayout()
        
        # Tipo de conexão
        grupo_conexao = QGroupBox("🌐 Tipo de Conexão")
        grupo_conexao_layout = QVBoxLayout()
        
        label_tipo = QLabel("Onde o bot está rodando?")
        grupo_conexao_layout.addWidget(label_tipo)
        
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems([
            "VPS Remoto (72.60.244.240)",
            "Localhost (127.0.0.1:8000)",
            "Outro URL personalizado"
        ])
        self.combo_tipo.currentIndexChanged.connect(self.atualizar_campos_conexao)
        grupo_conexao_layout.addWidget(self.combo_tipo)
        
        grupo_conexao.setLayout(grupo_conexao_layout)
        layout.addWidget(grupo_conexao)
        
        # URL Personalizada
        grupo_url = QGroupBox("📬 URL do Bot")
        grupo_url_layout = QVBoxLayout()
        
        label_url = QLabel("URL do servidor bot:")
        grupo_url_layout.addWidget(label_url)
        
        self.input_url = QLineEdit()
        self.input_url.setPlaceholderText("http://72.60.244.240:8000")
        grupo_url_layout.addWidget(self.input_url)
        
        grupo_url.setLayout(grupo_url_layout)
        layout.addWidget(grupo_url)
        
        # Timeout
        grupo_timeout = QGroupBox("⏱️ Configurações de Tempo")
        grupo_timeout_layout = QVBoxLayout()
        
        label_timeout = QLabel("Timeout de conexão (segundos):")
        grupo_timeout_layout.addWidget(label_timeout)
        
        self.input_timeout = QLineEdit()
        self.input_timeout.setText("10")
        self.input_timeout.setMaximumWidth(100)
        grupo_timeout_layout.addWidget(self.input_timeout)
        
        grupo_timeout.setLayout(grupo_timeout_layout)
        layout.addWidget(grupo_timeout)
        
        # Opções
        self.checkbox_ssl = QCheckBox("Verificar certificado SSL")
        self.checkbox_ssl.setChecked(True)
        layout.addWidget(self.checkbox_ssl)
        
        self.checkbox_debug = QCheckBox("Modo Debug (mais verboso)")
        layout.addWidget(self.checkbox_debug)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def criar_aba_testes(self):
        """Aba para executar testes"""
        widget = QDialog()
        layout = QVBoxLayout()
        
        # Botões de teste
        grupo_testes = QGroupBox("🧪 Testes Disponíveis")
        grupo_testes_layout = QVBoxLayout()
        
        btn_teste_token = QPushButton("🔑 Testar Token Discord")
        btn_teste_token.clicked.connect(self.testar_token)
        grupo_testes_layout.addWidget(btn_teste_token)
        
        btn_teste_conexao = QPushButton("🔌 Testar Conexão com Bot")
        btn_teste_conexao.clicked.connect(self.testar_conexao)
        grupo_testes_layout.addWidget(btn_teste_conexao)
        
        btn_teste_ping = QPushButton("📡 Ping no Bot")
        btn_teste_ping.clicked.connect(self.testar_ping)
        grupo_testes_layout.addWidget(btn_teste_ping)
        
        grupo_testes.setLayout(grupo_testes_layout)
        layout.addWidget(grupo_testes)
        
        # Resultado dos testes
        layout.addWidget(QLabel("📝 Resultado dos Testes:"))
        
        self.text_resultado = QTextEdit()
        self.text_resultado.setReadOnly(True)
        self.text_resultado.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                font-family: 'Courier New';
                font-size: 10px;
            }
        """)
        layout.addWidget(self.text_resultado)
        
        widget.setLayout(layout)
        return widget
    
    def criar_aba_status(self):
        """Aba de status geral"""
        widget = QDialog()
        layout = QVBoxLayout()
        
        # Status atual
        layout.addWidget(QLabel("📊 Status da Configuração:"))
        
        self.text_status = QTextEdit()
        self.text_status.setReadOnly(True)
        self.text_status.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                font-family: 'Courier New';
                font-size: 10px;
            }
        """)
        layout.addWidget(self.text_status)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def atualizar_campos_conexao(self):
        """Atualizar campos conforme o tipo de conexão"""
        indice = self.combo_tipo.currentIndex()
        
        if indice == 0:  # VPS Remoto
            self.input_url.setText("http://72.60.244.240:8000")
        elif indice == 1:  # Localhost
            self.input_url.setText("http://127.0.0.1:8000")
        elif indice == 2:  # Personalizado
            self.input_url.setText("")
    
    def testar_token(self):
        """Testar token Discord"""
        token = self.input_token.text().strip()
        
        if not token:
            self.text_resultado.append("❌ Token não fornecido!")
            return
        
        self.text_resultado.clear()
        self.text_resultado.append("🔍 Testando token Discord...")
        
        try:
            import requests
            
            headers = {"Authorization": f"Bot {token}"}
            response = requests.get(
                "https://discord.com/api/v10/users/@me",
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                bot_info = response.json()
                self.text_resultado.append(f"✅ Token válido!")
                self.text_resultado.append(f"Bot: {bot_info['username']}#{bot_info['discriminator']}")
                self.text_resultado.append(f"ID: {bot_info['id']}")
            else:
                self.text_resultado.append(f"❌ Token inválido (Status: {response.status_code})")
                self.text_resultado.append(response.text)
        
        except Exception as e:
            self.text_resultado.append(f"❌ Erro: {str(e)}")
    
    def testar_conexao(self):
        """Testar conexão com bot"""
        url = self.input_url.text().strip()
        
        if not url:
            self.text_resultado.append("❌ URL não fornecida!")
            return
        
        self.text_resultado.clear()
        self.text_resultado.append(f"🔌 Testando conexão com {url}...")
        
        try:
            import requests
            
            response = requests.get(
                f"{url}/health",
                timeout=5
            )
            
            if response.status_code == 200:
                self.text_resultado.append(f"✅ Bot respondendo corretamente!")
                self.text_resultado.append(response.json())
            else:
                self.text_resultado.append(f"⚠️ Status: {response.status_code}")
        
        except Exception as e:
            self.text_resultado.append(f"❌ Erro: {str(e)}")
    
    def testar_ping(self):
        """Testar ping no bot"""
        url = self.input_url.text().strip()
        
        if not url:
            self.text_resultado.append("❌ URL não fornecida!")
            return
        
        self.text_resultado.clear()
        self.text_resultado.append(f"📡 Enviando ping para {url}...")
        
        try:
            import requests
            import time
            
            inicio = time.time()
            response = requests.get(f"{url}/ping", timeout=5)
            tempo_resposta = (time.time() - inicio) * 1000
            
            if response.status_code == 200:
                self.text_resultado.append(f"✅ Pong! ({tempo_resposta:.0f}ms)")
            else:
                self.text_resultado.append(f"⚠️ Status: {response.status_code}")
        
        except Exception as e:
            self.text_resultado.append(f"❌ Erro: {str(e)}")
    
    def testar_tudo(self):
        """Testar todas as configurações"""
        self.text_resultado.clear()
        self.text_resultado.append("=" * 50)
        self.text_resultado.append("🧪 TESTANDO TUDO...")
        self.text_resultado.append("=" * 50 + "\n")
        
        # Teste 1: Token
        self.text_resultado.append("1️⃣ Testando Token Discord...")
        self.testar_token()
        self.text_resultado.append("\n")
        
        # Teste 2: Conexão
        self.text_resultado.append("2️⃣ Testando Conexão com Bot...")
        self.testar_conexao()
        self.text_resultado.append("\n")
        
        # Teste 3: Ping
        self.text_resultado.append("3️⃣ Testando Ping...")
        self.testar_ping()
        self.text_resultado.append("\n" + "=" * 50)
        self.text_resultado.append("✅ TESTES CONCLUÍDOS")
        self.text_resultado.append("=" * 50)
    
    def carregar_configs(self):
        """Carregar configurações existentes"""
        # Carregar do .env
        load_dotenv(self.env_file)
        
        token = os.getenv("DISCORD_TOKEN", "")
        if token:
            self.input_token.setText(token)
        
        # Carregar do JSON se existir
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                self.input_server_id.setText(config.get("server_id", ""))
                self.input_channel_id.setText(config.get("channel_id", ""))
                self.input_user_id.setText(config.get("user_id", ""))
                self.input_url.setText(config.get("bot_url", ""))
                self.input_timeout.setText(str(config.get("timeout", 10)))
                self.checkbox_debug.setChecked(config.get("debug", False))
            except Exception as e:
                print(f"Erro ao carregar config: {e}")
    
    def salvar_configuracoes(self):
        """Salvar todas as configurações"""
        try:
            # Salvar token no .env
            token = self.input_token.text().strip()
            if token:
                env_content = f"DISCORD_TOKEN={token}\n"
                with open(self.env_file, 'w', encoding='utf-8') as f:
                    f.write(env_content)
            
            # Salvar outras config no JSON
            config = {
                "server_id": self.input_server_id.text().strip(),
                "channel_id": self.input_channel_id.text().strip(),
                "user_id": self.input_user_id.text().strip(),
                "bot_url": self.input_url.text().strip(),
                "timeout": int(self.input_timeout.text() or "10"),
                "debug": self.checkbox_debug.isChecked(),
                "ssl_verify": self.checkbox_ssl.isChecked()
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            QMessageBox.information(
                self,
                "✅ Sucesso",
                "Configurações salvas com sucesso!\n\n"
                f"Token: {self.env_file}\n"
                f"Config: {self.config_file}"
            )
        
        except Exception as e:
            QMessageBox.critical(self, "❌ Erro", f"Erro ao salvar: {str(e)}")


def main():
    """Executar interface de setup"""
    app = QApplication(sys.argv)
    
    dialog = SetupClienteCompleto()
    dialog.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
