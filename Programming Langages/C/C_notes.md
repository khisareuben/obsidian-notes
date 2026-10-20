# C Programming - Complete Revision Notes

> Concise, code-first. Assumes you know programming logic.

## 1. Boilerplate & printf

```c
#include <stdio.h>  // std I/O

int main() {
    printf("Hello, C\n");
    printf("Number: %d, Float: %.2f, Char: %c, String: %s, Hex: %x, Ptr: %p\n", 
           42, 3.14, 'A', "hi", 255, (void*)"hi");
    return 0;
}
```
**Format:** `%d %i %u %f %lf %c %s %p %x %o %%` | `%.2f` ` %5d` `%-5d` ` %05d`
`\n \t \\ \"`

## 2. Variables, Data Types, sizeof

```c
int a = 10;              // 4 bytes typically
char c = 'X';            // 1 byte
float f = 3.14f;
double d = 3.141592;
long long big = 1LL;
_Bool b = 1;             // or bool from <stdbool.h>
unsigned int u = 300;

printf("%zu\n", sizeof(int)); // size_t -> %zu
```
**Types:** `char, short, int, long, long long, float, double, void`
`sizeof(type/var)` gives bytes.

## 3. Constants & Literals

```c
#define PI 3.14          // preprocessor, no type
const int MAX = 100;     // typed, scoped
enum { FALSE, TRUE };    // 0,1

const char *msg = "immutable pointer to literal";
char *const p = buffer;  // const pointer
```

## 4. Operators

```c
int x=10, y=3;
x + y; x - y; x * y; x / y; x % y;
x++; ++x; x--; --x;
x += 2; x *= 2;

x == y; x != y; x > y; x < y; x >= y; x <= y;
x && y; x || y; !x;

int z = (x > y) ? x : y; // ternary
```

## 5. Input - scanf, getchar, fgets

```c
int age;
char name[50];
printf("Age: ");
scanf("%d", &age);       // & needed except for arrays
getchar(); // consume \n

printf("Name: ");
fgets(name, sizeof(name), stdin); // safer than gets/scanf("%s")

// scanf with strings leaves \n, fgets includes \n
name[strcspn(name, "\n")] = '\0'; // trim newline -> needs <string.h>

int c = getchar();
putchar(c);
```

## 6. Conditionals

```c
if (age >= 18) {
    printf("Adult\n");
} else if (age >= 13) {
    printf("Teen\n");
} else {
    printf("Kid\n");
}

switch (age) {
    case 18: printf("Just adult\n"); break;
    case 21: printf("US adult\n"); break;
    default: printf("Other\n");
}
```

## 7. Loops

```c
for (int i=0; i<5; i++) {
    if (i==2) continue;
    if (i==4) break;
    printf("%d ", i);
}

int i=0;
while (i < 5) { printf("%d ", i++); }

do {
    printf("%d ", i++);
} while (i < 5);
```

## 8. Functions

```c
// prototype
int add(int a, int b);
void greet(void);

int add(int a, int b) { return a + b; }

// pass by value (copy). To modify, pass pointer.
void inc(int *p) { (*p)++; }

int factorial(int n) { // recursion
    return (n <= 1) ? 1 : n * factorial(n-1);
}

int main() {
    int x=5; inc(&x);
    return 0;
}
```
**Scope:** local, global, static. Variables inside {} die outside.

## 9. Arrays

```c
int arr[5] = {1,2,3,4,5};
int arr2[] = {1,2,3}; // size inferred 3
int m[2][3] = {{1,2,3},{4,5,6}};

for (int i=0; i<5; i++) arr[i] *= 2;

int len = sizeof(arr)/sizeof(arr[0]); // array length trick (only in same scope)

void print_arr(int a[], int n) { // decays to pointer
    for(int i=0;i<n;i++) printf("%d ", a[i]);
}
```

## 10. Strings (char arrays)

```c
#include <string.h>

char s1[20] = "Hello";
char s2[] = "World";

strlen(s1);               // length
strcpy(s1, s2);           // copy
strncpy(s1, s2, sizeof(s1)-1);
strcat(s1, s2);           // concat
strcmp(s1, s2);           // 0 if equal
strchr(s1, 'l');          // find char
strstr(s1, "lo");         // find substring
strcspn(s1, "\n");        // for trimming

// Always null-terminated: '\0'
for(char *p=s1; *p!='\0'; p++) putchar(*p);
```

## 11. Pointers - The Core

```c
int a = 10;
int *p = &a;   // p holds address of a
printf("%d %p %d\n", a, (void*)p, *p); // *p = value at address

*p = 20;       // modifies a
int *nullp = NULL;

int arr[] = {10,20,30};
int *pa = arr; // arr == &arr[0]
printf("%d\n", *(pa+1)); // 20
```

## 12. Pointers + Arrays + Pointer Arithmetic

