
```python
from PySide6.QtWidgets import QApplication, QMainWidget, QPushButton
import sys

class ButtonHandler(QMainWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Button app")
		button = QPushButton("Press me")
		self.setCentralWidget(button)

app = QApplication(sys.argv)
window = ButtonHandler()
window.show()

app.exec()
```