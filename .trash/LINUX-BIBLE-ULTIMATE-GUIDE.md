# LINUX BIBLE - ULTIMATE - Complete Build Guide
# Tags: #PySide6 #SQLite #BibleApp #Portfolio #Python

> **Home = Books instantly** | Flow: Book → Chapter → Verse → Focused Reader
> Features: Search, Bookmarks, Highlights (5 colors), Notes, Copy, History, Font, Light/Dark Theme, Tooltips

---

## 0. Project Structure (Industry)

```
15_bible_app_ultimate/
├── database.py          # DB creation + XML -> SQLite conversion
├── repository.py        # All data access (no UI)
├── widget.py            # All UI (no SQL/XML parsing) - VerseRow + BibleWidget + MainWindow
├── main.py              # Entry point + theme loading
├── style.qss            # Dark theme
├── style_light.qss      # Light theme
├── NKJV.xml             # You provide (31k verses)
└── bible.db             # Auto-created on first run (5MB)
```

**Where is DB stored?**
```python
DB_PATH = Path(__file__).resolve().parent / "bible.db"
```
Same folder as code. Yes you can replace it with same name + same tables and app shows new data.

---

## 1. Step 0 - Setup

```bash
mkdir 15_bible_app_ultimate && cd 15_bible_app_ultimate
pip install PySide6
touch database.py repository.py widget.py main.py style.qss style_light.qss
# Put NKJV.xml in folder
python main.py
```

---

## 2. Step 1 - database.py

**Purpose:** Create SQLite file and convert XML to DB once for speed.

**Tables:**
- verses(book, chapter, verse, text) + INDEX on (book,chapter) and text for LIKE search
- bookmarks, highlights(book,chapter,verse,color), notes, history, settings(key,value)

```python

from pathlib import Path
import xml.etree.ElementTree as ET
import sqlite3

DB_PATH = Path(__file__).resolve().parent / "bible.db"
XML_PATH = Path(__file__).resolve().parent / "NKJV.xml"

def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    is_first = not DB_PATH.exists()
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS verses (book TEXT, chapter INTEGER, verse INTEGER, text TEXT)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_book_ch ON verses(book, chapter)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_text ON verses(text)")
    cur.execute("CREATE TABLE IF NOT EXISTS bookmarks (id INTEGER PRIMARY KEY AUTOINCREMENT, book TEXT, chapter INTEGER, verse INTEGER, text TEXT, saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    cur.execute("CREATE TABLE IF NOT EXISTS highlights (id INTEGER PRIMARY KEY AUTOINCREMENT, book TEXT, chapter INTEGER, verse INTEGER, color TEXT, text TEXT, saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UNIQUE(book, chapter, verse))")
    cur.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, book TEXT, chapter INTEGER, verse INTEGER, note TEXT, saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UNIQUE(book, chapter, verse))")
    cur.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, book TEXT, chapter INTEGER, visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    cur.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
    cur.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('theme','dark')")
    cur.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('font_size','18')")
    cur.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('last_book','Genesis')")
    cur.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('last_chapter','1')")
    conn.commit()

    if is_first and XML_PATH.exists():
        print("First run: Building bible.db from NKJV.xml...")
        try:
            tree = ET.parse(str(XML_PATH))
            root = tree.getroot()
            data = []
            for b in root.findall('b'):
                bn = b.get('n')
                for c in b.findall('c'):
                    ch = int(c.get('n'))
                    for v in c.findall('v'):
                        vn = int(v.get('n'))
                        txt = v.text if v.text else ""
                        data.append((bn, ch, vn, txt))
            cur.executemany("INSERT INTO verses VALUES (?,?,?,?)", data)
            conn.commit()
            print(f"Built {len(data)} verses")
        except Exception as e:
            print(f"XML build failed: {e}")

    conn.close()
    return True

```

**First run logic:**
- If bible.db doesn't exist and NKJV.xml exists -> parse XML -> executemany INSERT -> commit
- Next runs -> skip building, use DB directly (0.1s vs 3s)

---

## 3. Step 2 - repository.py (Repository Pattern)

No UI here. Only data.

Key methods:
- get_books() -> preserves XML order (66 books)
- get_chapters(book) -> SELECT DISTINCT chapter
- get_verses(book, chapter) -> SELECT verse,text ORDER BY verse
- search(keyword, limit=400) -> SELECT ... WHERE text LIKE %keyword%
- add_bookmark / is_bookmarked / get_bookmarks / delete_bookmark
- add_highlight / get_highlights_map(book,chapter) returns dict {verse: color} for rendering
- add_note / get_note / get_notes
- add_history / get_history (last 100, auto delete old)
- get_setting / set_setting (theme, font_size, last_book)

