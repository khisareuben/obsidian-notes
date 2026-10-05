# Forever Navigation WITH Arguments - PySide6 6.11.2
### Pure Navigation + Typed Args Passing - Production Pattern

> **Update:** Now covers passing arguments between screens the industry-standard way.
> Type-safe, no globals, no singletons.

---

## What was missing? Now fixed:

Old: `navigate_to(Route.PROJECTS)` -> Page has no data
New: `navigate_to(Route.PROJECTS, ProjectParams(project_id=42, tab="files"))`

---

## 1. Project Structure (Updated)

```
forever_nav/
├── src/forever_nav/
│   ├── navigation/
│   │   ├── routes.py          # Route Enum + RouteMeta + Params
│   │   ├── controller.py      # Now holds current params per route
│   │   └── history.py         # History with params
│   ├── components/
│   │   └── sidebar_view.py    # Same - still dumb
│   ├── pages/
│   │   ├── base.py            # Base now has on_navigated_to(params)
│   │   ├── projects.py        # Example: receives args
│   │   └── project_detail.py  # Example: receives project_id
│   └── main_window.py         # Wires factories with args
```

---

## 2. Core - Routes with Typed Params

**`src/forever_nav/navigation/routes.py`**
```python
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, Optional, Any

class Route(Enum):
    HOME = auto()
    INBOX = auto()
    PROJECTS = auto()
    PROJECT_DETAIL = auto()  # New: detail page that REQUIRES args
    ANALYTICS = auto()
    SETTINGS = auto()

# ============= TYPED PARAMS - The forever way =============
# One dataclass per route that needs args. Type-safe, autocomplete forever.

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
    scroll_to: Optional[str] = None

@dataclass(frozen=True)
class InboxParams:
    message_id: Optional[int] = None
    highlight: bool = False

# Union type for all params - Python 3.10+ way
RouteParams = NoParams | ProjectsParams | ProjectDetailParams | InboxParams

@dataclass(frozen=True)
class RouteMeta:
    id: Route
    title: str
    icon: str
    tooltip: str
    # What params type this route expects (for validation)
    params_type: type = NoParams

ROUTES: Dict[Route, RouteMeta] = {
    Route.HOME: RouteMeta(Route.HOME, "Home", "⌂", "Home", NoParams),
    Route.INBOX: RouteMeta(Route.INBOX, "Inbox", "✉", "Inbox", InboxParams),
    Route.PROJECTS: RouteMeta(Route.PROJECTS, "Projects", "◧", "Projects", ProjectsParams),
    Route.PROJECT_DETAIL: RouteMeta(Route.PROJECT_DETAIL, "Project Detail", "◧", "Detail", ProjectDetailParams),
    Route.ANALYTICS: RouteMeta(Route.ANALYTICS, "Analytics", "◫", "Analytics", NoParams),
    Route.SETTINGS: RouteMeta(Route.SETTINGS, "Settings", "⚙", "Settings", NoParams),
}
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
```

**`src/forever_nav/navigation/controller.py`**
```python
from typing import Dict, Callable
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget
from .routes import Route, RouteParams, NoParams, ROUTES
from .history import NavigationHistory, HistoryEntry

class NavigationController(QObject):
    # Now emits params too
    route_changed = Signal(Route, object, Route)  # new_route, params, old_route
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
        """
        Factory signature: def factory(params: RouteParams) -> QWidget
        For pages that don't need args, ignore params.
        """
        self._factories[route] = factory

    def get_page(self, route: Route, params: RouteParams) -> QWidget:
        # For simplicity: if page exists, update it with new params via on_navigated_to
        # For detail pages, we recreate if ID changed (see projects.py example)
        if route not in self._pages:
            if route not in self._factories:
                raise ValueError(f"No factory for {route}")
            self._pages[route] = self._factories[route](params)
        else:
            # Notify existing page of new params
            page = self._pages[route]
            if hasattr(page, "on_navigated_to"):
                page.on_navigated_to(params)
        return self._pages[route]

    def navigate_to(self, route: Route, params: RouteParams = NoParams()):
        # Validate params type
        expected = ROUTES[route].params_type
        if not isinstance(params, expected):
            raise TypeError(f"Route {route} expects {expected}, got {type(params)}")

        if route == self._current and params == self._current_params:
            return

        if self._current:
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
        prev_entry = self._history.pop_back(current_entry)
        if prev_entry:
            old = self._current
            self._current = prev_entry.route
            self._current_params = prev_entry.params
            self.route_changed.emit(prev_entry.route, prev_entry.params, old)
            self.can_go_back_changed.emit(self._history.can_go_back())
            self.can_go_forward_changed.emit(self._history.can_go_forward())

    def go_forward(self):
        if not self._history.can_go_forward():
            return
        current_entry = HistoryEntry(self._current, self._current_params)
        next_entry = self._history.pop_forward(current_entry)
        if next_entry:
            old = self._current
            self._current = next_entry.route
            self._current_params = next_entry.params
            self.route_changed.emit(next_entry.route, next_entry.params, old)
            self.can_go_back_changed.emit(self._history.can_go_back())
            self.can_go_forward_changed.emit(self._history.can_go_forward())

    @property
    def current(self) -> Route | None:
        return self._current

    @property
    def current_params(self) -> RouteParams:
        return self._current_params
```

