
This will all be the full notes on python basics and most of it will be shortened but still have the key things to learn and practice python code.

# Table of Contents

# Table of Contents

| 1. [[python full notes#variables]] | 2. [[python full notes#Typecasting]] | 3. [[python full notes#User Input]] |
|------------------------------------|--------------------------------------|-------------------------------------|
| 4. [[python full notes#arithmetic operators]] | 5. [[python full notes#if statement]] | 6. [[python full notes#Match-case statement(switch)]] |
| 7. [[python full notes#logical operators]] | 8. [[python full notes#conditional expressions]] | 9. [[python full notes#string indexing]] |
| 10. [[python full notes#format specifiers]] | 11. [[python full notes#while loop]] | 12. [[python full notes#for loop]] |
| 13. [[python full notes#nested loop]] | 14. [[python full notes#collection]] | 15. [[python full notes#2D list]] |
| 16. [[python full notes#Dictionary]] | 17. [[python full notes#random module]] | 18. [[python full notes#functions]] |
| 19. [[python full notes#variable scope]] | 20. [[python full notes#Membership operators]] | 21. [[python full notes#list comprehension]] |
| 22. [[python full notes#modules]] | 23. [[python full notes#Object oriented programming]] | 24. [[python full notes#Inheritance]] |
| 25. [[python full notes#Super function]] | 26. [[python full notes#polymorphism]] | 27. [[python full notes#static methods]] |
| 28. [[python full notes#Class methods]] | 29. [[python full notes#magic methods]] | 30. [[python full notes#property decorators]] |
| 31. [[python full notes#Decorators]] | 32. [[python full notes#exception]] | 33. [[python full notes#File Handling]] |
| 34. [[python full notes#1. File detection]] | 35. [[python full notes#2. Writing files]] | 36. [[python full notes#3. Reading files]] |



To print the output on the screen

```python
print("I like ramen")
```

#### variables
variable is a container for a value(string, integer, float, boolean)

```python
food = "Ramen" #string
number = 25 #integer
price = 10.99 #float
is_student = True #boolean
is_not_student = False #boolean

print(f"I like {food}") #a formatted string

```


#### Typecasting 
is the process of converting a variable from one data type to another str(), int(), float(), bool()

```python
food = "Ramen"
number = 25
price = 10.99
is_student = True

print(type(food)) #to check the data type
number = float(number) #converting to float
price = int(price) #converting to interger
number = str(number) #converting to string
food = bool(food) #converting to boolean
```

#### User Input
A function that prompts the user to enter data. and returns the entered data as a string

```python
name = input("What is your name?: ")
age = int(input("How old are you?: "))
  
print(f"Hello {name}")
print(f"you are {age} years old")
```

#### arithmetic operators

```python
friends = 0
friends += 1 #argumented assignment operator (friends = friends + 1)
friends -= 2 # friends = friends - 2
friedns *= 2 #friends = friends * 2
friends /= 2 #friends = friends / 2
friends **= 2 # friends = friends ** 2 (to the power of 2) or pow(friends, 2)
friends %= 2 #friends = friends % 2 (gives you the remainder after division)
```

#### if statement

```python
age = int(input("Enter your age: "))

if age >= 18:
	print("You are now signed up!")
elif age < 0:
	print("You haven't been born yet!")
else:
	print("You must be 18+ to sign up")
```

#### Match-case statement(switch)
An alternative to using many 'elif' statements. Executes some code if a value matches a 'case'
```python
def switch_example(value):
    match value:
        case "a":
            return "Option A selected"
        case "b":
            return "Option B selected"
        case "c":
            return "Option C selected"
        case _:
            return "Default option"

print(switch_example("b"))  # Output: Option B selected

```

#### logical operators
Evaluates multiple conditions(or, and, not)
or = at least one condition must be True
and = both conditions must be True
not = inverts the condition(not False, not True)

```python
temp = 25
is_raining = False

if temp > 35 or temp < 0 or is_raining:
	print("The outdoor event is cancelled")
elif temp >= 28 and is_raining is False:
	print("It's hot outside")
else:
	print("The outdoor even is still scheduled")
```

#### conditional expressions 
A one-line shortcut for the if-else statement(ternary operator). Print or assign one of two values based on a condition.
X if condition else Y

```python
num = 5
result = "Even" if num % 2 == 0 else "ODD" #returns even if the condition is True
print(result)
```

#### string indexing
indexing = accessing element of a sequence using [] (indexing operator) 
[start : end : step]

```python
credit_number = "1234-5678-9012-3456"

print(credit_number[0]) #gets the first index
print(credit_number[:4]) #gets 1234
print(credit_number[5:9]) #gets 5678
print(credit_number[5:]) #gets 5 going to the end
print(credit_number[-1]) #gets the last digit which is 6
print(credit_number[::3]) #chooses from first to last jumping 3 steps each
```

#### format specifiers 
{value:flags} format a value based on what flags are inserted
.(number)f = round to that many decimal places(fixed point)
:(number) = allocate that many spaces
:03 = allocate and zero pad that many spaces
:< = left justify
:>= right justify
:^ = center align
:+ = use a plus sign to indicate positive value
:= = place sign to left most position
: = insert a space before positive numbers
:, = comma separator

```python
price = 3.14159

print(f"Price is {price:.2f}") #2 decimal spaces
print(f"Price is {price:10}") #the output will take 10 spaces(7filled spaces with the values and 3 empty)
print(f"Price is {price:010}") #now the 3 empty spaces will be filled with zeros
print(f"Price is {price:<10}") #(numbers are justified on the left)the empty spaces will be on the right
print(f"Price is {price:>10}") #the empty spaces will be on the left
print(f"Price is {price:^10}") #(number are justified on the right)the number will be aligned at the center
print(f"Price is {price:+}") #the numbers will be preceded with a positive(+)
print(f"Price is {price: }") #the numbers will be precede with a space
print(f"Price is {price:,}") #it will add , to the number e.g 3,000
```


#### while loop
Execute some code while some conditions remains true
```python
number = 1

while number <= 5:
	print("Number going up")
	number +=1
print("end of the loop") 
```

#### for loop
execute a block of code a fixed number of time. You can iterate over a range, sequence, etc.
```python
food = "Ramen"

for x in food:
	print(x)
	
#another example
for x in range(1, 11):
	print(x) #or print(x, end="")
```

#### nested loop
a loop within another loop(outer, inner)
```python
for x in range(3):
	for y in range(1,10):
		print(y, end="")
	print()
```

#### collection
single variable use to store multiple values
- List = [] ordered and changeable. Duplicates OK
- Set  = {} unordered and immutable, but add/remove OK. No dupicates
- Tuple = () ordered and unchangeable. Duplicates OK. Faster
```python
fruits = ["mango", "banana", "coconut"]
print(fruits)
print(fruits[1])
#print(dir(fruits)) to see the methods on sets/list/tuples
# fruits[0] = "pineapple"
# fruits.append("pineapple")
#fruits.remove("apple")
#fruits.insert(0, "tomato")
#fruits.sort()
#fruits.reverse()
#fruits.clear()
#print(fruits.index("apple"))
#print(fruits.count("banana"))
fruits = {"mango", "banana", "coconut"} #set.
fruits = ("mango", "banana", "coconut") #tuple
```

#### 2D list

```python
groceries = [["apple", "orange", "banana", "coconut"],
			["celery", "carrots", "potatoes"],
			["chicken", "fish", "turkey"]]

for collection in groceries:
	for food in collection:
		print(food, end=" ")
	print()
```

quiz game 3:03:19

#### Dictionary
A collection of {key:value} pairs ordered and changeable. No duplicates
```python
capitals = {

"USA" : "Washington D.C.",
"India": "New Delhi",
"China": "Beijing",
"Russia": "Moscow"
}

print(capitals.get("USA"))
capitals.update({"Germany": "Berlin"}) #updat the dictionary
capitals.pop("China") #remove china
capitals.clear() #it will clear the dictionary
keys = capitals.keys() #it will return all the keys in the dictionary
values = capitals.values() #returns all the values
items = capitals.items #returns both the keys and values

for key, value in capitals.items():
	print(f"{key}: {value}")
```

#### random module
```python
import random

#random integer
number = random.randint(1,6)
print(number)

#random choice
options = ("rock", "paper", "scissors")
option = random.choice(options)
print(option)

#random shuffle
cards = ["2", "3", "4", "5", "6", "7", "8", "9"]
random.shuffle(cards)
print(cards)
```

#### functions
A block of reusable code
```python
def programming():
	print("i love programming with python and kotlin)
programming()

def programming(language, proficiency):
	print(f"I love coding with {language}")
	print(f"I am {proficiency} with writing {language}")

print()
programming("python", "proficient")
print()
programming("kotlin", "proficient")
```


return - statement used to end a function and send a result back to the caller
```python
def adding():
	result = 3 + 3
	return result
printing = adding()
print(printing) #or print(adding())

# or
def adding():
	return 3 + 3
result = adding()
print(result)
```

*args and **kwargs
```python
# *args = allows you to pass multiple non-key arguments and pack everything as a tuple
# **kwargs = allows you to pass multiple keyword-arguments and pack everything as a dict
# * unpaking operator

def add(*args):
	total = 0
	for arg in args:
		total += arg
	return total

print(add(1, 2, 3, 4)) 

#**kwargs
def print_address(**kwargs):
	for key, value in kwargs.items():
		print(f"{key}: {value}")
print_address(street= "123 fare st.", city="Detroit", state="MI", zip="81138")
```

#### variable scope 
where a variable is visible and accessible
scope resolution - (LEGB) Local -> Enclosed -> Global -> Built-in
```python
local - is a varible within a function and is not accessible outside of that function
Enclosed - is a variable whithin the main function if there is another function inside it
Global - is a variable outside any functions
Built-in - is a variable within an imported module

```

#### Membership operators
```python
# Membership operators = used to test whether a value or variable is found in a sequence
# 1. in
# 2. not in

students = {"Spongebob", "Patrick", "Sandy"}
student = input("Enter the name of a student: ") 

if student in students:
	print(f"{student} is a student")
else:
	print(f"{student} was not found")
```

#### list comprehension
```python
""" List comprehension = A concise way to create lists in python
	Compact and easier to read than traditional loops
	[expression for value in iterable if condition]
"""
# list comprehension
doubles = [x * 2 for x in range(1, 11)]
print(doubles)

#normal loop
doubles = []
for x in range(1, 11):
	doubles.append(x * 2)
print(doubles)

# list comprehension
fruits = ["apple", "orange", "banana", "coconut"]
fruits = [fruit.upper() for fruit in fruits]
print(fruits)

# list comprehension
numbers = [1, -2, 3, -4, 5, -6]
positive_nums = [num for num in numbers if num >= 0]
negative_nums = [num for num in numbers if num <= 0]
```

#### modules
A file containing code you want to include in your program. Use `import` to include a module(built in or your own)
```python
print(help("modules")) #to see the modules available

import math #(recommended)
import math as m #(recommended if the module name is long)
from math import pi # to import a specific element in a module
from math import *

print(math.pi) #import math
print(m.pi) #import math as m
print(pi) # from math import pi
```

```python
# if __name__ == __main__: (this script can be imported or run standalone)
							# Functions and classes in this module can be reused
							# without the main block of code executing

def main():
	print("This is a test")

if __name__== '__main__': #it checks if you are running the main program directly and if so the it executes the main function
	main() #main will run if its being called directly in this file and not imported by another file
  

'''
USE CASE: let's say you are importing a the main() function in another file but you don't want the function
to execute unless its the main file calling it, thats where this comes in.
In short if you import the main() function in another file and run it, it won't execute or show anything
unless you call it in its original file.
This avoids unintended execution
'''
```

## Object oriented programming
Object - A bundle of elated attributes(variables) and methods(functions) e.g. phone, cup, book
you need a `class` to create many objects
`class` - a blueprint used to design the structure and layout of an object
`methods` - are actions our class can perform
`class variables` - shared among all instances of a class -> defined outside the constructor -> 
Allow you to share data among all objects created from that class

```python
class Car:
	def __init__(self, model, year, color, price): #constructor: we need this in order to create objects
		self.model = model
		self.year = year
		self.color = color
		self.price = price

car1 = Car("Toyota raise", 2019, "light brown", "2.5M")
car2 = Car("BYD Shark 6", "2025", "white", "10M")

print(car1.model)
print(car1.year)
print(car1.color)
print(car1.price)
print()
print(car2.model)
print(car2.year)
print(car2.color)
print(car2.price)
```

```python
class Car:
	car_type = "SUV"
	def __init__(self, model, year, color, price): #constructor: we need this in order to create objects
		self.model = model
		self.year = year
		self.color = color
		self.price = price
	
	def drive(self):
		print("You drive the car")
	
	def stop(self):
		print("You stop the car")

car1 = Car("Toyota raise", 2019, "light brown", "2.5M")
car1.drive()
car1.stop()

print(car1.model)
print(car1.year)
print(car1.color)
print(car1.price)
print(Car.car_type)
```

```python
class Student:

	class_year = 2024
	num_students = 0 # to check the number of objects/students created

	def __init__(self, name, age):
		self.name = name
		self.age = age
		Student.num_students +=1  

student1 = Student("Harold Moose", 25)
student2 = Student("John Doe", 30)
print(f"my graduating class of {Student.class_year} has {Student.num_students} students")
```

#### Inheritance
Allows a class to inherit attributes and methods from another class. Helps with code re-usability and extensibility
class Child(Parent)
```python
class Animal:

	def __init__(self, name):
		self.name = name
		self.is_alive = True
	
	def eat(self):
		print(f"{self.name} is eating")
	
	def sleep(self):
		print(f"{self.name} is sleeping")

class Dog(Animal):
	pass
class Cat(Animal):
	pass
class Mouse(Animal):
	pass


dog = Dog("Doggy")
cat = Cat("Catty")
mouse = Mouse("Mousy")

print(dog.name)
print(dog.is_alive)
dog.eat()
dog.sleep()
```

*Note*:
`multiple inheritance` = inherit from more than one parent class. C(A,B)
`multilvel inheritance` = inherit from a parent which inherits from another parent. 
- C(B) <- B(A) <- A

#### Super function
`super()` - Function used in a child class to call methods from a parent class(supperclass).
- Allows you to extend the functionality of the inherited methods
- In Short it calls the constructors of the parent class to be reused in the child class

```python
class Shape:
	def __init__(self, color, is_filled):
	self.color = color
	self.is_filled = is_filled
	
	def describe(self):
		print("Parent description")

class Circle(Shape):
	def __init__(self, color, is_filled, radius):
	super().__init__(color, is_filled) # it will use the parent assigned constructors
	self.radius = radius
	
	def describe(self):
		print("Circle description")
		super().describe() # it will also use the parent describe intead of overriwriting it

class Square(Shape):
	def __init__(self, color, is_filled, width):
	super().__init__(color, is_filled)
	self.width = width
  
circle = Circle("red", True, 5)
print(circle.color)
print(circle.is_filled)
print(circle.radius)
circle.describe()
```

#### polymorphism
Greek word that means to have many forms or faces. **Poly= many**, **Morphe = form**
TO achieve plymorphism:
- Inheritance - An object could be treated of the same type as parent class
- "Duck typing" - Object must have necessary attributes/methods

```python
from abc import ABC, abstractmethod

class Shape(ABC):
	@abstractmethod #This makes sure that the children must have and define the area method or there'll be an error
	def area(self):
		pass

class Circle(Shape):
	def __init__(self, radius):
	self.radius = radius

	def area(self):
		return 3.14 * self.radius ** 2

class Square(Shape):
	def __init__(self, side):
		self.side = side

	def area(self):
		return self.side ** 2
  
shapes = [Circle(4), Square(5)]
for shape in shapes:
	print(shape.area())
```

#### static methods

`Static methods` = A method that belong to a class rather than any object from that class(instance)
- Usually used for general utility functions
`Static methods` = Best for utility functions that do not need access to class data
- In static methods you don't need to create a person to call it, you can just call it directly e.g.
- `employee1 = Employee.get_info()` X `Employee.is_valid_position()`
- this is because it doesn't access the constructors/objects created

`Instance methods` = Best for operations on instances of the class(objects) 
- You create an instance in order to use it e.g. `employee1 = Employee.get_info()`

```python
class Employee:

	def __init__(self, name, position):
		self.name = name
		self.position = position

	#Instance methods(these are the normal methods we use)
	def get_info(self):
		return f"{self.name} = {self.position}"

	#static methods
	@staticmethod
	def is_valid_position(position):
		valid_positions = ["Manager", "Cashier", "Cook", "Janitor"]
		return position in valid_positions

employee1 = Employee.get_info() #instance method
print(Employee.is_valid_position("Cook")) #static method
```

#### Class methods 
Allow operations related to the class itself. Take (cls) as the first parameter, which represents the class itself.
- It isn't tied to one object but the class itself

```python
class Counter:
	count = 0

	@classmethod
	def increment(cls):
		cls.count += 1

Counter.increment()
Counter.increment()
print(Counter.count)
```

```python
class Dog:
    species = "Canine"

    def __init__(self, name):
        self.name = name
        
    # Instance method
    def bark(self):
        return f"{self.name} says woof!"

    # Class method
    @classmethod
    def what_species(cls):
        return f"All dogs are {cls.species}"
        
d = Dog("Buddy")
print(d.bark())   # Buddy says woof!
print(Dog.what_species())  # All dogs are Canine, it tied to the class not any object/person

```

#### 🚦 Think of it like this:

- **Instance method (**`self`**)**: "I’m an object, and I’ll do something with _my own data_."
- **Static method**: "I’m just a helper function sitting inside the class, but I don’t care about the class or any object."
- **Class method (**`cls`**)**: "I’m tied to the _class_, not an object. I can create new objects or change class-wide settings."

#### magic methods 
```python
# Magic methods = Dunder methods(double underscore) __init__, __str__, __eq__
# They are automatically called by many of python's built-in operations.
# They allow developers to define or customize the behavior of objects

class Book:

def __init__(self, title, author, num_pages):
	self.title = title
	self.author = author
	self.num_pages = num_pages

	#the print statement will return this string instead of the default memory address
	def __str__(self):
		return f"'{self.title}' by {self.author}"
	
	#checks if one object is equal to another(True/Flase) instead of the default False(always)
	def __eq__(self, other):
		return self.title == other.title and self.author == other.author
	
	#checks if one object is less than(lt) another
	def __lt__(self, other):
		return self.num_pages < other.num_pages
	
	#adds one object to another
	def __add__(self, other):
		return f"{self.num_pages + other.num_pages} pages"

book1 = Book("THe Hobbit", "J.R.R Tolkien", 310)
book2 = Book("Harry Potter and The Philosopher's Stone", "J.K. Rowling", 223)
book3 = Book("The Lion, the Witch and the Wardrobe", "C.S. Lewis", 172)

print(book1) #__str__
print(book1 == book2) #__eq__ book1 is self and book2 is other
print(book2 < book3) #__lt__
print(book1 + book2) #__add__
```

*Note:* in short when you create and call a person of a class object you can't print it unless you specify the
object you want to access e.g. `print(book1.author)`, so if you only call `print(book1)` it will return the
memory address where its stored.
So the magic methods allow you to return something specific instead of the memory address
and they are so many than the ones demonstrated above

#### property decorators

```python
# @property = Decorator used to defne a method as a property(it can be accessed like an attribute)
# Benefit: Add additional logic when read, write, or delete attributes
# Gives you getter, setter, and deleter method

class Rectangle:

	def __init__(self, width, height):
		self._width = width
		self._height = height
	
	@property
	def width(self):
		return f"{self._width:.1f}cm"
	
	@property
	def height(self):
		return f"{self._height:.1f}cm"
	
	@width.setter
	def width(self, new_width):
		if new_width > 0:
			self._width = new_width
		else:
			print("width must be greater than zero")
	
	@height.setter
	def width(self, new_height):
		if new_height > 0:
			self._height = new_height
		else:
			print("width must be greater than zero")
	
	@width.deleter
	def width(self):
		del self._width
		print("width has been deleted")
	
	@height.deleter
	def height(self):
		del self._height
		print("height has been deleted")

rectangle = Rectangle(3, 4) 
rectangle.width = 5 #width.setter changes the width to 5 instead of 3

print(rectangle.width) #answer will be the modified width and height 3.0cm
print(rectangle._width) #access the raw number which will be 3

del rectangle.width
del rectangle.height
```

#### Decorators

```python
# Decorator = A function that extends the behavior of another function
# w/o modifying the base function
# Pass the base funtion as an argument to the decorator


def add_sprinkles(func):
	def wrapper(): #this inside funtion is amust to have
		print("You add sprinkles")
		func() #this calls the get ice cream function (get_ice_cream = add_sprinkles(get_ice_cream))
	return wrapper

def add_fudge(func):
	def wrapper():
		print("you add fudge")
		func()
	return wrapper

@add_sprinkles
@add_fudge
def get_ice_cream():
print("Here is your ice cream") 
get_ice_cream() # it calls the decorator functions first and then the func() calls the main function(get_ice_cream())
```

#### exception 
An event that interrupts the flow of a program(ZeroDivionError, TypeError, ValueError)
- `try, except, finally` 

```python
try:
	number = int(input("Enter a number: "))
	print(1/ number)

except ZeroDivisionError:
	print("You can't divide by zeor IDIOt!")
except ValueError:
	print("Enter only numbers please!")
except Exception:
	print("something went wrong!")
finally:
	print("Do some cleanup here")

# except Exception: - catches all exceptions but its a bad practice
# finally always execute regarless there's an exception or not
```


# File Handling

#### 1. File detection
```python
import os

file_path = "Documents/test.txt" 

# check if the files/folder exist
if os.path.exists(file_path):
	print(f"THe location '{file_path}' exists") 

	#check if its a file or folder
	if os.path.isfile(file_path):
		print("That is a file")
	elif os.path.isdir(file_path):
		print("That is a dirctory")

else:
	print("That location doesn't exist")
```

#### 2. Writing files
(.txt, .json, .csv)

```python
f = open("data.txt", "w")
f.write("Hello, world!")
f.close()   # you must remember this

```

**Note:** `with` automatically closes the file for you so it more recommended

| Mode  | Meaning            | Behavior if File Exists     |
| ----- | ------------------ | --------------------------- |
| `"w"` | Write              | Overwrites the file         |
| `"a"` | Append             | Adds to the end of the file |
| `"x"` | Exclusive creation | Error if file exists        |
| `"r"` | Read               | Error if file doesn’t exist |
`.txt`
```python
file_path = "output.txt"
text_data = "I like Ramen"

with open(file_path, "w") as file:
	file.write(text_data)
	print(f"text file '{file_path}' was created")
	
with open(file_path, "a") as file:
	file.write("\n" + text_data) # to add/append in a new line
	print(f"text file '{file_path}' was created")
```

`.json`
```python
import json

file_path = "jsonfile.json"
employee = {
	"name": "Harold",
	"age": 30,
	"job": "Dev"

}

with open(file_path, "w") as file:
	json.dump(employee, file, indent=4)
	print(f"json file '{file_path}' was created")
```

`.csv`
```python
import json
import csv

file_path = "output.csv"
employees = [

	["Name", "Age", "Job"],
	["Alice", 28, "Engineer"],
	["Brian", 35, "Teacher"],
	["Cynthia", 42, "Doctor"],
	["David", 30, "Designer"]
]

with open(file_path, "w", newline="") as file:
	writer = csv.writer(file)
	for row in employees:
		writer.writerow(row)
	print(f"csv file '{file_path}' was created")
```

#### 3. Reading files
```python
import json
import csv

file_path = "output.txt"

try:
    with open(file_path, "r") as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print("That file was not found")
except PermissionError:
    print("You don't have permission to read that file")

```

`.json`
```python
import json
import csv

file_path = "output.json"   # change to your JSON file

try:
    with open(file_path, "r") as file:
        content = json.load(file)   # load JSON instead of plain text
        print(content)
except FileNotFoundError:
    print("That file was not found")
except PermissionError:
    print("You don't have permission to read that file")

```

`.csv`
```python
import json
import csv

file_path = "output.csv"   # change to your CSV file

try:
    with open(file_path, "r") as file:
        reader = csv.reader(file)   # use csv.reader instead of file.read()
        for row in reader:
            print(row)
except FileNotFoundError:
    print("That file was not found")
except PermissionError:
    print("You don't have permission to read that file")

```