# Professional Icons in PySide6 with qtawesome - Full Detailed Guide (Offline Ready)

You have qtawesome installed. Now how to add icons professionally like real apps, not amateur emoji buttons.

---

## PART 1: WHAT IS PROFESSIONAL vs AMATEUR ICONS

Amateur:
```python
btn.setText("🔖 Bookmark")  # emoji, not recolorable, blurry, different on each OS
btn.setIcon(QIcon("C:/Users/me/Desktop/book.png"))  # breaks on other PC
```

Professional:
```python
import qtawesome as qta
btn.setIcon(qta.icon('mdi.bookmark-outline', color='#f1fa8c'))  # vector, recolorable, crisp, embedded in font
```

Professional icons are:
- Vector (SVG/font), not PNG
- Recolorable (color, hover color)
- Cached and fast
- Embedded in exe via font files
- Works offline after one install
- Same look on Windows/Linux/Mac

qtawesome gives you that.

---

## PART 2: SETUP CHECK

You already installed, but verify:

```bash
python -c "import qtawesome as qta; print(qta.__version__)"
# Should print 1.4.2 or similar, no error
```

If error:
```bash
cd offline_packages
pip install *.whl
```

---

## PART 3: BASIC USAGE

```python
import qtawesome as qta
from PySide6.QtWidgets import QPushButton

btn = QPushButton(" Search")
btn.setIcon(qta.icon('mdi.magnify', color='white'))
```

Syntax:
```python
qta.icon('prefix.name', color='hex', color_active='hover_hex', color_disabled='gray', size=24)
```

Prefixes you have:
- `fa.` = FontAwesome 4 (600 icons)
- `fa5.` = FontAwesome 5 Regular (1500 icons)
- `fa5s.` = FontAwesome 5 Solid (1500 icons) - most used
- `fa5b.` = FontAwesome 5 Brands (400 icons) - youtube, github etc
- `mdi.` = Material Design Icons (7000+ icons) - best for apps
- `ei.` = Elusive Icons
- `msc.` = VS Code icons

---

## PART 4: HOW TO FIND ICON NAMES (4 Ways)

### WAY 1: qta-browser (BEST, OFFLINE, VISUAL)

```bash
qta-browser
# or
python -m qtawesome
```

Opens window:
- Left: list of prefixes (fa, fa5s, mdi)
- Search bar: type "book", "search", "bookmark"
- Shows all matching icons
- Name under icon: `mdi.book-open`
- Click Copy button, paste as `qta.icon('mdi.book-open')`

Works 100% offline. Use this.

### WAY 2: Python Search Script (OFFLINE)

Create `find_icons.py`:

```python
import qtawesome as qta

def search(query):
    print(f"\nSearching for '{query}':")
    for prefix in ['fa', 'fa5', 'fa5s', 'fa5b', 'mdi']:
        try:
            font = qta.iconic_font(prefix)
            matches = [name for name in font.chars.keys() if query in name]
            if matches:
                print(f"  {prefix}:")
                for m in matches[:15]:
                    print(f"    {prefix}.{m}")
        except Exception as e:
            pass

search("book")
search("search")
search("bookmark")
search("bible")
search("settings")
search("home")
```

Run:
```bash
python find_icons.py
```

### WAY 3: Websites (Need internet once, screenshot)

- Material: https://materialdesignicons.com/ or https://pictogrammers.com/library/mdi/
- FontAwesome 4: https://fontawesome.com/v4.7.0/icons/
- FontAwesome 5: https://fontawesome.com/icons?d=gallery&m=free

Search "book", copy name `book-open-page-variant`, use `mdi.book-open-page-variant`

### WAY 4: Ready List for Bible App (Copy-Paste)

```
Navigation:
mdi.home, mdi.arrow-left, mdi.arrow-right, mdi.chevron-down, mdi.menu, mdi.close

Bible:
mdi.book-open-page-variant, mdi.book-open, fa5s.bible, fa.book, mdi.book

Search:
mdi.magnify, fa.search, fa5s.search

Bookmarks:
mdi.bookmark, mdi.bookmark-outline, mdi.bookmark-check, fa5s.bookmark

Notes:
mdi.note-edit-outline, mdi.note-plus-outline, mdi.note-text-outline, fa5s.sticky-note

Actions:
mdi.content-copy, mdi.delete-outline, mdi.trash-can-outline, mdi.check, mdi.plus, mdi.minus

Settings / Theme:
mdi.brightness-6, mdi.white-balance-sunny, mdi.weather-night, mdi.cog, mdi.tune

Font:
mdi.format-font-size-increase, mdi.format-font-size-decrease, mdi.format-size

Highlight:
mdi.circle, mdi.circle-outline, mdi.marker, mdi.highlight, mdi.format-color-highlight

History:
mdi.history, mdi.clock-outline, mdi.book-clock
```

