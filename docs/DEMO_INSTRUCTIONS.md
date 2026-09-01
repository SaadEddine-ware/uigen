# Demo GIF Instructions

Since we can't record a GIF directly, here's how to create one:

## Option 1: Use VHS (Recommended)

[VHS](https://github.com/charmbracelet/vhs) creates terminal recordings as GIFs.

1. Install VHS:
   ```bash
   go install github.com/charmbracelet/vhs@latest
   ```

2. Create a tape file `demo.tape`:
   ```
   Output demo.gif
   Width 1200
   Height 800
   FontSize 16

   type "pip install uigen"
   enter
   sleep 1s

   type "uigen init my-store"
   enter
   sleep 1s

   type "cd my-store"
   enter
   sleep 500ms

   type "cat main.py"
   enter
   sleep 2s

   type "python main.py"
   enter
   sleep 1s

   type "open dist/index.html"
   enter
   sleep 2s
   ```

3. Run VHS:
   ```bash
   vhs demo.tape
   ```

## Option 2: Useasciinema + agg

1. Record:
   ```bash
   asciinema rec demo.cast
   ```

2. Convert to GIF:
   ```bash
   agg demo.cast demo.gif
   ```

## Option 3: Use Loom or OBS

1. Open terminal
2. Record screen while running:
   ```bash
   pip install uigen
   uigen init my-store
   cd my-store
   python main.py
   ```
3. Edit and export as GIF

## Demo Script

Run the demo script to see uigen in action:

```bash
python examples/demo.py
```

This shows:
- Before (raw HTML)
- After (Python with uigen)
- Generating all 4 outputs
- Performance comparison
