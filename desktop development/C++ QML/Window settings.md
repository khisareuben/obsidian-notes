
#### for window to open in maximized mode

```c++
import QtQuick

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Hello World")
    visibility: Window.Manimized //Minimized, FullScreen

}
```

You can use `flags` to gain more control on the windows behavior

```c++
import QtQuick

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Hello World")
    visibility: Window.Manimized //Minimized, FullScreen
    
    flags: Qt.Window | Qt.WindowStaysOnTopHint | Qt.WindowTitleHint | Qt.WindowSystemMenuHint
    | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint


}
```