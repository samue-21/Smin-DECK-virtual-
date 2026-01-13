"""
Servidor de Updates para Smin-DECK Virtual (roda no VPS)
Endpoints para servir atualizações e gerenciar versões
"""

from flask import Flask, request, jsonify, send_file
import os
import json
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

# Configurações
UPDATES_DIR = "/root/smin_deck_updates"  # Alterar conforme ambiente
VERSION_FILE = os.path.join(UPDATES_DIR, "current_version.json")

os.makedirs(UPDATES_DIR, exist_ok=True)

# Inicializar versão se não existe
if not os.path.exists(VERSION_FILE):
    with open(VERSION_FILE, 'w') as f:
        json.dump({
            "version": "1.0.0",
            "download_url": None,
            "changelog": "Versão inicial",
            "released": datetime.now().isoformat()
        }, f)


@app.route('/api/updates/check', methods=['GET'])
def check_updates():
    """Endpoint para verificar se há atualizações disponíveis"""
    try:
        with open(VERSION_FILE, 'r') as f:
            data = json.load(f)
        
        return jsonify({
            "version": data.get("version", "1.0.0"),
            "download_url": data.get("download_url"),
            "changelog": data.get("changelog", ""),
            "released": data.get("released")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/deploy/upload', methods=['POST'])
def deploy_upload():
    """Endpoint para fazer upload de novo pacote de atualização"""
    try:
        if 'package' not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400
        
        version = request.form.get('version', '1.0.0')
        changelog = request.form.get('changelog', 'Atualizações')
        
        package_file = request.files['package']
        filename = f"smin_deck_v{version}.zip"
        filepath = os.path.join(UPDATES_DIR, filename)
        
        # Salvar arquivo
        package_file.save(filepath)
        print(f"✅ Pacote salvo: {filepath}")
        
        # Atualizar versão
        download_url = f"http://72.60.244.240:8000/download/{filename}"
        
        version_data = {
            "version": version,
            "download_url": download_url,
            "changelog": changelog,
            "released": datetime.now().isoformat(),
            "file_size": os.path.getsize(filepath)
        }
        
        with open(VERSION_FILE, 'w') as f:
            json.dump(version_data, f, indent=2)
        
        print(f"✅ Versão atualizada: {version}")
        
        return jsonify({
            "success": True,
            "message": "Pacote publicado com sucesso",
            "version": version,
            "download_url": download_url
        })
    
    except Exception as e:
        print(f"❌ Erro no upload: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/download/<filename>', methods=['GET'])
def download_update(filename):
    """Endpoint para fazer download do pacote de atualização"""
    try:
        filepath = os.path.join(UPDATES_DIR, filename)
        
        if not os.path.exists(filepath):
            return jsonify({"error": "Arquivo não encontrado"}), 404
        
        print(f"📥 Download iniciado: {filename}")
        return send_file(filepath, as_attachment=True)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/updates/history', methods=['GET'])
def update_history():
    """Lista histórico de atualizações"""
    try:
        updates = []
        
        for file in os.listdir(UPDATES_DIR):
            if file.endswith('.zip'):
                filepath = os.path.join(UPDATES_DIR, file)
                size = os.path.getsize(filepath) / (1024 * 1024)
                
                updates.append({
                    "file": file,
                    "size_mb": round(size, 2),
                    "timestamp": datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
                })
        
        return jsonify({"updates": sorted(updates, key=lambda x: x['timestamp'], reverse=True)})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({"status": "ok", "service": "Smin-DECK Updates Server"})


if __name__ == '__main__':
    print("🚀 Servidor de Updates Smin-DECK iniciado")
    print(f"📁 Pasta de updates: {UPDATES_DIR}")
    print("Endpoints disponíveis:")
    print("  GET  /api/updates/check        - Verificar nova versão")
    print("  GET  /api/updates/history      - Histórico de atualizações")
    print("  POST /api/deploy/upload        - Upload de novo pacote")
    print("  GET  /download/<filename>      - Download do pacote")
    print("  GET  /health                   - Health check")
    
    app.run(host='0.0.0.0', port=8000, debug=False)
