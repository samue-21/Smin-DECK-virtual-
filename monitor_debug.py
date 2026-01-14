#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONITOR DE DEBUG - Mostra o que está acontecendo em tempo real

Execute em PARALELO com teste_completo_end_to_end.py
em outro terminal!

Monitora:
1. Banco de dados - quando arquivo chega
2. Pasta de downloads - quando arquivo é baixado
3. Processamento do sincronizador
"""

import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class MonitorDebug:
    def __init__(self):
        self.downloads_dir = Path.home() / '.smindeckbot' / 'downloads'
        self.banco_arquivos = {}
        self.download_arquivos = {}
        
    def limpar_tela(self):
        """Limpa a tela"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_timestamp(self):
        """Mostra hora atual"""
        agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{agora}] MONITOR DE DEBUG - SISTEMA DE ARQUIVOS\n")
    
    def monitorer_banco(self):
        """Monitora banco de dados"""
        print("=" * 70)
        print("[BANCO DE DADOS]")
        print("=" * 70)
        
        try:
            from database import obter_atualizacoes
            
            todas = obter_atualizacoes()
            if not todas:
                print("[VAZIO] Nenhuma atualizacao no banco\n")
                return
            
            # Mostra as últimas 3
            para_mostrar = todas[:3]
            print(f"[TOTAL] {len(todas)} atualizacoes no banco\n")
            
            for i, att in enumerate(para_mostrar, 1):
                id_att, chave, tipo, botao, dados_str, criada_em = att
                
                try:
                    dados = json.loads(dados_str)
                except:
                    dados = dados_str
                
                print(f"[#{i}] ID: {id_att} | Data: {criada_em}")
                print(f"     Tipo: {tipo} | Botao: {botao}")
                print(f"     Chave: {chave[:20]}...")
                
                if isinstance(dados, dict):
                    if 'arquivo' in dados:
                        print(f"     [OK] Arquivo: {dados['arquivo']}")
                        print(f"     [OK] Nome: {dados.get('nome', '???')}")
                    elif 'conteudo' in dados:
                        print(f"     [AVISO] Conteudo (texto): {str(dados['conteudo'])[:40]}")
                    else:
                        print(f"     Dados: {json.dumps(dados, ensure_ascii=True)[:50]}")
                else:
                    print(f"     Valor: {str(dados)[:50]}")
                print()
                
        except Exception as e:
            print(f"[ERRO] Nao conseguiu ler banco: {e}\n")
    
    def monitorer_downloads(self):
        """Monitora pasta de downloads"""
        print("=" * 70)
        print("[PASTA DE DOWNLOADS]")
        print("=" * 70)
        
        if not self.downloads_dir.exists():
            print(f"[VAZIO] Pasta nao existe: {self.downloads_dir}\n")
            return
        
        arquivos = list(self.downloads_dir.glob('*'))
        if not arquivos:
            print("[VAZIO] Nenhum arquivo em downloads\n")
            return
        
        print(f"[TOTAL] {len(arquivos)} arquivo(s) em downloads\n")
        
        for arq in sorted(arquivos):
            ext = arq.suffix.lower()
            tamanho = arq.stat().st_size / (1024 * 1024)
            modificado = datetime.fromtimestamp(arq.stat().st_mtime).strftime('%H:%M:%S')
            
            print(f"[FILE] {arq.name}")
            print(f"       Tamanho: {tamanho:.2f}MB")
            print(f"       Extensao: {ext}")
            print(f"       Modificado: {modificado}")
            
            # Verificar magic bytes
            try:
                with open(arq, 'rb') as f:
                    magic = f.read(16)
                
                if b'ftyp' in magic[:12]:
                    tipo = 'MP4 (video)'
                elif magic[:8] == b'\x89PNG\r\n\x1a\n':
                    tipo = 'PNG (imagem)'
                elif magic[:3] == b'\xff\xd8\xff':
                    tipo = 'JPEG (imagem)'
                elif magic[:3] == b'ID3':
                    tipo = 'MP3 (audio)'
                elif magic[:4] == b'fLaC':
                    tipo = 'FLAC (audio)'
                else:
                    tipo = 'Desconhecido'
                
                print(f"       Tipo detectado: {tipo}")
            except:
                pass
            
            if ext == '.bin':
                print(f"       [AVISO] Arquivo ainda em .bin!")
            
            print()
    
    def monitorer_logs(self):
        """Mostra logs recentes"""
        print("=" * 70)
        print("[LOGS DO SISTEMA]")
        print("=" * 70)
        
        try:
            # Procura por log file
            log_files = list(Path('.').glob('*.log'))
            
            if not log_files:
                print("[INFO] Nenhum log file encontrado\n")
                return
            
            # Pega o mais recente
            log_file = max(log_files, key=lambda p: p.stat().st_mtime)
            print(f"[LOG FILE] {log_file.name}\n")
            
            # Mostra últimas linhas
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                linhas = f.readlines()
            
            # Últimas 10 linhas
            para_mostrar = linhas[-10:]
            for linha in para_mostrar:
                linha = linha.rstrip()
                # Mostrar apenas linhas interessantes
                if any(x in linha.lower() for x in ['arquivo', 'download', 'erro', 'sucesso', 'processando']):
                    print(f"  {linha[:100]}")
            
        except Exception as e:
            print(f"[ERRO] Nao conseguiu ler logs: {e}\n")
    
    def executar(self, intervalo=3):
        """Executa monitor em loop"""
        print("\n[INICIANDO MONITOR]\n")
        time.sleep(2)
        
        iteracao = 0
        try:
            while True:
                iteracao += 1
                
                # Limpar tela a cada 5 ciclos para não ficar muito longo
                if iteracao % 5 == 0:
                    self.limpar_tela()
                else:
                    print("\n\n")
                
                self.mostrar_timestamp()
                
                self.monitorer_banco()
                self.monitorer_downloads()
                self.monitorer_logs()
                
                print("=" * 70)
                print(f"[ATUALIZANDO EM {intervalo}s] (Ctrl+C para parar)")
                print("=" * 70)
                
                time.sleep(intervalo)
                
        except KeyboardInterrupt:
            print("\n\n[MONITOR PARADO]")
            sys.exit(0)


def main():
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        intervalo = int(sys.argv[1])
    else:
        intervalo = 3
    
    monitor = MonitorDebug()
    monitor.executar(intervalo)


if __name__ == "__main__":
    main()
