import platform
import sys
from pathlib import Path


def create_bat_shortcut():
    # Get absolute paths
    script_dir = Path(__file__).resolve().parent  # Main folder of the repo
    main_script = script_dir / "app.py"
    python_exe = Path(sys.executable).resolve()

    print(f"Script path: {main_script}")
    print(f"Python executable: {python_exe}")
    print(f"Saving shortcut in: {script_dir}")

    if platform.system() == "Windows":
        # Save batch file in the same directory as this script
        bat_path = script_dir / "Data_Input_App.bat"
        bat_content = (
            f"@echo off\n"
            f"set PYTHONPATH={script_dir.parent.parent}\n"
            f'"{python_exe}" "{main_script}"\n'
            f"pause"
        )
        try:
            with open(bat_path, "w") as f:
                f.write(bat_content)
            print(f"Batch file created successfully at: {bat_path}")

        except Exception as e:
            print(f"Error creating batch file: {e!s}")
            raise


if __name__ == "__main__":
    create_bat_shortcut()