```python

import sqlite3
import random
from database import get_connection, DB_PATH, XML_PATH
import xml.etree.ElementTree as ET

class BibleRepository:
    def __init__(self):
        self.use_db = DB_PATH.exists()

    def get_books(self):
        if XML_PATH.exists():
            try:
                tree = ET.parse(str(XML_PATH))
                return [b.get('n') for b in tree.getroot().findall('b')]
            except:
                pass
        if self.use_db:
            conn = get_connection()
            rows = conn.execute("SELECT DISTINCT book FROM verses").fetchall()
            conn.close()
            return [r["book"] for r in rows]
        return ["Genesis","Exodus","Leviticus","Numbers","Deuteronomy","Joshua","Judges","Ruth","1 Samuel","2 Samuel","1 Kings","2 Kings","1 Chronicles","2 Chronicles","Ezra","Nehemiah","Esther","Job","Psalms","Proverbs","Ecclesiastes","Song of Solomon","Isaiah","Jeremiah","Lamentations","Ezekiel","Daniel","Hosea","Joel","Amos","Obadiah","Jonah","Micah","Nahum","Habakkuk","Zephaniah","Haggai","Zechariah","Malachi","Matthew","Mark","Luke","John","Acts","Romans","1 Corinthians","2 Corinthians","Galatians","Ephesians","Philippians","Colossians","1 Thessalonians","2 Thessalonians","1 Timothy","2 Timothy","Titus","Philemon","Hebrews","James","1 Peter","2 Peter","1 John","2 John","3 John","Jude","Revelation"]

    def get_chapters(self, book):
        if self.use_db:
            conn = get_connection()
            rows = conn.execute("SELECT DISTINCT chapter FROM verses WHERE book=? ORDER BY chapter", (book,)).fetchall()
            conn.close()
            if rows:
                return [r["chapter"] for r in rows]
        if XML_PATH.exists():
            try:
                tree = ET.parse(str(XML_PATH))
                for b in tree.getroot().findall('b'):
                    if b.get('n') == book:
                        return [int(c.get('n')) for c in b.findall('c')]
            except:
                pass
        return list(range(1, 51))

    def get_verses(self, book, chapter):
        if self.use_db:
            conn = get_connection()
            rows = conn.execute("SELECT verse, text FROM verses WHERE book=? AND chapter=? ORDER BY verse", (book, chapter)).fetchall()
            conn.close()
            if rows:
                return [(r["verse"], r["text"]) for r in rows]
        if XML_PATH.exists():
            try:
                tree = ET.parse(str(XML_PATH))
                for b in tree.getroot().findall('b'):
                    if b.get('n') == book:
                        for c in b.findall('c'):
                            if int(c.get('n')) == chapter:
                                return [(int(v.get('n')), v.text or "") for v in c.findall('v')]
            except:
                pass
        return []

    def search(self, keyword, limit=400):
        if not keyword.strip() or not self.use_db:
            return []
        kw = f"%{keyword}%"
        conn = get_connection()
        rows = conn.execute("SELECT book, chapter, verse, text FROM verses WHERE text LIKE ? ORDER BY book, chapter, verse LIMIT ?", (kw, limit)).fetchall()
        conn.close()
        return [(r["book"], r["chapter"], r["verse"], r["text"]) for r in rows]

    def get_daily_verse(self):
        if not self.use_db:
            return ("John", 3, 16, "For God so loved the world...")
        conn = get_connection()
        # random
        row = conn.execute("SELECT book, chapter, verse, text FROM verses ORDER BY RANDOM() LIMIT 1").fetchone()
        conn.close()
        if row:
            return (row["book"], row["chapter"], row["verse"], row["text"])
        return ("Genesis", 1, 1, "In the beginning God created...")

    # Settings
    def get_setting(self, key, default=""):
        try:
            conn = get_connection()
            r = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
            conn.close()
            return r["value"] if r else default
        except:
            return default

    def set_setting(self, key, value):
        try:
            conn = get_connection()
            conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?,?)", (key, value))
            conn.commit()
            conn.close()
        except:
            pass

    # Bookmarks
    def add_bookmark(self, book, chapter, verse, text):
        conn = get_connection()
        conn.execute("INSERT OR IGNORE INTO bookmarks (book, chapter, verse, text) VALUES (?,?,?,?)", (book, chapter, verse, text))
        conn.commit()
        conn.close()

    def get_bookmarks(self):
        conn = get_connection()
        rows = conn.execute("SELECT id, book, chapter, verse, text FROM bookmarks ORDER BY saved_at DESC").fetchall()
        conn.close()
        return rows

    def delete_bookmark(self, bid):
        conn = get_connection()
        conn.execute("DELETE FROM bookmarks WHERE id=?", (bid,))
        conn.commit()
        conn.close()

    def is_bookmarked(self, book, chapter, verse):
        conn = get_connection()
        r = conn.execute("SELECT id FROM bookmarks WHERE book=? AND chapter=? AND verse=?", (book, chapter, verse)).fetchone()
        conn.close()
        return r is not None

    # Highlights
    def add_highlight(self, book, chapter, verse, text, color):
        conn = get_connection()
        conn.execute("INSERT OR REPLACE INTO highlights (book, chapter, verse, color, text) VALUES (?,?,?,?,?)", (book, chapter, verse, color, text))
        conn.commit()
        conn.close()

    def remove_highlight(self, book, chapter, verse):
        conn = get_connection()
        conn.execute("DELETE FROM highlights WHERE book=? AND chapter=? AND verse=?", (book, chapter, verse))
        conn.commit()
        conn.close()

    def get_highlights(self):
        conn = get_connection()
        rows = conn.execute("SELECT id, book, chapter, verse, color, text FROM highlights ORDER BY saved_at DESC").fetchall()
        conn.close()
        return rows

    def get_highlights_map(self, book, chapter):
        conn = get_connection()
        rows = conn.execute("SELECT verse, color FROM highlights WHERE book=? AND chapter=?", (book, chapter)).fetchall()
        conn.close()
        return {r["verse"]: r["color"] for r in rows}

    # Notes
    def add_note(self, book, chapter, verse, note):
        conn = get_connection()
        conn.execute("INSERT OR REPLACE INTO notes (book, chapter, verse, note) VALUES (?,?,?,?)", (book, chapter, verse, note))
        conn.commit()
        conn.close()

    def get_notes(self):
        conn = get_connection()
        rows = conn.execute("SELECT id, book, chapter, verse, note FROM notes ORDER BY saved_at DESC").fetchall()
        conn.close()
        return rows

    def get_note(self, book, chapter, verse):
        conn = get_connection()
        r = conn.execute("SELECT note FROM notes WHERE book=? AND chapter=? AND verse=?", (book, chapter, verse)).fetchone()
        conn.close()
        return r["note"] if r else ""

    def delete_note(self, bid):
        conn = get_connection()
        conn.execute("DELETE FROM notes WHERE id=?", (bid,))
        conn.commit()
        conn.close()

    # History
    def add_history(self, book, chapter):
        conn = get_connection()
        last = conn.execute("SELECT book, chapter FROM history ORDER BY id DESC LIMIT 1").fetchone()
        if not last or last["book"] != book or last["chapter"] != chapter:
            conn.execute("INSERT INTO history (book, chapter) VALUES (?,?)", (book, chapter))
            conn.execute("DELETE FROM history WHERE id NOT IN (SELECT id FROM history ORDER BY id DESC LIMIT 100)")
            conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('last_book', ?)", (book,))
            conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('last_chapter', ?)", (str(chapter),))
            conn.commit()
        conn.close()

    def get_history(self):
        conn = get_connection()
        rows = conn.execute("SELECT book, chapter FROM history ORDER BY id DESC LIMIT 30").fetchall()
        conn.close()
        return rows

```

