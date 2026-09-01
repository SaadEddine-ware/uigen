"""UI component definitions."""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field as dc_field
from typing import Any


@dataclass
class Component:
    """Base class for all UI components."""

    tag: str = "div"
    children: list[Component] = dc_field(default_factory=list)
    attrs: dict[str, Any] = dc_field(default_factory=dict)
    classes: list[str] = dc_field(default_factory=list)

    def add_class(self, *class_names: str) -> Component:
        self.classes.extend(class_names)
        return self

    def to_dict(self) -> dict[str, Any]:
        return {
            "tag": self.tag,
            "children": [c.to_dict() for c in self.children],
            "attrs": self.attrs,
            "classes": self.classes,
        }


@dataclass
class Page(Component):
    """Top-level page container."""

    title: str = ""
    description: str = ""

    def __post_init__(self) -> None:
        self.tag = "page"


@dataclass
class Card(Component):
    """A card container with padding and shadow."""

    def __post_init__(self) -> None:
        self.tag = "card"
        self.classes.append("card")


@dataclass
class Heading(Component):
    """A heading element."""

    level: int = 1
    text: str = ""

    def __post_init__(self) -> None:
        self.tag = f"h{self.level}"


@dataclass
class Text(Component):
    """A text/paragraph element."""

    text: str = ""

    def __post_init__(self) -> None:
        self.tag = "p"


@dataclass
class Button(Component):
    """A button element."""

    text: str = ""
    variant: str = "primary"
    onclick: str = ""

    def __post_init__(self) -> None:
        self.tag = "button"
        if self.onclick:
            self.attrs["onclick"] = self.onclick


@dataclass
class Input(Component):
    """A form input element."""

    name: str = ""
    input_type: str = "text"
    label: str = ""
    placeholder: str = ""
    value: str = ""
    required: bool = False

    def __post_init__(self) -> None:
        self.tag = "input"
        self.attrs["type"] = self.input_type
        self.attrs["name"] = self.name
        if self.placeholder:
            self.attrs["placeholder"] = self.placeholder
        if self.value:
            self.attrs["value"] = self.value
        if self.required:
            self.attrs["required"] = "true"


@dataclass
class Select(Component):
    """A select dropdown element."""

    name: str = ""
    label: str = ""
    options: list[str] = dc_field(default_factory=list)
    value: str = ""

    def __post_init__(self) -> None:
        self.tag = "select"
        self.attrs["name"] = self.name


@dataclass
class Table(Component):
    """A data table element."""

    columns: list[str] = dc_field(default_factory=list)
    rows: list[dict[str, Any]] = dc_field(default_factory=list)

    def __post_init__(self) -> None:
        self.tag = "table"


@dataclass
class Form(Component):
    """A form container."""

    action: str = ""
    method: str = "POST"

    def __post_init__(self) -> None:
        self.tag = "form"
        if self.action:
            self.attrs["action"] = self.action
        self.attrs["method"] = self.method


@dataclass
class Modal(Component):
    """A modal dialog container."""

    title: str = ""

    def __post_init__(self) -> None:
        self.tag = "modal"


@dataclass
class Grid(Component):
    """A grid layout container."""

    columns: int = 2

    def __post_init__(self) -> None:
        self.tag = "grid"
        self.attrs["columns"] = self.columns


@dataclass
class Stack(Component):
    """A vertical stack layout."""

    spacing: str = "md"

    def __post_init__(self) -> None:
        self.tag = "stack"
        self.attrs["spacing"] = self.spacing
