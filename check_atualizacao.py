#!/usr/bin/env python3
import requests

API_URL = 'http://72.60.244.240:5001'

resp = requests.get(f'{API_URL}/api/atualizacoes', timeout=10)
if resp.status_code == 200:
    dados = resp.json()
    if dados['atualizacoes']:
        att = dados['atualizacoes'][0]
        print(f'Atualização mais recente:')
        print(f'  ID: {att["id"]}')
        print(f'  Botão: {att["botao"]}')
        print(f'  Tipo: {att["tipo"]}')
        print(f'  Dados: {att["dados"]}')
        print()
        if 'arquivo' in att['dados']:
            print('✅ Tem "arquivo" nos dados')
            print(f'   Nome: {att["dados"]["arquivo"]}')
        else:
            print('❌ NÃO tem "arquivo" nos dados')
            print(f'   Keys presentes: {list(att["dados"].keys())}')
