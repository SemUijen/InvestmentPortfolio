"""Base screen and input field definitions (PySide6).

Replaces the tkinter version:
- InputField no longer carries a tk variable; it declares label, python type,
  and optional placeholder. Widgets are created by BaseScreen.
- Placeholders are native Qt placeholders (display-only), so placeholder text
  can never leak into submitted values.
- Numeric fields get validators, so invalid characters can't be typed at all.
"""

import datetime
from dataclasses import dataclass
from typing import TYPE_CHECKING

from PySide6.QtCore import QDate, QLocale
from PySide6.QtGui import QDoubleValidator, QIntValidator
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

if TYPE_CHECKING:
    from investment_gui.application.application import MainApplication


@dataclass
class InputField:
    """Declares one input on a screen.

    input_type: str, float, int, or datetime.date
    choices: when set, the field renders as a dropdown with these options
    """

    label: str
    input_type: type
    placeholder: str | None = None
    choices: list[str] | None = None


class ValidationError(Exception):
    """Raised by get_values() when one or more fields are invalid/empty."""


class BaseScreen(QWidget):
    """Base class for all screens with common form functionality."""

    def __init__(self, app_controller: "MainApplication") -> None:
        super().__init__()
        self.app_controller = app_controller

        # Screens add their own widgets to self.layout;
        # input fields go into self.form (label/field rows).
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.form = QFormLayout()
        self.layout.addLayout(self.form)

        # label -> (InputField, widget)
        self._fields: dict[str, tuple[InputField, QWidget]] = {}

    # ------------------------------------------------------------------ build
    def add_input_fields(self, input_fields: list[InputField]) -> None:
        """Create one form row per InputField."""
        for field in input_fields:
            widget = self._create_widget(field)
            self.form.addRow(f"{field.label}:", widget)
            self._fields[field.label] = (field, widget)

    def _create_widget(self, field: InputField) -> QWidget:
        if field.choices is not None:
            combo = QComboBox()
            combo.addItems(field.choices)
            return combo

        if field.input_type is datetime.date:
            date_edit = QDateEdit()
            date_edit.setCalendarPopup(True)
            date_edit.setDisplayFormat("yyyy-MM-dd")
            date_edit.setDate(QDate.currentDate())
            return date_edit

        line = QLineEdit()
        if field.placeholder:
            line.setPlaceholderText(field.placeholder)

        if field.input_type is float:
            validator = QDoubleValidator()
            # Force '.' as decimal separator regardless of system locale
            validator.setLocale(QLocale(QLocale.Language.C))
            validator.setNotation(QDoubleValidator.Notation.StandardNotation)
            line.setValidator(validator)
        elif field.input_type is int:
            line.setValidator(QIntValidator())

        return line

    # ------------------------------------------------------------------ read
    def get_values(self) -> dict[str, str | float | int | datetime.date]:
        """Return {label: typed value} for all fields.

        Raises ValidationError listing every empty/invalid field, so the
        caller can show one message instead of failing field by field.
        """
        values: dict[str, str | float | int | datetime.date] = {}
        problems: list[str] = []

        for label, (field, widget) in self._fields.items():
            if isinstance(widget, QComboBox):
                values[label] = widget.currentText()
                continue

            if isinstance(widget, QDateEdit):
                values[label] = widget.date().toPython()
                continue

            assert isinstance(widget, QLineEdit)
            text = widget.text().strip()
            if not text:
                problems.append(f"'{label}' is empty")
                continue
            try:
                if field.input_type is float:
                    values[label] = float(text)
                elif field.input_type is int:
                    values[label] = int(text)
                else:
                    values[label] = text
            except ValueError:
                problems.append(f"'{label}' is not a valid {field.input_type.__name__}")

        if problems:
            raise ValidationError("\n".join(problems))
        return values

    def clear_fields(self) -> None:
        """Reset all inputs (useful after a successful submit)."""
        for _, widget in self._fields.values():
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QDateEdit):
                widget.setDate(QDate.currentDate())
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)