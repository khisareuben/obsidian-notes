
```c++
import QtQuick

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Hello World")
    visibility: Window.Manimized



    Text {
        text: "The fox is white"
        font.pointSize: 25
        font.bold: true
        font.italic: true
        font.underline: true
        color: "green"
    }

}

```

```c++
Text {
        text: "The fox is white"
        wrapMode: Text.WrapAnywhere //Text.WordWrap
    }
    
Text {
        text: "The <b>fox</b> is white"
    }
    
//plain text is if you want everything to be literal <b> and not a html style   
Text {
        text: "The <b>fox</b> is white"
        textFormat: Text.PlainText 
         //Text.RichText is by default
    }

```