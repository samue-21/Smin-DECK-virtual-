#!/usr/bin/env python3
"""
Tela de carregamento com barra de progresso para sincronização do banco de dados
Exibida ao iniciar o APP
"""

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from database_client import DatabaseClient, sincronizar_banco_local
import time

class SyncThread(QThread):
    """Thread para sincronizar banco de dados em background"""
    
    progress = pyqtSignal(int, str)  # (progresso, mensagem)
    finished = pyqtSignal(bool)  # sucesso
    
    def __init__(self):
        super().__init__()
        self.client = DatabaseClient()
    
    def run(self):
        """Executa sincronização"""
        def callback(progresso, mensagem):
            self.progress.emit(progresso, mensagem)
            time.sleep(0.1)  # Pequeno delay para visualizar progresso
        
        # Verificar conexão
        self.progress.emit(10, "Verificando conexão...")
        if not self.client.health_check():
            self.progress.emit(0, "❌ Erro: API indisponível")
            self.finished.emit(False)
            return
        
        self.progress.emit(20, "Conectando ao banco de dados...")
        
        # Sincronizar
        sucesso = sincronizar_banco_local(self.client, callback)
        self.finished.emit(sucesso)

class LoadingDialog(QDialog):
    """Diálogo de carregamento com barra de progresso - Só aparece se há atualizações"""
    
    def __init__(self, parent=None, mostrar=True):
        super().__init__(parent)
        self.mostrar = mostrar
        
        if not mostrar:
            # Sem atualizações pendentes, não mostra nada
            self.accept()
            return
        
        self.setWindowTitle("SminDeck - Atualizando")
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a2e;
            }
            QLabel {
                color: #e0e0e0;
            }
            QProgressBar {
                border: 2px solid #16213e;
                border-radius: 5px;
                background-color: #0f3460;
                text-align: center;
                color: #00d4ff;
            }
            QProgressBar::chunk {
                background-color: #00d4ff;
                border-radius: 3px;
            }
        """)
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Título
        title = QLabel("Atualizando seu app...")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setFixedHeight(30)
        layout.addWidget(self.progress_bar)
        
        # Mensagem de status
        self.status_label = QLabel("Inicializando...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_font = QFont()
        status_font.setPointSize(10)
        self.status_label.setFont(status_font)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
        # Configurar tamanho
        self.setFixedSize(400, 200)
        
        # Iniciar sincronização
        self.sync_thread = SyncThread()
        self.sync_thread.progress.connect(self.update_progress)
        self.sync_thread.finished.connect(self.on_finished)
        self.sync_thread.start()
    
    def update_progress(self, valor, mensagem):
        """Atualiza barra de progresso"""
        self.progress_bar.setValue(valor)
        self.status_label.setText(mensagem)
    
    def on_finished(self, sucesso):
        """Callback quando sincronização termina"""
        if sucesso:
            self.progress_bar.setValue(100)
            self.status_label.setText("✅ Sincronização concluída!")
            self.accept()  # Fecha e continua
        else:
            self.status_label.setText("❌ Erro na sincronização")
            # Esperar 2 segundos e fechar mesmo assim (fallback)
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(2000, self.accept)

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    dialog = LoadingDialog()
    dialog.exec()
