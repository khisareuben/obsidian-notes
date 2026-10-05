# Forever Navigation - Project Structure - PySide6 6.11.2
### Pure Navigation Only - Built to Last Forever

> **Principle:** Sidebar is dumb. Controller is smart. Routes are type-safe.
> This is the exact pattern used in VS Code, Linear, Qt Creator.

---

## 1. Project Structure

```
forever_nav/
├── pyproject.toml
├── requirements.txt
├── README.md
├── src/
│   └── forever_nav/
│       ├── __init__.py
│       ├── __main__.py
│       ├── app.py
│       ├── config.py
│       ├── main_window.py
│       ├── navigation/
│       │   ├── __init__.py
│       │   ├── routes.py           # Route Enum + RouteMeta (single source)
│       │   ├── controller.py       # NavigationController - the brain
│       │   └── history.py          # History stack (back/forward)
│       ├── components/
│       │   ├── __init__.py
│       │   ├── sidebar_view.py     # Dumb view - emits navigate_requested
│       │   └── icon_rail_view.py   # Optional 56px rail - same signal
│       ├── pages/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── home.py
│       │   ├── projects.py
│       │   └── settings.py
│       └── resources/
│           └── styles/
│               ├── theme.qss
│               └── theme.py
└── tests/
    └── test_navigation.py
```

---

## 2. Setup Files

**`pyproject.toml`**
```toml
[project]
name = "forever-nav"
version = "1.0.0"
description = "Forever navigation - PySide6 6.11.2 pure navigation pattern"
requires-python = ">=3.10"
dependencies = ["PySide6==6.11.2"]

[project.scripts]
forever-nav = "forever_nav.app:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**`requirements.txt`**
```
PySide6==6.11.2
```

**`src/forever_nav/__init__.py`**
```python
__version__ = "1.0.0"
```

**`src/forever_nav/__main__.py`**
```python
from .app import main
if __name__ == "__main__":
    main()
```

**`src/forever_nav/config.py`**
```python
SIDEBAR_WIDTH = 240
RAIL_WIDTH = 56
ORG_NAME = "YourCompany"
APP_NAME = "ForeverNav"
```

---

## 3. Navigation Core - This is the forever part

**`src/forever_nav/navigation/routes.py`**
```python
# Single source of truth for all routes. Add new page here only.
from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict

class Route(Enum):
    HOME = auto()
    INBOX = auto()
    PROJECTS = auto()
    ANALYTICS = auto()
    HISTORY = auto()
    FAVORITES = auto()
    SETTINGS = auto()

@dataclass(frozen=True)
class RouteMeta:
    id: Route
    title: str
    icon: str  # Replace with icon path later: ":/icons/home.svg"
    tooltip: str
    shortcut: str = ""  # e.g. "Ctrl+1"

ROUTES: Dict[Route, RouteMeta] = {
    Route.HOME: RouteMeta(Route.HOME, "Home", "⌂", "Home", "Ctrl+1"),
    Route.INBOX: RouteMeta(Route.INBOX, "Inbox", "✉", "Inbox", "Ctrl+2"),
    Route.PROJECTS: RouteMeta(Route.PROJECTS, "Projects", "◧", "Projects", "Ctrl+3"),
    Route.ANALYTICS: RouteMeta(Route.ANALYTICS, "Analytics", "◫", "Analytics", "Ctrl+4"),
    Route.HISTORY: RouteMeta(Route.HISTORY, "History", "↺", "History", "Ctrl+5"),
    Route.FAVORITES: RouteMeta(Route.FAVORITES, "Favorites", "☆", "Favorites", "Ctrl+6"),
    Route.SETTINGS: RouteMeta(Route.SETTINGS, "Settings", "⚙", "Settings", "Ctrl+,"),
}

PRIMARY_ROUTES = [Route.HOME, Route.INBOX, Route.PROJECTS, Route.ANALYTICS, Route.HISTORY, Route.FAVORITES]
BOTTOM_ROUTES = [Route.SETTINGS]
```

**`src/forever_nav/navigation/history.py`**
```python
from .routes import Route

class NavigationHistory:
    def __init__(self):
        self._back: list[Route] = []
        self._forward: list[Route] = []

    def push(self, current: Route):
        if current:
            self._back.append(current)
            self._forward.clear()

    def can_go_back(self) -> bool:
        return len(self._back) > 0

    def can_go_forward(self) -> bool:
        return len(self._forward) > 0

    def pop_back(self, current: Route) -> Route | None:
        if not self.can_go_back():
            return None
        self._forward.append(current)
        return self._back.pop()

    def pop_forward(self, current: Route) -> Route | None:
        if not self.can_go_forward():
            return None
        self._back.append(current)
        return self._forward.pop()
