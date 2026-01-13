import sqlite3
import uuid
from datetime import datetime
import os
from pathlib import Path


def _data_dir() -> Path:
    """Retorna uma pasta gravável para dados do bot.

    Evita gravar em Program Files (sem permissão) quando instalado via setup.
    Pode ser sobrescrito com SMINDECK_BOT_DATA_DIR.
    """
    override = (os.environ.get("SMINDECK_BOT_DATA_DIR") or "").strip()
    if override:
        return Path(override).expanduser()

    appdata = (os.environ.get("APPDATA") or "").strip()
    if appdata:
        return Path(appdata) / "SminDeckBot"

    return Path.home() / ".smindeckbot"


DATA_DIR = _data_dir()
DB_FILE = str(DATA_DIR / "smindeck_bot.db")


def _connect() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_FILE)


def init_db():
    """Inicializa o banco de dados"""
    conn = _connect()
    cursor = conn.cursor()

    # Tabela de chaves de conexão
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS connection_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server_id TEXT UNIQUE NOT NULL,
            connection_key TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabela de URLs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            connection_key TEXT NOT NULL,
            button_number INTEGER NOT NULL,
            url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (connection_key) REFERENCES connection_keys(connection_key),
            UNIQUE(connection_key, button_number)
        )
    """)

    # Configurações por servidor (UX mais simples)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS server_settings (
            server_id TEXT PRIMARY KEY,
            default_button INTEGER NOT NULL DEFAULT 1,
            channel_id TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Migração leve: adicionar coluna channel_id se a tabela já existia
    try:
        cursor.execute("ALTER TABLE server_settings ADD COLUMN channel_id TEXT")
    except sqlite3.OperationalError:
        # Coluna já existe (ou tabela recém criada)
        pass

    conn.commit()
    conn.close()


def set_default_button(server_id: str, button_number: int):
    """Define o botão padrão (1-12) para o servidor."""
    if not (1 <= button_number <= 12):
        return False, "Número do botão deve estar entre 1 e 12"

    conn = _connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO server_settings (server_id, default_button, updated_at)
               VALUES (?, ?, CURRENT_TIMESTAMP)
               ON CONFLICT(server_id)
               DO UPDATE SET default_button=?, updated_at=CURRENT_TIMESTAMP""",
            (server_id, button_number, button_number),
        )
        conn.commit()
        return True, "OK"
    except sqlite3.Error as e:
        return False, str(e)
    finally:
        conn.close()


def get_default_button(server_id: str) -> int:
    """Obtém o botão padrão do servidor. Se não existir, retorna 1."""
    conn = _connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT default_button FROM server_settings WHERE server_id = ?",
            (server_id,),
        )
        row = cursor.fetchone()
        if row and isinstance(row[0], int):
            return row[0]
        return 1
    finally:
        conn.close()


def get_default_button_optional(server_id: str):
    """Obtém o botão padrão do servidor. Se não existir, retorna None."""
    conn = _connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT default_button FROM server_settings WHERE server_id = ?",
            (server_id,),
        )
        row = cursor.fetchone()
        if row and isinstance(row[0], int):
            return row[0]
        return None
    finally:
        conn.close()


def set_bot_channel(server_id: str, channel_id: str):
    """Define o canal dedicado (texto) onde o bot aceitará mensagens tipo 'ola'."""
    conn = _connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO server_settings (server_id, channel_id, updated_at)
               VALUES (?, ?, CURRENT_TIMESTAMP)
               ON CONFLICT(server_id)
               DO UPDATE SET channel_id=?, updated_at=CURRENT_TIMESTAMP""",
            (server_id, str(channel_id), str(channel_id)),
        )
        conn.commit()
        return True, "OK"
    except sqlite3.Error as e:
        return False, str(e)
    finally:
        conn.close()


def get_bot_channel(server_id: str):
    """Retorna channel_id do canal dedicado ou None."""
    conn = _connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT channel_id FROM server_settings WHERE server_id = ?",
            (server_id,),
        )
        row = cursor.fetchone()
        if row and row[0]:
            return str(row[0])
        return None
    finally:
        conn.close()


def generate_connection_key():
    """Gera uma chave de conexão única"""
    return str(uuid.uuid4())[:8].upper()


def create_connection_key(server_id):
    """Cria uma nova chave de conexão para um servidor"""
    conn = _connect()
    cursor = conn.cursor()

    # Verificar se já existe
    cursor.execute("SELECT connection_key FROM connection_keys WHERE server_id = ?", (server_id,))
    result = cursor.fetchone()

    if result:
        conn.close()
        return result[0]

    # Criar nova
    key = generate_connection_key()
    try:
        cursor.execute(
            "INSERT INTO connection_keys (server_id, connection_key) VALUES (?, ?)",
            (server_id, key)
        )
        conn.commit()
        conn.close()
        return key
    except sqlite3.IntegrityError:
        conn.close()
        return create_connection_key(server_id)  # Retentar com nova chave


def get_connection_key(server_id):
    """Obtém a chave de um servidor"""
    conn = _connect()
    cursor = conn.cursor()
    cursor.execute("SELECT connection_key FROM connection_keys WHERE server_id = ?", (server_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def update_url(connection_key, button_number, url):
    """Atualiza ou insere uma URL"""
    conn = _connect()
    cursor = conn.cursor()

    # Validar chave
    cursor.execute("SELECT id FROM connection_keys WHERE connection_key = ?", (connection_key,))
    if not cursor.fetchone():
        conn.close()
        return False, "Chave de conexão inválida"

    # Validar número do botão
    if not (1 <= button_number <= 12):
        conn.close()
        return False, "Número do botão deve estar entre 1 e 12"

    try:
        cursor.execute(
            """INSERT INTO urls (connection_key, button_number, url, updated_at)
               VALUES (?, ?, ?, CURRENT_TIMESTAMP)
               ON CONFLICT(connection_key, button_number)
               DO UPDATE SET url=?, updated_at=CURRENT_TIMESTAMP""",
            (connection_key, button_number, url, url)
        )
        conn.commit()
        conn.close()
        return True, "URL atualizada com sucesso!"
    except sqlite3.Error as e:
        conn.close()
        return False, f"Erro: {str(e)}"


def get_urls(connection_key):
    """Obtém todas as URLs de uma chave de conexão"""
    conn = _connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT button_number, url FROM urls WHERE connection_key = ? ORDER BY button_number",
        (connection_key,)
    )
    results = cursor.fetchall()
    conn.close()

    return {button: url for button, url in results}


def get_url(connection_key, button_number):
    """Obtém a URL de um botão específico"""
    conn = _connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT url FROM urls WHERE connection_key = ? AND button_number = ?",
        (connection_key, button_number)
    )
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def delete_url(connection_key, button_number):
    """Deleta a URL de um botão"""
    conn = _connect()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM urls WHERE connection_key = ? AND button_number = ?",
        (connection_key, button_number)
    )
    conn.commit()
    conn.close()
    return True


if __name__ == "__main__":
    init_db()
    print(" Banco de dados inicializado!")
    print(f" DB: {DB_FILE}")
