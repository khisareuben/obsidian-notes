# PROJECT 1: SIDEBAR IN REAL PROJECTS - PySide6 6.11.2
### How Professional Teams Actually Build and Use a Sidebar

> Focus: **Sidebar as a UI component** - layout, sections, styling, collapsible, not navigation logic.

---

## What This Project Shows

In real products, Sidebar is a **standalone widget** that product teams reuse:
- VS Code: Activity Bar + Side Bar are separate packages
- Slack: Sidebar has workspaces, channels, DMs, sections
- Notion: Sidebar has favorites, private, shared

This project shows exactly that.

```
sidebar_real_world/
├── pyproject.toml
├── src/sidebar_real_world/
│   ├── app.py
│   ├── main_window.py
│   ├── config.py
│   ├── models/
│   │   └── sidebar.py          # SidebarSection, SidebarItem models
│   ├── components/
│   │   ├── sidebar.py          # The reusable Sidebar widget (240px)
│   │   ├── sidebar_section.py  # Collapsible section (like Notion)
│   │   ├── sidebar_item.py     # Item with icon, badge, actions
│   │   ├── icon_rail.py        # 56px rail
│   │   └── search_field.py
│   ├── pages/
│   │   └── placeholder.py
│   └── resources/
│       └── styles/theme.qss
```

---

## 1. Models - How Sidebar Data is Structured in Real Apps

**`src/sidebar_real_world/models/sidebar.py`**
```python
from dataclasses import dataclass, field
from typing import List, Optional, Callable

@dataclass
class SidebarItem:
    id: str
    title: str
    icon: str = "•"
    badge: Optional[str] = None  # e.g. "3", "NEW"
    tooltip: str = ""
    children: List['SidebarItem'] = field(default_factory=list)  # For nested
    on_click: Optional[Callable] = None
    context_menu: bool = True

@dataclass
class SidebarSection:
    id: str
    title: str  # e.g. "FAVORITES", "WORKSPACES"
    collapsible: bool = True
    collapsed: bool = False
    items: List[SidebarItem] = field(default_factory=list)
    show_add_button: bool = False
    show_more_button: bool = False

# Example data as you'd get from API / DB
MOCK_SECTIONS = [
    SidebarSection("favorites", "FAVORITES", True, False, [
        SidebarItem("fav1", "Design System", "★", tooltip="Pinned"),
        SidebarItem("fav2", "Q1 Roadmap", "★", badge="3"),
    ], show_add_button=True),
    SidebarSection("workspaces", "WORKSPACES", True, False, [
        SidebarItem("ws1", "Acme Corp", "◼", badge="12"),
        SidebarItem("ws2", "Side Project", "◼"),
    ]),
    SidebarSection("recent", "RECENT", True, False, [
        SidebarItem("r1", "Fix sidebar bug", "↺"),
        SidebarItem("r2", "PR #128", "↺"),
    ], show_more_button=True),
]
```

---

## 2. Sidebar Components - Reusable

**`src/sidebar_real_world/components/sidebar_item.py`**
```python
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QToolButton
from ..models.sidebar import SidebarItem

class SidebarItemWidget(QFrame):
    clicked = Signal(str)  # id
    more_clicked = Signal(str)

    def __init__(self, item: SidebarItem, parent=None):
        super().__init__(parent)
        self.item_model = item
        self.setObjectName("SidebarItem")
        self.setFixedHeight(32)
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        icon = QLabel(self.item_model.icon)
        icon.setObjectName("ItemIcon")
        layout.addWidget(icon)

        title = QLabel(self.item_model.title)
        title.setObjectName("ItemTitle")
        layout.addWidget(title, 1)

        if self.item_model.badge:
            badge = QLabel(self.item_model.badge)
            badge.setObjectName("Badge")
            layout.addWidget(badge)

        if self.item_model.context_menu:
            more = QToolButton()
            more.setText("⋯")
            more.setObjectName("ItemMore")
            more.clicked.connect(lambda: self.more_clicked.emit(self.item_model.id))
            layout.addWidget(more)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.item_model.id)
        super().mousePressEvent(event)
```

**`src/sidebar_real_world/components/sidebar_section.py`**
```python
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QToolButton
from ..models.sidebar import SidebarSection
from .sidebar_item import SidebarItemWidget

class SidebarSectionWidget(QFrame):
    item_clicked = Signal(str)
    add_clicked = Signal(str)  # section id
    toggle_collapsed = Signal(str, bool)

    def __init__(self, section: SidebarSection, parent=None):
        super().__init__(parent)
        self.section_model = section
        self.setObjectName("SidebarSection")
        self._item_widgets = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(2)

        # Header
        header = QFrame()
        header.setObjectName("SectionHeaderFrame")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(4, 4, 4, 4)
        hl.setSpacing(4)

        self.collapse_btn = QToolButton()
        self.collapse_btn.setText("▼" if not self.section_model.collapsed else "▶")
        self.collapse_btn.setObjectName("CollapseBtn")
        self.collapse_btn.clicked.connect(self._toggle)
        hl.addWidget(self.collapse_btn)

        title = QLabel(self.section_model.title)
        title.setObjectName("SectionTitle")
        hl.addWidget(title, 1)

        if self.section_model.show_add_button:
            add = QToolButton()
            add.setText("+")
            add.setObjectName("AddBtn")
            add.clicked.connect(lambda: self.add_clicked.emit(self.section_model.id))
            hl.addWidget(add)

        if self.section_model.show_more_button:
            more = QToolButton()
            more.setText("⋯")
            more.setObjectName("MoreBtn")
            hl.addWidget(more)

        layout.addWidget(header)

        # Items container (collapsible)
        self.items_container = QFrame()
        self.items_container.setObjectName("ItemsContainer")
        self.items_layout = QVBoxLayout(self.items_container)
        self.items_layout.setContentsMargins(0,0,0,0)
        self.items_layout.setSpacing(1)

        for item_model in self.section_model.items:
            w = SidebarItemWidget(item_model)
            w.clicked.connect(self.item_clicked.emit)
            self._item_widgets.append(w)
            self.items_layout.addWidget(w)

        self.items_container.setVisible(not self.section_model.collapsed)
        layout.addWidget(self.items_container)

    def _toggle(self):
        new_state = not self.items_container.isVisible()
        self.items_container.setVisible(new_state)
        self.collapse_btn.setText("▼" if new_state else "▶")
        self.toggle_collapsed.emit(self.section_model.id, not new_state)

    def filter(self, text: str):
        # Real app: filter items
        t = text.lower()
        for w in self._item_widgets:
            w.setVisible(t in w.item_model.title.lower())
```

