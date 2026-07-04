
```c++
import QtQuick

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Hello World")
    visibility: Window.Manimized



    Rectangle {
        width: 100
        height: 100
        color: "green"
        radius: 6
    }

}

```

To take the width and height of its parent component
```c++
Rectangle {
        width: parent.width
        height: parent.height
        color: "green"
    }
    
Rectangle {
        anchors.fill: parent
        color: "green"
    }
```

```c++
Rectangle {
	anchors.fill: parent
	gradient: Gradient {
			orientation: Qt.Horizontal //by default the gradient is vertical
			GradientStop { position: 0.0; color: "red" }
			GradientStop { position: 0.33; color: "yellow" }
			GradientStop { position: 1.0; color: "green" }
		}
}
```