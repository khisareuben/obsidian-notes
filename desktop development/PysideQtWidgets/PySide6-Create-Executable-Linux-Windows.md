# Creating an Executable for a PySide6 Project — Linux & Windows

How developers actually ship a PySide6 desktop app: build a standalone executable from your Python code so users don't need Python installed.

---

## 1. The Tool Developers Use: PyInstaller

Almost everyone uses **PyInstaller** for PySide6.

Why:
- Bundles Python + PySide6 + your code into one folder / one file
- Works on Linux and Windows
- Handles Qt plugins, images, `.qss`, `.ui` files if configured correctly
- No need for users to install Python

Alternatives you will hear about:
- **cx_Freeze** — good, but more config
- **Nuitka** — compiles to real C, faster startup, slower builds, harder to debug
- **Briefcase / fbs** — nice for polished installers, overkill for practice projects

> For learning + practice projects: start with PyInstaller. Learn Nuitka later if you need performance.

---

## 2. Prepare Your Project First

Developers don't build from a messy folder. Use this industry-standard structure:

```
my_app/
├── main.py
├── main_window.py
├── widget.py
├── style.qss
├── requirements.txt
├── README.md
├── assets/
│   ├── icons/
│   └── images/
└── .venv/
```

### Rules before building:

1. **Entry point must be one file:** `main.py`
2. **No absolute paths:** Never use `/home/...` or `C:\Users\...` in code
3. **Use paths relative to your file:**

```python
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
qss_path = BASE_DIR / "style.qss"
```

4. **Test from a clean venv:**

```bash
python -m venv .venv
source .venv/bin/activate  # Linux
# .venv\Scripts\activate  # Windows
pip install PySide6
pip install pyinstaller
```

5. **Freeze dependencies:**

```bash
pip freeze > requirements.txt
```

Your `requirements.txt` should look like:

```
PySide6==6.7.2
PyInstaller==6.10.0
```

---

## 3. Your `main.py` Should Look Like This

This is the pattern PyInstaller expects:

```python
# main.py
import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

### Loading `style.qss` correctly for both dev + exe:

PyInstaller extracts files to a temp folder when using `--onefile`. You need this helper:

```python
# main_window.py
import sys
from pathlib import Path
from PySide6.QtWidgets import QMainWindow

def resource_path(relative_path: str) -> Path:
    # Get absolute path to resource, works for dev and for PyInstaller.
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent
    return base_path / relative_path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.resize(900, 600)
        qss_file = resource_path("style.qss")
        if qss_file.exists():
            self.setStyleSheet(qss_file.read_text(encoding="utf-8"))
```

Use `resource_path()` for **every** asset: `.qss`, icons, images, `.db`, `.json`.

---

## 4. Build for Linux

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Build — One Folder (Recommended for dev)

```bash
pyinstaller --name "MyApp" \
            --windowed \
            --add-data "style.qss:." \
            --add-data "assets:assets" \
            main.py
```

Result:

```
dist/
└── MyApp/
    ├── MyApp       <- executable, double-click to run
    ├── style.qss
    └── assets/
```

Run it:

```bash
./dist/MyApp/MyApp
```

### Step 3: Build — One File (Easier to share)

```bash
pyinstaller --name "MyApp" \
            --windowed \
            --onefile \
            --add-data "style.qss:." \
            --add-data "assets:assets" \
            main.py
```

Result:

```
dist/
└── MyApp   <- single file
```

> Developers prefer `--onedir` (one folder) for real apps: faster startup, easier to debug, easier to update. Use `--onefile` only for simple sharing.

### Linux Notes:

- `--windowed` = no terminal window pops up
- `--add-data` syntax on Linux uses `:` -> `"source:destination"`
- The output is NOT portable to Windows. You must build on Linux for Linux.
- To make it executable from anywhere, users can move it to `~/.local/bin/` or create a `.desktop` file.

### Optional: Make a `.desktop` launcher (Linux)

Create `MyApp.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=MyApp
Exec=/home/user/MyApp/MyApp
Icon=/home/user/MyApp/assets/icons/app.png
Terminal=false
Categories=Utility;
```

---

## 5. Build for Windows

You **must** build on Windows. A Linux build will NOT run on Windows.

### Step 1: On a Windows PC, setup venv

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install PySide6 pyinstaller
```

### Step 2: Build — One Folder (Recommended)

```powershell
pyinstaller --name "MyApp" `
            --windowed `
            --add-data "style.qss;." `
            --add-data "assets;assets" `
            main.py
```

Result:

```
dist\
└── MyApp\
    ├── MyApp.exe
    ├── style.qss
    └── assets\
```

### Step 3: Build — One File

```powershell
pyinstaller --name "MyApp" `
            --windowed `
            --onefile `
            --add-data "style.qss;." `
            --add-data "assets;assets" `
            main.py
