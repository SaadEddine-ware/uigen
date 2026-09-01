"""Tests for the Flask renderer."""

from uigen import App, Model, ui
from uigen.renderers.lflask import LFlaskRenderer


class TestLFlaskRenderer:
    def setup_method(self):
        self.renderer = LFlaskRenderer()

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
        assert "<a" in html or "<button" in html

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

    def test_generate_app_py(self):
        app_py = self.renderer.generate_app_py("My App", ["index", "about"])
        assert "from flask import Flask" in app_py
        assert '@app.route("/")' in app_py
        assert "def index():" in app_py
        assert '@app.route("/about")' in app_py

    def test_generate_base_html(self):
        base = self.renderer.generate_base_html("Test App")
        assert "Test App" in base
        assert "tailwindcss" in base
        assert 'block content' in base

    def test_generate_requirements(self):
        req = self.renderer.generate_requirements()
        assert "flask" in req


class TestFlaskRendering:
    def test_render_produces_files(self, tmp_path):
        page = ui.page(
            ui.card(ui.heading("Test")),
            title="Test Page",
        )
        app = App(title="Test App", pages=[page])
        output = app.render("lflask", output=str(tmp_path / "flask_output"))

        assert output.exists()
        assert (output / "app.py").exists()
        assert (output / "requirements.txt").exists()
        assert (output / "templates" / "base.html").exists()
        assert (output / "templates" / "pages" / "test_page.html").exists()

    def test_render_multiple_pages(self, tmp_path):
        page1 = ui.page(ui.heading("Home"), title="Home")
        page2 = ui.page(ui.heading("About"), title="About")
        app = App(title="Multi", pages=[page1, page2])
        output = app.render("lflask", output=str(tmp_path / "flask_output"))

        assert (output / "templates" / "pages" / "home.html").exists()
        assert (output / "templates" / "pages" / "about.html").exists()

    def test_app_py_has_routes(self, tmp_path):
        page = ui.page(ui.heading("Dashboard"), title="Dashboard")
        app = App(title="My App", pages=[page])
        output = app.render("lflask", output=str(tmp_path / "flask_output"))

        app_py = (output / "app.py").read_text()
        assert "def dashboard():" in app_py
        assert "render_template" in app_py
