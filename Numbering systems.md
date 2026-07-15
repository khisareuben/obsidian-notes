

The secret to mastering this easily is to stop treating them as separate systems and use a **Hub-and-Spoke** mental model.

## 1. The "Hub-and-Spoke" Mental Model

Instead of trying to connect every base to every other base directly, use **Decimal (Base 10)** as your central hub.

If you want to convert from Octal (Base 8) to Hexadecimal (Base 16), don't look for an "Octal-to-Hex" formula. Just convert **Octal $\to$ Decimal**, and then **Decimal $\to$ Hex**.

By doing this, you only ever have to learn **two universal formulas** to convert _any_ base to _any_ other base:

```
                  [ ANY BASE ]
                   ^        |
     Rule 2:       |        |   Rule 1:
     Divide &      |        |   Multiply
     Remainder     |        v
                  [ DECIMAL ] (The Hub)
```

### Rule 1: Going TO Decimal (The "Multiply" Rule)

To convert **any base** to Decimal, write down the digits, assign them positional powers of your starting base (starting at 0 from the right), and multiply.

For example, to convert Hexadecimal $3\text{A}$ (Base 16) to Decimal:

1. Write the digits: $3$ and $\text{A}$ (which is $10$).
    
2. Assign powers of 16 from right to left: $16^1$ and $16^0$.
    
3. Multiply and add:
    
    $$(3 \times 16^1) + (10 \times 16^0) = 48 + 10 = 58$$
    

### Rule 2: Going FROM Decimal (The "Divide & Remainder" Rule)

To convert **Decimal** to any base, repeatedly divide the decimal number by your target base. Write down the remainders from **bottom to top** (or last to first).

For example, to convert Decimal $58$ to Hexadecimal (Base 16):

1. $58 \div 16 = 3$ with a remainder of **$10$** (which is **$\text{A}$**).
    
2. $3 \div 16 = 0$ with a remainder of **$3$**.
    
3. Read the remainders from bottom to top: **$3\text{A}$**.
    

## 2. The "Powers of 2" Shortcut (The Ultimate Cheat Code)

There is one major exception where you should **never** use the Decimal hub: when converting between **Binary (2), Octal (8), and Hex (16)**. Because 8 and 16 are perfect powers of 2, they map to each other perfectly:

- **Octal (Base 8):** $2^3 = 8$. This means **1 Octal digit = exactly 3 Binary bits**.
    
- **Hexadecimal (Base 16):** $2^4 = 16$. This means **1 Hex digit = exactly 4 Binary bits**.
    

### Converting Hex $\leftrightarrow$ Binary instantly:

If you have the Hex number $\text{B}5$:

1. Split it: $\text{B}$ and $5$.
    
2. Convert each directly to 4-bit binary ($\text{B} = 11$, which is $1011$; $5$ is $0101$).
    
3. Put them together: $10110101$.
    

You can do this entire process in reverse to go from Binary to Hex just by grouping the bits into blocks of 4 starting from the right!