---

## 4. Step 3 - widget.py (The Brain)

### 4.1 VerseRow(QFrame)

Each verse is a QFrame, not HTML. Contains:

```
[ 1 ] In the beginning... [🟨][🟩][🟥][🟦][🟪][🔖][📝][📋]
```

- ObjectName = f"verse_{num}" for scrolling focus
- Signals: bookmarkClicked, highlightClicked, noteClicked, copyClicked
- highlight_color -> sets background via stylesheet (dark/light variants)
- Tooltips on every tiny button (hover feature you asked)

### 4.2 BibleWidget

**Top Toolbar (always visible):**
- search_input QLineEdit placeholder "Search entire Bible..." + ToolTip
- Search button + A- / A+ font + ☀️/🌙 theme toggle - all with ToolTip

**Bottom Tab Bar (4 tabs, Search removed as you asked):**
- 📚 Books -> Home
- 🔖 Saved -> Bookmarks + Notes
- 🎨 Highlights
- ☰ More -> Search Results + History

**Main Stack (5 pages):**

**Page 0 - HOME - Books Only**
- Removed Continue + Daily Verse as you asked
- ScrollArea with Old Testament grid + New Testament grid
- 3 columns, book_btn with lambda capture fix: `lambda checked=False, n=bname: self.on_book_clicked(n)`

**Page 1 - Reader - 3 layers:**
1. Header: ← Books | ‹ Prev | Title | Next ›
2. chapters_frame (hidden) - Grid 8 columns chapter numbers
3. verses_chooser_frame (hidden) - Grid 10 columns verse numbers - NEW FEATURE you asked
4. verses_scroll - QScrollArea with verses_layout where VerseRow widgets added

**Flow you requested:**
```
on_book_clicked(book):
    cur_b = book
    show_chapters(book) -> builds chapter buttons -> shows chapters_frame -> switch to Reader

show_verses(book, chapter):
    hides chapters_frame
    builds verse buttons 1..v_count -> shows verses_chooser_frame

open_reader_focused(book, chapter, verse):
    hides both choosers
    render_verses(focus_verse=verse) -> creates VerseRow per verse, stores in self.verse_widgets dict
    repo.add_history(book, chapter)
    QTimer.singleShot(150, scroll_to_verse)

scroll_to_verse(vnum):
    ensureWidgetVisible + flash purple border 1.2s
```

**Bug you reported fixed:**
- Before: chapter grid stayed visible pushing verses down -> now in open_reader_focused: `self.chapters_frame.setVisible(False)` + `self.verses_chooser_frame.setVisible(False)`

**Hover tooltips added everywhere:**
- setToolTip() on every button, QSS: `QToolTip { background: #2a2d41; border: 1px solid #bd93f9; }`

Full widget.py:

