# QStackedWidget + Collapsible Sidebar - Full Project (Copy-Paste Build)

> Open this file and copy each section to recreate the entire project from scratch.
> Tested with Python 3.10+ and PySide6.

## Project Structure to Create
Create folders exactly like this:

```
qstacked_sidebar/
├── main.py
├── page_types.py
├── navigation.py
├── main_window.py
├── style.qss
├── requirements.txt
├── widgets/
│   ├── __init__.py
│   └── sidebar.py
└── pages/
    ├── __init__.py
    ├── base_page.py
    ├── home_page.py
    ├── notes_page.py
    └── settings_page.py
```

Run:
```bash
pip install -r requirements.txt
python main.py
```

---

### File: `requirements.txt`
```txt
PySide6>=6.6.0
```

### File: `page_types.py`
```python
from enum import IntEnum

class Page(IntEnum):
    HOME = 0
    NOTES = 1
    SETTINGS = 2
```

### File: `navigation.py`
```python
from PySide6.QtCore import QObject, Signal
from page_types import Page

class NavigationController(QObject):
    page_changed = Signal(Page)
    history_changed = Signal(bool, bool)

    def __init__(self):
        super().__init__()
        self._history: list[Page] = []
        self._future: list[Page] = []
        self._current: Page | None = None

    @property
    def current(self) -> Page | None:
        return self._current

    def can_go_back(self) -> bool:
        return len(self._history) > 0

    def can_go_forward(self) -> bool:
        return len(self._future) > 0

    def navigate_to(self, page: Page, add_to_history: bool = True):
        if self._current == page:
            return
        if add_to_history and self._current is not None:
            self._history.append(self._current)
            self._future.clear()
        self._current = page
        self.page_changed.emit(page)
        self.history_changed.emit(self.can_go_back(), self.can_go_forward())

    def go_back(self):
        if not self.can_go_back():
            return
        if self._current is not None:
            self._future.append(self._current)
        prev_page = self._history.pop()
        self._current = prev_page
        self.page_changed.emit(prev_page)
        self.history_changed.emit(self.can_go_back(), self.can_go_forward())

    def go_forward(self):
        if not self.can_go_forward():
            return
        if self._current is not None:
            self._history.append(self._current)
        next_page = self._future.pop()
        self._current = next_page
        self.page_changed.emit(next_page)
        self.history_changed.emit(self.can_go_back(), self.can_go_forward())
```

### File: `widgets/__init__.py`
```python
from .sidebar import SidebarWidget
__all__ = ["SidebarWidget"]
```

