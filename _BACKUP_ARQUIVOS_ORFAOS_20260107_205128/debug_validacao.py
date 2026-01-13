import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.60.244.240', username='root', password='Amor180725###')

print("DEBUGANDO: PÓS VALIDAÇÃO")
print("="*60)

# Ver o que acontece após validar
cmd = 'sed -n "472,490p" /opt/smindeck-bot/bot.py'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode()
print("BOT.PY - Fluxo pós validação:")
print(output)

print("\n" + "="*60)

# Ver a função check_validar_chave
cmd = 'sed -n "233,240p" /opt/smindeck-bot/bot.py'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode()
print("\ncheck_validar_chave:")
print(output)

print("\n" + "="*60)

# Ver se usuario_esta_ativo está correto
cmd = 'sed -n "227,240p" /opt/smindeck-bot/database.py'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode()
print("\nusuario_esta_ativo em database.py:")
print(output)

ssh.close()
