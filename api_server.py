#!/usr/bin/env python3
"""
API REST para acessar o banco de dados do Bot
Endpoints disponíveis para APP e Bot se comunicarem via banco de dados SQLite
Porta: 5001
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from database import (
    init_database, criar_chave, validar_chave, obter_info_chave,
    listar_chaves_ativas, registrar_atualizacao, obter_atualizacoes,
    deletar_atualizacao
)

class APIHandler(BaseHTTPRequestHandler):
    """Handler para requisições HTTP da API"""
    
    def do_POST(self):
        """POST requests"""
        path = self.path
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body) if body else {}
        
        try:
            # POST /api/chave/criar - Criar nova chave
            if path == '/api/chave/criar':
                user_id = data.get('user_id')
                guild_id = data.get('guild_id')
                channel_id = data.get('channel_id')
                
                if user_id and guild_id and channel_id:
                    chave = criar_chave(user_id, guild_id, channel_id)
                    if chave:
                        self._json_response(200, {'chave': chave})
                    else:
                        self._json_response(500, {'error': 'Erro ao criar chave'})
                else:
                    self._json_response(400, {'error': 'Faltam parâmetros'})
            
            # POST /api/chave/validar - Verificar se chave está autenticada
            elif path == '/api/chave/validar':
                chave = data.get('chave', '').upper()
                user_id = data.get('user_id')
                guild_id = data.get('guild_id')
                channel_id = data.get('channel_id')
                
                if chave and user_id and guild_id and channel_id:
                    # Apenas verificar se a chave já está em chaves_ativas
                    # (a autenticação acontece automaticamente no bot)
                    import sqlite3
                    import os
                    db_path = os.path.expanduser('~/.smindeckbot/smindeckbot.db')
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    try:
                        cursor.execute('SELECT * FROM chaves_ativas WHERE chave = ?', (chave,))
                        result = cursor.fetchone()
                        if result:
                            self._json_response(200, {'sucesso': True, 'msg': '✅ Chave autenticada com sucesso!'})
                        else:
                            self._json_response(400, {'sucesso': False, 'msg': '❌ Chave não encontrada ou expirada'})
                    finally:
                        conn.close()
                else:
                    self._json_response(400, {'error': 'Faltam parâmetros'})
            
            # POST /api/atualizacao/registrar - Registrar atualização do Bot
            elif path == '/api/atualizacao/registrar':
                chave = data.get('chave')
                tipo = data.get('tipo')
                botao = data.get('botao')
                dados = data.get('dados', {})
                
                if chave and tipo and botao is not None:
                    registrar_atualizacao(chave, tipo, botao, dados)
                    self._json_response(200, {'status': 'registrado'})
                else:
                    self._json_response(400, {'error': 'Faltam parâmetros'})
            
            else:
                self._json_response(404, {'error': 'Endpoint não encontrado'})
        
        except Exception as e:
            self._json_response(500, {'error': str(e)})
    
    def do_GET(self):
        """GET requests"""
        path = self.path
        
        try:
            # GET /api/chave/info/<chave> - Obter info da chave
            if path.startswith('/api/chave/info/'):
                chave = path.split('/api/chave/info/')[1].upper()
                info = obter_info_chave(chave)
                
                if info:
                    self._json_response(200, info)
                else:
                    self._json_response(404, {'error': 'Chave não encontrada'})
            
            # GET /api/chaves/ativas - Listar chaves ativas
            elif path == '/api/chaves/ativas':
                chaves = listar_chaves_ativas()
                self._json_response(200, {'chaves': chaves})
            
            # GET /api/atualizacoes - Obter atualizações
            elif path == '/api/atualizacoes':
                desde = self.headers.get('X-Desde')
                atualizacoes = obter_atualizacoes(desde)
                self._json_response(200, {'atualizacoes': atualizacoes})
            
            # GET /api/arquivo/<filename> - Download de arquivo otimizado
            elif path.startswith('/api/arquivo/'):
                filename = path.split('/api/arquivo/')[1]
                self._servir_arquivo(filename)
            
            # GET /api/health - Health check
            elif path == '/api/health':
                self._json_response(200, {'status': 'ok'})
            
            else:
                self._json_response(404, {'error': 'Endpoint não encontrado'})
        
        except Exception as e:
            self._json_response(500, {'error': str(e)})
    
    def do_DELETE(self):
        """DELETE requests"""
        path = self.path
        
        try:
            # DELETE /api/atualizacao/<id> - Deletar atualização processada
            if path.startswith('/api/atualizacao/'):
                atualizacao_id = path.split('/api/atualizacao/')[1]
                try:
                    atualizacao_id = int(atualizacao_id)
                    if deletar_atualizacao(atualizacao_id):
                        self._json_response(200, {'status': 'deletado'})
                    else:
                        self._json_response(404, {'error': 'Atualização não encontrada'})
                except ValueError:
                    self._json_response(400, {'error': 'ID inválido'})
            
            # DELETE /api/arquivo/<filename> - Deletar arquivo após consumo
            elif path.startswith('/api/arquivo/'):
                filename = path.split('/api/arquivo/')[1]
                if self._deletar_arquivo(filename):
                    self._json_response(200, {'status': 'arquivo deletado'})
                else:
                    self._json_response(404, {'error': 'Arquivo não encontrado'})
            
            else:
                self._json_response(404, {'error': 'Endpoint não encontrado'})
        
        except Exception as e:
            self._json_response(500, {'error': str(e)})
    
    def _json_response(self, status, data):
        """Envia resposta JSON"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _servir_arquivo(self, filename: str):
        """Serve arquivo binário do diretório uploads"""
        uploads_dir = "/opt/smindeck-bot/uploads"
        if os.name == 'nt':
            uploads_dir = "uploads"
        
        # Sanitizar filename (prevenir path traversal)
        if '/' in filename or '\\' in filename or '..' in filename:
            self._json_response(400, {'error': 'Nome de arquivo inválido'})
            return
        
        arquivo_path = os.path.join(uploads_dir, filename)
        
        if not os.path.exists(arquivo_path):
            self._json_response(404, {'error': 'Arquivo não encontrado'})
            return
        
        try:
            with open(arquivo_path, 'rb') as f:
                conteudo = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
            self.send_header('Content-Length', str(len(conteudo)))
            self.end_headers()
            self.wfile.write(conteudo)
        except Exception as e:
            self._json_response(500, {'error': str(e)})
    
    def _deletar_arquivo(self, filename: str) -> bool:
        """Deleta arquivo do diretório uploads"""
        uploads_dir = "/opt/smindeck-bot/uploads"
        if os.name == 'nt':
            uploads_dir = "uploads"
        
        # Sanitizar filename
        if '/' in filename or '\\' in filename or '..' in filename:
            return False
        
        arquivo_path = os.path.join(uploads_dir, filename)
        
        if not os.path.exists(arquivo_path):
            return False
        
        try:
            os.remove(arquivo_path)
            return True
        except Exception:
            return False
    
    def log_message(self, format, *args):
        """Silencia logs padrão"""
        pass

def start_api_server():
    """Inicia servidor da API"""
    init_database()
    server = HTTPServer(('0.0.0.0', 5001), APIHandler)
    print("✅ API iniciada em http://0.0.0.0:5001")
    server.serve_forever()

if __name__ == '__main__':
    start_api_server()