---

## 3. Pages - Now Receive Args

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
        self._layout.addWidget(self._label)

    def on_navigated_to(self, params: RouteParams):
        """
        Override this. Called EVERY time you navigate to this page,
        even if page already exists. This is where you use args.
        """
        pass

    def set_text(self, text: str):
        self._label.setText(text)
```

**`src/forever_nav/pages/projects.py`**
```python
from ..pages.base import BasePage
from ..navigation.routes import ProjectsParams

class ProjectsPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("PROJECTS", parent)

    def on_navigated_to(self, params: ProjectsParams):
        # This is where you filter list, etc.
        if isinstance(params, ProjectsParams):
            self.set_text(f"PROJECTS\n\nFilter: {params.filter}\nSearch: {params.search}\n\nThis updates without recreating page")

    def open_project(self, project_id: int, controller):
        # Example of navigating to detail WITH args
        from ..navigation.routes import Route, ProjectDetailParams
        controller.navigate_to(Route.PROJECT_DETAIL, ProjectDetailParams(project_id=project_id, tab="overview"))
```

**`src/forever_nav/pages/project_detail.py`**
```python
from ..pages.base import BasePage
from ..navigation.routes import ProjectDetailParams

class ProjectDetailPage(BasePage):
    def __init__(self, parent=None):
        super().__init__("PROJECT DETAIL", parent)
        self._current_id: int | None = None

    def on_navigated_to(self, params: ProjectDetailParams):
        if isinstance(params, ProjectDetailParams):
            # If same project but different tab, just switch tab
            # If different project, reload data
            if params.project_id != self._current_id:
                print(f"Loading project {params.project_id} from API...")
                self._current_id = params.project_id
            
            self.set_text(f"PROJECT DETAIL\n\nID: {params.project_id}\nTab: {params.tab}\nScroll: {params.scroll_to}")
```

**`src/forever_nav/pages/home.py`**
```python
from PySide6.QtWidgets import QPushButton
from ..pages.base import BasePage
from ..navigation.routes import Route, ProjectsParams, ProjectDetailParams

class HomePage(BasePage):
    def __init__(self, controller=None, parent=None):
        super().__init__("HOME", parent)
        self.controller = controller
        # Example buttons that navigate WITH args
        btn1 = QPushButton("Go to Active Projects")
        btn1.clicked.connect(lambda: controller.navigate_to(Route.PROJECTS, ProjectsParams(filter="active")) if controller else None)
        self._layout.addWidget(btn1)

        btn2 = QPushButton("Open Project #42")
        btn2.clicked.connect(lambda: controller.navigate_to(Route.PROJECT_DETAIL, ProjectDetailParams(project_id=42, tab="files")) if controller else None)
        self._layout.addWidget(btn2)
