from database_client import DatabaseClient

client = DatabaseClient()
print("Testando tem_atualizacoes_pendentes()...")

# Teste 1: Health check
health = client.health_check()
print(f"API Online: {health}")

# Teste 2: Obter atualizacoes direto
atualizacoes = client.obter_atualizacoes()
print(f"Atualizações direto: {atualizacoes}")
print(f"Quantidade: {len(atualizacoes)}")

# Teste 3: Método tem_atualizacoes_pendentes
tem_updates = client.tem_atualizacoes_pendentes()
print(f"tem_atualizacoes_pendentes(): {tem_updates}")
print(f"Tipo: {type(tem_updates)}")
