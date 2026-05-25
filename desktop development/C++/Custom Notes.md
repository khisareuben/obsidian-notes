


| 1. [[Custom Notes#Basic output]]         | 2. [[Custom Notes#Comments]]           | 3. [[Custom Notes#Data types and variables]]     |
| ---------------------------------------- | -------------------------------------- | ------------------------------------------------ |
| 4. [[Custom Notes#Namespace]]            | 5. [[Custom Notes#Typedef]]            | 6. [[Custom Notes#Using keyword]]                |
| 7. [[Custom Notes#Arithmetic operators]] | 8. [[Custom Notes#input]]              | 9. [[Custom Notes#Basic math functions]]         |
| 10. [[Custom Notes#If statements]]       | 11. [[Custom Notes#switch statement]]  | 12. [[Custom Notes#Operators]]                   |
| 13. [[Custom Notes#Important functions]] | 14. [[Custom Notes#Do while loop]]     | 15. [[Custom Notes#For loop]]                    |
| 16. [[Custom Notes#break and continue]]  | 17. [[Custom Notes#Random number]]     | 18. [[Custom Notes#Functions]]                   |
| 19. [[Custom Notes#Arrays]]              | 20. [[Custom Notes#sizeof()]]          | 21. [[Custom Notes#foreach loop]]                |
| 22. [[Custom Notes#3D arrays]]           | 23. [[Custom Notes#memory address]]    | 24. [[Custom Notes#pointers]]                    |
| 25. [[Custom Notes#Dynamic memory]]      | 26. [[Custom Notes#Recursion]]         | 27. [[Custom Notes#function template]]           |
| 28. [[Custom Notes#Struct]]              | 29. [[Custom Notes#enums]]             | 30. [[Custom Notes#object oriented programming]] |
| 31. [[Custom Notes#constructor]]         | 32. [[Custom Notes#getter and setter]] | 33. [[Custom Notes#inheritence]]                 |



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
    
    // std::cin.clear():
    // fflush(stdin);       {these are for invalid values, it clears the buffer so it does'nt crush}

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
    
    // j = toupper(j)

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


### Functions

It is valid for functions to share the same name as long as they have different parameters.

```cpp
#include <iostream>
#include <random>
// void is used if not returning anything otherwise you can specify the data type to return
void myfunction(){
    std::cout << "THis is a function";
}

int main() {

    myfunction();
    return 0;
}

```

```cpp
#include <iostream>
#include <random>
// this is the one thats mostly used 
void myfunction();

int main() {

    myfunction();
    return 0;
}

void myfunction(){
    std::cout << "THis is my function";
}
```

### Arrays

```cpp
#include <iostream>

int main() {
    std::string cars[] = {"BYD", "Toyota Raize", "Ford f150"};
    double price[] = {50.22, 20.10, 59.45};

    std::cout << cars[0] << '\n';
    std::cout << cars[1] << '\n';
    std::cout << cars[2] << '\n';

    return 0;
}
```

### sizeof()

Determines the size in bytes of a: variable, data type, class, objects, etc.

```cpp
#include <iostream>

int main() {
    int age = 25;
    std::string cars[] = {"BYD", "Toyota Raize", "Ford f150"};
    
    std::cout << sizeof(age) << " bytes";
    std::cout << sizeof(cars)/sizeof(std::string); // calcs number of elements in array

    return 0;
}
```

```cpp
#include <iostream>

int main() {
    std::string cars[] = {"BYD", "Toyota Raize", "Ford f150"};
    
    int size = sizeof(cars)/sizeof(std::string)
    
    for(int i = 0; i < size; i++) {
        std::cout << cars[i] << "\n";
    }

    return 0;
}
```


### foreach loop
Is a loop that eases the traversal over an iterable data set

```cpp
#include <iostream>

int main() {
    std::string cars[] = {"BYD", "Toyota Raize", "Ford f150"};

    for(std::string car : cars) {
        std::cout << car << "\n";
    }

    return 0;
}
```

```cpp
#include <iostream>

int main() {
    const int SIZE = 100;
    std::string foods[SIZE]{};

	//fill() - fills a range of elements with a specified value. fill(begin, end, value)
    fill(foods, foods + SIZE, "Jesus");

    for(std::string food : foods) {
        std::cout << food << "\n";
    }


    return 0;
}
```


### 3D arrays

```cpp
#include <iostream>

int main() {
    std::string food[][3]{{"Mango", "Banana", "Tomoko"},
                         {"Sukuma Wiki", "Cabbage", "Managu"},
                         {"Rice", "Ugali", "Bread"}};
    //[row][column]
    std::cout << food[0][0] << '\n';
    std::cout << food[1][0] << '\n';
    std::cout << food[2][0] << '\n';

    return 0;
}
```

### memory address

```cpp
#include <iostream>

int main() {
    std::string name{"Reuben"};
    int age{25};
    double salary{100000.00};
    
    std::cout << &name << '\n';
    std::cout << &age << '\n';
    std::cout << &salary << '\n';

    return 0;
}
```


### pointers

Is a variable that stores the memory address of another variable

```cpp
#include <iostream>

int main() {
    std::string name = "Reuben";
    std::string food[]{"Mango", "Banana", "Tomoko"};

    std::string *pName = &name;
    std::string *pfood = food; //arrays are already in the form of a memory address

    std::cout << pName << '\n'; //0x7ffe6b1ef460
    std::cout << *pName << '\n'; //Reuben
    std::cout << pfood << '\n';
    std::cout << *pfood << '\n';

    return 0;
}
```

`null pointer` - an empty pointer
```cpp
#include <iostream>

int main() {
    int *pointer = nullptr;
    int x = 123;
    pointer = &x;

    if(pointer == nullptr){
        std::cout << "Address was not assigned";
    }else{
        std::cout << "Address was assigned";
    }
    return 0;
}
```

### Dynamic memory
This is memory that is allocated after the program is already compiled and running.
Use the `new` to allocate memory in the heap rather than the stack
It is useful when we don't know how much memory we will need e.g `inputs` 
```cpp
#include <iostream>

int main() {
    int *pNum = NULL;
    pNum = new int;
    *pNum = 21;

    std::cout << pNum << "\n";
    std::cout << *pNum << "\n";

    delete pNum; //to prevent memory leak
    
    return 0;
}
```
or
```cpp
#include <memory>
#include <iostream>

int main() {
    auto pNum = std::make_unique<int>(21);
    std::cout << *pNum << "\n"; // prints 21
} // memory auto-freed when pNum goes out of scope

```

### Recursion
A programming technique where a functions invokes itself from within. You could either use `recursion` or `iterative` like for loops.
It is mostly used in algorithms e.g search algorithms
```cpp
#include <iostream>

void walk(int steps);

int main() {
	walk(100);
	return 0;
}
void walk(int steps){
	if(steps > 0){
		std::cout << "You take a step!\n";
		walk(steps - 1);
	}
}
```

```cpp
#include <iostream>
int factorial(int num);
int main (){
	std::cout << factorial(10);
	return 0;
}
int factorial(int num){
	if(num > 1){
		return num * factorial(num - 1);
	} else{
		return 1;
	}
}
```

### function template
Describes what a function looks like. Can be used to generate as many overloaded functions as needed, each using different data types.
Simply, it allows you to have different data types in one function.
```cpp
#include <iostream>
template <typename T>
T max(T x, T y) {
	return (x > y) ? x : y;
}
int main() {
	std::cout << max(1.1, 2.1) << '\n';
	return 0;
}
```

```cpp
#include <iostream>
template <typename T, typename Y>
auto max(T x, Y y) {
	return (x > y) ? x : y;
}
int main() {
	std::cout << max(1.1, 2.1) << '\n';
	return 0;
}
```

### Struct
A structure that group related variables under one name. 
Structs can contain many different data types (string, bool, int, double, etc.)
Variables in a struct are know as `members`
members can be access with `.` "class member access operator"

```cpp
#include <iostream>

struct student {
    std::string name;
    double gpa;
    bool enrolled;
};

int main(){
    student student1;
    student1.name = "John Doe";
    student1.gpa = 3.1;
    student1.enrolled = false;

    student student2;
    student2.name = "Zhou Shen";
    student2.gpa = 4.1;
    student2.enrolled = true;

    std::cout << student1.name << '\n';
    std::cout << student1.gpa << '\n';
    std::cout << student1.enrolled << '\n';
}
```

```cpp
#include <iostream>

struct Car{
    std::string model;
    int year;
    std::string color;
};
void printCar(Car car);

int main(){
    Car car1;
    Car car2;

    car1.model = "Toyota Raize";
    car1.year = 2023;
    car1.color = "red";

    car2.model = "ford f-150";
    car2.year = 2026;
    car2.color = "blue";

    printCar(car1);

    return 0;
}

void printCar(Car car){
    std::cout << car.model << '\n';
    std::cout << car.year << '\n';
    std::cout << car.color << '\n';
}
```

### enums
A user-defined type that consists of paired named-integer constants.
They are great if you have a set of potential options
```cpp
#include <iostream>

enum Day {
    sunday=0, monday=1, tuesday=2, wednesday=3, 
    thursday=4, friday=5, saturday=6};

int main(){
    Day today = wednesday;

    switch(today){
        case 0: std::cout << "It is Sunday!\n";
            break;
        case 1: std::cout << "It is Monday!\n";
            break;
        case 2: std::cout << "It is Tuesday!\n";
            break;
        case wednesday: std::cout << "It is Wednesday!\n";
            break;
        case 4: std::cout << "It is Thursday!\n";
            break;
        case 5: std::cout << "It is Friday!\n";
            break;
        case saturday: std::cout << "It is Saturday!\n";
            break;

    }
    return 0;
}
```

### object oriented programming
An object is a collection of attributes and methods
```cpp
#include <iostream>

class Human{
    public:
	    //attibutes
        std::string name;
        std::string occupation;
        int age;

		//methods
        void eat(){
            std::cout << "This person is eating\n";
        }
        void drink(){
            std::cout << "This person is drinking\n";
        }
        void sleep(){
            std::cout << "This person is sleeping\n";
        }
        void Human::run()
        
};

//recommended for writing huge classes/methods nowadays
void Human::run(){
	std::cout << "This person is running\n";
}

int main(){
    Human human1;  //object

    human1.name = "Rick";
    human1.occupation = "Developer";
    human1.age = 35;

    std::cout << human1.name << '\n';
    std::cout << human1.occupation << '\n';
    std::cout << human1.age << '\n';

    human1.eat();
    human1.drink();
    human1.sleep();

    return 0;

}
```

#### constructor
A special method that is automatically called when a object is instantiated.
useful for assigning values to attributes as arguments
`preferred than the first one above`

```cpp
#include <iostream>

class Student{
    public:
        std::string name;
        int age;
        double gpa;

	//constructor
    Student(std::string name, int age, double gpa){
        this->name = name;
        this->age = age;
        this->gpa = gpa;
    }
};

int main(){
    Student student1("Spongebob", 25, 3.2);

    std::cout << student1.name << '\n';
    std::cout << student1.age << '\n';
    std::cout << student1.gpa << '\n';
}
```

### getter and setter

`Abstrcution` - hiding unnecessary data from outside a class
`getter` - function that makes a private attribute READABLE
`setter` - function that makes a private attribute WRITABLE

```cpp
#include <iostream>

class Stove{
    private:
        int temperature = 0;
    public:
        //getter(readonly)
        // the temperature can be seen though its private
        int getTmeperature(){
            return temperature;
        }
        //setter(writable)
        //the temperature can be writable though its private
        void setTemperature(int temperature){
            this->temperature = temperature;
        }
};

int main(){
    Stove stove;

    stove.setTemperature(1000);
    std::cout << "The temperature setting is: " << stove.getTmeperature(); 
}
```

### inheritence
A class that can recieve attributes and methods from another class
```cpp
#include <iostream>

class Animal{
    public:
        bool alive = true;
        
        void eat(){
            std::cout << "This animal is eating\n";
        }
};
class Dog : public Animal {

};

int main(){
     Dog dog;
     std::cout << dog.alive << '\n';
     dog.eat();
}
```

[[Custom Notes#Basic output]]