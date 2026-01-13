# Configuração de conexão com o Bot Discord no VPS
# Este arquivo substitui a lógica local do bot

VPS_IP = "72.60.244.240"
VPS_API_PORT = 5000
VPS_API_URL = f"http://{VPS_IP}:{VPS_API_PORT}"

# Usar HTTPS em produção!
# VPS_API_URL = f"https://seu_dominio.com"

class BotClient:
    """Cliente para comunicar com o Bot Discord no VPS"""
    
    def __init__(self):
        import requests
        self.requests = requests
        self.base_url = VPS_API_URL
    
    def health_check(self):
        """Verifica se o bot está online"""
        try:
            response = self.requests.get(f"{self.base_url}/api/health", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Erro ao conectar ao bot: {e}")
            return False
    
    def get_urls(self, connection_key):
        """Obtém todas as URLs cadastradas"""
        try:
            response = self.requests.get(
                f"{self.base_url}/api/deck/{connection_key}",
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"❌ Erro ao buscar URLs: {e}")
            return None
    
    def verify_key(self, connection_key):
        """Verifica se uma chave é válida"""
        try:
            response = self.requests.get(
                f"{self.base_url}/api/verify/{connection_key}",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Erro ao verificar chave: {e}")
            return False


# Instância global
bot = BotClient()

if __name__ == "__main__":
    # Testar conexão
    if bot.health_check():
        print("✓ Bot está online no VPS!")
    else:
        print("✗ Bot não está respondendo")
