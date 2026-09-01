"""Example: Perfume Store Website with uigen.

A complete e-commerce perfume store with:
- Product catalog with categories
- Featured products
- Shopping cart UI
- Contact form
- About section

Run with:
    python examples/perfume_store.py

Then open dist/index.html in your browser.
"""

from uigen import App, Model, ui
from uigen.core.components import Card


# ============================================================
# Data Models
# ============================================================

class Perfume(Model):
    name: str
    brand: str
    price: float
    category: str
    description: str = ""
    stock: int = 0


class Customer(Model):
    name: str
    email: str
    message: str = ""


# ============================================================
# Sample Data
# ============================================================

perfumes = [
    {
        "name": "Noir Essence",
        "brand": "Maison Lumiere",
        "price": 189.99,
        "category": "For Him",
        "description": "A sophisticated blend of leather, oud, and dark amber.",
        "stock": 15,
    },
    {
        "name": "Rose Elixir",
        "brand": "Jardin Secret",
        "price": 245.00,
        "category": "For Her",
        "description": "Bulgarian rose, peony, and a whisper of vanilla.",
        "stock": 8,
    },
    {
        "name": "Citrus Dusk",
        "brand": "Atelier Soleil",
        "price": 129.99,
        "category": "Unisex",
        "description": "Fresh bergamot, neroli, and white musk.",
        "stock": 22,
    },
    {
        "name": "Velvet Storm",
        "brand": "Maison Lumiere",
        "price": 199.99,
        "category": "For Him",
        "description": "Sandalwood, black pepper, and smoky vetiver.",
        "stock": 12,
    },
    {
        "name": "Fleur d'Or",
        "brand": "Jardin Secret",
        "price": 275.00,
        "category": "For Her",
        "description": "Golden orchid, jasmine sambac, and honeyed amber.",
        "stock": 5,
    },
    {
        "name": "Aqua Verte",
        "brand": "Atelier Soleil",
        "price": 149.99,
        "category": "Unisex",
        "description": "Green tea, sea salt, and driftwood.",
        "stock": 18,
    },
    {
        "name": "Midnight Rose",
        "brand": "Jardin Secret",
        "price": 225.00,
        "category": "For Her",
        "description": "Dark rose, blackcurrant, and creamy sandalwood.",
        "stock": 10,
    },
    {
        "name": "Cuir Royal",
        "brand": "Maison Lumiere",
        "price": 320.00,
        "category": "For Him",
        "description": "Royal leather, tobacco leaf, and aged cognac.",
        "stock": 3,
    },
]

featured = perfumes[:4]
new_arrivals = perfumes[4:]


# ============================================================
# Helper: Product Card
# ============================================================

def product_card(product: dict) -> Card:
    """Create a product card component."""
    stock_label = "In Stock" if product["stock"] > 0 else "Out of Stock"
    stock_variant = "secondary" if product["stock"] > 0 else "danger"

    return ui.card(
        ui.heading(f"{product['name']}", level=3),
        ui.text(f"by {product['brand']}"),
        ui.text(product["description"]),
        ui.stack(
            ui.heading(f"${product['price']:.2f}", level=2),
            ui.text(f"Category: {product['category']}"),
            spacing="sm",
        ),
        ui.stack(
            ui.button(stock_label, variant=stock_variant),
            ui.button("Add to Cart", variant="primary"),
            spacing="sm",
        ),
    )


# ============================================================
# Page 1: Home
# ============================================================