### File: `widgets/sidebar.py`
```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame
from PySide6.QtCore import Qt, Signal
from page_types import Page

class SidebarWidget(QWidget):
    request_navigate = Signal(Page)
    request_back = Signal()
    request_forward = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("sidebar")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._is_expanded = True
        self.collapsed_width = 65
        self.expanded_width = 220
        self.setFixedWidth(self.expanded_width)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 10, 8, 10)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.toggle_btn = QPushButton("☰  Collapse")
        self.toggle_btn.setObjectName("toggleBtn")
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        layout.addWidget(self.toggle_btn)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Plain)
        layout.addWidget(sep)

        self.btn_home = QPushButton("◉  Dashboard")
        self.btn_notes = QPushButton("⧉  My Notes")
        self.btn_settings = QPushButton("⚙  Settings")

        self.btn_home.clicked.connect(lambda: self.request_navigate.emit(Page.HOME))
        self.btn_notes.clicked.connect(lambda: self.request_navigate.emit(Page.NOTES))
        self.btn_settings.clicked.connect(lambda: self.request_navigate.emit(Page.SETTINGS))

        for btn in [self.btn_home, self.btn_notes, self.btn_settings]:
            btn.setObjectName("navBtn")
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            layout.addWidget(btn)

        layout.addStretch()

        self.btn_back = QPushButton("← Back")
        self.btn_forward = QPushButton("Forward →")
        self.btn_back.setObjectName("smallNavBtn")
        self.btn_forward.setObjectName("smallNavBtn")
        self.btn_back.clicked.connect(self.request_back.emit)
        self.btn_forward.clicked.connect(self.request_forward.emit)
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_forward.setCursor(Qt.PointingHandCursor)

        layout.addWidget(self.btn_back)
        layout.addWidget(self.btn_forward)

        self._buttons = {
            Page.HOME: self.btn_home,
            Page.NOTES: self.btn_notes,
            Page.SETTINGS: self.btn_settings
        }

    def toggle_sidebar(self):
        end = self.collapsed_width if self._is_expanded else self.expanded_width
        self._is_expanded = not self._is_expanded
        self.setFixedWidth(end)

        if self._is_expanded:
            self.toggle_btn.setText("☰  Collapse")
            self.btn_home.setText("◉  Dashboard")
            self.btn_notes.setText("⧉  My Notes")
            self.btn_settings.setText("⚙  Settings")
            self.btn_back.setText("← Back")
            self.btn_forward.setText("Forward →")
        else:
            self.toggle_btn.setText("☰")
            self.btn_home.setText("◉")
            self.btn_notes.setText("⧉")
            self.btn_settings.setText("⚙")
            self.btn_back.setText("←")
            self.btn_forward.setText("→")

    def set_active_page(self, page: Page):
        for p, btn in self._buttons.items():
            btn.setChecked(p == page)

    def set_history_state(self, can_back: bool, can_forward: bool):
        self.btn_back.setEnabled(can_back)
        self.btn_forward.setEnabled(can_forward)
```

### File: `pages/__init__.py`
```python
from .base_page import BasePage
from .home_page import HomePage
from .notes_page import NotesPage
from .settings_page import SettingsPage

__all__ = ["BasePage", "HomePage", "NotesPage", "SettingsPage"]
```

### File: `pages/base_page.py`
```python
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal
from page_types import Page

class BasePage(QWidget):
    request_navigate = Signal(Page)

    def on_enter(self):
        pass

    def on_leave(self):
        pass
```

### File: `pages/home_page.py`
```python
from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton
from .base_page import BasePage
from page_types import Page

class HomePage(BasePage):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24,24,24,24)
        layout.setSpacing(12)

        layout.addWidget(QLabel("<h1>Dashboard</h1>"))
        layout.addWidget(QLabel("This is your landing page. State is preserved when you navigate away."))

        btn_notes = QPushButton("Go to My Notes →")
        btn_settings = QPushButton("Go to Settings →")
        btn_notes.clicked.connect(lambda: self.request_navigate.emit(Page.NOTES))
        btn_settings.clicked.connect(lambda: self.request_navigate.emit(Page.SETTINGS))

        layout.addWidget(btn_notes)
        layout.addWidget(btn_settings)
        layout.addStretch()
```

### File: `pages/notes_page.py`
```python
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
'''
Sidebar/Button --(request_navigate)--> NavigationController --(page_changed)--> MainWindow.setCurrentWidget()
'''
## Why Sidebar is wrapped in QWidget
- `QLayout` cannot have `background-color`
- `QWidget` with `WA_StyledBackground` can
- So each nav section is a `QWidget` container

## COllapsible Logic
'''python
collapsed_width = 65
expanded_width = 220
setFixedWidth(end) # toggle between
'''

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

```



### File: `pages/settings_page.py`

```python
from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton
from .base_page import BasePage
from page_types import Page

class SettingsPage(BasePage):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24,24,24,24)
        layout.setSpacing(12)

        layout.addWidget(QLabel("<h1>Settings</h1>"))
        layout.addWidget(QLabel("App configuration. This page also preserves state."))

        btn_home = QPushButton("← Back to Dashboard")
        btn_notes = QPushButton("Go to My Notes")
        btn_home.clicked.connect(lambda: self.request_navigate.emit(Page.HOME))
        btn_notes.clicked.connect(lambda: self.request_navigate.emit(Page.NOTES))

        layout.addWidget(btn_home)
        layout.addWidget(btn_notes)
        layout.addStretch()
```

