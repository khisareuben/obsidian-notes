# QTAWESOME OFFLINE - Full Detailed Guide for PySide6 (You are mostly offline)

This is Method 2 - the best offline icon solution. After one download, works forever without internet.

---

## WHAT IS QTAWESOME?

- Python package that bundles icon fonts: FontAwesome 4, FontAwesome 5, Material Design Icons, Elusive Icons, etc.
- 1000+ icons inside .ttf font files, no internet needed after install
- Designed for Qt (PySide6, PyQt5, PyQt6)
- Colors, sizes, animations supported

---

## PART 1: INSTALL OFFLINE (Do Once)

### On PC WITH Internet (once):

```bash
mkdir offline_packages
cd offline_packages
pip download qtawesome
pip download qtpy
```

You will get 2 files like:
- qtawesome-1.4.2-py3-none-any.whl
- QtPy-2.4.3-py3-none-any.whl

Copy that whole `offline_packages` folder to USB stick.

### On your OFFLINE PC (your main PC):

You got error before because `./offline_packages` is relative. Use absolute path.

**Fix A: Use absolute path (Linux/Mac):**
```bash
pwd
# shows /home/yourname/offline_packages

pip install --no-index --find-links=/home/yourname/offline_packages qtawesome
```

**Fix B: Use file:// scheme (Windows):**
```bash
pip install --no-index --find-links=file:///C:/Users/YourName/offline_packages qtawesome
```

**Fix C: Easiest - cd into folder:**
```bash
cd offline_packages
pip install --no-index --find-links=. qtawesome
# OR
pip install *.whl
```

If it says "already installed", you are done!

Test:
```bash
python -c "import qtawesome as qta; print('qtawesome works')"
```

---

## PART 2: HOW TO USE IN PYSIDE6 PROJECTS

### Basic Import:

```python
import qtawesome as qta
from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow

app = QApplication([])

btn = QPushButton(" Search")
btn.setIcon(qta.icon('mdi.magnify', color='white'))
btn.show()

app.exec()
```

### Syntax:

```python
qta.icon('PREFIX.NAME', color='color', color_active='hover_color', size=24)
```

- PREFIX: fa, fa5, fa5s, fa5b, mdi, ei
- NAME: icon name like book, magnify, bookmark

### Examples for your Bible App:

```python
import qtawesome as qta

# Top toolbar
search_btn.setIcon(qta.icon('mdi.magnify', color='white'))
font_down.setIcon(qta.icon('mdi.format-font-size-decrease', color='white'))
font_up.setIcon(qta.icon('mdi.format-font-size-increase', color='white'))
theme_btn.setIcon(qta.icon('mdi.brightness-6', color='white'))

# Home / Navigation
home_btn.setIcon(qta.icon('mdi.home', color='white'))
history_btn.setIcon(qta.icon('mdi.history', color='white'))
saved_btn.setIcon(qta.icon('mdi.bookmark-outline', color='#f1fa8c'))

# Verse row (your VerseRow class)
bookmark_btn.setIcon(qta.icon('mdi.bookmark-outline', color='#f1fa8c'))
bookmark_btn_filled = qta.icon('mdi.bookmark', color='gold')

note_btn.setIcon(qta.icon('mdi.note-edit-outline', color='#8be9fd'))
copy_btn.setIcon(qta.icon('mdi.content-copy', color='#8be9fd'))

# Highlights (colored dots)
yellow_icon = qta.icon('mdi.circle', color='yellow')
green_icon = qta.icon('mdi.circle', color='#50fa7b')

# Bible book icon
bible_btn.setIcon(qta.icon('fa5s.bible', color='#bd93f9'))
```

### With Multiple Colors / Stacked:

```python
# Two icons stacked
icon = qta.icon('fa5s.book', 'fa5s.bookmark',
                options=[{'color': 'white'}, {'color': 'gold', 'offset': (0.3, 0.3)}])

# Spin animation
icon = qta.icon('mdi.loading', color='white', animation=qta.Spin(btn))
```

---

## PART 3: HOW TO KNOW ICON NAMES (Most Important)

You have 4 ways, all work offline after install except websites:

### WAY 1: qta-browser - Visual Browser (BEST, OFFLINE):

```bash
qta-browser
# or
python -m qtawesome
```

- Opens window with ALL icons
- Search box: type "book", "search", "bookmark"
- Shows icon name under it, e.g., "mdi.book-open"
- Copy that name, use as `qta.icon('mdi.book-open')`
- Works 100% offline

