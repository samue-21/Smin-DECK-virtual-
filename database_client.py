#!/usr/bin/env python3
"""
Cliente do banco de dados para o APP
Conecta com a API REST na VPS para sincronizar dados
"""

import requests
import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

# Local do banco de dados do APP
LOCAL_DB = os.path.expanduser('~/.smindeckbot/smindeckbot.db')

class DatabaseClient:
    """Cliente para comunicação com API do banco de dados"""
    
    def __init__(self, api_url='http://72.60.244.240:5001'):
        self.api_url = api_url
        self.timeout = 10
    
    def health_check(self):
        """Verifica se a API está online"""
        try:
            resp = requests.get(f'{self.api_url}/api/health', timeout=self.timeout)
            return resp.status_code == 200
        except Exception as e:
            print(f"❌ Erro ao conectar com API: {e}")
            return False
    
    def criar_chave(self, user_id, guild_id, channel_id):
        """Cria uma nova chave no banco de dados remoto"""
        try:
            data = {
                'user_id': user_id,
                'guild_id': guild_id,
                'channel_id': channel_id
            }
            resp = requests.post(
                f'{self.api_url}/api/chave/criar',
                json=data,
                timeout=self.timeout
            )
            if resp.status_code == 200:
                return resp.json().get('chave')
            return None
        except Exception as e:
            print(f"❌ Erro ao criar chave: {e}")
            return None
    
    def validar_chave(self, chave, user_id, guild_id, channel_id):
        """Valida uma chave no banco de dados remoto"""
        try:
            data = {
                'chave': chave.upper(),
                'user_id': user_id,
                'guild_id': guild_id,
                'channel_id': channel_id
            }
            resp = requests.post(
                f'{self.api_url}/api/chave/validar',
                json=data,
                timeout=self.timeout
            )
            if resp.status_code == 200:
                result = resp.json()
                return result.get('sucesso', False), result.get('msg', '')
            return False, resp.json().get('error', 'Erro desconhecido')
        except Exception as e:
            print(f"❌ Erro ao validar chave: {e}")
            return False, str(e)
    
    def obter_info_chave(self, chave):
        """Obtém informações de uma chave"""
        try:
            resp = requests.get(
                f'{self.api_url}/api/chave/info/{chave.upper()}',
                timeout=self.timeout
            )
            if resp.status_code == 200:
                return resp.json()
            return None
        except Exception as e:
            print(f"❌ Erro ao obter info da chave: {e}")
            return None
    
    def listar_chaves_ativas(self):
        """Lista todas as chaves ativas"""
        try:
            resp = requests.get(
                f'{self.api_url}/api/chaves/ativas',
                timeout=self.timeout
            )
            if resp.status_code == 200:
                return resp.json().get('chaves', [])
            return []
        except Exception as e:
            print(f"❌ Erro ao listar chaves ativas: {e}")
            return []
    
    def registrar_atualizacao(self, chave, tipo, botao, dados):
        """Registra uma atualização do Bot"""
        try:
            data = {
                'chave': chave,
                'tipo': tipo,
                'botao': botao,
                'dados': dados
            }
            resp = requests.post(
                f'{self.api_url}/api/atualizacao/registrar',
                json=data,
                timeout=self.timeout
            )
            return resp.status_code == 200
        except Exception as e:
            print(f"❌ Erro ao registrar atualização: {e}")
            return False
    
    def obter_atualizacoes(self, desde=None):
        """Obtém atualizações desde um timestamp"""
        try:
            headers = {'X-Desde': desde} if desde else {}
            resp = requests.get(
                f'{self.api_url}/api/atualizacoes',
                headers=headers,
                timeout=self.timeout
            )
            if resp.status_code == 200:
                return resp.json().get('atualizacoes', [])
            return []
        except Exception as e:
            print(f"❌ Erro ao obter atualizações: {e}")
            return []
    
    def tem_atualizacoes_pendentes(self):
        """Verifica se há atualizações pendentes"""
        try:
            atualizacoes = self.obter_atualizacoes()
            return len(atualizacoes) > 0
        except Exception as e:
            print(f"❌ Erro ao verificar atualizações: {e}")
            return False

def sincronizar_banco_local(client, callback=None):
    """
    Sincroniza o banco de dados local com as atualizações da API
    callback(progresso) - callback para atualizar barra de progresso
    """
    try:
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(LOCAL_DB), exist_ok=True)
        
        # Obter último timestamp de sincronização
        conn = sqlite3.connect(LOCAL_DB)
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT ultimo_timestamp FROM sincronizacao ORDER BY id DESC LIMIT 1')
            row = cursor.fetchone()
            desde = row[0] if row else None
        except:
            desde = None
        
        if callback:
            callback(25, "Conectando ao banco remoto...")
        
        # Obter atualizações
        atualizacoes = client.obter_atualizacoes(desde)
        total_atualizacoes = len(atualizacoes)
        
        if callback:
            callback(50, f"Processando {total_atualizacoes} atualizações...")
        
        # Processar atualizações (implementar conforme necessário)
        for i, atualizacao in enumerate(atualizacoes):
            # Salvar ou processar atualizacao
            progresso = 50 + int((i / max(total_atualizacoes, 1)) * 40)
            if callback:
                callback(progresso, f"Sincronizando... {i+1}/{total_atualizacoes}")
        
        # Registrar sincronização
        agora = datetime.now().isoformat()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sincronizacao (
                    id INTEGER PRIMARY KEY,
                    ultimo_timestamp TEXT,
                    data_sincronizacao TEXT
                )
            ''')
            cursor.execute(
                'INSERT INTO sincronizacao (ultimo_timestamp, data_sincronizacao) VALUES (?, ?)',
                (agora, agora)
            )
            conn.commit()
        except:
            pass
        
        if callback:
            callback(100, "Sincronização concluída!")
        
        conn.close()
        return True
    
    except Exception as e:
        print(f"❌ Erro na sincronização: {e}")
        if callback:
            callback(0, f"Erro: {str(e)}")
        return False

if __name__ == '__main__':
    client = DatabaseClient()
    print("Testando conexão...")
    if client.health_check():
        print("✅ API está online!")
    else:
        print("❌ API offline")
