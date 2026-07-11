
First you need to add the image in the .qrc file:
create a new folder(assets) > import the image into the assets folder > 
create a new file > choose the qt resource file > open the .qrc file > add a prefix > then add the image file

your resource file should automatically be included in the `CMakeLists.txt` when you created it 
add `set(CMAKE_AUTORCC ON)` in the **CMakeLists.txt**

```c++
import QtQuick

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Hello World")
    visibility: Window.Manimized


    
    Image {
        width: 500
        height: 500
        source: "qrc:/new/prefix1/source/duck_doctor.jpg"
    }
}

```

```c++
Image{
	anchors.fill: parent
	source: "qrc:/new/prefix1/source/duck_doctor.jpg"
	fillMode: Image.PreserveAspectFit // Image.PreserveAspectCrop, Image.Stretch
}
```