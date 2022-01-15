import time
from xmlrpc.client import Boolean

from mcrcon import MCRcon

from main import config

mcr = MCRcon(config.rcon_host, config.rcon_passwd, config.rcon_port)


def connect() -> Boolean:
    try:
        print(
            f"📶 Connecting ({config.rcon_host}:{config.rcon_port} passwd: {config.rcon_passwd})"
        )
        mcr.connect()
    except Exception:
        print("\033[31mRcon connection failed. Reconnect after 5 seconds.\033[0m")
        time.sleep(5)
        connect()
    return True


is_connected: Boolean = connect()


def disable() -> None:
    try:
        mcr.command(f"plugman unload {config.plugin_name}")
    except Exception as e:
        print(e)


def enable() -> None:
    try:
        mcr.command(f"plugman load {config.plugin_name}")
    except Exception as e:
        print(e)
