from PySide6.QtCore import QObject, Signal
from page_types import Page

class NavigationController(QObject):
    page_changed = Signal(Page)
    history_changed = Signal(bool, bool)

    def __init__(self):
        super().__init__()
        self._history: list[Page] = []
        self._future: list[Page] = []
        self._current: Page | None = None

    @property
    def current(self) -> Page | None:
        return self._current

    def can_go_back(self) -> bool:
        return len(self._history) > 0

    def can_go_forward(self) -> bool:
        return len(self._future) > 0

    def navigate_to(self, page: Page, add_to_history: bool = True):
        if self._current == page:
            return
        if add_to_history and self._current is not None:
            self._history.append(self._current)
            self._future.clear()
        self._current = page
        self.page_changed.emit(page)
        self.history_changed.emit(self.can_go_back(), self.can_go_forward())

    def go_back(self):
        if not self.can_go_back():
            return
        if self._current is not None:
            self._future.append(self._current)
        prev_page = self._history.pop()
        self._current = prev_page
        self.page_changed.emit(prev_page)
        self.history_changed.emit(self.can_go_back(), self.can_go_forward())

    def go_forward(self):
        if not self.can_go_forward():
            return
        if self._current is not None:
            self._history.append(self._current)
        next_page = self._future.pop()
        self._current = next_page
        self.page_changed.emit(next_page)
        self.history_changed.emit(self.can_go_back(), self.can_go_forward())
