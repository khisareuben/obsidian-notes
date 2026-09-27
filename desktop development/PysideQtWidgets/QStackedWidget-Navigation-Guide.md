# QStackedWidget Navigation - Industry Standard PySide6

Complete production-ready template for back/forth navigation with QStackedWidget.

## Project Structure
```
qstacked_demo/
├── main.py                 # Entry only
├── navigation.py           # Page enum + NavigationController (brain)
├── main_window.py          # Owns QStackedWidget, connects signals
└── pages/
    ├── __init__.py         # Public API
    ├── base_page.py        # Base class with lifecycle
    ├── home_page.py
    ├── profile_page.py
    └── settings_page.py
```

### How it works
1. `NavigationController` keeps two stacks: `history` and `future` (browser behavior)
2. Pages NEVER call `stack.setCurrentIndex()`. They emit `request_navigate` signal
3. `MainWindow` listens to controller and does `setCurrentWidget()`
4. Pages are created ONCE -> state preserved when you go back

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
    app.setApplicationName("QStackedWidget Demo")
    app.setStyle("Fusion") # Industry standard - consistent cross-platform

    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

`page_types.py`
```python
"""
page_types.py - Central Page enum
Industry: Keep enums in their own file with ZERO dependencies
So any module can import it without circular imports
"""
from enum import IntEnum

class Page(IntEnum):
    HOME = 0
    PROFILE = 1
    SETTINGS = 2
```

## File: `navigation.py`
The brain. Browser-like history stack, no magic numbers.

```python
"""
navigation.py - Navigation controller with Back/Forward history
"""
# Import QObject (base class for Qt objects with signals) and Signal (for emitting events) from PySide6
from PySide6.QtCore import QObject, Signal
# Import the Page type definition from your page_types module
from page_types import Page

# Define NavigationController class that inherits from QObject so it can use Qt Signals
class NavigationController(QObject):
    # Define a signal that will be emitted when the current page changes, carrying a Page object
    page_changed = Signal(Page)
    # Define a signal that will be emitted when history state changes, carrying two booleans (can_go_back, can_go_forward)
    history_changed = Signal(bool, bool)

    # Constructor / initializer for the NavigationController
    def __init__(self):
        # Call the parent QObject's initializer
        super().__init__()
        # Initialize empty list to store past pages (back history), with type hint list[Page]
        self._history: list[Page] = []
        # Initialize empty list to store future pages (forward history) after going back
        self._future: list[Page] = []
        # Initialize current page as None, type hint says it can be Page or None
        self._current: Page | None = None

    # Decorator to make 'current' act like a read-only property
    @property
    # Method to get the current page
    def current(self) -> Page | None:
        # Return the private _current variable
        return self._current

    # Method to check if we can go back, returns bool
    def can_go_back(self) -> bool:
        # Return True if _history list has at least one item, otherwise False
        return len(self._history) > 0

    # Method to check if we can go forward, returns bool
    def can_go_forward(self) -> bool:
        # Return True if _future list has at least one item, otherwise False
        return len(self._future) > 0

    # Method to navigate to a new page, with optional flag to add to history (defaults to True)
    def navigate_to(self, page: Page, add_to_history: bool = True):
        # If the requested page is already the current page, do nothing and exit
        if self._current == page:
            return
        # If we should add to history AND there is a current page set
        if add_to_history and self._current is not None:
            # Add the current page to the back history list
            self._history.append(self._current)
            # Clear the forward history because we branched to a new page
            self._future.clear()
        # Set the new page as the current page
        self._current = page
        # Emit the page_changed signal with the new page so UI can update
        self.page_changed.emit(page)
        # Emit history_changed signal with updated back/forward availability
        self.history_changed.emit(self.can_go_back(), self.can_go_forward())

    # Method to go back to the previous page
    def go_back(self):
        # If there is no back history, do nothing and exit
        if not self.can_go_back():
            return
        # If there is a current page, save it to the future (forward) list
        if self._current is not None:
            self._future.append(self._current)
        # Remove and get the last page from history (most recent previous page)
        prev_page = self._history.pop()
        # Set that previous page as the new current page
        self._current = prev_page
        # Emit signal to tell UI the page has changed to the previous page
        self.page_changed.emit(prev_page)
        # Emit signal to update back/forward buttons state
        self.history_changed.emit(self.can_go_back(), self.can_go_forward())

    # Method to go forward to the next page (after having gone back)
    def go_forward(self):
        # If there is no forward history, do nothing and exit
        if not self.can_go_forward():
            return
        # If there is a current page, save it to the back history list
        if self._current is not None:
            self._history.append(self._current)
        # Remove and get the last page from the future list (next page to go forward to)
        next_page = self._future.pop()
        # Set that next page as the new current page
        self._current = next_page
        # Emit signal to tell UI the page has changed to the next page
        self.page_changed.emit(next_page)
        # Emit signal to update back/forward buttons state
        self.history_changed.emit(self.can_go_back(), self.can_go_forward())
```