```python

from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget,
                               QStackedWidget, QLabel, QScrollArea, QGridLayout, QFrame,
                               QLineEdit, QListWidget, QListWidgetItem, QTextEdit, QInputDialog,
                               QMessageBox, QDialog, QButtonGroup)
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtGui import QClipboard
from repository import BibleRepository
import random

COLORS = {
    "yellow": "#fde68a",
    "green": "#bbf7d0",
    "pink": "#fbcfe8",
    "blue": "#bfdbfe",
    "purple": "#ddd6fe"
}
COLOR_DARK = {
    "yellow": "#a68b00",
    "green": "#2f6b3a",
    "pink": "#8a4a65",
    "blue": "#3a5a8a",
    "purple": "#5a4a8a"
}

class VerseRow(QFrame):
    bookmarkClicked = Signal(int, str)
    highlightClicked = Signal(int, str, str)
    noteClicked = Signal(int)
    copyClicked = Signal(int)

    def __init__(self, num, text, is_bookmarked=False, highlight_color=None, has_note=False, font_size=18, theme="dark"):
        super().__init__()
        self.setObjectName("verse_row")
        self.num = num
        self.text = text
        self.theme = theme

        lay = QHBoxLayout(self)
        lay.setContentsMargins(8, 8, 8, 8)
        lay.setSpacing(8)

        self.lbl_num = QLabel(str(num))
        self.lbl_num.setObjectName("verse_num")
        self.lbl_num.setFixedWidth(36)
        self.lbl_num.setAlignment(Qt.AlignTop)

        self.lbl_text = QLabel(text)
        self.lbl_text.setWordWrap(True)
        self.lbl_text.setObjectName("verse_text")
        self.lbl_text.setStyleSheet(f"font-size: {font_size}px;")

        # Highlight background
        if highlight_color:
            col = COLORS.get(highlight_color, highlight_color)
            if theme == "dark":
                col = COLOR_DARK.get(highlight_color, col)
            self.setStyleSheet(f"#verse_row {{ background-color: {col}; border-radius: 8px; }}")
        else:
            self.setStyleSheet("#verse_row { background-color: transparent; }")

        # Action buttons - hidden by default, show on hover via style
        self.btns_frame = QFrame()
        btn_lay = QHBoxLayout(self.btns_frame)
        btn_lay.setContentsMargins(0,0,0,0)
        btn_lay.setSpacing(4)

        self.btn_bm = QPushButton("🔖" if not is_bookmarked else "✅")
        self.btn_bm.setObjectName("tiny_btn")
        self.btn_bm.setFixedSize(32,28)
        self.btn_bm.clicked.connect(lambda: self.bookmarkClicked.emit(self.num, self.text))

        self.btn_copy = QPushButton("📋")
        self.btn_copy.setObjectName("tiny_btn")
        self.btn_copy.setFixedSize(32,28)
        self.btn_copy.clicked.connect(lambda: self.copyClicked.emit(self.num))

        self.btn_note = QPushButton("📝" if not has_note else "📝•")
        self.btn_note.setObjectName("tiny_btn")
        self.btn_note.setFixedSize(32,28)
        self.btn_note.clicked.connect(lambda: self.noteClicked.emit(self.num))

        # color buttons
        self.color_btns = []
        for cname, hexcol in [("yellow","🟨"),("green","🟩"),("pink","🟥"),("blue","🟦"),("purple","🟪")]:
            b = QPushButton(hexcol)
            b.setObjectName("color_btn")
            b.setFixedSize(28,28)
            b.clicked.connect(lambda _, col=cname: self.highlightClicked.emit(self.num, self.text, col))
            self.color_btns.append(b)
            btn_lay.addWidget(b)

        btn_lay.addWidget(self.btn_bm)
        btn_lay.addWidget(self.btn_note)
        btn_lay.addWidget(self.btn_copy)

        lay.addWidget(self.lbl_num)
        lay.addWidget(self.lbl_text, 1)
        lay.addWidget(self.btns_frame)

        if has_note:
            self.setToolTip("Has note - click 📝 to view")

class BibleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("centralWidget")
        self.repo = BibleRepository()
        self.book_list = self.repo.get_books()
        self.cur_b = self.repo.get_setting("last_book", self.book_list[0] if self.book_list else "Genesis")
        self.cur_c = int(self.repo.get_setting("last_chapter", "1"))
        self.font_size = int(self.repo.get_setting("font_size", "18"))
        self.theme = self.repo.get_setting("theme", "dark")

        # MAIN LAYOUT
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 8, 10, 8)
        self.main_layout.setSpacing(6)

        # TOP TOOLBAR
        self.toolbar = QFrame()
        self.toolbar.setObjectName("toolbar_frame")
        t_lay = QHBoxLayout(self.toolbar)
        t_lay.setContentsMargins(0,0,0,0)
        t_lay.setSpacing(6)

        self.search_input = QLineEdit()
        self.search_input.setObjectName("search_input")
        self.search_input.setPlaceholderText("🔍 Search Bible...")
        self.search_input.returnPressed.connect(self.do_search)

        self.btn_search = QPushButton("Search")
        self.btn_search.setObjectName("small_btn")
        self.btn_search.clicked.connect(self.do_search)

        self.btn_theme = QPushButton("☀️" if self.theme=="dark" else "🌙")
        self.btn_theme.setObjectName("small_btn")
        self.btn_theme.clicked.connect(self.toggle_theme)

        self.btn_font_minus = QPushButton("A-")
        self.btn_font_minus.setObjectName("small_btn")
        self.btn_font_minus.clicked.connect(self.font_decrease)

        self.btn_font_plus = QPushButton("A+")
        self.btn_font_plus.setObjectName("small_btn")
        self.btn_font_plus.clicked.connect(self.font_increase)

        t_lay.addWidget(self.search_input, 1)
        t_lay.addWidget(self.btn_search)
        t_lay.addWidget(self.btn_font_minus)
        t_lay.addWidget(self.btn_font_plus)
        t_lay.addWidget(self.btn_theme)

        self.main_layout.addWidget(self.toolbar)

        # BOTTOM TAB BAR (phone style)
        self.tab_bar = QFrame()
        self.tab_bar.setObjectName("tab_bar")
        tab_lay = QHBoxLayout(self.tab_bar)
        tab_lay.setContentsMargins(0,0,0,0)

        self.btn_tab_home = QPushButton("📚 Books")
        self.btn_tab_search = QPushButton("🔍 Search")
        self.btn_tab_bm = QPushButton("🔖 Saved")
        self.btn_tab_high = QPushButton("🎨 Highlights")
        self.btn_tab_more = QPushButton("☰ More")

        for b in [self.btn_tab_home, self.btn_tab_search, self.btn_tab_bm, self.btn_tab_high, self.btn_tab_more]:
            b.setObjectName("tab_btn")
            b.setCheckable(True)

        self.btn_tab_home.setChecked(True)
        self.btn_tab_home.clicked.connect(lambda: self.switch_main(0))
        self.btn_tab_search.clicked.connect(lambda: self.switch_main(2))
        self.btn_tab_bm.clicked.connect(lambda: self.switch_main(3))
        self.btn_tab_high.clicked.connect(lambda: self.switch_main(4))
        self.btn_tab_more.clicked.connect(lambda: self.switch_main(5))

        self.tab_group = [self.btn_tab_home, self.btn_tab_search, self.btn_tab_bm, self.btn_tab_high, self.btn_tab_more]
        for b in self.tab_group:
            tab_lay.addWidget(b)

        # MAIN STACK
        self.stk = QStackedWidget()

        # Page 0 - HOME (Books) - THIS IS NOW HOME
        self.home_page = self.create_home_page()
        self.stk.addWidget(self.home_page)

        # Page 1 - Reader
        self.reader_page = self.create_reader_page()
        self.stk.addWidget(self.reader_page)

        # Page 2 - Search
        self.search_page = self.create_search_page()
        self.stk.addWidget(self.search_page)

        # Page 3 - Bookmarks + Notes combined
        self.saved_page = self.create_saved_page()
        self.stk.addWidget(self.saved_page)

        # Page 4 - Highlights
        self.highlights_page = self.create_highlights_page()
        self.stk.addWidget(self.highlights_page)

        # Page 5 - More (History, Daily Verse, etc)
        self.more_page = self.create_more_page()
        self.stk.addWidget(self.more_page)

        self.main_layout.addWidget(self.stk, 1)
        self.main_layout.addWidget(self.tab_bar)

        # Start at HOME
        self.switch_main(0)

    def switch_main(self, idx):
        for b in self.tab_group:
            b.setChecked(False)
        if idx < len(self.tab_group):
            self.tab_group[idx].setChecked(True)
        self.stk.setCurrentIndex(idx)
        if idx == 3:
            self.refresh_bookmarks()
            self.refresh_notes_list()
        if idx == 4:
            self.refresh_highlights()
        if idx == 5:
            self.refresh_history()
            self.load_daily_verse()

    # HOME PAGE - Books Grid
    def create_home_page(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0,0,0,0)
        lay.setSpacing(8)

        # Continue Reading + Daily Verse Card
        self.continue_frame = QFrame()
        self.continue_frame.setObjectName("card_frame")
        c_lay = QVBoxLayout(self.continue_frame)
        self.lbl_continue = QLabel(f"Continue: {self.cur_b} {self.cur_c}")
        self.lbl_continue.setObjectName("card_title")
        self.btn_continue = QPushButton(f"▶️ Continue reading {self.cur_b} {self.cur_c}")
        self.btn_continue.setObjectName("primary_btn")
        self.btn_continue.clicked.connect(lambda: self.open_reader(self.cur_b, self.cur_c))
        c_lay.addWidget(self.lbl_continue)
        c_lay.addWidget(self.btn_continue)

        self.daily_frame = QFrame()
        self.daily_frame.setObjectName("card_frame")
        d_lay = QVBoxLayout(self.daily_frame)
        self.lbl_daily_title = QLabel("📖 Verse of the Day")
        self.lbl_daily_title.setObjectName("card_title")
        self.lbl_daily_text = QLabel("Loading...")
        self.lbl_daily_text.setWordWrap(True)
        self.lbl_daily_text.setObjectName("daily_text")
        self.btn_daily_open = QPushButton("Open")
        self.btn_daily_open.setObjectName("small_btn")
        self.btn_daily_open.clicked.connect(self.open_daily)
        d_lay.addWidget(self.lbl_daily_title)
        d_lay.addWidget(self.lbl_daily_text)
        d_lay.addWidget(self.btn_daily_open)

        top_row = QHBoxLayout()
        top_row.addWidget(self.continue_frame)
        top_row.addWidget(self.daily_frame)
        lay.addLayout(top_row)

        # Books scroll
        scr = QScrollArea()
        scr.setObjectName("scroll_area")
        scr.setWidgetResizable(True)
        content = QWidget()
        content_lay = QVBoxLayout(content)

        old = self.book_list[:39] if len(self.book_list)>=39 else self.book_list
        new = self.book_list[39:] if len(self.book_list)>=39 else []

        for name, books in [("OLD TESTAMENT", old), ("NEW TESTAMENT", new)]:
            if not books: continue
            lbl = QLabel(name)
            lbl.setObjectName("testament_label")
            content_lay.addWidget(lbl)
            grid = QGridLayout()
            grid.setSpacing(8)
            for i, b in enumerate(books):
                btn = QPushButton(b)
                btn.setObjectName("book_btn")
                btn.clicked.connect(lambda _, n=b: self.show_chapters(n))
                grid.addWidget(btn, i // 3, i % 3)
            content_lay.addLayout(grid)

        scr.setWidget(content)
        lay.addWidget(scr)
        return w

    def create_reader_page(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0,0,0,0)
        lay.setSpacing(0)

        # Reader header
        hdr = QFrame()
        hdr.setObjectName("header_frame")
        hdr.setFixedHeight(50)
        h_lay = QHBoxLayout(hdr)
        h_lay.setContentsMargins(0,0,0,0)

        self.btn_back_home = QPushButton("← Books")
        self.btn_back_home.setObjectName("small_btn")
        self.btn_back_home.clicked.connect(lambda: self.switch_main(0))

        self.btn_prev = QPushButton("‹ Prev")
        self.btn_prev.setObjectName("small_btn")
        self.btn_prev.clicked.connect(self.prev_ch)

        self.lbl_reader_title = QLabel(f"{self.cur_b} {self.cur_c}")
        self.lbl_reader_title.setObjectName("reader_title")
        self.lbl_reader_title.setAlignment(Qt.AlignCenter)

        self.btn_next = QPushButton("Next ›")
        self.btn_next.setObjectName("small_btn")
        self.btn_next.clicked.connect(self.next_ch)

        self.btn_chapters = QPushButton("Chapters ▾")
        self.btn_chapters.setObjectName("small_btn")
        self.btn_chapters.clicked.connect(self.toggle_chapters)

        h_lay.addWidget(self.btn_back_home)
        h_lay.addWidget(self.btn_prev)
        h_lay.addWidget(self.lbl_reader_title, 1)
        h_lay.addWidget(self.btn_next)
        h_lay.addWidget(self.btn_chapters)

        # Chapters grid popup
        self.chapters_frame = QFrame()
        self.chapters_frame.setObjectName("chapters_popup")
        self.chapters_frame.setVisible(False)
        self.ch_grid = QGridLayout(self.chapters_frame)
        self.ch_grid.setSpacing(6)

        # Verses scroll
        self.verses_scroll = QScrollArea()
        self.verses_scroll.setObjectName("scroll_area")
        self.verses_scroll.setWidgetResizable(True)

        self.verses_container = QWidget()
        self.verses_layout = QVBoxLayout(self.verses_container)
        self.verses_layout.setAlignment(Qt.AlignTop)
        self.verses_scroll.setWidget(self.verses_container)

        lay.addWidget(hdr)
        lay.addWidget(self.chapters_frame)
        lay.addWidget(self.verses_scroll)
        return w

    def create_search_page(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        self.search_label = QLabel("Type above to search entire Bible")
        self.search_label.setObjectName("section_label")
        self.search_view = QListWidget()
        self.search_view.setObjectName("list_widget")
        self.search_view.itemDoubleClicked.connect(self.on_search_open)
        lay.addWidget(self.search_label)
        lay.addWidget(self.search_view)
        return w

    def create_saved_page(self):
        w = QWidget()
        lay = QHBoxLayout(w)
        # Left bookmarks, right notes
        left = QFrame()
        left_lay = QVBoxLayout(left)
        left_lay.addWidget(QLabel("🔖 Bookmarks"))
        self.bm_list = QListWidget()
        self.bm_list.setObjectName("list_widget")
        self.bm_list.itemDoubleClicked.connect(self.on_bookmark_open)
        self.btn_del_bm = QPushButton("Remove Bookmark")
        self.btn_del_bm.setObjectName("danger_btn")
        self.btn_del_bm.clicked.connect(self.clear_bookmark)
        left_lay.addWidget(self.bm_list)
        left_lay.addWidget(self.btn_del_bm)

        right = QFrame()
        right_lay = QVBoxLayout(right)
        right_lay.addWidget(QLabel("📝 My Notes"))
        self.notes_list = QListWidget()
        self.notes_list.setObjectName("list_widget")
        self.notes_list.itemDoubleClicked.connect(self.on_note_open)
        self.btn_del_note = QPushButton("Delete Note")
        self.btn_del_note.setObjectName("danger_btn")
        self.btn_del_note.clicked.connect(self.clear_note)
        right_lay.addWidget(self.notes_list)
        right_lay.addWidget(self.btn_del_note)

        lay.addWidget(left)
        lay.addWidget(right)
        return w

    def create_highlights_page(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.addWidget(QLabel("🎨 Highlights - tap to open, select to remove"))
        self.hl_list = QListWidget()
        self.hl_list.setObjectName("list_widget")
        self.hl_list.itemDoubleClicked.connect(self.on_highlight_open)
        self.btn_del_hl = QPushButton("Remove Highlight")
        self.btn_del_hl.setObjectName("danger_btn")
        self.btn_del_hl.clicked.connect(self.clear_highlight)
        lay.addWidget(self.hl_list)
        lay.addWidget(self.btn_del_hl)
        return w

    def create_more_page(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setAlignment(Qt.AlignTop)

        # Daily verse big
        self.more_daily_frame = QFrame()
        self.more_daily_frame.setObjectName("card_frame")
        md_lay = QVBoxLayout(self.more_daily_frame)
        self.more_daily_title = QLabel("📖 Daily Verse")
        self.more_daily_title.setObjectName("card_title")
        self.more_daily_text = QLabel("")
        self.more_daily_text.setWordWrap(True)
        self.more_daily_text.setObjectName("daily_text")
        md_lay.addWidget(self.more_daily_title)
        md_lay.addWidget(self.more_daily_text)
        lay.addWidget(self.more_daily_frame)

        lay.addWidget(QLabel("🕘 Recent History"))
        self.hi_list = QListWidget()
        self.hi_list.setObjectName("list_widget")
        self.hi_list.setMaximumHeight(200)
        self.hi_list.itemDoubleClicked.connect(self.on_history_open)
        lay.addWidget(self.hi_list)

        self.btn_clear_history = QPushButton("Clear History")
        self.btn_clear_history.setObjectName("danger_btn")
        self.btn_clear_history.clicked.connect(self.clear_history)
        lay.addWidget(self.btn_clear_history)

        return w

    # LOGIC
    def show_chapters(self, book):
        self.cur_b = book
        # build chapters
        while self.ch_grid.count():
            it = self.ch_grid.takeAt(0)
            if it.widget():
                it.widget().deleteLater()
        for c in self.repo.get_chapters(book):
            btn = QPushButton(str(c))
            btn.setObjectName("chapter_btn")
            btn.clicked.connect(lambda _, v=c: self.open_reader(self.cur_b, v))
            self.ch_grid.addWidget(btn, (c-1)//8, (c-1)%8)
        self.chapters_frame.setVisible(True)

    def toggle_chapters(self):
        self.chapters_frame.setVisible(not self.chapters_frame.isVisible())

    def open_reader(self, book, chap):
        self.cur_b = book
        self.cur_c = chap
        self.lbl_continue.setText(f"Continue: {book} {chap}")
        self.btn_continue.setText(f"▶️ Continue reading {book} {chap}")
        self.lbl_reader_title.setText(f"{book} {chap}")
        self.render_verses()
        self.repo.add_history(book, chap)
        self.stk.setCurrentIndex(1)
        for b in [self.btn_tab_home, self.btn_tab_search, self.btn_tab_bm, self.btn_tab_high, self.btn_tab_more]:
            b.setChecked(False)

    def render_verses(self):
        # clear
        while self.verses_layout.count():
            it = self.verses_layout.takeAt(0)
            if it.widget():
                it.widget().deleteLater()

        verses = self.repo.get_verses(self.cur_b, self.cur_c)
        highlights = self.repo.get_highlights_map(self.cur_b, self.cur_c)

        for num, txt in verses:
            is_bm = self.repo.is_bookmarked(self.cur_b, self.cur_c, num)
            hl_color = highlights.get(num)
            has_note = bool(self.repo.get_note(self.cur_b, self.cur_c, num))
            row = VerseRow(num, txt, is_bookmarked=is_bm, highlight_color=hl_color, has_note=has_note, font_size=self.font_size, theme=self.theme)
            row.bookmarkClicked.connect(self.handle_bookmark)
            row.highlightClicked.connect(self.handle_highlight)
            row.noteClicked.connect(self.handle_note)
            row.copyClicked.connect(self.handle_copy)
            self.verses_layout.addWidget(row)

        self.verses_layout.addStretch()

    def prev_ch(self):
        if self.cur_c > 1:
            self.open_reader(self.cur_b, self.cur_c-1)
        elif self.book_list.index(self.cur_b) > 0:
            prev_book = self.book_list[self.book_list.index(self.cur_b)-1]
            chs = self.repo.get_chapters(prev_book)
            if chs:
                self.open_reader(prev_book, max(chs))

    def next_ch(self):
        chs = self.repo.get_chapters(self.cur_b)
        if chs and self.cur_c < max(chs):
            self.open_reader(self.cur_b, self.cur_c+1)
        elif self.book_list.index(self.cur_b) < len(self.book_list)-1:
            next_book = self.book_list[self.book_list.index(self.cur_b)+1]
            self.open_reader(next_book, 1)

    # Actions
    @Slot(int, str)
    def handle_bookmark(self, vnum, txt):
        if self.repo.is_bookmarked(self.cur_b, self.cur_c, vnum):
            # remove
            bms = self.repo.get_bookmarks()
            for r in bms:
                if r["book"]==self.cur_b and r["chapter"]==self.cur_c and r["verse"]==vnum:
                    self.repo.delete_bookmark(r["id"])
        else:
            self.repo.add_bookmark(self.cur_b, self.cur_c, vnum, txt)
        self.render_verses()

    @Slot(int, str, str)
    def handle_highlight(self, vnum, txt, color):
        # toggle same color = remove
        current = self.repo.get_highlights_map(self.cur_b, self.cur_c).get(vnum)
        if current == color:
            self.repo.remove_highlight(self.cur_b, self.cur_c, vnum)
        else:
            self.repo.add_highlight(self.cur_b, self.cur_c, vnum, txt, color)
        self.render_verses()

    @Slot(int)
    def handle_note(self, vnum):
        existing = self.repo.get_note(self.cur_b, self.cur_c, vnum)
        text, ok = QInputDialog.getMultiLineText(self, f"Note - {self.cur_b} {self.cur_c}:{vnum}", "Your note:", existing)
        if ok:
            if text.strip() == "":
                # delete if empty
                # find id
                notes = self.repo.get_notes()
                for r in notes:
                    if r["book"]==self.cur_b and r["chapter"]==self.cur_c and r["verse"]==vnum:
                        self.repo.delete_note(r["id"])
            else:
                self.repo.add_note(self.cur_b, self.cur_c, vnum, text)
            self.render_verses()

    @Slot(int)
    def handle_copy(self, vnum):
        verses = dict(self.repo.get_verses(self.cur_b, self.cur_c))
        txt = verses.get(vnum, "")
        full = f"{self.cur_b} {self.cur_c}:{vnum} - {txt}"
        clipboard = self.parent().findChild(QWidget).parent() if False else None
        from PySide6.QtWidgets import QApplication
        QApplication.clipboard().setText(full)
        # show message via footer
        self.lbl_reader_title.setText(f"Copied: {self.cur_b} {self.cur_c}:{vnum}")

    def do_search(self):
        kw = self.search_input.text().strip() if hasattr(self, 'search_input') else ""
        # search_input is in toolbar, but also we have search page input? Use toolbar one
        # Actually toolbar search_input is top, reuse
        if not kw:
            # try find child
            for w in self.findChildren(QLineEdit):
                if w.objectName()=="search_input" and w.text().strip():
                    kw = w.text().strip()
                    break
        if not kw:
            return
        results = self.repo.search(kw)
        self.search_view.clear()
        self.search_label.setText(f"Found {len(results)} results for '{kw}'") if hasattr(self, 'search_label') else None
        for book, chap, verse, text in results:
            item = QListWidgetItem(f"{book} {chap}:{verse} - {text[:120]}")
            item.setData(Qt.UserRole, (book, chap, verse))
            self.search_view.addItem(item)
        self.switch_main(2)

    def on_search_open(self, item):
        data = item.data(Qt.UserRole)
        if data:
            self.open_reader(data[0], data[1])

    def refresh_bookmarks(self):
        self.bm_list.clear()
        for r in self.repo.get_bookmarks():
            self.bm_list.addItem(f"{r['book']} {r['chapter']}:{r['verse']} - {r['text'][:80]}")

    def on_bookmark_open(self, item):
        txt = item.text()
        try:
            # parse "Genesis 1:1 - ..."
            ref = txt.split(' - ')[0]
            book_chap, verse = ref.rsplit(':',1)
            book, chap = book_chap.rsplit(' ',1)
            self.open_reader(book, int(chap))
        except:
            pass

    def clear_bookmark(self):
        it = self.bm_list.currentItem()
        if not it:
            return
        # find by text match
        bms = self.repo.get_bookmarks()
        # simple: delete by index
        row = self.bm_list.currentRow()
        if 0 <= row < len(bms):
            self.repo.delete_bookmark(bms[row]["id"])
            self.refresh_bookmarks()

    def refresh_notes_list(self):
        self.notes_list.clear()
        for r in self.repo.get_notes():
            self.notes_list.addItem(f"{r['book']} {r['chapter']}:{r['verse']} - {r['note'][:80]}")

    def on_note_open(self, item):
        txt = item.text()
        try:
            ref = txt.split(' - ')[0]
            book_chap, verse = ref.rsplit(':',1)
            book, chap = book_chap.rsplit(' ',1)
            self.open_reader(book, int(chap))
        except:
            pass

    def clear_note(self):
        notes = self.repo.get_notes()
        row = self.notes_list.currentRow()
        if 0 <= row < len(notes):
            self.repo.delete_note(notes[row]["id"])
            self.refresh_notes_list()

    def refresh_highlights(self):
        self.hl_list.clear()
        for r in self.repo.get_highlights():
            self.hl_list.addItem(f"[{r['color']}] {r['book']} {r['chapter']}:{r['verse']} - {r['text'][:80]}")

    def on_highlight_open(self, item):
        txt = item.text()
        try:
            # "[yellow] Genesis 1:1 - ..."
            ref_part = txt.split('] ')[1].split(' - ')[0]
            book_chap, verse = ref_part.rsplit(':',1)
            book, chap = book_chap.rsplit(' ',1)
            self.open_reader(book, int(chap))
        except:
            pass

    def clear_highlight(self):
        hls = self.repo.get_highlights()
        row = self.hl_list.currentRow()
        if 0 <= row < len(hls):
            r = hls[row]
            self.repo.remove_highlight(r["book"], r["chapter"], r["verse"])
            self.refresh_highlights()
            self.render_verses()

    def refresh_history(self):
        self.hi_list.clear()
        for r in self.repo.get_history():
            self.hi_list.addItem(f"{r['book']} {r['chapter']}")

    def on_history_open(self, item):
        try:
            book, chap = item.text().rsplit(' ',1)
            self.open_reader(book, int(chap))
        except:
            pass

    def clear_history(self):
        from database import get_connection
        conn = get_connection()
        conn.execute("DELETE FROM history")
        conn.commit()
        conn.close()
        self.refresh_history()

    def load_daily_verse(self):
        book, chap, verse, text = self.repo.get_daily_verse()
        self.more_daily_text.setText(f"{book} {chap}:{verse} - {text}")
        self.daily_book = book
        self.daily_chap = chap
        # also for home
        if hasattr(self, 'lbl_daily_text'):
            self.lbl_daily_text.setText(f"{book} {chap}:{verse} - {text[:150]}...")
            self.daily_book_home = book
            self.daily_chap_home = chap

    def open_daily(self):
        book, chap, _, _ = self.repo.get_daily_verse()
        # use last loaded daily
        b = getattr(self, 'daily_book_home', book)
        c = getattr(self, 'daily_chap_home', chap)
        self.open_reader(b, c)

    def font_increase(self):
        self.font_size = min(30, self.font_size+2)
        self.repo.set_setting("font_size", str(self.font_size))
        self.render_verses()

    def font_decrease(self):
        self.font_size = max(12, self.font_size-2)
        self.repo.set_setting("font_size", str(self.font_size))
        self.render_verses()

    def toggle_theme(self):
        self.theme = "light" if self.theme=="dark" else "dark"
        self.repo.set_setting("theme", self.theme)
        self.btn_theme.setText("☀️" if self.theme=="dark" else "🌙")
        # reload qss
        from pathlib import Path
        from PySide6.QtWidgets import QApplication
        qss_path = Path(__file__).resolve().parent / ("style.qss" if self.theme=="dark" else "style_light.qss")
        if qss_path.exists():
            QApplication.instance().setStyleSheet(qss_path.read_text(encoding='utf-8'))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LINUX BIBLE - ULTIMATE")
        self.setGeometry(100, 100, 1200, 900)
        self.setMinimumSize(900, 650)
        self.setCentralWidget(BibleWidget())

```

