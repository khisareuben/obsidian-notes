 
This will all be the full notes on python basics and most of it will be shortened but still have the key things to learn and practice python code.

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