# SminDeck Bot - Cliente Remoto
# Conecta ao Bot Discord rodando no VPS

import requests
import time
import json

# ============ CONFIGURAÇÃO ============
VPS_IP = "72.60.244.240"
VPS_API_PORT = 5000
VPS_API_URL = f"http://{VPS_IP}:{VPS_API_PORT}"

print(f"""
╔═══════════════════════════════════════════════════════╗
║     SMINDECK BOT - CLIENT REMOTO                      ║
║     Conectando ao VPS: {VPS_IP}:{VPS_API_PORT}         
║                                                       ║
╚═══════════════════════════════════════════════════════╝
""")

class BotClient:
    def __init__(self, api_url):
        self.api_url = api_url
        self.connected = False
    
    def health_check(self):
        """Verifica se o bot está online"""
        try:
            response = requests.get(f"{self.api_url}/api/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Bot online: {data.get('message')}")
                self.connected = True
                return True
        except Exception as e:
            print(f"✗ Erro: {e}")
        self.connected = False
        return False
    
    def get_urls(self, connection_key):
        """Obtém URLs para uma chave"""
        try:
            response = requests.get(
                f"{self.api_url}/api/deck/{connection_key}",
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"✗ Erro ao buscar URLs: {e}")
        return None
    
    def verify_key(self, connection_key):
        """Verifica se a chave é válida"""
        try:
            response = requests.get(
                f"{self.api_url}/api/verify/{connection_key}",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"✗ Erro ao verificar chave: {e}")
        return False

# Instância global
bot = BotClient(VPS_API_URL)

# ============ TESTES ============
if __name__ == "__main__":
    print("Testando conexão com bot remoto...")
    print("-" * 50)
    
    if bot.health_check():
        print("\n✓ Conexão estabelecida!")
        print("\nVocê pode usar 'bot.get_urls(connection_key)' para obter URLs")
        print("Exemplo:")
        print('  urls = bot.get_urls("ABC12345")')
        print('  print(urls)')
    else:
        print("\n✗ Não conseguiu conectar ao bot")
        print(f"  URL: {VPS_API_URL}")
        print("\n  Verifique se:")
        print(f"  - O VPS {VPS_IP} está online")
        print(f"  - O bot está rodando em http://{VPS_IP}:{VPS_API_PORT}")