**`src/sidebar_real_world/components/sidebar.py`**
```python
# The main reusable Sidebar widget - this is what you import in any project
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QScrollArea, QWidget, QLabel, QLineEdit
from ..models.sidebar import MOCK_SECTIONS, SidebarSection
from .sidebar_section import SidebarSectionWidget

class Sidebar(QFrame):
    # Public API - what app cares about
    item_selected = Signal(str)  # item id
    section_toggled = Signal(str, bool)
    search_changed = Signal(str)

    def __init__(self, sections=None, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(280)
        self.setMinimumWidth(200)
        self.setMaximumWidth(360)
        self._sections_data = sections or MOCK_SECTIONS
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        # Header with search
        header = QFrame()
        header.setObjectName("SidebarHeader")
        hl = QVBoxLayout(header)
        hl.setContentsMargins(12,12,12,12)
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search...")
        self.search.setObjectName("SearchField")
        self.search.textChanged.connect(self._on_search)
        hl.addWidget(self.search)
        layout.addWidget(header)

        # Scrollable sections
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(8,8,8,16)
        self.content_layout.setSpacing(12)

        self._section_widgets = []
        for sec_model in self._sections_data:
            w = SidebarSectionWidget(sec_model)
            w.item_clicked.connect(self.item_selected.emit)
            w.toggle_collapsed.connect(self.section_toggled.emit)
            w.add_clicked.connect(lambda sid: print(f"Add clicked in {sid}"))
            self._section_widgets.append(w)
            self.content_layout.addWidget(w)

        self.content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll, 1)

        # Footer - user profile / bottom pinned
        footer = QFrame()
        footer.setObjectName("SidebarFooter")
        fl = QVBoxLayout(footer)
        fl.setContentsMargins(12,8,12,8)
        fl.addWidget(QLabel("John Doe • Pro"))
        layout.addWidget(footer)

    def _on_search(self, text):
        self.search_changed.emit(text)
        for sec in self._section_widgets:
            sec.filter(text)

    # Public method to add item dynamically (real app: after API call)
    def add_item_to_section(self, section_id: str, item):
        for sec_w in self._section_widgets:
            if sec_w.section_model.id == section_id:
                from .sidebar_item import SidebarItemWidget
                w = SidebarItemWidget(item)
                w.clicked.connect(self.item_selected.emit)
                sec_w.items_layout.addWidget(w)
                break
```

**`src/sidebar_real_world/components/icon_rail.py`**
```python
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QVBoxLayout, QToolButton
from ..config import RAIL_WIDTH

class IconRail(QFrame):
    navigate = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(RAIL_WIDTH)
        self.setObjectName("IconRail")
        layout = QVBoxLayout(self)
        for icon, id_ in [("⌂","home"),("◧","projects"),("↺","recent"),("☆","fav"),("⚙","settings")]:
            btn = QToolButton()
            btn.setText(icon)
            btn.setFixedSize(40,40)
            btn.clicked.connect(lambda _, i=id_: self.navigate.emit(i))
            layout.addWidget(btn)
        layout.addStretch()
```

---

## 3. Main Window - How Sidebar is Used

**`src/sidebar_real_world/main_window.py`**
```python
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QSplitter, QLabel, QStackedWidget
from .components.sidebar import Sidebar
from .components.icon_rail import IconRail
from .resources.styles.theme import load_qss

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sidebar Real World - How Sidebar is Used")
        self.resize(1200, 700)
        self.setStyleSheet(load_qss())
        self._setup_ui()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0,0,0,0)

        self.rail = IconRail()
        self.sidebar = Sidebar()
        self.content = QStackedWidget()
        self.content.addWidget(QLabel("Select an item from sidebar"))

        self.sidebar.item_selected.connect(self._on_item_selected)

        left = QWidget()
        ll = QHBoxLayout(left)
        ll.setContentsMargins(0,0,0,0)
        ll.setSpacing(0)
        ll.addWidget(self.rail)
        ll.addWidget(self.sidebar)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left)
        splitter.addWidget(self.content)

        root.addWidget(splitter)

    def _on_item_selected(self, item_id: str):
        self.content.addWidget(QLabel(f"Content for {item_id}"))
        self.content.setCurrentIndex(self.content.count()-1)
```

This project teaches: **How to BUILD a sidebar** - sections, items, badges, collapsible, search filter, footer.

---

# Usage
```bash
pip install PySide6==6.11.2 -e .
python -m sidebar_real_world.app
```