```

**`src/forever_nav/navigation/controller.py`**
```python
# THE BRAIN - Industry standard router pattern
from typing import Dict, Callable
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QWidget
from .routes import Route
from .history import NavigationHistory

class NavigationController(QObject):
    # new_route, old_route
    route_changed = Signal(Route, Route)
    can_go_back_changed = Signal(bool)
    can_go_forward_changed = Signal(bool)

    def __init__(self):
        super().__init__()
        self._current: Route | None = None
        self._history = NavigationHistory()
        self._factories: Dict[Route, Callable[[], QWidget]] = {}
        self._pages: Dict[Route, QWidget] = {}

    def register(self, route: Route, factory: Callable[[], QWidget]):
        """Register lazy factory. Page created only on first visit."""
        self._factories[route] = factory

    def get_page(self, route: Route) -> QWidget:
        if route not in self._pages:
            if route not in self._factories:
                raise ValueError(f"No factory for {route}")
            self._pages[route] = self._factories[route]()
        return self._pages[route]

    def navigate_to(self, route: Route):
        if route == self._current:
            return
        if self._current:
            self._history.push(self._current)
        
        old = self._current
        self._current = route
        self.route_changed.emit(route, old)
        self.can_go_back_changed.emit(self._history.can_go_back())
        self.can_go_forward_changed.emit(self._history.can_go_forward())

    def go_back(self):
        if not self._history.can_go_back():
            return
        prev = self._history.pop_back(self._current)
        if prev:
            old = self._current
            self._current = prev
            self.route_changed.emit(prev, old)
            self.can_go_back_changed.emit(self._history.can_go_back())
            self.can_go_forward_changed.emit(self._history.can_go_forward())

    def go_forward(self):
        if not self._history.can_go_forward():
            return
        nxt = self._history.pop_forward(self._current)
        if nxt:
            old = self._current
            self._current = nxt
            self.route_changed.emit(nxt, old)
            self.can_go_back_changed.emit(self._history.can_go_back())
            self.can_go_forward_changed.emit(self._history.can_go_forward())

    @property
    def current(self) -> Route | None:
        return self._current

    def __init_subclass__(cls):
        pass
```

**`src/forever_nav/navigation/__init__.py`**
```python
from .routes import Route, ROUTES, PRIMARY_ROUTES, BOTTOM_ROUTES
from .controller import NavigationController
from .history import NavigationHistory

__all__ = ["Route", "ROUTES", "PRIMARY_ROUTES", "BOTTOM_ROUTES", "NavigationController", "NavigationHistory"]
```

---

## 4. Components - Dumb Views Only

**`src/forever_nav/components/sidebar_view.py`**
```python
# Dumb view. Only responsibility: emit navigate_requested(Route)
from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QListWidget, QListWidgetItem
from ..navigation import Route, ROUTES, PRIMARY_ROUTES, BOTTOM_ROUTES

class SidebarView(QFrame):
    navigate_requested = Signal(Route)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(240)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 12, 8, 12)
        layout.setSpacing(4)

        self.main_list = QListWidget()
        self.main_list.setFrameShape(QFrame.Shape.NoFrame)
        self.main_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        for route in PRIMARY_ROUTES:
            meta = ROUTES[route]
            item = QListWidgetItem(f"{meta.icon}  {meta.title}")
            item.setData(Qt.ItemDataRole.UserRole, route)
            item.setToolTip(f"{meta.tooltip} {meta.shortcut}")
            self.main_list.addItem(item)

        self.main_list.currentItemChanged.connect(self._on_item_changed)
        layout.addWidget(self.main_list)
        layout.addStretch()

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setObjectName("Separator")
        layout.addWidget(sep)

        self.bottom_list = QListWidget()
        self.bottom_list.setFrameShape(QFrame.Shape.NoFrame)
        self.bottom_list.setFixedHeight(48)
        self.bottom_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        for route in BOTTOM_ROUTES:
            meta = ROUTES[route]
            item = QListWidgetItem(f"{meta.icon}  {meta.title}")
            item.setData(Qt.ItemDataRole.UserRole, route)
            self.bottom_list.addItem(item)
        self.bottom_list.currentItemChanged.connect(self._on_item_changed)
        layout.addWidget(self.bottom_list)

    def _on_item_changed(self, current: QListWidgetItem, _prev):
        if not current:
            return
        route = current.data(Qt.ItemDataRole.UserRole)
        # Deselect other list
        if current.listWidget() == self.main_list:
            self.bottom_list.clearSelection()
        else:
            self.main_list.clearSelection()
        self.navigate_requested.emit(route)

    @Slot(Route, Route)
    def sync_selection(self, new_route: Route, old_route: Route):
        # Called by MainWindow when route_changed (for back/forward sync)
        for lst in [self.main_list, self.bottom_list]:
            lst.blockSignals(True)
            lst.clearSelection()
            for i in range(lst.count()):
                it = lst.item(i)
                if it.data(Qt.ItemDataRole.UserRole) == new_route:
                    lst.setCurrentItem(it)
                    break
            lst.blockSignals(False)
