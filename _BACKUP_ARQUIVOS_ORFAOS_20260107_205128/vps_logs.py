import os
import sys
import paramiko

HOST = os.environ.get("SMIN_VPS_HOST", "72.60.244.240")
USER = os.environ.get("SMIN_VPS_USER", "root")
PASS = os.environ.get("SMIN_VPS_PASS")

# Evita UnicodeEncodeError no console do Windows (cp1252) ao imprimir logs com símbolos.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

if not PASS:
    print("ERRO: defina a env var SMIN_VPS_PASS antes de rodar.", file=sys.stderr)
    sys.exit(2)

COMMANDS = [
    ("STATUS", "systemctl status smindeck-bot --no-pager | head -40"),
    ("JOURNAL", "journalctl -u smindeck-bot -n 200 --no-pager"),
    ("OOM_KERNEL", "journalctl -k -n 400 --no-pager | grep -Ei 'oom|out of memory|killed process' || true"),
    ("DMESG_TAIL", "dmesg -T | tail -n 160"),
    ("UNIT_FILE", "systemctl cat smindeck-bot --no-pager"),
]


def main() -> int:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(HOST, username=USER, password=PASS, timeout=10)

    for title, cmd in COMMANDS:
        print("\n" + "=" * 20 + f" {title} " + "=" * 20)
        _, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode(errors="replace")
        err = stderr.read().decode(errors="replace")
        if out.strip():
            print(out)
        if err.strip():
            print("--- STDERR ---")
            print(err)

    ssh.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
