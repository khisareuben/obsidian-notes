# PROJECT 2: NAVIGATION IN REAL PROJECTS - PySide6 6.11.2
### How Professional Teams Actually Handle Navigation

> Focus: **Navigation as logic** - routes, args, history, guards, deep linking.
> No sidebar styling - just the brain that makes any UI navigate correctly.

---

## What This Project Shows

In real products, Navigation is **separate from Sidebar**:
- Sidebar says "user clicked Projects"
- Navigation decides "go to Projects with filter=active, save history, check if unsaved changes"

This project shows exactly that - with a minimal UI so you see only navigation.

```
navigation_real_world/
├── pyproject.toml
├── src/navigation_real_world/
│   ├── app.py
│   ├── main_window.py
│   ├── config.py
│   ├── navigation/
│   │   ├── routes.py          # Route + Params (SSOT)
│   │   ├── controller.py      # Router with args + history + guards
│   │   ├── history.py         # HistoryEntry with params
│   │   └── guards.py          # e.g. UnsavedChangesGuard
│   ├── pages/
│   │   ├── base.py            # Base with on_navigated_to + on_leaving
│   │   ├── dashboard.py
│   │   ├── projects.py        # List -> navigates with project_id
│   │   ├── project_detail.py  # Receives id, tab, shows back preservation
│   │   └── settings.py
│   ├── components/
│   │   └── nav_bar.py         # Simple buttons that call controller (not sidebar)
│   └── resources/styles/theme.qss
```

---

## 1. Routes + Typed Args (SSOT)

**`src/navigation_real_world/navigation/routes.py`**
```python
from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict

class Route(Enum):
    DASHBOARD = auto()
    PROJECTS = auto()
    PROJECT_DETAIL = auto()
    SETTINGS = auto()

@dataclass(frozen=True)
class NoParams: pass

@dataclass(frozen=True)
class ProjectsParams:
    filter: str = "all"  # all, active, archived
    query: str = ""

@dataclass(frozen=True)
class ProjectDetailParams:
    project_id: int
    tab: str = "overview"  # overview, tasks, files
    # In real app: this comes from API after navigation

RouteParams = NoParams | ProjectsParams | ProjectDetailParams

@dataclass(frozen=True)
class RouteMeta:
    id: Route
    title: str
    params_type: type = NoParams
    requires_args: bool = False

ROUTES: Dict[Route, RouteMeta] = {
    Route.DASHBOARD: RouteMeta(Route.DASHBOARD, "Dashboard", NoParams),
    Route.PROJECTS: RouteMeta(Route.PROJECTS, "Projects", ProjectsParams),
    Route.PROJECT_DETAIL: RouteMeta(Route.PROJECT_DETAIL, "Project Detail", ProjectDetailParams, True),
    Route.SETTINGS: RouteMeta(Route.SETTINGS, "Settings", NoParams),
}
```

---

## 2. History with Params Preservation

**`src/navigation_real_world/navigation/history.py`**
```python
from dataclasses import dataclass
from .routes import Route, RouteParams, NoParams

@dataclass
class HistoryEntry:
    route: Route
    params: RouteParams = NoParams()

class NavigationHistory:
    def __init__(self):
        self.back: list[HistoryEntry] = []
        self.forward: list[HistoryEntry] = []

    def push(self, entry: HistoryEntry):
        self.back.append(entry)
        self.forward.clear()

    def pop_back(self, current: HistoryEntry) -> HistoryEntry | None:
        if not self.back:
            return None
        self.forward.append(current)
        return self.back.pop()

    def pop_forward(self, current: HistoryEntry) -> HistoryEntry | None:
        if not self.forward:
            return None
        self.back.append(current)
        return self.forward.pop()
```

---

## 3. Controller with Guards

**`src/navigation_real_world/navigation/guards.py`**
```python
# Real app: check unsaved changes, auth, etc.
from typing import Callable

class NavigationGuard:
    def __init__(self, check: Callable[[], bool], message: str = "Unsaved changes"):
        self.check = check
        self.message = message

    def can_navigate(self) -> bool:
        return self.check()
```