```

**`src/forever_nav/components/icon_rail_view.py`**
```python
# Optional: 56px rail version. Same signal, interchangeable.
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QToolButton, QButtonGroup, QLabel
from ..navigation import Route, ROUTES, PRIMARY_ROUTES, BOTTOM_ROUTES
from ..config import RAIL_WIDTH

class IconRailView(QFrame):
    navigate_requested = Signal(Route)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("IconRail")
        self.setFixedWidth(RAIL_WIDTH)
        self._buttons: dict[Route, QToolButton] = {}
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 8, 4, 8)
        layout.setSpacing(8)

        self.group = QButtonGroup(self)
        self.group.setExclusive(True)

        for route in PRIMARY_ROUTES:
            meta = ROUTES[route]
            btn = self._make_btn(meta)
            self.group.addButton(btn)
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.addStretch()

        for route in BOTTOM_ROUTES:
            meta = ROUTES[route]
            btn = self._make_btn(meta, checkable=False)
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        avatar = QLabel("U")
        avatar.setFixedSize(32, 32)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setObjectName("Avatar")
        layout.addWidget(avatar, alignment=Qt.AlignmentFlag.AlignHCenter)

    def _make_btn(self, meta, checkable=True):
        btn = QToolButton()
        btn.setText(meta.icon)
        btn.setToolTip(f"{meta.title} {meta.shortcut}")
        btn.setCheckable(checkable)
        btn.setFixedSize(40, 40)
        btn.setObjectName("RailButton")
        btn.clicked.connect(lambda _, r=meta.id: self.navigate_requested.emit(r))
        self._buttons[meta.id] = btn
        return btn

    def sync_selection(self, new_route: Route, old_route: Route):
        for route, btn in self._buttons.items():
            if btn.isCheckable():
                btn.setChecked(route == new_route)
```

**`src/forever_nav/components/__init__.py`**
```python
from .sidebar_view import SidebarView
from .icon_rail_view import IconRailView

__all__ = ["SidebarView", "IconRailView"]
```

---

## 5. Pages

**`src/forever_nav/pages/base.py`**
```python
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class BasePage(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setObjectName("Page")
        layout = QVBoxLayout(self)
        lbl = QLabel(title)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)
```

**`src/forever_nav/pages/home.py`**
```python
from .base import BasePage

class HomePage(BasePage):
    def __init__(self, parent=None):
        super().__init__("HOME\n\nLazy loaded on first visit", parent)
```

**`src/forever_nav/pages/projects.py`**
```python
from .base import BasePage

class ProjectsPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("PROJECTS", parent)
```

**`src/forever_nav/pages/settings.py`**
```python
from .base import BasePage

class SettingsPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("SETTINGS", parent)
```

**`src/forever_nav/pages/__init__.py`**
```python
from .base import BasePage
from .home import HomePage
from .projects import ProjectsPage
from .settings import SettingsPage

__all__ = ["BasePage", "HomePage", "ProjectsPage", "SettingsPage"]
```

---

## 6. Resources

**`src/forever_nav/resources/styles/theme.py`**
```python
from pathlib import Path
def load_qss() -> str:
    return (Path(__file__).parent / "theme.qss").read_text(encoding="utf-8")
