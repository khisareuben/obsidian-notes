
# QML Colors

## 1. Ways to Define Colors

### Named Colors

- Use standard SVG color names.
    
- Examples: `"red"`, `"green"`, `"lightsteelblue"`, `"transparent"`.
    

```q
Rectangle {
    color: "steelblue"
    width: 40; height: 40
}
```

### Hexadecimal Codes

- RGB triplet: `"#RRGGBB"` → `"#FF0000"` for red.
    
- ARGB quad: `"#AARRGGBB"` → `"#800000FF"` for semi-transparent blue.
    

```q
Rectangle {
    color: "#800000FF" // 50% transparent blue
}
```

### Qt Functions

- `Qt.rgba(r, g, b, a)` → values between 0–1.
    
- `Qt.hsva(h, s, v, a)` → hue, saturation, value.
    
- `Qt.hsla(h, s, l, a)` → hue, saturation, lightness.
    
- Transformations:
    
    - `Qt.darker(color, factor)`
        
    - `Qt.lighter(color, factor)`
        
    - `Qt.tint(base, overlay)`
        

```q
Rectangle {
    color: Qt.rgba(0.2, 0.6, 0.8, 1.0) // teal-like color
}
```

---

## 2. Best Practices

- Avoid hardcoding colors everywhere.
    
- Define them centrally in a theme file.
    
- Use Qt Quick Controls 2 palettes (Material, Fusion).
    

```q
ApplicationWindow {
    Material.theme: Material.Dark
    Material.primary: "#6200EE"
}
```

---

## 3. Theme Example

```q
// Theme.qml
QtObject {
    property color primary: "#000000"
    property color accent: "#FFD700"
}

// Usage
Rectangle {
    color: Theme.primary
    border.color: Theme.accent
}
```

---

## 4. Comparison Table

|Method|Example|Pros|Cons|
|---|---|---|---|
|Named Colors|`"red"`|Easy, readable|Limited set|
|Hex Codes|`"#FF0000"`|Precise, standard|Harder to read|
|Qt Functions|`Qt.rgba(1,0,0,1)`|Flexible, supports alpha|Verbose|
|Theme Properties|`Theme.primary`|Centralized, scalable|Requires setup|

---

## 5. Key Takeaways

- Colors in QML can be defined by names, hex codes, or Qt functions.
    
- Centralize color definitions for consistency.
    
- Use themes for branding and easy light/dark mode switching.