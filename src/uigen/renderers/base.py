"""Abstract base renderer — defines the interface all renderers must implement."""

from __future__ import annotations

from abc import ABC, abstractmethod

from uigen.core.components import Component, Page


class BaseRenderer(ABC):
    """Abstract base class for all renderers.

    Each renderer must implement render_page() to produce output
    for a specific target (HTML, React, Flask, Django, etc.).
    """

    @abstractmethod
    def render_page(self, page: Page, title: str = "") -> str:
        """Render a Page component to the target format.

        Args:
            page: The Page component tree to render.
            title: Optional page title.

        Returns:
            Rendered output as a string.
        """
        ...

    @abstractmethod
    def render_component(self, component: Component) -> str:
        """Render a single component to the target format.

        Args:
            component: The component to render.

        Returns:
            Rendered output as a string.
        """
        ...

    def _render_children(self, component: Component) -> str:
        """Helper to render all children of a component."""
        parts = []
        for child in component.children:
            parts.append(self.render_component(child))
        return "\n".join(parts)
