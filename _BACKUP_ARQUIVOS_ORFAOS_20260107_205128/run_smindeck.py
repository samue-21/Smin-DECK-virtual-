#!/usr/bin/env python
"""
SminDeck Launcher - Instala deps e roda
"""
import sys
import subprocess
import os

def install_missing_deps():
    """Instala apenas as dependências faltantes"""
    deps = ['requests', 'Pillow']
    for dep in deps:
        try:
            __import__(dep if dep != 'Pillow' else 'PIL')
            print(f"✓ {dep} OK")
        except:
            print(f"Instalando {dep}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', dep])

# Instalar deps
print("Verificando dependências...")
install_missing_deps()

# Rodar app
print("\nIniciando SminDeck...")
print("=" * 50)

if __name__ == '__main__':
    try:
        from PyQt6.QtWidgets import QApplication
        from deck_window import DeckWindow
        from PyQt6.QtGui import QIcon
        import ctypes
        from theme import get_stylesheet
        from beta_warning import BetaWarningDialog
        
        def resource_path(rel):
            if hasattr(sys, "_MEIPASS"):
                return os.path.join(sys._MEIPASS, rel)
            return os.path.join(os.path.abspath("."), rel)
        
        app = QApplication(sys.argv)
        app.setStyleSheet(get_stylesheet())
        
        icon = QIcon(resource_path("logo-5.ico"))
        app.setWindowIcon(icon)
        
        window = DeckWindow()
        window.setWindowIcon(icon)
        window.resize(600, 400)
        window.show()
        
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("com.smin.smindesk")
        
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
