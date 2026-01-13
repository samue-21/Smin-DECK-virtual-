"""
💻 Dialog de DEV - Resetar chaves para testes
Apenas para desenvolvimento - NÃO mostra para cliente
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QMessageBox, QLineEdit, QSpinBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
import subprocess
import sys

class ResetWorkerThread(QThread):
    """Thread pra executar reset sem congelar UI"""
    status_changed = pyqtSignal(str)
    
    def __init__(self, script_name):
        super().__init__()
        self.script_name = script_name
    
    def run(self):
        try:
            self.status_changed.emit("⏳ Executando...")
            result = subprocess.run(
                [sys.executable, self.script_name],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.status_changed.emit("✅ Sucesso!")
            else:
                self.status_changed.emit(f"❌ Erro: {result.stderr[:100]}")
        except Exception as e:
            self.status_changed.emit(f"❌ Erro: {str(e)[:100]}")

class DevResetDialog(QDialog):
    """Dialog para dev resetar chaves"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔧 DEV - Resetar Chaves")
        self.setGeometry(100, 100, 500, 300)
        self.worker = None
        
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("🛠️ Ferramentas de Desenvolvimento")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Info
        info = QLabel("Limpe o banco de dados para testes")
        layout.addWidget(info)
        
        # Botões
        btn_layout = QVBoxLayout()
        
        # Botão 1: Limpar banco local
        btn1 = QPushButton("🗑️ Limpar BD Local")
        btn1.clicked.connect(self.limpar_local)
        btn_layout.addWidget(btn1)
        
        # Botão 2: Resetar tudo (local + VPS)
        btn2 = QPushButton("🔄 Resetar Tudo (Local + VPS)")
        btn2.clicked.connect(self.resetar_tudo)
        btn_layout.addWidget(btn2)
        
        # Status
        self.status_label = QLabel("✅ Pronto")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        btn_layout.addWidget(self.status_label)
        
        layout.addLayout(btn_layout)
        
        # Botão fechar
        btn_close = QPushButton("Fechar")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)
        
        self.setLayout(layout)
    
    def limpar_local(self):
        """Limpa banco de dados local"""
        try:
            import os
            db_path = os.path.expanduser('~/.smindeckbot/smindeckbot.db')
            
            if os.path.exists(db_path):
                os.remove(db_path)
                self.status_label.setText("✅ BD Local limpo!")
                self.status_label.setStyleSheet("color: green; font-weight: bold;")
                QMessageBox.information(self, "Sucesso", "Banco de dados local foi limpo!\n\nAproxime novamente.")
            else:
                self.status_label.setText("⚠️ BD não encontrado")
                self.status_label.setStyleSheet("color: orange; font-weight: bold;")
        except Exception as e:
            self.status_label.setText(f"❌ Erro: {str(e)[:50]}")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            QMessageBox.critical(self, "Erro", f"Erro ao limpar BD:\n{str(e)}")
    
    def resetar_tudo(self):
        """Reseta BD local e VPS"""
        reply = QMessageBox.warning(
            self,
            "⚠️ Confirmar Reset",
            "Isto vai limpar TUDO (local + VPS)!\n\nTem certeza?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # 1. Limpar local
                import os
                db_path = os.path.expanduser('~/.smindeckbot/smindeckbot.db')
                if os.path.exists(db_path):
                    os.remove(db_path)
                
                # 2. Limpar VPS via auto_vps
                self.status_label.setText("⏳ Conectando ao VPS...")
                self.status_label.setStyleSheet("color: orange; font-weight: bold;")
                self.update()
                
                from vps_config import VPS_CONFIG
                import paramiko
                
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(
                    VPS_CONFIG['host'],
                    port=VPS_CONFIG['port'],
                    username=VPS_CONFIG['user'],
                    password=VPS_CONFIG['password'],
                    timeout=10
                )
                
                # Executar limpeza no VPS
                self.status_label.setText("⏳ Limpando VPS...")
                self.update()
                
                cmd = """
                rm -f /root/.smindeckbot/smindeckbot.db 2>/dev/null
                mkdir -p /root/.smindeckbot
                echo 'Reset completo'
                """
                stdin, stdout, stderr = ssh.exec_command(cmd)
                stdout.read()
                ssh.close()
                
                self.status_label.setText("✅ Tudo resetado!")
                self.status_label.setStyleSheet("color: green; font-weight: bold;")
                QMessageBox.information(self, "Sucesso", "✅ Tudo foi resetado!\n\nLocal + VPS limpos")
                
            except Exception as e:
                self.status_label.setText(f"❌ Erro: {str(e)[:50]}")
                self.status_label.setStyleSheet("color: red; font-weight: bold;")
                QMessageBox.critical(self, "Erro", f"Erro ao resetar:\n{str(e)}")