---

## PART 5: PROFESSIONAL PATTERNS (How Real Apps Do It)

### Pattern 1: Central Icon Manager (Don't call qta.icon everywhere)

Create `icons.py`:

```python
# icons.py - professional icon manager
import qtawesome as qta
from functools import lru_cache

class Icons:
    @staticmethod
    @lru_cache(maxsize=256)
    def get(name: str, color='white', active=None, size=22):
        """Cached icon loader"""
        if active:
            return qta.icon(name, color=color, color_active=active)
        return qta.icon(name, color=color)

    # Predefined for your app - change colors in one place
    @staticmethod
    def search(): return Icons.get('mdi.magnify', color='white')
    @staticmethod
    def bookmark(): return Icons.get('mdi.bookmark-outline', color='#f1fa8c')
    @staticmethod
    def bookmark_filled(): return Icons.get('mdi.bookmark', color='gold')
    @staticmethod
    def note(): return Icons.get('mdi.note-edit-outline', color='#8be9fd')
    @staticmethod
    def copy(): return Icons.get('mdi.content-copy', color='#8be9fd')
    @staticmethod
    def theme(): return Icons.get('mdi.brightness-6', color='white')
    @staticmethod
    def home(): return Icons.get('mdi.home', color='white')
    @staticmethod
    def bible(): return Icons.get('fa5s.bible', color='#bd93f9')

# Usage:
# from icons import Icons
# btn.setIcon(Icons.search())
# btn.setIcon(Icons.bookmark())
```

Benefits: change color in one place, cached (fast), consistent.

### Pattern 2: Button with Icon + Text

```python
from PySide6.QtWidgets import QPushButton
from icons import Icons

btn = QPushButton(" Search")
btn.setIcon(Icons.search())
btn.setIconSize(QSize(20, 20))  # control size
```

### Pattern 3: Icon-Only Buttons (Toolbar)

```python
btn = QPushButton()
btn.setIcon(Icons.theme())
btn.setIconSize(QSize(24, 24))
btn.setFixedSize(36, 36)
btn.setFlat(True)  # no border
btn.setToolTip("Toggle theme")
```

### Pattern 4: Different Colors for States

```python
icon = qta.icon('mdi.bookmark-outline',
                color='white',           # normal
                color_active='gold',     # hover
                color_disabled='gray',   # disabled
                color_selected='orange') # selected
btn.setIcon(icon)
```

### Pattern 5: Animated Icons

```python
# Loading spinner
spin_icon = qta.icon('mdi.loading', color='white', animation=qta.Spin(btn))
btn.setIcon(spin_icon)

# Pulse
pulse_icon = qta.icon('fa5s.bell', color='red', animation=qta.Pulse(btn))
```

### Pattern 6: Stacked Icons (Badge)

```python
# Book with bookmark corner
icon = qta.icon('fa5s.book', 'fa5s.bookmark',
                options=[{'color': 'white'},
                         {'color': 'gold', 'scale_factor': 0.5, 'offset': (0.4, 0.4)}])
btn.setIcon(icon)
```

---

## PART 6: THEME SUPPORT (Dark/Light)