**`src/navigation_real_world/navigation/controller.py`**
```python
from typing import Dict, Callable
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget, QMessageBox
from .routes import Route, RouteParams, NoParams, ROUTES
from .history import NavigationHistory, HistoryEntry
from .guards import NavigationGuard

class NavigationController(QObject):
    route_changed = Signal(Route, object, object)  # new, params, old
    can_go_back_changed = Signal(bool)
    can_go_forward_changed = Signal(bool)

    def __init__(self):
        super().__init__()
        self._current: Route | None = None
        self._current_params: RouteParams = NoParams()
        self._history = NavigationHistory()
        self._factories: Dict[Route, Callable[[RouteParams], QWidget]] = {}
        self._pages: Dict[Route, QWidget] = {}
        self._guards: list[NavigationGuard] = []

    def register(self, route: Route, factory: Callable[[RouteParams], QWidget]):
        self._factories[route] = factory

    def add_guard(self, guard: NavigationGuard):
        self._guards.append(guard)

    def get_page(self, route: Route, params: RouteParams) -> QWidget:
        if route not in self._pages:
            page = self._factories[route](params)
            self._pages[route] = page
            if hasattr(page, "on_navigated_to"):
                page.on_navigated_to(params)
        else:
            page = self._pages[route]
            if hasattr(page, "on_navigated_to"):
                page.on_navigated_to(params)
        return self._pages[route]

    def _check_guards(self) -> bool:
        for guard in self._guards:
            if not guard.can_navigate():
                # In real app, show dialog
                # ret = QMessageBox.question(None, "Confirm", guard.message)
                # if ret != QMessageBox.Yes: return False
                print(f"[GUARD] Blocked: {guard.message}")
                return False
        return True

    def navigate_to(self, route: Route, params: RouteParams = NoParams()):
        if not self._check_guards():
            return

        expected = ROUTES[route].params_type
        if not isinstance(params, expected):
            raise TypeError(f"{route.name} expects {expected.__name__}, got {type(params).__name__}")

        if route == self._current and params == self._current_params:
            return

        if self._current is not None:
            # Call on_leaving on old page
            old_page = self._pages.get(self._current)
            if old_page and hasattr(old_page, "on_leaving"):
                if not old_page.on_leaving():
                    return
            self._history.push(HistoryEntry(self._current, self._current_params))

        old = self._current
        self._current = route
        self._current_params = params
        self.route_changed.emit(route, params, old)
        self.can_go_back_changed.emit(len(self._history.back) > 0)
        self.can_go_forward_changed.emit(len(self._history.forward) > 0)

    def go_back(self):
        if not self._history.back:
            return
        if not self._check_guards():
            return
        current = HistoryEntry(self._current, self._current_params)
        prev = self._history.pop_back(current)
        if prev:
            old = self._current
            self._current = prev.route
            self._current_params = prev.params
            self.route_changed.emit(prev.route, prev.params, old)
            self.can_go_back_changed.emit(len(self._history.back) > 0)
            self.can_go_forward_changed.emit(len(self._history.forward) > 0)

    def go_forward(self):
        if not self._history.forward:
            return
        current = HistoryEntry(self._current, self._current_params)
        nxt = self._history.pop_forward(current)
        if nxt:
            old = self._current
            self._current = nxt.route
            self._current_params = nxt.params
            self.route_changed.emit(nxt.route, nxt.params, old)
            self.can_go_back_changed.emit(len(self._history.back) > 0)
            self.can_go_forward_changed.emit(len(self._history.forward) > 0)

    @property
    def current(self) -> Route | None:
        return self._current

    @property
    def current_params(self) -> RouteParams:
        return self._current_params
```

---

## 4. Pages - How Navigation is Actually Used

**`src/navigation_real_world/pages/base.py`**
```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from ..navigation.routes import RouteParams

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
        """Called every time, with new args. Real app loads data here."""
        pass

    def on_leaving(self) -> bool:
        """Return False to block navigation (unsaved changes guard)"""
        return True

    def set_text(self, t: str):
        self._label.setText(t)
```

