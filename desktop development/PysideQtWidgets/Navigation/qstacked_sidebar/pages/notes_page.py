from PySide6.QtWidgets import QVBoxLayout, QLabel
from PySide6.QtWidgets import QTextBrowser
from .base_page import BasePage

class NotesPage(BasePage):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24,24,24,24)
        layout.setSpacing(12)

        title = QLabel("<h1>My Markdown Notes</h1>")
        title.setObjectName("pageTitle")

        viewer = QTextBrowser()
        viewer.setObjectName("markdownViewer")
        viewer.setOpenExternalLinks(True)
        viewer.setMarkdown("""
# PySide6 Sidebar + Navigation Study

## Pattern
**Pages request, Controller decides, MainWindow executes.**

```
Sidebar/Button --(request_navigate)--> NavigationController --(page_changed)--> MainWindow.setCurrentWidget()
```

## Why Sidebar is wrapped in QWidget
- `QLayout` cannot have `background-color`
- `QWidget` with `WA_StyledBackground` can
- So each nav section is a `QWidget` container

## Collapsible Logic
```python
collapsed_width = 65
expanded_width = 220
setFixedWidth(end) # toggle between
```

Text switch: `"◉ Dashboard"` -> `"◉"` when collapsed.

## History Stack
- `_history = []` back stack
- `_future = []` forward stack
- `navigate_to()` pushes current to history, clears future
- `go_back()` pops history -> pushes current to future

### Try it
1. Go Dashboard -> Notes -> Settings
2. Press Back twice
3. Press Forward
4. Type in Notes search (if you add QLineEdit) -> go away -> come back, text stays!

> Pages are created ONCE in MainWindow, never destroyed. That's state preservation.

## To extend
- Load real `.md` files: `open("note.md").read()`
- Add `QListWidget` of notes on left of this page
- Add icons: `QIcon.fromTheme()` or `QIcon(":/icons/note.svg")`
""")

        layout.addWidget(title)
        layout.addWidget(viewer)

    def on_enter(self):
        print("[NotesPage] on_enter - load notes here")

    def on_leave(self):
        print("[NotesPage] on_leave - save notes here")
