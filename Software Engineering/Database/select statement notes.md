
### SQL `SELECT` Statement Notes

**Purpose**: Retrieve data from a database.

**Basic Syntax**:

SQL

```sql
SELECT column1, column2, ...
FROM table_name;
```

AI-generated code. Review and use carefully. .

**Select All Columns**:

SQL

```sql
SELECT * FROM table_name;
```


**Filtering Data**:

- **WHERE Clause**: Filters records based on specified conditions.
    
    SQL
    
    ```sql
    SELECT column1, column2
    FROM table_name
    WHERE condition;
    ```
    
    

**Common Clauses**:

- **ORDER BY**: Sorts the result set.
    
    SQL
    
    ```sql
    SELECT column1, column2
    FROM table_name
    ORDER BY column1 [ASC|DESC];
    ```
    
    
- **GROUP BY**: Groups rows sharing a property so aggregate functions can be applied.
    
    SQL
    
    ```sql
    SELECT column1, COUNT(*)
    FROM table_name
    GROUP BY column1;
    ```
    
    
- **HAVING**: Filters groups based on a condition.
    
    SQL
    
    ```sql
    SELECT column1, COUNT(*)
    FROM table_name
    GROUP BY column1
    HAVING COUNT(*) > 1;
    ```
    
    

**Aggregate Functions**:

- **COUNT()**: Returns the number of rows.
- **SUM()**: Returns the sum of a numeric column.
- **AVG()**: Returns the average value of a numeric column.
- **MIN()**: Returns the smallest value.
- **MAX()**: Returns the largest value.

**Additional Conditions**:

- **SELECT DISTINCT**: Returns only distinct (different) values.
    
    SQL
    
    ```sql
    SELECT DISTINCT column1
    FROM table_name;
    ```
    
    
- **SELECT COUNT**: Returns the number of rows that match a specified criterion.
    
    SQL
    
    ```sql
    SELECT COUNT(column1)
    FROM table_name
    WHERE condition;
    ```
    
    
- **SELECT LIMIT**: Specifies the number of records to return.
    
    SQL
    
    ```sql
    SELECT column1, column2
    FROM table_name
    LIMIT number;
    ```
    
    
- **SELECT RANDOM**: Selects random rows (syntax may vary by database).
    
    SQL
    
    ```sql
    SELECT column1, column2
    FROM table_name
    ORDER BY RANDOM()
    LIMIT number;
    ```
    
    
- **SELECT SUM**: Returns the total sum of a numeric column.
    
    SQL
    
    ```sql
    SELECT SUM(column1)
    FROM table_name
    WHERE condition;
    ```
    
    
- **SELECT BETWEEN**: Filters the result set within a certain range.
    
    SQL
    
    ```sql
    SELECT column1, column2
    FROM table_name
    WHERE column1 BETWEEN value1 AND value2;
    ```
    
    

**Example**:

SQL

```sql
SELECT DISTINCT CustomerName, City
FROM Customers
WHERE Country = 'Germany'
ORDER BY CustomerName
LIMIT 10;
```

### SQL `LIKE` Clause

The `LIKE` operator is used in a `WHERE` clause to search for a specified pattern in a column. It is particularly useful for pattern matching in strings.

#### Wildcards

- **`%` (Percent Sign)**: Represents zero, one, or multiple characters.
    - Example: `LIKE 'a%'` matches any string starting with ‘a’.
- **`_` (Underscore)**: Represents a single character.
    - Example: `LIKE 'a_'` matches any string starting with ‘a’ followed by exactly one character.

#### Examples

1. **Starts With**:
    
    SQL
    
    ```sql
    SELECT * FROM patients WHERE first_name LIKE 'Ab%';
    ```
    
    AI-generated code. Review and use carefully. .
    
    This query retrieves all patients whose first names start with “Ab”.
    
2. **Ends With**:
    
    SQL
    
    ```sql
    SELECT * FROM patients WHERE first_name LIKE '%son';
    ```
    
    AI-generated code. Review and use carefully. .
    
    This query retrieves all patients whose first names end with “son”.
    
3. **Contains**:
    
    SQL
    
    ```sql
    SELECT * FROM patients WHERE first_name LIKE '%ann%';
    ```
    
    AI-generated code. Review and use carefully. .
    
    This query retrieves all patients whose first names contain “ann”.
    
4. **Single Character Match**:
    
    SQL
    
    ```sql
    SELECT * FROM patients WHERE first_name LIKE 'A_';
    ```
    
    AI-generated code. Review and use carefully. .
    
    This query retrieves all patients whose first names start with “A” and are exactly two characters long.