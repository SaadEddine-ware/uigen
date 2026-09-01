"""Tests for the core uigen module."""

from uigen import App, Model, ui


class TestModel:
    def test_basic_model(self):
        class User(Model):
            name: str
            email: str
            role: str = "viewer"

        user = User(name="Alice", email="alice@example.com")
        assert user.name == "Alice"
        assert user.role == "viewer"

    def test_model_to_dict(self):
        class User(Model):
            name: str
            email: str

        user = User(name="Bob", email="bob@example.com")
        assert user.to_dict() == {"name": "Bob", "email": "bob@example.com"}

    def test_model_fields(self):
        class User(Model):
            name: str
            email: str
            role: str = "viewer"

        fields = User.fields()
        assert len(fields) == 3
        assert fields[0].name == "name"
        assert fields[2].name == "role"


class TestUI:
    def test_heading(self):
        h = ui.heading("Hello", level=2)
        assert h.tag == "h2"
        assert h.text == "Hello"

    def test_button(self):
        b = ui.button("Click me", variant="danger")
        assert b.text == "Click me"
        assert b.variant == "danger"

    def test_card(self):
        h = ui.heading("Title")
        t = ui.text("Content")
        card = ui.card(h, t)
        assert len(card.children) == 2

    def test_table_from_data(self):
        data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
        table = ui.table(data=data)
        assert table.columns == ["name", "age"]
        assert len(table.rows) == 2


class TestCompiler:
    def test_app_creation(self):
        app = App(title="Test App")
        assert app.title == "Test App"
        assert len(app.pages) == 0

    def test_app_with_page(self):
        page = ui.page(ui.card(ui.heading("Hello")), title="Home")
        app = App(title="Test", pages=[page])
        assert len(app.pages) == 1
