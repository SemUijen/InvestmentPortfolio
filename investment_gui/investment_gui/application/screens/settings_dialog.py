"""Dialog for viewing and setting environment variables (PySide6).

Saves to the project's .env file and updates os.environ for the running
session, so changes take effect without restarting the app.
"""

import os
import re
from pathlib import Path

from dotenv import dotenv_values, set_key
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


# This file lives at: investment_gui/investment_gui/application/screens/settings_dialog.py
_PARENTS = Path(__file__).resolve().parents
GUI_ENV_PATH = _PARENTS[3] / ".env"  # investment_gui/investment_gui/.env
DOCKER_ENV_PATH = _PARENTS[3] / "docker" / "run_medaillon" / ".env"
ENV_PATHS = (GUI_ENV_PATH, DOCKER_ENV_PATH)


class EnvSettingsDialog(QDialog):
    """Small popup for editing the env variables the app depends on."""

    # (env var name, human label, is_directory)
    ENV_VARS: list[tuple[str, str, bool]] = [
        ("DATA_DIR", "Data directory", True),
        ("ALPHAVANTAGE_API_KEY", "AlphaVantage API key", False),
    ]

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumWidth(450)

        layout = QVBoxLayout(self)
        form = QFormLayout()
        layout.addLayout(form)

        # Prefill from the saved .env file so values reappear on reopen;
        # fall back to the live environment for values set another way.
        saved = dotenv_values(GUI_ENV_PATH) if GUI_ENV_PATH.is_file() else {}

        self._edits: dict[str, QLineEdit] = {}
        for name, label, is_directory in self.ENV_VARS:
            edit = QLineEdit(saved.get(name) or os.getenv(name, ""))
            self._edits[name] = edit

            if is_directory:
                row = QHBoxLayout()
                row.addWidget(edit)
                browse = QPushButton("Browse…")
                browse.clicked.connect(
                    lambda _=False, e=edit: self._browse_directory(e)
                )
                row.addWidget(browse)
                form.addRow(f"{label}:", row)
            else:
                form.addRow(f"{label}:", edit)

        hint = QLabel("Saved to:\n" + "\n".join(str(p) for p in ENV_PATHS))
        hint.setStyleSheet("color: gray;")
        layout.addWidget(hint)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    # ------------------------------------------------------------------ utils
    def _browse_directory(self, edit: QLineEdit) -> None:
        start_dir = edit.text() or str(Path.home())
        directory = QFileDialog.getExistingDirectory(
            self, "Select data directory", start_dir
        )
        if directory:
            edit.setText(directory)

    # ------------------------------------------------------------------- save
    @staticmethod
    def _normalize_path(value: str) -> str:
        """Convert a Windows-style path (C:\\...) to its WSL form (/mnt/c/...).

        Only applies when running on a non-Windows OS; other values pass
        through unchanged.
        """
        if os.name != "nt" and re.match(r"^[A-Za-z]:[\\/]", value):
            drive = value[0].lower()
            rest = value[2:].replace("\\", "/")
            return f"/mnt/{drive}{rest}"
        return value

    def _save(self) -> None:
        for env_path in ENV_PATHS:
            env_path.parent.mkdir(parents=True, exist_ok=True)
            env_path.touch(exist_ok=True)
            for name, edit in self._edits.items():
                value = self._normalize_path(edit.text().strip())
                if value:
                    set_key(str(env_path), name, value)
                    os.environ[name] = value  # effective immediately, no restart
        self.accept()