from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton
from .base_page import BasePage
from page_types import Page

class HomePage(BasePage):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24,24,24,24)
        layout.setSpacing(12)

        layout.addWidget(QLabel("<h1>Dashboard</h1>"))
        layout.addWidget(QLabel("This is your landing page. State is preserved when you navigate away."))

        btn_notes = QPushButton("Go to My Notes →")
        btn_settings = QPushButton("Go to Settings →")
        btn_notes.clicked.connect(lambda: self.request_navigate.emit(Page.NOTES))
        btn_settings.clicked.connect(lambda: self.request_navigate.emit(Page.SETTINGS))

        layout.addWidget(btn_notes)
        layout.addWidget(btn_settings)
        layout.addStretch()
