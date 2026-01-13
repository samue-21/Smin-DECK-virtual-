import zipfile
import os
import tempfile

# Testar extração do ZIP
zip_path = os.path.expanduser('~/.smindeckbot/downloads/video_botao_6.bin')

print(f"Testando extração: {zip_path}")
print(f"Existe? {os.path.exists(zip_path)}")
print(f"Tamanho: {os.path.getsize(zip_path)} bytes")

# Verificar magic bytes
with open(zip_path, 'rb') as f:
    magic = f.read(4)
    print(f"Magic bytes: {magic} (esperado: b'PK\\x03\\x04')")

# Tentar extrair
try:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Listar conteúdo
        files = zip_ref.namelist()
        print(f"\nArquivos no ZIP ({len(files)} arquivos):")
        for fname in files[:10]:
            print(f"  - {fname}")
        
        # Extrair para temp
        temp_dir = tempfile.mkdtemp()
        print(f"\nExtraindo para: {temp_dir}")
        zip_ref.extractall(temp_dir)
        
        # Listar o que foi extraído
        print("\nArquivos extraídos:")
        for root, dirs, extracted_files in os.walk(temp_dir):
            for file in extracted_files:
                file_path = os.path.join(root, file)
                size = os.path.getsize(file_path)
                rel_path = os.path.relpath(file_path, temp_dir)
                print(f"  - {rel_path}: {size:,} bytes")
        
        # Encontrar maior arquivo de vídeo
        print("\nProcurando arquivos de vídeo:")
        for root, dirs, extracted_files in os.walk(temp_dir):
            for file in extracted_files:
                if file.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.webm')):
                    file_path = os.path.join(root, file)
                    size = os.path.getsize(file_path)
                    rel_path = os.path.relpath(file_path, temp_dir)
                    print(f"  - {rel_path}: {size:,} bytes")
                    
                    # Verificar primeiros bytes
                    with open(file_path, 'rb') as fp:
                        header = fp.read(16)
                        print(f"    Magic bytes: {header}")
        
except Exception as e:
    import traceback
    print(f"Erro: {e}")
    traceback.print_exc()