home_page = ui.page(
    # Hero Section
    ui.card(
        ui.heading("Discover Your Signature Scent", level=1),
        ui.text(
            "Explore our curated collection of luxury fragrances from "
            "the world's finest perfume houses."
        ),
        ui.stack(
            ui.button("Shop Now", variant="primary"),
            ui.button("View Collections", variant="secondary"),
            spacing="sm",
        ),
    ),

    # Featured Products
    ui.card(
        ui.heading("Featured Fragrances", level=2),
        ui.text("Our most beloved scents, chosen by connoisseurs."),
        ui.grid(
            *[product_card(p) for p in featured],
            columns=2,
        ),
    ),

    # Categories
    ui.card(
        ui.heading("Shop by Category", level=2),
        ui.grid(
            ui.card(
                ui.heading("For Him", level=3),
                ui.text("Bold, sophisticated, and unforgettable."),
                ui.button("Explore", variant="primary"),
            ),
            ui.card(
                ui.heading("For Her", level=3),
                ui.text("Elegant, floral, and timeless."),
                ui.button("Explore", variant="primary"),
            ),
            ui.card(
                ui.heading("Unisex", level=3),
                ui.text("Fresh, modern, and versatile."),
                ui.button("Explore", variant="primary"),
            ),
            columns=3,
        ),
    ),

    # New Arrivals
    ui.card(
        ui.heading("New Arrivals", level=2),
        ui.text("The latest additions to our collection."),
        ui.grid(
            *[product_card(p) for p in new_arrivals],
            columns=2,
        ),
    ),

    # Newsletter
    ui.card(
        ui.heading("Join Our Newsletter", level=2),
        ui.text(
            "Subscribe for exclusive offers, new releases, and "
            "fragrance tips delivered to your inbox."
        ),
        ui.form(
            ui.input("email", label="Email Address", type="email",
                     placeholder="your@email.com"),
            ui.button("Subscribe", variant="primary"),
            action="/subscribe",
        ),
    ),

    title="Lumiere Parfums — Luxury Fragrances",
)


# ============================================================
# Page 2: Shop
# ============================================================

shop_page = ui.page(
    ui.heading("Our Collection", level=1),
    ui.text(f"Browse all {len(perfumes)} fragrances."),

    # Filter by Category
    ui.card(
        ui.heading("Filter by Category", level=3),
        ui.form(
            ui.select("category", options=["All", "For Him", "For Her", "Unisex"],
                     label="Category"),
            ui.button("Apply Filter", variant="primary"),
        ),
    ),

    # Product Grid
    ui.grid(
        *[product_card(p) for p in perfumes],
        columns=2,
    ),

    title="Shop — Lumiere Parfums",
)


# ============================================================
# Page 3: About
# ============================================================

about_page = ui.page(
    ui.heading("Our Story", level=1),
    ui.card(
        ui.text(
            "Founded in 2020, Lumiere Parfums was born from a passion "
            "for exceptional fragrances. We partner with independent "
            "perfumers around the world to bring you scents that tell "
            "stories and evoke emotions."
        ),
        ui.text(
            "Every fragrance in our collection is carefully selected "
            "for its artistry, quality, and uniqueness. We believe "
            "that a great perfume is more than a scent — it's an "
            "experience, a memory, a statement."
        ),
    ),

    ui.card(
        ui.heading("Our Values", level=2),
        ui.grid(
            ui.card(
                ui.heading("Quality First", level=3),
                ui.text(
                    "We only carry fragrances made with the finest "
                    "ingredients from around the world."
                ),
            ),
            ui.card(
                ui.heading("Sustainability", level=3),
                ui.text(
                    "Eco-friendly packaging and responsible sourcing "
                    "are at the heart of everything we do."
                ),
            ),
            ui.card(
                ui.heading("Community", level=3),
                ui.text(
                    "We support independent perfumers and celebrate "
                    "the art of fragrance creation."
                ),
            ),
            columns=3,
        ),
    ),

    ui.card(
        ui.heading("Contact Us", level=2),
        ui.text("Have a question? We'd love to hear from you."),
        ui.form(
            ui.input("name", label="Your Name", placeholder="John Doe"),
            ui.input("email", label="Email", type="email",
                     placeholder="john@example.com"),
            ui.input("message", label="Message",
                     placeholder="How can we help?"),
            ui.button("Send Message", variant="primary"),
            action="/contact",
        ),
    ),

    title="About — Lumiere Parfums",
)


# ============================================================
# Build the App
# ============================================================

app = App(
    title="Lumiere Parfums",
    models=[Perfume, Customer],
    pages=[home_page, shop_page, about_page],
)


if __name__ == "__main__":
    import sys

    renderer = sys.argv[1] if len(sys.argv) > 1 else "lnative"

    if renderer == "lreact":
        output = app.render("lreact", output="./react-app")
        print(f"React app generated at {output}/")
        print("To run:")
        print("  cd react-app")
        print("  npm install")
        print("  npm start")
    else:
        output = app.render("lnative", output="./dist")
        print(f"Perfume store generated at {output}/")
        print("Files:")
        print("  - index.html  (Home)")
        print("  - page_1.html (Shop)")
        print("  - page_2.html (About)")
        print("\nOpen index.html in your browser to view the store!")
