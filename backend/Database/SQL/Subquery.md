
# 📌 MySQL SUBQUERY — Explained

## 🔹 What Is a Subquery?

A **subquery** is a query nested inside another SQL query. It’s used when you need results from one query to feed into another.

## 🔹 Syntax



```sql
SELECT column
FROM table
WHERE column IN (SELECT column FROM other_table WHERE condition);
```

- The inner query runs first.
    
- The outer query uses its result.
    

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

## 🔹 Subquery Example

Find customers who placed orders:



```sql
SELECT name
FROM customers
WHERE id IN (SELECT customer_id FROM orders);
```

**Result**

|name|
|---|
|Alice|
|Bob|

✅ The inner query `(SELECT customer_id FROM orders)` returns `[1, 2]`. The outer query then selects customers whose `id` is in that list.

## 🔹 Types of Subqueries

- **Single‑row subquery** → returns one value, used with `=`.
    
- **Multi‑row subquery** → returns multiple values, used with `IN`.
    
- **Correlated subquery** → references columns from the outer query, runs repeatedly.
    

## ✅ Summary

- A **subquery** is a query inside another query.
    
- Useful for filtering, comparisons, and complex conditions.
    
- Can be single‑row, multi‑row, or correlated.
    
- Always runs **inner query first**, then outer query uses its result.