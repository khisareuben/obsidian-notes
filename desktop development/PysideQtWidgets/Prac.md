
```python
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout, QFormLayout, QLineEdit, QLabel, QGroupBox
import sys

class Window(QWidget):
    """Learn: QHBoxLayout, QVBoxLayout, QGridLayout, QFormLayout, stretch, spacing, nested layouts"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("06 - Layouts Mastery")
        self.resize(600, 400)
        
        # 1. Form Layout - Login
        form_group = QGroupBox("QFormLayout - Login Form")
        form = QFormLayout()
        form.addRow("Username:", QLineEdit())
        form.addRow("Password:", QLineEdit())
        form.addRow("", QPushButton("Login"))
        form_group.setLayout(form)
        
        # 2. Grid Layout - Calculator buttons
        grid_group = QGroupBox("QGridLayout - Calculator")
        grid = QGridLayout()
        buttons = ["7","8","9","/","4","5","6","*","1","2","3","-","0",".","=","+"]
        for i, txt in enumerate(buttons):
            btn = QPushButton(txt)
            grid.addWidget(btn, i//4, i%4)
        grid_group.setLayout(grid)
        
        # 3. Nested H and V
        h_group = QGroupBox("QHBox + QVBox")
        v = QVBoxLayout()
        h = QHBoxLayout()
        h.addWidget(QPushButton("Left"))
        h.addWidget(QPushButton("Center"))
        h.addWidget(QPushButton("Right"))
        v.addLayout(h)
        v.addWidget(QLabel("This is nested layout example"), 1) # stretch
        h_group.setLayout(v)
        
        main = QVBoxLayout()
        top_row = QHBoxLayout()
        top_row.addWidget(form_group)
        top_row.addWidget(grid_group)
        main.addLayout(top_row)
        main.addWidget(h_group)
        self.setLayout(main)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec())
```