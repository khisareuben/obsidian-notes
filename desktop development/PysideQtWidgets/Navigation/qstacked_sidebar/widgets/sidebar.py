from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame
from PySide6.QtCore import Qt, Signal
from page_types import Page

class SidebarWidget(QWidget):
    request_navigate = Signal(Page)
    request_back = Signal()
    request_forward = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("sidebar")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._is_expanded = True
        self.collapsed_width = 65
        self.expanded_width = 220
        self.setFixedWidth(self.expanded_width)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 10, 8, 10)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignTop)

        self.toggle_btn = QPushButton("☰  Collapse")
        self.toggle_btn.setObjectName("toggleBtn")
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        layout.addWidget(self.toggle_btn)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Plain)
        layout.addWidget(sep)

        self.btn_home = QPushButton("◉  Dashboard")
        self.btn_notes = QPushButton("⧉  My Notes")
        self.btn_settings = QPushButton("⚙  Settings")

        self.btn_home.clicked.connect(lambda: self.request_navigate.emit(Page.HOME))
        self.btn_notes.clicked.connect(lambda: self.request_navigate.emit(Page.NOTES))
        self.btn_settings.clicked.connect(lambda: self.request_navigate.emit(Page.SETTINGS))

        for btn in [self.btn_home, self.btn_notes, self.btn_settings]:
            btn.setObjectName("navBtn")
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            layout.addWidget(btn)

        layout.addStretch()

        self.btn_back = QPushButton("← Back")
        self.btn_forward = QPushButton("Forward →")
        self.btn_back.setObjectName("smallNavBtn")
        self.btn_forward.setObjectName("smallNavBtn")
        self.btn_back.clicked.connect(self.request_back.emit)
        self.btn_forward.clicked.connect(self.request_forward.emit)
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_forward.setCursor(Qt.PointingHandCursor)

        layout.addWidget(self.btn_back)
        layout.addWidget(self.btn_forward)

        self._buttons = {
            Page.HOME: self.btn_home,
            Page.NOTES: self.btn_notes,
            Page.SETTINGS: self.btn_settings
        }

    def toggle_sidebar(self):
        end = self.collapsed_width if self._is_expanded else self.expanded_width
        self._is_expanded = not self._is_expanded
        self.setFixedWidth(end)

        if self._is_expanded:
            self.toggle_btn.setText("☰  Collapse")
            self.btn_home.setText("◉  Dashboard")
            self.btn_notes.setText("⧉  My Notes")
            self.btn_settings.setText("⚙  Settings")
            self.btn_back.setText("← Back")
            self.btn_forward.setText("Forward →")
        else:
            self.toggle_btn.setText("☰")
            self.btn_home.setText("◉")
            self.btn_notes.setText("⧉")
            self.btn_settings.setText("⚙")
            self.btn_back.setText("←")
            self.btn_forward.setText("→")

    def set_active_page(self, page: Page):
        for p, btn in self._buttons.items():
            btn.setChecked(p == page)

    def set_history_state(self, can_back: bool, can_forward: bool):
        self.btn_back.setEnabled(can_back)
        self.btn_forward.setEnabled(can_forward)
