# LINUX BIBLE ULTIMATE - Exact Zip Build


```
README.md
database.py
main.py
repository.py
style.qss
style_light.qss
widget.py
```

Each file below is separated into its own section as it is in the zip. Copy each file as named.

---

## README.md

```markdown

# LINUX BIBLE ULTIMATE - Phone features, no audio

HOME = Books instantly (Old/New Testament grid) - no Genesis auto-open

Features:
- 📚 Home: Old/New Testament grid, Continue Reading, Verse of Day
- 📖 Reader: Verse rows with own buttons: Bookmark, Note, Copy, Highlight colors (yellow/green/pink/blue/purple)
- Click verse number row to see options. Highlight persists with color in bible.db
- 🔍 Search: full text LIKE search, 400 limit, click to jump
- 🔖 Saved: left Bookmarks, right Notes (add note via 📝 button, prompts input)
- 🎨 Highlights: all highlights list, color shown
- ☰ More: Daily Verse random, History (30), Clear History, Theme toggle
- Aa Font +/- saved to settings table
- Light/Dark theme toggle ☀️/🌙 - style.qss and style_light.qss
- Copy verse copies "Book Chapter:Verse - text" to clipboard
- DB tables: verses, bookmarks, highlights, notes, history, settings

How to run:
pip install PySide6
Put NKJV.xml in folder (if no bible.db yet)
python main.py

First run builds bible.db

```


---

## database.py

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

---

## main.py

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

## repository.py

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

## style.qss

```css

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
#book_btn:hover { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #d6bcfa, stop:1 #9a67ea); color: #1a1b26; }

#chapter_btn { background: #2a2d41; color: white; border-radius: 8px; height: 44px; font: bold 13px; border: 1px solid #3b4252; }
#chapter_btn:hover { background: #bd93f9; color: #1a1b26; }

#card_frame { background: #24283b; border: 1px solid #3b4252; border-radius: 12px; padding: 4px; }
#card_title { color: #d6bcfa; font-weight: bold; font-size: 13px; }
#daily_text { color: #a9b1d6; font-size: 13px; }
#primary_btn { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #d6bcfa, stop:1 #9a67ea); color: #1a1b26; border-radius: 8px; font: bold 12px; padding: 10px; border: none; }
#reader_title { color: white; font: bold 14px; }
#section_label { color: #d6bcfa; font-weight: bold; font-size: 13px; padding: 4px; }
#list_widget { background: #1e1e2e; color: white; font-size: 13px; border: 1px solid #3b4252; border-radius: 10px; padding: 4px; }
#list_widget::item { padding: 12px; border-radius: 8px; border-bottom: 1px solid #2a2d41; }
#list_widget::item:selected { background: #2a2d41; color: #d6bcfa; }

#danger_btn { background: #3a1f1f; color: #ff7a7a; font-weight: bold; padding: 10px; border: 1px solid #5a2a2a; border-radius: 8px; }
#chapters_popup { background: #24283b; border: 1px solid #3b4252; border-radius: 12px; padding: 8px; }

QScrollBar:vertical { border: none; background: transparent; width: 8px; }
QScrollBar::handle:vertical { background: #3b4252; min-height: 30px; border-radius: 4px; }
QScrollBar::handle:vertical:hover { background: #bd93f9; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }

#scroll_area { border: none; background: transparent; }

#verse_btn { background: #2a2d41; color: white; border-radius: 8px; height: 38px; font: bold 12px; border: 1px solid #3b4252; } #verse_btn:hover { background: #bd93f9; color: #1a1b26; }

```

---


## style_light.qss

