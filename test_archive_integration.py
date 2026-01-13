#!/usr/bin/env python3
"""
Teste de integração: Simula fluxo completo de extração e sincronização
"""

import os
import sys
import tempfile
import zipfile
import json
from pathlib import Path

sys.path.insert(0, 'c:\\Users\\SAMUEL\\Desktop\\Smin-DECK virtual')

def criar_zip_teste():
    """Cria um ZIP de teste com múltiplos tipos de arquivo"""
    # Criar diretório permanente para este teste
    test_dir = os.path.join(tempfile.gettempdir(), 'smindeckbot_zip_test')
    os.makedirs(test_dir, exist_ok=True)
    
    # Criar arquivos simulados
    video_path = os.path.join(test_dir, 'video.mp4')
    with open(video_path, 'wb') as f:
        f.write(b'fake_video_mp4_' * 200)  # 3KB
    
    imagem_path = os.path.join(test_dir, 'poster.jpg')
    with open(imagem_path, 'wb') as f:
        f.write(b'fake_jpeg_' * 150)  # 1.5KB
    
    audio_path = os.path.join(test_dir, 'soundtrack.mp3')
    with open(audio_path, 'wb') as f:
        f.write(b'fake_mp3_' * 100)  # 0.9KB
    
    readme_path = os.path.join(test_dir, 'README.txt')
    with open(readme_path, 'w') as f:
        f.write('Este eh um arquivo de teste para extracao')
    
    # Criar ZIP
    zip_path = os.path.join(test_dir, 'conteudo_completo.zip')
    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.write(video_path, arcname='video.mp4')
        zf.write(imagem_path, arcname='poster.jpg')
        zf.write(audio_path, arcname='soundtrack.mp3')
        zf.write(readme_path, arcname='README.txt')
    
    print(f"[TESTE] ZIP criado: {os.path.basename(zip_path)}")
    print(f"        Caminho completo: {zip_path}")
    print(f"        Tamanho: {os.path.getsize(zip_path)} bytes")
    
    # Limpar arquivos temporarios mas manter o ZIP
    import shutil
    try:
        os.remove(video_path)
        os.remove(imagem_path)
        os.remove(audio_path)
        os.remove(readme_path)
    except:
        pass
    
    return zip_path

def teste_fluxo_completo():
    """Simula fluxo completo de servidor -> cliente"""
    print("\n" + "="*60)
    print("TESTE DE INTEGRACAO: Fluxo Completo de Extracao")
    print("="*60)
    
    from arquivo_processor import extrair_arquivo_compactado, eh_arquivo_compactado
    
    # Configurar UPLOADS_DIR para teste
    upload_temp = tempfile.mkdtemp()
    os.environ['UPLOADS_DIR'] = upload_temp
    print(f"\n[SERVIDOR] UPLOADS_DIR: {upload_temp}")
    
    # Configurar DOWNLOADS_DIR para cliente
    download_temp = tempfile.mkdtemp()
    print(f"[CLIENTE] DOWNLOADS_DIR: {download_temp}")
    
    # PASSO 1: Criar ZIP
    print("\n[PASSO 1] Criando ZIP de teste...")
    zip_path = criar_zip_teste()
    
    # PASSO 2: Testar detecção no servidor
    print("\n[PASSO 2] Detectando tipo de arquivo no servidor...")
    eh_compactado = eh_arquivo_compactado(zip_path)
    print(f"[SERVIDOR] eh_arquivo_compactado: {eh_compactado}")
    assert eh_compactado, "Falha na detecção!"
    
    # PASSO 3: Extrair no servidor
    print("\n[PASSO 3] Extraindo arquivo no servidor...")
    print("[SERVIDOR] Tipo selecionado: VIDEO")
    arquivo_video = extrair_arquivo_compactado(zip_path, 'video')
    assert arquivo_video, "Falha ao extrair video!"
    print(f"[SERVIDOR] Video extraido: {os.path.basename(arquivo_video)}")
    print(f"           Tamanho: {os.path.getsize(arquivo_video)} bytes")
    
    print("[SERVIDOR] Tipo selecionado: IMAGEM")
    arquivo_imagem = extrair_arquivo_compactado(zip_path, 'imagem')
    assert arquivo_imagem, "Falha ao extrair imagem!"
    print(f"[SERVIDOR] Imagem extraida: {os.path.basename(arquivo_imagem)}")
    
    # PASSO 4: Simular sincronização no cliente
    print("\n[PASSO 4] Sincronizacao do cliente...")
    import sys
    sys.path.insert(0, upload_temp)  # Permitir download local
    sys.path.insert(0, download_temp)
    
    # Copiar arquivo para simular download
    import shutil
    origem = arquivo_video
    destino_cliente = os.path.join(download_temp, os.path.basename(arquivo_video))
    shutil.copy(origem, destino_cliente)
    print(f"[CLIENTE] Arquivo baixado: {os.path.basename(destino_cliente)}")
    print(f"          Tamanho: {os.path.getsize(destino_cliente)} bytes")
    
    # PASSO 5: Verificar conteúdo
    print("\n[PASSO 5] Verificacao do conteudo...")
    
    tamanho_upload = os.path.getsize(arquivo_video)
    tamanho_download = os.path.getsize(destino_cliente)
    
    print(f"[VERIFICACAO] Tamanho uploadado: {tamanho_upload} bytes")
    print(f"              Tamanho baixado:   {tamanho_download} bytes")
    
    assert tamanho_upload == tamanho_download, "Tamanho dos arquivos nao corresponde!"
    print("[OK] Tamanhos correspondem!")
    
    # Ler e verificar conteúdo
    with open(arquivo_video, 'rb') as f:
        conteudo_upload = f.read()
    
    with open(destino_cliente, 'rb') as f:
        conteudo_download = f.read()
    
    assert conteudo_upload == conteudo_download, "Conteudo dos arquivos nao corresponde!"
    print("[OK] Conteudo identico!")
    
    # PASSO 6: Testar tipo nao encontrado
    print("\n[PASSO 6] Teste: Tipo nao encontrado no ZIP")
    print("[SERVIDOR] Procurando por AUDIO em novo ZIP...")
    
    # Recrear ZIP sem audio
    with tempfile.TemporaryDirectory() as temp:
        video_path = os.path.join(temp, 'video.mp4')
        with open(video_path, 'wb') as f:
            f.write(b'fake_video_' * 100)
        
        imagem_path = os.path.join(temp, 'imagem.jpg')
        with open(imagem_path, 'wb') as f:
            f.write(b'fake_image_' * 100)
        
        zip_path_novo = os.path.join(temp, 'sem_audio.zip')
        with zipfile.ZipFile(zip_path_novo, 'w') as zf:
            zf.write(video_path, arcname='video.mp4')
            zf.write(imagem_path, arcname='imagem.jpg')
        
        resultado_audio = extrair_arquivo_compactado(zip_path_novo, 'audio')
        if resultado_audio is None:
            print("[OK] Corretamente retornou None (audio nao encontrado)")
        else:
            print("[ERRO] Deveria ter retornado None!")
            return False
    
    # Limpeza
    print("\n[LIMPEZA] Removendo diretorios temporarios...")
    import shutil
    shutil.rmtree(upload_temp)
    shutil.rmtree(download_temp)
    print("[OK] Limpeza completa!")
    
    return True

