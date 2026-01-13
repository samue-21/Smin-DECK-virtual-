#!/usr/bin/env python3
import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("72.60.244.240", 22, "root", "Amor180725###", timeout=10)

# Logs
stdin, stdout, stderr = ssh.exec_command("tail -50 /tmp/update_server.log")
print(stdout.read().decode())

ssh.close()