## File: `main_window.py`
Owns QStackedWidget. Industry: Controller pattern.

```python
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QPushButton, QToolBar
from PySide6.QtGui import QAction
from navigation import NavigationController
from page_types import Page
from pages import HomePage, ProfilePage, SettingsPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QStackedWidget - Industry Standard")
        self.resize(800, 600)
        self.nav_controller = NavigationController()
        self.stack = QStackedWidget()
        self.pages_map = {
            Page.HOME: HomePage(),
            Page.PROFILE: ProfilePage(),
            Page.SETTINGS: SettingsPage(),
        }
        for page_widget in self.pages_map.values():
            self.stack.addWidget(page_widget)
            page_widget.request_navigate.connect(self.nav_controller.navigate_to)
        self.nav_controller.page_changed.connect(self.on_page_changed)
        self.nav_controller.history_changed.connect(self.update_nav_buttons)
        self.setup_toolbar()
        self.setup_central()
        self.nav_controller.navigate_to(Page.HOME, add_to_history=False)

    def setup_toolbar(self):
        toolbar = QToolBar("Navigation")
        self.addToolBar(toolbar)
        self.action_back = QAction("← Back", self)
        self.action_back.setShortcut("Alt+Left")
        self.action_back.triggered.connect(self.nav_controller.go_back)
        self.action_forward = QAction("Forward →", self)
        self.action_forward.setShortcut("Alt+Right")
        self.action_forward.triggered.connect(self.nav_controller.go_forward)
        toolbar.addAction(self.action_back)
        toolbar.addAction(self.action_forward)

    def setup_central(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0,0,0,0)
        nav_bar = QHBoxLayout()
        self.btn_back = QPushButton("←")
        self.btn_forward = QPushButton("→")
        self.btn_back.setFixedWidth(50)
        self.btn_forward.setFixedWidth(50)
        self.btn_back.clicked.connect(self.nav_controller.go_back)
        self.btn_forward.clicked.connect(self.nav_controller.go_forward)
        nav_bar.addWidget(self.btn_back)
        nav_bar.addWidget(self.btn_forward)
        nav_bar.addStretch()
        layout.addLayout(nav_bar)
        layout.addWidget(self.stack)
        self.setCentralWidget(container)

    def on_page_changed(self, page: Page):
        if hasattr(self, '_last_page') and self._last_page in self.pages_map:
            self.pages_map[self._last_page].on_leave()
        widget = self.pages_map[page]
        self.stack.setCurrentWidget(widget)
        widget.on_enter()
        self._last_page = page
        self.statusBar().showMessage(f"Current: {page.name}")

    def update_nav_buttons(self, can_back: bool, can_forward: bool):
        self.btn_back.setEnabled(can_back)
        self.btn_forward.setEnabled(can_forward)
        self.action_back.setEnabled(can_back)
        self.action_forward.setEnabled(can_forward)
```


## File: `pages/__init__.py`
Public API for pages package - clean imports.

