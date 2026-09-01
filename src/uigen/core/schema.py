"""Model system — define data schemas that auto-generate forms and tables."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Field:
    """A field in a Model schema."""

    name: str
    type: type = str
    default: Any = None
    label: str = ""
    required: bool = True
    help_text: str = ""
    options: list[str] | None = None

    def __post_init__(self) -> None:
        if not self.label:
            self.label = self.name.replace("_", " ").title()
        if self.default is not None:
            self.required = False


class ModelMeta(type):
    """Metaclass that collects Field definitions from Model subclasses."""

    def __new__(
        mcs, name: str, bases: tuple[type, ...], namespace: dict[str, Any]
    ) -> ModelMeta:
        fields: dict[str, Field] = {}

        for base in bases:
            if hasattr(base, "__fields__"):
                fields.update(base.__fields__)

        annotations = namespace.get("__annotations__", {})
        for field_name, field_type in annotations.items():
            if field_name.startswith("_"):
                continue

            default = namespace.get(field_name)
            if isinstance(default, Field):
                fields[field_name] = default
            else:
                fields[field_name] = Field(
                    name=field_name,
                    type=field_type,
                    default=default if default is not None else ...,
                )

        cls = super().__new__(mcs, name, bases, namespace)
        cls.__fields__ = fields
        return cls


class Model(metaclass=ModelMeta):
    """Base class for data models.

    Usage:
        class User(Model):
            name: str
            email: str
            role: str = "viewer"
    """

    __fields__: dict[str, Field]

    def __init__(self, **kwargs: Any) -> None:
        for name, field in self.__fields__.items():
            value = kwargs.get(name, field.default)
            if value is ... and field.required:
                raise ValueError(f"Missing required field: {name}")
            setattr(self, name, value)

    def to_dict(self) -> dict[str, Any]:
        return {name: getattr(self, name) for name in self.__fields__}

    @classmethod
    def fields(cls) -> list[Field]:
        return list(cls.__fields__.values())

    @classmethod
    def field_names(cls) -> list[str]:
        return list(cls.__fields__.keys())
