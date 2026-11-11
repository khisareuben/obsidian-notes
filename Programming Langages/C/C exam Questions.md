`Grade System`
```c
#include <stdio.h>
#include <string.h>

// write a c programm to read a student name and the score for a particula subject. They should output grades as shown:
//  above 90 "A"
// 80 - 89 "B"
//  70 - 79 "C"
// 60-69 "C"
//  Below 60 "FAIL"

int main()
{

    char name[50];
    int score;
    printf("Enter name: ");
    fgets(name, sizeof(name), stdin);
    // name[strcspn(name, "\n")] = '\0';

    printf("Enter score: ");
    scanf("%d", &score);
    if (score >= 90)
        printf("A");
    else if (score >= 80)
        printf("B");
    else if (score >= 70)
        printf("C");
    else if (score >= 60)
        printf("D");
    else
        printf("FAIL");

    return 0;
}
```

`Factorial`
```c
#include <stdio.h>

int main()
{

    int n, i;
    long long f = 1;

    printf("Enter and interger: ");
    scanf("%d", &n);

    for (i = 2; i <= n; i++)
    {
        printf("%d ", i);
        f *= i;
    }

    printf("\n%lld", f);

    return 0;
}
```


`ascending array`
```c
#include <stdio.h>

int main()
{

    int score[10], i, j, t;

    for (i = 0; i < 10; i++)
    {
        printf("Enter number: ");
        scanf("%d", &score[i]);
    }

    for (i = 0; i < 9; i++)
        for (j = 0; j < 9 - i; j++)
            if (score[j] > score[j + 1])
            {
                t = score[j];
                score[j] = score[j + 1];
                score[j + 1] = t;
            }
    for (i = 0; i < 10; i++)
        printf("%d ", score[i]);

    return 0;
}
```

`Smallest of Three`
```c
#include <stdio.h>

int main()
{

    int a, b, c, s;
    scanf("%d %d %d", &a, &b, &c);
    s = a;
    if (b < s)
        s = b;
    if (c < s)
        s = c;

    printf("Smallest %d", s);

    return 0;
}
```

`Cube Function`
```c
#include <stdio.h>

int cube(int x)
{
    return x * x * x;
}

int main()
{

    int x;
    scanf("%d", &x);
    printf("%d", cube(x));

    return 0;
}
```

`Sum avg while`
```c
#include <stdio.h>

int main()
{

    int i = 0, n, sum = 0;

    while (i < 3)
    {
        scanf("%d", &n);
        sum += n;
        i++;
    }

    printf("Sum %d Avg %.2f", sum, sum / 3.0);

    return 0;
}
```

`Largest of 10`
```c
#include <stdio.h>

int main()
{

    int num[10], i, l;

    for (i = 0; i < 10; i++)
    {
        printf("Enter number: ");
        scanf("%d", &num[i]);
    }

    l = num[0];

    for (i = 0; i < 10; i++)
    {
        if (num[i] > l)
            l = num[i];
    }

    printf("Largest: %d", l);

    return 0;
}
```


`Area with Switch`
```c
#include <stdio.h>
#define PI 3.14159

float circle(float r)
{
    return PI * r * r;
}
float rectangle(float l, float w)
{
    return l * w;
}
float cylinder(float r, float h)
{
    return 2 * PI * r * (r + h);
}

int main()
{
    int ch;
    float r, l, w, h;
    printf("Choose 1 For area of a Circle \nChoose 2 For area of a Rectangle \nChoose 3 For area of a cylinder\n");
    printf("Choose: ");
    scanf("%d", &ch);
    switch (ch)
    {
    case 1:
        printf("\nEnter Radius: ");
        scanf("%f", &r);
        printf("%.2f", circle(r));
        break;
    case 2:
        printf("\nEnter Length and Width: ");
        scanf("%f %f", &l, &w);
        printf("%.2f", rectangle(l, w));
        break;
    case 3:
        printf("\nEnter Radius and height: ");
        scanf("%f %f", &r, &h);
        printf("%.2f", cylinder(r, h));
        break;
    }
    return 0;
}
```

`Sum Avg Even 1-100`
```c
#include <stdio.h>

int main()
{

    int i, sum = 0, c = 0;
    for (i = 1; i <= 100; i++)
    {
        if (i % 2 == 0)
        {
            sum += i;
            c++;
        }
    }
    float avg = sum / c;
    printf("Sum %d Avg %.2f", sum, avg);

    return 0;
}
```


`Sum 1-10 For`
```c
#include <stdio.h>

int main()
{

    int i, sum = 0;
    for (i = 1; i <= 10; i++)
    {
        sum += i;
    }

    printf("Sum: %d\n", sum);

    return 0;
}
```

