# ULTIMATE SIDEBAR + QStackedWidget Navigation - Reusable Template
> Copy this structure into ANY PySide6 / PyQt6 project that needs navigation.
> Industry Standard: Controller owns history, Pages emit signals, MainWindow owns QStackedWidget.

---

## Project Structure
```
sidebar_demo/
├── main.py                 # Entry only - no logic
├── page_types.py           # Enum with ZERO dependencies (avoid circular imports)
├── navigation.py           # NavigationController - THE BRAIN (browser behavior)
├── main_window.py          # Owns QStackedWidget + Sidebar, connects signals
├── components/
│   ├── __init__.py
│   └── sidebar.py          # Ultimate reusable Sidebar widget
└── pages/
    ├── __init__.py         # Public API
    ├── base_page.py        # Base class with lifecycle + navigation contract
    ├── home_page.py
    ├── profile_page.py
    ├── settings_page.py
    └── analytics_page.py   # Example extra page
```

---

### How it works (THE LAW)
1.  `NavigationController` keeps two stacks: `history` and `future` (browser back/forward)
2.  Pages & Sidebar NEVER call `stack.setCurrentIndex()`. They emit `request_navigate`
3.  `MainWindow` is the ONLY place that calls `setCurrentWidget()`
4.  Pages are created ONCE -> state preserved when you go back (input text stays)
5.  Sidebar is a dumb view: it gets `current_page` + `can_back/can_forward` and emits `request_navigate`

---

## File: `main.py`
Entry point - only starts QApplication. No logic here.

```python
"""
main.py - Application entry point
Run: python main.py
"""
import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Ultimate Sidebar Demo")
    app.setStyle("Fusion") # Industry standard - consistent cross-platform

    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

---

## File: `page_types.py`
Central Page enum - Keep enums in their own file with ZERO dependencies
So any module can import it without circular imports

```python
"""
page_types.py - Central Page enum
Industry: Keep enums in their own file with ZERO dependencies
"""
from enum import IntEnum, auto

class Page(IntEnum):
    HOME = 0
    PROFILE = 1
    SETTINGS = 2
    ANALYTICS = 3
    # ADD NEW PAGES HERE - auto() works too if you don't care about indexes
    # REPORTS = auto()

# OPTIONAL: Metadata for Sidebar (Icons, Labels, Tooltip) - keeps UI data centralized
# This is what makes it "ultimate" - one place to control sidebar appearance
PAGE_META = {
    Page.HOME:      {"label": "Home",      "icon": "🏠", "tooltip": "Dashboard"},
    Page.PROFILE:   {"label": "Profile",   "icon": "👤", "tooltip": "User profile"},
    Page.ANALYTICS: {"label": "Analytics", "icon": "📊", "tooltip": "Analytics & Reports"},
    Page.SETTINGS:  {"label": "Settings",  "icon": "⚙️", "tooltip": "App configuration"},
}
```

---

## File: `navigation.py`
The brain. Browser-like history stack, no magic numbers. 100% reused from your code.

```python
"""
navigation.py - Navigation controller with Back/Forward history
This is the single source of truth for navigation.
"""
from PySide6.QtCore import QObject, Signal
from page_types import Page

class NavigationController(QObject):
    # Controller -> UI signals
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

---

## File: `components/sidebar.py`
ULTIMATE REUSABLE SIDEBAR - Drop this into any project.