Your Bible app has dark theme (#121212). Icons should adapt:

```python
# icons.py with theme
class Icons:
    @staticmethod
    def for_theme(is_dark=True):
        color = 'white' if is_dark else 'black'
        return {
            'search': qta.icon('mdi.magnify', color=color),
            'bookmark': qta.icon('mdi.bookmark-outline', color='#f1fa8c' if is_dark else '#b8860b'),
        }

# In MainWindow when theme toggles:
# icons = Icons.for_theme(dark=True)
# self.search_btn.setIcon(icons['search'])
```

---

## PART 7: YOUR BIBLE APP FULL REWRITE WITH ICONS

```python
# widget.py professional with icons
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QSize
from icons import Icons
import resources_rc

class TopBar(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)

        self.btn_home = QPushButton()
        self.btn_home.setIcon(Icons.home())
        self.btn_home.setIconSize(QSize(22, 22))
        self.btn_home.setToolTip("Home")

        self.btn_search = QPushButton(" Search")
        self.btn_search.setIcon(Icons.search())
        self.btn_search.setIconSize(QSize(20, 20))

        self.btn_theme = QPushButton()
        self.btn_theme.setIcon(Icons.theme())
        self.btn_theme.setIconSize(QSize(22, 22))

        layout.addWidget(self.btn_home)
        layout.addWidget(self.btn_search)
        layout.addStretch()
        layout.addWidget(self.btn_theme)

class VerseRow(QWidget):
    def __init__(self, verse_text):
        super().__init__()
        layout = QHBoxLayout(self)

        label = QLabel(verse_text)

        self.btn_copy = QPushButton()
        self.btn_copy.setIcon(Icons.copy())
        self.btn_copy.setFlat(True)
        self.btn_copy.setToolTip("Copy verse")

        self.btn_bookmark = QPushButton()
        self.btn_bookmark.setIcon(Icons.bookmark())
        self.btn_bookmark.setFlat(True)
        self.btn_bookmark.setCheckable(True)

        self.btn_note = QPushButton()
        self.btn_note.setIcon(Icons.note())
        self.btn_note.setFlat(True)

        layout.addWidget(label)
        layout.addStretch()
        layout.addWidget(self.btn_copy)
        layout.addWidget(self.btn_bookmark)
        layout.addWidget(self.btn_note)
```

---

## PART 8: SIZE, DPI, AND PERFORMANCE

```python
# Always set icon size, don't rely on default
btn.setIconSize(QSize(20, 20))  # small toolbar
btn.setIconSize(QSize(24, 24))  # normal
btn.setIconSize(QSize(32, 32))  # large

# High-DPI
# main.py
from PySide6.QtCore import Qt
app.setAttribute(Qt.AA_UseHighDpiPixmaps)  # crisp on 4K

# Cache - Icons.get() uses lru_cache, so 100 buttons with same icon = 1 font load
```

---

## PART 9: COMMON MISTAKES

Mistake 1: Emoji instead of icon
```python
btn.setText("🔖")  # bad: different on each OS, not recolorable
btn.setIcon(Icons.bookmark())  # good
```

Mistake 2: PNG for icons
```python
QIcon("book.png")  # bad: blurry when scaled, not recolorable
qta.icon('mdi.book')  # good: vector, crisp
```

Mistake 3: No icon size
```python
btn.setIcon(icon)  # bad: tiny default
btn.setIcon(icon)
btn.setIconSize(QSize(22,22))  # good
```

Mistake 4: Calling qta.icon() 100 times
```python
for i in range(100):
    btn.setIcon(qta.icon('mdi.book'))  # bad: loads font 100 times
# good: use Icons.get() cached
btn.setIcon(Icons.book())
```

---

## PART 10: FULL CHECKLIST

1. Installed: `pip install *.whl` in offline_packages -> check `python -c "import qtawesome"`
2. Created `icons.py` with `Icons` class and `lru_cache`
3. Find names: run `qta-browser` offline, search, copy `mdi.name`
4. Use: `btn.setIcon(Icons.search())` + `btn.setIconSize(QSize(22,22))`
5. Theme: colors white for dark theme, black for light
6. Build: works in PyInstaller because fonts embedded

You now have professional vector icons offline forever.

---

## APPENDIX: QUICK TEST FILE

Create `test_icons.py`:

```python
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
import qtawesome as qta

app = QApplication(sys.argv)
w = QWidget()
layout = QVBoxLayout(w)

for name in ['mdi.book-open-page-variant', 'mdi.bookmark-outline', 'mdi.magnify', 'mdi.brightness-6', 'fa5s.bible']:
    btn = QPushButton(name)
    btn.setIcon(qta.icon(name, color='white'))
    layout.addWidget(btn)

w.setStyleSheet("background: #121212; color: white;")
w.show()
sys.exit(app.exec())
```

Run: `python test_icons.py` - if you see icons, you're professional ready.
