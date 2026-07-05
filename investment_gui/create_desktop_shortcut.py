"""Create a Windows-desktop shortcut for an app that lives inside WSL.

Fixes over the previous version:
- Pins the WSL distro in the shortcut (-d <name>) instead of relying on the default
- Copies the icon to the Windows filesystem (icons on \\wsl.localhost paths
  usually fail to render in .lnk files)
- The launcher keeps the console open if the app fails, so errors are visible
"""

import os
import shutil
import stat
import subprocess
from pathlib import Path

APP_NAME = "Investment Portfolio"
SCRIPT_DIR = Path(__file__).resolve().parent
MAIN_SCRIPT = SCRIPT_DIR / "investment_gui" / "app.py"
PYTHON_EXE = SCRIPT_DIR / ".venv" / "bin" / "python"


def ps(command: str) -> str:
    """Run a PowerShell command from WSL and return its stdout, stripped."""
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def win_to_wsl(win_path: str) -> Path:
    """Convert a Windows path (C:\\...) to a WSL path (/mnt/c/...)."""
    result = subprocess.run(
        ["wslpath", "-u", win_path], capture_output=True, text=True, check=True
    )
    return Path(result.stdout.strip())


def create_sh_launcher() -> Path:
    """Create the launcher script. On failure it keeps the window open."""
    sh_path = SCRIPT_DIR / f"{APP_NAME.replace(' ', '_').lower()}.sh"
    sh_content = (
        f"#!/usr/bin/env bash\n"
        f'export PYTHONPATH="{SCRIPT_DIR}"\n'
        f'cd "{SCRIPT_DIR}"\n'
        f'"{PYTHON_EXE}" "{MAIN_SCRIPT}"\n'
        f"status=$?\n"
        f"if [ $status -ne 0 ]; then\n"
        f'  echo ""\n'
        f'  echo "App exited with status $status. Press Enter to close."\n'
        f"  read\n"
        f"fi\n"
    )
    sh_path.write_text(sh_content, encoding="utf-8")
    sh_path.chmod(sh_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return sh_path


def copy_icon_to_windows() -> str:
    """Copy currency.ico to the Windows filesystem and return its Windows path.

    Icons referenced through \\\\wsl.localhost\\... paths often do not render,
    so we store a copy under %LOCALAPPDATA%\\InvestmentPortfolio.
    """
    icon_src = SCRIPT_DIR / "currency.ico"
    if not icon_src.exists():
        print(f"Warning: icon not found at {icon_src}, shortcut will use default icon")
        return ""

    local_appdata_win = ps("[Environment]::GetFolderPath('LocalApplicationData')")
    dest_dir_wsl = win_to_wsl(local_appdata_win) / "InvestmentPortfolio"
    dest_dir_wsl.mkdir(parents=True, exist_ok=True)
    shutil.copy2(icon_src, dest_dir_wsl / "currency.ico")

    return f"{local_appdata_win}\\InvestmentPortfolio\\currency.ico"


def create_wsl_shortcut() -> None:
    sh_path = create_sh_launcher()

    distro = os.environ.get("WSL_DISTRO_NAME", "")
    if not distro:
        print(
            "Warning: WSL_DISTRO_NAME not set; the shortcut will use the default distro"
        )

    desktop_win = ps("[Environment]::GetFolderPath('Desktop')")
    shortcut_win = f"{desktop_win}\\{APP_NAME}.lnk"
    icon_win = copy_icon_to_windows()

    distro_arg = f"-d {distro} " if distro else ""
    arguments = f'{distro_arg}-e "{sh_path}"'

    ps_script = (
        "$ws = New-Object -ComObject WScript.Shell; "
        f"$s = $ws.CreateShortcut('{shortcut_win}'); "
        "$s.TargetPath = 'C:\\Windows\\System32\\wsl.exe'; "
        f"$s.Arguments = '{arguments}'; "
        + (f"$s.IconLocation = '{icon_win},0'; " if icon_win else "")
        + "$s.Save()"
    )
    subprocess.run(["powershell.exe", "-NoProfile", "-Command", ps_script], check=True)

    print(f"Shortcut created: {shortcut_win}")
    print(f"Launcher script:  {sh_path}")
    print()
    print("Test the launcher directly first:")
    print(f"  bash '{sh_path}'")
    print("If the app opens with that command but not via the shortcut,")
    print("run this in PowerShell to see the real error:")
    print(f'  wsl.exe {distro_arg}-e "{sh_path}"')


if __name__ == "__main__":
    create_wsl_shortcut()
