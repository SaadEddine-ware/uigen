"""Tests for the React renderer."""

from uigen import App, Model, ui
from uigen.renderers.lreact import LReactRenderer


class TestLReactRenderer:
    def setup_method(self):
        self.renderer = LReactRenderer()

    def test_render_heading(self):
        from uigen.core.components import Heading
        h = Heading(text="Hello", level=1)
        jsx = self.renderer.render_component(h)
        assert "<h1" in jsx
        assert "Hello" in jsx
        assert 'className=' in jsx

    def test_render_button(self):
        from uigen.core.components import Button
        b = Button(text="Click me", variant="primary")
        jsx = self.renderer.render_component(b)
        assert "Click me" in jsx
        assert "<button" in jsx
        assert 'className=' in jsx

    def test_render_text(self):
        from uigen.core.components import Text
        t = Text(text="Hello world")
        jsx = self.renderer.render_component(t)
        assert "<p" in jsx
        assert "Hello world" in jsx

    def test_render_card(self):
        from uigen.core.components import Card, Heading
        card = Card(children=[Heading(text="Title", level=2)])
        jsx = self.renderer.render_component(card)
        assert "bg-white" in jsx
        assert "rounded-lg" in jsx
        assert "shadow-md" in jsx

    def test_render_table(self):
        from uigen.core.components import Table
        table = Table(
            columns=["name", "age"],
            rows=[{"name": "Alice", "age": 30}],
        )
        jsx = self.renderer.render_component(table)
        assert "<table" in jsx
        assert "Alice" in jsx
        assert "className=" in jsx

    def test_render_empty_table(self):
        from uigen.core.components import Table
        table = Table()
        jsx = self.renderer.render_component(table)
        assert "No data" in jsx

    def test_render_input(self):
        from uigen.core.components import Input
        inp = Input(name="email", label="Email", input_type="email")
        jsx = self.renderer.render_component(inp)
        assert "Email" in jsx
        assert "email" in jsx
        assert "input" in jsx

    def test_render_select(self):
        from uigen.core.components import Select
        sel = Select(name="role", options=["admin", "user"], label="Role")
        jsx = self.renderer.render_component(sel)
        assert "Role" in jsx
        assert "admin" in jsx
        assert "select" in jsx

    def test_to_pascal_case(self):
        assert self.renderer._to_pascal_case("hello world") == "HelloWorld"
        assert self.renderer._to_pascal_case("my app") == "MyApp"
        assert self.renderer._to_pascal_case("admin dashboard") == "AdminDashboard"

    def test_to_var_name(self):
        assert self.renderer._to_var_name("Hello World") == "helloWorld"
        assert self.renderer._to_var_name("My App") == "myApp"

    def test_generate_package_json(self):
        pkg = self.renderer.generate_package_json("My Store")
        assert '"name": "my-store"' in pkg
        assert '"react"' in pkg
        assert '"react-dom"' in pkg

    def test_generate_index_html(self):
        html = self.renderer.generate_index_html("Test App")
        assert "Test App" in html
        assert "tailwindcss" in html
        assert 'id="root"' in html


class TestReactRendering:
    def test_render_produces_files(self, tmp_path):
        page = ui.page(
            ui.card(ui.heading("Test")),
            title="Test Page",
        )
        app = App(title="Test App", pages=[page])
        output = app.render("lreact", output=str(tmp_path / "react_output"))

        assert output.exists()
        assert (output / "package.json").exists()
        assert (output / "index.html").exists()
        assert (output / "src" / "App.tsx").exists()
        assert (output / "src" / "index.tsx").exists()
        assert (output / "src" / "components" / "TestPage.tsx").exists()

    def test_render_multiple_pages(self, tmp_path):
        page1 = ui.page(ui.heading("Home"), title="Home")
        page2 = ui.page(ui.heading("About"), title="About")
        app = App(title="Multi Page", pages=[page1, page2])
        output = app.render("lreact", output=str(tmp_path / "react_output"))

        assert (output / "src" / "components" / "Home.tsx").exists()
        assert (output / "src" / "components" / "About.tsx").exists()

    def test_react_component_has_imports(self, tmp_path):
        page = ui.page(
            ui.card(ui.heading("Dashboard")),
            title="Dashboard",
        )
        app = App(title="My App", pages=[page])
        output = app.render("lreact", output=str(tmp_path / "react_output"))

        component_file = output / "src" / "components" / "Dashboard.tsx"
        content = component_file.read_text()
        assert "import React" in content
        assert "useState" in content
