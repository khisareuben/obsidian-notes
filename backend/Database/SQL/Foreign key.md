
## 🔹 What a Foreign Key Is

A **foreign key** is a column in one table that **references the primary key** of another table. It creates a **relationship** between the two tables.

Example:

- `customers.id` → **primary key** (unique for each customer)
    
- `orders.customer_id` → **foreign key** (points to `customers.id`)
    

## 🔹 How They Become “Identical”

They’re not automatically identical — you **make them identical by design** when inserting data.

### Step 1: Create the tables



```sql
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    city VARCHAR(50)
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    product VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

✅ The `FOREIGN KEY (customer_id)` line tells MySQL:

> “Every value in `orders.customer_id` must exist in `customers.id`.”

### Step 2: Insert matching data



```sql
INSERT INTO customers (name, city)
VALUES ('Alice', 'Nairobi'), ('Bob', 'Mombasa'), ('Carol', 'Kisumu');

INSERT INTO orders (customer_id, product)
VALUES (1, 'Laptop'), (2, 'Phone'), (2, 'Tablet');
```

✅ Here, the numbers `1` and `2` in `customer_id` match the `id` values in `customers`. That’s how the link is formed — **you insert the same ID manually or via application logic**.

### Step 3: MySQL enforces the link

If you try to insert an order with a non‑existent `customer_id`, MySQL will reject it:



```sql
INSERT INTO orders (customer_id, product) VALUES (99, 'Camera');
```

❌ Error: _Cannot add or update a child row: a foreign key constraint fails._

## 🔹 Why This Matters for JOINS

When you run:



```sql
SELECT c.name, o.product
FROM customers AS c
INNER JOIN orders AS o ON c.id = o.customer_id;
```

MySQL matches rows **where** `customers.id` **equals** `orders.customer_id` — that’s the foreign key relationship in action.

## ✅ Takeaway

- **Primary key** → unique identifier in the parent table.
    
- **Foreign key** → column in the child table referencing that primary key.
    
- They’re “identical” because you insert matching values, and MySQL enforces that link.
    
- This relationship is what makes joins possible and reliable.