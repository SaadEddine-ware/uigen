# uigen

**Write UI logic once, deploy anywhere.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-88%20passing-brightgreen.svg)](#testing)
[![GitHub Stars](https://img.shields.io/github/stars/SaadEddine-ware/uigen.svg?style=social)](https://github.com/SaadEddine-ware/uigen)

---

## Demo

### The Problem

Backend devs need to build UIs but hate writing HTML. A simple table takes 35+ lines:

```html
<!-- 35+ lines of HTML for a basic table -->
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

### The Solution

Write 15 lines of Python instead:

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

### The Result

Same output. **57% less code.**

```
┌─────────────────────────────────────────────────────────┐
│  Metric              HTML         Python (uigen)       │
├─────────────────────────────────────────────────────────┤
│  Lines of code       35+          15                   │
│  Characters          ~1,500       ~500                 │
│  Time to write       10-15 min    2-3 min              │
│  Reduction           —            57%                  │
└─────────────────────────────────────────────────────────┘
```

<!-- [![Demo](https://github.com/SaadEddine-ware/uigen/raw/main/docs/demo.gif)](https://github.com/SaadEddine-ware/uigen/raw/main/docs/demo.gif) -->

*Run `python examples/demo.py` to see the full transformation*

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

| Renderer | Output | Best For |
|----------|--------|----------|
| `lnative` | Static HTML/CSS/JS | Landing pages, admin panels |
| `lreact` | React components | Complex SPAs |
| `lflask` | Flask/Jinja2 templates | Python web apps |
| `ldjango` | Django templates | Enterprise apps |

---

## Using Renderers

### lnative — Static HTML

Generates a standalone HTML file with Tailwind CSS. No build step needed.

```python
from uigen import App, ui

page = ui.page(
    ui.card(ui.heading("Hello")),
    title="My Page"
)

app = App(title="My App", pages=[page])
app.render("lnative", output="./dist")
```

**Output:**
```
dist/
└── index.html    # Open in browser, works offline
```

### lreact — React Components

Generates a React project with components, package.json, and index.html.

```python
app.render("lreact", output="./my-react-app")
```

**Output:**
```
my-react-app/
├── package.json
├── index.html
└── src/
    └── components/
        ├── App.jsx
        └── MyPage.jsx
```

**Setup:**
```bash
cd my-react-app
npm install
npm start
```

### lflask — Flask Templates

Generates a Flask app with Jinja2 templates and route stubs.

```python
app.render("lflask", output="./my-flask-app")
```

**Output:**
```
my-flask-app/
├── app.py              # Flask app with routes
├── requirements.txt
└── templates/
    ├── base.html
    └── my_page.html
```

**Setup:**
```bash
cd my-flask-app
pip install -r requirements.txt
python app.py
```

### ldjango — Django Templates

Generates a Django app with templates, views, and URL configuration.

```python
app.render("ldjango", output="./my-django-app")
```

**Output:**
```
my-django-app/
├── manage.py
├── requirements.txt
├── my_django_app/
│   ├── settings.py
│   ├── urls.py
│   └── views.py
└── templates/
    ├── base.html
    └── my_page.html
```

**Setup:**
```bash
cd my-django-app
pip install -r requirements.txt
python manage.py runserver
```

---

### CLI Usage

You can also generate from the command line:

```bash
# Generate HTML
uigen generate --renderer lnative --output ./dist

# Generate React
uigen generate --renderer lreact --output ./my-react-app

# Generate Flask
uigen generate --renderer lflask --output ./my-flask-app

# Generate Django
uigen generate --renderer ldjango --output ./my-django-app
```

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

## Themes

uigen includes a theme customization system with built-in themes:

```python
from uigen import App, ui, get_theme, list_themes

# List available themes
print(list_themes())  # ['default', 'dark', 'emerald', 'purple', 'rose']

# Use a theme
app = App(title="My App", pages=[page], theme="emerald")
app.render("lnative", output="./dist")
```

### Built-in Themes

| Theme | Primary Color | Use Case |
|-------|--------------|----------|
| `default` | Blue | General purpose |
| `dark` | Blue | Dark mode interfaces |
| `emerald` | Green | Success, nature, finance |
| `purple` | Purple | Creative, luxury |
| `rose` | Rose | Fashion, beauty |

### Custom Themes

```python
from uigen import Theme, register_theme, ColorPalette

# Create a custom theme
custom = Theme(
    name="my-brand",
    colors=ColorPalette(
        primary="indigo",
        primary_500="#6366f1",
        primary_600="#4f46e5",
        primary_700="#4338ca",
    ),
)

# Register and use it
register_theme("my-brand", custom)
app = App(title="My App", pages=[page], theme="my-brand")
```

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

# Generate static HTML
python perfume_store.py lnative

# Generate React app
python perfume_store.py lreact

# Generate Flask app
python perfume_store.py lflask

# Generate Django app
python perfume_store.py ldjango
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
- [x] `lreact` renderer (React)
- [x] `lflask` renderer (Flask)
- [x] `ldjango` renderer (Django)
- [x] CLI support
- [x] Theme customization (5 built-in themes)
- [x] C extension for HTML escaping
- [x] Tests (88 passing)
- [x] Examples (dashboard, perfume store)
- [ ] More components (charts, calendars, etc.)
- [ ] VS Code extension
- [ ] Demo GIF recording

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
