#!/usr/bin/env python3
"""
Script para notificar o Bot que uma chave foi autenticada no APP
Uso: python notify_bot.py <bot_ip> <user_id> <guild_id> <channel_id>
Exemplo: python notify_bot.py 72.60.244.240 123456 789012 345678
"""

import sys
import requests
import asyncio

def notify_bot(bot_ip, user_id, guild_id, channel_id):
    """Envia webhook ao Bot para notificar autenticação"""
    try:
        url = f'http://{bot_ip}:5000/auth_webhook'
        payload = {
            'user_id': int(user_id),
            'guild_id': int(guild_id),
            'channel_id': int(channel_id)
        }
        
        response = requests.post(url, json=payload, timeout=5)
        
        if response.status_code == 200:
            print("✓ Bot notificado com sucesso!")
            return True
        else:
            print(f"⚠️ Erro ao notificar Bot: {response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️ Não foi possível notificar o Bot: {e}")
        print("(O APP foi autenticado, mas o Bot pode não ter recebido a notificação)")
        return True  # Não falhar

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Uso: python notify_bot.py <bot_ip> <user_id> <guild_id> <channel_id>")
        sys.exit(1)
    
    bot_ip = sys.argv[1]
    user_id = sys.argv[2]
    guild_id = sys.argv[3]
    channel_id = sys.argv[4]
    
    notify_bot(bot_ip, user_id, guild_id, channel_id)
