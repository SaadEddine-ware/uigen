#!/usr/bin/env python3
"""Demo script for uigen — shows the power of code generation.

Run this script to see uigen in action:

    python examples/demo.py

It will generate all 4 renderers and show the before/after comparison.
"""

import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from uigen import App, Model, ui


def print_header(text: str) -> None:
    """Print a styled header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_code(code: str) -> None:
    """Print code with syntax highlighting (basic)."""
    for line in code.split("\n"):
        print(f"  │ {line}")
    print()


def demo_before():
    """Show the 'before' — raw HTML."""
    print_header("BEFORE: Writing HTML manually")
    print_code("""<div class="bg-white rounded-lg shadow-md p-6">
  <h2 class="text-2xl font-semibold text-gray-900 mb-4">Users</h2>
  <table class="w-full">
    <thead>
      <tr class="border-b border-gray-200">
        <th class="px-4 py-2 text-left text-sm font-medium text-gray-700">Name</th>
        <th class="px-4 py-2 text-left text-sm font-medium text-gray-700">Email</th>
        <th class="px-4 py-2 text-left text-sm font-medium text-gray-700">Role</th>
      </tr>
    </thead>
    <tbody>
      <tr class="border-t border-gray-200">
        <td class="px-4 py-2 text-sm text-gray-600">Alice Johnson</td>
        <td class="px-4 py-2 text-sm text-gray-600">alice@example.com</td>
        <td class="px-4 py-2 text-sm text-gray-600">admin</td>
      </tr>
      <tr class="border-t border-gray-200">
        <td class="px-4 py-2 text-sm text-gray-600">Bob Smith</td>
        <td class="px-4 py-2 text-sm text-gray-600">bob@example.com</td>
        <td class="px-4 py-2 text-sm text-gray-600">viewer</td>
      </tr>
    </tbody>
  </table>
  <button class="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
    Add User
  </button>
</div>""")
    print(f"  Lines of code: 35+")
    print(f"  Time to write: 10-15 minutes")


def demo_after():
    """Show the 'after' — Python with uigen."""
    print_header("AFTER: Writing Python with uigen")
    print_code("""from uigen import App, Model, ui

class User(Model):
    name: str
    email: str
    role: str = "viewer"

page = ui.page(
    ui.card(
        ui.heading("Users"),
        ui.table(data=[
            {"name": "Alice Johnson", "email": "alice@example.com", "role": "admin"},
            {"name": "Bob Smith", "email": "bob@example.com", "role": "viewer"},
        ]),
        ui.button("Add User"),
    ),
    title="User Management",
)

app = App(title="My App", pages=[page])
app.render("lnative", output="./dist")""")
    print(f"  Lines of code: 18")
    print(f"  Time to write: 2-3 minutes")


def demo_generators():
    """Show all 4 generators in action."""
    print_header("DEMO: Generate 4 outputs from the same code")

    # Define the app
    class User(Model):
        name: str
        email: str
        role: str = "viewer"

    page = ui.page(
        ui.card(
            ui.heading("Users"),
            ui.table(data=[
                {"name": "Alice", "email": "alice@example.com", "role": "admin"},
                {"name": "Bob", "email": "bob@example.com", "role": "viewer"},
            ]),
            ui.button("Add User"),
        ),
        title="User Management",
    )

    app = App(title="My App", pages=[page])

    # Generate all 4 outputs
    renderers = ["lnative", "lreact", "lflask", "ldjango"]
    outputs = {}

    for renderer in renderers:
        output_dir = Path(f"demo-output/{renderer}")
        start = time.time()
        app.render(renderer, output=str(output_dir))
        elapsed = time.time() - start
        outputs[renderer] = (output_dir, elapsed)

        # Count files
        file_count = sum(1 for _ in output_dir.rglob("*") if _.is_file())
        print(f"  ✓ {renderer:10} → {output_dir} ({file_count} files, {elapsed:.3f}s)")

    print()
    return outputs


def demo_comparison():
    """Show a side-by-side comparison."""
    print_header("COMPARISON: HTML vs Python")

    html_lines = 35
    python_lines = 18
    reduction = ((html_lines - python_lines) / html_lines) * 100

    print(f"  {'Metric':<20} {'HTML':<15} {'Python (uigen)':<15}")
    print(f"  {'─' * 50}")
    print(f"  {'Lines of code':<20} {html_lines:<15} {python_lines:<15}")
    print(f"  {'Characters':<20} {'~1,500':<15} {'~600':<15}")
    print(f"  {'Time to write':<20} {'10-15 min':<15} {'2-3 min':<15}")
    print(f"  {'Reduction':<20} {'—':<15} {f'{reduction:.0f}%':<15}")
    print()


def demo_next_steps():
    """Show next steps."""
    print_header("NEXT STEPS")
    print("""
  1. Install uigen:
     pip install uigen

  2. Create a project:
     uigen init my-app

  3. Edit main.py with your UI

  4. Generate:
     uigen generate --renderer lnative

  5. Open dist/index.html in your browser

  Documentation: https://github.com/SaadEddine-ware/uigen
""")


def main():
    """Run the full demo."""
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║" + " uigen — Write UI logic once, deploy anywhere ".center(58) + "║")
    print("╚" + "═" * 58 + "╝")

    demo_before()
    demo_after()
    outputs = demo_generators()
    demo_comparison()
    demo_next_steps()

    # Cleanup
    print("Cleaning up demo output...")
    import shutil
    demo_dir = Path("demo-output")
    if demo_dir.exists():
        shutil.rmtree(demo_dir)
    print("Done!\n")


if __name__ == "__main__":
    main()
