"""
Dialog de aviso para versão Beta da aplicação
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QCheckBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from theme import get_stylesheet


class BetaWarningDialog(QDialog):
    """Dialog informando que a aplicação está em versão de teste"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("⚠️ Aviso - Versão Beta")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        
        # Armazenar o estado do checkbox ANTES de deletar
        self.checkbox_state = False
        
        # Aplicar stylesheet
        self.setStyleSheet(get_stylesheet())
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # ===============================
        # TÍTULO
        # ===============================
        title = QLabel("⚠️ VERSÃO BETA - AVISO IMPORTANTE")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #ff9800;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # ===============================
        # SEPARADOR
        # ===============================
        sep = QLabel("")
        sep.setStyleSheet("border-bottom: 2px solid #ff9800;")
        sep.setFixedHeight(2)
        layout.addWidget(sep)
        
        # ===============================
        # MENSAGEM PRINCIPAL
        # ===============================
        msg = QLabel(
            "Esta aplicação está em fase de desenvolvimento (Build Beta).\n\n"
            "🔍 Status: Teste e Validação\n"
            "⚠️ Aviso: Podem ocorrer erros, bugs ou falhas inesperadas\n"
            "💥 Risco: A aplicação pode fechar abruptamente\n\n"
            "Agradecemos sua paciência e compreensão durante este período "
            "de testes. Se encontrar qualquer problema, anomalia ou comportamento "
            "inesperado, por favor reporte ao desenvolvedor informando:\n\n"
            "  • O que estava fazendo quando o erro ocorreu\n"
            "  • Qual foi a mensagem de erro (se houver)\n"
            "  • Como reproduzir o problema (se possível)\n"
            "  • Screenshots ou vídeo do problema (se aplicável)\n\n"
            "Seu feedback é fundamental para melhorar a aplicação! 🙏"
        )
        msg.setFont(QFont("Segoe UI", 10))
        msg.setWordWrap(True)
        msg.setStyleSheet("color: #e0e0e0; line-height: 1.6;")
        msg.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(msg)
        
        # ===============================
        # CHECKBOX - NÃO MOSTRAR NOVAMENTE
        # ===============================
        self.dont_show_again = QCheckBox("Não mostrar este aviso novamente")
        self.dont_show_again.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.dont_show_again)
        
        # ===============================
        # BOTÃO OK
        # ===============================
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_ok = QPushButton("✓ Entendi e Aceito")
        btn_ok.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        btn_ok.setFixedSize(220, 40)
        btn_ok.setObjectName("okBtn")
        btn_ok.clicked.connect(self.accept_dialog)
        
        btn_layout.addWidget(btn_ok)
        layout.addLayout(btn_layout)
        
        # Aplicar estilo customizado
        self.apply_custom_style()
    
    def accept_dialog(self):
        """Salvar estado do checkbox antes de fechar"""
        self.checkbox_state = self.dont_show_again.isChecked()
        self.accept()
    
    def apply_custom_style(self):
        """Aplicar estilos customizados para o dialog de aviso"""
        additional_style = """
            QDialog {
                background-color: #1e1e2e;
                border: 2px solid #ff9800;
                border-radius: 8px;
            }
            
            QLabel {
                color: #ffffff;
            }
            
            QCheckBox {
                color: #ffffff;
                spacing: 8px;
                padding: 8px;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 3px;
                border: 2px solid #ff9800;
                background-color: #2a2a3e;
            }
            
            QCheckBox::indicator:hover {
                border: 2px solid #ffb84d;
                background-color: #3a3a4e;
            }
            
            QCheckBox::indicator:checked {
                background-color: #ff9800;
                border: 2px solid #ff9800;
            }
            
            QPushButton#okBtn {
                background-color: #ff9800;
                border: 2px solid #e68900;
                color: #ffffff;
                font-weight: bold;
                border-radius: 6px;
            }
            
            QPushButton#okBtn:hover {
                background-color: #ffb84d;
                border: 2px solid #ff9800;
            }
            
            QPushButton#okBtn:pressed {
                background-color: #e68900;
            }
        """
        current_style = self.styleSheet()
        self.setStyleSheet(current_style + additional_style)
    
    def should_not_show_again(self):
        """Retorna True se o usuário marcou para não mostrar novamente"""
        return self.checkbox_state
