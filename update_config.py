"""
Configuração de Endpoints para Auto-Update
Permite usar múltiplos servidores/VPS como backup
"""

import os
import json

# Configuração de Endpoints (em ordem de prioridade)
ENDPOINTS = {
    "primary": {
        "name": "VPS Principal",
        "api_url": "http://72.60.244.240:8000",
        "check_endpoint": "/api/updates/check",
        "download_base": "/download",
        "active": False  # Desativar por enquanto
    },
    "bot_vps": {
        "name": "VPS do Bot",
        "api_url": "http://72.60.244.240:8000",
        "check_endpoint": "/api/updates/check",
        "download_base": "/download",
        "active": True  # ✅ ATIVO
    },
    "github": {
        "name": "GitHub Releases",
        "api_url": "https://api.github.com/repos/seu-usuario/smin-deck/releases",
        "check_endpoint": "/latest",
        "download_base": "/assets",
        "active": True  # Usar como fallback
    },
    "local": {
        "name": "Servidor Local",
        "api_url": "http://localhost:8000",
        "check_endpoint": "/api/updates/check",
        "download_base": "/download",
        "active": False  # Para testes locais
    }
}

# Salvar configuração
CONFIG_FILE = "update_endpoints.json"

def save_config():
    """Salva configuração de endpoints"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(ENDPOINTS, f, indent=2, ensure_ascii=False)
    print(f"✅ Configuração salva em {CONFIG_FILE}")

def load_config():
    """Carrega configuração de endpoints"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return ENDPOINTS

def get_active_endpoints():
    """Retorna lista de endpoints ativos em ordem de prioridade"""
    config = load_config()
    active = []
    
    # Ordem de prioridade
    priority_order = ["primary", "bot_vps", "local", "github"]
    
    for key in priority_order:
        if key in config and config[key].get("active"):
            active.append((key, config[key]))
    
    return active

if __name__ == "__main__":
    save_config()
    print("\n📋 Endpoints configurados:")
    for key, ep in ENDPOINTS.items():
        status = "✅ ATIVO" if ep.get("active") else "❌ INATIVO"
        print(f"  [{key}] {ep['name']} - {ep['api_url']} {status}")
