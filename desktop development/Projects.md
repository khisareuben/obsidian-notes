
# 🔹 PySide6 + QML Project Notes

## 1. Click Counter

**Goal:** A button that increments a counter every time it’s clicked.



```python
# click_counter.py
# Python entry point for QML app

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

app = QApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.load("click_counter.qml")

if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())
```



```q
// click_counter.qml
import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 300
    height: 200
    title: "Click Counter"

    property int count: 0 // variable to store clicks

    Column {
        anchors.centerIn: parent
        spacing: 10

        Label {
            text: "Count: " + count
        }

        Button {
            text: "Click Me"
            onClicked: count++ // increment counter
        }
    }
}
```

## 2. To-Do List

**Goal:** Add tasks to a list and display them.



```python
# todo.py
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

app = QApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.load("todo.qml")

if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())
```



```q
// todo.qml
import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 400
    height: 300
    title: "To-Do List"

    ListModel { id: todoModel } // holds tasks

    Column {
        anchors.fill: parent
        spacing: 10
        padding: 10

        TextField { id: taskInput; placeholderText: "Enter task" }

        Button {
            text: "Add Task"
            onClicked: {
                if (taskInput.text !== "") {
                    todoModel.append({ "task": taskInput.text })
                    taskInput.text = "" // clear input
                }
            }
        }

        ListView {
            anchors.fill: parent
            model: todoModel
            delegate: Label { text: task }
        }
    }
}
```

## 3. Text Editor

**Goal:** A simple text area for writing notes.



```python
# text_editor.py
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

app = QApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.load("text_editor.qml")

if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())
```



```q
// text_editor.qml
import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 500
    height: 400
    title: "Text Editor"

    TextArea {
        anchors.fill: parent
        placeholderText: "Write something..."
        wrapMode: TextEdit.Wrap // auto-wrap text
    }
}
```

## 4. Currency Converter

**Goal:** Convert USD to KES using a static rate.



```python
# currency_converter.py
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

app = QApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.load("currency.qml")

if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())
```

l

```q
// currency.qml
import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 300
    height: 200
    title: "Currency Converter"

    property double rate: 150.0 // Example: 1 USD = 150 KES
    property double result: 0

    Column {
        anchors.centerIn: parent
        spacing: 10

        TextField { id: usd; placeholderText: "Enter USD" }

        Button {
            text: "Convert"
            onClicked: result = parseFloat(usd.text) * rate
        }

        Label { text: "KES: " + result }
    }
}
```

## 5. Notes App (SQLite) — With Add, Update, Delete



```python
# notes_app.py
# Backend with SQLite database for notes

import sys
import sqlite3
from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

class NotesBackend(QObject):
    notesChanged = Signal(list)  # Signal to update QML

    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect("notes.db")
        self.cursor = self.conn.cursor()
        # Create table if not exists
        self.cursor.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, text TEXT)")
        self.conn.commit()
        self.load_notes()

    @Slot(str)
    def add_note(self, text):
        """Add a new note"""
        self.cursor.execute("INSERT INTO notes (text) VALUES (?)", (text,))
        self.conn.commit()
        self.load_notes()

    @Slot(int, str)
    def update_note(self, note_id, new_text):
        """Update an existing note"""
        self.cursor.execute("UPDATE notes SET text=? WHERE id=?", (new_text, note_id))
        self.conn.commit()
        self.load_notes()

    @Slot(int)
    def delete_note(self, note_id):
        """Delete a note"""
        self.cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
        self.conn.commit()
        self.load_notes()

    def load_notes(self):
        """Load all notes and emit to QML"""
        self.cursor.execute("SELECT id, text FROM notes")
        notes = [{"id": row[0], "text": row[1]} for row in self.cursor.fetchall()]
        self.notesChanged.emit(notes)

app = QApplication(sys.argv)
engine = QQmlApplicationEngine()

backend = NotesBackend()
engine.rootContext().setContextProperty("backend", backend)

engine.load("notes.qml")

if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())
```



```q
// notes.qml
import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 400
    height: 300
    title: "Notes App"

    ListModel { id: notesModel }

    Column {
        anchors.fill: parent
        spacing: 10
        padding: 10

        TextField { id: noteInput; placeholderText: "Enter note" }

        Button {
            text: "Add Note"
            onClicked: {
                backend.add_note(noteInput.text)
                noteInput.text = ""
            }
        }

        ListView {
            anchors.fill: parent
            model: notesModel
            delegate: Row {
                spacing: 10
                Label { text: text }
                Button {
                    text: "Update"
                    onClicked: backend.update_note(id, "Updated: " + text)
                }
                Button {
                    text: "Delete"
                    onClicked: backend.delete_note(id)
                }
            }
        }
    }

    // Sync QML model with backend
    Connections {
        target: backend
        onNotesChanged: function(notes) {
            notesModel.clear()
            for (var i = 0; i < notes.length; i++) {
                notesModel.append(notes[i])
            }
        }
    }
}
```