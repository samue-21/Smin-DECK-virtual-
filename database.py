#!/usr/bin/env python3
"""
Gerenciador de banco de dados SQLite para SminDeck Bot + APP
Comunicação centralizada via banco de dados
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = os.path.expanduser('~/.smindeckbot/smindeckbot.db')

def init_database():
    """Inicializa o banco de dados com as tabelas necessárias"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    print(f"Inicializando banco de dados em: {DB_PATH}")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Tabela de chaves geradas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chaves (
                id INTEGER PRIMARY KEY,
                chave TEXT UNIQUE NOT NULL,
                user_id INTEGER,
                guild_id INTEGER,
                channel_id INTEGER,
                criada_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expira_em TIMESTAMP,
                status TEXT DEFAULT 'pendente'  -- pendente, ativa, expirada
            )
        ''')
        
        # Tabela de chaves autenticadas (ativas)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chaves_ativas (
                id INTEGER PRIMARY KEY,
                chave TEXT UNIQUE NOT NULL,
                user_id INTEGER,
                guild_id INTEGER,
                channel_id INTEGER,
                autenticada_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultima_sincronizacao TIMESTAMP,
                FOREIGN KEY (chave) REFERENCES chaves(chave)
            )
        ''')
        
        # Tabela de atualizações (arquivos modificados pelo Bot)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS atualizacoes (
                id INTEGER PRIMARY KEY,
                chave TEXT,
                tipo TEXT,  -- link, video, imagem, conteudo
                botao INTEGER,  -- qual botão foi atualizado (1-12)
                dados TEXT,  -- JSON com os dados
                criada_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tentativas INTEGER DEFAULT 0,  -- Contador de tentativas de download
                FOREIGN KEY (chave) REFERENCES chaves(chave)
            )
        ''')
        
        conn.commit()
        print(f"OK - Banco de dados inicializado com sucesso!")
        
    except Exception as e:
        print(f"ERRO ao inicializar banco: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

def criar_chave(user_id, guild_id, channel_id):
    """Cria nova chave no banco e AUTENTICA automaticamente
    
    IMPORTANTE: Se o usuário já tem uma chave ativa, retorna a existente
    (não cria duplicatas)
    """
    import random
    import string
    import logging
    
    log = logging.getLogger(__name__)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # [0] VERIFICAR SE JÁ EXISTE CHAVE ATIVA
        print(f"[VERIFICANDO] Procurando chave ativa para user_id={user_id}")
        cursor.execute('''
            SELECT chave FROM chaves_ativas WHERE user_id = ?
        ''', (user_id,))
        
        resultado = cursor.fetchone()
        if resultado:
            chave_existente = resultado[0]
            print(f"[REUTILIZANDO] Chave já ativa encontrada: {chave_existente}")
            log.info(f"[REUTILIZANDO] Chave já ativa para user {user_id}: {chave_existente}")
            conn.close()
            return chave_existente
        
        # [1] Se não tem chave ativa, procurar em chaves (talvez expirada)
        print(f"[CHECANDO] Procurando chave anterior (expirada?) para user_id={user_id}")
        cursor.execute('''
            SELECT chave, expira_em FROM chaves 
            WHERE user_id = ? 
            ORDER BY criada_em DESC 
            LIMIT 1
        ''', (user_id,))
        
        resultado_anterior = cursor.fetchone()
        
        # Se achou chave anterior, reativar (mesmo que expirada)
        if resultado_anterior:
            chave_anterior = resultado_anterior[0]
            print(f"[REATIVANDO] Encontrada chave anterior: {chave_anterior}")
            log.info(f"[REATIVANDO] Chave anterior encontrada para user {user_id}: {chave_anterior}")
            
            # [1.5] Deletar entrada antiga em chaves_ativas (se houver)
            cursor.execute('DELETE FROM chaves_ativas WHERE chave = ?', (chave_anterior,))
            
            # [2] Reativar em chaves_ativas
            cursor.execute('''
                INSERT INTO chaves_ativas (chave, user_id, guild_id, channel_id, autenticada_em)
                VALUES (?, ?, ?, ?, ?)
            ''', (chave_anterior, user_id, guild_id, channel_id, datetime.now().isoformat()))
            
            # [3] Atualizar a chave com novo timestamp de expiração
            novo_expira_em = (datetime.now() + timedelta(minutes=5)).isoformat()
            cursor.execute('''
                UPDATE chaves 
                SET expira_em = ?, status = 'ativa'
                WHERE chave = ?
            ''', (novo_expira_em, chave_anterior))
            
            conn.commit()
            print(f"[OK] Chave reativada: {chave_anterior}")
            log.info(f"[OK] Chave reativada e autenticada: {chave_anterior}")
            return chave_anterior
        
        # [4] Se REALMENTE não tem nenhuma chave, criar nova
        print(f"[CRIANDO] Nenhuma chave anterior encontrada. Criando nova...")
        chave = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        expira_em = datetime.now() + timedelta(minutes=5)
        
        print(f"[CRIANDO] Criando chave: {chave}")
        print(f"[BD] DB_PATH: {DB_PATH}")
        log.info(f"[CRIANDO] Criando chave: {chave} | DB: {DB_PATH}")
        
        # [5] Inserir na tabela chaves
        cursor.execute('''
            INSERT INTO chaves (chave, user_id, guild_id, channel_id, expira_em, status)
            VALUES (?, ?, ?, ?, ?, 'ativa')
        ''', (chave, user_id, guild_id, channel_id, expira_em.isoformat()))
        
        # [6] Automaticamente autenticar (inserir em chaves_ativas)
        cursor.execute('''
            INSERT INTO chaves_ativas (chave, user_id, guild_id, channel_id, autenticada_em)
            VALUES (?, ?, ?, ?, ?)
        ''', (chave, user_id, guild_id, channel_id, datetime.now().isoformat()))
        
        conn.commit()
        print(f"[OK] Chave criada E autenticada: {chave}")
        log.info(f"[OK] Chave criada E autenticada: {chave}")
        return chave
        
    except Exception as e:
        print(f"[ERRO] Erro ao criar chave: {e}")
        log.error(f"[ERRO] Erro ao criar chave: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        conn.close()

def validar_chave(chave, user_id, guild_id, channel_id):
    """Valida e ativa a chave"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Verificar se chave existe e não expirou
        cursor.execute('SELECT expira_em, status FROM chaves WHERE chave = ?', (chave,))
        resultado = cursor.fetchone()
        
        if not resultado:
            return False, "[ERRO] Chave inválida!"
        
        expira_em_str, status = resultado
        expira_em = datetime.fromisoformat(expira_em_str)
        
        if datetime.now() > expira_em:
            return False, "[ERRO] Chave expirada!"
        
        # Ativar chave
        cursor.execute('''
            INSERT INTO chaves_ativas (chave, user_id, guild_id, channel_id)
            VALUES (?, ?, ?, ?)
        ''', (chave, user_id, guild_id, channel_id))
        
        # Atualizar status na tabela de chaves
        cursor.execute('UPDATE chaves SET status = ? WHERE chave = ?', ('ativa', chave))
        
        conn.commit()
        return True, "[OK] Autenticado!"
        
    except Exception as e:
        print(f"[ERRO] Erro ao validar chave: {e}")
        return False, f"[ERRO] Erro: {e}"
    finally:
        conn.close()

def obter_info_chave(chave):
    """Obtém informações de uma chave"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT user_id, guild_id, channel_id FROM chaves WHERE chave = ?', (chave,))
        resultado = cursor.fetchone()
        
        if resultado:
            return {
                'user_id': resultado[0],
                'guild_id': resultado[1],
                'channel_id': resultado[2] }
        return None
    finally:
        conn.close()

def listar_chaves_ativas():
    """Lista todas as chaves ativas"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT chave, user_id, guild_id, channel_id FROM chaves_ativas')
        return [
            {
                'chave': row[0],
                'user_id': row[1],
                'guild_id': row[2],
                'channel_id': row[3] }
            for row in cursor.fetchall()
        ]
    finally:
        conn.close()

def usuario_esta_ativo(user_id):
    """Verifica se um usuario esta ativo (autenticado)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT COUNT(*) FROM chaves_ativas WHERE user_id = ?', (user_id,))
        count = cursor.fetchone()[0]
        return count > 0
    except Exception as e:
        print(f"[ERRO] Erro ao verificar usuario ativo: {e}")
        return False
    finally:
        conn.close()

def registrar_atualizacao(chave, tipo, botao, dados):
    """Registra uma atualização feita pelo Bot
    
    Regra de deduplicação: Se o mesmo botão/tipo já foi atualizado, 
    remove o arquivo antigo e apenas atualiza o nome no BD
    """
    print(f"\n[BANCO] Iniciando registrar_atualizacao()...")
    print(f"[BANCO] Chave: {chave[:20]}...")
    print(f"[BANCO] Tipo: {tipo}")
    print(f"[BANCO] Botão: {botao}")
    print(f"[BANCO] Dados: {dados}")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # [1] VERIFICAR SE JÁ EXISTE ATUALIZAÇÃO ANTERIOR DO MESMO BOTÃO/TIPO
        print(f"[BANCO] [1] Verificando se existe atualização anterior...")
        cursor.execute('''
            SELECT id, dados FROM atualizacoes 
            WHERE chave = ? AND tipo = ? AND botao = ?
            ORDER BY criada_em DESC
            LIMIT 1
        ''', (chave, tipo, botao))
        
        resultado_anterior = cursor.fetchone()
        print(f"[BANCO] [2] Resultado anterior: {resultado_anterior is not None}")
        
        if resultado_anterior:
            # Há uma atualização anterior do mesmo botão
            id_anterior, dados_anterior_json = resultado_anterior
            dados_anterior = json.loads(dados_anterior_json)
            print(f"[BANCO] [3] Removendo atualização anterior (ID: {id_anterior})...")
            
            # Se é arquivo (tem 'arquivo' ou 'conteudo'), remover o arquivo antigo
            if tipo in ['video', 'imagem', 'audio'] and 'arquivo' in dados_anterior:
                arquivo_antigo = dados_anterior.get('arquivo')
                if arquivo_antigo:
                    # Caminho do arquivo antigo
                    caminho_arquivo_antigo = os.path.join(
                        os.path.expanduser('~/.smindeckbot/arquivos'),
                        arquivo_antigo
                    )
                    try:
                        if os.path.exists(caminho_arquivo_antigo):
                            os.remove(caminho_arquivo_antigo)
                            print(f"[LIMPEZA] Arquivo antigo removido: {arquivo_antigo}")
                    except Exception as e:
                        print(f"[AVISO] Aviso ao remover arquivo antigo: {e}")
            
            # [2] DELETAR A ATUALIZAÇÃO ANTERIOR
            cursor.execute('DELETE FROM atualizacoes WHERE id = ?', (id_anterior,))
            print(f"[BANCO] [4] Atualização anterior deletada (ID: {id_anterior})")
        
        # [3] INSERIR A NOVA ATUALIZAÇÃO
        print(f"[BANCO] [5] Inserindo nova atualização...")
        cursor.execute('''
            INSERT INTO atualizacoes (chave, tipo, botao, dados)
            VALUES (?, ?, ?, ?)
        ''', (chave, tipo, botao, json.dumps(dados)))
        
        print(f"[BANCO] [6] Atualizando timestamp de sincronização...")
        # Atualizar timestamp de última sincronização
        cursor.execute(
            'UPDATE chaves_ativas SET ultima_sincronizacao = CURRENT_TIMESTAMP WHERE chave = ?',
            (chave,)
        )
        
        print(f"[BANCO] [7] Fazendo commit...")
        conn.commit()
        print(f"[BANCO] ✅ OK! Atualização registrada: Botão {botao} | Tipo: {tipo}")
    except Exception as e:
        print(f"[BANCO] ❌ ERRO ao registrar: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()
        print(f"[BANCO] Conexão fechada\n")

def obter_atualizacoes(desde=None):
    """Obtém atualizações desde um timestamp"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        if desde:
            cursor.execute('''
                SELECT id, chave, tipo, botao, dados, criada_em
                FROM atualizacoes
                WHERE criada_em > ?
                ORDER BY criada_em DESC
            ''', (desde,))
        else:
            cursor.execute('''
                SELECT id, chave, tipo, botao, dados, criada_em
                FROM atualizacoes
                ORDER BY criada_em DESC
            ''')
        
        return [
            {
                'id': row[0],
                'chave': row[1],
                'tipo': row[2],
                'botao': row[3],
                'dados': json.loads(row[4]),
                'criada_em': row[5] }
            for row in cursor.fetchall()
        ]
    finally:
        conn.close()

def deletar_atualizacao(atualizacao_id):
    """Deleta uma atualização pelo ID (após o app processar)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM atualizacoes WHERE id = ?', (atualizacao_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"[ERRO] Erro ao deletar atualização: {e}")
        return False
    finally:
        conn.close()

def incrementar_tentativa(atualizacao_id):
    """Incrementa contador de tentativas de download para uma atualização"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('UPDATE atualizacoes SET tentativas = tentativas + 1 WHERE id = ?', (atualizacao_id,))
        conn.commit()
        
        # Retornar o novo valor de tentativas
        cursor.execute('SELECT tentativas FROM atualizacoes WHERE id = ?', (atualizacao_id,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else 0
    except Exception as e:
        print(f"[ERRO] Falha ao incrementar tentativa: {e}")
        return 0
    finally:
        conn.close()

def obter_tentativas(atualizacao_id):
    """Obtém número de tentativas para uma atualização"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT tentativas FROM atualizacoes WHERE id = ?', (atualizacao_id,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else 0
    except Exception as e:
        print(f"[ERRO] Falha ao obter tentativas: {e}")
        return 0
    finally:
        conn.close()

def obter_atualizacoes_falhadas(max_tentativas=2):
    """Obtém atualizações que falharam no máximo de tentativas"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT id, chave, tipo, botao, dados, criada_em, tentativas
            FROM atualizacoes
            WHERE tentativas >= ?
            ORDER BY criada_em ASC
        ''', (max_tentativas,))
        
        return [
            {
                'id': row[0],
                'chave': row[1],
                'tipo': row[2],
                'botao': row[3],
                'dados': json.loads(row[4]),
                'criada_em': row[5],
                'tentativas': row[6] }
            for row in cursor.fetchall()
        ]
    finally:
        conn.close()

if __name__ == '__main__':
    init_database()
    print(f"[OK] Banco de dados inicializado em {DB_PATH}")
