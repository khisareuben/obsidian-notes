
```markdown
# MySQL Commands Cheat Sheet

## Connecting to MySQL Server
- Connect to MySQL server:
  ```sql
  mysql -u [username] -p
```

- Connect to a specific database:
    
    SQL
    
    ```sql
    mysql -u [username] -p [database]
    ```
    
    
- Exit MySQL client:
    
    SQL
    
    ```sql
    quit
    ```
    
    

## Database Operations

- Create a new database:
    
    SQL
    
    ```sql
    CREATE DATABASE [database_name];
    ```
    
    
- List all databases:
    
    SQL
    
    ```sql
    SHOW DATABASES;
    ```
    

To import my sql 
```
cd to the directory where the file is
sudo mysql < filename
```

- Select a database:
    
    SQL    
    
    ```sql
    USE [database_name];
    ```
    
    
- Drop a database:
    
    SQL
    
    ```sql
    DROP DATABASE [database_name];
    ```
    
    AI-generated code. Review and use carefully. .
    

## Table Operations

- Create a new table:
    
    SQL
	 datatype include int, varchar(255)

    ```sql
    CREATE TABLE [table_name] (
      column1 datatype auto_increment primary key,
      column2 datatype not null,
      ...
    );
    ```
    
    
- List all tables in a database:
    
    SQL
    
    ```sql
    SHOW TABLES;
    ```
    
    
- Describe a table’s structure:
    
    SQL
    
    ```sql
    DESCRIBE [table_name];
    ```
    
    
- Drop a table:
    
    SQL  To delete a table
    
    ```sql
    DROP TABLE [table_name];
    ```
    
    

## Data Manipulation

- Insert data into a table:
    
    SQL
    
    ```sql
    INSERT INTO [table_name] (column1, column2, ...)
    VALUES (value1, value2, ...);
    ```
    
    
- Update data in a table:
    
    SQL
    
    ```sql
    UPDATE [table_name]
    SET column1 = value1, column2 = value2, ...
    WHERE condition;
    ```
    
    AI-generated code. Review and use carefully. .
    
- Delete data from a table:
    
    SQL
    
    ```sql
    DELETE FROM [table_name]
    WHERE condition;
    ```
    
    AI-generated code. Review and use carefully. .
    

## Querying Data

- Select all data from a table:
    
    SQL
    
    ```sql
    SELECT * FROM [table_name];
    ```
    
    AI-generated code. Review and use carefully. .
    
- Select specific columns:
    
    SQL
    
    ```sql
    SELECT column1, column2, ...
    FROM [table_name];
    ```
    
    AI-generated code. Review and use carefully. .
    
- Select with conditions:
    
    SQL
    
    ```sql
    SELECT * FROM [table_name]
    WHERE condition;
    ```
    
    AI-generated code. Review and use carefully. .
    
- Sorting results:
    
    SQL
    
    ```sql
    SELECT * FROM [table_name]
    ORDER BY column1 [ASC|DESC];
    ```
    
    AI-generated code. Review and use carefully. .
    

## Aggregate Functions

- Count rows:
    
    SQL
    
    ```sql
    SELECT COUNT(*)
    FROM [table_name];
    ```
    
    AI-generated code. Review and use carefully. .
    
- Sum values:
    
    SQL
    
    ```sql
    SELECT SUM(column_name)
    FROM [table_name];
    ```
    
    AI-generated code. Review and use carefully. .
    
- Average values:
    
    SQL
    
    ```sql
    SELECT AVG(column_name)
    FROM [table_name];
    ```
    
    AI-generated code. Review and use carefully. .
    

## Joining Tables

- Inner join:
    
    SQL
    
    ```sql
    SELECT columns
    FROM table1
    INNER JOIN table2
    ON table1.column = table2.column;
    ```
    
    AI-generated code. Review and use carefully. .
    
- Left join:
    
    SQL
    
    ```sql
    SELECT columns
    FROM table1
    LEFT JOIN table2
    ON table1.column = table2.column;
    ```
    
    AI-generated code. Review and use carefully. .
    

## Backup and Restore

- Export a database:
    
    ```bash
    mysqldump -u [username] -p [database_name] > backup.sql
    ```
    
- Import a database:
    
    ```bash
    mysql -u [username] -p [database_name] < backup.sql
    ```
    

## Additional Commands

- Show current user:
    
    SQL
    
    ```sql
    SELECT USER();
    ```
    
    AI-generated code. Review and use carefully. .
    
- Show current database:
    
    SQL
    
    ```sql
    SELECT DATABASE();
    ```