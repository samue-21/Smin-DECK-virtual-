"""
Ponto de entrada alternativo para o SminDeck
"""
import sys
import os

def main():
    """Executa o SminDeck"""
    try:
        # Importar e executar o main original
        from main import app, window
        
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Erro ao iniciar SminDeck: {e}")
        import traceback
        traceback.print_exc()
        
        # Tentar mostrar em dialog
        try:
            from PyQt6.QtWidgets import QMessageBox, QApplication
            app = QApplication([])
            QMessageBox.critical(None, "Erro ao Iniciar", f"Erro: {str(e)}")
        except:
            pass
        
        sys.exit(1)

if __name__ == '__main__':
    main()
