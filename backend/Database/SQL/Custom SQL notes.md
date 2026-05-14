
We will be using `mysql workbench` to execute the sql commands


| 1. [[Custom SQL notes#Creating a database]]          | 2. [[Custom SQL notes#Dropping/deleting a database]] |
| ---------------------------------------------------- | ---------------------------------------------------- |
| 3. [[Custom SQL notes#selecting a database]]         | 3. [[Custom SQL notes#Read only mode]]               |
|                                                      |                                                      |
| 1. [[Custom SQL notes#creating tables]]              | 2. [[Custom SQL notes#selecting a table]]            |
| 3. [[Custom SQL notes#renaming a table and columns]] | 4. [[Custom SQL notes#modifying a column]]           |
| 5. [[Custom SQL notes#drop a column]]                | 6. [[Custom SQL notes#dropping a table]]             |
|                                                      |                                                      |
| 1. [[Custom SQL notes#insert rows/values]]           |                                                      |




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

--modify the limit and postion to come just after last_name
ALTER TABLE employees
MODIFY COLUMN email VARCHAR(50)
AFTER last_name
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
VALUE (1, "john", "Doe", 25.50, "2026-05-06");

	--inserting many values at the same time
INSERT INTO employees
VALUE 	(1, "john", "Doe", 25.50, "2026-05-06"), 
		(2, "mercy", "kang", 35.50, "2026-05-06"), 
		(3, "Angel", "gong", 35.50, "2026-05-06"), 
		(4, "James", "Walt", 35.50, "2026-05-06");

--for specific fields
INSERT INTO employees (employee_id, first_name, last_name)
VALUE 	(5, "Jambo", "Karibu");
```


