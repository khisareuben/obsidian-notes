# Forever Navigation + Args - FULL Project Structure - PySide6 6.11.2
### The Complete Version - Pure Navigation + Typed Args + Production Structure

> This is the FINAL version that combines everything:
> - Full src-layout (not flat)
> - Icon rail + Sidebar swappable
> - Typed args passing (the forever way)
> - History with args preserved
> - Lazy factories, QSplitter, shortcuts, QSS, tests

---

## 1. Full Project Structure

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
│       │   ├── routes.py              # Route + Params + Meta (SSOT)
│       │   ├── controller.py          # Controller with params
│       │   └── history.py             # HistoryEntry with params
│       ├── components/
│       │   ├── __init__.py
│       │   ├── sidebar_view.py        # 240px list view
│       │   └── icon_rail_view.py      # 56px rail view (same signal)
│       ├── pages/
│       │   ├── __init__.py
│       │   ├── base.py                # BasePage with on_navigated_to
│       │   ├── home.py                # Example: buttons that navigate with args
│       │   ├── projects.py            # Receives ProjectsParams
│       │   ├── project_detail.py      # Receives ProjectDetailParams (required)
│       │   ├── inbox.py
│       │   └── settings.py
│       └── resources/
│           └── styles/
│               ├── __init__.py
│               ├── theme.qss
│               └── theme.py
└── tests/
    └── test_navigation.py
```

---

## 2. Setup

**`pyproject.toml`**
```toml
[project]
name = "forever-nav"
version = "2.0.0"
description = "Forever navigation with args - PySide6 6.11.2"
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
__version__ = "2.0.0"
```

**`src/forever_nav/__main__.py`**
```python
from .app import main
if __name__ == "__main__":
    main()
```

**`src/forever_nav/config.py`**
```python
SIDEBAR_WIDTH = 260
EXPANDED_WIDTH = 260
RAIL_WIDTH = 56
MIN_SIDEBAR_WIDTH = 200
MAX_SIDEBAR_WIDTH = 360
ANIM_DURATION_MS = 220
HANDLE_WIDTH = 1
ORG_NAME = "YourCompany"
APP_NAME = "ForeverNav"

# QSettings Keys
KEY_COLLAPSED = "sidebar/collapsed"
KEY_WIDTH = "sidebar/width"
KEY_GEOMETRY = "window/geometry"
```

---

## 3. Navigation Core (Forever Part with Args)

**`src/forever_nav/navigation/routes.py`**
```python
from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict

class Route(Enum):
    HOME = auto()
    INBOX = auto()
    PROJECTS = auto()
    PROJECT_DETAIL = auto()
    ANALYTICS = auto()
    HISTORY = auto()
    FAVORITES = auto()
    SETTINGS = auto()

# ---------- TYPED PARAMS ----------
@dataclass(frozen=True)
class NoParams:
    pass

@dataclass(frozen=True)
class ProjectsParams:
    filter: str = "all"  # all | active | archived
    search: str = ""

@dataclass(frozen=True)
class ProjectDetailParams:
    project_id: int
    tab: str = "overview"  # overview | files | settings
    scroll_to: str | None = None

@dataclass(frozen=True)
class InboxParams:
    message_id: int | None = None
    highlight: bool = False

RouteParams = NoParams | ProjectsParams | ProjectDetailParams | InboxParams

@dataclass(frozen=True)
class RouteMeta:
    id: Route
    title: str
    icon: str
    tooltip: str
    shortcut: str = ""
    params_type: type = NoParams
    requires_args: bool = False

ROUTES: Dict[Route, RouteMeta] = {
    Route.HOME: RouteMeta(Route.HOME, "Home", "⌂", "Home", "Ctrl+1", NoParams),
    Route.INBOX: RouteMeta(Route.INBOX, "Inbox", "✉", "Inbox", "Ctrl+2", InboxParams),
    Route.PROJECTS: RouteMeta(Route.PROJECTS, "Projects", "◧", "Projects", "Ctrl+3", ProjectsParams),
    Route.PROJECT_DETAIL: RouteMeta(Route.PROJECT_DETAIL, "Project Detail", "◧", "Detail", "", ProjectDetailParams, True),
    Route.ANALYTICS: RouteMeta(Route.ANALYTICS, "Analytics", "◫", "Analytics", "Ctrl+4", NoParams),
    Route.HISTORY: RouteMeta(Route.HISTORY, "History", "↺", "History", "Ctrl+5", NoParams),
    Route.FAVORITES: RouteMeta(Route.FAVORITES, "Favorites", "☆", "Favorites", "Ctrl+6", NoParams),
    Route.SETTINGS: RouteMeta(Route.SETTINGS, "Settings", "⚙", "Settings", "Ctrl+,", NoParams),
}

