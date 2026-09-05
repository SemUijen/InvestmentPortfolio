"""Startup screen with navigation options (PySide6)."""

from pathlib import Path
from typing import TYPE_CHECKING

from PySide6.QtCore import QProcess, Qt
from PySide6.QtWidgets import QLabel, QPushButton

from .base_screen import BaseScreen
from .settings_dialog import EnvSettingsDialog

if TYPE_CHECKING:
    from investment_gui.application.application import MainApplication


class StartupScreen(BaseScreen):
    """Startup screen with navigation options."""

    def _open_settings(self) -> None:
        """Open the environment settings popup."""
        EnvSettingsDialog(self).exec()

    def __init__(self, app_controller: "MainApplication") -> None:
        super().__init__(app_controller)

        title = QLabel("Stock Investment Manager")
        font = title.font()
        font.setPointSize(16)
        font.setBold(True)
        title.setFont(font)
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(title)
        self.layout.addSpacing(30)

        data_input_btn = QPushButton("Data Input")
        data_input_btn.clicked.connect(self.app_controller.show_data_input_screen)
        self.layout.addWidget(data_input_btn)

        options_btn = QPushButton("Add Investment Options")
        options_btn.clicked.connect(self.app_controller.show_investment_options_screen)
        self.layout.addWidget(options_btn)

        self.pipeline_btn = QPushButton("Run Medaillon Pipeline")
        self.pipeline_btn.clicked.connect(self.run_medaillon_pipeline)
        self.layout.addWidget(self.pipeline_btn)

        settings_btn = QPushButton("Settings")
        settings_btn.clicked.connect(self._open_settings)
        self.layout.addWidget(settings_btn)

        self.layout.addStretch()

        # Async process for the pipeline; created once, reused per run.
        self._pipeline = QProcess(self)
        self._pipeline.finished.connect(self._on_pipeline_finished)
        self._pipeline.errorOccurred.connect(self._on_pipeline_error)

    # ---------------------------------------------------------------- pipeline
    def run_medaillon_pipeline(self) -> None:
        """Run the Medaillon ETL pipeline without blocking the UI."""
        if self._pipeline.state() != QProcess.ProcessState.NotRunning:
            return  # already running

        docker_dir = Path(__file__).resolve().parents[3] / "docker"
        self._pipeline.setWorkingDirectory(str(docker_dir))

        self.pipeline_btn.setEnabled(False)
        self.pipeline_btn.setText("Pipeline running…")
        self._pipeline.start(
            "docker-compose", ["run", "--rm", "run-medaillon-pipeline"]
        )

    def _on_pipeline_finished(self, exit_code: int, _status) -> None:
        self._reset_pipeline_button()
        if exit_code == 0:
            self.app_controller.show_info("Medaillon pipeline completed successfully!")
        else:
            stderr = bytes(self._pipeline.readAllStandardError()).decode(errors="replace")
            self.app_controller.show_error(
                f"Medaillon pipeline failed (exit code {exit_code}).\n\n{stderr[-2000:]}"
            )

    def _on_pipeline_error(self, _error) -> None:
        """Fires when the process could not start at all (e.g. command not found)."""
        self._reset_pipeline_button()
        self.app_controller.show_error(
            "Could not start the pipeline: "
            f"{self._pipeline.errorString()} (is docker-compose installed and on PATH?)"
        )

    def _reset_pipeline_button(self) -> None:
        self.pipeline_btn.setEnabled(True)
        self.pipeline_btn.setText("Run Medaillon Pipeline")