```c
int arr[3] = {10,20,30};
int *p = arr;
p++; // moves by sizeof(int)

printf("%d\n", *(arr+2)); // same as arr[2]

char *msg = "hello"; // string literal (read-only)
char msg2[] = "hello"; // mutable copy

int *a1 = arr;
int *a2 = &arr[2];
ptrdiff_t diff = a2 - a1; // 2
```

## 13. Double Pointers & Pointer to Pointer

```c
int x=10;
int *p = &x;
int **pp = &p;

printf("%d %d %d\n", x, *p, **pp);

char *names[] = {"Alice","Bob","Carol"}; // array of pointers
char **np = names;

int **matrix; // for dynamic 2D
```

## 14. Dynamic Memory - heap

```c
#include <stdlib.h>

int *arr = malloc(5 * sizeof(int)); // uninitialized
if (!arr) return 1;

int *zero = calloc(5, sizeof(int)); // zeroed

for(int i=0;i<5;i++) arr[i]=i;

arr = realloc(arr, 10 * sizeof(int)); // resize, may move

free(arr);
free(zero);
arr = NULL; // avoid dangling

// 2D dynamic
int **mat = malloc(3 * sizeof(int*));
for(int i=0;i<3;i++) mat[i]=malloc(4*sizeof(int));
// ... use mat[i][j]
for(int i=0;i<3;i++) free(mat[i]);
free(mat);
```
**Rule:** every malloc/calloc/realloc -> free.

## 15. Structures

```c
struct Point {
    int x;
    int y;
};

struct Point p1 = {10,20};
struct Point p2 = {.x=5, .y=7}; // designated

struct Point *pp = &p1;
pp->x = 100; // same as (*pp).x

typedef struct {
    char name[50];
    int age;
} Person;

Person ps = {"John", 25};

// Nested & array of struct
typedef struct {
    Person members[4];
    int count;
} Team;

// Struct size = padding may apply
printf("%zu\n", sizeof(Person));
```

## 16. Union & Typedef

```c
union Data {
    int i;
    float f;
    char c;
}; // shares memory, size = largest member

union Data d;
d.i = 10;
printf("%d\n", d.i);

typedef unsigned int uint;
typedef int* intptr;
```

## 17. Enum

```c
typedef enum {
    RED,    // 0
    GREEN,  // 1
    BLUE=5, // 5
    YELLOW  // 6
} Color;

Color c = GREEN;
if (c == GREEN) {}
```

## 18. Storage Classes

```c
auto int x=10; // default local, rarely used keyword

static int count = 0; // persists across calls, file-scoped if outside func
void counter() {
    static int c=0;
    c++; printf("%d\n", c);
}

extern int global_var; // defined in another file

register int fast = 10; // hint to keep in register (compiler ignores mostly)
```

## 19. Preprocessor

```c
#define MAX 100
#define SQUARE(x) ((x)*(x)) // parens important!
#define DEBUG 1

#ifdef DEBUG
    #define LOG(msg) printf("LOG: %s\n", msg)
#else
    #define LOG(msg)
#endif

#undef MAX

#include <stdio.h>
#include "myheader.h"

// include guards in header:
// #ifndef MYHEADER_H
// #define MYHEADER_H
// ... content
// #endif

#if 0 // block comment out
#endif

// #pragma once, __FILE__, __LINE__, __DATE__
```

## 20. File I/O

```c
#include <stdio.h>

FILE *f = fopen("data.txt", "w"); // r,w,a, r+, w+, a+, b for binary
if (!f) return 1;

fprintf(f, "Hello %d\n", 42);
fputs("Line\n", f);

fclose(f);

f = fopen("data.txt", "r");
char buf[100];
while (fgets(buf, sizeof(buf), f)) {
    printf("%s", buf);
}

fseek(f, 0, SEEK_SET); // SEEK_CUR, SEEK_END
long pos = ftell(f);
rewind(f);

int ch = fgetc(f);
fputc('A', f);

fclose(f);

// binary
FILE *bf = fopen("bin.dat", "wb");
int nums[]={1,2,3};
fwrite(nums, sizeof(int), 3, bf);
fclose(bf);

bf = fopen("bin.dat", "rb");
int out[3];
fread(out, sizeof(int), 3, bf);
fclose(bf);

// stdin stdout stderr are FILE*
fprintf(stderr, "Error!\n");
```

## 21. Bitwise Operators

```c
int a=5; // 0101
int b=3; // 0011
a & b; // 0001 AND
a | b; // 0111 OR
a ^ b; // 0110 XOR
~a;    // NOT
a << 1; // 1010 left shift
a >> 1; // 0010 right shift

// Masks & flags
#define FLAG_READ  (1<<0) // 1
#define FLAG_WRITE (1<<1) // 2
int flags = FLAG_READ | FLAG_WRITE;
if (flags & FLAG_READ) {}
flags |= FLAG_WRITE;
flags &= ~FLAG_READ;
```

## 22. Type Casting & void*

