# Bot Connector - Gerencia conexão automaticamente com o bot remoto

import requests
import json
import os
from pathlib import Path

VPS_API_URL = "http://72.60.244.240:5000"

class BotConnector:
    """Gerenciador de conexão com Bot Discord remoto"""
    
    def __init__(self):
        self.api_url = VPS_API_URL
        self.keys_file = Path.home() / ".smindeckbot" / "keys.json"
        self.keys_file.parent.mkdir(parents=True, exist_ok=True)
        self.load_keys()
    
    def load_keys(self):
        """Carrega chaves salvas"""
        try:
            if self.keys_file.exists():
                with open(self.keys_file, 'r') as f:
                    self.keys = json.load(f)
            else:
                self.keys = {}
        except:
            self.keys = {}
    
    def save_keys(self):
        """Salva chaves localmente"""
        with open(self.keys_file, 'w') as f:
            json.dump(self.keys, f, indent=2)
    
    def health_check(self):
        """Verifica se bot está online"""
        try:
            response = requests.get(f"{self.api_url}/api/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def add_key(self, connection_key, server_name="SminDeck"):
        """
        Adiciona uma chave e faz handshake com bot
        Retorna: (sucesso: bool, mensagem: str)
        """
        connection_key = connection_key.strip().upper()
        
        # 1. Verificar health
        if not self.health_check():
            return False, "❌ Bot não está respondendo"
        
        # 2. Validar chave
        try:
            response = requests.get(
                f"{self.api_url}/api/verify/{connection_key}",
                timeout=5
            )
            if response.status_code != 200:
                return False, f"❌ Chave '{connection_key}' inválida"
        except Exception as e:
            return False, f"❌ Erro ao validar chave: {e}"
        
        # 3. Tentar buscar URLs (confirma que chave funciona)
        try:
            response = requests.get(
                f"{self.api_url}/api/deck/{connection_key}",
                timeout=5
            )
            urls = response.json().get("urls", {})
        except Exception as e:
            return False, f"❌ Erro ao buscar dados: {e}"
        
        # 4. Salvar chave
        self.keys[connection_key] = {
            "name": server_name,
            "connected": True,
            "urls": urls,
            "added_at": str(Path(__file__))
        }
        self.save_keys()
        
        # 5. Sucesso!
        return True, f"✓ Conectado com sucesso!"
    
    def get_urls(self, connection_key):
        """Obtém URLs para uma chave"""
        connection_key = connection_key.strip().upper()
        
        try:
            response = requests.get(
                f"{self.api_url}/api/deck/{connection_key}",
                timeout=5
            )
            if response.status_code == 200:
                return response.json().get("urls", {})
        except:
            pass
        
        return None
    
    def list_keys(self):
        """Lista todas as chaves conectadas"""
        return self.keys
    
    def remove_key(self, connection_key):
        """Remove uma chave"""
        connection_key = connection_key.strip().upper()
        if connection_key in self.keys:
            del self.keys[connection_key]
            self.save_keys()
            return True
        return False


# Instância global
connector = BotConnector()

if __name__ == "__main__":
    print("🤖 Bot Connector Test")
    print("=" * 50)
    
    # Verificar conexão
    if connector.health_check():
        print("✓ Bot está online!")
        
        # Testar com chave de exemplo
        chave_teste = "ABC12345"
        success, msg = connector.add_key(chave_teste)
        print(f"Teste: {msg}")
    else:
        print("✗ Bot está offline")
