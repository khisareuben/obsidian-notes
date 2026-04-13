
# Part 1: Setup & Hello World in PySide6 + QML

## 🔧 Step 1: Install PySide6

Open your terminal and run:

bash

```
python3 -m venv venv        # Create a virtual environment
source venv/bin/activate    # Activate it
pip install pyside6         # Install PySide6
```

This ensures you’re working in an isolated environment.

## 📂 Step 2: Project Structure

Create a folder for your project:

Code

```
pyside6_qml_hello/
├── main.py
└── main.qml
```

## 📝 Step 3: Write the Python Loader

`main.py` will load the QML file and start the app.



```python
# main.py
import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

# Create the application object
app = QGuiApplication(sys.argv)

# Load the QML engine
engine = QQmlApplicationEngine()
engine.load("main.qml")

# Exit if QML failed to load
if not engine.rootObjects():
    sys.exit(-1)

# Run the app loop
sys.exit(app.exec())
```

## 🎨 Step 4: Create the QML UI

`main.qml` defines the interface.

qml

```q
// main.qml
import QtQuick
import QtQuick.Controls

ApplicationWindow {
    visible: true
    width: 400
    height: 200
    title: "Hello World"

    Text {
        text: "Hello, PySide6 + QML!"
        anchors.centerIn: parent
        font.pixelSize: 20
    }
}
```

## ▶️ Step 5: Run the App

In your terminal:



```bash
python main.py
```

You should see a small window with the text **“Hello, PySide6 + QML!”** centered.

## 🧠 Key Concepts Learned

- **PySide6** provides the Python bindings.
    
- **QML** handles the UI layer.
    
- **QQmlApplicationEngine** loads QML files.
    
- **ApplicationWindow** is the root container for your app.