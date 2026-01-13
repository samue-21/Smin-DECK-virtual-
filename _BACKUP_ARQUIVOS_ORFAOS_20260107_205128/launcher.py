"""
SminDeck - App Launcher com verificação de dependências
"""
import sys
import subprocess

def check_and_install_dependencies():
    """Verifica e instala dependências faltantes"""
    required_packages = {
        'PyQt6': 'PyQt6',
        'requests': 'requests',
        'PIL': 'Pillow',
    }
    
    missing = []
    
    for module_name, package_name in required_packages.items():
        try:
            __import__(module_name)
            print(f"✓ {module_name} encontrado")
        except ImportError:
            print(f"✗ {module_name} NÃO encontrado")
            missing.append(package_name)
    
    if missing:
        print(f"\nInstalando pacotes faltantes: {', '.join(missing)}")
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install'] + missing,
            check=True
        )
        print("Pacotes instalados com sucesso!")
    else:
        print("\nTodas as dependências estão instaladas!")

if __name__ == '__main__':
    print("=" * 50)
    print("SminDeck - Verificador de Dependências")
    print("=" * 50)
    print()
    
    check_and_install_dependencies()
    
    print("\nIniciando SminDeck...")
    print()
    
    # Importar e executar a aplicação
    from main_app import main
    main()
