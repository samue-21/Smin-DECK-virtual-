import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.60.244.240', username='root', password='Amor180725###')

# Ver toda a função usuario_autenticado
cmd = 'sed -n "238,260p" /opt/smindeck-bot/bot.py'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode()
print("FUNÇÃO usuario_autenticado COMPLETA:")
print(output)

print("\n" + "="*60)

# Ver database.obter_info_chave
cmd = 'grep -n "def obter_info_chave" /opt/smindeck-bot/database.py'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode()
print("obter_info_chave em database.py:")
print(output)

if output.strip():
    line = output.split(':')[0]
    cmd = f'sed -n "{line},{int(line)+15}p" /opt/smindeck-bot/database.py'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().decode()
    print("\nCÓDIGO:")
    print(output)

ssh.close()
