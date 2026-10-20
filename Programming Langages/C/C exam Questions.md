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
    {#include <stdio.h>

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

