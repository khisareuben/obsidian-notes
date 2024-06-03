# Layouts

#### main.py

```python
from PySide6.QtWidgets import QApplication
from rockwidget import RockWidget
import sys

app = QApplication(sys.argv)
window = RockWidget()
window.show() 

app.exec()
```


#### rockwidget.py

```python
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout  

class RockWidget(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("My app")
		 
		button1 = QPushButton("button1")
		button1.clicked.connect(self.button1_clicked)
		button2 = QPushButton("button2")
		button2.clicked.connect(self.button2_clicked)  
		
		button_layout = QVBoxLayout()
		button_layout.addWidget(button1)
		button_layout.addWidget(button2)
		 
		self.setLayout(button_layout)

  
def button1_clicked(self):
	print("button1 is clicked") 

def button2_clicked(self):
	print("button2 is clicked")
```