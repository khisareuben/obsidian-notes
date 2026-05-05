


| 1. [[Custom Notes#Basic output]]         | 2. [[Custom Notes#Comments]] | 3. [[Custom Notes#Data types and variables]] |
| ---------------------------------------- | ---------------------------- | -------------------------------------------- |
| 4. [[Custom Notes#Namespace]]            | 5. [[Custom Notes#Typedef]]  | 6. [[Custom Notes#Using keyword]]            |
| 7. [[Custom Notes#Arithmetic operators]] | 8.                           |                                              |



### Basic output

```cpp
#include <iostream>

int main(){

	std::cout << "hello world" << '\n';
	std::cout << "Basic output" << std::endl; //recommended
	return 0;

}
```


## Comments

```cpp
#include <iostream>  

int main(){

	// this is a comment
	
	/*
	
	this is a multi line comment
	
	*/
	
	std::cout << "hello world" << '\n';
	std::cout << "Basic output" << std::endl; //recommended
	return 0;

}
```


### Data types and variables

```python
int age = 25; or int age{25} //recommended

double price = 10.99; or double price{10.99}

float price{10.4f}; or {10.4} //without f

char grade = 'A';

bool isStudent = true;

string name = "Harold";

const double PI{3.14159}
```


### Namespace

Provides a solution for preventing name conflicts in large projects. 

```cpp
#include <iostream>

namespace first {
    int x{25};
}

namespace second {
    int x{15};
}

int main(){

    int x{0};

    std::cout << x << '\n';
    std::cout << first::x << '\n';
    std::cout << second::x << '\n';

    return 0;
}
```


### Typedef

In C++, `typedef` is a keyword used to create an alias (alternative name) for an existing type. It doesn’t create a new type—it just gives a more convenient name to an existing one. 
> [!Note] It is better to use `using` keyword than `typedef`

```cpp

typedef std::string text;
text name{"Json"};

typedef unsigned int uint;
uint age = 25;

typedef unsigned long long ull;
ull bigNumber = 123456789;

```

```cpp
#include <iostream>

typedef std::string text;

int main(){
    text name {"Json"};
    std::cout << name;
    return 0;
}
```


### Using keyword

same as `typedef`
```cpp
#include <iostream>

using text = std::string;

int main(){
    text name {"Json"};
    std::cout << name;
    return 0;
}
```


### Arithmetic operators

```cpp
#include <iostream>
using namespace std;

int main() {
    int a, b;

    cout << "Enter two integers: ";
    cin >> a >> b;

    cout << "Addition: " << (a + b) << endl;
    cout << "Subtraction: " << (a - b) << endl;
    cout << "Multiplication: " << (a * b) << endl;

    if (b != 0) {
        cout << "Division: " << (a / b) << endl;
        cout << "Modulus: " << (a % b) << endl;
    } else {
        cout << "Division and modulus not possible (b = 0)" << endl;
    }

    return 0;
}

```


### Type Casting

- Converting one data type to another.
- **Implicit**: automatic conversion.
- **Explicit**: using casts.

```cpp
double pi = 3.14; //or double pi = (int) 3.14
int x = (int)pi;        // old style
int y = static_cast<int>(pi); // modern style
```


47 min