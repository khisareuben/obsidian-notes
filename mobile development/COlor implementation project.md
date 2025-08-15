
## Goal

Create a UI like this:

Code

```
🔴 High ▼
🟡 Medium ▼
🟢 Low ▼
```

Where:

- The **dot color** reflects the selected priority.
    
- The **dropdown** lets the user change the priority.
    
- The UI updates reactively.
    

## 🧱 Step-by-Step Implementation in Jetpack Compose

### 1. Define Priority Enum


```kotlin

enum class Priority(val label: String, val color: Color) {
    HIGH("High", Color.Red),
    MEDIUM("Medium", Color.Yellow),
    LOW("Low", Color.Green)
}
```

### 2. Create State in Your Composable



```kotlin
@Composable
fun PrioritySelector(
    modifier: Modifier = Modifier,
    initialPriority: Priority = Priority.MEDIUM,
    onPrioritySelected: (Priority) -> Unit
) {
    var expanded by remember { mutableStateOf(false) }
    var selectedPriority by remember { mutableStateOf(initialPriority) }

    Box(modifier = modifier) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier
                .clickable { expanded = true }
                .padding(8.dp)
        ) {
            // Colored dot
            Box(
                modifier = Modifier
                    .size(12.dp)
                    .background(selectedPriority.color, shape = CircleShape)
            )

            Spacer(modifier = Modifier.width(8.dp))

            Text(text = selectedPriority.label)

            Spacer(modifier = Modifier.width(4.dp))

            Icon(Icons.Default.ArrowDropDown, contentDescription = null)
        }

        DropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false }
        ) {
            Priority.values().forEach { priority ->
                DropdownMenuItem(
                    onClick = {
                        selectedPriority = priority
                        expanded = false
                        onPrioritySelected(priority)
                    }
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(12.dp)
                                .background(priority.color, shape = CircleShape)
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(text = priority.label)
                    }
                }
            }
        }
    }
}
```

### 3. Use It in Your Screen



```kotlin
@Composable
fun TaskScreen() {
    var priority by remember { mutableStateOf(Priority.MEDIUM) }

    PrioritySelector(
        initialPriority = priority,
        onPrioritySelected = { newPriority ->
            priority = newPriority
            // You can also update your ViewModel or DB here
        }
    )
}
```

## 🧠 What’s Happening

- The **colored dot** is a `Box` with a dynamic `background` color.
    
- The **dropdown** is a `DropdownMenu` populated with `Priority.values()`.
    
- When a priority is selected, the state updates and the UI re-renders.
    

## 🧪 Bonus: Make It Reusable

You can extract the `PrioritySelector` into a reusable component and even style it with custom typography, icons, or animations.

Would you like to integrate this into your Post project as a priority field for tasks or posts? I can help you wire it up with Room and ViewModel too.