PRIMARY_ROUTES = [Route.HOME, Route.INBOX, Route.PROJECTS, Route.ANALYTICS, Route.HISTORY, Route.FAVORITES]
BOTTOM_ROUTES = [Route.SETTINGS]
# Detail routes are not shown in sidebar, only via navigation
```

**`src/forever_nav/navigation/history.py`**
```python
from dataclasses import dataclass
from .routes import Route, RouteParams, NoParams

@dataclass
class HistoryEntry:
    route: Route
    params: RouteParams = NoParams()

class NavigationHistory:
    def __init__(self):
        self._back: list[HistoryEntry] = []
        self._forward: list[HistoryEntry] = []

    def push(self, entry: HistoryEntry):
        self._back.append(entry)
        self._forward.clear()

    def can_go_back(self) -> bool:
        return len(self._back) > 0

    def can_go_forward(self) -> bool:
        return len(self._forward) > 0

    def pop_back(self, current: HistoryEntry) -> HistoryEntry | None:
        if not self.can_go_back():
            return None
        self._forward.append(current)
        return self._back.pop()

    def pop_forward(self, current: HistoryEntry) -> HistoryEntry | None:
        if not self.can_go_forward():
            return None
        self._back.append(current)
        return self._forward.pop()

    def clear(self):
        self._back.clear()
        self._forward.clear()
```

**`src/forever_nav/navigation/controller.py`**
```python
from typing import Dict, Callable
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget
from .routes import Route, RouteParams, NoParams, ROUTES
from .history import NavigationHistory, HistoryEntry

class NavigationController(QObject):
    # new_route, params, old_route
    route_changed = Signal(Route, object, object)
    can_go_back_changed = Signal(bool)
    can_go_forward_changed = Signal(bool)

    def __init__(self):
        super().__init__()
        self._current: Route | None = None
        self._current_params: RouteParams = NoParams()
        self._history = NavigationHistory()
        self._factories: Dict[Route, Callable[[RouteParams], QWidget]] = {}
        self._pages: Dict[Route, QWidget] = {}

    def register(self, route: Route, factory: Callable[[RouteParams], QWidget]):
        self._factories[route] = factory

    def get_page(self, route: Route, params: RouteParams) -> QWidget:
        if route not in self._pages:
            if route not in self._factories:
                raise ValueError(f"No factory for {route}")
            page = self._factories[route](params)
            self._pages[route] = page
            # Call on_navigated_to for first time too
            if hasattr(page, "on_navigated_to"):
                page.on_navigated_to(params)
        else:
            page = self._pages[route]
            if hasattr(page, "on_navigated_to"):
                page.on_navigated_to(params)
        return self._pages[route]

    def navigate_to(self, route: Route, params: RouteParams = NoParams()):
        expected = ROUTES[route].params_type
        if not isinstance(params, expected):
            raise TypeError(f"Route {route.name} expects {expected.__name__}, got {type(params).__name__}")

        if ROUTES[route].requires_args and isinstance(params, NoParams):
            raise ValueError(f"Route {route.name} requires args: {expected.__name__}")

        if route == self._current and params == self._current_params:
            return

        if self._current is not None:
            self._history.push(HistoryEntry(self._current, self._current_params))

        old = self._current
        self._current = route
        self._current_params = params
        self.route_changed.emit(route, params, old)
        self.can_go_back_changed.emit(self._history.can_go_back())
        self.can_go_forward_changed.emit(self._history.can_go_forward())

    def go_back(self):
        if not self._history.can_go_back():
            return
        current_entry = HistoryEntry(self._current, self._current_params)
        prev = self._history.pop_back(current_entry)
        if prev:
            old = self._current
            self._current = prev.route
            self._current_params = prev.params
            self.route_changed.emit(prev.route, prev.params, old)
            self.can_go_back_changed.emit(self._history.can_go_back())
            self.can_go_forward_changed.emit(self._history.can_go_forward())

    def go_forward(self):
        if not self._history.can_go_forward():
            return
        current_entry = HistoryEntry(self._current, self._current_params)
        nxt = self._history.pop_forward(current_entry)
        if nxt:
            old = self._current
            self._current = nxt.route
            self._current_params = nxt.params
            self.route_changed.emit(nxt.route, nxt.params, old)
            self.can_go_back_changed.emit(self._history.can_go_back())
            self.can_go_forward_changed.emit(self._history.can_go_forward())

    @property
    def current(self) -> Route | None:
        return self._current

    @property
    def current_params(self) -> RouteParams:
        return self._current_params
