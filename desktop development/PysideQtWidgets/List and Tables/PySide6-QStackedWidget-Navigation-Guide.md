# PySide6 QStackedWidget & Navigation - Complete Guide

> **Stack:** PySide6 / QtWidgets (Qt 6.x)
> **Level:** Beginner to Production
> **Last Updated:** 2026

---

## Table of Contents
1. [Core Concept](#1-core-concept)
2. [QStackedWidget vs Alternatives](#2-qstackedwidget-vs-alternatives)
3. [Basic Setup](#3-basic-setup)
4. [Core API Reference](#4-core-api-reference)
5. [Adding & Managing Pages](#5-adding--managing-pages)
6. [Navigation Fundamentals](#6-navigation-fundamentals)
7. [Back Navigation & History Stack](#7-back-navigation--history-stack)
8. [Production Navigation Manager Pattern](#8-production-navigation-manager-pattern)
9. [Signals & Slots](#9-signals--slots)
10. [UI Integration Patterns](#10-ui-integration-patterns)
11. [Animations & Transitions](#11-animations--transitions)
12. [Data Passing Between Pages](#12-data-passing-between-pages)
13. [Memory & Performance](#13-memory--performance)
14. [Styling (QSS)](#14-styling-qss)
15. [Common Pitfalls & Best Practices](#15-common-pitfalls--best-practices)
16. [Complete Production Example](#16-complete-production-example)
17. [Testing](#17-testing)

---

## 1. Core Concept

`QStackedWidget` is a container that holds multiple widgets/pages but shows only ONE at a time. Think of it like a deck of cards - you only see the top card.

It's the standard way to build:
- Multi-step wizards
- Sidebar navigation (like Settings app)
- Login -> Dashboard flow
- Onboarding flows

It inherits from `QFrame` -> `QWidget`.

## 2. QStackedWidget vs Alternatives

| Widget | When to Use | When NOT to Use |
| :--- | :--- | :--- |
| **QStackedWidget** | Custom navigation, sidebar, app pages, you control buttons | You need visible tabs |
| **QTabWidget** | Has built-in tabs, browser-like UI | You want custom side menu navigation |
| **QStackedLayout** | Same as QStackedWidget but as a Layout (no frame). Use inside other layouts | You want a standalone widget |
| **QWizard** | Standard Next/Back wizard with validation | Custom UI flow |

**Industry Rule:** Use `QStackedWidget` for app-level navigation, `QStackedLayout` for component-level switching.

## 3. Basic Setup

```python
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QLabel, QVBoxLayout
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StackedWidget Basics")
        self.resize(800, 600)

        # 1. Create the StackedWidget - this is your page router
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # 2. Create pages (each page is a QWidget)
        self.page_home = self.create_page("Home Page")
        self.page_profile = self.create_page("Profile Page")
        self.page_settings = self.create_page("Settings Page")

        # 3. Add pages to stack
        self.stack.addWidget(self.page_home)      # index 0
        self.stack.addWidget(self.page_profile)   # index 1
        self.stack.addWidget(self.page_settings)  # index 2

        # 4. Show first page
        self.stack.setCurrentIndex(0)

    def create_page(self, text):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel(text))
        return page

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
```

## 4. Core API Reference

This is 90% of what you will use daily.

```python
# Adding
index = stacked.addWidget(widget)          # Returns index
stacked.insertWidget(index, widget)        # Insert at position

# Removing (CRITICAL: does NOT delete widget)
stacked.removeWidget(widget)               # Removes but widget still exists in memory
widget.deleteLater()                       # Actually delete it

# Navigation
stacked.setCurrentIndex(0)                 # Go to index
stacked.setCurrentWidget(widget)           # Go to widget object
stacked.currentIndex() -> int              # Get current index
stacked.currentWidget() -> QWidget         # Get current widget

# Info
stacked.count() -> int                     # Total pages
stacked.widget(index) -> QWidget           # Get widget at index
stacked.indexOf(widget) -> int             # Get index of widget

# Signals
stacked.currentChanged(index)              # Emitted when page changes
stacked.widgetRemoved(index)               # Emitted when removed
```

## 5. Adding & Managing Pages

### Industry Standard: Enum + Dict Pattern

Never use magic numbers like `setCurrentIndex(2)`. This breaks when you reorder pages.

```python
from enum import IntEnum

class PageIndex(IntEnum):
    HOME = 0
    PROFILE = 1
    SETTINGS = 2
    CHECKOUT = 3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stack = QStackedWidget()
        
        self.pages = {
            PageIndex.HOME: HomePage(),
            PageIndex.PROFILE: ProfilePage(),
            PageIndex.SETTINGS: SettingsPage(),
        }
        
        for page in self.pages.values():
            self.stack.addWidget(page)
    
    def navigate_to(self, page: PageIndex):
        self.stack.setCurrentIndex(page)
```

### Lazy Loading for Performance

For heavy pages, don't create all at once.

```python
def navigate_to(self, page_index):
    widget = self.stack.widget(page_index)
    if widget is None:
        # Create on demand
        if page_index == PageIndex.REPORTS:
            widget = ReportsPage() # Heavy page
            self.stack.addWidget(widget)
    self.stack.setCurrentIndex(page_index)
```

## 6. Navigation Fundamentals

Three ways to navigate:

**1. By Index (fast but fragile):**
```python
self.stack.setCurrentIndex(0)
```

**2. By Widget Reference (recommended):**
```python
self.stack.setCurrentWidget(self.profile_page)
```

**3. Next/Previous helpers:**
```python
# Custom helpers - Qt doesn't provide these
def go_next(self):
    next_idx = (self.stack.currentIndex() + 1) % self.stack.count()
    self.stack.setCurrentIndex(next_idx)

def go_prev(self):
    prev_idx = (self.stack.currentIndex() - 1) % self.stack.count()
    self.stack.setCurrentIndex(prev_idx)
```

## 7. Back Navigation & History Stack

**This is the most important part.** `QStackedWidget` has NO built-in back button or history. You must implement it yourself. This is industry standard.

### The History Stack Pattern

```python
from collections import deque

class NavigableStackedWidget(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.history = deque(maxlen=20) # Prevent memory leak
        self._is_going_back = False

        # Track history automatically
        self.currentChanged.connect(self._on_page_changed)

    def _on_page_changed(self, new_index):
        if self._is_going_back:
            self._is_going_back = False
            return
        
        # Save previous index to history
        # We need to get sender? Better to track manually in navigate_to
        pass

    def navigate_to(self, index: int):
        # Save current before moving
        current = self.currentIndex()
        if current != -1 and current != index:
            self.history.append(current)
        self.setCurrentIndex(index)

    def can_go_back(self) -> bool:
        return len(self.history) > 0

    def go_back(self):
        if not self.can_go_back():
            return
        
        self._is_going_back = True
        prev_index = self.history.pop()
        self.setCurrentIndex(prev_index)
```

### Production-Ready Navigation Controller

This is how it's done in real apps:

```python
from PySide6.QtCore import QObject, Signal

class NavigationController(QObject):
    navigated = Signal(int, int) # from, to

    def __init__(self, stacked_widget: QStackedWidget):
        super().__init__()
        self.stack = stacked_widget
        self.history: list[int] = []
        self.future: list[int] = [] # For forward navigation

    def navigate(self, index: int, add_to_history=True):
        if index < 0 or index >= self.stack.count():
            return
        
        current = self.stack.currentIndex()
        if current == index:
            return

        if add_to_history and current != -1:
            self.history.append(current)
            self.future.clear() # Clear forward on new navigation

        self.stack.setCurrentIndex(index)
        self.navigated.emit(current, index)

    def back(self):
        if not self.history:
            return False
        current = self.stack.currentIndex()
        prev = self.history.pop()
        self.future.append(current)
        self.stack.setCurrentIndex(prev)
        return True

    def forward(self):
        if not self.future:
            return False
        next_idx = self.future.pop()
        self.history.append(self.stack.currentIndex())
        self.stack.setCurrentIndex(next_idx)
        return True

    def can_go_back(self): return bool(self.history)
    def can_go_forward(self): return bool(self.future)
```

Usage with Back Button:
```python
self.nav = NavigationController(self.stack)
self.btn_back.clicked.connect(self.nav.back)
self.btn_next.clicked.connect(self.nav.forward)

# Enable/disable buttons automatically
self.nav.navigated.connect(lambda: self.btn_back.setEnabled(self.nav.can_go_back()))
```

## 8. Production Navigation Manager Pattern

For large apps, separate pages into their own classes with a common interface.

```python
class BasePage(QWidget):
    # All pages should have this
    def on_enter(self, data=None):
        """Called when page becomes visible"""
        pass

    def on_leave(self):
        """Called when leaving page - use for cleanup/saving"""
        pass

class HomePage(BasePage):
    def __init__(self, navigator):
        super().__init__()
        self.navigator = navigator
        btn = QPushButton("Go to Profile")
        btn.clicked.connect(lambda: navigator.navigate(PageIndex.PROFILE))

# In MainWindow
def setup_navigation(self):
    self.stack.currentChanged.connect(self._handle_page_change)
    self._last_index = 0

def _handle_page_change(self, new_index):
    old_widget = self.stack.widget(self._last_index)
    if hasattr(old_widget, 'on_leave'):
        old_widget.on_leave()
    
    new_widget = self.stack.widget(new_index)
    if hasattr(new_widget, 'on_enter'):
        new_widget.on_enter()
    
    self._last_index = new_index
```

## 9. Signals & Slots

```python
# React to page changes
self.stack.currentChanged.connect(self.on_page_changed)

def on_page_changed(self, index):
    print(f"Switched to page {index}")
    # Update window title, sidebar highlight, etc.
    
    if index == PageIndex.SETTINGS:
        self.pages[PageIndex.SETTINGS].load_settings()

# Disconnect safely
self.stack.currentChanged.disconnect()
```

## 10. UI Integration Patterns

### Pattern A: Sidebar Navigation (Modern Apps)

```python
# Layout: [Sidebar | StackedWidget]
from PySide6.QtWidgets import QHBoxLayout, QListWidget

container = QWidget()
layout = QHBoxLayout(container)
sidebar = QListWidget()
sidebar.addItems(["Home", "Profile", "Settings"])
layout.addWidget(sidebar, 1)
layout.addWidget(self.stack, 4)

sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)
```

### Pattern B: Top Nav + StackedWidget

Use QToolBar or custom buttons.

### Pattern C: Wizard with Validation

```python
def go_next(self):
    current_page = self.stack.currentWidget()
    if hasattr(current_page, 'validate'):
        if not current_page.validate():
            return # Block navigation
    self.nav.navigate(self.stack.currentIndex() + 1)
```

## 11. Animations & Transitions

QStackedWidget has no built-in animation. Industry approach: use QPropertyAnimation or fake it.

**Simple Fade (Industry Standard):**

```python
from PySide6.QtCore import QPropertyAnimation
from PySide6.QtWidgets import QGraphicsOpacityEffect

def fade_to(self, next_index):
    current = self.stack.currentWidget()
    effect = QGraphicsOpacityEffect(current)
    current.setGraphicsEffect(effect)
    
    self.anim = QPropertyAnimation(effect, b"opacity")
    self.anim.setDuration(150)
    self.anim.setStartValue(1.0)
    self.anim.setEndValue(0.0)
    self.anim.finished.connect(lambda: self._switch_after_fade(next_index))
    self.anim.start()

def _switch_after_fade(self, next_index):
    self.stack.setCurrentIndex(next_index)
```

For slide animations, use two stacked widgets or `QParallelAnimationGroup`. Most production apps skip heavy animations for performance.

## 12. Data Passing Between Pages

**ANTI-PATTERN:** Global variables

**PATTERN 1: Shared Model / Service**
```python
class AppState:
    user = None
    cart = []

# Inject into pages
page = ProfilePage(app_state)
```

**PATTERN 2: Signals (Loosely Coupled)**
```python
class CheckoutPage(QWidget):
    order_placed = Signal(dict)

# MainWindow connects
checkout.order_placed.connect(lambda data: self.pages[PageIndex.SUCCESS].show_order(data))
```

**PATTERN 3: Navigator with payload**
```python
def navigate_with_data(self, index, data):
    widget = self.stack.widget(index)
    if hasattr(widget, 'on_enter'):
        widget.on_enter(data)
    self.stack.setCurrentIndex(index)
```

## 13. Memory & Performance

1.  `removeWidget()` does NOT delete. You must call `deleteLater()` if you want to free memory.
2.  For 20+ pages, use lazy loading.
3.  Don't put heavy `__init__` logic in pages - put it in `on_enter()`.
4.  Use `QStackedLayout.setStackingMode(QStackedLayout.StackAll)` if you need background pages to keep updating (e.g., video).

## 14. Styling (QSS)

```css
/* QStackedWidget itself is invisible */
QStackedWidget {
    background: #f5f5f5;
    border: none;
}

/* Style pages individually */
#HomePage {
    background: white;
}
```

Apply object names:
```python
page.setObjectName("HomePage")
```

## 15. Common Pitfalls & Best Practices

| Pitfall | Fix |
| :--- | :--- |
| Using magic numbers `setCurrentIndex(3)` | Use `IntEnum` |
| Memory leak from not deleting removed widgets | Call `widget.deleteLater()` |
| No back functionality | Implement `NavigationController` |
| Heavy init blocking UI | Lazy load + move logic to `on_enter` |
| Tight coupling between pages | Use Signals or shared service, not `main_window.stack.set...` inside page |
| Forgetting to handle `currentIndex() == -1` on startup | Check before navigating |

**Checklist for Production:**
- [ ] Use Enum for indexes
- [ ] Implement history stack with `deque(maxlen=50)`
- [ ] Pages inherit from `BasePage` with `on_enter/on_leave`
- [ ] Navigation logic lives in ONE controller, not scattered
- [ ] Back button disabled when `can_go_back() == False`
- [ ] Keyboard shortcuts: `Alt+Left` for back, `Alt+Right` for forward

```python
# Keyboard shortcut
from PySide6.QtGui import QShortcut, QKeySequence
QShortcut(QKeySequence("Alt+Left"), self, self.nav.back)
```

## 16. Complete Production Example

```python
import sys
from enum import IntEnum
from PySide6.QtWidgets import *
from PySide6.QtCore import QObject, Signal

class Pages(IntEnum):
    LOGIN = 0
    DASHBOARD = 1
    SETTINGS = 2

class BasePage(QWidget):
    def on_enter(self, data=None): pass
    def on_leave(self): pass

class LoginPage(BasePage):
    login_success = Signal(dict)
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Login"))
        btn = QPushButton("Login")
        btn.clicked.connect(lambda: self.login_success.emit({"user": "kevin"}))
        layout.addWidget(btn)

class DashboardPage(BasePage):
    def on_enter(self, data=None):
        print(f"Dashboard entered with {data}")

class NavigationController(QObject):
    def __init__(self, stack: QStackedWidget):
        super().__init__()
        self.stack = stack
        self.history = []

    def go(self, page: Pages, data=None):
        curr = self.stack.currentIndex()
        if curr != page:
            self.history.append(curr)
        w = self.stack.widget(page)
        if hasattr(w, 'on_enter'):
            w.on_enter(data)
        self.stack.setCurrentIndex(page)

    def back(self):
        if self.history:
            prev = self.history.pop()
            self.stack.setCurrentIndex(prev)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.nav = NavigationController(self.stack)

        self.login = LoginPage()
        self.dashboard = DashboardPage()
        self.settings = BasePage()

        self.stack.addWidget(self.login)
        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.settings)

        self.login.login_success.connect(lambda d: self.nav.go(Pages.DASHBOARD, d))

        # Back button
        toolbar = self.addToolBar("Nav")
        toolbar.addAction("Back", self.nav.back)

app = QApplication(sys.argv)
win = MainWindow()
win.show()
app.exec()
```

## 17. Testing

```python
def test_navigation(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.stack.currentIndex() == Pages.LOGIN
    window.nav.go(Pages.DASHBOARD)
    assert window.stack.currentIndex() == Pages.DASHBOARD
    window.nav.back()
    assert window.stack.currentIndex() == Pages.LOGIN
```

---

### TL;DR Industry Rules

1.  **Never hardcode indexes.** Use Enum.
2.  **QStackedWidget has no history.** You build it.
3.  **One NavigationController** to rule them all.
4.  **Pages should not know about each other.** They talk via controller/signals.
5.  **Lazy load heavy pages.**
6.  **on_enter / on_leave** is your lifecycle.

You now know more than 90% of PySide6 devs about stacked navigation.
