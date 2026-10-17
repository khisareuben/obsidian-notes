`main.py`
```python
from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt
from widget import SidebarWidget
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Practice")
        self.resize(1000, 700)
        self.ui = SidebarWidget()
        self.setCentralWidget(self.ui)

        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Collapsible Sidebar Study")
        self.resize(800, 500)

        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        self.sidebar = SidebarWidget()
        self.content = QLabel("Content Area")
        self.content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content.setObjectName("content")

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content, 1) # stretch 1 = takes rest of space

        try:
            with open("style.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("style.qss not found")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

```

`widget.py`
```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve

class SidebarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("sidebar")
        self.setAttribute(Qt.WA_StyledBackground, True)

        # State
        self._is_expanded = True
        self.collapsed_width = 60
        self.expanded_width = 220
        self.setFixedWidth(self.expanded_width)

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 10, 5, 10)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignTop)

        # 1. Toggle Button
        self.toggle_btn = QPushButton("☰  Collapse")
        self.toggle_btn.setObjectName("toggleBtn")
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        layout.addWidget(self.toggle_btn)

        # Separator
        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.HLine)
        layout.addWidget(sep)

        # 2. Fake Tabs - they don't need to work
        self.btn_dashboard = QPushButton("◉  Dashboard")
        self.btn_files = QPushButton("⧉  Files")
        self.btn_settings = QPushButton("⚙  Settings")

        for btn in [self.btn_dashboard, self.btn_files, self.btn_settings]:
            btn.setObjectName("navBtn")
            btn.setCursor(Qt.PointingHandCursor)
            layout.addWidget(btn)

        layout.addStretch()

        # Animation for smooth expand/collapse
        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)

    def toggle_sidebar(self):
        start = self.width()
        end = self.collapsed_width if self._is_expanded else self.expanded_width

        self.animation.setStartValue(start)
        self.animation.setEndValue(end)
        self.animation.start()

        self._is_expanded = not self._is_expanded

        # Hide text when collapsed
        if self._is_expanded:
            self.toggle_btn.setText("☰  Collapse")
            self.btn_dashboard.setText("◉  Dashboard")
            self.btn_files.setText("⧉  Files")
            self.btn_settings.setText("⚙  Settings")
        else:
            self.toggle_btn.setText("☰")
            self.btn_dashboard.setText("◉")
            self.btn_files.setText("⧉")
            self.btn_settings.setText("⚙")

        # Also lock max width so it doesn't stretch
        self.setFixedWidth(end)
```


`style.qss`
```python
#centralWidget {
    background-color: #f5f5f5;
}
#sidebar {
    background-color: #1e1e1e;
}
#toggleBtn {
    background-color: #2d2d2d;
    color: white;
    padding: 12px;
    border: none;
    border-radius: 6px;
    text-align: left;
}
#navBtn {
    background-color: transparent;
    color: #a0a0a0;
    padding: 12px;
    border: none;
    border-radius: 6px;
    text-align: left;
}
#navBtn:hover {
    background-color: #2d2d2d;
    color: white;
}
#separator {
    background-color: #333;
    max-height: 1px;
}
#content {
    background-color: white;
}
```