**`src/navigation_real_world/pages/dashboard.py`**
```python
from PySide6.QtWidgets import QPushButton
from .base import BasePage
from ..navigation.routes import Route, ProjectsParams

class DashboardPage(BasePage):
    def __init__(self, controller=None, parent=None):
        super().__init__("DASHBOARD", parent)
        self.controller = controller

        if controller:
            b1 = QPushButton("Go to Active Projects")
            b1.clicked.connect(lambda: controller.navigate_to(Route.PROJECTS, ProjectsParams(filter="active")))
            self._layout.addWidget(b1)

            b2 = QPushButton("Go to Archived")
            b2.clicked.connect(lambda: controller.navigate_to(Route.PROJECTS, ProjectsParams(filter="archived")))
            self._layout.addWidget(b2)
```

**`src/navigation_real_world/pages/projects.py`**
```python
from PySide6.QtWidgets import QListWidget, QListWidgetItem
from .base import BasePage
from ..navigation.routes import ProjectsParams, Route, ProjectDetailParams

class ProjectsPage(BasePage):
    def __init__(self, controller=None, parent=None):
        super().__init__("PROJECTS", parent)
        self.controller = controller
        self.list = QListWidget()
        self.list.itemDoubleClicked.connect(self._open)
        self._layout.addWidget(self.list)

    def _open(self, item: QListWidgetItem):
        pid = int(item.text().split("#")[1])
        if self.controller:
            self.controller.navigate_to(Route.PROJECT_DETAIL, ProjectDetailParams(project_id=pid, tab="overview"))

    def on_navigated_to(self, params: ProjectsParams):
        # This is the key: same page, different args -> reload
        self.list.clear()
        for i in range(1, 6):
            self.list.addItem(f"Project #{i} - filter={params.filter} query={params.query}")
        self._label.setText(f"PROJECTS\nfilter={params.filter}")
```

**`src/navigation_real_world/pages/project_detail.py`**
```python
from PySide6.QtWidgets import QPushButton, QHBoxLayout
from .base import BasePage
from ..navigation.routes import ProjectDetailParams

class ProjectDetailPage(BasePage):
    def __init__(self, controller=None, parent=None):
        super().__init__("DETAIL", parent)
        self.controller = controller
        self._current_id = None
        self._has_unsaved = False

        # Tab buttons = navigate with same ID, different tab (same page, new args)
        tabs = QHBoxLayout()
        for tab in ["overview", "tasks", "files"]:
            b = QPushButton(tab)
            b.clicked.connect(lambda _, t=tab: self._switch_tab(t))
            tabs.addWidget(b)
        self._layout.addLayout(tabs)

        edit = QPushButton("Make unsaved change (to test guard)")
        edit.clicked.connect(lambda: setattr(self, "_has_unsaved", True))
        self._layout.addWidget(edit)

    def _switch_tab(self, tab: str):
        if self.controller and self._current_id is not None:
            # Navigate to same route, same ID, different tab -> on_navigated_to called again
            self.controller.navigate_to(
                self.controller.current,
                ProjectDetailParams(project_id=self._current_id, tab=tab)
            )

    def on_navigated_to(self, params: ProjectDetailParams):
        if params.project_id != self._current_id:
            print(f"[API CALL] Fetch project {params.project_id}")
            self._current_id = params.project_id
            self._has_unsaved = False

        self.set_text(f"Project #{params.project_id}\nTab: {params.tab}\n\nBack button will preserve previous filter")

    def on_leaving(self) -> bool:
        if self._has_unsaved:
            print("[GUARD] Has unsaved changes - would show dialog")
            # return False to block, True to allow
            # For demo, allow but reset flag
            self._has_unsaved = False
        return True
```

**`src/navigation_real_world/pages/settings.py`**
```python
from .base import BasePage

class SettingsPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("SETTINGS", parent)
```

---

## 5. Components - Simple Nav Bar (Not Sidebar)

