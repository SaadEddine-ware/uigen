"""ldjango renderer — generates Django templates."""

from __future__ import annotations

from uigen.core.components import Component, Page
from uigen.renderers.base import BaseRenderer


class LDjangoRenderer(BaseRenderer):
    """Generates Django template files."""

    def render_page(self, page: Page, title: str = "") -> str:
        # TODO: Implement Django template generation
        raise NotImplementedError("Django renderer coming in Phase 3")

    def render_component(self, component: Component) -> str:
        raise NotImplementedError("Django renderer coming in Phase 3")
