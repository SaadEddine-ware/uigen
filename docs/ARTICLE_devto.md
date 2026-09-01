---
title: "I Built a Python Library That Generates UIs — Here's Why"
published: false
description: "How I created uigen, a tool that lets backend developers write UIs in Python and generate HTML, React, Flask, or Django code."
tags: python, webdev, javascript, react
canonical_url:
cover_image:
---

# I Built a Python Library That Generates UIs — Here's Why

As a backend developer, I always dreaded one thing: **building UIs**.

I can write Python all day. I can architect APIs, design databases, optimize queries. But ask me to build a simple admin panel with a table and a form? Suddenly I'm drowning in HTML, CSS, and JavaScript boilerplate.

So I built **uigen** — a Python library that lets you define UIs using Python functions, then generate production-ready code for multiple targets.

## The Problem

Let me show you what I mean. Here's a simple user management table in raw HTML:

```html
<div class="bg-white rounded-lg shadow-md p-6">
  <h2 class="text-2xl font-semibold text-gray-900 mb-4">Users</h2>
  <table class="w-full">
    <thead>
      <tr class="border-b border-gray-200">
        <th class="px-4 py-2 text-left text-sm font-medium text-gray-700">Name</th>
        <th class="px-4 py-2 text-left text-sm font-medium text-gray-700">Email</th>
        <th class="px-4 py-2 text-left text-sm font-medium text-gray-700">Role</th>
      </tr>
    </thead>
    <tbody>
      <tr class="border-t border-gray-200">
        <td class="px-4 py-2 text-sm text-gray-600">Alice Johnson</td>
        <td class="px-4 py-2 text-sm text-gray-600">alice@example.com</td>
        <td class="px-4 py-2 text-sm text-gray-600">admin</td>
      </tr>
      <tr class="border-t border-gray-200">
        <td class="px-4 py-2 text-sm text-gray-600">Bob Smith</td>
        <td class="px-4 py-2 text-sm text-gray-600">bob@example.com</td>
        <td class="px-4 py-2 text-sm text-gray-600">viewer</td>
      </tr>
    </tbody>
  </table>
  <button class="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
    Add User
  </button>
</div>
```

That's **35+ lines** of HTML for a basic table with two rows. And I haven't even added:
- Responsive design
- Form validation
- Modal dialogs
- Loading states

## The Solution

Now here's the same table in Python with uigen:

```python
from uigen import App, Model, ui

class User(Model):
    name: str
    email: str
    role: str = "viewer"

page = ui.page(
    ui.card(
        ui.heading("Users"),
        ui.table(data=[
            {"name": "Alice Johnson", "email": "alice@example.com", "role": "admin"},
            {"name": "Bob Smith", "email": "bob@example.com", "role": "viewer"},
        ]),
        ui.button("Add User"),
    ),
    title="User Management",
)

app = App(title="My App", pages=[page])
app.render("lnative", output="./dist")
```

**15 lines.** Same result. 57% less code.

## How It Works

uigen has three core concepts:

### 1. Models

Define your data schemas using Python type hints:

```python
class User(Model):
    name: str
    email: str
    role: str = "viewer"
    active: bool = True
```

### 2. Components

Build UIs using composable components:

```python
page = ui.page(
    ui.card(
        ui.heading("Dashboard"),
        ui.grid(
            ui.card(ui.text("Stats 1")),
            ui.card(ui.text("Stats 2")),
            columns=2,
        ),
        ui.table(data=users),
        ui.form(
            ui.input("email", label="Email"),
            ui.button("Submit"),
        ),
    )
)
```

### 3. Renderers

Generate code for different targets:

```python
app = App(title="My App", pages=[page])

# Generate static HTML
app.render("lnative", output="./dist")

# Generate React components
app.render("lreact", output="./react-app")

# Generate Flask templates
app.render("lflask", output="./flask-app")

# Generate Django templates
app.render("ldjango", output="./django-app")
```

## Why I Built This

### 1. Backend Devs Should Build UIs Too

Not every project needs a dedicated frontend developer. Sometimes you just need a quick admin panel, a dashboard, or a simple form. uigen lets backend devs build these without learning React, Vue, or vanilla HTML.

### 2. Code Generation > Templates

I tried other solutions:
- **Jinja2 templates** — Still need to write HTML
- **Streamlit** — Great for data apps, but not for general UIs
- **Gradio** — Same limitation
- **Reflex** — Interesting, but too opinionated

uigen generates **code you own**. After generation, you can edit the HTML, customize the React components, or modify the Django templates. It's not a runtime dependency.

### 3. Multiple Targets, One API

Why write the same UI four times for different frameworks? With uigen, you write it once in Python and generate all four.

## Real-World Example: Perfume Store

Here's a complete perfume store I built with uigen:

```python
from uigen import App, Model, ui

class Perfume(Model):
    name: str
    brand: str
    price: float
    category: str

# Product card component
def product_card(product: dict) -> Card:
    return ui.card(
        ui.heading(product["name"], level=3),
        ui.text(f"by {product['brand']}"),
        ui.text(f"${product['price']:.2f}"),
        ui.button("Add to Cart", variant="primary"),
    )

# Home page
home = ui.page(
    ui.card(
        ui.heading("Discover Your Signature Scent"),
        ui.text("Luxury fragrances from the world's finest perfume houses."),
        ui.button("Shop Now"),
    ),
    ui.card(
        ui.heading("Featured Products"),
        ui.grid(
            *[product_card(p) for p in products],
            columns=3,
        ),
    ),
    title="Lumiere Parfums",
)

app = App(title="Lumiere Parfums", pages=[home])
app.render("lnative", output="./dist")
```

One Python file → complete HTML store.

## Installation

```bash
pip install uigen
```

Or from source:

```bash
git clone https://github.com/SaadEddine-ware/uigen.git
cd uigen
pip install -e ".[dev]"
```

## Quick Start

```bash
# Create a new project
uigen init my-app
cd my-app

# Edit main.py with your UI

# Generate
python main.py

# Open dist/index.html
```

## What's Next

uigen is still in early development. Here's what's planned:

- [x] Core API and Model system
- [x] Static HTML renderer
- [x] React renderer
- [x] Flask renderer
- [x] Django renderer
- [ ] C extension for 10x faster generation
- [ ] Theme customization (colors, fonts, spacing)
- [ ] More components (charts, calendars, etc.)
- [ ] VS Code extension

## Contributing

Contributions are welcome! Check out the [GitHub repo](https://github.com/SaadEddine-ware/uigen) and the [CONTRIBUTING.md](https://github.com/SaadEddine-ware/uigen/blob/main/CONTRIBUTING.md) guide.

## Conclusion

Backend devs shouldn't avoid building UIs because of the boilerplate. uigen lets you stay in Python, write clean code, and generate production-ready frontend code.

**57% less code. Same result.**

Try it out and let me know what you think!

---

*GitHub: [github.com/SaadEddine-ware/uigen](https://github.com/SaadEddine-ware/uigen)*

*PyPI: Coming soon*
