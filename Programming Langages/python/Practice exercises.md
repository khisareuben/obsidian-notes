



| [[Practice exercises#1. How to find average of N numbers in Python]] | [[Practice exercises#2. How to sum the first n integers]]] |
| -------------------------------------------------------------------- | ---------------------------------------------------------- |
| [[Practice exercises#3. How to get time of a program's execution]]]  | [[Practice exercises#4. How to get the current username]]] |
|                                                                      |                                                            |
|                                                                      |                                                            |
|                                                                      |                                                            |




#### 1. How to find average of N numbers in Python

```python
num = int(input("How many numbers: "))
total = 0

for n in range(1,num+1):
    numbers = float(input(f"Enter you {n} number: "))
    total += numbers

avg = total / num

print(f"Average = {avg}")
```

#### 2. How to sum the first n integers

This calculates the sum of the first n integers e.g
if n = 5 then sum will be (1+2+3+4+5)
Its `factorial` but with addition instead of *

```python
n = int(input("Enter the number: "))

sum = (n * (n + 1)) / 2
print(sum)

# or

n = int(input("Enter the number: "))
sum = 0
for i in range(1, n+1):
    sum += i
print(sum)
```

#### 3. How to get time of a program's execution

```python
import time

def myfun():
    start_time = time.time()
    s = 0
    
    for i in range(1, n+1):
        s += i
    end_time = time.time()
    return s, end_time-start_time

n = 5
print(myfun())
```

#### 4. How to get the current username

```python
import getpass
print(getpass.getuser())
```