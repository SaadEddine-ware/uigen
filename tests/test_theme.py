"""Tests for the theme system."""

from uigen import App, Model, ui, Theme, get_theme, list_themes, register_theme
from uigen.theme import ColorPalette, Typography


class TestTheme:
    def test_default_theme(self):
        theme = get_theme("default")
        assert theme.name == "default"
        assert theme.colors.primary == "blue"

    def test_dark_theme(self):
        theme = get_theme("dark")
        assert theme.name == "dark"

    def test_emerald_theme(self):
        theme = get_theme("emerald")
        assert theme.colors.primary == "emerald"
        assert theme.colors.primary_500 == "#10b981"

    def test_purple_theme(self):
        theme = get_theme("purple")
        assert theme.colors.primary == "purple"

    def test_list_themes(self):
        themes = list_themes()
        assert "default" in themes
        assert "dark" in themes
        assert "emerald" in themes
        assert "purple" in themes
        assert "rose" in themes

    def test_to_css(self):
        theme = get_theme("default")
        css = theme.to_css()
        assert ":root" in css
        assert "--color-primary" in css
        assert "#3b82f6" in css

    def test_custom_theme(self):
        custom = Theme(
            name="custom",
            colors=ColorPalette(primary="teal", primary_500="#14b8a6"),
        )
        register_theme("custom", custom)
        assert "custom" in list_themes()
        assert get_theme("custom").colors.primary == "teal"

    def test_to_tailwind_config(self):
        theme = get_theme("default")
        config = theme.to_tailwind_config()
        assert "theme" in config
        assert "extend" in config["theme"]


class TestThemeRendering:
    def test_render_with_theme(self, tmp_path):
        page = ui.page(
            ui.card(ui.heading("Themed Page")),
            title="Themed",
        )
        app = App(title="Themed App", pages=[page], theme="emerald")
        output = app.render("lnative", output=str(tmp_path / "themed"))

        assert output.exists()
        html = (output / "index.html").read_text()
        assert "#10b981" in html  # Emerald primary color

    def test_render_dark_theme(self, tmp_path):
        page = ui.page(
            ui.card(ui.heading("Dark Page")),
            title="Dark",
        )
        app = App(title="Dark App", pages=[page], theme="dark")
        output = app.render("lnative", output=str(tmp_path / "dark"))

        html = (output / "index.html").read_text()
        assert "#1f2937" in html  # Dark theme gray
