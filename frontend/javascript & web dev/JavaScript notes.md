
### JavaScript Basics

#### What is JavaScript?

JavaScript is a versatile, high-level programming language primarily used for web development. It allows you to create interactive and dynamic web pages.

#### Key Concepts

1. **Variables**: Used to store data values.
    
    JavaScript
    
    ```javascript
    let name = "John";
    const age = 30;
    var isStudent = true;

	to find the length of a variable
	var NameLength = name.length
    ```
    
    AI-generated code. Review and use carefully. .
    
2. **Data Types**: Common types include strings, numbers, booleans, objects, and arrays.
    
    JavaScript
    
    ```javascript
    let message = "Hello, World!"; // String
    let count = 42; // Number
    let isActive = false; // Boolean
    let user = { name: "Alice", age: 25 }; // Object
    let colors = ["red", "green", "blue"]; // Array

	add and remove
	push() //add at the end of an array
	pop() // remove at the end
	unshift() // add at the beginning
	shift() // remove at the beginning
    ```
    
    
3. **Functions**: Blocks of code designed to perform a particular task.
    
    JavaScript
    
    ```javascript
    function greet(name) {
        return `Hello, ${name}!`;
    }
    console.log(greet("Alice")); // Output: Hello, Alice!

// to turn an array into a string
let fruits = ["Apple", "Banana", "Cherry"];
let jsonString = JSON.stringify(fruits);
console.log(jsonString); // Outputs: '["Apple","Banana","Cherry"]'

    ```
    
    AI-generated code. Review and use carefully. .


1. **objects**: this is same a dictionaries in python 

```javascript
var object = {
	"name" : "Reuben",
	"school": "Jooust",
	"home" : "Mariakani"
}

var results = object.name //or
var results = object["name"]
```



    
4. **Control Structures**: Includes conditionals and loops.
    
    JavaScript
    
    ```javascript
    // Conditional
    if (age > 18) {
        console.log("Adult");
    } else {
        console.log("Minor");
    }
    
    // Loop
    for (let i = 0; i < 5; i++) {
        console.log(i);
    }
    ```



### While Loop

A `while` loop repeats a block of code as long as a specified condition is true.

javascript

Copy

```javascript
let count = 0;
while (count < 5) {
    console.log(count);
    count++;
}
```

_This will print numbers 0 to 4._

### Objects

Objects are collections of properties, defined using key-value pairs.

javascript

Copy

```javascript
let car = {
    make: 'Toyota',
    model: 'Corolla',
    year: 2020
};
console.log(car.make);  // Outputs: Toyota
```

### Classes and Inheritance

Classes are templates for creating objects, and they can use inheritance to extend other classes.

javascript

Copy

```javascript
class Animal {
    constructor(name) {
        this.name = name;
    }

    speak() {
        console.log(`${this.name} makes a sound.`);
    }
}

class Dog extends Animal {
    speak() {
        console.log(`${this.name} barks.`);
    }
}

let dog = new Dog('Rex');
dog.speak();  // Outputs: Rex barks.
```

These basic examples should get you started. Anything specific you want to dive deeper into?
    
5. **Events**: Actions that can be detected by JavaScript, such as clicks or key presses.
    
    JavaScript
    
    ```javascript
    document.getElementById("myButton").addEventListener("click", function() {
        alert("Button clicked!");
    });
    ```
    
    AI-generated code. Review and use carefully. .
    

#### Advanced Topics

1. **Asynchronous JavaScript**: Handling operations that take time to complete, like fetching data from an API.
    
    JavaScript
    
    ```javascript
    // Using Promises
    fetch('https://api.example.com/data')
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
    
    // Using async/await
    async function fetchData() {
        try {
            let response = await fetch('https://api.example.com/data');
            let data = await response.json();
            console.log(data);
        } catch (error) {
            console.error('Error:', error);
        }
    }
    fetchData();
    ```
    
    AI-generated code. Review and use carefully. .
    
2. **DOM Manipulation**: Changing the content and structure of the web page.
    
    JavaScript
    
    ```javascript
    let element = document.getElementById("myElement");
    element.textContent = "New Content";
    element.style.color = "blue";
    ```
    
    AI-generated code. Review and use carefully. .
    
3. **ES6 Features**: Modern JavaScript features like arrow functions, template literals, and destructuring.
    
    JavaScript
    
    ```javascript
    // Arrow Function
    const add = (a, b) => a + b;
    
    // Template Literals
    let greeting = `Hello, ${name}!`;
    
    // Destructuring
    let { name, age } = user;
    ```
    