```

**`src/forever_nav/resources/styles/theme.qss`**
```css
#Sidebar, #IconRail { background: #252526; border-right: 1px solid #2d2d2d; }
QListWidget { background: transparent; outline: 0; color: #cccccc; border: none; }
QListWidget::item { padding: 8px 12px; border-radius: 6px; margin: 2px 0; }
QListWidget::item:selected { background: #37373d; color: white; }
QListWidget::item:hover { background: #2a2d2e; }
#RailButton { background: transparent; color: #9a9a9a; border-radius: 8px; font-size: 18px; }
#RailButton:hover { background: #2d2d2d; color: white; }
#RailButton:checked { background: #3a3a3a; color: white; }
#Separator { background: #2d2d2d; max-height: 1px; }
#Page { background: #1e1e1e; color: #cccccc; font-size: 18px; }
#Avatar { background: #4f46e5; color: white; border-radius: 16px; }
```

---

## 7. Main Window - The Only Place That Wires

**`src/forever_nav/main_window.py`**
```python
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QSplitter
from .config import SIDEBAR_WIDTH, RAIL_WIDTH
from .navigation import Route, ROUTES, NavigationController
from .components import SidebarView, IconRailView
from .pages import HomePage, ProjectsPage, SettingsPage, BasePage
from .resources.styles.theme import load_qss

class MainWindow(QMainWindow):
    def __init__(self, use_rail: bool = False):
        super().__init__()
        self.setWindowTitle("Forever Navigation")
        self.resize(1100, 700)
        self.nav = NavigationController()
        self._register_pages()
        self._setup_ui(use_rail)
        self._setup_shortcuts()
        self.setStyleSheet(load_qss())
        self.nav.navigate_to(Route.HOME)

    def _register_pages(self):
        # Lazy factories - page created only once, on first visit
        self.nav.register(Route.HOME, lambda: HomePage())
        self.nav.register(Route.INBOX, lambda: BasePage("INBOX"))
        self.nav.register(Route.PROJECTS, lambda: ProjectsPage())
        self.nav.register(Route.ANALYTICS, lambda: BasePage("ANALYTICS"))
        self.nav.register(Route.HISTORY, lambda: BasePage("HISTORY"))
        self.nav.register(Route.FAVORITES, lambda: BasePage("FAVORITES"))
        self.nav.register(Route.SETTINGS, lambda: SettingsPage())

    def _setup_ui(self, use_rail: bool):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0,0,0,0)
        root.setSpacing(0)

        # Swap views without changing anything else - that's why this lasts forever
        if use_rail:
            self.sidebar = IconRailView()
        else:
            self.sidebar = SidebarView()

        self.stack = QStackedWidget()

        # Splitter for future resizable
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.stack)
        self.splitter.setSizes([SIDEBAR_WIDTH, 800])

        root.addWidget(self.splitter)

        # WIRING - 3 connections only
        self.sidebar.navigate_requested.connect(self.nav.navigate_to)
        self.nav.route_changed.connect(self._on_route_changed)
        self.nav.route_changed.connect(self.sidebar.sync_selection)

    def _setup_shortcuts(self):
        # Ctrl+1..6 for primary routes
        for i, route in enumerate([Route.HOME, Route.INBOX, Route.PROJECTS, Route.ANALYTICS, Route.HISTORY, Route.FAVORITES], start=1):
            act = QAction(self)
            act.setShortcut(f"Ctrl+{i}")
            act.triggered.connect(lambda _, r=route: self.nav.navigate_to(r))
            self.addAction(act)

        # Back/Forward like browser
        back = QAction(self)
        back.setShortcut("Alt+Left")
        back.triggered.connect(self.nav.go_back)
        self.addAction(back)

        fwd = QAction(self)
        fwd.setShortcut("Alt+Right")
        fwd.triggered.connect(self.nav.go_forward)
        self.addAction(fwd)

    @Slot(Route, Route)
    def _on_route_changed(self, new_route: Route, old_route: Route):
        page = self.nav.get_page(new_route)
        if self.stack.indexOf(page) == -1:
            self.stack.addWidget(page)
        self.stack.setCurrentWidget(page)
        self.setWindowTitle(f"{ROUTES[new_route].title} - ForeverNav")

    # Make register alias for nicer API
    def _register(self, route, factory):
        self.nav.register(route, factory)
```

**`src/forever_nav/app.py`**
```python
import sys
from PySide6.QtWidgets import QApplication
from .main_window import MainWindow

def main(use_rail: bool = False):
    app = QApplication(sys.argv)
    win = MainWindow(use_rail=use_rail)
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    # Change to True to get 56px icon rail version
    main(use_rail=False)
```

---

## 8. Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run list version (240px)
python -m forever_nav

# Run rail version (56px) - change use_rail=True in app.py
python -m forever_nav.app

# Or install
pip install -e .
forever-nav
```

**`tests/test_navigation.py`**
```python
from forever_nav.navigation import Route, NavigationController

def test_navigation():
    nav = NavigationController()
    nav.register(Route.HOME, lambda: None)
    nav.navigate_to(Route.HOME)
    assert nav.current == Route.HOME

def test_history():
    nav = NavigationController()
    for r in [Route.HOME, Route.PROJECTS, Route.SETTINGS]:
        nav.register(r, lambda: None)
    nav.navigate_to(Route.HOME)
    nav.navigate_to(Route.PROJECTS)
    assert nav._history.can_go_back()
    nav.go_back()
    assert nav.current == Route.HOME
```

---

## 9. How to Extend Forever

**Add new page:**
1. In `navigation/routes.py`: add `NEW = auto()` + entry in `ROUTES`
2. In `main_window.py`: `self.nav.register(Route.NEW, lambda: NewPage())`
Done.

**Swap sidebar style:**
Change one line in `MainWindow`: `self.sidebar = IconRailView()` instead of `SidebarView()`. Same signal, no other change.

**Add breadcrumbs:**
Listen to `route_changed` and build from `nav._history._back`

**Add guard (unsaved changes):**
In `controller.py`, add `before_navigate` signal and allow veto.

This structure will never need a rewrite. Only new routes and new page factories.
