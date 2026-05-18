
# 🔄 MySQL SELF JOIN — Explained

## 🔹 What Is a Self Join?

A **self join** is when a table is joined with itself. It’s useful when you want to compare rows within the same table — for example, finding relationships between employees in an organization.

## 🔹 Syntax



```sql
SELECT a.column, b.column
FROM table_name AS a
JOIN table_name AS b
ON a.common_field = b.common_field;
```

Here, `a` and `b` are **aliases** for the same table.

## 🔹 Example Table: Employees

|id|name|manager_id|
|---|---|---|
|1|Alice|NULL|
|2|Bob|1|
|3|Carol|1|
|4|David|2|

- `id` → employee ID
    
- `manager_id` → references the `id` of another employee (their manager)
    

## 🔹 Self Join Example



```sql
SELECT e.name AS Employee, m.name AS Manager
FROM employees AS e
LEFT JOIN employees AS m
ON e.manager_id = m.id;
```

**Result**

|Employee|Manager|
|---|---|
|Alice|NULL|
|Bob|Alice|
|Carol|Alice|
|David|Bob|

✅ Each employee is matched with their manager from the same table.

## 🔹 Practical Uses

- **Organizational hierarchy** → employees and managers.
    
- **Recursive relationships** → categories and subcategories.
    
- **Comparisons** → finding rows with similar attributes in the same table.
    

## ✅ Summary

- A **self join** is just a normal join, but the table is referenced twice with different aliases.
    
- It’s powerful for hierarchical or recursive data.
    
- Always use **aliases**