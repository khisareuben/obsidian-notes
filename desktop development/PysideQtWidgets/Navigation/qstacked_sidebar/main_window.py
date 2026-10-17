from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from navigation import NavigationController
from page_types import Page
from widgets.sidebar import SidebarWidget
from pages import HomePage, NotesPage, SettingsPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sidebar + QStacked Navigation - Industry Standard")
        self.resize(1000, 600)

        self.nav_controller = NavigationController()
        self.stack = QStackedWidget()
        self.stack.setObjectName("stack")

        self.pages_map = {
            Page.HOME: HomePage(),
            Page.NOTES: NotesPage(),
            Page.SETTINGS: SettingsPage(),
        }

        for page_widget in self.pages_map.values():
            self.stack.addWidget(page_widget)
            page_widget.request_navigate.connect(self.nav_controller.navigate_to)

        # Sidebar - the collapsible navigation you studied earlier
        self.sidebar = SidebarWidget()
        self.sidebar.request_navigate.connect(self.nav_controller.navigate_to)
        self.sidebar.request_back.connect(self.nav_controller.go_back)
        self.sidebar.request_forward.connect(self.nav_controller.go_forward)

        # Controller -> UI
        self.nav_controller.page_changed.connect(self.on_page_changed)
        self.nav_controller.history_changed.connect(self.sidebar.set_history_state)

        container = QWidget()
        container.setObjectName("centralWidget")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack, 1)
        self.setCentralWidget(container)

        self.nav_controller.navigate_to(Page.HOME, add_to_history=False)

    def on_page_changed(self, page: Page):
        if hasattr(self, '_last_page') and self._last_page in self.pages_map:
            self.pages_map[self._last_page].on_leave()

        widget = self.pages_map[page]
        self.stack.setCurrentWidget(widget)
        widget.on_enter()

        self.sidebar.set_active_page(page)
        self._last_page = page
        self.statusBar().showMessage(f"Current: {page.name} | History: {len(self.nav_controller._history)} Back, {len(self.nav_controller._future)} Forward")
