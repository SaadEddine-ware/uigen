"""Additional tests for uigen components and renderers."""

from uigen import App, Model, ui
from uigen.renderers.lnative import LNativeRenderer


class TestInput:
    def test_input_basic(self):
        inp = ui.input("email")
        assert inp.name == "email"
        assert inp.input_type == "text"
        assert inp.label == "Email"

    def test_input_with_label(self):
        inp = ui.input("email", label="Your Email")
        assert inp.label == "Your Email"

    def test_input_required(self):
        inp = ui.input("email", required=True)
        assert inp.required is True

    def test_input_type(self):
        inp = ui.input("password", type="password")
        assert inp.input_type == "password"


class TestSelect:
    def test_select_basic(self):
        sel = ui.select("role", options=["admin", "user"])
        assert sel.name == "role"
        assert sel.options == ["admin", "user"]

    def test_select_with_label(self):
        sel = ui.select("role", options=["admin"], label="User Role")
        assert sel.label == "User Role"


class TestForm:
    def test_form_basic(self):
        form = ui.form(
            ui.input("name"),
            ui.input("email"),
        )
        assert len(form.children) == 2
        assert form.method == "POST"

    def test_form_with_action(self):
        form = ui.form(ui.input("name"), action="/submit")
        assert form.action == "/submit"


class TestModal:
    def test_modal_basic(self):
        modal = ui.modal(
            ui.heading("Title"),
            ui.text("Content"),
        )
        assert len(modal.children) == 2
        assert modal.title == ""

    def test_modal_with_title(self):
        modal = ui.modal(ui.text("Hi"), title="Welcome")
        assert modal.title == "Welcome"


class TestGrid:
    def test_grid_default_columns(self):
        grid = ui.grid(ui.text("A"), ui.text("B"))
        assert grid.attrs.get("columns") == 2

    def test_grid_custom_columns(self):
        grid = ui.grid(ui.text("A"), ui.text("B"), ui.text("C"), columns=3)
        assert grid.attrs.get("columns") == 3


class TestStack:
    def test_stack_default_spacing(self):
        stack = ui.stack(ui.text("A"), ui.text("B"))
        assert stack.attrs.get("spacing") == "md"

    def test_stack_custom_spacing(self):
        stack = ui.stack(ui.text("A"), ui.text("B"), spacing="lg")
        assert stack.attrs.get("spacing") == "lg"


class TestLNativeRenderer:
    def setup_method(self):
        self.renderer = LNativeRenderer()

    def test_render_heading(self):
        from uigen.core.components import Heading
        h = Heading(text="Hello", level=1)
        html = self.renderer.render_component(h)
        assert "<h1" in html
        assert "Hello" in html

    def test_render_button(self):
        from uigen.core.components import Button
        b = Button(text="Click", variant="primary")
        html = self.renderer.render_component(b)
        assert "Click" in html
        assert "button" in html

    def test_render_text(self):
        from uigen.core.components import Text
        t = Text(text="Hello world")
        html = self.renderer.render_component(t)
        assert "<p" in html
        assert "Hello world" in html

    def test_render_table(self):
        from uigen.core.components import Table
        table = Table(
            columns=["name", "age"],
            rows=[{"name": "Alice", "age": 30}],
        )
        html = self.renderer.render_component(table)
        assert "<table" in html
        assert "Alice" in html

    def test_render_empty_table(self):
        from uigen.core.components import Table
        table = Table()
        html = self.renderer.render_component(table)
        assert "No data" in html


class TestAppRendering:
    def test_render_produces_html(self, tmp_path):
        page = ui.page(
            ui.card(ui.heading("Test")),
            title="Test Page",
        )
        app = App(title="Test App", pages=[page])
        output = app.render("lnative", output=str(tmp_path / "output"))
        assert output.exists()
        assert (output / "index.html").exists()

    def test_render_multiple_pages(self, tmp_path):
        page1 = ui.page(ui.heading("Page 1"), title="Page 1")
        page2 = ui.page(ui.heading("Page 2"), title="Page 2")
        app = App(title="Multi", pages=[page1, page2])
        output = app.render("lnative", output=str(tmp_path / "output"))
        assert (output / "index.html").exists()
        assert (output / "page_1.html").exists()
