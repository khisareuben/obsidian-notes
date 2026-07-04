It is much more powerful than `text`

```c++
import QtQuick
import QtQuick.Controls

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Hello World")
    visibility: Window.Manimized



    Label{
        text: "I am the label"
        font.pointSize: 25
        padding: 23
        background: Rectangle{
            color: "green"
        }
    }

}

```