This is the way you should use.

### WAY 2: List All Icons in Python (OFFLINE):

```python
import qtawesome as qta

# List all Material Design Icons
mdi_icons = list(qta.iconic_font('mdi').chars.keys())
print(mdi_icons[:100])  # first 100

# List all FontAwesome 5 Solid
fa5s_icons = list(qta.iconic_font('fa5s').chars.keys())
print([i for i in fa5s_icons if 'book' in i])  # search book

# Search function:
def search_icons(query):
    for prefix in ['fa', 'fa5', 'fa5s', 'mdi']:
        try:
            font = qta.iconic_font(prefix)
            matches = [f"{prefix}.{name}" for name in font.chars.keys() if query in name]
            if matches:
                print(f"\n{prefix}:")
                for m in matches[:20]:
                    print(f"  {m}")
        except:
            pass

search_icons('book')
search_icons('search')
search_icons('bookmark')
```

### WAY 3: Websites (Need internet once, screenshot or save):

- FontAwesome 4: https://fontawesome.com/v4.7.0/icons/
- FontAwesome 5: https://fontawesome.com/icons (filter Free)
- Material Design Icons: https://materialdesignicons.com/ or https://pictogrammers.com/library/mdi/
- On site, search "bible", copy name "book-open-page-variant", use as "mdi.book-open-page-variant"

### WAY 4: My Ready List for Bible App (Copy-Paste):

```
Bible / Reading:
mdi.book-open-page-variant, mdi.book-open, fa5s.bible, fa.book, mdi.book

Search:
mdi.magnify, fa.search, fa5s.search

Bookmarks:
mdi.bookmark, mdi.bookmark-outline, mdi.bookmark-check, fa.bookmark, fa5s.bookmark

Notes / Edit:
mdi.note-edit-outline, mdi.note-plus-outline, mdi.note-text, fa5s.sticky-note

Copy:
mdi.content-copy, fa.copy, fa5s.copy

Theme / Settings:
mdi.brightness-6, mdi.brightness-4, mdi.white-balance-sunny, mdi.weather-night
mdi.cog, mdi.settings, fa.cog

Font Size:
mdi.format-font-size-increase, mdi.format-font-size-decrease, mdi.format-size

Navigation:
mdi.home, mdi.arrow-left, mdi.arrow-right, mdi.history, mdi.chevron-down

Highlights:
mdi.circle, mdi.circle-outline, mdi.marker, mdi.highlight

Actions:
mdi.check, mdi.close, mdi.delete, mdi.trash-can-outline, mdi.plus, mdi.minus
```

---

## PART 4: COMMON ERRORS AND FIXES

Error: `Location './offline_packages' is ignored`
Fix: Use absolute path `/home/user/offline_packages` or `file:///C:/...` or cd into folder

Error: `No matching distribution found`
Fix: Folder empty, re-download: `pip download qtawesome -d offline_packages`

Error: `qtawesome is already installed`
Fix: You are done! Already installed, just use `import qtawesome`

Error: `ModuleNotFoundError: No module named 'qtawesome'`
Fix: Install again with `pip install *.whl` inside offline_packages

---

## PART 5: FULL WORKING EXAMPLE FOR YOUR BIBLE APP

```python
# widget.py
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QWidget
import qtawesome as qta

class TopBar(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        
        search_btn = QPushButton(" Search")
        search_btn.setIcon(qta.icon('mdi.magnify', color='white'))
        
        theme_btn = QPushButton()
        theme_btn.setIcon(qta.icon('mdi.brightness-6', color='white'))
        
        font_down = QPushButton()
        font_down.setIcon(qta.icon('mdi.format-font-size-decrease', color='white'))
        
        font_up = QPushButton()
        font_up.setIcon(qta.icon('mdi.format-font-size-increase', color='white'))
        
        layout.addWidget(search_btn)
        layout.addWidget(font_down)
        layout.addWidget(font_up)
        layout.addWidget(theme_btn)

# Run browser to find more:
# qta-browser
```

---

## SUMMARY CHECKLIST

1. Download once on internet PC: `pip download qtawesome -d offline_packages`
2. Copy folder to offline PC
3. Install: `cd offline_packages && pip install *.whl` or absolute path method
4. Use: `import qtawesome as qta; btn.setIcon(qta.icon('mdi.book'))`
5. Find names: Run `qta-browser` offline, search, copy name

You now have 1000+ icons offline forever.
