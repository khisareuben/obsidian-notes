

# 📘 C++ Notes – Enum

## Introduction

- **Enum (enumeration)** is a user‑defined type that consists of a set of named integral constants.
    
- Useful for representing fixed sets of related values (e.g., days of the week, colors, states).
    
- Improves code readability and reduces errors compared to using raw integers.
    

## Basic Enum



```cpp
enum Color { RED, GREEN, BLUE };

Color myColor = RED;

if (myColor == RED) {
    cout << "Color is red";
}
```

- By default, values start at **0** and increment by 1.
    
    - `RED = 0`, `GREEN = 1`, `BLUE = 2`.
        

## Custom Values



```cpp
enum Status { PENDING = 1, APPROVED = 5, REJECTED = 10 };

Status s = APPROVED;
cout << s; // prints 5
```

- You can assign specific integer values to enum members.
    
- Useful when mapping to external codes or protocols.
    

## Scoped Enum (C++11 – `enum class`)



```cpp
enum class Direction { NORTH, SOUTH, EAST, WEST };

Direction d = Direction::NORTH;

if (d == Direction::NORTH) {
    cout << "Going north";
}
```

- **Scoped enums** prevent name conflicts.
    
- Values must be accessed with the scope operator (`Direction::NORTH`).
    
- Strongly typed (cannot implicitly convert to int).
    

## Underlying Type



```cpp
enum class ErrorCode : int { OK = 0, NotFound = 404, ServerError = 500 };
```

- You can specify the **underlying type** (`int`, `char`, `unsigned int`).
    
- Useful when working with specific ranges or external systems.
    

## Iterating Enums

Enums don’t directly support iteration, but you can simulate it:



```cpp
enum Day { MON, TUE, WED, THU, FRI, SAT, SUN };

for (int d = MON; d <= SUN; d++) {
    cout << d << endl;
}
```

## Best Practices

- Use `enum class` instead of plain `enum` in modern C++ for type safety.
    
- Prefer descriptive names (`Status::Approved` instead of just `APPROVED`).
    
- Use enums when values are fixed and finite.
    

## ✅ Quick Summary

- **Plain enum**: older style, values are global, auto‑convert to int.
    
- **Scoped enum (**`enum class`**)**: modern style, safer, avoids conflicts.
    
- **Custom values**: map enums to meaningful integers.
    
- **Underlying type**: control storage type.