
# ⏱️ MySQL Triggers — Explained

## 🔹 What Is a Trigger?

A **trigger** is a special stored program in MySQL that automatically executes (fires) in response to certain events on a table — such as `INSERT`, `UPDATE`, or `DELETE`.

## 🔹 Syntax


```sql
CREATE TRIGGER trigger_name
AFTER INSERT ON table_name
FOR EACH ROW
BEGIN
   -- SQL statements here
END;
```

- `AFTER` or `BEFORE` → defines when the trigger runs.
    
- `INSERT`, `UPDATE`, `DELETE` → defines which action activates the trigger.
    
- `FOR EACH ROW` → runs once for every affected row.
    

## 🔹 Example: Log Customer Inserts

Suppose we want to log whenever a new customer is added.

### Step 1: Create a log table



```sql
CREATE TABLE customer_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(50),
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Step 2: Create the trigger



```sql
CREATE TRIGGER after_customer_insert
AFTER INSERT ON customers
FOR EACH ROW
BEGIN
   INSERT INTO customer_log (customer_name)
   VALUES (NEW.name);
END;
```

- `NEW.name` → refers to the value of the newly inserted row.
    
- Every time a customer is added, their name is logged automatically.
    

## 🔹 Example: Prevent Negative Stock



```sql
CREATE TRIGGER before_product_update
BEFORE UPDATE ON products
FOR EACH ROW
BEGIN
   IF NEW.stock < 0 THEN
      SET NEW.stock = 0;
   END IF;
END;
```

✅ Ensures stock values never go below zero.

## 🔹 Benefits

- **Automation** → actions happen automatically.
    
- **Data integrity** → enforce rules (e.g., no negative stock).
    
- **Auditing** → log changes for accountability.
    

## ✅ Summary

- A **trigger** runs automatically when a table event occurs.
    
- Use `BEFORE` or `AFTER` with `INSERT`, `UPDATE`, or `DELETE`.
    
- Access row values with `NEW` (for inserted/updated data) and `OLD` (for deleted/updated data).
    
- Great for enforcing rules and logging changes.