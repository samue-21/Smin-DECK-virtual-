#!/usr/bin/env python3
"""
Setup interativo para configurar o token do Discord Bot.
Interface gráfica PyQt6.
"""

import os
import sys
from pathlib import Path

try:
    from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
    from PyQt6.QtCore import Qt
except ImportError:
    print("Erro: PyQt6 não instalado")
    sys.exit(1)


class TokenSetupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.env_file = Path.cwd() / ".env"
        self.token = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Configuração do Token Discord")
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("🤖 Configurar Token do Discord Bot")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)
        
        # Instruções
        instructions = QLabel(
            "1. Acesse: https://discord.com/developers/applications\n"
            "2. Clique em 'New Application'\n"
            "3. Vá para 'Bot' → 'Add Bot'\n"
            "4. Clique em 'Copy' embaixo de TOKEN\n"
            "5. Cole seu token abaixo:"
        )
        instructions.setStyleSheet("margin: 10px; white-space: pre-wrap;")
        layout.addWidget(instructions)
        
        # Campo de entrada
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Cole seu DISCORD_TOKEN aqui...")
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.token_input)
        
        # Botão confirmar
        confirm_btn = QPushButton("Confirmar e Salvar Token")
        confirm_btn.clicked.connect(self.save_token)
        layout.addWidget(confirm_btn)
        
        # Botão cancelar
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)
        
        self.setLayout(layout)
    
    def save_token(self):
        """Salva o token no arquivo .env"""
        token = self.token_input.text().strip()
        
        if not token:
            QMessageBox.warning(self, "Erro", "Token não pode estar vazio!")
            return
        
        if len(token) < 20:
            QMessageBox.warning(self, "Aviso", "Token parece muito curto.\nVerifique se copiou corretamente.")
            return
        
        try:
            # Ler .env existente
            lines = []
            if self.env_file.exists():
                with open(self.env_file, 'r', encoding='utf-8') as f:
                    lines = [line.rstrip('\n') for line in f if not line.startswith('DISCORD_TOKEN=')]
            
            # Adicionar novo token
            lines.append(f"DISCORD_TOKEN={token}")
            
            # Salvar
            with open(self.env_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines) + '\n')
            
            self.token = token
            QMessageBox.information(
                self, 
                "Sucesso", 
                f"✅ Token configurado com sucesso!\n\nArquivo: {self.env_file}"
            )
            self.accept()
        
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar .env:\n{e}")


def main():
    """Executa a interface gráfica"""
    app = QApplication(sys.argv)
    dialog = TokenSetupDialog()
    dialog.show()
    sys.exit(app.exec())
        return False


if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n❌ Setup falhou. Tente novamente.")
        sys.exit(1)
    
    print("\n🎉 Pronto! Você pode iniciar o bot agora.\n")
    sys.exit(0)