```

**`src/forever_nav/navigation/__init__.py`**
```python
from .routes import Route, ROUTES, PRIMARY_ROUTES, BOTTOM_ROUTES, NoParams, ProjectsParams, ProjectDetailParams, InboxParams, RouteParams
from .controller import NavigationController
from .history import NavigationHistory, HistoryEntry

__all__ = ["Route", "ROUTES", "PRIMARY_ROUTES", "BOTTOM_ROUTES", "NoParams", "ProjectsParams", "ProjectDetailParams", "InboxParams", "RouteParams", "NavigationController", "NavigationHistory", "HistoryEntry"]
```

---

## 4. Components (Dumb Views)

**`src/forever_nav/components/sidebar_view.py`**
```python
from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QListWidget, QListWidgetItem, QLabel
from ..navigation import Route, ROUTES, PRIMARY_ROUTES, BOTTOM_ROUTES

class SidebarView(QFrame):
    navigate_requested = Signal(Route)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(260)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 12, 8, 12)
        layout.setSpacing(4)

        self.main_list = QListWidget()
        self.main_list.setFrameShape(QFrame.Shape.NoFrame)
        self.main_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.main_list.setObjectName("NavList")

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
        self.bottom_list.setObjectName("NavList")
        for route in BOTTOM_ROUTES:
            meta = ROUTES[route]
            item = QListWidgetItem(f"{meta.icon}  {meta.title}")
            item.setData(Qt.ItemDataRole.UserRole, route)
            self.bottom_list.addItem(item)
        self.bottom_list.currentItemChanged.connect(self._on_item_changed)
        layout.addWidget(self.bottom_list)

    def _on_item_changed(self, current, _prev):
        if not current:
            return
        route = current.data(Qt.ItemDataRole.UserRole)
        if current.listWidget() == self.main_list:
            self.bottom_list.clearSelection()
        else:
            self.main_list.clearSelection()
        self.navigate_requested.emit(route)

    @Slot(Route, object, object)
    def sync_selection(self, new_route: Route, params, old_route):
        # Don't highlight detail routes in sidebar - keep parent highlighted
        display_route = new_route
        if new_route == Route.PROJECT_DETAIL:
            display_route = Route.PROJECTS

        for lst in [self.main_list, self.bottom_list]:
            lst.blockSignals(True)
            lst.clearSelection()
            for i in range(lst.count()):
                it = lst.item(i)
                if it.data(Qt.ItemDataRole.UserRole) == display_route:
                    lst.setCurrentItem(it)
                    break
            lst.blockSignals(False)
```

**`src/forever_nav/components/icon_rail_view.py`**
```python
from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QToolButton, QButtonGroup, QLabel
from ..config import RAIL_WIDTH
from ..navigation import Route, ROUTES, PRIMARY_ROUTES, BOTTOM_ROUTES

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

    @Slot(Route, object, object)
    def sync_selection(self, new_route: Route, params, old_route):
        display_route = new_route
        if new_route == Route.PROJECT_DETAIL:
            display_route = Route.PROJECTS
        for route, btn in self._buttons.items():
            if btn.isCheckable():
                btn.setChecked(route == display_route)
```

**`src/forever_nav/components/__init__.py`**
```python
from .sidebar_view import SidebarView
from .icon_rail_view import IconRailView
__all__ = ["SidebarView", "IconRailView"]
```

---

## 5. Pages (All Receive Args)

**`src/forever_nav/pages/base.py`**
```python
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from ..navigation.routes import RouteParams, NoParams

