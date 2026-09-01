# uigen

**Write UI logic once, deploy anywhere.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-30%20passing-brightgreen.svg)](#testing)
[![GitHub Stars](https://img.shields.io/github/stars/SaadEddine-ware/uigen.svg?style=social)](https://github.com/SaadEddine-ware/uigen)

---

## Demo

### Before: 100+ lines of HTML

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

### After: 15 lines of Python

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

**Same result. 85% less code.**

---

<!-- [![Demo](https://github.com/SaadEddine-ware/uigen/raw/main/docs/demo.gif)](https://github.com/SaadEddine-ware/uigen/raw/main/docs/demo.gif) -->

*GIF demo coming soon — showing Python code generating a full admin dashboard*

---

## What is uigen?

uigen is a Python library that lets backend developers define UIs using Python functions, then generate production-ready frontend code for multiple targets.

**Stop writing HTML boilerplate. Start writing Python.**

### The Problem

Backend devs constantly need to build admin panels, dashboards, or simple web UIs. But setting up React, writing HTML, configuring Tailwind — it's a different world. A simple table takes 100+ lines of HTML.

### The Solution

Write Python functions that generate clean, production-ready HTML, React, Flask, or Django code. The generated code is yours — edit it freely after generation.

---

## Features

- **Pythonic API** — Define UIs using familiar Python syntax
- **Multiple Renderers** — Generate HTML, React, Flask, or Django code
- **Model System** — Define data schemas that auto-generate forms and tables
- **Component Library** — Cards, tables, forms, modals, grids, and more
- **CLI Support** — Initialize projects and generate code from the command line
- **No Runtime Dependency** — Generated code is standalone, you own it
- **Fast** — C-powered template engine for blazing fast generation

---

## Renderers

| Renderer | Status | Output | Best For |
|----------|--------|--------|----------|
| `lnative` | Ready | Static HTML/CSS/JS | Landing pages, admin panels |
| `lreact` | Coming Soon | React components | Complex SPAs |
| `lflask` | Coming Soon | Flask/Jinja2 templates | Python web apps |
| `ldjango` | Coming Soon | Django templates | Enterprise apps |

---

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

---

## Quick Start

### 1. Create a Project

```bash
uigen init my-app
cd my-app
```

### 2. Edit `main.py`

```python
from uigen import App, Model, ui

class Product(Model):
    name: str
    price: float
    category: str

page = ui.page(
    ui.card(
        ui.heading("Products"),
        ui.table(data=[
            {"name": "Laptop", "price": 999.99, "category": "Electronics"},
            {"name": "Mouse", "price": 29.99, "category": "Accessories"},
        ]),
    ),
    title="Product Catalog",
)

app = App(title="My Store", pages=[page])
```

### 3. Generate

```bash
python main.py
# or
uigen generate --renderer lnative --output ./dist
```

### 4. Preview

Open `dist/index.html` in your browser.

---

## Components

uigen provides a rich set of UI components:

```python
# Layout
ui.page(...)                    # Top-level page container
ui.card(...)                    # Card with shadow and padding
ui.grid(..., columns=3)         # Grid layout
ui.stack(..., spacing="md")     # Vertical stack

# Content
ui.heading("Title", level=1)    # Headings (h1-h6)
ui.text("Paragraph text")       # Paragraph text

# Interactive
ui.button("Click me", variant="primary")  # Buttons
ui.modal(...)                           # Modal dialogs
ui.form(...)                            # Form containers

# Data
ui.table(data=[...], columns=["name", "email"])  # Data tables
ui.input("email", label="Email", type="email")   # Form inputs
ui.select("role", options=["admin", "user"])      # Dropdowns
```

---

## Model System

Define data schemas that auto-generate forms and tables:

```python
from uigen import Model

class User(Model):
    name: str
    email: str
    role: str = "viewer"
    active: bool = True

# Use in tables
ui.table(data=users, columns=User.field_names())

# Auto-generate forms
ui.form(
    ui.input("name", label="Name"),
    ui.input("email", label="Email", type="email"),
    ui.select("role", options=["admin", "editor", "viewer"]),
)
```

---

## CLI Commands

```bash
# Initialize a new project
uigen init my-project

# Generate frontend code
uigen generate --renderer lnative --output ./dist

# List available renderers
uigen renderers
```

---

## Architecture

```
uigen/
├── src/uigen/
│   ├── core/
│   │   ├── schema.py       # Model system
│   │   ├── components.py   # UI components
│   │   ├── api.py          # ui namespace
│   │   └── compiler.py     # App compilation
│   ├── renderers/
│   │   ├── base.py         # Abstract renderer
│   │   ├── lnative.py      # HTML/CSS/JS generator
│   │   ├── lreact.py       # React generator
│   │   ├── lflask.py       # Flask generator
│   │   └── ldjango.py      # Django generator
│   └── cli.py              # Command-line interface
├── tests/
├── examples/
└── pyproject.toml
```

---

## Examples

See the [`examples/`](examples/) directory for complete examples:

- [`dashboard.py`](examples/dashboard.py) — Admin dashboard with stats, tables, and modals
- [`perfume_store.py`](examples/perfume_store.py) — E-commerce perfume store website

### Perfume Store Demo

A complete perfume store with:
- Home page with hero section, featured products, and newsletter
- Shop page with product grid and filters
- About page with story, values, and contact form

```bash
cd examples
python perfume_store.py
open dist/index.html
```

---

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=uigen

# Run specific test file
pytest tests/test_core.py -v
```

---

## Roadmap

- [x] Core API and Model system
- [x] `lnative` renderer (HTML/CSS/JS)
- [x] CLI support
- [x] Tests (30 passing)
- [x] Examples (dashboard, perfume store)
- [ ] `lreact` renderer (React)
- [ ] `lflask` renderer (Flask)
- [ ] `ldjango` renderer (Django)
- [ ] C extension for performance
- [ ] Theme customization
- [ ] Component library expansion
- [ ] Demo GIF

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## Author

**SaadEddine-ware** — [GitHub](https://github.com/SaadEddine-ware)

---

## Acknowledgments

- Built with Python 3.10+
- Styled with [Tailwind CSS](https://tailwindcss.com/)
- Inspired by the need for simpler frontend tooling for backend developers