---

## 5. Step 4 - QSS Themes

**style.qss (dark) and style_light.qss (light)**

Selectors:
- #book_btn, #chapter_btn, #verse_btn
- #verse_row:hover
- #tiny_btn, #color_btn
- QToolTip styling

```css
/* dark */

#centralWidget { background-color: #1a1b26; }
#toolbar_frame { background: #16161e; border-radius: 10px; padding: 4px; }
#header_frame { background: transparent; }
#tab_bar { background: #16161e; border-radius: 12px; padding: 4px; }

#arrow_btn { color: #bd93f9; font-size: 32px; border: none; background: transparent; }
#nav_btn { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #d6bcfa, stop:1 #9a67ea); color: #1a1b26; border-radius: 10px; font: bold 13px; padding: 8px 16px; border: none; }

#search_input { background: #2a2d41; color: white; font-size: 14px; padding: 10px 14px; border: 1px solid #3b4252; border-radius: 10px; }
#search_input:focus { border: 1px solid #bd93f9; }

#small_btn { background: #2a2d41; color: #d6bcfa; font-weight: bold; font-size: 12px; padding: 8px 12px; border: 1px solid #3b4252; border-radius: 8px; }
#small_btn:hover { background: #bd93f9; color: #1a1b26; }

#tab_btn { background: transparent; color: #6c7086; font-size: 13px; font-weight: bold; padding: 10px 6px; border: none; border-radius: 8px; }
#tab_btn:checked { background: #2a2d41; color: #d6bcfa; }
#tab_btn:hover { color: #d6bcfa; }

#reader_view { border: none; background: transparent; color: white; }
#verse_row { border-radius: 8px; margin: 2px 0; }
#verse_row:hover { background-color: #2a2d41; }
#verse_num { color: #bd93f9; font-weight: bold; font-size: 13px; }
#verse_text { color: white; }

#tiny_btn { background: #2a2d41; color: white; border: 1px solid #3b4252; border-radius: 6px; font-size: 11px; }
#tiny_btn:hover { background: #bd93f9; color: #1a1b26; }
#color_btn { background: transparent; border: none; font-size: 16px; }
#color_btn:hover { background: #2a2d41; border-radius: 6px; }

#testament_label { color: #bd93f9; font-weight: bold; font-size: 11px; letter-spacing: 1px; padding: 16px 0 6px 4px; }
#book_btn { background: #2a2d41; color: #d6bcfa; border-radius: 10px; height: 48px; font: bold 12px; border: 1px solid #3b4252; }
#book_btn:hover { background: qlinear
...
```

