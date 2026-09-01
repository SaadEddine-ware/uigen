"""Example: Admin Dashboard with uigen.

This example shows how to build a complete admin dashboard
using uigen's Python API. Run with:

    python examples/dashboard.py

Then open dist/index.html in your browser.
"""

from uigen import App, Model, ui


# Define data models
class User(Model):
    name: str
    email: str
    role: str = "viewer"
    active: bool = True


class Product(Model):
    name: str
    price: float
    category: str
    stock: int = 0


# Sample data
users = [
    {"name": "Alice Johnson", "email": "alice@example.com", "role": "admin", "active": True},
    {"name": "Bob Smith", "email": "bob@example.com", "role": "editor", "active": True},
    {"name": "Charlie Brown", "email": "charlie@example.com", "role": "viewer", "active": False},
    {"name": "Diana Prince", "email": "diana@example.com", "role": "editor", "active": True},
]

products = [
    {"name": "Laptop Pro", "price": 1299.99, "category": "Electronics", "stock": 45},
    {"name": "Wireless Mouse", "price": 29.99, "category": "Accessories", "stock": 150},
    {"name": "Monitor 4K", "price": 599.99, "category": "Electronics", "stock": 23},
    {"name": "Keyboard Mechanical", "price": 89.99, "category": "Accessories", "stock": 67},
]


# Build the dashboard UI
dashboard = ui.page(
    ui.heading("Admin Dashboard", level=1),
    ui.text("Welcome back! Here's what's happening today."),
    ui.stack(
        # Stats cards
        ui.grid(
            ui.card(
                ui.heading("Total Users", level=3),
                ui.text(f"{len(users)}"),
            ),
            ui.card(
                ui.heading("Active Products", level=3),
                ui.text(f"{len(products)}"),
            ),
            ui.card(
                ui.heading("Revenue", level=3),
                ui.text(f"${sum(p['price'] * p['stock'] for p in products):,.2f}"),
            ),
            columns=3,
        ),
        # Users table
        ui.card(
            ui.heading("Users", level=2),
            ui.table(data=users, columns=["name", "email", "role", "active"]),
            ui.button("Add User", onclick="showModal('user-modal')"),
        ),
        # Products table
        ui.card(
            ui.heading("Products", level=2),
            ui.table(data=products, columns=["name", "price", "category", "stock"]),
            ui.button("Add Product", onclick="showModal('product-modal')"),
        ),
        spacing="lg",
    ),
    # Add User Modal
    ui.modal(
        ui.form(
            ui.input("name", label="Name", placeholder="Enter name"),
            ui.input("email", label="Email", type="email", placeholder="Enter email"),
            ui.select("role", options=["admin", "editor", "viewer"], label="Role"),
            ui.button("Save", variant="primary"),
        ),
        title="Add New User",
    ),
    # Add Product Modal
    ui.modal(
        ui.form(
            ui.input("name", label="Name", placeholder="Product name"),
            ui.input("price", label="Price", type="number", placeholder="0.00"),
            ui.input("category", label="Category", placeholder="Category"),
            ui.input("stock", label="Stock", type="number", placeholder="0"),
            ui.button("Save", variant="primary"),
        ),
        title="Add New Product",
    ),
    title="Admin Dashboard",
)


# Create and render the app
app = App(title="Admin Dashboard", pages=[dashboard])

if __name__ == "__main__":
    output = app.render("lnative", output="./dist")
    print(f"Dashboard generated at {output}/index.html")
    print("Open it in your browser to see the result!")
