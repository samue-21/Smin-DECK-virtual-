import os

APP_NAME = "SminDeck"


def get_app_data_path():
    """
    Retorna um diretório seguro para escrita:
    C:\\Users\\USER\\AppData\\Local\\SminDeck
    """
    base = os.getenv("LOCALAPPDATA") or os.getcwd()
    path = os.path.join(base, APP_NAME)
    os.makedirs(path, exist_ok=True)
    return path


# ========= ARQUIVOS DO APP =========

STARTUP_LOG = os.path.join(get_app_data_path(), "STARTUP_LOG.txt")

BG_TEXT_FILE = os.path.join(get_app_data_path(), "bg_text.txt")
BG_MODE_FILE = os.path.join(get_app_data_path(), "bg_mode.txt")
BG_LOOP_FILE = os.path.join(get_app_data_path(), "bg_loop.txt")
