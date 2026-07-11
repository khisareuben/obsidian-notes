
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



    Button{
        x: 200
        y: 200
        
        text: "click Me"
        
        leftPadding: 40
        rightPadding: 40
        topPadding: 20
        bottomPadding: 20


        background: Rectangle {
            radius: 5
            color: "green"
        }
    }

}

```

```c++
Button{
        
	leftPadding: 40
	rightPadding: 40
	topPadding: 20
	bottomPadding: 20

	contentItem: Label {
		text: "Click Me"
		font.pointSize: 25
		color: "darkblue"
	}

	background: Rectangle {
		id: backgroundRect
		radius: 5
		color: "green"
	}
	
	onClicked: {
		backgroundRect.color = "red"
	}

}

```