```css

#centralWidget { background-color: #f5f5f7; }
#toolbar_frame { background: #ffffff; border-radius: 10px; padding: 4px; border: 1px solid #e5e7eb; }
#header_frame { background: transparent; }
#tab_bar { background: #ffffff; border-radius: 12px; padding: 4px; border: 1px solid #e5e7eb; }

#arrow_btn { color: #7c3aed; font-size: 32px; border: none; background: transparent; }
#nav_btn { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #8b5cf6, stop:1 #6d28d9); color: white; border-radius: 10px; font: bold 13px; padding: 8px 16px; border: none; }

#search_input { background: #ffffff; color: #111827; font-size: 14px; padding: 10px 14px; border: 1px solid #e5e7eb; border-radius: 10px; }
#search_input:focus { border: 1px solid #8b5cf6; }

#small_btn { background: #ffffff; color: #6d28d9; font-weight: bold; font-size: 12px; padding: 8px 12px; border: 1px solid #e5e7eb; border-radius: 8px; }
#small_btn:hover { background: #8b5cf6; color: white; }

#tab_btn { background: transparent; color: #6b7280; font-size: 13px; font-weight: bold; padding: 10px 6px; border: none; border-radius: 8px; }
#tab_btn:checked { background: #ede9fe; color: #6d28d9; }

#verse_row { border-radius: 8px; margin: 2px 0; }
#verse_row:hover { background-color: #ede9fe; }
#verse_num { color: #7c3aed; font-weight: bold; }
#verse_text { color: #111827; }

#tiny_btn { background: #ffffff; color: #111827; border: 1px solid #e5e7eb; border-radius: 6px; }
#tiny_btn:hover { background: #8b5cf6; color: white; }

#testament_label { color: #6d28d9; font-weight: bold; font-size: 11px; padding: 16px 0 6px 4px; }
#book_btn { background: #ffffff; color: #6d28d9; border-radius: 10px; height: 48px; font: bold 12px; border: 1px solid #e5e7eb; }
#book_btn:hover { background: #8b5cf6; color: white; }

#chapter_btn { background: #ffffff; color: #111827; border-radius: 8px; height: 44px; font: bold 13px; border: 1px solid #e5e7eb; }
#chapter_btn:hover { background: #8b5cf6; color: white; }

#card_frame { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 4px; }
#card_title { color: #6d28d9; font-weight: bold; }
#daily_text { color: #4b5563; }
#primary_btn { background: #6d28d9; color: white; border-radius: 8px; font: bold 12px; padding: 10px; border: none; }
#reader_title { color: #111827; font: bold 14px; }
#section_label { color: #6d28d9; font-weight: bold; }
#list_widget { background: #ffffff; color: #111827; border: 1px solid #e5e7eb; border-radius: 10px; }
#list_widget::item { padding: 12px; border-radius: 8px; border-bottom: 1px solid #f3f4f6; }
#list_widget::item:selected { background: #ede9fe; color: #6d28d9; }
#danger_btn { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; border-radius: 8px; padding: 10px; }
#chapters_popup { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 8px; }
QScrollBar:vertical { width: 8px; background: transparent; }
QScrollBar::handle:vertical { background: #d1d5db; border-radius: 4px; }
#scroll_area { border: none; background: transparent; }

#verse_btn { background: #2a2d41; color: white; border-radius: 8px; height: 38px; font: bold 12px; border: 1px solid #3b4252; } #verse_btn:hover { background: #bd93f9; color: #1a1b26; }

```

---

## widget.py

