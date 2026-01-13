import os
import subprocess
import sys


def _spawn(exe_name: str) -> None:
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    exe_path = os.path.join(base_dir, exe_name)

    if not os.path.exists(exe_path):
        return

    creationflags = 0
    if os.name == "nt":
        creationflags = (
            subprocess.CREATE_NO_WINDOW
            | subprocess.DETACHED_PROCESS
            | subprocess.CREATE_NEW_PROCESS_GROUP
        )

    try:
        subprocess.Popen(
            [exe_path],
            cwd=base_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creationflags,
            close_fds=True,
        )
    except Exception:
        pass


def main() -> int:
    # Ordem: API primeiro, depois o bot.
    _spawn("api_server.exe")
    _spawn("discord_bot.exe")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())