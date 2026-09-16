# LINUX BIBLE ULTIMATE - How Files Connect (No Code)

This explains the exact zip you shared (30 files) and how each file type connects. No code.

## Overview of the 30 Files

The zip contains 4 versions of the same project built over time. That's why you see `_1`, `_1_1`, `_2` suffixes:

- `database.py`, `database_1.py`, `database_1_1.py`, `database_2.py` → same role, different iterations
- `main.py`, `main_1.py`, `main_1_1.py`, `main_2.py` → same role
- `repository.py`, `repository_1.py`, `repository_1_1.py`, `repository_2.py` → same role
- `style.qss`, `style_1.qss`, `style_1_1.qss`, `style_2.qss` → dark themes
- `style_light.qss`, `style_light_1.qss`, `style_light_1_1.qss`, `style_light_2.qss` → light themes
- `widget.py`, `widget_1.py`, `widget_1_1.py`, `widget_2.py`, `widget_2_1.py`, `widget_3.py` → UI iterations
- `README.md` versions → docs

For the final app to run, you only need ONE set of 6 files:
`database.py` + `repository.py` + `widget.py` + `main.py` + `style.qss` + `style_light.qss`
The other `_1` files are older saves. The app picks the base names.

---

## File Roles

### 1. database.py - The Storage
- Defines where `bible.db` lives: same folder as the code
- Creates 6 tables: verses, bookmarks, highlights, notes, history, settings
- On first run: reads `NKJV.xml` and converts to `bible.db` for speed
- Does NOT know about UI

### 2. repository.py - The Middleman
- No UI code at all
- Talks to `database.py` (SQLite) and `NKJV.xml` (if DB not yet built)
- Provides functions like: get_books(), get_chapters(book), get_verses(book,chapter), search(keyword), add_bookmark(), add_highlight(), add_note(), add_history(), get_setting()
- This is called Repository Pattern - separates data from UI

### 3. widget.py - The UI (Brain)
Contains 3 classes:
- `VerseRow`: one row per verse with buttons for highlight colors, bookmark, note, copy
- `BibleWidget`: main widget with:
  - Top toolbar (search bar, font size, theme toggle)
  - Home page (Books grid: Old/New Testament)
  - Reader page (3 layers: chapter chooser grid, verse chooser grid, verses scroll)
  - Saved page (bookmarks + notes lists)
  - Highlights page
  - More page (search results + history)
- `MainWindow`: window container that holds BibleWidget

### 4. main.py - The Starter
- Calls `init_db()` from database.py
- Loads theme setting from repository.py
- Applies QSS stylesheet
- Creates and shows MainWindow

### 5. style.qss - Dark Theme
- Colors, borders, hover effects, tooltip style for dark mode
- No logic, only appearance

### 6. style_light.qss - Light Theme
- Same selectors as style.qss but light colors
- Toggled by theme button in widget.py

---

## How They Connect (Flow)

```
NKJV.xml
   ↓ (first run only)
database.py → creates bible.db (verses table + indexes)
   ↑
   | get_connection()
   |
repository.py → SELECT, INSERT, DELETE queries
   ↑           ↓
   | provides lists like get_books(), get_verses()
   |
widget.py → calls repository methods to get data, builds UI
   ↑        → VerseRow, grids, lists
   |
main.py → init_db() → repository.get_setting(theme) → loads style.qss/style_light.qss → shows widget.py MainWindow
   ↑
   |
style.qss / style_light.qss → applied by main.py and toggled by widget.py button
```

### Step-by-step connection:

1. User double-clicks `main.py`
2. `main.py` → `database.py: init_db()` → checks if `bible.db` exists. If not, parses `NKJV.xml` and creates it
3. `main.py` → `repository.py: get_setting("theme")` → knows dark or light
4. `main.py` → loads `style.qss` or `style_light.qss` text and applies to entire app
5. `main.py` → creates `MainWindow` → creates `BibleWidget`
6. `BibleWidget` → `repository.py: get_books()` → gets 66 books → builds Home grid of book buttons
7. User clicks a book (e.g., Genesis) → `widget.py: on_book_clicked()` → `repository.py: get_chapters("Genesis")` → builds chapter grid
8. User clicks chapter (e.g., 1) → `widget.py: show_verses()` → `repository.py: get_verses("Genesis",1)` → builds verse grid
9. User clicks verse (e.g., 5) → `widget.py: open_reader_focused()` → `repository.py: get_verses()` again + `get_highlights_map()` + `is_bookmarked()` + `get_note()` → creates VerseRow widgets for each verse → scrolls to verse 5
10. In VerseRow, user clicks highlight → `widget.py` → `repository.py: add_highlight()` → writes to `database.py` bible.db → re-renders
11. User clicks bookmark → same flow to `add_bookmark()`
12. User types in top search → `widget.py: do_search()` → `repository.py: search()` → LIKE query on verses.text → fills list in More page
13. Theme button → `widget.py: toggle_theme()` → `repository.py: set_setting("theme")` → loads other QSS file
14. Font buttons → `set_setting("font_size")` → re-renders with new size

---

## Why 30 Files in Zip?

- `database.py` + `database_1.py` + `database_1_1.py` + `database_2.py` are 4 saves of database.py as you added features (history, settings, highlights). Final version is `database.py` (or `database_2.py` is newest). Same for others.
- `widget.py` to `widget_3.py` are 6 UI iterations: basic reader → added bookmarks → added highlights → added verse chooser → added tooltips → final focused scroll
- `style.qss` variants are dark theme iterations, `style_light` variants are light theme iterations

If you want to run final app: keep only base names (`database.py`, `repository.py`, `widget.py`, `main.py`, `style.qss`, `style_light.qss`) - those are the newest. The `_1` files are backup history.

---

## Summary

- `main.py` starts everything
- `database.py` is the hard drive
- `repository.py` is the librarian that fetches from hard drive
- `widget.py` is the pages the user sees
- `style.qss` is the paint
- They connect via imports: main imports database + repository + widget, widget imports repository, repository imports database