```

---

## 4. Main Window - Updated Wiring

**`src/forever_nav/main_window.py`**
```python
from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from .navigation import Route, ROUTES, NavigationController
from .navigation.routes import NoParams, RouteParams
from .components.sidebar_view import SidebarView
from .pages import HomePage, ProjectsPage, SettingsPage, BasePage
from .pages.project_detail import ProjectDetailPage
from .resources.styles.theme import load_qss

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Forever Nav + Args")
        self.resize(1100, 700)
        self.nav = NavigationController()
        self._register_pages()
        self._setup_ui()
        self.setStyleSheet(load_qss())
        self.nav.navigate_to(Route.HOME)

    def _register_pages(self):
        # Factory now receives params
        self.nav.register(Route.HOME, lambda params: HomePage(controller=self.nav))
        self.nav.register(Route.PROJECTS, lambda params: ProjectsPage())
        self.nav.register(Route.PROJECT_DETAIL, lambda params: ProjectDetailPage())
        self.nav.register(Route.INBOX, lambda params: BasePage("INBOX"))
        self.nav.register(Route.SETTINGS, lambda params: SettingsPage())

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0,0,0,0)
        root.setSpacing(0)

        self.sidebar = SidebarView()
        self.stack = QStackedWidget()

        root.addWidget(self.sidebar)
        root.addWidget(self.stack, 1)

        self.sidebar.navigate_requested.connect(lambda r: self.nav.navigate_to(r))
        self.nav.route_changed.connect(self._on_route_changed)
        self.nav.route_changed.connect(self.sidebar.sync_selection)

    @Slot(Route, object, Route)
    def _on_route_changed(self, new_route: Route, params: RouteParams, old_route: Route):
        page = self.nav.get_page(new_route, params)
        if self.stack.indexOf(page) == -1:
            self.stack.addWidget(page)
        self.stack.setCurrentWidget(page)
        # on_navigated_to already called inside get_page if page existed
        # For new page, call it too
        if hasattr(page, "on_navigated_to") and self.stack.indexOf(page) != -1 and len(self.stack) == 1 or True:
            # Ensure new pages also get params
            if page not in [self.stack.widget(i) for i in range(self.stack.count()-1)]:
                page.on_navigated_to(params)
        self.setWindowTitle(f"{ROUTES[new_route].title} - {params}")
```

---

## 5. How to Use - The 3 Patterns

### Pattern A: Simple filter args (same page, new data)
```python
# From anywhere you have controller:
from navigation.routes import Route, ProjectsParams
controller.navigate_to(Route.PROJECTS, ProjectsParams(filter="archived", search="api"))
# ProjectsPage.on_navigated_to will be called with those args
```

### Pattern B: Detail page with ID (required args)
```python
from navigation.routes import Route, ProjectDetailParams
controller.navigate_to(Route.PROJECT_DETAIL, ProjectDetailParams(project_id=123, tab="files"))
# ProjectDetailPage loads project 123
```

### Pattern C: From a list item click
```python
# In ProjectsPage:
def on_project_clicked(self, project_id):
    self.controller.navigate_to(
        Route.PROJECT_DETAIL, 
        ProjectDetailParams(project_id=project_id)
    )
```

### Pattern D: Go back with previous args preserved
```python
controller.go_back()  # Automatically restores previous params too
# If you were on Projects(filter=active) -> Detail(42) -> go_back() returns to filter=active
```

---

## 6. Why This Way? (Industry Standard)

| Bad way (breaks) | Forever way (this file) |
|---|---|
| Global variable `current_project_id` | `ProjectDetailParams(project_id=42)` typed |
| `page.project_id = 42; stack.setCurrentIndex()` | `navigate_to(Route.PROJECT_DETAIL, Params(...))` |
| Args lost on back button | History stores `HistoryEntry(route, params)` |
| `def __init__(self, project_id)` - can't reuse page | `on_navigated_to(params)` - page reused, updated |
| Dict `{"id": 42}` no autocomplete | Dataclass frozen, autocomplete + type checker |

**This is how Flutter Navigator, React Navigation, and Qt itself recommend.**

---

## 7. Add New Page With Args - Checklist

1. In `routes.py`: Add `Route.MY_PAGE` + `MyPageParams` dataclass + add to `ROUTES`
2. In `pages/my_page.py`: Create `MyPage(BasePage)` with `on_navigated_to(self, params: MyPageParams)`
3. In `main_window.py`: `self.nav.register(Route.MY_PAGE, lambda p: MyPage())`

Done. Type-safe forever.

Want me to regenerate the zip with this args version included?