def teste_multiplas_sincronizacoes():
    """Testa multiplas extrações em sequência"""
    print("\n" + "="*60)
    print("TESTE: Multiplas Sincronizacoes")
    print("="*60)
    
    from arquivo_processor import extrair_arquivo_compactado
    
    upload_temp = tempfile.mkdtemp()
    os.environ['UPLOADS_DIR'] = upload_temp
    
    tipos_teste = [
        ('video', ['.mp4', 'teste.mp4']),
        ('imagem', ['.jpg', 'imagem.jpg']),
        ('audio', ['.mp3', 'som.mp3']),
    ]
    
    for tipo, (ext, nome_arquivo) in tipos_teste:
        print(f"\n[TESTE] Extraindo tipo: {tipo}")
        
        # Criar ZIP com arquivo específico
        with tempfile.TemporaryDirectory() as temp:
            arquivo_path = os.path.join(temp, nome_arquivo)
            with open(arquivo_path, 'wb') as f:
                f.write(b'conteudo_teste_' * 50)
            
            zip_path = os.path.join(temp, f'arquivo_{tipo}.zip')
            with zipfile.ZipFile(zip_path, 'w') as zf:
                zf.write(arquivo_path, arcname=nome_arquivo)
            
            resultado = extrair_arquivo_compactado(zip_path, tipo)
            
            if resultado:
                print(f"[OK] {tipo}: {os.path.basename(resultado)}")
                assert os.path.exists(resultado), f"Arquivo {tipo} não existe!"
            else:
                print(f"[ERRO] Falha ao extrair {tipo}")
                return False
    
    import shutil
    shutil.rmtree(upload_temp)
    return True

if __name__ == '__main__':
    print("\n" + "="*60)
    print("SUITE DE TESTES: Extracao de Arquivos Compactados")
    print("="*60)
    
    testes = [
        ("Fluxo Completo", teste_fluxo_completo),
        ("Multiplas Sincronizacoes", teste_multiplas_sincronizacoes),
    ]
    
    resultados = {}
    for nome_teste, funcao_teste in testes:
        try:
            print(f"\n>>> Executando: {nome_teste}")
            resultado = funcao_teste()
            resultados[nome_teste] = '[OK] PASSOU' if resultado else '[ERRO] FALHOU'
        except Exception as e:
            print(f"\n[EXCECAO] Erro em {nome_teste}: {e}")
            import traceback
            traceback.print_exc()
            resultados[nome_teste] = f'[EXCECAO] {str(e)[:50]}'
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO FINAL")
    print("="*60)
    for nome_teste, resultado in resultados.items():
        print(f"{resultado} - {nome_teste}")
    
    todas_passaram = all('[OK]' in r for r in resultados.values())
    if todas_passaram:
        print("\n[SUCESSO] TODOS OS TESTES PASSARAM!")
        sys.exit(0)
    else:
        print("\n[FALHA] ALGUNS TESTES FALHARAM!")
        sys.exit(1)
