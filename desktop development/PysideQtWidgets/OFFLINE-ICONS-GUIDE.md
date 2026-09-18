# OFFLINE ICONS FOR PYSIDE6 - Complete Guide

Since you're mostly offline, here are 4 methods that work 100% offline after one download.

---

## METHOD 1: QStyle Standard Icons (NO DOWNLOAD NEEDED)
Built into Qt, always offline. 70+ icons.

```python
from PySide6.QtWidgets import QStyle
from PySide6.QtGui import QIcon

style = QApplication.style()
icon = style.standardIcon(QStyle.SP_FileIcon)
icon = style.standardIcon(QStyle.SP_DirIcon)
icon = style.standardIcon(QStyle.SP_DialogOkButton)
icon = style.standardIcon(QStyle.SP_MessageBoxInformation)
icon = style.standardIcon(QStyle.SP_MediaPlay)

btn.setIcon(icon)
```

Full list in `qstyle_demo/qstyle_icons.py` in the pack.

Pros: Zero download, always works
Cons: Only 70 icons, system style, not colorful

---

## METHOD 2: qtawesome - BEST FOR OFFLINE (1000+ icons)
Contains FontAwesome 4, FontAwesome 5, Material Design Icons, all in font files. Works offline after install.

### On PC with internet (once):
```bash
pip download qtawesome --dest ./offline_packages
pip download qtpy --dest ./offline_packages
```

### Copy offline_packages folder to your offline PC:
```bash
pip install --no-index --find-links=./offline_packages qtawesome
```

### Usage (offline):
```python
import qtawesome as qta

# FontAwesome
btn.setIcon(qta.icon('fa.book'))
btn.setIcon(qta.icon('fa5s.bible'))
btn.setIcon(qta.icon('fa5s.search', color='#bd93f9'))

# Material Design Icons (mdi)
btn.setIcon(qta.icon('mdi.book-open-page-variant'))
btn.setIcon(qta.icon('mdi.bookmark', color='gold'))
btn.setIcon(qta.icon('mdi.magnify'))
btn.setIcon(qta.icon('mdi.brightness-6')) # theme toggle

# In your Bible app:
search_btn.setIcon(qta.icon('mdi.magnify', color='white'))
bookmark_btn.setIcon(qta.icon('mdi.bookmark-outline', color='#f1fa8c'))
```

This is what I recommend for your Bible app.

---

## METHOD 3: Download SVG Icon Packs (Manual, 100% offline)

Download once, keep forever:

1. **Material Icons** (Google): https://github.com/google/material-design-icons -> download zip, extract svg/
2. **Feather Icons**: https://feathericons.com/ -> 280+ clean icons, MIT
3. **Bootstrap Icons**: https://icons.getbootstrap.com/ -> 2000+ icons

In your pack I included sample SVGs in `material/` and `feather/` folders.

Usage:
```python
from PySide6.QtGui import QIcon

icon = QIcon("offline_icons_pack/material/book.svg")
btn.setIcon(icon)

# Or with resource file:
# 1. Create icons.qrc listing all SVGs
# 2. pyside6-rcc icons.qrc -o icons_rc.py
# 3. import icons_rc
# 4. QIcon(":/icons/material/book.svg")
```

---

## METHOD 4: Emoji / Text Icons (Zero files)
For quick prototyping, your Bible app already uses this:
```python
book_btn.setText("📚 Genesis")
bookmark_btn.setText("🔖")
```

Works offline, but not customizable.

---

## What to download for full offline setup (one time):

On internet PC:
```bash
mkdir offline_setup
cd offline_setup
pip download PySide6 qtawesome qtpy
# Also download icon zips:
# - https://github.com/google/material-design-icons/archive/refs/heads/master.zip
# - https://github.com/feathericons/feather/archive/refs/heads/master.zip
```

Copy entire offline_setup folder to offline PC via USB.

On offline PC:
```bash
pip install --no-index --find-links=. PySide6 qtawesome
```

Now you have 1000+ icons offline forever.

---

## For your Bible App specifically:

Replace emoji buttons with qtawesome:

```python
import qtawesome as qta

# Top toolbar
search_btn.setIcon(qta.icon('mdi.magnify', color='white'))
font_minus.setIcon(qta.icon('mdi.format-font-size-decrease', color='white'))
font_plus.setIcon(qta.icon('mdi.format-font-size-increase', color='white'))
theme_btn.setIcon(qta.icon('mdi.brightness-6', color='white'))

# Verse row
bookmark_btn.setIcon(qta.icon('mdi.bookmark-outline'))
note_btn.setIcon(qta.icon('mdi.note-edit-outline'))
copy_btn.setIcon(qta.icon('mdi.content-copy'))
```

All will work offline after one qtawesome install.