```python
"""
pages/__init__.py - Public API for pages package
Industry: Central import point, so main_window.py doesn't import from deep files
"""
# Import BasePage class from base_page.py module in the same package (the . means current package)
from .base_page import BasePage
# Import HomePage class from home_page.py module in the same package
from .home_page import HomePage
# Import ProfilePage class from profile_page.py module in the same package
from .profile_page import ProfilePage
# Import SettingsPage class from settings_page.py module in the same package
from .settings_page import SettingsPage

# Define __all__ - list of public symbols exported when someone does 'from pages import *'
__all__ = ["BasePage", "HomePage", "ProfilePage", "SettingsPage"]
```

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
    This enforces decoupled architecture.
    """
    # Defines a class-level Qt Signal that carries a Page object
	# Any page can do self.request_navigate.emit(Page.HOME) to ASK to navigate
	# It does NOT navigate itself - main_window listens to this signal and decides
	# This is how you enforce decoupling: pages never touch QStackedWidget directly
    request_navigate = Signal(Page)

    def on_enter(self):
        """Called when page becomes visible. Override if needed."""
        pass

    def on_leave(self):
        """Called when page is about to be hidden. Override if needed."""
        pass
```

## File: `pages/home_page.py`

```python
"""
pages/home_page.py - Home screen
Only responsible for its own UI
"""
from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton
from .base_page import BasePage
from page_types import Page

class HomePage(BasePage):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h1>Home Page</h1>"))
        layout.addWidget(QLabel("Landing page. Use buttons to navigate."))

        btn_profile = QPushButton("Go to Profile →")
        btn_settings = QPushButton("Go to Settings →")
        
        # INDUSTRY: Pages emit signal, they don't call stack.setCurrentIndex
        btn_profile.clicked.connect(lambda: self.request_navigate.emit(Page.PROFILE))
        btn_settings.clicked.connect(lambda: self.request_navigate.emit(Page.SETTINGS))

        layout.addWidget(btn_profile)
        layout.addWidget(btn_settings)
        layout.addStretch()
```

## File: `pages/profile_page.py`

```python
"""
pages/profile_page.py - Profile screen
Demonstrates state preservation when navigating back/forth
"""
from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QLineEdit
from .base_page import BasePage
from page_types import Page

class ProfilePage(BasePage):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h1>Profile Page</h1>"))
        
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Type something - it will stay when you go back")
        layout.addWidget(self.input_name)

        btn_home = QPushButton("← Back to Home")
        btn_home.clicked.connect(lambda: self.request_navigate.emit(Page.HOME))
        layout.addWidget(btn_home)
        layout.addStretch()

    def on_enter(self):
        print("ProfilePage entered")

    def on_leave(self):
        print("ProfilePage left")
```

## File: `pages/settings_page.py`

```python
"""
pages/settings_page.py - Settings screen
"""
from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton
from .base_page import BasePage
from page_types import Page

class SettingsPage(BasePage):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h1>Settings Page</h1>"))
        layout.addWidget(QLabel("App configuration."))

        btn_home = QPushButton("← Back to Home")
        btn_profile = QPushButton("Go to Profile")

        btn_home.clicked.connect(lambda: self.request_navigate.emit(Page.HOME))
        btn_profile.clicked.connect(lambda: self.request_navigate.emit(Page.PROFILE))

        layout.addWidget(btn_home)
        layout.addWidget(btn_profile)
        layout.addStretch()
```

---

## Industry Rules Summary

1.  **One file per page** in `pages/` package - prevents git conflicts
2.  **Enum, not int**: `Page.HOME` not `0`
3.  **Signal, not direct call**: `request_navigate.emit()` not `stack.setCurrentIndex()`
4.  **setCurrentWidget, not setCurrentIndex**: More readable and safe
5.  **Pages created ONCE**: Preserves state, no memory leak
6.  **Lifecycle hooks**: `on_enter()` / `on_leave()` for analytics, data loading
7.  **Browser behavior**: New navigation clears forward stack

## To Run
```bash
pip install PySide6
python main.py
```
Shortcuts: Alt+Left = Back, Alt+Right = Forward
