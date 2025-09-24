
## **Basic Math Functions**

| Formula           | Description                   | Example                       |
| ----------------- | ----------------------------- | ----------------------------- |
| `=SUM(A1:A5)`     | Adds all numbers in the range | Adds values in cells A1 to A5 |
| `=AVERAGE(B1:B5)` | Calculates the mean           | Average of B1 to B5           |
| `=MIN(C1:C5)`     | Finds the smallest value      | Minimum in C1 to C5           |
| `=MAX(D1:D5)`     | Finds the largest value       | Maximum in D1 to D5           |
| `=ROUND(E1, 2)`   | Rounds to 2 decimal places    | Rounds E1 to 2 digits         |
| `=LARGE(B1:B6,2)` | Returns the second largest    | Second largest number         |

## 📊 **Logical Functions**

|Formula|Description|Example|
|---|---|---|
|`=IF(A1>100, "High", "Low")`|Returns "High" if A1 > 100, else "Low"|Decision-making|
|`=AND(A1>50, B1<100)`|Returns TRUE if both are true|Logical test|
|`=OR(A1>50, B1<100)`|Returns TRUE if either is true|Logical test|
|`=NOT(A1>100)`|Reverses logic|TRUE if A1 ≤ 100|

## 🔍 **Lookup & Reference**

|Formula|Description|Example|
|---|---|---|
|`=VLOOKUP("John", A2:C10, 2, FALSE)`|Finds "John" in column A and returns value from column B|Vertical lookup|
|`=HLOOKUP("Math", A1:D5, 2, FALSE)`|Horizontal lookup|Finds "Math" in row 1|
|`=INDEX(A2:C5, 2, 3)`|Returns value at row 2, column 3|Flexible lookup|
|`=MATCH(90, A1:A10, 0)`|Finds position of 90 in A1:A10|Returns row number|

## 📅 **Date & Time Functions**

|Formula|Description|Example|
|---|---|---|
|`=TODAY()`|Returns current date|Auto-updates daily|
|`=NOW()`|Returns current date & time|Real-time stamp|
|`=DATEDIF(A1, B1, "d")`|Days between two dates|Difference in days|
|`=TEXT(A1, "dd-mm-yyyy")`|Formats date|Custom date format|

## 🔠 **Text Functions**

|Formula|Description|Example|
|---|---|---|
|`=CONCAT(A1, B1)`|Joins text from A1 and B1|Combines names|
|`=LEFT(A1, 5)`|First 5 characters from left|Extracts prefix|
|`=RIGHT(A1, 3)`|Last 3 characters|Extracts suffix|
|`=LEN(A1)`|Counts characters|Useful for validation|
|`=TRIM(A1)`|Removes extra spaces|Cleans data|

## 📋 **Statistical & Count Functions**

|Formula|Description|Example|
|---|---|---|
|`=COUNT(A1:A10)`|Counts numbers only|Ignores text|
|`=COUNTA(A1:A10)`|Counts non-empty cells|Includes text|
|`=COUNTIF(A1:A10, ">50")`|Counts cells > 50|Conditional count|
|`=SUMIF(A1:A10, ">50")`|Sums cells > 50|Conditional sum|
|`=AVERAGEIF(A1:A10, ">50")`|Average of cells > 50|Conditional average|

## 🧠 **Information Functions**

| Formula         | Description              | Example               |
| --------------- | ------------------------ | --------------------- |
| `=ISNUMBER(A1)` | Checks if A1 is a number | Returns TRUE/FALSE    |
| `=ISBLANK(A1)`  | Checks if A1 is empty    | Useful for validation |
| `=ISERROR(A1)`  | Checks for any error     | Returns TRUE if error |


## What Does `A2:D100` Mean?

This is a **range**—a rectangular block of cells in Excel.

- **Starts at cell A2** (top-left corner)
    
- **Ends at cell D100** (bottom-right corner)
    
- Includes **columns A to D** and **rows 2 to 100**
    

So it covers:

- A2 to A100 (first column)
    
- B2 to B100 (second column)
    
- C2 to C100 (third column)
    
- D2 to D100 (fourth column)
    

It’s like selecting a table with 4 columns and 99 rows.

## 🧠 What Does “Searches for a Value in the First Column” Mean?

Let’s say you have this table:

| A (ID) | B (Name) | C (Department) | D (Salary) |
| ------ | -------- | -------------- | ---------- |
| EMP001 | Alice    | HR             | 50,000     |
| EMP002 | Brian    | IT             | 60,000     |
| EMP003 | Carol    | Finance        | 55,000     |

Now, you want to **find the salary of EMP002**.

You use:



```excel
=VLOOKUP("EMP002", A2:D100, 4, FALSE)
```

### 🔍 Breakdown:

- `"EMP002"` → the value you're searching for
    
- `A2:D100` → the table you're searching in
    
- `4` → the column number to return from (column D = Salary)
    
- `FALSE` → exact match only
    

### ✅ Result: `60,000`

Excel looks in **column A** (the first column of the range), finds `EMP002`, then jumps to **column 4** of that same row and returns the salary.

## 🧭 How to Make Sense of It

Think of `VLOOKUP` like asking:

> “In this table, find the row where the first column matches my search, then give me the value from another column in that same row.”

It’s like scanning a list of student IDs and saying:

> “Find student ID `STU045` and tell me their grade.”

## 🧪 Try This Exercise

Imagine this table in Excel:

|A (Student ID)|B (Name)|C (Subject)|D (Score)|
|---|---|---|---|
|STU001|John|Math|78|
|STU002|Mary|English|85|
|STU003|Peter|Science|90|

To find Peter’s score:



```excel
=VLOOKUP("STU003", A2:D100, 4, FALSE)
```

Returns: `90`