
### The Fix

In your `main.qml` file, locate the **`RowLayout`** delegate inside the `verseListView` and change the alignment properties to use `Layout.alignment`:

#### Change This:

QML

```
// Verse Marker
Text {
    text: model.num
    font.pixelSize: 11
    font.bold: true
    color: accentGreen
    alignment: Qt.AlignTop       // ❌ Error! "alignment" does not exist here
    Layout.preferredWidth: 20
    horizontalAlignment: Text.AlignRight
}
```

#### To This:

QML

```
// Verse Marker
Text {
    text: model.num
    font.pixelSize: 11
    font.bold: true
    color: accentGreen
    Layout.alignment: Qt.AlignTop //  Fixed! Uses the attached property Layout.
    Layout.preferredWidth: 20
    horizontalAlignment: Text.AlignRight
}
```

Make sure to apply the same change to any other layout children (e.g., if you used `alignment` anywhere else instead of `Layout.alignment`). Once you make this adjustment, run your python file again and the app will load successfully!