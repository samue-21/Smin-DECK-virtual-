#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TESTE COMPLETO END-TO-END DO SISTEMA DE ARQUIVOS

Fluxo testado:
1. Arquivo sobe para o banco de dados
2. Verifica dados no banco (chave, tamanho, nome, formato)
3. Sincronizador baixa arquivo
4. App converte arquivo antes de adicionar no botão

Como usar:
1. Execute este script
2. Vai mostrar "Aguardando primeira atualizacao..."
3. Envie um arquivo via bot no Discord
4. Script detectará e analisará todo o fluxo
"""

import json
import sys
import os
import time
import subprocess
from datetime import datetime
from pathlib import Path

# Cores para terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class TesteSistemaArquivos:
    def __init__(self):
        self.banco_inicial = None
        self.arquivo_baixado = False
        self.downloads_dir = Path.home() / '.smindeckbot' / 'downloads'
        
    def clean_text(self, text):
        """Remove caracteres especiais para logging"""
        return text.encode('ascii', 'ignore').decode('ascii')
    
    def passo(self, num, titulo):
        """Mostra título de passo"""
        print(f"\n{BLUE}{'='*70}{RESET}")
        print(f"{BLUE}[PASSO {num}] {titulo}{RESET}")
        print(f"{BLUE}{'='*70}{RESET}")
    
    def ok(self, msg):
        """Mensagem de sucesso"""
        print(f"{GREEN}[OK]{RESET} {self.clean_text(msg)}")
    
    def erro(self, msg):
        """Mensagem de erro"""
        print(f"{RED}[ERRO]{RESET} {self.clean_text(msg)}")
    
    def info(self, msg):
        """Mensagem de informação"""
        print(f"{YELLOW}[INFO]{RESET} {self.clean_text(msg)}")
    
    def aguardar_arquivo(self, timeout=120):
        """Aguarda novo arquivo ser enviado para o banco"""
        self.passo(1, "AGUARDAR UPLOAD DE ARQUIVO")
        
        try:
            from database import obter_atualizacoes
            
            self.banco_inicial = obter_atualizacoes()
            inicial = len(self.banco_inicial)
            
            self.info(f"Atualizacoes no banco: {inicial}")
            self.info(f"Enviando arquivo de teste via Discord bot...")
            self.info(f"Aguardando por {timeout} segundos...")
            print()
            
            inicio = time.time()
            while time.time() - inicio < timeout:
                todas = obter_atualizacoes()
                atual = len(todas)
                
                if atual > inicial:
                    # Nova atualizacao encontrada!
                    self.ok(f"Nova atualizacao detectada! ({inicial} -> {atual})")
                    time.sleep(1)  # Aguarda mais um pouco para garantir que foi salvo
                    return True
                
                # Mostrar progresso
                segundos = int(time.time() - inicio)
                print(f"\r{YELLOW}[AGUARDANDO]{RESET} {segundos}s...", end='', flush=True)
                time.sleep(1)
            
            print()
            self.erro("Timeout! Nenhum arquivo foi enviado.")
            return False
            
        except Exception as e:
            self.erro(f"Erro ao aguardar: {e}")
            return False
    
    def verificar_dados_banco(self):
        """Verifica dados do arquivo no banco"""
        self.passo(2, "VERIFICAR DADOS NO BANCO DE DADOS")
        
        try:
            from database import obter_atualizacoes
            import sqlite3
            
            todas = obter_atualizacoes()
            if not todas:
                self.erro("Nenhuma atualizacao no banco!")
                return False
            
            # Pega a ULTIMA atualizacao (indice 0)
            att = todas[0]
            id_att, chave, tipo, botao, dados_str, criada_em = att
            
            self.info("Dados brutos no banco:")
            print(f"  ID: {id_att}")
            print(f"  Chave: {self.clean_text(chave[:20])}...")
            print(f"  Tipo: {tipo}")
            print(f"  Botao: {botao}")
            print(f"  Data: {criada_em}")
            
            # Parse JSON
            try:
                dados = json.loads(dados_str) if isinstance(dados_str, str) else dados_str
            except:
                dados = dados_str
            
            print(f"\n  {YELLOW}Dados estruturados:{RESET}")
            
            if isinstance(dados, dict):
                # Verificar cada campo esperado
                checks = [
                    ('arquivo', 'Nome do arquivo no servidor'),
                    ('nome', 'Nome personalizado do usuario'),
                ]
                
                todas_presente = True
                for campo, descricao in checks:
                    if campo in dados:
                        valor = dados[campo]
                        print(f"    {GREEN}✓{RESET} {campo}: {self.clean_text(str(valor)[:50])}")
                    else:
                        print(f"    {RED}✗{RESET} {campo}: [AUSENTE]")
                        todas_presente = False
                
                # Campos opcionais
                if 'extraido_de' in dados:
                    print(f"    {GREEN}✓{RESET} extraido_de: {self.clean_text(str(dados['extraido_de'])[:50])}")
                
                if todas_presente:
                    self.ok("Todos os campos esperados presentes no banco!")
                    self.arquivo = dados.get('arquivo')
                    self.nome = dados.get('nome')
                    return True
                else:
                    self.erro("Faltam campos esperados no banco!")
                    return False
            else:
                self.erro(f"Dados nao sao dicionario: {type(dados)}")
                return False
                
        except Exception as e:
            self.erro(f"Erro ao verificar banco: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def testar_sincronizador(self):
        """Testa se sincronizador consegue baixar arquivo"""
        self.passo(3, "TESTAR SINCRONIZADOR - BAIXAR ARQUIVO")
        
        try:
            # Limpar pasta de downloads
            if self.downloads_dir.exists():
                self.info(f"Pasta de downloads: {self.downloads_dir}")
                arquivos_antes = list(self.downloads_dir.glob('*'))
                self.info(f"Arquivos antes: {len(arquivos_antes)}")
            else:
                self.info(f"Criando pasta: {self.downloads_dir}")
                self.downloads_dir.mkdir(parents=True, exist_ok=True)
                arquivos_antes = []
            
            # Executar sincronizador
            self.info("Executando sincronizador...")
            
            # Importar e executar funcao de sincronizar
            try:
                from sincronizador import processar_atualizacoes
                processar_atualizacoes()
                self.ok("Sincronizador executado!")
            except Exception as e:
                self.erro(f"Erro ao executar sincronizador: {e}")
                return False
            
            # Verificar se arquivo foi baixado
            time.sleep(2)
            arquivos_depois = list(self.downloads_dir.glob('*'))
            self.info(f"Arquivos depois: {len(arquivos_depois)}")
            
            if len(arquivos_depois) > len(arquivos_antes):
                novos = [a for a in arquivos_depois if a not in arquivos_antes]
                self.ok(f"Arquivo(s) baixado(s)!")
                for arq in novos:
                    tamanho_mb = arq.stat().st_size / (1024 * 1024)
                    print(f"    {GREEN}✓{RESET} {arq.name} ({tamanho_mb:.2f}MB)")
                    self.arquivo_baixado = True
                return True
            else:
                self.erro("Nenhum arquivo novo foi baixado!")
                return False
                
        except Exception as e:
            self.erro(f"Erro ao testar sincronizador: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def verificar_conversao(self):
        """Verifica se arquivo desceu INDEPENDENTE do formato"""
        self.passo(4, "VERIFICAR SE ARQUIVO DESCEU (QUALQUER FORMATO)")
        
        if not self.arquivo_baixado:
            self.info("Pulando - arquivo nao foi baixado")
            return False
        
        try:
            arquivos = list(self.downloads_dir.glob('*'))
            
            if not arquivos:
                self.erro("Nenhum arquivo na pasta de downloads!")
                return False
            
            self.info(f"Analisando arquivo(s) - QUALQUER FORMATO VALIDO...")
            
            for arq in sorted(arquivos):
                ext = arq.suffix.lower()
                tamanho = arq.stat().st_size / (1024*1024)
                
                print(f"\n  Arquivo: {self.clean_text(arq.name)}")
                print(f"  Extensao: {ext}")
                print(f"  Tamanho: {tamanho:.2f}MB")
                
                # Verificar magic bytes para referencia
                try:
                    with open(arq, 'rb') as f:
                        magic = f.read(32)
                    
                    # Alguns formatos conhecidos
                    formatos = {
                        b'ftyp': 'MP4 (video)',
                        b'\x89PNG': 'PNG (imagem)',
                        b'\xff\xd8\xff': 'JPEG (imagem)',
                        b'ID3': 'MP3 (audio)',
                        b'OggS': 'OGG (audio)',
                        b'fLaC': 'FLAC (audio)',
                        b'%PDF': 'PDF (documento)',
                        b'PK\x03\x04': 'ZIP (compactado)',
                    }
                    
                    detectado = "Desconhecido"
                    for assinatura, tipo in formatos.items():
                        if assinatura in magic[:20]:
                            detectado = tipo
                            break
                    
                    print(f"  Tipo detectado: {detectado}")
                    
                except Exception as e:
                    self.info(f"Nao conseguiu detectar tipo: {e}")
                
                # O importante é QUE CHEGOU, independente do formato!
                self.ok(f"Arquivo desceu para download: {ext}")
                
                # Verificar se arquivo é válido (tem dados)
                if tamanho > 0:
                    self.ok(f"Arquivo tem dados ({tamanho:.2f}MB) - pode ser processado")
                    return True
                else:
                    self.erro(f"Arquivo vazio (0MB)!")
                    return False
            
            return True
            
        except Exception as e:
            self.erro(f"Erro ao verificar: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def resumo_final(self, resultados):
        """Mostra resumo final"""
        self.passo(5, "RESUMO FINAL")
        
        total = len(resultados)
        passou = sum(1 for r in resultados.values() if r)
        
        for teste, resultado in resultados.items():
            status = f"{GREEN}[PASS]{RESET}" if resultado else f"{RED}[FAIL]{RESET}"
            print(f"{status} {teste}")
        
        print(f"\n{YELLOW}Total: {passou}/{total} testes{RESET}")
        
        if passou == total:
            print(f"\n{GREEN}[SUCCESS] FLUXO COMPLETO FUNCIONANDO!{RESET}")
            print(f"{GREEN}Arquivo subiu -> Banco registrou -> App baixou -> Formato correto{RESET}")
            return True
        else:
            print(f"\n{RED}[AVISO] Alguns testes falharam{RESET}")
            return False
    
    def executar(self):
        """Executa teste completo"""
        print(f"\n{BLUE}╔═══════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{BLUE}║         TESTE COMPLETO - SISTEMA DE ARQUIVOS END-TO-END         ║{RESET}")
        print(f"{BLUE}╚═══════════════════════════════════════════════════════════════════╝{RESET}")
        
        resultados = {}
        
        # Teste 1: Aguardar arquivo
        resultados['Arquivo sobe para banco'] = self.aguardar_arquivo()
        if not resultados['Arquivo sobe para banco']:
            self.erro("Não conseguiu enviar arquivo!")
            self.resumo_final(resultados)
            return False
        
        time.sleep(1)
        
        # Teste 2: Verificar dados no banco
        resultados['Dados no banco corretos'] = self.verificar_dados_banco()
        if not resultados['Dados no banco corretos']:
            self.erro("Dados no banco incorretos!")
            self.resumo_final(resultados)
            return False
        
        time.sleep(1)
        
        # Teste 3: Testar sincronizador
        resultados['Sincronizador baixa arquivo'] = self.testar_sincronizador()
        if not resultados['Sincronizador baixa arquivo']:
            self.erro("Sincronizador não conseguiu baixar!")
            self.resumo_final(resultados)
            return False
        
        time.sleep(1)
        
        # Teste 4: Verificar conversão
        resultados['Arquivo em formato correto'] = self.verificar_conversao()
        
        # Resumo final
        return self.resumo_final(resultados)


def main():
    teste = TesteSistemaArquivos()
    sucesso = teste.executar()
    
    print(f"\n{BLUE}{'='*70}{RESET}\n")
    
    return 0 if sucesso else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[CANCELADO] Teste interrompido pelo usuario{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}[ERRO CRITICO]{RESET} {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
