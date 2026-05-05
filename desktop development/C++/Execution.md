

## 🔧 The Two-Step Process

Let's say you have a file called `hello.cpp`:

### Step 1: Compile the code

bash

g++ hello.cpp -o hello

|Part|What it means|
|---|---|
|`g++`|The C++ compiler command|
|`hello.cpp`|Your source code file|
|`-o hello`|"Output" – name the executable file `hello` (you can pick any name)|

### Step 2: Run the executable

bash

./hello

The `./` means "look in the current folder for a program called hello."

## 📝 Full Example

Create a simple C++ file first:

bash

```
echo '#include <iostream>
int main() {
    std::cout << "Hello from C++" << std::endl;
    return 0;
}' > hello.cpp
```

Then compile and run:

bash

```
g++ hello.cpp -o hello
./hello
```
**Output:**

text

Hello from C++

## 🧠 Useful Variations

|What you want|Command|
|---|---|
|Compile with warnings (always do this)|`g++ -Wall hello.cpp -o hello`|
|Use C++11 standard|`g++ -std=c++11 hello.cpp -o hello`|
|Compile multiple files|`g++ main.cpp helper.cpp -o program`|
|Run without creating a named file|`g++ hello.cpp && ./a.out` (defaults to `a.out`)|
|Re-compile and run in one line|`g++ hello.cpp -o hello && ./hello`|

## ⚠️ Common Errors & Fixes

|Error message|What it means|Fix|
|---|---|---|
|`g++: command not found`|Compiler not installed|`sudo apt install g++`|
|`permission denied`|File can't execute|`chmod +x hello` then `./hello`|
|`undefined reference`|Missing library or function|Add `-lm` for math library, etc.|

## 💡 Pro Tip for QML + C++

When you start mixing QML with C++, you will use `cmake` instead of direct `g++` commands. But for learning pure C++ first, the `g++` terminal method is perfect.