class BasePage(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setObjectName("Page")
        self._layout = QVBoxLayout(self)
        self._label = QLabel(title)
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setWordWrap(True)
        self._layout.addWidget(self._label)

    def on_navigated_to(self, params: RouteParams):
        """Override in subclass. Called every time page is visited."""
        pass

    def set_text(self, text: str):
        self._label.setText(text)
```

**`src/forever_nav/pages/home.py`**
```python
from PySide6.QtWidgets import QPushButton
from .base import BasePage
from ..navigation.routes import Route, ProjectsParams, ProjectDetailParams, InboxParams

class HomePage(BasePage):
    def __init__(self, controller=None, parent=None):
        super().__init__("HOME", parent)
        self.controller = controller

        if controller:
            btn1 = QPushButton("Go to Active Projects (with args)")
            btn1.clicked.connect(lambda: controller.navigate_to(Route.PROJECTS, ProjectsParams(filter="active", search="")))
            self._layout.addWidget(btn1)

            btn2 = QPushButton("Open Project #42 → Files tab (with args)")
            btn2.clicked.connect(lambda: controller.navigate_to(Route.PROJECT_DETAIL, ProjectDetailParams(project_id=42, tab="files")))
            self._layout.addWidget(btn2)

            btn3 = QPushButton("Open Inbox Message #10")
            btn3.clicked.connect(lambda: controller.navigate_to(Route.INBOX, InboxParams(message_id=10, highlight=True)))
            self._layout.addWidget(btn3)
```

**`src/forever_nav/pages/projects.py`**
```python
from PySide6.QtWidgets import QPushButton, QListWidget, QListWidgetItem
from .base import BasePage
from ..navigation.routes import ProjectsParams, Route, ProjectDetailParams

class ProjectsPage(BasePage):
    def __init__(self, controller=None, parent=None):
        super().__init__("PROJECTS", parent)
        self.controller = controller
        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self._open_project)
        self._layout.addWidget(self.list_widget)
        self._load_projects("all")

    def _load_projects(self, filter_name: str):
        self.list_widget.clear()
        for i in range(1, 6):
            self.list_widget.addItem(QListWidgetItem(f"Project {i} - {filter_name}"))

    def _open_project(self, item):
        # Extract ID from text
        pid = int(item.text().split()[1])
        if self.controller:
            self.controller.navigate_to(Route.PROJECT_DETAIL, ProjectDetailParams(project_id=pid, tab="overview"))

    def on_navigated_to(self, params: ProjectsParams):
        if isinstance(params, ProjectsParams):
            self._load_projects(params.filter)
            self._label.setText(f"PROJECTS\n\nFilter: {params.filter}\nSearch: '{params.search}'\n\nDouble-click to open detail")
```

**`src/forever_nav/pages/project_detail.py`**
```python
from PySide6.QtWidgets import QPushButton, QHBoxLayout
from .base import BasePage
from ..navigation.routes import ProjectDetailParams

class ProjectDetailPage(BasePage):
    def __init__(self, controller=None, parent=None):
        super().__init__("PROJECT DETAIL", parent)
        self.controller = controller
        self._current_id: int | None = None

        # Tab buttons that navigate with different args (same page, new tab)
        tab_layout = QHBoxLayout()
        for tab in ["overview", "files", "settings"]:
            btn = QPushButton(tab)
            btn.clicked.connect(lambda _, t=tab: self._switch_tab(t))
            tab_layout.addWidget(btn)
        self._layout.addLayout(tab_layout)

    def _switch_tab(self, tab: str):
        if self.controller and self._current_id is not None:
            self.controller.navigate_to(
                self.controller.current,
                ProjectDetailParams(project_id=self._current_id, tab=tab)
            )

    def on_navigated_to(self, params: ProjectDetailParams):
        if not isinstance(params, ProjectDetailParams):
            return

        if params.project_id != self._current_id:
            print(f"[API] Loading project {params.project_id}...")
            self._current_id = params.project_id

        self.set_text(
            f"PROJECT DETAIL\n\n"
            f"ID: {params.project_id}\n"
            f"Tab: {params.tab}\n"
            f"ScrollTo: {params.scroll_to}\n\n"
            f"Page was NOT recreated, only updated via on_navigated_to()"
        )
```

**`src/forever_nav/pages/inbox.py`**
```python
from .base import BasePage
from ..navigation.routes import InboxParams

class InboxPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("INBOX", parent)

    def on_navigated_to(self, params: InboxParams):
        if isinstance(params, InboxParams) and params.message_id:
            self.set_text(f"INBOX\n\nHighlighted message: {params.message_id}\nHighlight: {params.highlight}")
        else:
            self.set_text("INBOX\n\nAll messages")
```

**`src/forever_nav/pages/settings.py`**
```python
from .base import BasePage
from ..navigation.routes import NoParams

class SettingsPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("SETTINGS", parent)

    def on_navigated_to(self, params: NoParams):
        self.set_text("SETTINGS\n\nNo params needed")
```

**`src/forever_nav/pages/__init__.py`**
```python
from .base import BasePage
from .home import HomePage
from .projects import ProjectsPage
from .project_detail import ProjectDetailPage
from .inbox import InboxPage
from .settings import SettingsPage

__all__ = ["BasePage", "HomePage", "ProjectsPage", "ProjectDetailPage", "InboxPage", "SettingsPage"]
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
QListWidget#NavList { background: transparent; outline: 0; color: #cccccc; border: none; }
QListWidget#NavList::item { padding: 8px 12px; border-radius: 6px; margin: 2px 4px; }
QListWidget#NavList::item:selected { background: #37373d; color: white; }
QListWidget#NavList::item:hover { background: #2a2d2e; }
#RailButton { background: transparent; color: #9a9a9a; border-radius: 8px; font-size: 18px; }
#RailButton:hover { background: #2d2d2d; color: white; }
#RailButton:checked { background: #3a3a3a; color: white; }
#Separator { background: #2d2d2d; max-height: 1px; }
#Page { background: #1e1e1e; color: #cccccc; font-size: 16px; }
#Avatar { background: #4f46e5; color: white; border-radius: 16px; font-weight: bold; }
QPushButton { background: #3a3a3a; color: white; padding: 8px; border-radius: 6px; border: none; }
QPushButton:hover { background: #4a4a4a; }
```

**`src/forever_nav/resources/styles/__init__.py`**
```python
from .theme import load_qss
__all__ = ["load_qss"]
```

**`src/forever_nav/resources/__init__.py`** empty

---

## 7. Main Window - Wiring with Args

**`src/forever_nav/main_window.py`**
```python
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QSplitter, QToolBar, QLabel
from .config import SIDEBAR_WIDTH
from .navigation import Route, ROUTES, NavigationController, NoParams, RouteParams
from .components import SidebarView, IconRailView
from .pages import HomePage, ProjectsPage, ProjectDetailPage, InboxPage, SettingsPage, BasePage
from .resources.styles.theme import load_qss

class MainWindow(QMainWindow):
    def __init__(self, use_rail: bool = False):
        super().__init__()
        self.setWindowTitle("Forever Nav + Args - Full")
        self.resize(1280, 800)
        self.nav = NavigationController()
        self._register_pages()
        self._setup_ui(use_rail)
        self._setup_shortcuts()
        self._setup_toolbar()
        self.setStyleSheet(load_qss())
        self.nav.navigate_to(Route.HOME)

    def _register_pages(self):
        # Factories receive params and can pass controller
        self.nav.register(Route.HOME, lambda params: HomePage(controller=self.nav))
        self.nav.register(Route.INBOX, lambda params: InboxPage())
        self.nav.register(Route.PROJECTS, lambda params: ProjectsPage(controller=self.nav))
        self.nav.register(Route.PROJECT_DETAIL, lambda params: ProjectDetailPage(controller=self.nav))
        self.nav.register(Route.ANALYTICS, lambda params: BasePage("ANALYTICS"))
        self.nav.register(Route.HISTORY, lambda params: BasePage("HISTORY"))
        self.nav.register(Route.FAVORITES, lambda params: BasePage("FAVORITES"))
        self.nav.register(Route.SETTINGS, lambda params: SettingsPage())

    def _setup_ui(self, use_rail: bool):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0,0,0,0)
        root.setSpacing(0)

        self.sidebar = IconRailView() if use_rail else SidebarView()
        self.stack = QStackedWidget()
        self.stack.setObjectName("ContentStack")

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setHandleWidth(1)
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.stack)
        self.splitter.setSizes([SIDEBAR_WIDTH, 900])

        root.addWidget(self.splitter)

        # Only 3 connections - forever
        self.sidebar.navigate_requested.connect(self.nav.navigate_to)
        self.nav.route_changed.connect(self._on_route_changed)
        self.nav.route_changed.connect(self.sidebar.sync_selection)

    def _setup_toolbar(self):
        toolbar = QToolBar("Navigation")
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)
        
        back_action = toolbar.addAction("← Back")
        back_action.triggered.connect(self.nav.go_back)
        self.nav.can_go_back_changed.connect(back_action.setEnabled)
        back_action.setEnabled(False)

        fwd_action = toolbar.addAction("Forward →")
        fwd_action.triggered.connect(self.nav.go_forward)
        self.nav.can_go_forward_changed.connect(fwd_action.setEnabled)
        fwd_action.setEnabled(False)

        self.title_label = QLabel("Home")
        toolbar.addWidget(self.title_label)

    def _setup_shortcuts(self):
        for i, route in enumerate([Route.HOME, Route.INBOX, Route.PROJECTS, Route.ANALYTICS, Route.HISTORY, Route.FAVORITES], start=1):
            act = QAction(self)
            act.setShortcut(f"Ctrl+{i}")
            act.triggered.connect(lambda _, r=route: self.nav.navigate_to(r))
            self.addAction(act)

        back = QAction(self)
        back.setShortcut("Alt+Left")
        back.triggered.connect(self.nav.go_back)
        self.addAction(back)

        fwd = QAction(self)
        fwd.setShortcut("Alt+Right")
        fwd.triggered.connect(self.nav.go_forward)
        self.addAction(fwd)

    @Slot(Route, object, object)
    def _on_route_changed(self, new_route: Route, params: RouteParams, old_route):
        page = self.nav.get_page(new_route, params)
        if self.stack.indexOf(page) == -1:
            self.stack.addWidget(page)
        self.stack.setCurrentWidget(page)
        self.title_label.setText(f"{ROUTES[new_route].title} | {params}")
        self.setWindowTitle(f"{ROUTES[new_route].title} - {params}")

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
    main(use_rail=False)  # True for 56px rail