### File: `main_window.py`
```python
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from navigation import NavigationController
from page_types import Page
from widgets.sidebar import SidebarWidget
from pages import HomePage, NotesPage, SettingsPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sidebar + QStacked Navigation - Industry Standard")
        self.resize(1000, 600)

        self.nav_controller = NavigationController()
        self.stack = QStackedWidget()
        self.stack.setObjectName("stack")

        self.pages_map = {
            Page.HOME: HomePage(),
            Page.NOTES: NotesPage(),
            Page.SETTINGS: SettingsPage(),
        }

        for page_widget in self.pages_map.values():
            self.stack.addWidget(page_widget)
            page_widget.request_navigate.connect(self.nav_controller.navigate_to)

        self.sidebar = SidebarWidget()
        self.sidebar.request_navigate.connect(self.nav_controller.navigate_to)
        self.sidebar.request_back.connect(self.nav_controller.go_back)
        self.sidebar.request_forward.connect(self.nav_controller.go_forward)

        self.nav_controller.page_changed.connect(self.on_page_changed)
        self.nav_controller.history_changed.connect(self.sidebar.set_history_state)

        container = QWidget()
        container.setObjectName("centralWidget")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack, 1)
        self.setCentralWidget(container)

        self.nav_controller.navigate_to(Page.HOME, add_to_history=False)

    def on_page_changed(self, page: Page):
        if hasattr(self, '_last_page') and self._last_page in self.pages_map:
            self.pages_map[self._last_page].on_leave()

        widget = self.pages_map[page]
        self.stack.setCurrentWidget(widget)
        widget.on_enter()

        self.sidebar.set_active_page(page)
        self._last_page = page
        self.statusBar().showMessage(f"Current: {page.name} | History: {len(self.nav_controller._history)} Back, {len(self.nav_controller._future)} Forward")
```

### File: `main.py`
```python
import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("QStackedWidget Sidebar Demo")
    app.setStyle("Fusion")

    try:
        with open("style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        pass

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

### File: `style.qss`
```css
#centralWidget {
    background-color: #f5f5f7;
}
#sidebar {
    background-color: #1e1e1e;
    border-right: 1px solid #2a2a2a;
}
#toggleBtn {
    background-color: #2d2d2d;
    color: white;
    padding: 12px;
    border: none;
    border-radius: 8px;
    text-align: left;
    font-weight: bold;
}
#toggleBtn:hover {
    background-color: #3a3a3a;
}
#navBtn {
    background-color: transparent;
    color: #a0a0a0;
    padding: 12px 12px;
    border: none;
    border-radius: 8px;
    text-align: left;
    font-size: 14px;
}
#navBtn:hover {
    background-color: #2d2d2d;
    color: white;
}
#navBtn:checked {
    background-color: #3a3a3a;
    color: white;
    border-left: 3px solid #0078d4;
}
#smallNavBtn {
    background-color: #252525;
    color: #a0a0a0;
    padding: 8px;
    border: none;
    border-radius: 6px;
    text-align: left;
}
#smallNavBtn:hover {
    background-color: #2d2d2d;
    color: white;
}
#smallNavBtn:disabled {
    color: #555;
    background-color: transparent;
}
#separator {
    background-color: #333;
    max-height: 1px;
    margin: 6px 0px;
}
#stack {
    background-color: white;
}
QLabel {
    color: #1e1e1e;
}
QTextBrowser#markdownViewer {
    background-color: white;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 8px;
}
```

---
## How it works - Quick Summary for this file

1. `page_types.py` = contract so no circular imports
2. `BasePage.request_navigate` = pages can only ASK to navigate
3. `SidebarWidget` = collapsible (setFixedWidth toggle) + emits same signal
4. `NavigationController` = browser history (_history/_future)
5. `MainWindow` = ONLY place that calls `stack.setCurrentWidget()`

To add a new page: Add enum -> Create file in pages/ -> Register in main_window.py -> Add button in sidebar.py
