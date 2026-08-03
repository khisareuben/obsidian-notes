
#### Basic print statement

```C
#include <stdio.h>

int main() {
    printf("Hellow world");
    return 0;
}
```

#### comments

These are non executable lines. 

```C
#include <stdio.h>

int main() {

    //this a single line comment
    /*
    this is a multi line comment
    */

    printf("Hellow world");
    return 0;
}
```


#### Data types and variables
A variable i a reusable container for a value. It behaves as if it were the value it contains
`int` `double` `float` `boolean`

`\n` - means new line

```C
#include <stdio.h>
#include <stdbool.h>

int main() {

    int age = 25; //integer 4 bytes
    float price = 10.99;   //float number  4 bytes
    double pi = 3.14159;   //double(larger decimal than float)  8 bytes
    char grade = 'A';      //character 1 byte
    char name[] = "Reuben";  //string(array of characters)
    bool isOnline = true; //trueorfalse 1or0  1 byte


    printf("You are %d years old\n", age);
    printf("The price is $%f\n", price);
    printf("PI = %lf\n", pi);
    printf("Your grade is %c\n", grade);
    printf("My name is %s\n", name);
    printf("True = %d\n", isOnline);

    return 0;
}
```

#### Format specifier
These are special tokens that begin with a `%` symbol, followed by a character that specifies the data type and optional modifiers(width, precision, flags)
They control how data is displayed or interpreted

`%d` - represent a string
`%f` - represents a float
`%lf` - represent a double
`%c` - represents a character
`%s` - represents a string

```C
#include <stdio.h>
#include <stdbool.h>

int main() {

    int age = 25;
    float price = 10.99; 
    double pi = 3.14159; 
    char grade = 'A';
    char name[] = "Reuben";
    bool isOnline = true;


    printf("You are %d years old\n", age);
    printf("The price is $%f\n", price);
    printf("PI = %lf\n", pi);
    printf("Your grade is %c\n", grade);
    printf("My name is %s\n", name);
    printf("True = %d\n", isOnline);

    return 0;
}
```