```c
int i=10;
float f = (float)i / 3;

void *vp = &i; // generic pointer
int *ip = (int*)vp;

int *p = (int*)malloc(sizeof(int)); // cast optional in C but okay

// implicit promotion: char -> int -> float -> double
```

## 23. Command Line Arguments

```c
// main signature
int main(int argc, char *argv[]) {
    printf("Args: %d\n", argc);
    for(int i=0;i<argc;i++) {
        printf("argv[%d]=%s\n", i, argv[i]);
    }
    // argv[0] is program name
    return 0;
}
// run: ./a.out hello 42
```

## 24. Function Pointers & Callbacks

```c
int add(int a,int b){return a+b;}
int sub(int a,int b){return a-b;}

int main() {
    int (*op)(int,int) = add;
    printf("%d\n", op(5,3)); // 8
    op = sub;
    printf("%d\n", op(5,3)); // 2

    // callback example with qsort
    int arr[]={3,1,4,1,5};
    int cmp(const void *a, const void *b){ return (*(int*)a - *(int*)b); }
    qsort(arr, 5, sizeof(int), cmp);

    // array of function pointers
    int (*ops[2])(int,int) = {add, sub};
}
```

## 25. Variadic Functions & Macros

```c
#include <stdarg.h>

int sum(int n, ...) {
    va_list args;
    va_start(args, n);
    int s=0;
    for(int i=0;i<n;i++) s+=va_arg(args, int);
    va_end(args);
    return s;
}
// sum(3, 10,20,30) -> 60

// variadic macro
#define LOGF(fmt, ...) printf("[LOG] " fmt "\n", ##__VA_ARGS__)
```

## 26. Header Files & Modular Code

```c
// mathutils.h
// #ifndef MATHUTILS_H
// #define MATHUTILS_H
// int add(int a,int b);
// #endif

// mathutils.c
// #include "mathutils.h"
// int add(int a,int b){return a+b;}

// main.c
// #include "mathutils.h"
// int main(){ add(2,3); }

// Compile: gcc main.c mathutils.c -o app
// Makefile snippet:
// app: main.c mathutils.c
//   gcc -Wall -Wextra -O2 -o app main.c mathutils.c
```

## 27. Error Handling, errno, assert

```c
#include <errno.h>
#include <string.h>
#include <assert.h>

FILE *f = fopen("no.txt","r");
if (!f) {
    printf("Error: %s (errno=%d)\n", strerror(errno), errno);
    perror("fopen"); // prints to stderr
}

int x=5;
assert(x>0); // aborts if false, use #include <assert.h>, disable with -DNDEBUG

// Return codes pattern
int divide(int a,int b,int *res){
    if(b==0) return -1; // error
    *res = a/b;
    return 0; // ok
}
```

## 28. Advanced: volatile, inline, _Generic

```c
volatile int sensor; // tells compiler value can change externally (hardware)

inline int max(int a,int b){ return a>b?a:b; } // hint to inline

// C11 _Generic - type-generic
#define print_val(x) _Generic((x), \
    int: printf("%d\n", x), \
    float: printf("%f\n", x), \
    double: printf("%lf\n", x), \
    default: printf("unknown\n") \
)
```

## 29. Common Pitfalls - Quick Check

```c
// 1. = vs ==
// if (x = 5) {} // bug, assigns

// 2. ; after if/for
// if (x==5); { printf("always\n"); }

// 3. Uninitialized var
// int x; printf("%d", x); // garbage

// 4. Buffer overflow
// char b[5]; strcpy(b, "toolong"); // overflow

// 5. Dangling pointer after free
// free(p); *p = 10; // UB

// 6. Off-by-one
// for(i=0;i<=n;i++) arr[i] // overflows if arr size n

// 7. scanf without &
// scanf("%d", x) // crash, need &x

// 8. Mixing = and ==, forgetting break in switch

// 9. Returning address of local var
// int* bad(){ int x=10; return &x; } // UB
```

## 30. Compilation & Tools CheatSheet

```bash
gcc file.c -o app           # compile
gcc -Wall -Wextra -Werror file.c -o app # all warnings as errors
gcc -g file.c -o app        # debug symbols for gdb/valgrind
gcc -O2 file.c -o app       # optimize
gcc -c file.c               # only object file .o
gcc main.c utils.c -o app   # multi-file

./app arg1 arg2
gdb ./app
valgrind ./app              # memory leak check
```

## 31. Mini Cheatsheet Table

| Concept | Syntax |
|---------|--------|
| printf | `printf("%d %s", n, s)` |
| scanf | `scanf("%d", &n)` |
| malloc | `int *p=malloc(n*sizeof(int))` |
| free | `free(p); p=NULL` |
| struct access | `s.field`, `ptr->field` |
| string len | `strlen(s)` |
| file open | `fopen("f.txt","r")` |
| function ptr | `int (*fp)(int,int)` |

---

**Tip:** Practice pattern: write small programs combining pointers + struct + malloc + file I/O. That's where most C interviews/bugs live.
