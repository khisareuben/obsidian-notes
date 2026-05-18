
# ⚙️ MySQL Stored Procedures — Explained

## 🔹 What Is a Stored Procedure?

A **stored procedure** is a set of SQL statements saved in the database that you can execute later with a single call. It’s useful for reusing logic, automating tasks, and improving performance.

## 🔹 Syntax



```sql
DELIMITER //

CREATE PROCEDURE procedure_name()
BEGIN
   -- SQL statements here
END //

DELIMITER ;
```

- `DELIMITER` changes the command terminator so MySQL knows where the procedure ends.
    
- `BEGIN ... END` wraps the procedure body.
    

## 🔹 Example: Get All Customers



```sql
DELIMITER //

CREATE PROCEDURE GetAllCustomers()
BEGIN
   SELECT * FROM customers;
END //

DELIMITER ;
```

### Run the procedure:



```sql
CALL GetAllCustomers();
```

✅ This executes the stored procedure and returns all rows from `customers`.

## 🔹 Example With Parameters



```sql
DELIMITER //

CREATE PROCEDURE GetCustomerOrders(IN cust_id INT)
BEGIN
   SELECT * FROM orders WHERE customer_id = cust_id;
END //

DELIMITER ;
```

### Run the procedure:



```sql
CALL GetCustomerOrders(2);
```

✅ Returns all orders for customer with `id = 2`.

## 🔹 Benefits

- **Reusability** → Write once, call many times.
    
- **Security** → Control access by exposing procedures instead of raw tables.
    
- **Performance** → Precompiled, reduces repeated parsing.
    
- **Maintainability** → Centralize business logic in the database.
    

## ✅ Summary

- A **stored procedure** is a saved SQL routine.
    
- Use `CREATE PROCEDURE` to define, `CALL` to execute.
    
- Can accept **parameters** for dynamic queries.
    
- Great for automation, security, and consistency.



```sql
DELIMITER $$ --change delimiter temporarily

CREATE PROCEDURE get_customers() 
BEGIN
	SELECT * FROM customers;
END$$

DELIMITER ; --change back to the original delimiter

CALL get_customers();

DROP PROCEDURE get_customers;
```

```sql
DELIMITER $$ --change delimiter temporarily

CREATE PROCEDURE find_customer(IN id INT) 
BEGIN
	SELECT * FROM customers
	WHERE customer_id = id;
END$$

DELIMITER ;

CALL find_customer(2);
```