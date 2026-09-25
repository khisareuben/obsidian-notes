# Professional Image Handling in PySide6 - Full Guide (Offline Ready)

You said: "these notes are crap, why would i need pixmap" - You're right that raw QPixmap(path) is amateur. But QPixmap itself is required. Here's the professional way.

---

## PART 1: WHY YOU STILL NEED QPIXMAP

Qt display: Disk File -> QImage (editable) -> QPixmap (GPU display) -> QLabel

- QLabel can ONLY display QPixmap via setPixmap()
- QIcon stores multiple QPixmaps
- QImage = pixel editing, slow
- QPixmap = optimized for screen

```python
pixmap = QPixmap(":/images/logo.png")
label.setPixmap(pixmap)
```

---

## PART 2: WHY RAW PATH IS CRAP

Your code: QPixmap("path/to/image.png") breaks when moved, breaks on other PC, breaks after PyInstaller, no cache, no high-DPI.

---

## PART 3: THE PROFESSIONAL WAY - 4 RULES

### RULE 1: Qt Resource System (.qrc)

Project structure:
```
image_app/
  assets/images/logo.png
  assets/icons/book.svg
  resources.qrc
  resources_rc.py
  assets.py
  image_widget.py
  main.py
```

resources.qrc:
```xml
<RCC>
  <qresource prefix="/images">
    <file>assets/images/logo.png</file>
  </qresource>
  <qresource prefix="/icons">
    <file>assets/icons/book.svg</file>
  </qresource>
</RCC>
```

Compile once:
```bash
pyside6-rcc resources.qrc -o resources_rc.py
```

Use:
```python
import resources_rc
pixmap = QPixmap(":/assets/images/logo.png")
label.setPixmap(pixmap)
```

### RULE 2: Asset Manager with Cache

assets.py:
```python
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
from functools import lru_cache

class Assets:
    @staticmethod
    @lru_cache(maxsize=128)
    def pixmap(path: str, w: int = 0, h: int = 0) -> QPixmap:
        pm = QPixmap(path)
        if pm.isNull():
            pm = QPixmap(w or 100, h or 100)
            pm.fill(Qt.gray)
        if w and h:
            pm = pm.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return pm

    @staticmethod
    def icon(path: str, w: int = 24, h: int = 24) -> QIcon:
        return QIcon(Assets.pixmap(path, w, h))
```

Usage: `label.setPixmap(Assets.pixmap(":/images/logo.png", 350, 250))`

### RULE 3: Icons vs Images

| Type | Use | Example |
|------|-----|------|
| Icons UI | qtawesome or SVG | search, bookmark |
| Photos | WebP/PNG + resource | user photo |

```python
import qtawesome as qta
btn.setIcon(qta.icon('mdi.book', color='white')) # icons
label.setPixmap(Assets.pixmap(":/images/cover.webp", 350, 250)) # photos
```

### RULE 4: Proper Scaling

```python
def display_pixmap(self):
    if self.btn_fit.isChecked():
        scaled = self.current_pixmap.scaled(
            self.label_image.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.label_image.setPixmap(scaled)
    else:
        self.label_image.setPixmap(self.current_pixmap)
```

Never use setScaledContents(True) - it distorts.

---

## PART 4: YOUR CODE REWRITTEN PROFESSIONALLY

```python
import resources_rc
from assets import Assets
import qtawesome as qta

class ImageWidget(QWidget):
    def __init__(self):
        self.current_pixmap = Assets.pixmap(":/images/placeholder.webp", 300, 180)
        self.label_image.setPixmap(self.current_pixmap)
        self.btn_load.setIcon(qta.icon('mdi.folder-open', color='white'))
```

---

## PART 5: HIGH-DPI AND PYINSTALLER

```python
# main.py high-DPI
app.setAttribute(Qt.AA_UseHighDpiPixmaps)
```

With .qrc, PyInstaller needs no --add-data: `pyinstaller --onefile --windowed main.py`

---

## PART 6: QIMAGE VS QPIXMAP CHEAT SHEET

```python
# Display only:
label.setPixmap(QPixmap(":/images/logo.png"))
# Edit:
image = QImage(":/images/logo.png")
image.setPixelColor(10,10, QColor("red"))
label.setPixmap(QPixmap.fromImage(image))
# Button:
btn.setIcon(QIcon(QPixmap(":/icons/book.svg")))
# Or
btn.setIcon(qta.icon('mdi.book'))
```

---

## PART 7: CHECKLIST

1. assets/ folder with images/icons
2. resources.qrc listing them
3. pyside6-rcc resources.qrc -o resources_rc.py
4. assets.py loader with cache
5. Use :/images/... everywhere, never C:/...
6. Icons via qtawesome, photos via Assets.pixmap()

Now works offline, in exe, on any PC.
