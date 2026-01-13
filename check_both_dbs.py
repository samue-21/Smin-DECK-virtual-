import sqlite3
import os

# Tentar ambos os arquivos
for db_name in ['data.db', 'smindeckbot.db']:
    db_path = os.path.expanduser(f'~/.smindeckbot/{db_name}')
    
    print(f"\n{'='*60}")
    print(f"Verificando: {db_name}")
    print(f"{'='*60}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Ver tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        if tables:
            print(f"Tabelas encontradas: {tables}")
            
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"\n{table}: {count} linhas")
                
                # Se for atualizacoes, mostrar dados
                if 'atualiza' in table.lower():
                    cursor.execute(f"SELECT * FROM {table} LIMIT 5")
                    rows = cursor.fetchall()
                    print(f"  Primeiras linhas: {rows}")
        else:
            print("  (nenhuma tabela)")
        
        conn.close()
    except Exception as e:
        print(f"Erro: {e}")
