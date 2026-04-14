
# 🔹 PySide6 + QML Key Concepts

## 1. `@Slot()`

- **Purpose:** Exposes a Python method to QML so it can be called directly.
    
- **Usage:** Decorate a method in your backend class with `@Slot()`.
    
- **Example:**
    



```python
from PySide6.QtCore import QObject, Slot

class Backend(QObject):
    @Slot(str)
    def greet(self, name):
        # This method can now be called from QML
        print(f"Hello, {name}!")
```



```q
Button {
    text: "Say Hello"
    onClicked: backend.greet("Harold") // Calls Python slot
}
```

## 2. `Signal`

- **Purpose:** Send data/events from Python to QML.
    
- **Usage:** Define a `Signal` in Python, emit it when needed, and connect it in QML.
    
- **Example:**
    



```python
from PySide6.QtCore import QObject, Signal

class Backend(QObject):
    messageChanged = Signal(str)  # Define signal

    def send_message(self, msg):
        self.messageChanged.emit(msg)  # Emit signal
```



```q
Connections {
    target: backend
    onMessageChanged: console.log("Message from Python:", msg)
}
```

## 3. `QQmlApplicationEngine`

- **Purpose:** Loads and runs QML files from Python.
    
- **Usage:** Create engine, load QML, and bind backend.
    
- **Example:**
    



```python
from PySide6.QtQml import QQmlApplicationEngine

engine = QQmlApplicationEngine()
engine.rootContext().setContextProperty("backend", backend)  # Expose backend
engine.load("main.qml")
```

## 4. `rootContext().setContextProperty`

- **Purpose:** Makes a Python object accessible in QML.
    
- **Usage:** Bind backend to QML under a name.
    
- **Example:**
    



```python
engine.rootContext().setContextProperty("backend", backend)
```


```q
// Now you can call backend methods directly in QML
backend.greet("World")
```

## 5. `Connections` in QML

- **Purpose:** Listen to Python signals inside QML.
    
- **Usage:** Use `Connections` block with `target`.
    
- **Example:**
    


```q
Connections {
    target: backend
    onMessageChanged: statusLabel.text = msg
}
```

## 6. `property` in QML

- **Purpose:** Store and bind values inside QML.
    
- **Usage:** Define reactive properties.
    
- **Example:**
    


```q
ApplicationWindow {
    property int count: 0

    Button {
        text: "Click"
        onClicked: count++
    }

    Label { text: "Count: " + count }
}
```

## 7. `ListModel` and `ListView`

- **Purpose:** Display lists of data.
    
- **Usage:** Define a model and bind to a view.
    
- **Example:**
    


```q
ListModel { id: todoModel }

ListView {
    model: todoModel
    delegate: Label { text: task }
}
```


```q
Button {
    text: "Add"
    onClicked: todoModel.append({ "task": "New Task" })
}
```

## 8. `Timer`

- **Purpose:** Run repeated actions at intervals.
    
- **Usage:** Define interval and start/stop.
    
- **Example:**
    


```q
Timer {
    id: timer
    interval: 1000 // 1 second
    repeat: true
    onTriggered: console.log("Tick")
}
```

## 9. `TextField` and `TextArea`

- **Purpose:** Input fields for user text.
    
- **Usage:** Bind text to properties or pass to backend.
    
- **Example:**
    


```q
TextField {
    id: input
    placeholderText: "Enter name"
}

Button {
    text: "Submit"
    onClicked: backend.greet(input.text)
}
```

## 10. `ComboBox`

- **Purpose:** Dropdown selection.
    
- **Usage:** Provide a model and read `currentText`.
    
- **Example:**
    


```q
ComboBox {
    id: formatChoice
    model: ["mp4", "mp3"]
}

Button {
    text: "Download"
    onClicked: backend.download_video(urlInput.text, formatChoice.currentText)
}
```

✅ These are the **core building blocks** you’ll see in almost every PySide6 + QML project: `@Slot`, `Signal`, `Connections`, `property`, `ListModel`, and the common controls.