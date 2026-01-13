import os
from sincronizador import extrair_arquivo_compactado_cliente

# Usar um dos ZIP que já existe
zip_path = os.path.expanduser('~/.smindeckbot/downloads/video_botao_7.bin')

print(f"Testando extrair_arquivo_compactado_cliente()")
print(f"ZIP: {zip_path}")
print(f"Tipo: video")

# Chamar a função
resultado = extrair_arquivo_compactado_cliente(zip_path, 'video')

print(f"\nResultado: {resultado}")

if resultado:
    if os.path.exists(resultado):
        size = os.path.getsize(resultado)
        print(f"✅ Arquivo extraído existe: {size:,} bytes")
    else:
        print(f"❌ Arquivo extraído não existe")
else:
    print(f"❌ Função retornou None")
