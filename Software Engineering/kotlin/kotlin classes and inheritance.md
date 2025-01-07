
```kotlin

class Phone(var brand: String, var ram: Int, var storage: Int, var network: String) {
    fun intro(){
        println("Brand : $brand")
        println("RAM : $ram")
        println("Storage : $storage")
        println("Network : $network")
    }
}

fun main() {
    var redmi = Phone("redmi", 16, 256, "5g")
    redmi.intro()
}

```


# inheritance

```kotlin

open class Product(val name: String, val price: Double) {
    open fun displayInfo() {
        println("Product: $name, Price: $$price")
    }
}


class Electronics(name: String, price: Double, val warranty: Int) : Product(name, price) {
    override fun displayInfo() {
        super.displayInfo()
        println("Warranty: $warranty years")
    }
}

class Clothing(name: String, price: Double, val size: String) : Product(name, price) {
    override fun displayInfo() {
        super.displayInfo()
        println("Size: $size")
    }
}

class Book(name: String, price: Double, val author: String) : Product(name, price) {
    override fun displayInfo() {
        super.displayInfo()
        println("Author: $author")
    }
}



```

**Note:**  when you use `super` is like calling the parent function together with the child function e.g. if the parent function was to print `complex` then just calling the child function will print `complex` and whatever is in the child function.
So in short you don't have to call the parent function coz the child function will do it 

so in the class below when you call the child function it will print two things  `product:` and `warranty:`
while when you remove `super` it will only print `warranty`

```kotlin

open class Product(val name: String, val price: Double) {
    open fun displayInfo() {
        println("Product: $name, Price: $$price")
    }
}

class ElectronicProduct(name: String, price: Double, val warranty: Int) : Product(name, price) {
    override fun displayInfo() {
        super.displayInfo()
        println("Warranty: $warranty months")
    }
}

fun main() {
    val electronicProduct = ElectronicProduct("Laptop", 1200.0, 24)
    electronicProduct.displayInfo()
}


```