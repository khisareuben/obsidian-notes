
## 🗄️ Dealing with Databases

- **Creating a database** **Q:** How do you create a database called `school`? **A:**
    
    
    
    ```sql
    CREATE DATABASE school;
    ```
    
- **Dropping a database** **Q:** How do you delete the database `school`? **A:**
    
    sql
    
    ```sql
    DROP DATABASE school;
    ```
    

## 📑 Dealing with Tables and Columns

- **Creating tables** **Q:** Create a table `students` with `id`, `name`, and `age`. **A:**
    
    sql
    
    ```sql
    CREATE TABLE students(
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INT
    );
    ```
    
- **Renaming a table** **Q:** Rename table `students` to `learners`. **A:**
    
    sql
    
    ```sql
    ALTER TABLE students RENAME TO learners;
    ```
    
- **Renaming a column** **Q:** Rename column `name` to `full_name`. **A:**
    
    sql
    
    ```sql
    ALTER TABLE learners RENAME COLUMN name TO full_name;
    ```
    
- **Altering a column** **Q:** Change column `age` to `SMALLINT`. **A:**
    
    sql
    
    ```sql
    ALTER TABLE learners ALTER COLUMN age TYPE SMALLINT;
    ```
    
- **Dropping a column** **Q:** Remove column `age`. **A:**
    
    sql
    
    ```sql
    ALTER TABLE learners DROP COLUMN age;
    ```
    
- **Dropping a table** **Q:** Delete table `learners`. **A:**
    
    sql
    
    ```sql
    DROP TABLE learners;
    ```
    

## 📊 Dealing with Rows and Data

- **Inserting rows**
    
    sql
    
    ```sql
    INSERT INTO learners(full_name, age) VALUES ('Reuben Khisa', 25);
    ```
    
- **Updating rows**
    
    sql
    
    ```sql
    UPDATE learners SET age = 26 WHERE full_name = 'Reuben Khisa';
    ```
    
- **Deleting rows**
    
    sql
    
    ```sql
    DELETE FROM learners WHERE full_name = 'Reuben Khisa';
    ```
    
- **Selecting data**
    
    sql
    
    ```sql
    SELECT * FROM learners;
    ```
    
- **WHERE clause**
    
    sql
    
    ```sql
    SELECT * FROM learners WHERE age > 20;
    ```
    
- **String functions**
    
    sql
    
    ```sql
    SELECT UPPER(full_name) FROM learners;
    ```
    
- **Joining columns**
    
    sql
    
    ```sql
    SELECT full_name || ' is ' || age || ' years old' FROM learners;
    ```
    

## 🔒 Constraints and Others

- **Primary key**
    
    sql
    
    ```sql
    CREATE TABLE teachers(
        id SERIAL PRIMARY KEY,
        name VARCHAR(50)
    );
    ```
    
- **Foreign key**
    
    sql
    
    ```sql
    CREATE TABLE classes(
        id SERIAL PRIMARY KEY,
        teacher_id INT REFERENCES teachers(id)
    );
    ```
    
- **Not null**
    
    sql
    
    ```sql
    ALTER TABLE learners ALTER COLUMN full_name SET NOT NULL;
    ```
    
- **Unique**
    
    sql
    
    ```sql
    ALTER TABLE learners 
    ADD CONSTRAINT unique_name UNIQUE(full_name);
    ```
    
- **Default**
    
    sql
    
    ```sql
    ALTER TABLE learners ALTER COLUMN age SET DEFAULT 18;
    ```
    
- **Check**
    
    sql
    
    ```sql
    ALTER TABLE learners ADD CONSTRAINT age_check CHECK (age > 0);
    ```
    

## 🔗 Joins and Aggregates

- **Joins**
    
    sql
    
    ```sql
    SELECT learners.full_name, classes.id
    FROM learners
    JOIN classes ON learners.id = classes.teacher_id;
    ```
    
- **Grouping**
    
    sql
    
    ```sql
    SELECT age, COUNT(*) FROM learners GROUP BY age;
    ```
    
- **HAVING**
    
    sql
    
    ```sql
    SELECT age, COUNT(*) FROM learners GROUP BY age HAVING COUNT(*) > 1;
    ```
    
- **Order**
    
    sql
    
    ```sql
    SELECT * FROM learners ORDER BY age DESC;
    ```
    
- **Limit/Offset**
    
    sql
    
    ```sql
    SELECT * FROM learners LIMIT 5 OFFSET 10;
    ```
    
- **Union**
    
    sql
    
    ```sql
    SELECT full_name FROM learners
    UNION
    SELECT name FROM teachers;
    ```
    
- **Subqueries**
    
    sql
    
    ```sql
    SELECT * FROM learners WHERE age > (SELECT AVG(age) FROM learners);
    ```
    
- **Distinct**
    
    sql
    
    ```sql
    SELECT DISTINCT age FROM learners;
    ```
    
- **Greatest/Least**
    
    sql
    
    ```sql
    SELECT GREATEST(10, 20, 5), LEAST(10, 20, 5);
    ```
    
- **CASE clause**
    
    sql
    
    ```sql
    SELECT full_name,
           CASE WHEN age < 18 THEN 'Minor'
                ELSE 'Adult'
           END AS category
    FROM learners;
    ```
    

👉 This gives you a **full practice Q&A set** across all the topics you listed, with self-contained examples (no external datasets).