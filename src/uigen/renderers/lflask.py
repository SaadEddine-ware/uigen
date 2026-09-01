"""lflask renderer — generates Flask/Jinja2 templates."""

from __future__ import annotations

from uigen.core.components import Component, Page
from uigen.renderers.base import BaseRenderer


class LFlaskRenderer(BaseRenderer):
    """Generates Jinja2 templates for Flask apps."""

    def render_page(self, page: Page, title: str = "") -> str:
        # TODO: Implement Flask template generation
        raise NotImplementedError("Flask renderer coming in Phase 3")

    def render_component(self, component: Component) -> str:
        raise NotImplementedError("Flask renderer coming in Phase 3")
