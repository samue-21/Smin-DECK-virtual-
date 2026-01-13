import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.60.244.240', username='root', password='Amor180725###', timeout=10)

cmds = [
    ('Arquivos .sdk', 'find /opt -name "*.sdk" 2>/dev/null'),
    ('Arquivos deck_config', 'find /opt -name "*deck_config*" 2>/dev/null'),
    ('Config no bot', 'cat /opt/smindeck-bot/deck_config.sdk 2>/dev/null || echo NAO_EXISTE'),
    ('Ls opt smindeck', 'ls -la /opt/smindeck-bot/'),
]

for title, cmd in cmds:
    print(f"\n=== {title} ===")
    _, o, e = ssh.exec_command(cmd)
    out = o.read().decode()
    if out.strip():
        print(out[:1000])

ssh.close()
