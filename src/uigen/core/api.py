"""Public API — the ui object that users interact with."""

from __future__ import annotations

from typing import Any

from uigen.core.components import (
    Button,
    Card,
    Component,
    Form,
    Grid,
    Heading,
    Input,
    Modal,
    Page,
    Select,
    Stack,
    Table,
    Text,
)
from uigen.core.schema import Model


class UI:
    """The ui namespace — provides methods to create UI components."""

    def page(
        self, *children: Component, title: str = "", description: str = ""
    ) -> Page:
        """Create a page container."""
        return Page(
            children=list(children),
            title=title,
            description=description,
        )

    def card(self, *children: Component, **attrs: Any) -> Card:
        """Create a card container."""
        return Card(children=list(children), attrs=attrs)

    def heading(self, text: str, level: int = 1) -> Heading:
        """Create a heading element."""
        return Heading(text=text, level=level)

    def text(self, content: str) -> Text:
        """Create a paragraph/text element."""
        return Text(text=content)

    def button(self, text: str, variant: str = "primary", onclick: str = "") -> Button:
        """Create a button element."""
        return Button(text=text, variant=variant, onclick=onclick)

    def input(
        self,
        name: str,
        label: str = "",
        type: str = "text",
        placeholder: str = "",
        value: str = "",
        required: bool = False,
    ) -> Input:
        """Create a form input."""
        return Input(
            name=name,
            label=label or name.replace("_", " ").title(),
            input_type=type,
            placeholder=placeholder,
            value=value,
            required=required,
        )

    def select(
        self, name: str, options: list[str], label: str = "", value: str = ""
    ) -> Select:
        """Create a select dropdown."""
        return Select(
            name=name,
            options=options,
            label=label or name.replace("_", " ").title(),
            value=value,
        )

    def table(
        self,
        data: list[dict[str, Any]] | Model | None = None,
        columns: list[str] | None = None,
    ) -> Table:
        """Create a data table.

        Args:
            data: List of dicts, a Model class (uses its fields), or None.
            columns: Column names. If None, auto-detected from data.
        """
        rows: list[dict[str, Any]] = []
        cols = columns or []

        if data is None:
            cols = cols or []
        elif isinstance(data, type) and issubclass(data, Model):
            cols = cols or data.field_names()
        elif isinstance(data, list):
            rows = data
            if not cols and rows:
                cols = list(rows[0].keys())

        return Table(columns=cols, rows=rows)

    def form(
        self, *children: Component, action: str = "", method: str = "POST"
    ) -> Form:
        """Create a form container."""
        return Form(children=list(children), action=action, method=method)

    def modal(self, *children: Component, title: str = "") -> Modal:
        """Create a modal dialog."""
        return Modal(children=list(children), title=title)

    def grid(self, *children: Component, columns: int = 2) -> Grid:
        """Create a grid layout."""
        return Grid(children=list(children), columns=columns)

    def stack(self, *children: Component, spacing: str = "md") -> Stack:
        """Create a vertical stack layout."""
        return Stack(children=list(children), spacing=spacing)


ui = UI()
