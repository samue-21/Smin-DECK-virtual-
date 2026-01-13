import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.60.244.240', username='root', password='Amor180725###')

print("DEBUGANDO: PÓS VALIDAÇÃO DE CHAVE")
print("="*60)

# Ver o fluxo após validar a chave
cmd = 'sed -n "470,510p" /opt/smindeck-bot/bot.py'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode()
print("🔍 BOT.PY - LINHAS 470-510 (APÓS VALIDAR CHAVE):")
print(output)

print("\n" + "="*60)

# Ver função mostrar_menu_principal
cmd = 'grep -n "async def mostrar_menu_principal" /opt/smindeck-bot/bot.py'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode()
print("📋 mostrar_menu_principal:")
print(output)

if output.strip():
    line = output.split(':')[0]
    cmd = f'sed -n "{line},{int(line)+20}p" /opt/smindeck-bot/bot.py'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().decode()
    print(output)

print("\n" + "="*60)

# Verificar se há log do bot
cmd = 'tail -100 /opt/smindeck-bot/bot.log 2>/dev/null | tail -50'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode()
print("📝 LOG DO BOT (últimas linhas):")
print(output if output.strip() else "  (sem log)")

ssh.close()