**`src/navigation_real_world/components/nav_bar.py`**
```python
# This is NOT a sidebar - just 4 buttons to demo navigation
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton
from ..navigation.routes import Route

class NavBar(QFrame):
    navigate_requested = Signal(Route)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(160)
        layout = QVBoxLayout(self)
        for name, route in [("Dashboard", Route.DASHBOARD), ("Projects", Route.PROJECTS), ("Settings", Route.SETTINGS)]:
            b = QPushButton(name)
            b.clicked.connect(lambda _, r=route: self.navigate_requested.emit(r))
            layout.addWidget(b)
        layout.addStretch()
```

---

## 6. Main Window - How Navigation is Wired in Real Projects

**`src/navigation_real_world/main_window.py`**
```python
from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QToolBar, QLabel
from PySide6.QtGui import QAction
from .navigation import Route, ROUTES, NavigationController, NoParams, RouteParams
from .components.nav_bar import NavBar
from .pages import DashboardPage, ProjectsPage, ProjectDetailPage, SettingsPage
from .pages.base import BasePage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Navigation Real World - How Navigation is Used")
        self.resize(1200, 700)
        self.nav = NavigationController()
        self._register()
        self._setup_ui()
        self._setup_toolbar()
        self._setup_shortcuts()
        self.nav.navigate_to(Route.DASHBOARD)

    def _register(self):
        # Factory receives params - page decides what to do with them
        self.nav.register(Route.DASHBOARD, lambda p: DashboardPage(controller=self.nav))
        self.nav.register(Route.PROJECTS, lambda p: ProjectsPage(controller=self.nav))
        self.nav.register(Route.PROJECT_DETAIL, lambda p: ProjectDetailPage(controller=self.nav))
        self.nav.register(Route.SETTINGS, lambda p: SettingsPage())

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0,0,0,0)

        self.nav_bar = NavBar()
        self.stack = QStackedWidget()

        root.addWidget(self.nav_bar)
        root.addWidget(self.stack, 1)

        self.nav_bar.navigate_requested.connect(self.nav.navigate_to)
        self.nav.route_changed.connect(self._on_route_changed)

    def _setup_toolbar(self):
        tb = QToolBar("Nav")
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, tb)
        back = tb.addAction("← Back")
        back.triggered.connect(self.nav.go_back)
        self.nav.can_go_back_changed.connect(back.setEnabled)
        back.setEnabled(False)

        fwd = tb.addAction("Forward →")
        fwd.triggered.connect(self.nav.go_forward)
        self.nav.can_go_forward_changed.connect(fwd.setEnabled)
        fwd.setEnabled(False)

        self.title_label = QLabel("Dashboard")
        tb.addWidget(self.title_label)

    def _setup_shortcuts(self):
        # Deep linking example: Ctrl+O opens project 1
        act = QAction(self)
        act.setShortcut("Ctrl+O")
        act.triggered.connect(lambda: self.nav.navigate_to(Route.PROJECT_DETAIL, __import__("navigation_real_world.navigation.routes", fromlist=["ProjectDetailParams"]).ProjectDetailParams(project_id=1)))
        self.addAction(act)

    @Slot(Route, object, object)
    def _on_route_changed(self, new_route: Route, params: RouteParams, old_route):
        page = self.nav.get_page(new_route, params)
        if self.stack.indexOf(page) == -1:
            self.stack.addWidget(page)
        self.stack.setCurrentWidget(page)
        self.title_label.setText(f"{ROUTES[new_route].title} | {params}")

    def closeEvent(self, event):
        # Guard example on window close
        super().closeEvent(event)
```

This project teaches: **How to USE navigation** - args passing, history with args preservation, guards, tab switching via same route different args, on_navigated_to vs __init__, back/forward.

---

## Run
```bash
pip install PySide6==6.11.2 -e .
python -m navigation_real_world.app
```

## Key Lessons

1. `on_navigated_to(params)` called EVERY time, not just __init__
2. Same route + different args = update, not recreate
3. History stores HistoryEntry(route, params) so back restores filter
4. Guards via on_leaving() -> return False blocks navigation
5. Controller is single source - no direct stack.setCurrentIndex()