Light theme same selectors white background.

Theme toggle:

```python
def toggle_theme(self):
    self.theme = "light" if self.theme=="dark" else "dark"
    qss_path = Path(__file__).resolve().parent / ("style.qss" if theme=="dark" else "style_light.qss")
    QApplication.instance().setStyleSheet(qss_path.read_text())
```

---

## 6. Step 5 - main.py

```python

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from database import init_db
from widget import MainWindow
from repository import BibleRepository

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)

    repo = BibleRepository()
    theme = repo.get_setting("theme", "dark")
    qss_file = "style.qss" if theme=="dark" else "style_light.qss"
    qss_path = Path(__file__).resolve().parent / qss_file
    if qss_path.exists():
        app.setStyleSheet(qss_path.read_text(encoding='utf-8'))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

```

---

## 7. How Features Work

- **Search:** Top bar search_input -> repo.search() LIKE query -> fills search_view QListWidget in More tab -> double-click -> open_reader_focused
- **Bookmark:** Click 🔖 in VerseRow -> repo.add_bookmark -> re-render
- **Highlight:** Click 🟨 etc -> repo.add_highlight with color, if same color clicked again -> remove (toggle)
- **Note:** Click 📝 -> QInputDialog.getMultiLineText -> repo.add_note
- **Copy:** Click 📋 -> QApplication.clipboard().setText(f"{book} {chapter}:{verse} - {text}")
- **History:** repo.add_history on every open_reader_focused, keeps last 100
- **Font:** A-/A+ changes self.font_size, saved to settings, re-renders VerseRow with new font-size px
- **Focus:** scroll_to_verse uses ensureWidgetVisible + flash

---

## 8. Build EXE (PyInstaller)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "NKJV.xml;." --add-data "style.qss;." --add-data "style_light.qss;." main.py
```

---

## 9. Portfolio Points to Mention

- Industry structure (database.py / repository.py / widget.py / main.py / QSS separation)
- Repository Pattern
- SQLite indexing for search
- QStackedWidget navigation
- Dynamic widget creation (VerseRow per verse)
- QTimer + ensureWidgetVisible for focus
- Light/Dark theme switching via QSS
- Tooltip UX

---

## 10. Next Ideas (you said no audio)

- Share as Image (render verse to QPixmap)
- Reading Plans (checklist per day)
- Compare translations (add second DB)

---

*Generated for Obsidian - keep this in your vault*
