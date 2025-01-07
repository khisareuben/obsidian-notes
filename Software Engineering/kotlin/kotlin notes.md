
### Kotlin Programming Language

#### Introduction

Kotlin is a modern, statically-typed programming language that runs on the Java Virtual Machine (JVM) and can also be compiled to JavaScript and native code. It was developed by JetBrains and is officially supported by Google for Android development.

#### Key Features

1. **Concise Syntax**: Reduces boilerplate code, making it more readable and maintainable.
    
2. **Interoperability**: Fully interoperable with Java, allowing you to use existing Java libraries and frameworks.
    
3. **Null Safety**: Helps eliminate null pointer exceptions by distinguishing between nullable and non-nullable types.
    
4. **Coroutines**: Simplifies asynchronous programming by providing a cleaner way to manage background tasks.
    
5. **Smart Casts**: Automatically casts types without the need for explicit type checks.
    

#### Basic Syntax

kotlin

```kotlin
fun main() {
    println("Hello, World!")
}
```

- `fun`: Keyword used to declare a function.
    
- `main`: The name of the function. The entry point of a Kotlin application.
    
- `println`: Function to print text to the console.
    

#### Variables and Data Types

kotlin

```kotlin
val name: String = "Alice"      // Immutable variable
var age: Int = 30               // Mutable variable
var isStudent: Boolean = true   // Boolean variable
var height: Double = 5.9        // Double precision floating point variable

var weight: Float = 70.5f       // Single precision floating point variable

var initial: Char = 'A'         // Character variable
val score: Long = 123456789L    // Long integer variable

val smallNumber: Short = 42     // Short integer variable

val tinyNumber: Byte = 8        // Byte variable

```

- `val`: Declares a read-only (immutable) variable.
    
- `var`: Declares a read-write (mutable) variable.
    
- `String`, `Int`: Data types in Kotlin.
    

#### Functions

kotlin

```kotlin
fun add(a: Int, b: Int): Int {
    return a + b
}
```

- `fun`: Keyword to declare a function.
    
- `add`: Function name.
    
- `a: Int`, `b: Int`: Function parameters with their types.
    
- `Int`: Return type of the function.
    
- `return`: Keyword to return a value from the function.
    

#### Classes and Objects

kotlin

```kotlin
class Person(val name: String, var age: Int)

fun main() {
    val person = Person("Bob", 25)
    println(person.name) // Accessing properties
}
```

- `class`: Keyword to define a class.
    
- `Person`: Class name.
    
- `val name: String`, `var age: Int`: Properties of the class with their types.
    
- `person`: Object instantiation of the `Person` class.
    

#### Null Safety

kotlin

```kotlin
var nullableString: String? = null // Nullable type
nullableString?.length // Safe call operator
```

- `String?`: Nullable type declaration.
    
- `?.`: Safe call operator, used to access properties or methods safely on nullable types.
    

#### Coroutines

kotlin

```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking {
    launch {
        delay(1000L)
        println("World!")
    }
    println("Hello,")
}
```

- `runBlocking`: Starts a new coroutine and blocks the current thread until it completes.
    
- `launch`: Launches a new coroutine without blocking the current thread.
    
- `delay`: Suspends the coroutine for a specified time.
    

#### Interoperability with Java

kotlin

```kotlin
// Java class
public class JavaClass {
    public void sayHello() {
        System.out.println("Hello from Java!");
    }
}

// Kotlin code
fun main() {
    val javaClass = JavaClass()
    javaClass.sayHello() // Calling Java method from Kotlin
}
```

- Kotlin seamlessly integrates with Java, allowing you to call Java code from Kotlin and vice versa.