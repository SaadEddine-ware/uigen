from PIL import Image, ImageDraw, ImageFont
import os

frames = []
width, height = 1200, 700

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 36)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 22)
except:
    font = ImageFont.load_default()
    font_small = font

def make_frame(lines, title=None, title_color=(139, 92, 246)):
    img = Image.new('RGB', (width, height), color=(30, 30, 46))
    draw = ImageDraw.Draw(img)
    y = 100
    if title:
        draw.text((80, y), title, fill=title_color, font=font)
        y += 80
    for text, color in lines:
        draw.text((80, y), text, fill=color, font=font_small)
        y += 40
    return img

green = (166, 227, 161)
white = (205, 214, 244)
pink = (243, 139, 168)
purple = (139, 92, 246)
yellow = (249, 226, 175)

frames.append(make_frame([
    ("Write UI logic once, deploy anywhere.", white),
]))

frames.append(make_frame([
    ("The Problem:", pink),
    ("", white),
    ("35+ lines of HTML for a basic table:", white),
    ("", white),
    ('<div class="bg-white rounded-lg shadow-md p-6">', green),
    ('  <h2 class="text-2xl font-semibold">Users</h2>', green),
    ('  <table class="w-full">', green),
    ('    <thead>...', green),
    ('    <tbody>...</tbody>', green),
    ('  </table>', green),
    ('</div>', green),
]))

frames.append(make_frame([
    ("The Solution:", purple),
    ("", white),
    ("15 lines of Python:", white),
    ("", white),
    ("from uigen import App, Model, ui", green),
    ("", white),
    ("class User(Model):", green),
    ("    name: str", green),
    ("    email: str", green),
    ('    role: str = "viewer"', green),
    ("", white),
    ('app.render("lnative", output="./dist")', yellow),
]))

frames.append(make_frame([
    ("Result: 57% less code", purple),
    ("", white),
    ("Lines:   35+   ->   15", white),
    ("Chars:   ~1500  ->   ~500", white),
    ("Time:    10-15 min  ->  2-3 min", white),
]))

frames.append(make_frame([
    ("4 Renderers", purple),
    ("", white),
    ("lnative   Static HTML/CSS/JS", white),
    ("lreact    React components", white),
    ("lflask    Flask/Jinja2 templates", white),
    ("ldjango   Django templates", white),
]))

frames.append(make_frame([
    ("Get Started", purple),
    ("", white),
    ("pip install uigen", green),
    ("uigen init my-app", green),
    ("cd my-app", green),
    ("python main.py", green),
    ("open dist/index.html", green),
]))

frames.append(make_frame([
    ("github.com/SaadEddine-ware/uigen", purple),
    ("", white),
    ("pip install uigen", white),
]))

frames[0].save(
    'docs/demo.gif',
    save_all=True,
    append_images=frames[1:],
    duration=[2500, 4000, 4000, 3000, 3000, 3500, 2500],
    loop=0,
    optimize=True
)

print(f"Created docs/demo.gif ({os.path.getsize('docs/demo.gif')//1024}KB)")
