import sys
import os
import io

# Forçar UTF-8 no Windows para suportar emojis
if sys.platform == 'win32':
    if sys.stdout and hasattr(sys.stdout, 'buffer') and sys.stdout.buffer:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    if sys.stderr and hasattr(sys.stderr, 'buffer') and sys.stderr.buffer:
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from PyQt6.QtWidgets import QApplication
from deck_window import DeckWindow
from PyQt6.QtGui import QIcon
import ctypes
from theme import get_stylesheet
from beta_warning import BetaWarningDialog
from threading import Thread
from auto_updater import AutoUpdater, start_auto_update_daemon

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
    "com.smin.smindesk"
)

def resource_path(rel):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, rel)
    return os.path.join(os.path.abspath("."), rel)


app = QApplication(sys.argv)

# 🎨 Aplicar tema moderno global
app.setStyleSheet(get_stylesheet())

icon = QIcon(resource_path("logo-5.ico"))

# 🔴 ÍCONE GLOBAL (taskbar, Alt+Tab)
app.setWindowIcon(icon)

window = DeckWindow()

# 🔴 ÍCONE DA JANELA
window.setWindowIcon(icon)

window.resize(600, 400)

# 🔄 Iniciar daemon de auto-update em background (a cada 60s = 1 minuto para testes)
try:
    update_thread = Thread(target=start_auto_update_daemon, args=(60,), daemon=True)
    update_thread.start()
    print("✅ Daemon de auto-update iniciado (intervalo: 1 minuto)")
except Exception as e:
    print(f"⚠️ Erro ao iniciar auto-update: {e}")

window.show()

# ℹ️ Sincronização automática agora é feita pelo timer de 5 segundos em deck_window.py
# Não precisa mais sincronizar na inicialização - isso evita sobrescrever dados da memória

# 🚀 Mostrar dialog de aviso Beta (se não foi desativado anteriormente)
# Usar pasta de dados do usuário em vez do diretório da aplicação
import pathlib
user_data_dir = pathlib.Path.home() / "AppData" / "Local" / "SminDeck"
user_data_dir.mkdir(parents=True, exist_ok=True)
config_file = user_data_dir / "beta_warning.ini"

# Versão da aplicação
APP_VERSION = "0.1.2"

show_warning = True

if config_file.exists():
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            # Se contém "disabled" E a versão é a mesma, não mostra
            if content.startswith("disabled:"):
                saved_version = content.split(":")[1] if ":" in content else ""
                show_warning = saved_version != APP_VERSION
            else:
                show_warning = content.lower() != "disabled"
    except Exception:
        show_warning = True

if show_warning:
    warning_dialog = BetaWarningDialog(window)
    result = warning_dialog.exec()
    
    # Capturar o valor do checkbox ANTES de o dialog ser deletado
    dont_show = warning_dialog.should_not_show_again()
    
    if dont_show:
        # Salvar configuração com versão
        try:
            with open(config_file, "w", encoding="utf-8") as f:
                f.write(f"disabled:{APP_VERSION}")
        except Exception:
            pass

sys.exit(app.exec())

def main():
    app = QApplication(sys.argv)

    window = DeckWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
    


