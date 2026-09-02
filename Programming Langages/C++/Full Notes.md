
# 📘 C++ Full Notes

## Table of Contents

| 1. [[Full Notes#Introduction]]                     | 2. [[Full Notes#Variables & Data Types]] | 3. [[Full Notes#Type Casting]]                 |
| -------------------------------------------------- | ---------------------------------------- | ---------------------------------------------- |
| 4. [[Full Notes#Operators]]                        | 5. [[Full Notes#Control Flow]]           | 6. [[Full Notess#Loops]]                       |
| 7. [[Full Notes#Functions]]                        | 8. [[Full Notes#Scope]]                  | 9. [[Full Notes#Object Oriented Programming]]  |
| 10. [[Full Notes#Inheritance]]                     | 11. [[Full Notes#Polymorphism]]          | 12. [[Full Notes#Encapsulation & Abstraction]] |
| 13. [[Full Notes#Templates]]                       | 14. [[Full Notes#Exception Handling]]    | 15. [[Full Notes#File Handling]]               |
| 16. [[Full Notes#STL (Standard Template Library)]] | 17. [[Full Notes#Modern C++ Features]]   | 18. [[Full Notes#Namespaces]]                  |

## Introduction

- C++ is a **compiled, general-purpose, object-oriented language**.
    
- Extension of C with classes, templates, and exceptions.
    
- Used in **system software, game engines, embedded systems, and desktop apps**.
    



```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Hello, C++!" << endl;
    return 0;
}
```

## Variables & Data Types

- **Primitive types**: `int`, `float`, `double`, `char`, `bool`.
    
- **Modifiers**: `short`, `long`, `signed`, `unsigned`.
    
- **Strings**: `string` (from `<string>`).
    

cpp

```cpp
int age = 25; or int age{25} //recommended

double price = 10.99; or double price{10.99}

float price{10.4f}; or {10.4} //without f

char grade = 'A';

bool isStudent = true;

string name = "Harold";

const double PI{3.14159}
```


```cpp
#include <iostream>
#include <string>   // <-- required

int main() {
    std::string name{"Reuben"};   // fully qualified
    std::cout << name;
}

```

```cpp
#include <iostream>
#include <string>

using namespace std;

int main() {
    string name{"Reuben"};   // works because of 'using namespace std'
    cout << name;
}

```

## Type Casting

- Converting one type to another.
- **Implicit**: automatic conversion.
- **Explicit**: using casts.
    

```cpp
double pi = 3.14;
int x = (int)pi;        // old style
int y = static_cast<int>(pi); // modern style
```

## Operators

- Arithmetic: `+`, `-`, `*`, `/`, `%`.
    
- Relational: `==`, `!=`, `<`, `>`, `<=`, `>=`.
    
- Logical: `&&`, `||`, `!`.
    
- Assignment: `=`, `+=`, `-=`, `*=`, `/=`, `%=`.
    

```cpp
int x = 10;
x += 5; // x = 15
```

## Control Flow


```cpp
int age;
cin >> age;

if (age >= 18) {
    cout << "You are an adult!";
} else {
    cout << "You are underage!";
}
```

- `switch` statement:
    


```cpp
int option = 2;
switch(option) {
    case 1: cout << "Option 1"; break;
    case 2: cout << "Option 2"; break;
    default: cout << "Invalid option";
}
```

## Loops


```cpp
// for loop
for (int i = 1; i <= 5; i++) {
    cout << i << endl;
}

// while loop
int n = 1;
while (n <= 5) {
    cout << n << endl;
    n++;
}

// do-while loop
int x = 1;
do {
    cout << x << endl;
    x++;
} while (x <= 5);
```

## Functions


```cpp
int add(int a, int b) {
    return a + b;
}

int main() {
    cout << add(3, 4);
}
```

- Pass by reference:
    

```cpp
void update(int &x) {
    x += 10;
}
```

## Scope

- **Local**: inside functions.
- **Global**: outside functions.
- **Static**: retains value between calls.
    

## Object Oriented Programming


```cpp
class Car {
public:
    string model;
    int year;

    Car(string m, int y) {
        model = m;
        year = y;
    }

    void drive() {
        cout << "Driving " << model;
    }
};
```

## Inheritance


```cpp
class Animal {
public:
    void eat() { cout << "Eating"; }
};

class Dog : public Animal {
public:
    void bark() { cout << "Woof!"; }
};
```

## Polymorphism


```cpp
class Shape {
public:
    virtual void draw() { cout << "Drawing shape"; }
};

class Circle : public Shape {
public:
    void draw() override { cout << "Drawing circle"; }
};
```

## Encapsulation & Abstraction


```cpp
class BankAccount {
private:
    double balance;

public:
    BankAccount(double b) { balance = b; }
    void deposit(double amount) { balance += amount; }
    double getBalance() { return balance; }
};
```

## Templates


```cpp
template <typename T>
T add(T a, T b) {
    return a + b;
}
```

## Exception Handling


```cpp
try {
    int x = 0;
    if (x == 0) throw runtime_error("Division by zero!");
} catch (exception &e) {
    cout << e.what();
}
```

## File Handling


```cpp
#include <fstream>
using namespace std;

int main() {
    ofstream file("data.txt");
    file << "Hello, file!";
    file.close();

    ifstream readFile("data.txt");
    string line;
    while (getline(readFile, line)) {
        cout << line << endl;
    }
}
```

## STL (Standard Template Library)

- **Containers**: `vector`, `list`, `map`, `set`.
    
- **Algorithms**: `sort`, `find`, `count`.
    

```cpp
#include <vector>
#include <algorithm>
vector<int> nums = {3, 1, 4};
sort(nums.begin(), nums.end());
```

## Modern C++ Features

- `auto` type deduction.
    
- Range-based `for`.
    
- `nullptr`.
    
- `constexpr`.
    
- Smart pointers (`unique_ptr`, `shared_ptr`).
    
- Lambdas:
    

```cpp
auto square = [](int x){ return x*x; };
```

## Namespaces


```cpp
namespace school {
    void greet() { cout << "Hello from school namespace"; }
}

int main() {
    school::greet();
}
```

✅ This is a **comprehensive Obsidian-ready notes file for C++**, mirroring your Python notes style: short explanations + code snippets, covering everything from basics to advanced features