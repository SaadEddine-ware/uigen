"""lflask renderer — generates Flask/Jinja2 templates."""

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


class LFlaskRenderer(BaseRenderer):
    """Generates Flask application with Jinja2 templates."""

    def render_page(self, page: Page, title: str = "") -> str:
        """Render a Page as a Jinja2 template."""
        page_title = title or page.title or "GeneratedPage"
        template_name = self._to_snake_case(page_title)
        children = self._render_children(page)

        return f"""{{% extends "base.html" %}}

{{% block title %}}{page_title}{{% endblock %}}

{{% block content %}}
{children}
{{% endblock %}}
"""

    def render_component(self, component: Component) -> str:
        """Render a single component to Jinja2 HTML."""
        renderer = _RENDERERS.get(type(component))
        if renderer is None:
            return self._render_generic(component)
        return renderer(self, component)

    def _render_generic(self, component: Component) -> str:
        children = self._render_children(component)
        return f'<div>\n{children}\n</div>'

    def _render_page(self, component: Page) -> str:
        return self._render_children(component)

    def _render_card(self, component: Card) -> str:
        children = self._render_children(component)
        return (
            '<div class="bg-white rounded-lg shadow-md p-6">\n'
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
        return f'<{tag} class="{cls} text-gray-900 mb-4">{component.text}</{tag}>'

    def _render_text(self, component: Text) -> str:
        return f'<p class="text-gray-600">{component.text}</p>'

    def _render_button(self, component: Button) -> str:
        variants = {
            "primary": "bg-blue-600 hover:bg-blue-700 text-white",
            "secondary": "bg-gray-200 hover:bg-gray-300 text-gray-800",
            "danger": "bg-red-600 hover:bg-red-700 text-white",
        }
        cls = variants.get(component.variant, variants["primary"])
        onclick = component.attrs.get("onclick", "")
        url = self._onclick_to_url(onclick)
        href = f' href="{{{{ url_for(\'{url}\') }}}}"' if url else ""
        classes = f'{cls} px-4 py-2 rounded-lg font-medium transition'
        return f'<a class="{classes}"{href}>{component.text}</a>'

    def _render_input(self, component: Input) -> str:
        label = ""
        if component.label:
            label = (
                f'<label class="block text-sm font-medium '
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
            f'class="w-full px-3 py-2 border border-gray-300 rounded-lg '
            f'focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />'
        )

    def _render_select(self, component: Select) -> str:
        label = ""
        if component.label:
            label = (
                f'<label class="block text-sm font-medium '
                f'text-gray-700 mb-1">{component.label}</label>\n'
            )
        options = "\n".join(
            f'<option value="{{{{ option }}}}">{{{{ option }}}}</option>'
            for opt in component.options
        )
        # For Flask, we use a generic loop
        return (
            f"{label}"
            f'<select name="{component.name}" '
            f'class="w-full px-3 py-2 border border-gray-300 rounded-lg '
            f'focus:ring-2 focus:ring-blue-500">\n'
            f'{{% for option in {component.name}_options %}}\n'
            f'<option value="{{{{ option }}}}">{{{{ option }}}}</option>\n'
            f'{{% endfor %}}\n'
            f"</select>"
        )

    def _render_table(self, component: Table) -> str:
        if not component.columns:
            return '<p class="text-gray-500">No data</p>'

        header = "".join(
            f'<th class="px-4 py-2 text-left text-sm font-medium text-gray-700">{col}</th>'
            for col in component.columns
        )

        # For Flask, we use Jinja2 loops
        row_cells = "".join(
            f'<td class="px-4 py-2 text-sm text-gray-600">'
            f'{{{{ row.{col} }}}}</td>'
            for col in component.columns
        )

        return (
            '<table class="w-full">\n'
            f'<thead><tr class="border-b border-gray-200">{header}</tr></thead>\n'
            f"<tbody>\n"
            f'{{% for row in table_data %}}\n'
            f'<tr class="border-t border-gray-200">\n'
            f"{row_cells}\n</tr>\n"
            f'{{% endfor %}}\n'
            f"</tbody>\n</table>"
        )

    def _render_form(self, component: Form) -> str:
        children = self._render_children(component)
        action = component.attrs.get("action", "")
        method = component.method

        action_url = ""
        if action:
            route = action.strip("/")
            action_url = f' action="{{{{ url_for(\'{route}\') }}}}"'

        return (
            f'<form method="{method}"{action_url} '
            f'class="space-y-4">\n'
            f"{children}\n</form>"
        )

    def _render_modal(self, component: Modal) -> str:
        modal_id = self._to_snake_case(component.title or "modal")
        children = self._render_children(component)
        title = ""
        if component.title:
            title = f'<h2 class="text-xl font-bold mb-4">{component.title}</h2>\n'

        return (
            f'<!-- Modal: {component.title or "Dialog"} -->\n'
            f'<div id="{modal_id}" class="modal hidden fixed inset-0 '
            f'bg-black/50 flex items-center justify-center z-50">\n'
            f'<div class="bg-white rounded-lg p-6 max-w-md w-full">\n'
            f"{title}"
            f"{children}\n"
            f'<button onclick="document.getElementById(\'{modal_id}\').classList.add(\'hidden\')" '
            f'class="mt-4 text-gray-500 hover:text-gray-700">Close</button>\n'
            f"</div>\n</div>\n"
            f'<script>\n'
            f"function show_{modal_id}() {{\n"
            f"  document.getElementById('{modal_id}').classList.remove('hidden');\n"
            f"}}\n"
            f"</script>"
        )

    def _render_grid(self, component: Grid) -> str:
        cols = component.attrs.get("columns", 2)
        children = self._render_children(component)
        return f'<div class="grid grid-cols-{cols} gap-4">\n{children}\n</div>'

    def _render_stack(self, component: Stack) -> str:
        spacing = component.attrs.get("spacing", "md")
        spacing_map = {"sm": "space-y-2", "md": "space-y-4", "lg": "space-y-6"}
        cls = spacing_map.get(spacing, "space-y-4")
        children = self._render_children(component)
        return f'<div class="{cls}">\n{children}\n</div>'

    def _to_snake_case(self, text: str) -> str:
        """Convert text to snake_case for file names."""
        return text.lower().replace(" ", "_").replace("-", "_")

    def _onclick_to_url(self, onclick: str) -> str:
        """Convert onclick to Flask url_for route."""
        if onclick.startswith("showModal("):
            return "index"  # Default route
        elif onclick.startswith("hideModal("):
            return "index"
        return onclick if onclick else ""

    def generate_app_py(self, title: str, routes: list[str]) -> str:
        """Generate the Flask app.py file."""
        route_definitions = []
        for route in routes:
            route_name = self._to_snake_case(route)
            if route_name == "index":
                route_definitions.append(
                    f'''@app.route("/")
def index():
    return render_template("pages/{route_name}.html")'''
                )
            else:
                route_definitions.append(
                    f'''@app.route("/{route_name}")
def {route_name}():
    return render_template("pages/{route_name}.html")'''
                )

        routes_code = "\n\n".join(route_definitions)

        return f'''"""Generated by uigen — {title}"""

from flask import Flask, render_template

app = Flask(__name__)


{routes_code}


if __name__ == "__main__":
    app.run(debug=True)
'''

    def generate_base_html(self, title: str) -> str:
        """Generate the base.html template."""
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{% block title %}}{title}{{% endblock %}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .modal {{ display: none; }}
        .modal.active {{ display: flex; }}
    </style>
</head>
<body class="bg-gray-50 min-h-screen p-8">
    <nav class="max-w-6xl mx-auto mb-8">
        <div class="bg-white rounded-lg shadow-md p-4 flex gap-4">
            <a href="{{{{ url_for('index') }}}}" class="text-gray-800 hover:text-blue-600">Home</a>
        </div>
    </nav>
    <main class="max-w-6xl mx-auto">
        {{% block content %}}{{% endblock %}}
    </main>
    <script>
        function showModal(id) {{
            document.getElementById(id).classList.remove('hidden');
        }}
        function hideModal(id) {{
            document.getElementById(id).classList.add('hidden');
        }}
    </script>
</body>
</html>'''

    def generate_requirements(self) -> str:
        """Generate requirements.txt."""
        return "flask>=3.0.0\n"


_RENDERERS = {
    Page: LFlaskRenderer._render_page,
    Card: LFlaskRenderer._render_card,
    Heading: LFlaskRenderer._render_heading,
    Text: LFlaskRenderer._render_text,
    Button: LFlaskRenderer._render_button,
    Input: LFlaskRenderer._render_input,
    Select: LFlaskRenderer._render_select,
    Table: LFlaskRenderer._render_table,
    Form: LFlaskRenderer._render_form,
    Modal: LFlaskRenderer._render_modal,
    Grid: LFlaskRenderer._render_grid,
    Stack: LFlaskRenderer._render_stack,
}
