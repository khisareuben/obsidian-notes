# PySide6 - Animation in QWidget - Complete Notes

> PySide6 animates QWidgets by interpolating **QObject properties** over time. There is no CSS keyframes-like system - you use `QPropertyAnimation` and animation groups.

## 1. Core Concepts

### The Animation Framework
All animation classes inherit from `QAbstractAnimation`.

- **QPropertyAnimation**: Animates a single property of a QObject (e.g., `pos`, `geometry`, `windowOpacity`)
- **QVariantAnimation**: Base class - animates a QVariant, you override `updateCurrentValue()`
- **QAnimationGroup**: Groups multiple animations
  - **QParallelAnimationGroup**: Runs animations in parallel
  - **QSequentialAnimationGroup**: Runs animations one after another
- **QPauseAnimation**: Insert a delay in a sequential group

**How it works:**
1. You pick a property that has a setter (via `setPropertyName`)
2. Set start/end values
3. Set duration (ms) and easing curve
4. Call `start()`

> You MUST keep a reference to the animation object in Python (e.g., `self.anim = ...`). If it gets garbage collected, it stops immediately.

### Requirements for a property to be animatable
1. Must be a `Q_PROPERTY` with a setter, OR
2. A dynamic property you added, but QWidget built-ins are best:
   - `pos` (QPoint)
   - `size` (QSize)
   - `geometry` (QRect)
   - `windowOpacity` (float 0.0-1.0)
   - `minimumWidth`, `maximumWidth`, etc.
   - `styleSheet` - NOT animatable directly

## 2. Basic Setup

```python
from PySide6.QtWidgets import QWidget, QPushButton
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QRect

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.button = QPushButton("Move me", self)

        self.anim = QPropertyAnimation(self.button, b"geometry")
        self.anim.setDuration(500) # ms
        self.anim.setStartValue(QRect(0, 0, 100, 30))
        self.anim.setEndValue(QRect(200, 100, 100, 30))
        self.anim.setEasingCurve(QEasingCurve.OutBounce)
        self.anim.start()
```

`b"geometry"` - property name must be bytes in PySide6.

## 3. The Most Useful QWidget Properties to Animate

| Property | Type | Use case |
| :--- | :--- | :--- |
| `b"pos"` | QPoint | Slide/move |
| `b"size"` | QSize | Grow/shrink |
| `b"geometry"` | QRect | Move + resize at once |
| `b"windowOpacity"` | float | Fade in/out (needs `setWindowOpacity`) |
| `b"maximumHeight"` | int | Smooth expand/collapse accordion |
| `b"minimumWidth"` | int | Sidebar slide |

**Note on `windowOpacity`:** Only works on top-level windows by default. For child widgets, use `QGraphicsOpacityEffect`.

## 4. Fade In / Fade Out for Child Widgets

Child QWidgets don't support `windowOpacity`. You need an effect:

```python
from PySide6.QtWidgets import QGraphicsOpacityEffect
from PySide6.QtCore import QPropertyAnimation

def fade_in(widget, duration=300):
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)
    
    anim = QPropertyAnimation(effect, b"opacity")
    anim.setDuration(duration)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setEasingCurve(QEasingCurve.InOutQuad)
    anim.start()
    widget._fade_anim = anim # keep reference!
    widget._fade_effect = effect
    return anim

def fade_out(widget, duration=300):
    effect = widget.graphicsEffect()
    if not isinstance(effect, QGraphicsOpacityEffect):
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)

    anim = QPropertyAnimation(effect, b"opacity")
    anim.setDuration(duration)
    anim.setStartValue(effect.opacity())
    anim.setEndValue(0.0)
    anim.start()
    widget._fade_anim = anim
    return anim
```

## 5. QEasingCurve - The Secret Sauce

Easing makes it feel natural. Always set one.

Common curves:
- `Linear` - robotic, constant speed
- `InQuad`, `OutQuad`, `InOutQuad` - standard smooth (best for UI)
- `OutCubic`, `InOutCubic` - slightly more natural
- `OutExpo` - fast start, gentle stop (modern UI)
- `OutBounce` - playful bounce
- `OutBack` - overshoots slightly (pop effect)

```python
self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
# Or custom:
curve = QEasingCurve(QEasingCurve.Type.OutBounce)
curve.setAmplitude(1.5)
self.anim.setEasingCurve(curve)
```

## 6. Animation Groups

### Parallel - Animate multiple properties at once
```python
from PySide6.QtCore import QParallelAnimationGroup, QPropertyAnimation

group = QParallelAnimationGroup()

pos_anim = QPropertyAnimation(self.card, b"pos")
pos_anim.setDuration(400)
pos_anim.setEndValue(QPoint(50, 50))

opacity_effect = QGraphicsOpacityEffect(self.card)
self.card.setGraphicsEffect(opacity_effect)
opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
opacity_anim.setDuration(400)
opacity_anim.setEndValue(1.0)

group.addAnimation(pos_anim)
group.addAnimation(opacity_anim)
group.start()
self.group = group
```

