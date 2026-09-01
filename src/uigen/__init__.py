"""uigen — Write UI logic once, deploy anywhere."""

from uigen.core.api import ui
from uigen.core.compiler import App
from uigen.core.schema import Field, Model
from uigen.theme import Theme, get_theme, list_themes, register_theme

__version__ = "0.1.0"

__all__ = [
    "Model",
    "Field",
    "ui",
    "App",
    "Theme",
    "get_theme",
    "list_themes",
    "register_theme",
]
