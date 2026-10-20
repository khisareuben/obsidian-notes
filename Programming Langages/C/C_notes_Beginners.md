# C Programming - Beginner Short Notes

## Contents
1. First Program  2. Variables  3. Data Types  4. Input/Output  5. Operators  6. If/Else  7. Switch  8. Loops  9. Functions  10. Arrays  11. Strings  12. Pointers  13. Struct / Union / Enum / Typedef  14. Dynamic Memory  15. File Handling  16. Other Essentials  17. Compile

---

### 1. First Program
Structure: `#include` + `main()` + `return`

```c
#include <stdio.h>

int main() {
    printf("Hello World\n");
    return 0;
}
```
`#include <stdio.h>` = input/output library
`main()` = entry point
`printf()` = print
`\n` = new line

### 2. Variables
Variable = storage for value.

```c
int age = 20;
float price = 9.99;
char grade = 'A';
```
Rules: start with letter/_, no spaces, case-sensitive.

### 3. Data Types

| Type | Size | Example |
|------|------|---------|
| int | 4B | 10, -5 |
| float | 4B | 3.14f |
| double | 8B | 3.1415 |
| char | 1B | 'A' |
| long long | 8B | 123456LL |

```c
printf("%zu\n", sizeof(int));
```
`%d` int, `%f` float, `%lf` double, `%c` char, `%s` string, `%zu` size, `%lld` long long

### 4. Input / Output

```c
int n;
char name[30];

scanf("%d", &n);
fgets(name, 30, stdin);
printf("%d %s", n, name);

getchar();
putchar('A');
```

`scanf` needs `&` except arrays. `fgets` safer than `scanf` for strings.

### 5. Operators
```c
int a=10, b=3;
a+b; a-b; a*b; a/b; a%b;
a==b; a!=b; a>b; a<b;
a && b; a || b; !a;
a++; ++a; a+=2;
int c = (a>b) ? a : b;
```

### 6. If / Else

```c
if (a > 10) {
    printf("big");
} else if (a == 10) {
    printf("ten");
} else {
    printf("small");
}
```

### 7. Switch

```c
int day = 2;
switch(day) {
    case 1: printf("Mon"); break;
    case 2: printf("Tue"); break;
    default: printf("Other");
}
```

### 8. Loops

```c
for(int i=0; i<3; i++) {
    printf("%d\n", i);
}

int i=0;
while(i<3) {
    printf("%d\n", i);
    i++;
}

do {
    printf("%d\n", i);
    i++;
} while(i<3);
```
`break` = exit loop, `continue` = skip iteration

### 9. Functions

```c
int add(int x, int y) {
    return x+y;
}

void greet() {
    printf("Hi\n");
}

int main() {
    int s = add(2,3);
    greet();
}
```
Function = reusable block. Call by value.

### 10. Arrays
Collection of same type.

```c
int arr[3] = {1,2,3};
int arr2[] = {4,5,6};

arr[0] = 10;
int n = sizeof(arr)/sizeof(arr[0]);

int mat[2][2] = {{1,2},{3,4}};
mat[0][1];
```

### 11. Strings
Array of chars ending with `\0`

```c
#include <string.h>

char s[20] = "Hello";
char t[] = "World";

strlen(s);
strcpy(s, t);
strcat(s, t);
strcmp(s, t);

fgets(s, 20, stdin);
```

### 12. Pointers
Pointer = holds address.

```c
int x = 10;
int *p = &x;

printf("%p\n", p);
printf("%d\n", *p);

*p = 20;

int arr[3] = {10,20,30};
int *q = arr;
*(q+1); // 20
```

`&` = address of, `*` = value at address
`NULL` = empty pointer

### 13. Struct / Union / Enum / Typedef

```c
struct Person {
    char name[20];
    int age;
};

struct Person p1 = {"John", 20};
p1.age = 21;

struct Person *ptr = &p1;
ptr->age = 22;

typedef struct {
    int x, y;
} Point;

union Data {
    int i;
    float f;
};

enum Color { RED, GREEN, BLUE };
enum Color c = GREEN;
```

Struct = group different types
Union = shares memory
Enum = named integers
Typedef = alias

### 14. Dynamic Memory
Allocate at runtime. Heap.

```c
#include <stdlib.h>

int *a = malloc(5 * sizeof(int));
int *b = calloc(5, sizeof(int));
a = realloc(a, 10 * sizeof(int));

free(a);
free(b);
```

`malloc` = allocate, `calloc` = zero allocate, `realloc` = resize, `free` = release

### 15. File Handling

```c
FILE *f = fopen("file.txt", "w");
fprintf(f, "Hello %d", 10);
fclose(f);

f = fopen("file.txt", "r");
char buf[100];
fgets(buf, 100, f);
fclose(f);

FILE *fb = fopen("data.bin", "wb");
int n[] = {1,2,3};
fwrite(n, sizeof(int), 3, fb);
fclose(fb);
```
Modes: `r` read, `w` write, `a` append, `r+` read+write, `b` binary
`fseek`, `ftell`, `rewind` for navigation

### 16. Other Essentials

**Bitwise**
```c
int a=5, b=3;
a & b; a | b; a ^ b; ~a; a << 1; a >> 1;
```

**Preprocessor**
```c
#define MAX 100
#define SQUARE(x) ((x)*(x))
#include <stdio.h>
```

**Command Line Args**
```c
int main(int argc, char *argv[]) {
    printf("%s %s", argv[0], argv[1]);
}
```

**Type Cast**
```c
int i=10;
float f = (float)i / 3;
```

**Function Pointer**
```c
int add(int a,int b){return a+b;}
int (*op)(int,int) = add;
op(2,3);
```

### 17. Compile & Run

```bash
gcc file.c -o app
./app

gcc -Wall -Wextra -g file.c -o app
gcc main.c utils.c -o app
```

**Common Errors to Avoid**
- `=` vs `==`
- Missing `&` in `scanf`
- Forgetting `\0` in strings
- Using freed pointer
- Missing `break` in switch
- Array out of bounds

**Quick Format Table**
`%d int` | `%f float` | `%c char` | `%s string` | `%p pointer` | `%x hex`
