
## 🔹 1. `std::cout` with manipulators (classic way)

You can format directly when printing:


```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    double price = 3.14159;
    cout << fixed << setprecision(2) << "Price: " << price << endl;
}
```

- `fixed` → use fixed‑point notation
    
- `setprecision(2)` → 2 decimal places
    
- Similar to Python’s format specifiers.
    

## 🔹 2. `std::ostringstream` (string stream formatting)

You can build a formatted string before printing:



```cpp
#include <iostream>
#include <sstream>
#include <iomanip>
using namespace std;

int main() {
    double pi = 3.14159;
    ostringstream oss;
    oss << "Pi = " << fixed << setprecision(3) << pi;
    string result = oss.str();
    cout << result;
}
```

- This gives you a **formatted string object** (`result`) you can reuse.
    

## 🔹 3. `std::format` (C++20 and newer)

Finally, modern C++ introduced `std::format`, which is very close to Python’s f‑strings:


```cpp
#include <iostream>
#include <format>
using namespace std;

int main() {
    string name = "Reuben";
    int age = 25;
    cout << format("Hello {}, you are {} years old", name, age);
}
```

- `{}` placeholders just like Python’s `f"..."`.
    
- Requires a compiler with **C++20 support** (e.g., GCC 13+, Clang 15+, MSVC recent versions).
    

## ✅ Summary

- **Older C++** → use `std::cout` + `<iomanip>` or `ostringstream`.
    
- **Modern C++20** → use `std::format`, which feels almost identical to Python’s f‑strings.



## ✅ How to Fix

Compile with the correct standard flag:


```bash
g++ -std=c++20 main.cpp -o main
```

Then run:

```bash
./main
```

## 🔹 Quick Tip

If you want to avoid “messing up the command you have in your head,” you can make **C++20 the default** by setting an alias in your shell:



```bash
alias g++='g++ -std=c++20'
```

Add that line to your `~/.bashrc` or `~/.zshrc`, then reload:



```bash
source ~/.bashrc
```

Now every time you type `g++ main.cpp -o main`, it will automatically compile with C++20.

## ✅ Takeaway

- Your GCC version is fine (13.3.0).
    
- Just add `-std=c++20` or set an alias so you don’t have to remember the flag each time.


working example:

```cpp

#include <iostream>
#include <string>
#include <format>
#include <limits>

int main() {
    std::string fullName{};
    std::cout << "Enter your full name: ";
    std::getline(std::cin, fullName);

    int age{};
    std::cout << "Enter your age: ";
    std::cin >> age;

    std::cout << std::format("Your name is {} and you are {} years old", fullName, age);
}


```