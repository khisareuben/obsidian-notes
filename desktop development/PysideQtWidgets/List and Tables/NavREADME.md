
# How to Use This in a Real Project

This is NOT theory. This is the exact structure used in production apps.

## Project Structure
```
your_app/
├── main.py              # MainWindow - wires sidebar + stack + toolbar
├── navigation.py        # NavigationController + Page Enum (THE BRAIN)
└── pages/
    ├── base.py          # BasePage with on_enter/on_leave
    ├── home.py
    ├── profile.py
    └── settings.py
```

## 3 Rules to Live By

### Rule 1: ONE Navigator
Never do `self.stack.setCurrentIndex()` inside a page.
Always do `self.navigator.navigate_to(Page.PROFILE)`

### Rule 2: Enum, not numbers
BAD: `navigate_to(1)`
GOOD: `navigate_to(Page.PROFILE)`

### Rule 3: Pages don't talk directly
BAD: `main_window.profile_page.name_input.setText(...)`
GOOD: Use `on_enter(data)` to pass data.

## How It Works Step-by-Step

1. **User clicks "Go to Profile" in HomePage**
   -> `HomePage` calls `navigator.navigate_to(Page.PROFILE, data={...})`

2. **Navigator saves history**
   -> Pushes current index (HOME) into `_history` deque
   -> Sets `_nav_data` on target widget

3. **Stack changes**
   -> Qt emits `currentChanged`
   -> `NavigationController._on_stack_changed` fires
   -> Old page's `on_leave()` is called (save data here)
   -> New page's `on_enter(data)` is called (load data here)

4. **Back button**
   -> `navigator.back()` pops from history and goes back
   -> Does NOT add current page to history again

## How to Add a New Page (4 steps)

1. Create `pages/checkout.py` inheriting `BasePage`
2. Add `CHECKOUT = 3` to `Page` Enum in `navigation.py`
3. In `main.py`: `self.checkout = CheckoutPage(self.navigator)` + `self.stack.addWidget(...)`
4. Navigate: `self.navigator.navigate_to(Page.CHECKOUT)`

## Running
```
pip install PySide6
python main.py
```
Try: Sidebar, Back/Forward buttons, Alt+Left/Right, buttons inside pages. All stay in sync.
