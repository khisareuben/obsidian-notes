
```python
from PySide6.QtWidgets import QApplication, QPushButton
import sys

def button_clicked(data):
	print(f"You clicked the button : {data}")  

app = QApplication(sys.argv)
button = QPushButton("press me")

button.setCheckable(True)

button.clicked.connect(button_clicked)
button.show()
  
app.exec()
```


#### Slider

This is like a volume slot where you can increase or decrease the it when you slide either left or right

```python
from PySide6.QtWidgets import QApplication, QSlider
from PySide6.QtCore import Qt
import sys


def respond_to_slider(data):
	print(f"Slider moved to : {data}")
 
app = QApplication(sys.argv)
slider = QSlider(Qt.Horizontal)
slider.setMinimum(1)
slider.setMaximum(100)
slider.setValue(20)

slider.valueChanged.connect(respond_to_slider)
slider.show() 

app.exec()
```


Next topic : [[Qt Widgets]]

previous topic : [[Button]]