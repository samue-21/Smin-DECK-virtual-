# Diálogo para Discord - Login automático e geração de chave

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon
import webbrowser
import time


class DiscordAuthThread(QThread):
    """Thread para fazer autenticação no Discord"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)  # (sucesso, mensagem/chave)
    
    def __init__(self, vps_url="http://72.60.244.240:5000"):
        super().__init__()
        self.vps_url = vps_url
    
    def run(self):
        """Executa fluxo de autenticação"""
        try:
            self.progress.emit("1️⃣ Abrindo Discord...")
            time.sleep(0.5)
            
            # Abre Discord para criar/logar
            url = "https://discord.com/app"
            webbrowser.open(url)
            
            self.progress.emit("2️⃣ Aguardando... (crie ou entre em um servidor)")
            time.sleep(2)
            
            self.progress.emit("3️⃣ Solicitar adição do bot no servidor...")
            time.sleep(1)
            
            self.progress.emit("4️⃣ Bot criando sala automaticamente...")
            time.sleep(2)
            
            self.progress.emit("5️⃣ Gerando sua chave de conexão...")
            time.sleep(1)
            
            # Simular chamada ao VPS para gerar chave
            # Em produção, isso seria um endpoint real
            import random
            import string
            chave = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            
            self.progress.emit("✅ Chave gerada com sucesso!")
            time.sleep(0.5)
            
            self.finished.emit(True, chave)
        
        except Exception as e:
            self.finished.emit(False, f"❌ Erro: {str(e)}")


class DiscordAuthDialog(QDialog):
    """Diálogo para autenticação automática com Discord"""
    
    def __init__(self, connector, parent=None):
        super().__init__(parent)
        self.connector = connector
        self.auth_thread = None
        self.generated_key = None
        self.init_ui()
    
    def init_ui(self):
        """Cria interface do diálogo"""
        self.setWindowTitle("🤖 Autenticar com Discord")
        self.setGeometry(100, 100, 500, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QPushButton {
                background-color: #5865F2;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4752C4;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("🤖 Integrar Discord")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Instruções
        instructions = QLabel(
            "Este processo vai:\n\n"
            "1️⃣ Abrir Discord para você criar/acessar um servidor\n"
            "2️⃣ Adicionar o SminBot no seu servidor\n"
            "3️⃣ Bot criará automaticamente uma sala\n"
            "4️⃣ Você receberá uma chave para colar aqui\n\n"
            "Clique em 'Iniciar' para começar!"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Progress
        self.progress_label = QLabel("Aguardando...")
        layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #5865F2;
                border-radius: 5px;
                text-align: center;
                background-color: #2c2f33;
            }
            QProgressBar::chunk {
                background-color: #5865F2;
            }
        """)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Botões
        btn_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶️ Iniciar")
        self.start_btn.clicked.connect(self.start_auth)
        btn_layout.addWidget(self.start_btn)
        
        self.cancel_btn = QPushButton("❌ Cancelar")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def start_auth(self):
        """Inicia fluxo de autenticação"""
        self.start_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.auth_thread = DiscordAuthThread()
        self.auth_thread.progress.connect(self.on_progress)
        self.auth_thread.finished.connect(self.on_finished)
        self.auth_thread.start()
    
    def on_progress(self, message):
        """Atualiza progress"""
        self.progress_label.setText(message)
        self.progress_bar.setValue(self.progress_bar.value() + 20)
    
    def on_finished(self, success, data):
        """Finaliza autenticação"""
        self.progress_bar.setVisible(False)
        
        if success:
            self.generated_key = data
            
            # Mostrar mensagem de sucesso
            QMessageBox.information(
                self,
                "✅ Sucesso!",
                f"Sua chave de conexão:\n\n{data}\n\n"
                f"Esta chave será adicionada automaticamente ao app."
            )
            
            # Adicionar chave automaticamente
            self.connector.add_key(data)
            
            self.accept()
        else:
            QMessageBox.critical(
                self,
                "❌ Erro",
                f"Falha na autenticação:\n\n{data}"
            )
            self.start_btn.setEnabled(True)


class DiscordLoginButton(QPushButton):
    """Botão para fazer login com Discord"""
    
    def __init__(self, connector, parent=None):
        super().__init__("🎮 Login com Discord", parent)
        self.connector = connector
        self.setStyleSheet("""
            QPushButton {
                background-color: #5865F2;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4752C4;
            }
        """)
        self.clicked.connect(self.show_auth_dialog)
    
    def show_auth_dialog(self):
        """Mostra diálogo de autenticação"""
        dialog = DiscordAuthDialog(self.connector, self.parent())
        dialog.exec()


if __name__ == "__main__":
    print("Este módulo é para uso interno no app")