```python
"""
components/sidebar.py - Ultimate reusable Sidebar
Industry pattern: Sidebar is a view, not a controller. It emits request_navigate.
Features:
- Auto-generates from Page enum + PAGE_META
- Active state styling
- Collapsible (icon-only mode)
- Back/Forward buttons integrated
- Never touches QStackedWidget
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QSizePolicy
from PySide6.QtCore import Signal, Qt
from page_types import Page, PAGE_META

class Sidebar(QWidget):
    request_navigate = Signal(Page)
    request_back = Signal()
    request_forward = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("Sidebar")
        self.setFixedWidth(240)
        self._collapsed = False
        self._current_page: Page | None = None
        
        # Store buttons to update active state
        self.buttons: dict[Page, QPushButton] = {}
        
        self._setup_ui()
        self._apply_stylesheet()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        # --- App Logo/Header ---
        self.lbl_logo = QLabel("⚡ QSTACKED")
        self.lbl_logo.setObjectName("Logo")
        layout.addWidget(self.lbl_logo)

        # --- Back/Forward ---
        nav_row = QFrame()
        nav_row_layout = QVBoxLayout(nav_row)
        nav_row_layout.setContentsMargins(0, 8, 0, 8)
        nav_row_layout.setSpacing(4)
        
        from PySide6.QtWidgets import QHBoxLayout
        h = QHBoxLayout()
        self.btn_back = QPushButton("←")
        self.btn_forward = QPushButton("→")
        self.btn_back.setFixedWidth(40)
        self.btn_forward.setFixedWidth(40)
        self.btn_back.clicked.connect(self.request_back.emit)
        self.btn_forward.clicked.connect(self.request_forward.emit)
        h.addWidget(self.btn_back)
        h.addWidget(self.btn_forward)
        h.addStretch()
        
        self.btn_collapse = QPushButton("⟨")
        self.btn_collapse.setFixedWidth(40)
        self.btn_collapse.clicked.connect(self.toggle_collapsed)
        h.addWidget(self.btn_collapse)
        
        nav_row_layout.addLayout(h)
        layout.addWidget(nav_row)

        # --- Separator ---
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setObjectName("Sep")
        layout.addWidget(sep)

        # --- Page Buttons (Auto-generated from enum) ---
        for page in Page:
            meta = PAGE_META.get(page, {"label": page.name.title(), "icon": "•"})
            btn = QPushButton(f" {meta['icon']}  {meta['label']}")
            btn.setCheckable(True) # For active state
            btn.setCursor(Qt.PointingHandCursor)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setMinimumHeight(42)
            btn.setProperty("page", page)
            # Lambda captures page value correctly
            btn.clicked.connect(lambda checked, p=page: self.request_navigate.emit(p))
            self.buttons[page] = btn
            layout.addWidget(btn)

        layout.addStretch()

        # --- Footer ---
        self.lbl_footer = QLabel("v1.0 • Fusion Style")
        self.lbl_footer.setObjectName("Footer")
        layout.addWidget(self.lbl_footer)

    def set_current_page(self, page: Page):
        self._current_page = page
        for p, btn in self.buttons.items():
            btn.setChecked(p == page)
            # Update text for collapsed mode
            meta = PAGE_META.get(p, {"label": p.name.title(), "icon": "•"})
            if self._collapsed:
                btn.setText(f"{meta['icon']}")
            else:
                btn.setText(f" {meta['icon']}  {meta['label']}")

    def set_history_state(self, can_back: bool, can_forward: bool):
        self.btn_back.setEnabled(can_back)
        self.btn_forward.setEnabled(can_forward)

    def toggle_collapsed(self):
        self._collapsed = not self._collapsed
        if self._collapsed:
            self.setFixedWidth(64)
            self.lbl_logo.setText("⚡")
            self.btn_collapse.setText("⟩")
        else:
            self.setFixedWidth(240)
            self.lbl_logo.setText("⚡ QSTACKED")
            self.btn_collapse.setText("⟨")
        
        # Refresh button texts
        if self._current_page is not None:
            self.set_current_page(self._current_page)

    def _apply_stylesheet(self):
        # Ultimate Sidebar QSS - looks pro in any project
        self.setStyleSheet("""
            #Sidebar {
                background-color: #1E1E2F;
                border-right: 1px solid #2D2D44;
            }
            #Sidebar #Logo {
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px 8px;
            }
            #Sidebar #Sep {
                color: #2D2D44;
            }
            #Sidebar QPushButton {
                text-align: left;
                padding: 8px 12px;
                border: none;
                border-radius: 8px;
                color: #A0A0B8;
                font-size: 14px;
            }
            #Sidebar QPushButton:hover {
                background-color: #2D2D44;
                color: white;
            }
            #Sidebar QPushButton:checked {
                background-color: #4F46E5;
                color: white;
                font-weight: bold;
            }
            #Sidebar QPushButton:disabled {
                color: #4A4A5E;
            }
            #Sidebar #Footer {
                color: #5A5A7A;
                font-size: 11px;
                padding: 8px;
            }
        """)

```

---

## File: `main_window.py`
Owns QStackedWidget + Sidebar. Industry: Controller pattern.

```python
"""
main_window.py - Main Window owns QStackedWidget + Sidebar
"""
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from navigation import NavigationController
from page_types import Page
from components.sidebar import Sidebar
from pages import HomePage, ProfilePage, SettingsPage, AnalyticsPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ultimate Sidebar - Industry Standard")
        self.resize(1100, 700)

        self.nav_controller = NavigationController()
        self.stack = QStackedWidget()
        self.sidebar = Sidebar()

        # Pre-instantiate all pages and map them to their enum identifier
        # This allows fast switching and state preservation
        self.pages_map = {
            Page.HOME: HomePage(),
            Page.PROFILE: ProfilePage(),
            Page.SETTINGS: SettingsPage(),
            Page.ANALYTICS: AnalyticsPage(),
        }

        for page_widget in self.pages_map.values():
            self.stack.addWidget(page_widget)
            page_widget.request_navigate.connect(self.nav_controller.navigate_to)

        # --- THE WIRING (This is the ultimate pattern) ---
        # 1. Sidebar -> Controller
        self.sidebar.request_navigate.connect(self.nav_controller.navigate_to)
        self.sidebar.request_back.connect(self.nav_controller.go_back)
        self.sidebar.request_forward.connect(self.nav_controller.go_forward)

        # 2. Controller -> UI (MainWindow + Sidebar)
        self.nav_controller.page_changed.connect(self.on_page_changed)
        self.nav_controller.history_changed.connect(self.on_history_changed)

        # --- Layout: Sidebar | Content ---
        central = QWidget()
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0,0,0,0)
        root_layout.setSpacing(0)
        root_layout.addWidget(self.sidebar)
        root_layout.addWidget(self.stack)
        self.setCentralWidget(central)

        # Initial navigation - don't add to history
        self.nav_controller.navigate_to(Page.HOME, add_to_history=False)

    def on_page_changed(self, page: Page):
        # Lifecycle: leave old
        if hasattr(self, '_last_page') and self._last_page in self.pages_map:
            self.pages_map[self._last_page].on_leave()

        # THE ONLY PLACE setCurrentWidget is allowed
        widget = self.pages_map[page]
        self.stack.setCurrentWidget(widget)
        widget.on_enter()

        # Tell sidebar to update active state
        self.sidebar.set_current_page(page)

        self._last_page = page
        self.statusBar().showMessage(f"Current: {page.name}")

    def on_history_changed(self, can_back: bool, can_forward: bool):
        self.sidebar.set_history_state(can_back, can_forward)
```

