
# 🛠️ Step‑by‑Step Guide: C++ + QML in VS Code

## 🔹 1. Install Dependencies

Make sure you have Qt6 and build tools installed:



```bash
sudo apt update
sudo apt install qt6-base-dev qt6-declarative-dev qt6-tools-dev cmake build-essential
```

👉 This gives you Qt6 libraries, QML support, and CMake.

## 🔹 2. VS Code Extensions

Install these extensions:

- **CMake Tools** → handles builds
    
- **C++ (ms-vscode.cpptools)** → IntelliSense + debugging
    
- **QML Syntax Highlighting** → makes `.qml` files readable
    

## 🔹 3. Project Structure

Create a folder like:


```Code
myproject/
 ├── CMakeLists.txt
 ├── main.cpp
 ├── qml/
 │    └── main.qml
 └── .vscode/
      ├── launch.json
      └── settings.json
```

## 🔹 4. Sample Code

**main.cpp**



```cpp
#include <QGuiApplication>
#include <QQmlApplicationEngine>

int main(int argc, char *argv[]) {
    QGuiApplication app(argc, argv);
    QQmlApplicationEngine engine;
    engine.load(QUrl(QStringLiteral("qrc:/qml/main.qml")));
    if (engine.rootObjects().isEmpty())
        return -1;
    return app.exec();
}
```

**qml/main.qml**



```python
import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 400
    height: 300
    title: "Hello Qt6 + VS Code"

    Text {
        text: "Hello World!"
        anchors.centerIn: parent
    }
}
```

## 🔹 5. CMakeLists.txt



```python
cmake_minimum_required(VERSION 3.16)
project(MyQtApp VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Qml Quick)

qt_add_executable(MyQtApp
    main.cpp
)

qt_add_qml_module(MyQtApp
    URI MyApp
    VERSION 1.0
    QML_FILES qml/main.qml
)

target_link_libraries(MyQtApp PRIVATE Qt6::Core Qt6::Gui Qt6::Qml Qt6::Quick)
```

## 🔹 6. Build Commands

From VS Code terminal:



```bash
cmake -S . -B build
cmake --build build
```

👉 This compiles your project into `build/MyQtApp`.

## 🔹 7. Run the App



```bash
./build/MyQtApp
```

👉 Your QML window should appear.

## 🔹 8. Debugging in VS Code

Create `.vscode/launch.json`:



```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Launch Qt App",
      "type": "cppdbg",
      "request": "launch",
      "program": "${workspaceFolder}/build/MyQtApp",
      "cwd": "${workspaceFolder}",
      "args": [],
      "MIMode": "gdb",
      "setupCommands": [
        { "description": "Enable pretty-printing", "text": "-enable-pretty-printing" }
      ]
    }
  ]
}
```

👉 Now you can press **F5** to debug just like in Qt Creator.

## 📊 Quick Mapping (Qt Creator → VS Code)

|**Qt Creator Action**|**VS Code Equivalent**|
|---|---|
|New Project Wizard|Create folder + `CMakeLists.txt`|
|Kit Selection|Install compiler + set Qt path in CMake|
|Run Button|`launch.json` debug config|
|QML Designer|QML Syntax extension + manual coding|
|Build Button|`CMake: Build` command|

✅ With this setup, you can **build and run C++ + QML desktop apps entirely in VS Code**. It mirrors what Qt Creator does, but gives you more flexibility.