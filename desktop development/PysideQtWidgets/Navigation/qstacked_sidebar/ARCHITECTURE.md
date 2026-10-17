# QStackedWidget Navigation + Collapsible Sidebar - Complete Guide

> Production-ready template for PySide6. Combines your collapsible sidebar with industry-standard QStackedWidget navigation.

## 1. Project Structure

```
qstacked_sidebar/
├── main.py                 # Entry only - no logic
├── page_types.py           # Enum contract - zero deps
├── navigation.py           # Brain - history stacks
├── main_window.py          # Boss - owns QStackedWidget, wires signals
├── style.qss               # All styling
├── widgets/
│   └── sidebar.py          # Collapsible sidebar you studied
└── pages/
    ├── base_page.py        # Enforces request_navigate
    ├── home_page.py
    ├── notes_page.py       # Markdown viewer example
    └── settings_page.py
```

## 2. Why This Architecture?

### Problem with beginner code:
```python
# BAD - tight coupling, magic numbers, state loss
sidebar.btn.clicked.connect(lambda: stack.setCurrentIndex(0))
```

### Industry solution: 3 Layers
```
[UI Layer] Pages + Sidebar --(Signal: request_navigate)--> 
[Brain Layer] NavigationController --(Signal: page_changed)--> 
[Owner Layer] MainWindow --(Method: setCurrentWidget)-->
```

**Rules:**
1.  **One file per page** - prevents git conflicts, clear ownership
2.  **Enum not int** - `Page.HOME` not `0`
3.  **Signal not direct call** - `request_navigate.emit()` not `stack.setCurrentIndex()`
4.  **Pages created ONCE** - state preserved (QLineEdit text stays when you go back)
5.  **Lifecycle hooks** - `on_enter()` / `on_leave()` for load/save
6.  **Browser behavior** - new navigation clears forward stack

## 3. File-by-File Deep Dive

### `page_types.py` - The Contract
Zero imports. Everyone can import it without circular imports.

### `widgets/sidebar.py` - Your Sidebar Upgraded
**Previous bug you had:** You styled `QVBoxLayout` with `background-color`. QLayout has no paint.
**Fix:** Wrap each area in `QWidget` + `setAttribute(WA_StyledBackground, True)`

Key features:
- `collapsed_width = 65`, `expanded_width = 220`
- `setFixedWidth(end)` to toggle
- Text swap: `"◉ Dashboard"` <-> `"◉"` when collapsed
- `request_navigate = Signal(Page)` - same as pages!
- `set_active_page()` highlights current page with `:checked` stylesheet
- `set_history_state()` enables/disables Back/Forward

### `navigation.py` - Browser History
Two lists: `_history` (back) and `_future` (forward)

```python
navigate_to(PROFILE):
  _history.append(current)  # save current to back
  _future.clear()           # clear forward (branch)
  _current = PROFILE

go_back():
  _future.append(current)   # save current to forward
  _current = _history.pop() # restore previous

go_forward():
  _history.append(current)  # save current to back
  _current = _future.pop()  # restore next
```

### `main_window.py` - Wiring
This is the only place that touches `QStackedWidget`:

```python
# A: Page/Sidebar -> Controller
page.request_navigate.connect(nav_controller.navigate_to)
sidebar.request_navigate.connect(nav_controller.navigate_to)

# B: Controller -> MainWindow
nav_controller.page_changed.connect(on_page_changed)
nav_controller.history_changed.connect(sidebar.set_history_state)

def on_page_changed(page):
    pages_map[last_page].on_leave()
    stack.setCurrentWidget(pages_map[page])
    pages_map[page].on_enter()
    sidebar.set_active_page(page)
```

### `pages/base_page.py` - Enforce Decoupling
```python
class BasePage(QWidget):
    request_navigate = Signal(Page) # ONLY way to navigate
```
Pages can NEVER do `self.parent().stack.setCurrentIndex()`. They request.

## 4. How to Add a New Page

1. Add to enum: `PROFILE = 3` in `page_types.py`
2. Create `pages/profile_page.py` inheriting `BasePage`
3. Register in `pages/__init__.py`
4. In `main_window.py`: `self.pages_map[Page.PROFILE] = ProfilePage()`
5. Add button in `sidebar.py` + mapping in `_buttons`

Done. No other file touches navigation logic.

## 5. Markdown Notes Integration

`NotesPage` uses `QTextBrowser.setMarkdown()` which natively renders markdown.

For real files:
```python
with open("notes/todo.md") as f:
    self.viewer.setMarkdown(f.read())
```

Add a `QListWidget` left of viewer to list files, and connect `currentRowChanged` to load markdown.

## 6. Styling Notes

- `QLayout` -> NOT stylable. Wrap in `QWidget`.
- `QWidget` needs `WA_StyledBackground` to receive `background-color`.
- Use objectName for QSS: `#sidebar`, `#navBtn:checked`

## 7. Run & Shortcuts

```bash
pip install PySide6
python main.py
```

Alt+Left = Back (add QAction if you want), Alt+Right = Forward

---

**Study order:** `page_types.py` -> `base_page.py` -> `navigation.py` -> `sidebar.py` -> `main_window.py`