```

---

## 8. Tests

**`tests/test_navigation.py`**
```python
from forever_nav.navigation import Route, NavigationController, ProjectsParams, ProjectDetailParams, NoParams

def test_navigate_with_args():
    nav = NavigationController()
    nav.register(Route.PROJECTS, lambda p: None)
    nav.register(Route.PROJECT_DETAIL, lambda p: None)
    
    nav.navigate_to(Route.PROJECTS, ProjectsParams(filter="active"))
    assert nav.current == Route.PROJECTS
    assert nav.current_params.filter == "active"

    nav.navigate_to(Route.PROJECT_DETAIL, ProjectDetailParams(project_id=42))
    assert nav.current == Route.PROJECT_DETAIL
    assert nav.current_params.project_id == 42

    nav.go_back()
    assert nav.current == Route.PROJECTS
    assert nav.current_params.filter == "active"  # Args preserved!

def test_requires_args_validation():
    nav = NavigationController()
    nav.register(Route.PROJECT_DETAIL, lambda p: None)
    try:
        nav.navigate_to(Route.PROJECT_DETAIL)  # Should fail - requires args
        assert False, "Should have raised"
    except ValueError:
        pass

def test_type_safety():
    nav = NavigationController()
    nav.register(Route.PROJECTS, lambda p: None)
    try:
        nav.navigate_to(Route.PROJECTS, ProjectDetailParams(project_id=1))  # Wrong type
        assert False
    except TypeError:
        pass
```

---

## 9. Run

```bash
pip install -e .
python -m forever_nav

# Rail version: change use_rail=True in app.py
```

## 10. How to Use Args Forever

```python
# 1. Filter list
controller.navigate_to(Route.PROJECTS, ProjectsParams(filter="archived", search="api"))

# 2. Open detail with ID
controller.navigate_to(Route.PROJECT_DETAIL, ProjectDetailParams(project_id=123, tab="files"))

# 3. Back preserves args automatically
controller.go_back()  # Returns to previous filter/search

# 4. In page, handle args
def on_navigated_to(self, params: ProjectDetailParams):
    if params.project_id != self._current_id:
        self.load_from_api(params.project_id)
```

This version is now **full structure + args + swappable rail/sidebar + history with args + tests + toolbar**. Nothing cut.

Want me to generate the actual zip so you can download and run it?
