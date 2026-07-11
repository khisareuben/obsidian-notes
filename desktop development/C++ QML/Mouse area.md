It is used to define click events and hover events on any element

```c++
import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Hello World")
    visibility: Window.Manimized



    Rectangle {
        id: recty
        color: "green"
        anchors.centerIn: parent
        width: 100
        height: 100

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            onEntered: {
                recty.color = "black"
            }
            onExited: {
                recty.color = "blue"
            }
            onClicked: {
                console.log("Rectangle clicked")
            }
            onDoubleClicked: {}
        }
        
    }

}

```