```

Result:

```
dist\
└── MyApp.exe
```

### Windows Notes:

- `--add-data` syntax on Windows uses `;` -> `"source;destination"` — this is the #1 mistake
- `--windowed` = no console window. If you need to see `print()` errors while debugging, remove `--windowed` and use `--console`
- Add an icon:

```powershell
pyinstaller --name "MyApp" --windowed --onefile --icon "assets/icons/app.ico" main.py
```

Icon must be `.ico` on Windows, `.png` on Linux.

### How to get Windows if you only have Linux:

1. Use a Windows VM (VirtualBox / VMware)
2. Use a friend's Windows PC
3. Use GitHub Actions (see Section 8) — builds Windows exe automatically from Linux

---

## 6. The Professional Way: Use a `.spec` File

After your first build, PyInstaller creates `MyApp.spec`. Developers edit this file and reuse it instead of typing long commands.

### Example `MyApp.spec`:

```python
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('style.qss', '.'),
        ('assets', 'assets'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MyApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icons/app.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MyApp',
)
```

Then build with just:

```bash
# Linux
pyinstaller MyApp.spec

# Windows
pyinstaller MyApp.spec
```

> Keep the `.spec` file in git. It's your build recipe.

---

## 7. Common Problems & Fixes

| Problem | Cause | Fix |
|---|---|---|
| App opens then closes instantly | Missing `.qss` / asset / crash hidden by `--windowed` | Build without `--windowed` once to see error, or check with `--console` |
| `FileNotFoundError: style.qss` | Used relative path like `open("style.qss")` | Use `resource_path()` helper from Section 3 |
| Icons / images missing in exe | Forgot `--add-data` | Add `--add-data "assets:assets"` (Linux) / `"assets;assets"` (Windows) |
| `ModuleNotFoundError` | PyInstaller missed a hidden import | Add `--hidden-import=module_name` or add to `hiddenimports` in `.spec` |
| Exe is very big (80-150MB) | Normal for PySide6 | Use `--onedir` + UPX, don't worry. PySide6 bundles all of Qt |
| Antivirus flags Windows exe | Common with PyInstaller onefile | Use `--onedir`, sign exe, or distribute via installer |
| Works on your PC, not on friend's | Missing Qt plugins / built on different OS | Always build on target OS, ship whole `dist/MyApp/` folder |

### Debug command (use this when it fails):

```bash
# Linux
pyinstaller --name "MyApp" --console --onefile main.py
./dist/MyApp

# Windows
pyinstaller --name "MyApp" --console --onefile main.py
.\dist\MyApp.exe
```

You will see the real error in terminal.

---

## 8. How Real Developers Ship It (Next Level)

For practice projects, `dist/` is enough. For real apps:

### Option A: GitHub Actions — Auto-build for both OS

Push code to GitHub, GitHub builds Linux + Windows exe automatically. You download them from Actions tab.

Create `.github/workflows/build.yml`:

```yaml
name: Build Executables
on:
  push:
    tags:
      - 'v*'
jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install PySide6 pyinstaller
      - run: pyinstaller MyApp.spec
      - uses: actions/upload-artifact@v4
        with:
          name: MyApp-${{ matrix.os }}
          path: dist/
```

### Option B: Create a real installer (Windows)

Use **Inno Setup** (free) to turn `dist/MyApp/` into a `MyAppSetup.exe` installer like real software.

### Option C: Create a real installer (Linux)

Use **AppImage** or **Flatpak**, or just zip the `dist/MyApp/` folder.

---

## 9. Quick Cheat Sheet

```bash
# --- Linux ---
pip install pyinstaller
pyinstaller --name "MyApp" --windowed --add-data "style.qss:." --add-data "assets:assets" main.py
# Output: dist/MyApp/MyApp

# --- Windows (PowerShell) ---
pip install pyinstaller
pyinstaller --name "MyApp" --windowed --add-data "style.qss;." --add-data "assets;assets" main.py
# Output: dist\MyApp\MyApp.exe

# --- Rebuild from spec (both OS) ---
pyinstaller MyApp.spec

# --- Clean rebuild ---
rm -rf build/ dist/ *.spec  # Linux
# Remove-Item -Recurse build, dist  # Windows PowerShell
```

---

## 10. Checklist Before You Share

- [ ] `main.py` is the only entry point
- [ ] All file loads use `resource_path()`
- [ ] Tested from clean `.venv`
- [ ] Built on the target OS (Linux build for Linux, Windows build for Windows)
- [ ] Shipped the whole `dist/MyApp/` folder if using `--onedir`
- [ ] Tested the exe on a different PC / VM without Python installed
- [ ] `requirements.txt` and `MyApp.spec` committed to git

---

*Built for a PySide6 project using `main.py`, `main_window.py`, `widget.py`, `style.qss` structure.*
