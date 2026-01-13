# Discord OAuth2 - Fluxo de autenticação automática

import requests
import webbrowser
import json
from urllib.parse import urlencode

# Configurações do Discord OAuth
DISCORD_CLIENT_ID = "YOUR_CLIENT_ID"  # Será substituído
DISCORD_REDIRECT_URI = "http://localhost:5000/discord/callback"
DISCORD_SCOPES = ["identify", "guilds"]

class DiscordOAuth:
    """Gerencia autenticação com Discord via OAuth2"""
    
    def __init__(self, vps_url="http://72.60.244.240:5000"):
        self.vps_url = vps_url
        self.auth_state = None
    
    def get_discord_login_url(self):
        """Retorna URL de login do Discord"""
        params = {
            "client_id": DISCORD_CLIENT_ID,
            "redirect_uri": DISCORD_REDIRECT_URI,
            "response_type": "code",
            "scope": " ".join(DISCORD_SCOPES),
            "state": "sminbot_login"
        }
        base_url = "https://discord.com/api/oauth2/authorize"
        return f"{base_url}?{urlencode(params)}"
    
    def open_discord_login(self):
        """Abre navegador para fazer login no Discord"""
        url = self.get_discord_login_url()
        webbrowser.open(url)
        return True
    
    def wait_for_callback(self, timeout=60):
        """Aguarda callback do Discord com código de autorização"""
        # Isso seria implementado como um local HTTP server
        # Por enquanto, cliente copia o código da URL de redirecionamento
        pass
    
    def exchange_code_for_token(self, code):
        """Troca código de autorização por token de acesso"""
        try:
            response = requests.post(
                f"{self.vps_url}/api/discord/exchange_token",
                json={"code": code},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return True, data.get("access_token")
            else:
                return False, "Falha ao trocar código"
        except Exception as e:
            return False, str(e)
    
    def get_user_info(self, access_token):
        """Pega informações do usuário Discord"""
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(
                "https://discord.com/api/users/@me",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, "Falha ao pegar info do usuário"
        except Exception as e:
            return False, str(e)
    
    def get_user_guilds(self, access_token):
        """Pega servidores do usuário"""
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(
                "https://discord.com/api/users/@me/guilds",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, "Falha ao pegar servidores"
        except Exception as e:
            return False, str(e)
    
    def generate_connection_key(self):
        """Gera uma chave de conexão após autenticação bem-sucedida"""
        try:
            response = requests.post(
                f"{self.vps_url}/api/discord/generate_key",
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return True, data.get("key")
            else:
                return False, "Falha ao gerar chave"
        except Exception as e:
            return False, str(e)


# Fluxo simplificado para o cliente
def login_discord_flow():
    """Fluxo completo de login via Discord"""
    oauth = DiscordOAuth()
    
    # 1. Abre navegador para login
    oauth.open_discord_login()
    
    # 2. Cliente é redirecionado para Discord
    # 3. Faz login/cria conta
    # 4. Confirma adição do bot
    # 5. VPS bot detecta o novo servidor
    # 6. VPS cria a sala automaticamente
    # 7. Cliente recebe chave
    # 8. Retorna a chave para o app
    
    return True  # Simplificado por enquanto


if __name__ == "__main__":
    print("Este módulo é para uso interno no app")
