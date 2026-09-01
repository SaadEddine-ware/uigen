# uigen — Project Plan

## Tagline
*"Write UI logic once, deploy anywhere."*

## What is uigen?

uigen is a Python library that lets backend developers define UIs using Python functions, then generate production-ready frontend code for multiple targets — static HTML, React, Flask templates, or Django templates.

**The problem it solves:** Backend devs hate dealing with HTML/CSS/JS boilerplate. A table that takes 100 lines of HTML should take 5 lines of Python.

**The target user:** Python/C developers who want to build UIs without becoming frontend experts.

---

## Architecture

```
uigen/
├── src/
│   └── uigen/
│       ├── __init__.py          # Public API exports
│       ├── core/
│       │   ├── __init__.py
│       │   ├── api.py           # ui.card(), ui.table(), ui.form() etc.
│       │   ├── schema.py        # Model definitions (data schemas)
│       │   ├── compiler.py      # Transforms API → renderer output
│       │   └── components.py    # Component definitions and registry
│       ├── renderers/
│       │   ├── __init__.py
│       │   ├── base.py          # Abstract renderer interface
│       │   ├── lnative.py       # → Static HTML/CSS/JS
│       │   ├── lreact.py        # → React component files
│       │   ├── lflask.py        # → Flask/Jinja2 templates
│       │   └── ldjango.py       # → Django templates
│       └── cli.py               # Command-line interface
├── tests/
├── examples/
├── docs/
├── pyproject.toml
├── README.md
└── PLAN.md                      # This file
```

---

## Core API Design

### 1. Model System
Define data schemas that auto-generate forms, tables, and validation:

```python
from uigen import Model

class User(Model):
    name: str
    email: str
    role: str = "viewer"
    active: bool = True
```

### 2. Component API
Build UIs with composable components:

```python
from uigen import ui

page = ui.page(
    ui.card(
        ui.heading("User Management"),
        ui.table(users, columns=["name", "email", "role"]),
        ui.button("Add User", onclick="showModal")
    ),
    ui.modal(
        ui.form(
            ui.input("name", label="Name"),
            ui.input("email", label="Email", type="email"),
            ui.select("role", options=["admin", "editor", "viewer"]),
            ui.submit("Save")
        )
    )
)
```

### 3. App Definition
Wire everything together:

```python
from uigen import App

app = App(
    title="My Admin Panel",
    models=[User],
    pages=[page]
)

# Choose output target
app.render("lnative", output="./dist")    # Static HTML files
app.render("lreact", output="./frontend")  # React project
app.render("lflask", output="./templates") # Flask templates
app.render("ldjango", output="./django_ui") # Django templates
```

---

## Renderer Specifications

### lnative (Static HTML/CSS/JS)
- Generates standalone HTML files
- Uses Tailwind CSS via CDN (or bundled)
- Vanilla JavaScript for interactivity
- No build step required
- **Best for:** Landing pages, simple admin panels, demos

### lreact (React Components)
- Generates .jsx/.tsx component files
- Includes package.json with React, Tailwind dependencies
- Auto-generates component imports and routing
- **Best for:** Complex SPAs, teams already using React

### lflask (Flask Templates)
- Generates Jinja2 templates
- Includes Flask route stubs
- Integrates with Flask-Login for auth
- **Best for:** Flask apps needing a quick admin UI

### ldjango (Django Templates)
- Generates Django template files
- Includes Django view and URL configuration
- Integrates with Django admin patterns
- **Best for:** Django projects, enterprise apps

---

## C Extension (Performance)

The template compiler will optionally use a C extension for:
- Fast template parsing and compilation
- Efficient code generation for large projects
- Benchmarks showing 10-50x speedup over pure Python

```python
# If C extension is available, use it automatically
from uigen import App
app = App(...)  # Uses C compiler if installed
```

---

## CLI Design

```bash
# Initialize a new uigen project
uigen init my-project

# Generate frontend from Python definitions
uigen generate --renderer lnative --output ./dist

# Preview generated output with hot reload
uigen preview

# List available renderers
uigen renderers

# Install a renderer
uigen install lreact
```

---

## Phased Roadmap

### Phase 1: Core + lnative (Week 1-2)
**Goal:** Working MVP that generates static HTML sites

- [ ] Set up project structure (pyproject.toml, src layout)
- [ ] Implement core API: `ui.card()`, `ui.table()`, `ui.form()`, `ui.button()`, `ui.input()`, `ui.select()`
- [ ] Implement Model system with field types
- [ ] Build abstract renderer interface
- [ ] Implement `lnative` renderer
  - HTML generation with Tailwind CSS
  - JavaScript for modals, forms, interactivity
  - Responsive grid system
- [ ] Build CLI: `uigen init`, `uigen generate`
- [ ] Write tests for core API
- [ ] Create 2-3 example projects

### Phase 2: lreact (Week 3-4)
**Goal:** React code generation

- [ ] Implement `lreact` renderer
  - Generate functional React components
  - TypeScript support
  - Proper prop types and state management
  - React Router integration
- [ ] Generate package.json with dependencies
- [ ] Add `uigen preview` for development
- [ ] Write tests for React renderer
- [ ] Create React example projects

### Phase 3: lflask + ldjango (Week 5-6)
**Goal:** Server-side rendering support

- [ ] Implement `lflask` renderer
  - Jinja2 template generation
  - Flask blueprint structure
  - WTForms integration
- [ ] Implement `ldjango` renderer
  - Django template generation
  - ModelForm integration
  - URL configuration
- [ ] Write integration tests
- [ ] Create framework-specific examples

### Phase 4: Polish + Portfolio (Week 7-8)
**Goal:** Make it shine on GitHub

- [ ] Write comprehensive README with:
  - Problem statement
  - Before/after code comparisons
  - Installation instructions
  - Quick start guide
  - Renderer comparison table
- [ ] Create demo GIFs/videos
- [ ] Add CI/CD (GitHub Actions)
- [ ] Write dev.to article or blog post
- [ ] Publish to PyPI
- [ ] Add contributing guidelines

---

## Success Metrics

| Metric | Target |
|--------|--------|
| GitHub stars (3 months) | 100+ |
| PyPI downloads (monthly) | 500+ |
| Time to generate a page | < 1 second |
| Lines of Python vs HTML | 5:100 ratio |
| Renderer coverage | 4 renderers |

---

## What Makes This Portfolio-Worthy

1. **Software Design** — Pluggable renderer architecture (Open/Closed Principle)
2. **Systems Skills** — C extension for performance-critical paths
3. **Full-Stack Awareness** — Understands both backend and frontend concerns
4. **Real Utility** — Solves a problem every backend dev faces
5. **Visual Impact** — Demo GIFs are highly shareable on social media
6. **Documentation** — Professional README shows communication skills

---

## Open Questions to Resolve

1. **Component styling:** Tailwind-only, or support multiple CSS frameworks?
2. **Interactivity:** How complex should the generated JavaScript be?
3. **Auth:** Should renderers include authentication boilerplate?
4. **Database:** Should uigen generate database schemas from Models, or stay UI-only?

---

## Next Steps

1. Create the GitHub repository
2. Set up the project structure
3. Build the core API
4. Implement the lnative renderer
5. Write the first example

---

*Last updated: 2026-09-01*
