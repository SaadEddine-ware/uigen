"""Compiler — transforms UI definitions into renderer output."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from uigen.core.components import Page
from uigen.core.schema import Model


class App:
    """Main application class that wires models and pages to renderers."""

    def __init__(
        self,
        title: str = "My App",
        models: list[type[Model]] | None = None,
        pages: list[Page] | None = None,
    ) -> None:
        self.title = title
        self.models = models or []
        self.pages = pages or []
        self._renderer: Any = None

    def add_page(self, page: Page) -> App:
        """Add a page to the app."""
        self.pages.append(page)
        return self

    def render(self, renderer_name: str, output: str = "./dist") -> Path:
        """Render all pages using the specified renderer.

        Args:
            renderer_name: Name of the renderer (e.g., "lnative", "lreact").
            output: Output directory path.

        Returns:
            Path to the output directory.
        """
        renderer = self._get_renderer(renderer_name)
        output_path = Path(output)
        output_path.mkdir(parents=True, exist_ok=True)

        for i, page in enumerate(self.pages):
            filename = "index.html" if i == 0 else f"page_{i}.html"
            content = renderer.render_page(page, title=self.title)
            (output_path / filename).write_text(content)

        return output_path

    def _get_renderer(self, name: str) -> Any:
        """Import and instantiate a renderer by name."""
        if name == "lnative":
            from uigen.renderers.lnative import LNativeRenderer
            return LNativeRenderer()
        elif name == "lreact":
            from uigen.renderers.lreact import LReactRenderer
            return LReactRenderer()
        elif name == "lflask":
            from uigen.renderers.lflask import LFlaskRenderer
            return LFlaskRenderer()
        elif name == "ldjango":
            from uigen.renderers.ldjango import LDjangoRenderer
            return LDjangoRenderer()
        else:
            available = "lnative, lreact, lflask, ldjango"
            raise ValueError(
                f"Unknown renderer: {name}. Available: {available}"
            )

    def __repr__(self) -> str:
        return (
            f"App(title={self.title!r}, "
            f"pages={len(self.pages)}, models={len(self.models)})"
        )
