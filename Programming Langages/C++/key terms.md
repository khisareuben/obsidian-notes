
`Progam/code/source code` - A sequence of instructions written by humans

`Machine code` - Code that can run on a machine

`Statement` - Type of instruction

`Syntax` - Rules of a programming language

`Compiler` - A software that translate source code to machine code in one go

`Interpreter` - A software that translate source code to machine one line by line

`Execution` - The process of running a program

`Syntax error` - A mistake in the syntax of a code

`Logic error` - A mistake that produces wrong result

`Runtime error` - Error during program execution

`Bug` - An error in a program

`Debug` - The process of finding and fixing bugs



## 📋 Categories of C++ Keywords

| Category                  | Keywords                                                                                                                   | Purpose                                                           |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| **Data Types**            | `int`, `char`, `float`, `double`, `void`, `bool`, `long`, `short`, `signed`, `unsigned`, `wchar_t`, `char16_t`, `char32_t` | Define variable types.                                            |
| **Control Flow**          | `if`, `else`, `switch`, `case`, `default`, `for`, `while`, `do`, `break`, `continue`, `goto`                               | Direct program execution.                                         |
| **Boolean & Null**        | `true`, `false`, `nullptr`                                                                                                 | Represent logical values and null pointers.                       |
| **Memory Management**     | `new`, `delete`, `sizeof`, `alignas`, `alignof`                                                                            | Allocate, free, and inspect memory.                               |
| **Classes & Structs**     | `class`, `struct`, `union`, `enum`, `friend`, `mutable`, `this`                                                            | Define and manage user‑defined types.                             |
| **Access Specifiers**     | `public`, `private`, `protected`                                                                                           | Control visibility of members.                                    |
| **Functions & Modifiers** | `inline`, `explicit`, `virtual`, `override`, `final`, `constexpr`, `operator`, `typedef`, `using`, `typename`              | Modify function behavior and type usage.                          |
| **Templates & Generics**  | `template`, `concept`, `requires`                                                                                          | Enable generic programming.                                       |
| **Exception Handling**    | `try`, `catch`, `throw`, `noexcept`                                                                                        | Manage runtime errors.                                            |
| **Casting & Type Info**   | `const_cast`, `dynamic_cast`, `reinterpret_cast`, `static_cast`, `decltype`, `typeid`                                      | Convert and inspect types.                                        |
| **Constants & Storage**   | `const`, `static`, `extern`, `register`, `thread_local`, `volatile`, `static_assert`                                       | Control variable lifetime and linkage.                            |
| **Modules / Namespaces**  | `export`, `namespace`                                                                                                      | Organize code into modules.                                       |
| **Coroutines (C++20)**    | `co_await`, `co_return`, `co_yield`                                                                                        | Support asynchronous programming.                                 |
| **Alternative Operators** | `and`, `or`, `not`, `xor`, `bitand`, `bitor`, `compl`, `and_eq`, `or_eq`, `not_eq`, `xor_eq`                               | Alternative spellings for operators.                              |
| **Miscellaneous**         | `asm`, `auto`, `return`                                                                                                    | Special cases (inline assembly, type inference, function return). |

## 📋 C++ Naming Conventions

| Category             | Convention Style                           | Example Name             |
| -------------------- | ------------------------------------------ | ------------------------ |
| **Variables**        | camelCase or snake_case                    | studentAge / student_age |
| **Constants**        | UPPER_CASE with underscores                | MAX_STUDENTS             |
| **Functions**        | camelCase                                  | calculateAverage         |
| **Classes/Structs**  | PascalCase                                 | StudentRecord            |
| **Namespaces**       | lowercase or snake_case                    | school_management        |
| **Member Variables** | Prefix `m_` or suffix `_`                  | m_age / name_            |
| **Global Variables** | Prefix `g_`                                | g_totalStudents          |
| **Enums**            | PascalCase for type, UPPER_CASE for values | Color / RED              |
| **Macros**           | UPPER_CASE with underscores                | DEBUG_MODE               |
