
## What Is `LocalContext.current` in Jetpack Compose?

In **Jetpack Compose**, `LocalContext.current` is how you access the **Android** `Context` inside a `@Composable` function.

### 🔹 What is `Context` in Android?

In traditional Android development, `Context` is an object that gives you access to:

- System services (like `ClipboardManager`, `LocationManager`)
    
- Resources (like strings, colors, dimensions)
    
- Starting activities or showing toasts
    
- Accessing databases, preferences, etc.
    

In an `Activity`, you’d normally use `this` or `applicationContext` to get it.