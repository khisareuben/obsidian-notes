from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton
from .base_page import BasePage
from page_types import Page

class SettingsPage(BasePage):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24,24,24,24)
        layout.setSpacing(12)

        layout.addWidget(QLabel("<h1>Settings</h1>"))
        layout.addWidget(QLabel("App configuration. This page also preserves state."))

        btn_home = QPushButton("← Back to Dashboard")
        btn_notes = QPushButton("Go to My Notes")
        btn_home.clicked.connect(lambda: self.request_navigate.emit(Page.HOME))
        btn_notes.clicked.connect(lambda: self.request_navigate.emit(Page.NOTES))

        layout.addWidget(btn_home)
        layout.addWidget(btn_notes)
        layout.addStretch()
