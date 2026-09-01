"""Tests for the Django renderer."""

from uigen import App, Model, ui
from uigen.renderers.ldjango import LDjangoRenderer


class TestLDjangoRenderer:
    def setup_method(self):
        self.renderer = LDjangoRenderer()

    def test_render_heading(self):
        from uigen.core.components import Heading
        h = Heading(text="Hello", level=1)
        html = self.renderer.render_component(h)
        assert "<h1" in html
        assert "Hello" in html
        assert 'class=' in html

    def test_render_button(self):
        from uigen.core.components import Button
        b = Button(text="Click me", variant="primary")
        html = self.renderer.render_component(b)
        assert "Click me" in html
        assert "<a" in html

    def test_render_text(self):
        from uigen.core.components import Text
        t = Text(text="Hello world")
        html = self.renderer.render_component(t)
        assert "<p" in html
        assert "Hello world" in html

    def test_render_card(self):
        from uigen.core.components import Card, Heading
        card = Card(children=[Heading(text="Title", level=2)])
        html = self.renderer.render_component(card)
        assert "bg-white" in html
        assert "rounded-lg" in html
        assert "shadow-md" in html

    def test_render_table(self):
        from uigen.core.components import Table
        table = Table(
            columns=["name", "age"],
            rows=[{"name": "Alice", "age": 30}],
        )
        html = self.renderer.render_component(table)
        assert "<table" in html
        assert "for row in table_data" in html

    def test_render_empty_table(self):
        from uigen.core.components import Table
        table = Table()
        html = self.renderer.render_component(table)
        assert "No data" in html

    def test_render_input(self):
        from uigen.core.components import Input
        inp = Input(name="email", label="Email", input_type="email")
        html = self.renderer.render_component(inp)
        assert "Email" in html
        assert "email" in html
        assert "input" in html

    def test_render_select(self):
        from uigen.core.components import Select
        sel = Select(name="role", options=["admin", "user"], label="Role")
        html = self.renderer.render_component(sel)
        assert "Role" in html
        assert "for option in role_options" in html

    def test_to_snake_case(self):
        assert self.renderer._to_snake_case("Hello World") == "hello_world"
        assert self.renderer._to_snake_case("My App") == "my_app"
        assert self.renderer._to_snake_case("Admin Dashboard") == "admin_dashboard"

    def test_generate_views_py(self):
        views = self.renderer.generate_views_py("My App", ["index", "about"])
        assert "from django.shortcuts import render" in views
        assert "def index(request):" in views
        assert "def about(request):" in views
        assert "render(request" in views

    def test_generate_urls_py(self):
        urls = self.renderer.generate_urls_py(["index", "about"])
        assert "from django.urls import path" in urls
        assert 'path("", views.index' in urls
        assert 'path("about/"' in urls

    def test_generate_base_html(self):
        base = self.renderer.generate_base_html("Test App")
        assert "Test App" in base
        assert "tailwindcss" in base
        assert 'block content' in base
        assert 'load static' in base

    def test_generate_settings_py(self):
        settings = self.renderer.generate_settings_py("My Store")
        assert "SECRET_KEY" in settings
        assert "my_store" in settings
        assert "INSTALLED_APPS" in settings

    def test_generate_requirements(self):
        req = self.renderer.generate_requirements()
        assert "django" in req


class TestDjangoRendering:
    def test_render_produces_files(self, tmp_path):
        page = ui.page(
            ui.card(ui.heading("Test")),
            title="Test Page",
        )
        app = App(title="Test App", pages=[page])
        output = app.render("ldjango", output=str(tmp_path / "django_output"))

        assert output.exists()
        assert (output / "settings.py").exists()
        assert (output / "requirements.txt").exists()
        assert (output / "templates" / "base.html").exists()
        assert (output / "templates" / "pages" / "test_page.html").exists()
        assert (output / "test_app" / "views.py").exists()
        assert (output / "test_app" / "urls.py").exists()

    def test_render_multiple_pages(self, tmp_path):
        page1 = ui.page(ui.heading("Home"), title="Home")
        page2 = ui.page(ui.heading("About"), title="About")
        app = App(title="Multi", pages=[page1, page2])
        output = app.render("ldjango", output=str(tmp_path / "django_output"))

        assert (output / "templates" / "pages" / "home.html").exists()
        assert (output / "templates" / "pages" / "about.html").exists()

    def test_views_has_routes(self, tmp_path):
        page = ui.page(ui.heading("Dashboard"), title="Dashboard")
        app = App(title="My App", pages=[page])
        output = app.render("ldjango", output=str(tmp_path / "django_output"))

        views_py = (output / "my_app" / "views.py").read_text()
        assert "def dashboard(request):" in views_py
        assert "render(request" in views_py

    def test_urls_has_patterns(self, tmp_path):
        page = ui.page(ui.heading("Dashboard"), title="Dashboard")
        app = App(title="My App", pages=[page])
        output = app.render("ldjango", output=str(tmp_path / "django_output"))

        urls_py = (output / "my_app" / "urls.py").read_text()
        assert 'path("dashboard/"' in urls_py
