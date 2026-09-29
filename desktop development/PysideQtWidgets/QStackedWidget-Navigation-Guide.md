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

        # Central controller for navigation logic (history, back/forward, current page)
        # Keeps UI decoupled from navigation rules
        self.nav_controller = NavigationController()

        # QStackedWidget holds all pages in a stack, but only shows one at a time
        # This is the industry standard for multi-page apps instead of creating/destroying pages
        self.stack = QStackedWidget()

        # Pre-instantiate all pages and map them to their enum identifier
        # This allows fast switching and state preservation
        self.pages_map = {
            Page.HOME: HomePage(),
            Page.PROFILE: ProfilePage(),
            Page.SETTINGS: SettingsPage(),
        }

        # Add each page to the stack and connect its internal navigation requests
        # to the central controller
        for page_widget in self.pages_map.values():
            self.stack.addWidget(page_widget)
            # Each page can emit request_navigate(Page.X) to request a page change
            page_widget.request_navigate.connect(self.nav_controller.navigate_to)

        # Controller -> UI: when the controller decides page has changed, update the UI
        self.nav_controller.page_changed.connect(self.on_page_changed)
        # Controller -> UI: when back/forward availability changes, update button states
        self.nav_controller.history_changed.connect(self.update_nav_buttons)

        self.setup_toolbar()
        self.setup_central()

        # Initial navigation - don't add to history since this is the first entry
        self.nav_controller.navigate_to(Page.HOME, add_to_history=False)

    def setup_toolbar(self):
        toolbar = QToolBar("Navigation")
        self.addToolBar(toolbar)

        # Browser-style actions with shortcuts Alt+Left / Alt+Right
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

        # Custom in-content navigation bar (duplicate of toolbar for convenience)
        nav_bar = QHBoxLayout()
        self.btn_back = QPushButton("←")
        self.btn_forward = QPushButton("→")
        self.btn_back.setFixedWidth(50)
        self.btn_forward.setFixedWidth(50)
        self.btn_back.clicked.connect(self.nav_controller.go_back)
        self.btn_forward.clicked.connect(self.nav_controller.go_forward)
        nav_bar.addWidget(self.btn_back)
        nav_bar.addWidget(self.btn_forward)
        nav_bar.addStretch() # Push buttons to the left

        layout.addLayout(nav_bar)
        layout.addWidget(self.stack) # Stack takes remaining space
        self.setCentralWidget(container)

    def on_page_changed(self, page: Page):
        # Call lifecycle hook on the page we're leaving (for cleanup / save state)
        if hasattr(self, '_last_page') and self._last_page in self.pages_map:
            self.pages_map[self._last_page].on_leave()

        # Switch the visible widget in the stack
        widget = self.pages_map[page]
        self.stack.setCurrentWidget(widget)

        # Call lifecycle hook on the page we're entering (for refresh / load data)
        widget.on_enter()

        # Track last page for next transition
        self._last_page = page
        self.statusBar().showMessage(f"Current: {page.name}")

    def update_nav_buttons(self, can_back: bool, can_forward: bool):
        # Enable/disable both toolbar and in-content buttons based on history state
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

This is a perfect **MVC-like decoupled architecture**. Think of it as 3 layers. Here is how they connect:

### The Big Picture

```
main.py → MainWindow → NavigationController → Pages
[STARTS] [OWNS EVERYTHING] [THE BRAIN] [DUMB UI]
```

**1. `page_types.py` - The Contract (no dependencies)**
This is at the bottom so EVERYONE can import it without circular imports. It's just an Enum: `HOME=0, PROFILE=1, SETTINGS=2`. It stops you from using magic numbers like `stack.setCurrentIndex(0)`.

**2. `pages/base_page.py` - The Rule**
Every page inherits from `BasePage`. It has one crucial line:

```python
request_navigate = Signal(Page)
```

This is the rule: **Pages are NOT allowed to touch `QStackedWidget`**. They can only say "I *request* to go to PROFILE" by emitting this signal. They are dumb.

**3. `pages/` - The UI**
`HomePage`, `ProfilePage`, etc. just emit:
```python
self.request_navigate.emit(Page.PROFILE)
```
They don't know who listens. They also have `on_enter()` / `on_leave()` - called when you arrive/leave, good for loading data.

`pages/__init__.py` just makes imports clean so MainWindow can do `from pages import HomePage` instead of `from pages.home_page import HomePage`.

**4. `navigation.py` - The Brain**
It owns two lists: `_history` and `_future` - exactly like a browser.

It does ZERO UI work. It just manages state:
- `navigate_to(Page.PROFILE)` -> pushes current page to `_history`, clears `_future`, sets `_current = PROFILE`, then emits `page_changed` and `history_changed`
- `go_back()` -> pops from `_history`, pushes current to `_future`
- `go_forward()` -> pops from `_future`, pushes current to `_history`

It talks to the outside world ONLY via signals: `page_changed` and `history_changed`.

**5. `main_window.py` - The Boss Who Wires Everything**
This is where everything connects. Look at `__init__`:

```python
# 1. Create brain
self.nav_controller = NavigationController()

# 2. Create the actual QStackedWidget
self.stack = QStackedWidget()

# 3. Create all pages ONCE - so state is preserved (your QLineEdit text stays)
self.pages_map = {
    Page.HOME: HomePage(),
    Page.PROFILE: ProfilePage(),
}

# 4. WIRING A: Page -> Controller
# When any page says "I want to navigate", tell the controller
page_widget.request_navigate.connect(self.nav_controller.navigate_to)

# 5. WIRING B: Controller -> MainWindow
# When controller says "page changed", MainWindow actually changes the UI
self.nav_controller.page_changed.connect(self.on_page_changed)
self.nav_controller.history_changed.connect(self.update_nav_buttons)

# 6. Start
self.nav_controller.navigate_to(Page.HOME, add_to_history=False)
```

Then `on_page_changed` does the only place where `QStackedWidget` is touched:

```python
def on_page_changed(self, page: Page):
    self.pages_map[self._last_page].on_leave() # old page cleanup
    self.stack.setCurrentWidget(self.pages_map[page]) # THE ONLY setCurrentWidget in app
    self.pages_map[page].on_enter() # new page init
```

**6. `main.py` - Entry only**
Just creates `QApplication` and shows `MainWindow`. This is why you don't get segfaults anymore - `app` lives for the whole program, `window` is kept as a variable until `app.exec()` finishes.

### Flow Example: Click "Go to Profile"

1. You are on `HOME`. You click button in `HomePage`
2. `HomePage` emits `request_navigate.emit(Page.PROFILE)`
3. `MainWindow` is listening, it calls `nav_controller.navigate_to(PROFILE)`
4. Controller: `_history = [HOME]`, `_current = PROFILE`, emits `page_changed(PROFILE)`
5. `MainWindow.on_page_changed` hears it: calls `home.on_leave()`, does `stack.setCurrentWidget(profile)`, calls `profile.on_enter()`
6. Controller also emits `history_changed(True, False)` -> MainWindow enables/disables Back/Forward buttons.

If you now press Back: `nav_controller.go_back()` -> `_history=[]`, `_future=[PROFILE]`, `_current=HOME` -> `page_changed(HOME)` -> UI switches back. Your text in Profile's QLineEdit is still there because the `ProfilePage` object was never deleted.

That's the industry rule: **Pages request, Controller decides, MainWindow executes.**
