
We will be using `mysql workbench` to execute the sql commands


| Dealing with Databases                               |                                                        |
| ---------------------------------------------------- | ------------------------------------------------------ |
| 1. [[Custom SQL notes#Creating a database]]          | 2. [[Custom SQL notes#Dropping/deleting a database]]   |
| 3. [[Custom SQL notes#selecting a database]]         | 3. [[Custom SQL notes#Read only mode]]                 |
| Dealing with Tables and Colums                       |                                                        |
| 1. [[Custom SQL notes#creating tables]]              | 2. [[Custom SQL notes#selecting a table]]              |
| 3. [[Custom SQL notes#renaming a table and columns]] | 4. [[Custom SQL notes#modifying a column]]             |
| 5. [[Custom SQL notes#drop a column]]                | 6. [[Custom SQL notes#dropping a table]]               |
| Dealing with rows and Data                           |                                                        |
| 1. [[Custom SQL notes#insert rows/values]]           | 2. [[Custom SQL notes#selecting data (data query)]]    |
| 3. [[Custom SQL notes#updating and deleting data]]   | 4. [[Custom SQL notes#auto commit, commit & rollback]] |
| 5. [[Custom SQL notes#date, time, datetime]]         |                                                        |
| Dealing with constraints                             |                                                        |
| 1. [[Custom SQL notes#unique constraint]]            | 2. [[Custom SQL notes#not null constraint]]            |
| 3. [[Custom SQL notes#check constraint]]             | 4. [[Custom SQL notes#default constraint]]             |
| 5. [[Custom SQL notes#primary key constraint]]       | 6. [[Custom SQL notes#auto increment attribute]]       |
| 7. [[Custom SQL notes#foreign key constraint]]       |                                                        |
| Dealing with joints                                  |                                                        |
| [[Joints]]                                           |                                                        |
| 1. [[Custom SQL notes#functions]]                    | 2. [[Custom SQL notes#logical operators]]              |
| 3. [[Custom SQL notes#wild car characters % , _]]    | 4. [[Custom SQL notes#order by]]                       |
| 5. [[Custom SQL notes#Limit clause]]                 | 6. [[Custom SQL notes#Union]]                          |
| 7. [[Self Join]]                                     | 8. [[Custom SQL notes#Views]]]                         |
| 9. [[Custom SQL notes#Index]]                        | 10. [[Subquery]]                                       |
| 11. [[Custom SQL notes#Group By clause]]             | 12. [[Custom SQL notes#Rollup]]                        |
| 13. [[Custom SQL notes#On Delete clause]]            | 14. [[Stored procedures]]                              |
| 15. [[Triggers]]                                     |                                                        |




### Creating a database
```sql
CREATE DATABASE databaseName;
```

### Dropping/deleting a database
```sql
DROP DATABASE databaseName;
```

### selecting a database 
```sql
USE databaseName;
```

### Read only mode
```sql
ALTER DATABASE mydb READ ONLY = 1; --read only 
ALTER DATABASE mydb READ ONLY = 0; --undo read only
```

---

### creating tables
```sql
CREATE TABLE employees(
	employee_id INT,
	first_name VARCHAR(50),
    last_name VARCHAR(50),
    hourly_pay DECIMAL(5, 2),  --(no. of digit(5), decimal places(2))
    hire_date DATE,
    --email VARCHAR(15)
);
```

### selecting a table
```sql
SELECT * FROM tableName;
```

### renaming a table and columns
```sql
RENAME TABLE currentTableName TO newTableName;
```

```sql
ALTER TABLE employees
RENAME COLUMN currentColumnName TO newColumnName;
```

### modifying a column
```sql
ALTER TABLE employees
MODIFY COLUMN email VARCHAR(20);  --it was (15) and now its (20)

--modify the limit and position to come just after last_name
ALTER TABLE employees
MODIFY COLUMN email VARCHAR(50)
AFTER last_name

--adding a column
ALTER TABLE employees
ADD COLUMN columnName VARCHAR(25) AFTER hourly_pay;
```

### drop a column
```sql
ALTER TABLE employees
DROP COLUMN columnName;
```

### dropping a table
```sql
DROP TABLE tableName;
```

---

### insert rows/values
```sql
	--base on the employess table created above
INSERT INTO employees
VALUES (1, "john", "Doe", 25.50, "2026-05-06");

	--inserting many values at the same time
INSERT INTO employees
VALUES 	(1, "john", "Doe", 25.50, "2026-05-06"), 
		(2, "mercy", "kang", 35.50, "2026-05-06"), 
		(3, "Angel", "gong", 35.50, "2026-05-06"), 
		(4, "James", "Walt", 35.50, "2026-05-06");

--for specific fields
INSERT INTO employees (employee_id, first_name, last_name)
VALUES 	(5, "Jambo", "Karibu");
```


### selecting data (data query)

```sql
--selecting everything in the table
SELECT * FROM employees;

--specific selection
SELECT first_name, last_name
FROM employees;

SELECT * FROM employees
WHERE employee_id = 1;

SELECT * FROM employees 
WHERE hire_date IS NULL
```
SELECT * FROM employees;
### updating and deleting data

```sql
--updating a specific data
UPDATE employees
SET hourly_pay = 10.50,
	hire_date = "2023-01-07"
WHERE employee_id = 5;

--all the rows will be changed to one value
UPDATE employees
SET hourly_pay = 10.50;

--deleting data
DELETE FROM employees
WHERE employee_id = 1;

```



### auto commit, commit & rollback
`auto commit` - Every transaction(executed query) is saved
`commit` - To create a safe point where you can go back to (undo) 
`rollback` - To go back to the previous safe point/commit

```sql
--to prevent commiting everything
SET AUTOCOMMIT = OFF

--create a safe point where you can go back to
COMMIT;

--if delete everything by mistakes e.g
DELETE FROM employees;

--to go back to when you commit or undo
ROLLBACK;
```

### date, time, datetime

```sql
CREATE TABLE test(
	my_date DATE,
	my_time TIME,
	my_datetime DATETIME
);

INSERT INTO test
VALUES(CURRENT_DATE(), CURRENT_TIME(), NOW());

```

### unique constraint
It makes sure that there's no identical data in a column e.g. no identical names

```sql
CREATE TABLE products(
	product_id INT,
	product_name VARCHAR(25) UNIQUE,
	price DECIMAL(4, 2)
);

--incase the table is already created without unique constraint
ALTER TABLE products
ADD CONSTRAINT
UNIQUE(product_name);
```

### not null constraint
It makes sure that there is no null value in the column
```sql
CREATE TABLE products(
	product_id INT,
	product_name VARCHAR(25),
	price DECIMAL(4, 2) NOT NULL
);

--incase the table is already created without not null constraint
ALTER TABLE products
MODIFY price DECIMAL(4, 2) NOT NULL;
```

### check constraint
It limits what values are placed in a column
```sql
CREATE TABLE employees(
	employee_id INT,
	first_name VARCHAR(50),
    last_name VARCHAR(50),
    hourly_pay DECIMAL(5, 2),
    hire_date DATE,
    CONSTRAINT chk_hourly_pay CHECK (hourly_pay >= 10.00) --10.00 will be the minimum value. chk_hourly_pay is a name we given the check constraint so that we may be able to drop it later if we want
    
);

--incase the table is already created without check constraint
ALTER TABLE employees
ADD CONSTRAINT chk_hourly_pay CHECK(hourly_pay >= 10.00)

ALTER TABLE employees
DROP CHECK chk_hourly_pay;
```

### default constraint
It add a value by default if not is set/entered 
```sql
CREATE TABLE products(
	product_id INT,
	product_name VARCHAR(25),
	price DECIMAL(4, 2) DEFAULT 0.00
);

--incase the table is already created without default constraint
ALTER TABLE products
ALTER price SET DEFAULT 0;
```

### primary key constraint

Is a unique key that does not accept duplicates or null values and can only be declared once per table

```sql
CREATE TABLE transactions(
	transaction_id INT PRIMARY KEY,
	amount DECIMAL(5, 2)
);

--incase the table is already created without primary key constraint
ALTER TABLE transactions
ADD CONSTRAINT
PRIMARY KEY(transaction_id);
```

### auto increment attribute
Mostly used with primary keys to auto generate them
```sql
CREATE TABLE transactions(
	transaction_id INT PRIMARY KEY AUTO_INCREMENT,
	amount DECIMAL(5, 2)
);

--set auto increment to begin at a certain value (1000)
ALTER TABLE transactions
AUTO_INCREMENT = 1000
```

### foreign key constraint
Simply, its a primary key that is on one table which can be found on another table. It creates a link between two tables
```sql
CREATE TABLE customers(
	customer_id INT PRIMARY KEY AUTO_INCREMENT,
	first_name VARCHAR(50),
	last_name VARCHAR(50)
);

CREATE TABLE transactions(
	transaction_id INT PRIMARY KEY AUTO_INCREMENT,
	amount DECIMAL(5, 2),
	customer_id INT,
	FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);

--to drop a foreign key. 
ALTER TABLE transactions
DROP FOREIGN KEY transactions_ibfk_1

--transactions_ibfk_1 this is found in the menu section under foregn keys

--to add a foreign key and also give it a unique name(fk_customer_id)
ALTER TABLE transactions
ADD CONSTRAINT fk_customer_id
FOREIGN KEY(customer_id) REFERENCES customer(customer_id)

```

### joints
Is a clause that is used to combine rows from two or more tables based on related column between them such as `foreign key`
To learn More [[Joints]]

### functions

```sql
--to returns the numer of rows in that column
SELECT COUNT(columnName)
FROM tableName;

--to return the maximum value
SELECT MAX(columnName) AS maximum
FROM tableName;

--to return the minimum
SELECT MIN(columnName)
FROM tableName;

AVG(columnName) -- for average
SUM(columnName) --for addition

--to concatenate values together
SELECT CONCAT(first_name, " ", last_name) AS full_name
FROM employees;
```

### logical operators

```sql
--AND
SELECT * FROM employees
WHERE hire_date < "2023-01-5" AND job = "cook";
--OR
SELECT * FROM employees
WHERE job = "cook" OR job = "cashier";
--NOT
SELECT * FROM employees
WHERE NOT job = "manager" AND NOT job = "asst. manager";
--BETWEEN
SELECT * FROM employees
WHERE hire_date BETWEEN "2023-01-04" AND "2023-01-07";
--IN
SELECT * FROM employees
WHERE job IN ("cook", "cashier", "janitor");
```

### wild car characters % , _
Used to substitute one or more characters in a string
`%` - substitute a string
`_` - substitute a single character
```sql
--where first name starts with "s"
SELECT * FROM employees
WHERE first_name LIKE "s%"

--wher job is "cook"
SELECT * FROM employees
WHERE job LIKE "_ook";

SELECT * FROM employees
WHERE hire_date LIKE "____-__-03";
```

### order by
```sql
SELECT * FROM employees
ORDER BY last_name --DESC--;

--if some have the same last name you can add another order by
SELECT * FROM employees
ORDER BY last_name, customer_id;
```

### Limit clause
- Limit clause is used to limit the number of records.
- useful if you're working with a lot of data.
- can be used to display a large data on pages(pagination).
```sql
--returns a limited result
SELECT * FROM employees
LIMIT 5;

--to return last data only base on last name
SELECT * FROM customers
ORDER BY last_name DESC LIMIT 1;

SELECT * FROM customers
LIMIT 10, 10; --offset
```

### Union 
Combines the results of two or more `SELECT` statements
They should have the same number of columns.
```sql
SELECT * FROM employees;
UNION --this won't work if they have diff no. of columns
SELECT * FROM customers;

SELECT first_name, last_name FROM employees;
UNION ALL --(ALL)to allow duplicates found in both columns
SELECT first_name, last_name FROM customers;
```

### Views
A virtual table based on the result-set of an SQL statement. The fields in a view are fields from one or more real tables in the database.
They are not real tables, but can be interacted with as if they were and any changes to the real table will automatically reflect on the view
```sql
--to a view of first_name and last_name
CREATE VIEW employee_attendance AS 
SELECT first_name, last_name
FROM employees;

SELECT * FROM employee_attendance;

--to drop the view
DROP VIEW employee_attendance;

```

### Index
Are used to find values within a specific column more quickly. MySQL normally searches sequentially through a column so the longer the column, the more expensive the operation is. However,
UPDATE takes more time, SELECT takes less time
```sql
--to show the indexes available in a table
SHOW INDEXES FROM customers;

--to create an index
CREATE INDEX last_name_idx
ON customers(last_name);

SELECT * FROM customers
WHERE last_name = "Puff"; --this will be much faster now

--to drop an index
ALTER TABLE customers
DROP INDEX last_name_idx;
```


### Group By clause
It aggregates all rows by a specific column often used with aggregate functions ex. `SUM(), MAX(), MIN(), AVG(), COUNT()`
```sql
--find total amount of each day
SELECT SUM(amount), order_date
FROM transactions
GROUP BY order_date

--count the no. of transactions made each day
SELECT COUNT(amount), order_date
FROM transactions
GROUP BY order_date

--counts the amount of transactions each customer made
SELECT COUNT(amount), customer_id)
FROM transactions 
GROUP BY customer_id
HAVING COUNT(amount) > 1; --WHERE cannot be use with GROUP BY
```

### Rollup
It is an extension of the GROUP BY clause. Produces another row and shows the grand total (super-aggregate value)
```sql
--it shows the grand total of the sum amount
SELECT SUM(amount), order_date
FROM transactions
GROUP BY order_date WITH ROLLUP;
```

### On Delete clause
`ON DELETE SET NULL` - When a FK is deleted, replace FK with Null
`ON DELETE CASCADE`- When a FK is deleted, delete row

```sql
SET foreign_key_checks = 0; --to allow deletion of FK

DELETE FROM customers
WHERE customer_id = 4;

ALTER TABLE transactions
ADD CONSTRAINT fk_customer_id
FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
ON DELETE SET NULL;

ALTER TABLE transactions
ADD CONSTRAINT fk_transactions_id
FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
ON DELETE CASCADE;

```


[[Custom SQL notes#Creating a database]]