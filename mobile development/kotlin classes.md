

## 1. Regular Class in Kotlin

### 🔍 What Is It?

A **regular class** in Kotlin is the most basic building block of object-oriented programming. It defines a blueprint for creating objects, encapsulating **properties (data)** and **functions (behavior)**.

### 🛠️ Syntax


```kotlin

class Car(val brand: String, var year: Int) {
    fun honk() {
        println("Beep! Beep!")
    }
}
```

### 🧪 Example Usage



```kotlin
fun main() {
    val myCar = Car("Toyota", 2020)
    println("Brand: ${myCar.brand}, Year: ${myCar.year}")
    myCar.honk()
}
```

### 📌 Key Concepts

- **Primary Constructor**: Declared in the class header.
    
- **Secondary Constructor**: Optional, used for additional initialization.
    
- **Properties**: Declared with `val` (read-only) or `var` (mutable).
    
- **Methods**: Functions defined inside the class.
    

### 🧠 Use Case

Use regular classes when you need to model real-world entities with both data and behavior, like `User`, `Product`, or `Vehicle`.

## 📦 2. Data Class

### 🔍 What Is It?

A **data class** is a concise way to create classes that are **primarily used to hold data**. Kotlin automatically generates:

- `equals()`
    
- `hashCode()`
    
- `toString()`
    
- `copy()`
    
- `componentN()` functions
    

### 🛠️ Syntax



```kotlin
data class User(val name: String, val age: Int)
```

### 🧪 Example Usage



```kotlin
val user1 = User("Alice", 25)
val user2 = user1.copy(age = 26)
println(user1) // User(name=Alice, age=25)
println(user2) // User(name=Alice, age=26)
```

### 📌 Key Concepts

- Must have at least one `val` or `var` in the primary constructor.
    
- Cannot be `abstract`, `open`, `sealed`, or `inner`.
    

### 🧠 Use Case

Ideal for modeling immutable data structures like API responses, DTOs, or simple state holders.

## 🧭 3. Sealed Class

### 🔍 What Is It?

A **sealed class** restricts class hierarchies. All subclasses must be defined in the same file. This enables **exhaustive** `when` **expressions** without needing an `else`.

### 🛠️ Syntax



```kotlin
sealed class Result
data class Success(val data: String) : Result()
data class Error(val exception: Exception) : Result()
object Loading : Result()
```

### 🧪 Example Usage



```kotlin
fun handle(result: Result) = when (result) {
    is Success -> println("Data: ${result.data}")
    is Error -> println("Error: ${result.exception}")
    Loading -> println("Loading...")
}
```

### 📌 Key Concepts

- Cannot be instantiated directly.
    
- Useful for modeling **finite state machines** or **UI states**.
    

### 🧠 Use Case

Use when you want to represent a **closed set of types**, like network responses (`Success`, `Error`, `Loading`).

## 🧱 4. Abstract Class

### 🔍 What Is It?

An **abstract class** cannot be instantiated. It can contain both **abstract members** (no implementation) and **concrete members** (with implementation).
In short you can write an abstract function in an abstract class without writing the implementation in the function but you can override it in another class or somewhere else

### 🛠️ Syntax



```kotlin
abstract class Animal {
    abstract fun makeSound()
    fun breathe() = println("Breathing...")
}
```

### 🧪 Example Usage



```kotlin
class Dog : Animal() {
    override fun makeSound() = println("Woof!")
}
```

### 📌 Key Concepts

- Use `abstract` keyword.
    
- Subclasses must implement abstract members.
    

### 🧠 Use Case

Use when you want to define a **base class with shared behavior** but require subclasses to implement specific functionality.

## 🔓 5. Open Class

### 🔍 What Is It?

By default, Kotlin classes are `final` (cannot be inherited). Use the `open` keyword to allow inheritance.

### 🛠️ Syntax



```kotlin
open class Vehicle {
    open fun start() = println("Starting vehicle...")
}
```

### 🧪 Example Usage



```kotlin
class Car : Vehicle() {
    override fun start() = println("Starting car...")
}
```

### 📌 Key Concepts

- `open` must be used on both class and methods to allow overriding.
    

### 🧠 Use Case

Use when you want to allow **customization through inheritance**.

## 🧬 6. Nested and Inner Classes

### 🔍 What Are They?

- **Nested Class**: Static by default, no access to outer class.
    
- **Inner Class**: Has access to outer class members.
    

### 🛠️ Syntax



```kotlin
class Outer {
    private val secret = "Outer secret"

    class Nested {
        fun greet() = "Hello from Nested"
    }

    inner class Inner {
        fun reveal() = "Accessing: $secret"
    }
}
```

### 🧪 Example Usage



```kotlin
val nested = Outer.Nested().greet()
val inner = Outer().Inner().reveal()
```

### 🧠 Use Case

Use **nested** for grouping logic; use **inner** when you need access to the outer class.

## 🎖️ 7. Enum Class

### 🔍 What Is It?

An **enum class** defines a fixed set of constants. Each constant is an object.

### 🛠️ Syntax



```kotlin
enum class Direction {
    NORTH, SOUTH, EAST, WEST
}
```

### 🧪 Example Usage



```kotlin
val dir = Direction.NORTH
println(dir.name) // "NORTH"
```

### 📌 Key Concepts

- Can have properties and methods.
    
- Can implement interfaces.
    

### 🧠 Use Case

Use for **fixed sets of values**, like days of the week, directions, or states.

## ⚡ 8. Inline (Value) Class

### 🔍 What Is It?

An **inline class** wraps a single value and avoids object allocation at runtime. Used for **type safety without performance cost**.

### 🛠️ Syntax



```kotlin
@JvmInline
value class UserId(val id: String)
```

### 🧪 Example Usage



```kotlin
fun greet(userId: UserId) = println("Hello ${userId.id}")
```

### 📌 Key Concepts

- Must have a single property.
    
- Cannot have mutable state or inheritance.
    

### 🧠 Use Case

Use when you want **type safety** for primitives (e.g., `UserId`, `Email`) without runtime overhead.

## 🧍 9. Object Declaration

### 🔍 What Is It?

An **object declaration** creates a **singleton**. It’s initialized lazily and thread-safe.

### 🛠️ Syntax



```kotlin
object Logger {
    fun log(msg: String) = println("Log: $msg")
}
```

### 🧪 Example Usage



```kotlin
Logger.log("App started")
```

### 🧠 Use Case

Use for **single-instance utilities**, like `Logger`, `Config`, or `DatabaseManager`.

## 👯 10. Companion Object

### 🔍 What Is It?

A **companion object** is a singleton tied to a class. It allows defining **static-like members**.

### 🛠️ Syntax



```kotlin
class User(val name: String) {
    companion object {
        fun create(name: String) = User(name)
    }
}
```

### 🧪 Example Usage



```kotlin
val user = User.create("Alice")
```

### 🧠 Use Case

Use for **factory methods**, constants, or static utilities related to a class.