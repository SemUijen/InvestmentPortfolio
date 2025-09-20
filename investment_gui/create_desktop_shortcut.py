import platform
from pathlib import Path

import win32com.client


def create_bat_shortcut():
    app_name = "Investment Portfolio"
    script_dir = Path(__file__).resolve().parent
    main_script = script_dir / "investment_gui/app.py"
    python_exe = script_dir / ".venv" / "Scripts" / "python.exe"
    bat_path = script_dir / f"{app_name}.bat"
    print(f"Script directory: {script_dir}")

    if platform.system() == "Windows":
        bat_content = (
            f"@echo off\n"
            f"set PYTHONPATH={script_dir}\n"
            f'"{python_exe}" "{main_script}"\n'
            f"pause"
        )
        try:
            with open(bat_path, "w") as f:
                f.write(bat_content)
            print(f"Batch file created successfully at: {bat_path}")

            # Create shortcut on Desktop with icon
            try:
                desktop = Path.home() / "OneDrive" / "Bureaublad"
                shortcut_path = desktop / f"{app_name}.lnk"
                icon_path = script_dir / "currency.ico"

                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(str(shortcut_path))
                shortcut.Targetpath = str(bat_path)
                shortcut.WorkingDirectory = str(script_dir)
                shortcut.IconLocation = str(icon_path)
                shortcut.save()
                print(f"Shortcut created on Desktop with icon: {shortcut_path}")
            except Exception as e:
                print(f"Error creating shortcut: {e!s}")

        except Exception as e:
            print(f"Error creating batch file: {e!s}")
            raise


if __name__ == "__main__":
    create_bat_shortcut()
