


| 1. [[Custom Notes#Basic output]]         | 2. [[Custom Notes#Comments]]          | 3. [[Custom Notes#Data types and variables]] |
| ---------------------------------------- | ------------------------------------- | -------------------------------------------- |
| 4. [[Custom Notes#Namespace]]            | 5. [[Custom Notes#Typedef]]           | 6. [[Custom Notes#Using keyword]]            |
| 7. [[Custom Notes#Arithmetic operators]] | 8. [[Custom Notes#input]]             | 9. [[Custom Notes#Basic math functions]]     |
| 10. [[Custom Notes#If statements]]       | 11. [[Custom Notes#switch statement]] | 12. [[Custom Notes#Operators]]               |
| 13. [[Custom Notes#Important functions]] | 14. [[Custom Notes#Do while loop]]    | 15. [[Custom Notes#For loop]]                |
| 16. [[Custom Notes#break and continue]]  | 17. [[Custom Notes#Random number]]    |                                              |



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


### input

```cpp
#include <iostream>

int main() {
    std::string name;
    
    std::cout << "What is your name?: ";
    std::cin >> name;

    std::cout << "Your name is " << name;
    return 0;
}
```

```cpp
#include <iostream>

int main() {
    std::string name;

    std::cout << "What is your full name?: ";
    std::getline(std::cin, name);

    std::cout << "Your name is " << name;
    return 0;
}
```

```cpp
std::getline(std::cin >> std::ws, name); //for eliminating whitespaces before it
//mostly used if there is another cin input before it
```


### Basic math functions

```cpp
#include <iostream>
#include <cmath>

int main() {
    double x{3};
    double y{4};
    double z;
    
    // z = std::max(x, y);
    // z = std::min(x, y);
    // z = pow(2, 3);
    // z = sqrt(9);
    // z = abs(-3);
    // z = round(x);
    // z = ceil(x);
    // z = floor(x);

    std::cout << z;
    return 0;
}
```


### If statements

```cpp
#include <iostream>

int main() {
    int age{};
    std::cout << "What is your age?: ";
    std::cin >> age;

    if(age >= 18) {
        std::cout << "You are eligible to vote";
    } else if(age < 0) {
        std::cout << "You are not born yet";
    } else {
        std::cout << "You are still a child";
    }

    return 0;
}
```


### switch statement

```cpp
#include <iostream>

int main() {
    int num;
    std::cout << "Enter number of day(1-7): ";
    std::cin >> num;

    switch(num) {
        case 1:
            std::cout << "Sunday";
            break;
        case 2:
            std::cout << "Monday";
            break;
        case 3:
            std::cout << "Tuesday";
            break;
        case 4:
            std::cout << "Wednesday";
            break;
        case 5:
            std::cout << "Thursday";
            break;
        case 6:
            std::cout << "Friday";
            break;
        case 7:
            std::cout << "Saturday";
            break;
        default:
            std::cout <<  "Invalid input";
    }

    return 0;
}
```

### Ternary operator

```cpp
#include <iostream>

int main() {
    int age{18};
    
    age >= 18 ? std::cout << "Adult" : std::cout << "Child";

    return 0;
}
```


### Operators

- Arithmetic: `+`, `-`, `*`, `/`, `%`.
    
- Relational: `==`, `!=`, `<`, `>`, `<=`, `>=`.
    
- Logical: `&&`, `||`, `!`.
    
- Assignment: `=`, `+=`, `-=`, `*=`, `/=`, `%=`.


### Important functions

```cpp
name.length() //to check the length
name.empty() //to check if its empty or not
name.append('@gmail.com') //adds at the end of the string
name.insert(0, '@') // instert at a specific index which is zero
name.find(' ') // to find something in a string...
name.erase(0, 3) //to remove something from index 0 to 3
```

### Do while loop

It does execute some block of code first, then repeat again if the condition is true.

```cpp
#include <iostream>

int main() {
    int number;
    
    do{
        std::cout << "Enter a positive #: ";
        std::cin >> number;
    }while(number < 0);

    std::cout << "THis # is: " << number;

    return 0;
}
```


### For loop

```cpp
#include <iostream>

int main() {
    
    for(int i = 1; i <=5; i++){
        std::cout << "I am a champion" << '\n';
    }

    return 0;
}
```

### break and continue

```cpp
#include <iostream>

int main() {
    // break = break out of the loop
    // continue - skip current iteration

    for(int i=1; i <= 15; i++){
        if(i == 13){
            continue;
        }
        std::cout << i << '\n';
    }

    return 0;
}
```

### Random number

```cpp
#include <iostream>
#include <cstdlib>   // for rand(), srand()
#include <ctime>     // for time()

using namespace std;

int main() {

    srand(time(0)); // seed with current time
    int randomNum = (rand() % 100) + 1; // random number between 0 and 100
    cout << "Random number: " << randomNum << endl;
}

```

```cpp
#include <iostream>
#include <random>

using namespace std;

int main() {
    random_device rd;  // seed
    mt19937 gen(rd()); // Mersenne Twister engine
    uniform_int_distribution<> dist(1, 100); // range 1–100

    int randomNum = dist(gen);
    cout << "Random number: " << randomNum << endl;
}

// modern way (c++ 11) recommended
// random_device → provides a seed.
// mt19937 → a high-quality random number generator.
// uniform_int_distribution → defines the range
```


