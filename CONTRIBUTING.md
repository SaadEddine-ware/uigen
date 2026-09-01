# Contributing to uigen

Thank you for your interest in contributing to uigen! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Community](#community)

---

## Code of Conduct

We are committed to providing a welcoming and inclusive experience for everyone. Please be respectful and constructive in all interactions.

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- pip or poetry

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/YOUR_USERNAME/uigen.git
cd uigen
```

3. Add the upstream remote:

```bash
git remote add upstream https://github.com/SaadEddine-ware/uigen.git
```

---

## Development Setup

### 1. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -e ".[dev]"
```

This installs uigen in editable mode with all development dependencies.

### 3. Verify Installation

```bash
# Run tests
pytest

# Run linter
ruff check src/ tests/

# Check types
mypy src/
```

---

## How to Contribute

### Reporting Bugs

Before creating a bug report, please check existing issues to avoid duplicates.

When creating a bug report, include:

- **Clear title** — Descriptive summary of the issue
- **Steps to reproduce** — Minimal code or steps to trigger the bug
- **Expected behavior** — What you expected to happen
- **Actual behavior** — What actually happened
- **Environment** — Python version, OS, uigen version

### Suggesting Features

Feature suggestions are welcome! Please provide:

- **Problem statement** — What problem does this solve?
- **Proposed solution** — How should it work?
- **Alternatives considered** — Other approaches you thought about
- **Use cases** — Real-world scenarios where this helps

### Contributing Code

1. **Find or create an issue** — Discuss what you want to change
2. **Fork and create a branch** — Work on a feature branch
3. **Write code** — Follow our coding standards
4. **Write tests** — Ensure your changes are tested
5. **Submit a PR** — Follow the pull request process

---

## Pull Request Process

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:
- `feature/add-react-renderer`
- `fix/table-sorting-bug`
- `docs/update-readme`

### 2. Make Your Changes

- Write clean, readable code
- Follow the coding standards below
- Add tests for new functionality
- Update documentation if needed

### 3. Commit Your Changes

Use clear, concise commit messages:

```bash
git commit -m "feat: add React renderer for component generation"
git commit -m "fix: resolve table sorting issue with nested data"
git commit -m "docs: add examples for Flask renderer"
```

Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation changes
- `style:` — Code style changes (formatting, etc.)
- `refactor:` — Code refactoring
- `test:` — Adding or updating tests
- `chore:` — Maintenance tasks

### 4. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:

- **Title** — Clear description of changes
- **Description** — What and why, not how
- **Related issues** — Link to relevant issues
- **Screenshots** — If visual changes are involved
- **Testing** — How you tested the changes

### 5. Code Review

- Respond to feedback promptly
- Make requested changes in new commits
- Squash commits if requested

---

## Coding Standards

### Python Style

We use [ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
# Check for issues
ruff check src/ tests/

# Auto-fix issues
ruff check src/ tests/ --fix

# Format code
ruff format src/ tests/
```

### Code Guidelines

- **Line length** — Maximum 88 characters
- **Type hints** — Use type hints for all public functions
- **Docstrings** — Write docstrings for all public classes and functions
- **Naming** — Use snake_case for functions and variables, PascalCase for classes
- **Imports** — Sort imports using ruff

### Example

```python
"""Module for rendering HTML output."""

from __future__ import annotations

from typing import Any

from uigen.core.components import Component


def render_component(component: Component, **kwargs: Any) -> str:
    """Render a component to HTML string.

    Args:
        component: The component to render.
        **kwargs: Additional rendering options.

    Returns:
        Rendered HTML string.
    """
    # Implementation here
    return "<div></div>"
```

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_core.py

# Run with coverage
pytest --cov=uigen --cov-report=html
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names
- One assertion per test when possible

### Example Test

```python
"""Tests for the table component."""

from uigen import ui


class TestTable:
    def test_table_from_dict_list(self):
        """Test creating table from list of dictionaries."""
        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]
        table = ui.table(data=data)

        assert table.columns == ["name", "age"]
        assert len(table.rows) == 2

    def test_table_empty_data(self):
        """Test creating table with no data."""
        table = ui.table()
        assert table.columns == []
        assert table.rows == []
```

---

## Documentation

### Code Documentation

- Write docstrings for all public APIs
- Use Google-style docstrings
- Include examples where helpful

### README Updates

When adding features:
- Update the README with usage examples
- Add to the features list
- Update the roadmap

### Examples

- Create example files in `examples/`
- Ensure examples run without errors
- Add comments explaining key concepts

---

## Community

### Getting Help

- Open a GitHub Issue for bugs or feature requests
- Check existing issues before creating new ones

### Staying Updated

- Watch the repository for updates
- Check the CHANGELOG for new releases

---

## Recognition

Contributors will be recognized in:
- The README contributors section
- Release notes
- Git commit history

Thank you for contributing to uigen!
