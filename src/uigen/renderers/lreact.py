"""lreact renderer — generates React component files."""

from __future__ import annotations

from pathlib import Path
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
from uigen.renderers.base import BaseRenderer


class LReactRenderer(BaseRenderer):
    """Generates React component files with TypeScript support."""

    def render_page(self, page: Page, title: str = "") -> str:
        """Render a Page as a React component."""
        page_title = title or page.title or "GeneratedPage"
        component_name = self._to_pascal_case(page_title)
        children = self._render_children(page)

        return f"""import React, {{ useState }} from 'react';

interface {component_name}Props {{
  className?: string;
}}

export const {component_name}: React.FC<{component_name}Props> = ({{ className }}) => {{
  return (
    <div className={{`min-h-screen bg-gray-50 p-8 ${{className || ''}}`}}>
      <div className="max-w-6xl mx-auto">
{children}
      </div>
    </div>
  );
}};

export default {component_name};
"""

    def render_component(self, component: Component) -> str:
        """Render a single component to React JSX."""
        renderer = _RENDERERS.get(type(component))
        if renderer is None:
            return self._render_generic(component)
        return renderer(self, component)

    def _render_generic(self, component: Component) -> str:
        children = self._render_children(component)
        return f"<div>{children}</div>"

    def _render_page(self, component: Page) -> str:
        return self._render_children(component)

    def _render_card(self, component: Card) -> str:
        children = self._render_children(component)
        return (
            '<div className="bg-white rounded-lg shadow-md p-6">\n'
            f"{children}\n"
            "</div>"
        )

    def _render_heading(self, component: Heading) -> str:
        tag = f"h{component.level}"
        size_classes = {
            1: "text-3xl font-bold",
            2: "text-2xl font-semibold",
            3: "text-xl font-medium",
            4: "text-lg",
        }
        cls = size_classes.get(component.level, "text-lg")
        return f'<{tag} className="{cls} text-gray-900 mb-4">{component.text}</{tag}>'

    def _render_text(self, component: Text) -> str:
        return f'<p className="text-gray-600">{component.text}</p>'

    def _render_button(self, component: Button) -> str:
        variants = {
            "primary": "bg-blue-600 hover:bg-blue-700 text-white",
            "secondary": "bg-gray-200 hover:bg-gray-300 text-gray-800",
            "danger": "bg-red-600 hover:bg-red-700 text-white",
        }
        cls = variants.get(component.variant, variants["primary"])
        onclick = component.attrs.get("onclick", "")
        handler = self._to_handler_name(onclick) if onclick else None
        click_prop = f" onClick={{{handler}}}" if handler else ""
        classes = f'{cls} px-4 py-2 rounded-lg font-medium transition'
        return f'<button className="{classes}"{click_prop}>{component.text}</button>'

    def _render_input(self, component: Input) -> str:
        label = ""
        if component.label:
            label = (
                f'<label className="block text-sm font-medium '
                f'text-gray-700 mb-1">{component.label}</label>\n'
            )
        input_type = component.attrs.get("type", "text")
        name = component.attrs.get("name", "")
        placeholder = component.attrs.get("placeholder", "")
        required = " required" if component.attrs.get("required") else ""

        return (
            f"{label}"
            f'<input type="{input_type}" name="{name}" '
            f'placeholder="{placeholder}"{required} '
            f'className="w-full px-3 py-2 border border-gray-300 rounded-lg '
            f'focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />'
        )

    def _render_select(self, component: Select) -> str:
        label = ""
        if component.label:
            label = (
                f'<label className="block text-sm font-medium '
                f'text-gray-700 mb-1">{component.label}</label>\n'
            )
        options = "\n".join(
            f'<option value="{opt}">{opt}</option>'
            for opt in component.options
        )
        return (
            f"{label}"
            f'<select name="{component.name}" '
            f'className="w-full px-3 py-2 border border-gray-300 rounded-lg '
            f'focus:ring-2 focus:ring-blue-500">\n'
            f"{options}\n"
            f"</select>"
        )

    def _render_table(self, component: Table) -> str:
        if not component.columns:
            return '<p className="text-gray-500">No data</p>'

        header = "".join(
            f'<th className="px-4 py-2 text-left text-sm font-medium text-gray-700">{col}</th>'
            for col in component.columns
        )

        rows = ""
        for row in component.rows:
            cells = "".join(
                f'<td className="px-4 py-2 text-sm text-gray-600">{row.get(col, "")}</td>'
                for col in component.columns
            )
            rows += f"<tr className=\"border-t border-gray-200\">\n{cells}\n</tr>\n"

        return (
            '<table className="w-full">\n'
            f'<thead><tr className="border-b border-gray-200">{header}</tr></thead>\n'
            f"<tbody>\n{rows}</tbody>\n</table>"
        )

    def _render_form(self, component: Form) -> str:
        children = self._render_children(component)
        action = component.attrs.get("action", "")
        method = component.method

        return (
            f'<form method="{method}" action="{action}" '
            f'className="space-y-4">\n'
            f"{children}\n</form>"
        )

    def _render_modal(self, component: Modal) -> str:
        modal_var = self._to_var_name(component.title or "modal")
        children = self._render_children(component)
        title = ""
        if component.title:
            title = f'<h2 className="text-xl font-bold mb-4">{component.title}</h2>\n'

        return (
            f"{{/* Modal: {component.title or 'Dialog'} */}}\n"
            f"{{isOpen_{modal_var} && (\n"
            f'<div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">\n'
            f'<div className="bg-white rounded-lg p-6 max-w-md w-full">\n'
            f"{title}"
            f"{children}\n"
            f'<button onClick={{() => setIsOpen_{modal_var}(false)}} '
            f'className="mt-4 text-gray-500 hover:text-gray-700">Close</button>\n'
            f"</div>\n</div>\n)}}\n"
        )

    def _render_grid(self, component: Grid) -> str:
        cols = component.attrs.get("columns", 2)
        children = self._render_children(component)
        return f'<div className="grid grid-cols-{cols} gap-4">\n{children}\n</div>'

    def _render_stack(self, component: Stack) -> str:
        spacing = component.attrs.get("spacing", "md")
        spacing_map = {"sm": "space-y-2", "md": "space-y-4", "lg": "space-y-6"}
        cls = spacing_map.get(spacing, "space-y-4")
        children = self._render_children(component)
        return f'<div className="{cls}">\n{children}\n</div>'

    def _to_pascal_case(self, text: str) -> str:
        """Convert text to PascalCase for component names."""
        return "".join(word.capitalize() for word in text.split() if word.isalnum())

    def _to_var_name(self, text: str) -> str:
        """Convert text to camelCase for variable names."""
        words = text.split()
        if not words:
            return "item"
        return words[0].lower() + "".join(w.capitalize() for w in words[1:])

    def _to_handler_name(self, onclick: str) -> str:
        """Convert onclick string to React handler name."""
        if onclick.startswith("showModal("):
            modal_id = onclick.replace("showModal(", "").replace(")", "")
            return f"() => setIsOpen_{self._to_var_name(modal_id)}(true)"
        elif onclick.startswith("hideModal("):
            modal_id = onclick.replace("hideModal(", "").replace(")", "")
            return f"() => setIsOpen_{self._to_var_name(modal_id)}(false)"
        return f"() => console.log('{onclick}')"

    def generate_package_json(self, title: str) -> str:
        """Generate a package.json for the React project."""
        name = title.lower().replace(" ", "-").replace("_", "-")
        return f"""{{
  "name": "{name}",
  "version": "0.1.0",
  "private": true,
  "dependencies": {{
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "typescript": "^4.9.5",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0"
  }},
  "scripts": {{
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }},
  "browserslist": {{
    "production": [">0.2%", "not dead", "not op_mini all"],
    "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
  }}
}}"""

    def generate_index_html(self, title: str) -> str:
        """Generate index.html for the React project."""
        return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>"""

    def generate_app_tsx(self, page_components: list[str]) -> str:
        """Generate the main App.tsx file."""
        imports = "\n".join(
            f"import {comp} from './components/{comp}';"
            for comp in page_components
        )
        routes = "\n".join(
            f'      <Route path="/{comp.lower()}" element={{<{comp} />}} />'
            for comp in page_components
        )

        return f"""import React from 'react';
{{imports}}

function App() {{
  return (
    <div className="App">
      <nav className="bg-white shadow-md p-4 mb-8">
        <div className="max-w-6xl mx-auto flex gap-4">
          <a href="/" className="text-gray-800 hover:text-blue-600">Home</a>
{chr(10).join(f'          <a href("/{c.lower()}" className="text-gray-800 hover:text-blue-600">{c}</a>' for c in page_components)}
        </div>
      </nav>
      <main>
{routes}
      </main>
    </div>
  );
}}

export default App;"""


_RENDERERS = {
    Page: LReactRenderer._render_page,
    Card: LReactRenderer._render_card,
    Heading: LReactRenderer._render_heading,
    Text: LReactRenderer._render_text,
    Button: LReactRenderer._render_button,
    Input: LReactRenderer._render_input,
    Select: LReactRenderer._render_select,
    Table: LReactRenderer._render_table,
    Form: LReactRenderer._render_form,
    Modal: LReactRenderer._render_modal,
    Grid: LReactRenderer._render_grid,
    Stack: LReactRenderer._render_stack,
}