```python

from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget,
                               QStackedWidget, QLabel, QScrollArea, QGridLayout, QFrame,
                               QLineEdit, QListWidget, QListWidgetItem, QInputDialog)
from PySide6.QtCore import Qt, Slot, Signal, QTimer
from repository import BibleRepository

class VerseRow(QFrame):
    bookmarkClicked = Signal(int, str)
    highlightClicked = Signal(int, str, str)
    noteClicked = Signal(int)
    copyClicked = Signal(int)

    def __init__(self, num, text, is_bookmarked=False, highlight_color=None, has_note=False, font_size=18, theme="dark"):
        super().__init__()
        self.setObjectName(f"verse_{num}")
        self.num = num
        self.text = text

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

        # highlight
        if highlight_color:
            from pathlib import Path
            # simple colors
            col_map = {"yellow": "#fde68a", "green": "#bbf7d0", "pink": "#fbcfe8", "blue": "#bfdbfe", "purple": "#ddd6fe"}
            col_dark = {"yellow": "#665500", "green": "#2f6b3a", "pink": "#7a3a55", "blue": "#2a4a7a", "purple": "#4a3a7a"}
            col = col_dark.get(highlight_color, col_map.get(highlight_color, "#fde68a")) if theme=="dark" else col_map.get(highlight_color, "#fde68a")
            self.setStyleSheet(f"#verse_{num} {{ background-color: {col}; border-radius: 8px; }}")
        else:
            self.setStyleSheet(f"#verse_{num} {{ background-color: transparent; }}")

        self.btns_frame = QFrame()
        btn_lay = QHBoxLayout(self.btns_frame)
        btn_lay.setContentsMargins(0,0,0,0)
        btn_lay.setSpacing(4)

        self.btn_bm = QPushButton("✅" if is_bookmarked else "🔖")
        self.btn_bm.setObjectName("tiny_btn")
        self.btn_bm.setToolTip("Remove bookmark" if is_bookmarked else "Bookmark this verse")
        self.btn_bm.setFixedSize(32,28)
        self.btn_bm.clicked.connect(lambda: self.bookmarkClicked.emit(self.num, self.text))

        self.btn_copy = QPushButton("📋")
        self.btn_copy.setObjectName("tiny_btn")
        self.btn_copy.setToolTip("Copy verse to clipboard")
        self.btn_copy.setFixedSize(32,28)
        self.btn_copy.clicked.connect(lambda: self.copyClicked.emit(self.num))

        self.btn_note = QPushButton("📝•" if has_note else "📝")
        self.btn_note.setObjectName("tiny_btn")
        self.btn_note.setToolTip("Has note - click to view" if has_note else "Add note")
        self.btn_note.setFixedSize(32,28)
        self.btn_note.clicked.connect(lambda: self.noteClicked.emit(self.num))

        for cname, emoji, tip in [("yellow","🟨","Highlight Yellow"),("green","🟩","Highlight Green"),("pink","🟥","Highlight Pink"),("blue","🟦","Highlight Blue"),("purple","🟪","Highlight Purple")]:
            b = QPushButton(emoji)
            b.setObjectName("color_btn")
            b.setToolTip(tip)
            b.setFixedSize(28,28)
            b.clicked.connect(lambda _, col=cname: self.highlightClicked.emit(self.num, self.text, col))
            btn_lay.addWidget(b)

        btn_lay.addWidget(self.btn_bm)
        btn_lay.addWidget(self.btn_note)
        btn_lay.addWidget(self.btn_copy)

        lay.addWidget(self.lbl_num)
        lay.addWidget(self.lbl_text, 1)
        lay.addWidget(self.btns_frame)


class BibleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("centralWidget")
        self.repo = BibleRepository()
        self.book_list = self.repo.get_books()
        self.cur_b = self.repo.get_setting("last_book", self.book_list[0] if self.book_list else "Genesis")
        self.cur_c = int(self.repo.get_setting("last_chapter", "1"))
        self.cur_v = 1
        self.font_size = int(self.repo.get_setting("font_size", "18"))
        self.theme = self.repo.get_setting("theme", "dark")
        self.pending_chapter = None

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 8, 10, 8)
        self.main_layout.setSpacing(6)

        # TOP TOOLBAR with search
        self.toolbar = QFrame()
        self.toolbar.setObjectName("toolbar_frame")
        t_lay = QHBoxLayout(self.toolbar)
        t_lay.setContentsMargins(0,0,0,0)
        t_lay.setSpacing(6)

        self.search_input = QLineEdit()
        self.search_input.setObjectName("search_input")
        self.search_input.setPlaceholderText("🔍 Search entire Bible...")
        self.search_input.setToolTip("Type keyword and press Enter to search")
        self.search_input.returnPressed.connect(self.do_search)

        self.btn_search = QPushButton("Search")
        self.btn_search.setObjectName("small_btn")
        self.btn_search.setToolTip("Search entire Bible")
        self.btn_search.clicked.connect(self.do_search)

        self.btn_theme = QPushButton("☀️" if self.theme=="dark" else "🌙")
        self.btn_theme.setObjectName("small_btn")
        self.btn_theme.setToolTip("Toggle Light/Dark Theme")
        self.btn_theme.clicked.connect(self.toggle_theme)

        self.btn_font_minus = QPushButton("A-")
        self.btn_font_minus.setObjectName("small_btn")
        self.btn_font_minus.setToolTip("Decrease font size")
        self.btn_font_minus.clicked.connect(self.font_decrease)

        self.btn_font_plus = QPushButton("A+")
        self.btn_font_plus.setObjectName("small_btn")
        self.btn_font_plus.setToolTip("Increase font size")
        self.btn_font_plus.clicked.connect(self.font_increase)

        t_lay.addWidget(self.search_input, 1)
        t_lay.addWidget(self.btn_search)
        t_lay.addWidget(self.btn_font_minus)
        t_lay.addWidget(self.btn_font_plus)
        t_lay.addWidget(self.btn_theme)

        self.main_layout.addWidget(self.toolbar)

        # BOTTOM TAB BAR - NO SEARCH TAB NOW (only 4 tabs)
        self.tab_bar = QFrame()
        self.tab_bar.setObjectName("tab_bar")
        tab_lay = QHBoxLayout(self.tab_bar)
        tab_lay.setContentsMargins(0,0,0,0)

        self.btn_tab_home = QPushButton("📚 Books")
        self.btn_tab_home.setToolTip("Home - All Books")
        self.btn_tab_bm = QPushButton("🔖 Saved")
        self.btn_tab_bm.setToolTip("Bookmarks & Notes")
        self.btn_tab_high = QPushButton("🎨 Highlights")
        self.btn_tab_high.setToolTip("All Highlighted Verses")
        self.btn_tab_more = QPushButton("☰ More")
        self.btn_tab_more.setToolTip("History & Settings")

        for b in [self.btn_tab_home, self.btn_tab_bm, self.btn_tab_high, self.btn_tab_more]:
            b.setObjectName("tab_btn")
            b.setCheckable(True)

        self.btn_tab_home.setChecked(True)
        self.btn_tab_home.clicked.connect(lambda: self.switch_main(0))
        self.btn_tab_bm.clicked.connect(lambda: self.switch_main(2))
        self.btn_tab_high.clicked.connect(lambda: self.switch_main(3))
        self.btn_tab_more.clicked.connect(lambda: self.switch_main(4))

        self.tab_group = [self.btn_tab_home, self.btn_tab_bm, self.btn_tab_high, self.btn_tab_more]
        for b in self.tab_group:
            tab_lay.addWidget(b)

        # MAIN STACK
        self.stk = QStackedWidget()

        # Page 0 - HOME (Books ONLY - removed continue and daily)
        self.home_page = self.create_home_page()
        self.stk.addWidget(self.home_page)

        # Page 1 - Reader
        self.reader_page = self.create_reader_page()
        self.stk.addWidget(self.reader_page)

        # Page 2 - Saved
        self.saved_page = self.create_saved_page()
        self.stk.addWidget(self.saved_page)

        # Page 3 - Highlights
        self.highlights_page = self.create_highlights_page()
        self.stk.addWidget(self.highlights_page)

        # Page 4 - More (History + Search Results)
        self.more_page = self.create_more_page()
        self.stk.addWidget(self.more_page)

        self.main_layout.addWidget(self.stk, 1)
        self.main_layout.addWidget(self.tab_bar)

        self.switch_main(0)

    def switch_main(self, idx):
        for b in self.tab_group:
            b.setChecked(False)
        # map idx to tab group index: 0->0, 2->1, 3->2, 4->3
        tab_map = {0:0, 2:1, 3:2, 4:3}
        if idx in tab_map:
            self.tab_group[tab_map[idx]].setChecked(True)
        self.stk.setCurrentIndex(idx)
        if idx == 2:
            self.refresh_bookmarks()
            self.refresh_notes_list()
        if idx == 3:
            self.refresh_highlights()
        if idx == 4:
            self.refresh_history()

    def create_home_page(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0,0,0,0)

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
            for i, bname in enumerate(books):
                btn = QPushButton(bname)
                btn.setObjectName("book_btn")
                btn.setToolTip(f"Open {bname} - choose chapter")
                # FIXED: capture correctly
                btn.clicked.connect(lambda checked=False, n=bname: self.on_book_clicked(n))
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

        hdr = QFrame()
        hdr.setObjectName("header_frame")
        hdr.setFixedHeight(50)
        h_lay = QHBoxLayout(hdr)
        h_lay.setContentsMargins(0,0,0,0)

        self.btn_back_home = QPushButton("← Books")
        self.btn_back_home.setObjectName("small_btn")
        self.btn_back_home.setToolTip("Back to Books")
        self.btn_back_home.clicked.connect(lambda: self.switch_main(0))

        self.btn_prev = QPushButton("‹ Prev")
        self.btn_prev.setObjectName("small_btn")
        self.btn_prev.setToolTip("Previous Chapter")
        self.btn_prev.clicked.connect(self.prev_ch)

        self.lbl_reader_title = QLabel(f"{self.cur_b} {self.cur_c}")
        self.lbl_reader_title.setObjectName("reader_title")
        self.lbl_reader_title.setAlignment(Qt.AlignCenter)

        self.btn_next = QPushButton("Next ›")
        self.btn_next.setObjectName("small_btn")
        self.btn_next.setToolTip("Next Chapter")
        self.btn_next.clicked.connect(self.next_ch)

        h_lay.addWidget(self.btn_back_home)
        h_lay.addWidget(self.btn_prev)
        h_lay.addWidget(self.lbl_reader_title, 1)
        h_lay.addWidget(self.btn_next)

        # Chapter chooser
        self.chapters_frame = QFrame()
        self.chapters_frame.setObjectName("chapters_popup")
        self.chapters_frame.setVisible(False)
        ch_vlay = QVBoxLayout(self.chapters_frame)
        ch_vlay.setContentsMargins(8,8,8,8)
        self.lbl_ch_choose = QLabel("Choose Chapter")
        self.lbl_ch_choose.setObjectName("section_label")
        ch_vlay.addWidget(self.lbl_ch_choose)
        self.ch_grid_container = QWidget()
        self.ch_grid = QGridLayout(self.ch_grid_container)
        self.ch_grid.setSpacing(6)
        ch_vlay.addWidget(self.ch_grid_container)

        # Verse chooser (NEW)
        self.verses_chooser_frame = QFrame()
        self.verses_chooser_frame.setObjectName("chapters_popup")
        self.verses_chooser_frame.setVisible(False)
        v_vlay = QVBoxLayout(self.verses_chooser_frame)
        v_vlay.setContentsMargins(8,8,8,8)
        self.lbl_v_choose = QLabel("Choose Verse")
        self.lbl_v_choose.setObjectName("section_label")
        v_vlay.addWidget(self.lbl_v_choose)
        self.v_grid_container = QWidget()
        self.v_grid = QGridLayout(self.v_grid_container)
        self.v_grid.setSpacing(6)
        v_vlay.addWidget(self.v_grid_container)

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
        lay.addWidget(self.verses_chooser_frame)
        lay.addWidget(self.verses_scroll)
        return w

    def create_saved_page(self):
        w = QWidget()
        lay = QHBoxLayout(w)
        left = QFrame()
        left_lay = QVBoxLayout(left)
        left_lay.addWidget(QLabel("🔖 Bookmarks - double-click to open"))
        self.bm_list = QListWidget()
        self.bm_list.setObjectName("list_widget")
        self.bm_list.itemDoubleClicked.connect(self.on_bookmark_open)
        self.btn_del_bm = QPushButton("Remove Bookmark")
        self.btn_del_bm.setObjectName("danger_btn")
        self.btn_del_bm.setToolTip("Remove selected bookmark")
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
        self.btn_del_note.setToolTip("Delete selected note")
        self.btn_del_note.clicked.connect(self.clear_note)
        right_lay.addWidget(self.notes_list)
        right_lay.addWidget(self.btn_del_note)

        lay.addWidget(left)
        lay.addWidget(right)
        return w

    def create_highlights_page(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.addWidget(QLabel("🎨 Highlights - double-click to open"))
        self.hl_list = QListWidget()
        self.hl_list.setObjectName("list_widget")
        self.hl_list.itemDoubleClicked.connect(self.on_highlight_open)
        self.btn_del_hl = QPushButton("Remove Highlight")
        self.btn_del_hl.setObjectName("danger_btn")
        self.btn_del_hl.setToolTip("Remove selected highlight")
        self.btn_del_hl.clicked.connect(self.clear_highlight)
        lay.addWidget(self.hl_list)
        lay.addWidget(self.btn_del_hl)
        return w

    def create_more_page(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setAlignment(Qt.AlignTop)

        # Search results inside More
        self.search_label = QLabel("🔍 Search Results - use top search bar")
        self.search_label.setObjectName("section_label")
        self.search_view = QListWidget()
        self.search_view.setObjectName("list_widget")
        self.search_view.setMaximumHeight(250)
        self.search_view.itemDoubleClicked.connect(self.on_search_open)

        lay.addWidget(self.search_label)
        lay.addWidget(self.search_view)

        lay.addWidget(QLabel("🕘 Recent History"))
        self.hi_list = QListWidget()
        self.hi_list.setObjectName("list_widget")
        self.hi_list.setMaximumHeight(250)
        self.hi_list.itemDoubleClicked.connect(self.on_history_open)
        lay.addWidget(self.hi_list)

        self.btn_clear_history = QPushButton("Clear History")
        self.btn_clear_history.setObjectName("danger_btn")
        self.btn_clear_history.setToolTip("Clear all history")
        self.btn_clear_history.clicked.connect(self.clear_history)
        lay.addWidget(self.btn_clear_history)

        return w

    # ACTIONS
    def on_book_clicked(self, book_name):
        # FIXED - directly called
        self.cur_b = book_name
        self.show_chapters(book_name)

    def show_chapters(self, book):
        self.cur_b = book
        self.stk.setCurrentIndex(1)
        self.lbl_reader_title.setText(f"{book} - Choose Chapter")
        self.verses_chooser_frame.setVisible(False)

        # clear
        while self.ch_grid.count():
            it = self.ch_grid.takeAt(0)
            if it.widget():
                it.widget().deleteLater()

        chs = self.repo.get_chapters(book)
        if not chs:
            chs = list(range(1, 31))
        for c in chs:
            btn = QPushButton(str(c))
            btn.setObjectName("chapter_btn")
            btn.setToolTip(f"Open {book} {c} - choose verse")
            btn.clicked.connect(lambda checked=False, v=c, bk=book: self.show_verses(bk, v))
            self.ch_grid.addWidget(btn, (c-1)//8, (c-1)%8)

        self.chapters_frame.setVisible(True)
        # hide verses
        while self.verses_layout.count():
            it = self.verses_layout.takeAt(0)
            if it.widget():
                it.widget().deleteLater()

    def show_verses(self, book, chapter):
        self.cur_b = book
        self.cur_c = chapter
        self.pending_chapter = chapter
        self.lbl_ch_choose.setText(f"{book} {chapter} - Choose Verse")
        self.chapters_frame.setVisible(False)

        while self.v_grid.count():
            it = self.v_grid.takeAt(0)
            if it.widget():
                it.widget().deleteLater()

        verses = self.repo.get_verses(book, chapter)
        v_count = len(verses) if verses else 30
        for vnum in range(1, v_count+1):
            btn = QPushButton(str(vnum))
            btn.setObjectName("verse_btn")
            btn.setToolTip(f"Read {book} {chapter}:{vnum}")
            btn.clicked.connect(lambda checked=False, vn=vnum, bk=book, ch=chapter: self.open_reader_focused(bk, ch, vn))
            self.v_grid.addWidget(btn, (vnum-1)//10, (vnum-1)%10)

        self.verses_chooser_frame.setVisible(True)

    def open_reader_focused(self, book, chapter, verse):
        self.cur_b = book
        self.cur_c = chapter
        self.cur_v = verse
        self.verses_chooser_frame.setVisible(False)
        self.chapters_frame.setVisible(False)
        self.lbl_reader_title.setText(f"{book} {chapter}")
        self.render_verses(focus_verse=verse)
        self.repo.add_history(book, chapter)
        self.stk.setCurrentIndex(1)

    def open_reader(self, book, chapter):
        self.open_reader_focused(book, chapter, 1)

    def render_verses(self, focus_verse=None):
        while self.verses_layout.count():
            it = self.verses_layout.takeAt(0)
            if it.widget():
                it.widget().deleteLater()

        verses = self.repo.get_verses(self.cur_b, self.cur_c)
        highlights = self.repo.get_highlights_map(self.cur_b, self.cur_c)
        self.verse_widgets = {}

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
            self.verse_widgets[num] = row

        self.verses_layout.addStretch()

        # Focus scroll to specific verse after render
        if focus_verse:
            QTimer.singleShot(150, lambda: self.scroll_to_verse(focus_verse))

    def scroll_to_verse(self, vnum):
        widget = self.verse_widgets.get(vnum)
        if widget:
            self.verses_scroll.ensureWidgetVisible(widget, 100, 100)
            # flash effect
            orig = widget.styleSheet()
            widget.setStyleSheet("background-color: #bd93f9; border-radius: 8px; border: 2px solid #d6bcfa;")
            QTimer.singleShot(1200, lambda: widget.setStyleSheet(orig))

    def prev_ch(self):
        if self.cur_c > 1:
            self.open_reader_focused(self.cur_b, self.cur_c-1, 1)
        elif self.book_list.index(self.cur_b) > 0:
            prev_book = self.book_list[self.book_list.index(self.cur_b)-1]
            chs = self.repo.get_chapters(prev_book)
            if chs:
                self.open_reader_focused(prev_book, max(chs), 1)

    def next_ch(self):
        chs = self.repo.get_chapters(self.cur_b)
        if chs and self.cur_c < max(chs):
            self.open_reader_focused(self.cur_b, self.cur_c+1, 1)
        elif self.book_list.index(self.cur_b) < len(self.book_list)-1:
            next_book = self.book_list[self.book_list.index(self.cur_b)+1]
            self.open_reader_focused(next_book, 1, 1)

    @Slot(int, str)
    def handle_bookmark(self, vnum, txt):
        if self.repo.is_bookmarked(self.cur_b, self.cur_c, vnum):
            bms = self.repo.get_bookmarks()
            for r in bms:
                if r["book"]==self.cur_b and r["chapter"]==self.cur_c and r["verse"]==vnum:
                    self.repo.delete_bookmark(r["id"])
        else:
            self.repo.add_bookmark(self.cur_b, self.cur_c, vnum, txt)
        self.render_verses(focus_verse=vnum)

    @Slot(int, str, str)
    def handle_highlight(self, vnum, txt, color):
        current = self.repo.get_highlights_map(self.cur_b, self.cur_c).get(vnum)
        if current == color:
            self.repo.remove_highlight(self.cur_b, self.cur_c, vnum)
        else:
            self.repo.add_highlight(self.cur_b, self.cur_c, vnum, txt, color)
        self.render_verses(focus_verse=vnum)

    @Slot(int)
    def handle_note(self, vnum):
        existing = self.repo.get_note(self.cur_b, self.cur_c, vnum)
        text, ok = QInputDialog.getMultiLineText(self, f"Note - {self.cur_b} {self.cur_c}:{vnum}", "Your note:", existing)
        if ok:
            if text.strip() == "":
                notes = self.repo.get_notes()
                for r in notes:
                    if r["book"]==self.cur_b and r["chapter"]==self.cur_c and r["verse"]==vnum:
                        self.repo.delete_note(r["id"])
            else:
                self.repo.add_note(self.cur_b, self.cur_c, vnum, text)
            self.render_verses(focus_verse=vnum)

    @Slot(int)
    def handle_copy(self, vnum):
        verses = dict(self.repo.get_verses(self.cur_b, self.cur_c))
        txt = verses.get(vnum, "")
        full = f"{self.cur_b} {self.cur_c}:{vnum} - {txt}"
        from PySide6.QtWidgets import QApplication
        QApplication.clipboard().setText(full)
        self.lbl_reader_title.setText(f"Copied: {self.cur_b} {self.cur_c}:{vnum}")

    def do_search(self):
        kw = self.search_input.text().strip()
        if not kw:
            return
        results = self.repo.search(kw)
        self.search_view.clear()
        self.search_label.setText(f"Found {len(results)} results for '{kw}' - double-click to open")
        for book, chap, verse, text in results:
            item = QListWidgetItem(f"{book} {chap}:{verse} - {text[:120]}")
            item.setData(Qt.UserRole, (book, chap, verse))
            item.setToolTip(f"Open {book} {chap}:{verse}")
            self.search_view.addItem(item)
        self.switch_main(4)

    def on_search_open(self, item):
        data = item.data(Qt.UserRole)
        if data:
            self.open_reader_focused(data[0], data[1], data[2])

    def refresh_bookmarks(self):
        self.bm_list.clear()
        for r in self.repo.get_bookmarks():
            it = QListWidgetItem(f"{r['book']} {r['chapter']}:{r['verse']} - {r['text'][:80]}")
            it.setToolTip(f"Double-click to open {r['book']} {r['chapter']}:{r['verse']}")
            self.bm_list.addItem(it)

    def on_bookmark_open(self, item):
        try:
            ref = item.text().split(' - ')[0]
            book_chap, verse = ref.rsplit(':',1)
            book, chap = book_chap.rsplit(' ',1)
            self.open_reader_focused(book, int(chap), int(verse))
        except:
            pass

    def clear_bookmark(self):
        bms = self.repo.get_bookmarks()
        row = self.bm_list.currentRow()
        if 0 <= row < len(bms):
            self.repo.delete_bookmark(bms[row]["id"])
            self.refresh_bookmarks()

    def refresh_notes_list(self):
        self.notes_list.clear()
        for r in self.repo.get_notes():
            it = QListWidgetItem(f"{r['book']} {r['chapter']}:{r['verse']} - {r['note'][:80]}")
            it.setToolTip("Double-click to open")
            self.notes_list.addItem(it)

    def on_note_open(self, item):
        try:
            ref = item.text().split(' - ')[0]
            book_chap, verse = ref.rsplit(':',1)
            book, chap = book_chap.rsplit(' ',1)
            self.open_reader_focused(book, int(chap), int(verse))
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
            it = QListWidgetItem(f"[{r['color']}] {r['book']} {r['chapter']}:{r['verse']} - {r['text'][:80]}")
            it.setToolTip(f"Double-click to open {r['book']} {r['chapter']}:{r['verse']}")
            self.hl_list.addItem(it)

    def on_highlight_open(self, item):
        try:
            ref_part = item.text().split('] ')[1].split(' - ')[0]
            book_chap, verse = ref_part.rsplit(':',1)
            book, chap = book_chap.rsplit(' ',1)
            self.open_reader_focused(book, int(chap), int(verse))
        except:
            pass

    def clear_highlight(self):
        hls = self.repo.get_highlights()
        row = self.hl_list.currentRow()
        if 0 <= row < len(hls):
            r = hls[row]
            self.repo.remove_highlight(r["book"], r["chapter"], r["verse"])
            self.refresh_highlights()

    def refresh_history(self):
        self.hi_list.clear()
        for r in self.repo.get_history():
            it = QListWidgetItem(f"{r['book']} {r['chapter']}")
            it.setToolTip(f"Open {r['book']} {r['chapter']}")
            self.hi_list.addItem(it)

    def on_history_open(self, item):
        try:
            book, chap = item.text().rsplit(' ',1)
            self.open_reader_focused(book, int(chap), 1)
        except:
            pass

    def clear_history(self):
        from database import get_connection
        conn = get_connection()
        conn.execute("DELETE FROM history")
        conn.commit()
        conn.close()
        self.refresh_history()

    def font_increase(self):
        self.font_size = min(30, self.font_size+2)
        self.repo.set_setting("font_size", str(self.font_size))

    def font_decrease(self):
        self.font_size = max(12, self.font_size-2)
        self.repo.set_setting("font_size", str(self.font_size))

    def toggle_theme(self):
        self.theme = "light" if self.theme=="dark" else "dark"
        self.repo.set_setting("theme", self.theme)
        self.btn_theme.setText("☀️" if self.theme=="dark" else "🌙")
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
