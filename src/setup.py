from cx_Freeze import setup, Executable

base = None

exe = Executable(script="src/main.py", base=base)

setup(name="mine_tool", version="0.2", description="converter", executables=[exe])
