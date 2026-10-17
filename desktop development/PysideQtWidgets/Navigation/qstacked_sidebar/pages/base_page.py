from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal
from page_types import Page

class BasePage(QWidget):
    request_navigate = Signal(Page)

    def on_enter(self):
        pass

    def on_leave(self):
        pass
