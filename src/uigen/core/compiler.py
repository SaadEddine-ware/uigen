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

        if renderer_name == "lreact":
            return self._render_react(renderer, output_path)
        elif renderer_name == "lflask":
            return self._render_flask(renderer, output_path)
        elif renderer_name == "ldjango":
            return self._render_django(renderer, output_path)
        else:
            return self._render_native(renderer, output_path)

    def _render_native(self, renderer: Any, output_path: Path) -> Path:
        """Render pages as static HTML files."""
        for i, page in enumerate(self.pages):
            filename = "index.html" if i == 0 else f"page_{i}.html"
            content = renderer.render_page(page, title=self.title)
            (output_path / filename).write_text(content)
        return output_path

    def _render_react(self, renderer: Any, output_path: Path) -> Path:
        """Render pages as a React project."""
        components_dir = output_path / "src" / "components"
        components_dir.mkdir(parents=True, exist_ok=True)

        component_names = []
        for i, page in enumerate(self.pages):
            page_title = page.title or f"Page{i}"
            component_name = renderer._to_pascal_case(page_title)
            component_names.append(component_name)

            content = renderer.render_page(page, title=self.title)
            (components_dir / f"{component_name}.tsx").write_text(content)

        # Generate package.json
        (output_path / "package.json").write_text(
            renderer.generate_package_json(self.title)
        )

        # Generate index.html
        (output_path / "index.html").write_text(
            renderer.generate_index_html(self.title)
        )

        # Generate App.tsx
        (output_path / "src" / "App.tsx").write_text(
            renderer.generate_app_tsx(component_names)
        )

        # Generate index.tsx
        (output_path / "src" / "index.tsx").write_text(
            """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);"""
        )

        return output_path

    def _render_flask(self, renderer: Any, output_path: Path) -> Path:
        """Render pages as a Flask project."""
        templates_dir = output_path / "templates" / "pages"
        static_dir = output_path / "static"
        templates_dir.mkdir(parents=True, exist_ok=True)
        static_dir.mkdir(parents=True, exist_ok=True)

        route_names = []
        for i, page in enumerate(self.pages):
            page_title = page.title or f"Page{i}"
            route_name = renderer._to_snake_case(page_title)
            route_names.append(route_name)

            content = renderer.render_page(page, title=self.title)
            (templates_dir / f"{route_name}.html").write_text(content)

        # Generate base.html
        (output_path / "templates" / "base.html").write_text(
            renderer.generate_base_html(self.title)
        )

        # Generate app.py
        (output_path / "app.py").write_text(
            renderer.generate_app_py(self.title, route_names)
        )

        # Generate requirements.txt
        (output_path / "requirements.txt").write_text(
            renderer.generate_requirements()
        )

        return output_path

    def _render_django(self, renderer: Any, output_path: Path) -> Path:
        """Render pages as a Django project."""
        project_name = renderer._to_snake_case(self.title)
        templates_dir = output_path / "templates" / "pages"
        app_dir = output_path / project_name
        templates_dir.mkdir(parents=True, exist_ok=True)
        app_dir.mkdir(parents=True, exist_ok=True)

        route_names = []
        for i, page in enumerate(self.pages):
            page_title = page.title or f"Page{i}"
            route_name = renderer._to_snake_case(page_title)
            route_names.append(route_name)

            content = renderer.render_page(page, title=self.title)
            (templates_dir / f"{route_name}.html").write_text(content)

        # Generate base.html
        (output_path / "templates" / "base.html").write_text(
            renderer.generate_base_html(self.title)
        )

        # Generate views.py
        (app_dir / "views.py").write_text(
            renderer.generate_views_py(self.title, route_names)
        )

        # Generate urls.py
        (app_dir / "urls.py").write_text(
            renderer.generate_urls_py(route_names)
        )

        # Generate settings.py
        (output_path / "settings.py").write_text(
            renderer.generate_settings_py(self.title)
        )

        # Generate requirements.txt
        (output_path / "requirements.txt").write_text(
            renderer.generate_requirements()
        )

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