---

## File: `pages/__init__.py`
Public API for pages package - clean imports.

```python
from .base_page import BasePage
from .home_page import HomePage
from .profile_page import ProfilePage
from .settings_page import SettingsPage
from .analytics_page import AnalyticsPage

__all__ = ["BasePage", "HomePage", "ProfilePage", "SettingsPage", "AnalyticsPage"]
```

---

## File: `pages/base_page.py`
All pages inherit from this to enforce navigation contract.

```python
"""
pages/base_page.py - Base class for all pages
Industry: All pages inherit from this to enforce navigation contract
"""
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal
from page_types import Page

class BasePage(QWidget):
    """
    Every page MUST emit request_navigate, never touch QStackedWidget directly.
    """
    request_navigate = Signal(Page)

    def on_enter(self):
        """Called when page becomes visible. Override if needed."""
        pass

    def on_leave(self):
        """Called when page is about to be hidden. Override if needed."""
        pass
```

---

## File: `pages/home_page.py`
```python
from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton
from .base_page import BasePage
from page_types import Page

class HomePage(BasePage):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h1>Home Page</h1>"))
        layout.addWidget(QLabel("Landing page. Sidebar + buttons both work."))

        btn_profile = QPushButton("Go to Profile →")
        btn_settings = QPushButton("Go to Settings →")
        
        btn_profile.clicked.connect(lambda: self.request_navigate.emit(Page.PROFILE))
        btn_settings.clicked.connect(lambda: self.request_navigate.emit(Page.SETTINGS))

        layout.addWidget(btn_profile)
        layout.addWidget(btn_settings)
        layout.addStretch()
```

## File: `pages/profile_page.py`
```python
from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit
from .base_page import BasePage

class ProfilePage(BasePage):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h1>Profile Page</h1>"))
        
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Type something - it will stay when you go back")
        layout.addWidget(self.input_name)
        layout.addStretch()

    def on_enter(self):
        print("ProfilePage entered")
```

## File: `pages/settings_page.py`
```python
from PySide6.QtWidgets import QVBoxLayout, QLabel
from .base_page import BasePage

class SettingsPage(BasePage):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h1>Settings Page</h1>"))
        layout.addWidget(QLabel("App configuration."))
        layout.addStretch()
```

## File: `pages/analytics_page.py`
```python
from PySide6.QtWidgets import QVBoxLayout, QLabel
from .base_page import BasePage

class AnalyticsPage(BasePage):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h1>Analytics Page</h1>"))
        layout.addWidget(QLabel("Example of adding new page in 3 steps: 1) Add to enum 2) Add to PAGE_META 3) Add to pages_map"))
        layout.addStretch()
```

---

## How to Add a New Page (30 seconds)
1.  `page_types.py`: Add `REPORTS = 4` to `Page` enum + add entry to `PAGE_META`
2.  Create `pages/reports_page.py` inheriting from `BasePage`
3.  `pages/__init__.py`: import and add to `__all__`
4.  `main_window.py`: import and add to `self.pages_map`

That's it. Sidebar auto-generates, history works, active state works, collapsed mode works.

---

## Why this is Ultimate
- **Single Responsibility**: NavigationController = logic, Sidebar = view, MainWindow = wiring, Pages = content
- **Zero Magic Numbers**: Uses `Page` enum everywhere, never index 0,1,2
- **Scalable**: Works for 3 pages or 30 pages
- **State Preserved**: Pages created once
- **Testable**: You can unit test `NavigationController` without Qt UI
- **Pro UI**: QSS, active states, collapsible, browser back/forward
- **Drop-in**: Copy `page_types.py`, `navigation.py`, `components/sidebar.py`, `pages/base_page.py` to any project
