#!/usr/bin/env python3
"""
Monitora logs do bot em tempo real usando 'tail -f'
"""
import paramiko
import time
from vps_config import VPS_CONFIG

def monitorar_logs():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(VPS_CONFIG['host'], port=VPS_CONFIG['port'], username=VPS_CONFIG['user'], password=VPS_CONFIG['password'], timeout=10)
    
    print("📡 Monitorando debug.log em tempo real... (Ctrl+C para parar)")
    print("="*60)
    
    # Usar tail -f para monitorar em tempo real
    transport = ssh.get_transport()
    channel = transport.open_session()
    channel.exec_command("tail -f /opt/smindeck-bot/debug.log")
    
    try:
        while True:
            if channel.recv_ready():
                data = channel.recv(1024).decode('utf-8', errors='ignore')
                if data:
                    print(data.rstrip())
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n" + "="*60)
        print("✅ Monitoramento parado")
    finally:
        channel.close()
        ssh.close()

if __name__ == "__main__":
    monitorar_logs()
