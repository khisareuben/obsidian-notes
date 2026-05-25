
**20 exercises, each explained and solved**. We’ll use a simple but realistic dataset: a **Students & Courses database**. This schema will give you plenty of practice across queries, joins, aggregations, and advanced SQL features.

# 🗄️ SQL Comprehensive Workbook (with Explanations)

### Database Schema

We’ll assume you have these tables:

**Students**

- `student_id` (PK)
    
- `name`
    
- `age`
    
- `major`
    

**Courses**

- `course_id` (PK)
    
- `course_name`
    
- `credits`
    

**Enrollments**

- `enrollment_id` (PK)
    
- `student_id` (FK)
    
- `course_id` (FK)
    
- `grade`
    

### 1. **Create table**

**Entails:** Define schema.

sql

```
CREATE TABLE Students (
  student_id SERIAL PRIMARY KEY,
  name VARCHAR(50),
  age INT,
  major VARCHAR(50)
);
```

👉 Foundation: creating tables.

### 2. **Insert data**

**Entails:** Add records.

sql

```
INSERT INTO Students (name, age, major)
VALUES ('Alice', 20, 'Computer Science');
```

👉 Populate tables with sample data.

### 3. **Select basics**

**Entails:** Retrieve columns.

sql

```
SELECT name, age FROM Students;
```

👉 Basic data retrieval.

### 4. **Filtering**

**Entails:** Use `WHERE`.

sql

```
SELECT * FROM Students WHERE age > 21;
```

👉 Narrow down results.

### 5. **Sorting**

**Entails:** Order results.

sql

```
SELECT * FROM Students ORDER BY age DESC;
```

👉 Ranking data.

### 6. **Aggregate functions**

**Entails:** Summaries.

sql

```
SELECT AVG(age) AS avg_age FROM Students;
```

👉 Compute statistics.

### 7. **Group By**

**Entails:** Summarize by category.

sql

```
SELECT major, COUNT(*) AS num_students
FROM Students
GROUP BY major;
```

👉 Grouped summaries.

### 8. **Joins**

**Entails:** Combine tables.

sql

```
SELECT s.name, c.course_name
FROM Students s
JOIN Enrollments e ON s.student_id = e.student_id
JOIN Courses c ON e.course_id = c.course_id;
```

👉 Joins connect related data.

### 9. **Aliases**

**Entails:** Shorten names.

sql

```
SELECT s.name AS student, c.course_name AS course
FROM Students s
JOIN Courses c ON s.major = c.course_name;
```

👉 Aliases improve readability.

### 10. **Subqueries**

**Entails:** Query inside query.

sql

```
SELECT name
FROM Students
WHERE age > (SELECT AVG(age) FROM Students);
```

👉 Compare against aggregate.

### 11. **HAVING**

**Entails:** Filter groups.

sql

```
SELECT major, COUNT(*) AS num_students
FROM Students
GROUP BY major
HAVING COUNT(*) > 5;
```

👉 Restrict grouped results.

### 12. **UPDATE**

**Entails:** Modify records.

sql

```
UPDATE Students SET age = age + 1 WHERE name = 'Alice';
```

👉 Update values.

### 13. **DELETE**

**Entails:** Remove records.

sql

```
DELETE FROM Students WHERE age < 18;
```

👉 Clean up data.

### 14. **DISTINCT**

**Entails:** Unique values.

sql

```
SELECT DISTINCT major FROM Students;
```

👉 Avoid duplicates.

### 15. **LIMIT**

**Entails:** Restrict rows.

sql

```
SELECT * FROM Students LIMIT 5;
```

👉 Useful for previews.

### 16. **CASE**

**Entails:** Conditional logic.

sql

```
SELECT name,
CASE 
  WHEN grade >= 90 THEN 'A'
  WHEN grade >= 80 THEN 'B'
  ELSE 'C'
END AS grade_letter
FROM Enrollments;
```

👉 Add logic to queries.

### 17. **INNER vs LEFT JOIN**

**Entails:** Compare join types.

sql

```
-- Inner join
SELECT s.name, e.grade
FROM Students s
INNER JOIN Enrollments e ON s.student_id = e.student_id;

-- Left join
SELECT s.name, e.grade
FROM Students s
LEFT JOIN Enrollments e ON s.student_id = e.student_id;
```

👉 Understand join differences.

### 18. **Indexes**

**Entails:** Speed up queries.

sql

```
CREATE INDEX idx_major ON Students(major);
```

👉 Indexes improve performance.

### 19. **Views**

**Entails:** Save queries as virtual tables.

sql

```
CREATE VIEW CS_Students AS
SELECT * FROM Students WHERE major = 'Computer Science';
```

👉 Views simplify repeated queries.

### 20. **Stored procedures**

**Entails:** Encapsulate logic.

sql

```
CREATE PROCEDURE GetTopStudents()
LANGUAGE SQL
AS $$
  SELECT name, grade
  FROM Enrollments
  WHERE grade > 90;
$$;
```

👉 Procedures automate tasks.

✅ That’s **20 SQL exercises with explanations + solutions** — covering table creation, CRUD operations, filtering, grouping, joins, subqueries, indexes, views, and procedures