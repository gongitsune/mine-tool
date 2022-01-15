from typing import Optional
from watchdog.events import LoggingEventHandler, FileModifiedEvent
from watchdog.observers import Observer
import json
import time
from pathlib import Path
import shutil
import rcon


class Config:
    def __init__(self) -> None:
        with open("config/config.json", "r") as f:
            data = json.load(f)
            self.target_dir = data["buildDir"]
            self.plugin_dir = data["pluginDir"]
            self.plugin_name = data["pluginName"]
            self.rcon_host = data["rconHost"]
            self.rcon_passwd = data["rconPassword"]
            self.rcon_port = data["rconPort"]

            exit_flag = False
            if not Path(self.target_dir).exists():
                print(f"ERROR: No such directory. ({self.target_dir})")
                exit_flag = True
            if not Path(self.plugin_dir).exists():
                print(f"ERROR: No such directory. ({self.plugin_dir})")
                exit_flag = True
            if exit_flag:
                quit()


config = Config()


class Handler(LoggingEventHandler):  # type: ignore
    to_path = Path(config.plugin_dir)
    time_stamp: Optional[float] = None

    def on_modified(self, event: FileModifiedEvent) -> None:
        mtime = Path(event.src_path).stat().st_mtime
        if not self.time_stamp:
            self.time_stamp = mtime
        elif mtime - self.time_stamp < 2:
            return
        self.time_stamp = mtime
        print("🍺 On modified!")
        rcon.disable()
        time.sleep(2)
        shutil.copy2(event.src_path, self.to_path)
        time.sleep(2)
        rcon.enable()


if __name__ == "__main__":
    while not rcon.is_connected:
        time.sleep(5)
    print("🍰 Enabled!!")

    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, config.target_dir, recursive=True)  # 監視設定
    observer.start()  # 監視開始
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        rcon.mcr.disconnect()  # type: ignore
