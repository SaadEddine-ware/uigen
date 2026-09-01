"""Theme customization system for uigen."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ColorPalette:
    """Color palette for themes."""

    primary: str = "blue"
    secondary: str = "gray"
    success: str = "green"
    danger: str = "red"
    warning: str = "yellow"
    info: str = "blue"

    # Specific shades
    primary_500: str = "#3b82f6"
    primary_600: str = "#2563eb"
    primary_700: str = "#1d4ed8"

    gray_100: str = "#f3f4f6"
    gray_200: str = "#e5e7eb"
    gray_300: str = "#d1d5db"
    gray_500: str = "#6b7280"
    gray_600: str = "#4b5563"
    gray_700: str = "#374151"
    gray_900: str = "#111827"


@dataclass
class Typography:
    """Typography settings."""

    font_family: str = "Inter, system-ui, sans-serif"
    font_size_xs: str = "0.75rem"
    font_size_sm: str = "0.875rem"
    font_size_base: str = "1rem"
    font_size_lg: str = "1.125rem"
    font_size_xl: str = "1.25rem"
    font_size_2xl: str = "1.5rem"
    font_size_3xl: str = "1.875rem"

    font_weight_normal: str = "400"
    font_weight_medium: str = "500"
    font_weight_semibold: str = "600"
    font_weight_bold: str = "700"


@dataclass
class Spacing:
    """Spacing settings."""

    xs: str = "0.25rem"
    sm: str = "0.5rem"
    md: str = "1rem"
    lg: str = "1.5rem"
    xl: str = "2rem"
    xxl: str = "3rem"


@dataclass
class BorderRadius:
    """Border radius settings."""

    none: str = "0"
    sm: str = "0.25rem"
    md: str = "0.375rem"
    lg: str = "0.5rem"
    xl: str = "0.75rem"
    full: str = "9999px"


@dataclass
class Shadows:
    """Box shadow settings."""

    none: str = "none"
    sm: str = "0 1px 2px 0 rgb(0 0 0 / 0.05)"
    md: str = "0 4px 6px -1px rgb(0 0 0 / 0.1)"
    lg: str = "0 10px 15px -3px rgb(0 0 0 / 0.1)"
    xl: str = "0 20px 25px -5px rgb(0 0 0 / 0.1)"


@dataclass
class Theme:
    """Complete theme configuration."""

    name: str = "default"
    colors: ColorPalette = field(default_factory=ColorPalette)
    typography: Typography = field(default_factory=Typography)
    spacing: Spacing = field(default_factory=Spacing)
    border_radius: BorderRadius = field(default_factory=BorderRadius)
    shadows: Shadows = field(default_factory=Shadows)

    # Custom CSS variables
    css_variables: dict[str, str] = field(default_factory=dict)

    def to_css(self) -> str:
        """Generate CSS custom properties from theme."""
        vars_dict = {
            "--color-primary": self.colors.primary_500,
            "--color-primary-hover": self.colors.primary_600,
            "--color-primary-active": self.colors.primary_700,
            "--color-gray-100": self.colors.gray_100,
            "--color-gray-200": self.colors.gray_200,
            "--color-gray-300": self.colors.gray_300,
            "--color-gray-500": self.colors.gray_500,
            "--color-gray-600": self.colors.gray_600,
            "--color-gray-700": self.colors.gray_700,
            "--color-gray-900": self.colors.gray_900,
            "--font-family": self.typography.font_family,
            "--font-size-sm": self.typography.font_size_sm,
            "--font-size-base": self.typography.font_size_base,
            "--font-size-lg": self.typography.font_size_lg,
            "--font-size-xl": self.typography.font_size_xl,
            "--font-size-2xl": self.typography.font_size_2xl,
            "--font-size-3xl": self.typography.font_size_3xl,
            "--spacing-sm": self.spacing.sm,
            "--spacing-md": self.spacing.md,
            "--spacing-lg": self.spacing.lg,
            "--spacing-xl": self.spacing.xl,
            "--radius-md": self.border_radius.md,
            "--radius-lg": self.border_radius.lg,
            "--shadow-sm": self.shadows.sm,
            "--shadow-md": self.shadows.md,
            "--shadow-lg": self.shadows.lg,
        }

        # Add custom CSS variables
        vars_dict.update(self.css_variables)

        lines = [f"  {key}: {value};" for key, value in vars_dict.items()]
        return ":root {\n" + "\n".join(lines) + "\n}"

    def to_tailwind_config(self) -> dict[str, Any]:
        """Generate Tailwind CSS configuration."""
        return {
            "theme": {
                "extend": {
                    "colors": {
                        "primary": {
                            "50": "#eff6ff",
                            "100": "#dbeafe",
                            "500": self.colors.primary_500,
                            "600": self.colors.primary_600,
                            "700": self.colors.primary_700,
                        },
                    },
                    "fontFamily": {
                        "sans": self.typography.font_family.split(", "),
                    },
                    "borderRadius": {
                        "md": self.border_radius.md,
                        "lg": self.border_radius.lg,
                    },
                    "boxShadow": {
                        "sm": self.shadows.sm,
                        "md": self.shadows.md,
                        "lg": self.shadows.lg,
                    },
                },
            },
        }


# Predefined themes
THEMES: dict[str, Theme] = {
    "default": Theme(name="default"),
    "dark": Theme(
        name="dark",
        colors=ColorPalette(
            primary="blue",
            gray_100="#1f2937",
            gray_200="#374151",
            gray_300="#4b5563",
            gray_500="#6b7280",
            gray_600="#9ca3af",
            gray_700="#d1d5db",
            gray_900="#f9fafb",
        ),
    ),
    "emerald": Theme(
        name="emerald",
        colors=ColorPalette(
            primary="emerald",
            primary_500="#10b981",
            primary_600="#059669",
            primary_700="#047857",
        ),
    ),
    "purple": Theme(
        name="purple",
        colors=ColorPalette(
            primary="purple",
            primary_500="#8b5cf6",
            primary_600="#7c3aed",
            primary_700="#6d28d9",
        ),
    ),
    "rose": Theme(
        name="rose",
        colors=ColorPalette(
            primary="rose",
            primary_500="#f43f5e",
            primary_600="#e11d48",
            primary_700="#be123c",
        ),
    ),
}


def get_theme(name: str = "default") -> Theme:
    """Get a theme by name."""
    return THEMES.get(name, THEMES["default"])


def register_theme(name: str, theme: Theme) -> None:
    """Register a custom theme."""
    THEMES[name] = theme


def list_themes() -> list[str]:
    """List all available themes."""
    return list(THEMES.keys())
