
# 🧩 MySQL JOINS — Detailed Notes

## 🔹 What Is a JOIN?

A **JOIN** combines rows from two or more tables based on a related column between them. It’s used to retrieve data that’s spread across multiple tables.

## 🔹 Common Types of JOINS

| **Join Type**  | **Description**                                                                                                                             | **Example Use Case**                                     |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| **INNER JOIN** | Returns rows that have matching values in both tables.                                                                                      | Get customers who placed orders.                         |
| **LEFT JOIN**  | Returns all rows from the left table and matching rows from the right table.                                                                | List all customers, even those without orders.           |
| **RIGHT JOIN** | Returns all rows from the right table and matching rows from the left table.                                                                | List all orders, even if customer info is missing.       |
| **FULL JOIN**  | Returns all rows when there’s a match in either table. _(MySQL doesn’t support FULL JOIN directly; use_ `UNION` _of LEFT and RIGHT joins.)_ | Combine all customers and orders, matched or not.        |
| **CROSS JOIN** | Returns the Cartesian product of both tables (every row from one with every row from the other).                                            | Generate combinations, e.g., all product‑category pairs. |

## 🔹 Example Tables

**Customers**

|id|name|city|
|---|---|---|
|1|Alice|Nairobi|
|2|Bob|Mombasa|
|3|Carol|Kisumu|

**Orders**

|id|customer_id|product|
|---|---|---|
|1|1|Laptop|
|2|2|Phone|
|3|2|Tablet|

## 🔹 INNER JOIN Example


```sql
SELECT customers.name, orders.product
FROM customers
INNER JOIN orders ON customers.id = orders.customer_id;
```

**Result**

|name|product|
|---|---|
|Alice|Laptop|
|Bob|Phone|
|Bob|Tablet|

✅ Only customers who have orders appear.

## 🔹 LEFT JOIN Example

```sql
SELECT customers.name, orders.product
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id;
```

**Result**

|name|product|
|---|---|
|Alice|Laptop|
|Bob|Phone|
|Bob|Tablet|
|Carol|NULL|

✅ Carol appears even though she has no order.

## 🔹 RIGHT JOIN Example


```sql
SELECT customers.name, orders.product
FROM customers
RIGHT JOIN orders ON customers.id = orders.customer_id;
```

✅ Shows all orders, even if the customer is missing (rare but possible).

## 🔹 FULL JOIN (Simulated)

```sql
SELECT customers.name, orders.product
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id
UNION
SELECT customers.name, orders.product
FROM customers
RIGHT JOIN orders ON customers.id = orders.customer_id;
```

✅ Combines both sides — all customers and all orders.

## 🔹 CROSS JOIN Example

```sql
SELECT customers.name, orders.product
FROM customers
CROSS JOIN orders;
```

✅ Every customer paired with every product (use carefully — can produce huge results).

## 🔹 Practical Tips

- Always specify the **join condition** (`ON table1.column = table2.column`).
    
- Use **table aliases** for readability:
    
    
    ```sql
    SELECT c.name, o.product
    FROM customers AS c
    INNER JOIN orders AS o ON c.id = o.customer_id;
    ```
    
- Avoid unnecessary joins — they slow down queries.
    
- Use **indexes** on join columns for better performance.
    

## ✅ Summary

|Join Type|Returns|
|---|---|
|INNER|Matching rows only|
|LEFT|All left + matched right|
|RIGHT|All right + matched left|
|FULL|All rows from both sides|
|CROSS|All possible combinations|