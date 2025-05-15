from cx_Freeze import Executable, setup

include_files = ['audio', 'font', 'images','venv','__pycache__'] # file or directory  # file or directory

options = {
'build_exe': {
    'include_msvcr': True,
    'build_exe': 'DinoRunner_exe',
    'include_files': include_files,
    }
}

executables = [
    Executable("Game.py", icon='"images/Player/icon.png"'),
]

setup(
    name="DinoRunner",
    version="1.0",
    description="Game",
    executables=executables,
    options=options,
)