### Sequential - Chain animations
```python
from PySide6.QtCore import QSequentialAnimationGroup, QPauseAnimation

seq = QSequentialAnimationGroup()

anim1 = QPropertyAnimation(self.btn, b"pos")
anim1.setDuration(200)
anim1.setEndValue(QPoint(100, 0))

pause = QPauseAnimation(100) # wait 100ms

anim2 = QPropertyAnimation(self.btn, b"pos")
anim2.setDuration(200)
anim2.setEndValue(QPoint(100, 100))

seq.addAnimation(anim1)
seq.addAnimation(pause)
seq.addAnimation(anim2)
seq.start()
self.seq = seq
```

## 7. Sliding / Accordion / Sidebar Pattern

Most common UI animation: animate `maximumHeight` for vertical collapse.

```python
def toggle_height(widget, collapsed_height=0, expanded_height=200, duration=250):
    start = widget.maximumHeight()
    end = expanded_height if start == collapsed_height else collapsed_height

    anim = QPropertyAnimation(widget, b"maximumHeight")
    anim.setDuration(duration)
    anim.setStartValue(start)
    anim.setEndValue(end)
    anim.setEasingCurve(QEasingCurve.InOutQuad)
    anim.start()
    widget._anim = anim
```

For sidebar: animate `maximumWidth` or `pos` depending on layout.

> If using QLayout, animating `geometry`/`pos` directly will fight the layout. Animate `maximumWidth`/`maximumHeight` or `minimumWidth` instead.

## 8. QVariantAnimation - Custom Animations

When you need to animate something that's not a property (like color, stylesheet).

```python
from PySide6.QtCore import QVariantAnimation
from PySide6.QtGui import QColor

class ColorAnimation(QVariantAnimation):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.valueChanged.connect(self.on_value_changed)

    def on_value_changed(self, color):
        # color is a QColor interpolated
        self.widget.setStyleSheet(f"background-color: {color.name()};")

anim = ColorAnimation(my_widget)
anim.setStartValue(QColor("#2a2a2a"))
anim.setEndValue(QColor("#ff5500"))
anim.setDuration(500)
anim.start()
my_widget._anim = anim
```

## 9. Signals to Know

```python
anim.finished.connect(lambda: print("done"))
anim.stateChanged.connect(lambda new, old: ...)
anim.valueChanged.connect(lambda value: ...)

# For chaining
anim.finished.connect(next_anim.start)

# Stop / Pause
anim.stop()
anim.pause()
anim.resume()
```

Set loop count:
```python
anim.setLoopCount(-1) # infinite
anim.setLoopCount(3) # 3 times
```

## 10. Common Gotchas in PySide6

1.  **GC Kills Animation**: Always do `self.anim = anim`. Local variable dies -> animation stops at frame 1.

2.  **Layout vs Geometry**: If widget is in a layout, `setGeometry`/`pos` animation will be overridden on next resize. Solution: animate `maximumSize`, or put widget inside a container with no layout, or animate the container.

3.  **Opacity on child widgets**: Must use `QGraphicsOpacityEffect`. Don't forget `setGraphicsEffect`.

4.  **b"" bytes**: PySide6 requires `b"propertyName"` not `"propertyName"` for QPropertyAnimation. PyQt6 accepts both, PySide6 is strict.

5.  **StyleSheet animation**: You CANNOT animate `styleSheet` property. It doesn't interpolate. Use QVariantAnimation and set stylesheet in `valueChanged`.

6.  **Performance**: `QGraphicsOpacityEffect` is somewhat expensive. For many widgets, prefer animating `maximumHeight` for hide/show instead of fading 50 items.

7.  **Animation on deletion**: If you animate then `deleteLater()`, connect to `finished`:
    ```python
    anim.finished.connect(widget.deleteLater)
    ```

## 11. Full Example - Animated Sliding Panel

```python
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QFrame, QVBoxLayout
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QPoint
import sys

class SlidingDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QWidget Animation")
        self.resize(400, 300)

        self.panel = QFrame(self)
        self.panel.setStyleSheet("background: #4a90e2; border-radius: 12px;")
        self.panel.setGeometry(0, 0, 100, 300)
        
        self.btn = QPushButton("Toggle", self)
        self.btn.move(150, 130)
        self.btn.clicked.connect(self.toggle)

        self.is_open = True

    def toggle(self):
        self.anim = QPropertyAnimation(self.panel, b"pos")
        self.anim.setDuration(350)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        
        start = self.panel.pos()
        end = QPoint(-100, 0) if self.is_open else QPoint(0, 0)
        
        self.anim.setStartValue(start)
        self.anim.setEndValue(end)
        self.anim.start()
        self.is_open = not self.is_open

app = QApplication(sys.argv)
w = SlidingDemo()
w.show()
app.exec()
```

## 12. Cheat Sheet

**I want to...**
- Slide a widget: `QPropertyAnimation(widget, b"pos")`
- Fade: `QGraphicsOpacityEffect` + animate `b"opacity"`
- Grow/shrink smoothly in layout: animate `b"maximumHeight"` / `b"maximumWidth"`
- Shake on error: sequential pos animation left-right-left
- Animate multiple things together: `QParallelAnimationGroup`
- Wait between steps: `QPauseAnimation` in `QSequentialAnimationGroup`

---

### Further Reading
- Qt Docs: `QPropertyAnimation`, `QAbstractAnimation`, `QEasingCurve`
- For QML-like animations in Widgets, check out `QTimeLine` (older API but still useful for progress-based animation)

*Generated for PySide6 6.6+ / Python 3.10+*
