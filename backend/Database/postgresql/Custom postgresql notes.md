
| Dealing with Databases                                        |                                                               |
| ------------------------------------------------------------- | ------------------------------------------------------------- |
| 1. [[Custom postgresql notes#Creating a database]]            | 2. [[Custom postgresql notes#Dropping/deleting a database]]   |
| Dealing with Tables and Colums                                |                                                               |
| 1. [[Custom postgresql notes#creating tables]]                | 2. [[Custom postgresql notes#renaming a table and columns]]   |
| 3. [[Custom postgresql notes#altering/modifying a column]]    | 4. [[Custom postgresql notes#dropping a column]]              |
| 5. [[Custom postgresql notes#dropping a table]]               |                                                               |
| Dealing with rows and Data                                    |                                                               |
| 1. [[Custom postgresql notes#Inserting rows/values]]          | 2. [[Custom postgresql notes#update rows/data]]               |
| 3. [[Custom postgresql notes#Deleting rows/data]]             | 4. [[Custom postgresql notes#Selecting data from the table]]] |
| 5. [[Custom postgresql notes#WHERE clause/filter]]            | 6. [[Custom postgresql notes#String Operators and functions]] |
| 7. [[Custom postgresql notes#Joining two columns]]            | 8. [[Custom postgresql notes#upper & lower case]]             |
| Dealing with constraints and others                           |                                                               |
| 1. [[Custom postgresql notes#auto commit, commit & rollback]] | 2. [[Custom postgresql notes#date, time, datetime]]           |
| 3. [[Custom postgresql notes#wild car characters % , _]]      | 4. [[Custom postgresql notes#primary key and foreign key]]    |
| 5. [[Custom postgresql notes#deleting foreign keys]]          | 6. [[Custom postgresql notes#not null constraint]]            |
| 7. [[Custom postgresql notes#default constraint]]             | 8. [[Custom postgresql notes#unique constraint]]              |
| 9. [[Custom postgresql notes#constraint removal]]             | 10. [[Custom postgresql notes#check validation]]              |
| Dealing with joints and others                                |                                                               |
| [[Joints]]                                                    | 1. [[Custom postgresql notes#Joins]]                          |
| 2. [[Custom postgresql notes#Grouping and Aggregates]]        | 3. [[Custom postgresql notes#HAVING clause/filter]]           |
| 4. [[Custom postgresql notes#Order/sorting]]                  | 5. [[Custom postgresql notes#offset and limit]]               |
| 6. [[Custom postgresql notes#Union clause]]                   | 7. [[Custom postgresql notes#Subqueries]]                     |
| 8. [[Custom postgresql notes#Distinct]]                       | 9. [[Custom postgresql notes#Greatest and least function]]    |
| 10. [[Custom postgresql notes#case clause]]                   |                                                               |
|                                                               |                                                               |

#### Creating a database
```sql
CREATE DATABASE databaseName;
```

#### Dropping/deleting a database
```sql
DROP DATABASE databaseName;
or
DROP DATABASE databaseName with (FORCE);
```

### Read only mode
```sql
-- For current session only
SET default_transaction_read_only = on;

--For entire database - needs superuser
ALTER DATABASE dbname SET default_transaction_read_only = on;
```

---

#### creating tables
We will be creating a table called `cities`

```sql
CREATE TABLE cities (
	name VARCHAR(50),
	country VARCHAR(50),
	population INTEGER,
	area INTEGER
);
```

### renaming a table and columns
```sql
ALTER TABLE old_table_name
RENAME TO new_table_name;
```

```sql
ALTER TABLE tableName
RENAME COLUMN currentColumnName TO newColumnName;
```


#### altering/modifying a column

```sql
ALTER TABLE cities
ALTER COLUMN population
SET NOT NULL

--for altering datatype of a column
ALTER TABLE tableName
ALTER COLUMN columnName TYPE VARCHAR(45)
```

#### dropping a column
```sql
ALTER TABLE cities
DROP COLUMN population
```

#### dropping a table
```sql
DROP TABLE tableName;
```


---
#### Inserting rows/values

```sql
INSERT INTO cities (name, country, population, area)
VALUES ('Tokyo', 'Japan', 385050000, 8223),
		('Delhi', 'India', 28125000, 2240),
		('Shanghai', 'China', 22125000, 4015),
		('Sao Paulo', 'Brazil', 20935000, 3043);
```

#### update rows/data
```sql
UPDATE cities SET population = 39505000 WHERE name = 'Tokyo';
```

#### Deleting rows/data
```sql
DELETE FROM cities WHERE name = 'Tokyo';
```

#### Selecting data from the table

```sql
-- selecting everything
SELECT * FROM cities;

--selecting something specific
SELECT name, country FROM cities;

--doing a calculation
SELECT name, population / area FROM cities;
SELECT name, population / area AS population_density
FROM cities; 
```

#### WHERE clause/filter
```sql
SELECT name, area FROM cities WHERE area > 4000;

SELECT name, area FROM cities WHERE area = 8223;

SELECT name, area FROM cities WHERE area <> 8223;

SELECT name, area FROM cities WHERE area BETWEEN 2000 AND 4000;

SELECT name, area FROM cities WHERE name IN ('Delhi', 'Shanghai');

SELECT name, area FROM cities WHERE name NOT IN ('Delhi', 'Shanghai');

SELECT name, area FROM cities WHERE area NOT IN (3043, 8223);

SELECT name, area FROM cities WHERE area NOT IN (3043, 8223) AND name = 'Delhi';

SELECT name, area FROM cities WHERE area NOT IN (3043, 8223) OR name = 'Delhi';



```

---
## String Operators and functions

- || - joining two strings
- CONCAT() - joining two strings
- UPPER(), LOWER()
- LENGTH() - gives the number of characters in a string
#### Joining two columns
```sql
-- ||, CONCAT() is a for joining two strings
SELECT name || ', ' || country AS location FROM cities;
--or
SELECT CONCAT(name, ', ', country) AS location FROM cities;


--result Tokyo, Japan... under location column
```

#### upper & lower case

```sql
SELECT
	CONCAT(UPPER(name), ', ', UPPER(country)) AS LOCATION
FROM
	CITIES;
	
--or

SELECT UPPER(CONCAT(name, ', ', country)) AS location FROM cities;

```

---

#### auto commit, commit & rollback
`auto commit` - Every transaction(executed query) is saved by default
`commit` - To create a safe point where you can go back to (undo) 
`rollback` - To go back to the previous safe point/commit

```sql
--to prevent commiting everything automatically set off auto commit
BEGIN;

 --the query should be here between begin and commit
 --if delete everything by mistakes e.g
DELETE FROM employees;

--to go back to what it was before BEGIN
ROLLBACK;
 
--Both updates are now permanet. can't undo
COMMIT;


```

#### date, time, datetime

```sql
CREATE TABLE test(
	my_date DATE,
	my_time TIME,
	my_datetime TIMESTAMP
);

INSERT INTO test
VALUES(CURRENT_DATE, CURRENT_TIME, NOW());

--another example
SELECT EXTRACT(YEAR FROM NOW());
SELECT EXTRACT(MONTH FROM NOW());
SELECT EXTRACT(DOW FROM NOW());
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

--for case-insensitive searches use ILIKE instead of LIKE 

```



#### primary key and foreign key

- A **primary key** Is a unique key that does not accept duplicates or null values and can only be declared once per table
- A **foreign key** is a column in one table that **references the primary key** of another table. It creates a **relationship** between the two tables.
- A **serial** is command that auto generates the primary key

NOTE: We are going to create two tables `users` `photos` where by **photos** will contain the **foreign key** which is the **primary key** of **users**

```sql
CREATE TABLE users(
	id SERIAL PRIMARY KEY,
	username VARCHAR(50)
);

INSERT INTO users (username)
VALUES ('monahan93'),
		('pferrer'),
		('si93onis'),
		('99stroman');
```

```sql
CREATE TABLE photos (
	id SERIAL PRIMARY KEY,
	url VARCHAR(200),
	user_id INTEGER REFERENCES users(id)
);

INSERT INTO photos (url, user_id)
VALUES 
	('https://img2.jpg', 1),
	('https://img3.jpg', 1),
	('https://img4.jpg', 2),
	('https://img5.jpg', 3),
	('https://img5.jpg', 4);

```

#### deleting foreign keys
Lets say we want to delete a raw in the **users** table when is being referenced in the **photos** table.

- `ON DELETE RESTRICT` - Throw an error
- `ON DELETE NO ACTION` - Throw an error
- `ON DELETE CASCADE` - Delete the photo too!
- `ON DELETE SET NULL` - Set the 'user_id' of the photo to 'NULL'
- `ON DELETE SET DEFAULT` - Set the 'user_id' of the photo to a default value, if one is provided

```sql
CREATE TABLE photos (
	id SERIAL PRIMARY KEY,
	url VARCHAR(200),
	user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
```

---

#### not null constraint
- It makes sure that there is no null value in the column
- It won't work where the column already has null values, so you'll need to update or remove the null values

```sql
--updates all the null values in the price column
UPDATE products
SET price = 999
WHERE price IS NULL;

--incase the table is already created without default constraint
ALTER TABLE products
ALTER COLUMN price
SET NOT NULL;

--
CREATE TABLE products (
	id SERIAL PRIMARY KEY,
	name VARCHAR(50),
	department VARCHAR(50),
	price INTEGER NOT NULL,
	weight INTEGER
);
```

#### default constraint
It add a value by default if not is set/entered 
```sql
CREATE TABLE products (
	id SERIAL PRIMARY KEY,
	name VARCHAR(50),
	department VARCHAR(50),
	price INTEGER DEFAULT 999,
	weight INTEGER
);

--incase the table is already created without default constraint
ALTER TABLE products
ALTER COLUMN price 
SET DEFAULT 999;
```

### unique constraint
It makes sure that there's no identical data in a column e.g. no identical names

```sql
CREATE TABLE products (
	id SERIAL PRIMARY KEY,
	name VARCHAR(50) UNIQUE,
	department VARCHAR(50),
	price INTEGER,
	weight INTEGER
);

--incase the table is already created without unique constraint
ALTER TABLE products
ADD UNIQUE(name, department);
```

#### constraint removal
- You can find the name of the constraint in the columns menu section 
```sql
ALTER TABLE products
DROP CONSTRAINT nameOFtheCOnstraint;
```

#### check validation
138
- It checks if a certain condition is true in order for a new row to be added
- A check can only work on the row we are adding/updating

```sql
-- this makes sure that price is always a positive number
CREATE TABLE products (
	id SERIAL PRIMARY KEY,
	name VARCHAR(50),
	department VARCHAR(50),
	price INTEGER CHECK (price > 0),
	weight INTEGER
);

--incase the table is already created without check validation
ATER TABLE products
ADD CHECK (price > 0);

```

---
#### Joins 

- **Joins** - Produces values by merging together rows from different related tables. Use a join most times that you're asked to find data that involves multiple resources. This is same as `INNER JOIN`
- **Aggregation** - Looks at many rows and calculates a single value. Words like `most` `average` `least` are a sign that you need to use an aggregation
 
We will work with three tables to show this `photos users comments`

comments

| id  | contents                     | user_id | photo_id |
| --- | ---------------------------- | ------- | -------- |
| 1   | The man was full of fire     | 3       | 4        |
| 2   | Jesus paid it all            | 4       | 5        |
| 3   | All to Him i owe             | 2       | 3        |
| 4   | Sin had left a crimson stain | 1       | 3        |
| 5   | He washed it white as snow   | 1       | 3        |


users                                                           photos

| id  | username            |     | id  | url          | user_id |
| --- | ------------------- | --- | --- | ------------ | ------- |
| 1   | Reyna.Marvin        |     | 1   | https://img1 | 2       |
| 2   | Micah.Cremin        |     | 2   | https://img2 | 3       |
| 3   | Alfredo77           |     | 3   | https://img3 | 1       |
| 4   | Gerald_Mitchell42   |     |     |              |         |
| 5   | Frederique_Donnelly |     |     |              |         |

**INNER JOIN**
```sql
SELECT contents, username
FROM comments
JOIN users ON users.id = comments.user_id;

SELECT contents, url
FROM comments
JOIN photos ON photos.id = comments.photo_id;


--more complex three way join(joining three tables)
SELECT url, contents, username
FROM comments
JOIN photos ON photos.id = comments.photo_id
JOIN users ON users.id = comments.user_id AND users.id = photos.user_id;
```

**LEFT AND RIGHT JOIN**
```sql
SELECT url, username
FROM photos
LEFT JOIN users ON users.id = photos.user_id;

SELECT url, username
FROM photos
RIGHT JOIN users ON users.id = photos.user_id;
```

FULL JOIN
```sql
SELECT url, username
FROM photos
FULL JOIN users ON users.id = photos.user_id;
```

This will show a list of contents and username where the `user.id` is found in `comments.user_id`

[[Joints]]

---

#### Grouping and Aggregates
57
- **Grouping** - Reduces many rows down to fewer rows. Done by using the `GROUP BY` keyword. It groups by a unique data(repeated/similar data will fall under one group)
- **Aggregates** - Reduces many values down to one. Done by using `aggregate functions` 
	 `COUNT()` - Returns the number of values in a group of values. `NULL` values are not counted unless `COUNT(*)`
	 `SUM()` - Finds the sum of a group of numbers
	 `AVG()` - Finds the average of a group of numbers
	 `MIN()`  - Returns the minimum value from a group of numbers
	 `MAX()` - Returns the maximum value from a group of numbers

```sql
-- it groups by
SELECT user_id
FROM comments
GROUP BY user_id;
```

```sql
SELECT MAX(id)
FROM comments;

SELECT SUM(id)
FROM comments;

SELECT COUNT(id)
FROM comments;

SELECT AVG(id)
FROM comments;
```

```sql
SELECT user_id, COUNT(id) AS num_comments_created
FROM comments
GROUP BY user_id;

SELECT photo_id, COUNT(*)
FROM comments
GROUP BY photo_id
```

NOTE: Group by and aggregate functions can be used together but you can't select another column when using `GROUP BY` only without group by
e.g `SELECT user_id, urls...` In short we can only select columns that have been used by **grouped by** or have **aggregate functions**


#### HAVING clause/filter
- Filters the set of groups
- Mostly used with `aggregate functions`
Example: Find the number of comments for each photo
where
the photo_id is less than 3
and
the photo has more than 2 comments

```sql
SELECT photo_id, COUNT(*)
FROM comments
WHERE photo_id < 3
GROUP BY photo_id
HAVING COUNT(*) > 2;
```

Another Example: Find the users(user_ids)
where
the user has commented on the first 2 photos
and
the user added more that 2 comments on those photos

```sql
SELECT user_id, COUNT(*)
FROM comments
WHERE photo_id < 50
GROUP BY user_id
HAVING COUNT(*) > 20
```


**NOTE:** #sequence Sql queries sequence `FROM JOIN WHERE GROUP BY HAVING LIMIT/OFFSET` 


#### Order/sorting
- `ASC` going up and `DESC` going down

```sql
SELECT *
FROM products
ORDER BY price ASC;

SELECT *
FROM products
ORDER BY price DESC;
```


#### offset and limit
- OFFSET - Skip the specified number of rows (n) of the results set
- LIMIT - Only give the specified number of rows

```sql
--skip 40 rows
SELECT *
FROM users
OFFSET 40;
```

```sql
-- limit 
SELECT *
FROM users
LIMIT 10
OFFSET 20;
```

#### Union clause

- Used to join two sql queries
- We are only allowed to use `UNION` between the results of two queries where the results have the same columns
- It does not include duplicates unless you specify `UNION ALL`
```sql
(
	SELECT * 
	FROM products
	ORDER BY price DESC
	LIMIT 4
)
UNION
(
	SELECT *
	FROM products
	ORDER BY price / weight DESC
	LIMIT 4
);

--or if its something small
SELECT * FROM products
UNION
SELECT * FROM products;
```

84

| `UNION`         | Join together the results of two queries and remove duplicate rows                    |
| --------------- | ------------------------------------------------------------------------------------- |
| `UNION ALL`     | Join together results of two queries                                                  |
| `INTERSECT`     | Find the rows common in the results of two queries. Remove duplicates                 |
| `INTERSECT ALL` | Find the rows common in the results of two queries                                    |
| `EXCEPT `       | Find the rows that are present in first query but not second query. Remove duplicates |
| `EXCEPT ALL`    | Find the rows that are present in first query but not second query<br>                |

```sql
(
	SELECT * 
	FROM products
	ORDER BY price DESC
	LIMIT 4
)
INTERSECT 
(
	SELECT *
	FROM products
	ORDER BY price / weight DESC
	LIMIT 4
);
```

```sql
(
	SELECT * 
	FROM products
	ORDER BY price DESC
	LIMIT 4
)
EXCEPT
(
	SELECT *
	FROM products
	ORDER BY price / weight DESC
	LIMIT 4
);
```

89

--- 
#### Subqueries

- When inserting sub-queries at the `SELECT STATEMENT POSITION` , that sub-query should result in a single value only.

```sql
SELECT name, price,subquery 
FROM products 
WHERE price > 876;

-- subquery at the select statement position - Any subquery that results in a single value

SELECT name, price, (SELECT MAX(price) FROM products)
FROM products
WHERE price > 876

SELECT name, price, (
SELECT price FROM products WHERE id = 3
)
FROM products
WHERE price > 867;
``` 

- When inserting sub-queries at the `FROM STATEMENT POSITION` , you can insert any sub query, so long as the outer **selects/wheres/etc** are compatible.
- We must apply an alias to the result of the sub query

```sql
--this is just an example not a real scenario
SELECT name, price_weight_ratio
FROM (
SELECT name, price / weight AS price_weight_ratio
FROM products
) AS p
WHERE price_weight_ratio > 5;

--or
SELECT *
FROM (SELECT MAX(price) FROM products) AS p;
```

- When inserting sub-queries at the `JOIN STATEMENT POSITION` , you can insert any sub query that returns data compatible with the `ON` clause

```sql
--the example is not useful and just for learning
SELECT first_name
FROM users
JOIN (
	SELECT user_id FROM orders WHERE product_id = 3
) AS o
ON o.user_id = users.id;

```

- When inserting sub-queries at the `WHERE STATEMENT POSITION` , this is the most commonly used 

```sql
SELECT id 
FROM orders
WHERE product_id IN (
	SELECT id FROM products WHERE price / weight > 50
);
```


#### Distinct

- Is always placed inside of the `SELECT` keyword
- Is going to give you all the list of all the different **distinct** values in a column
- Kinda same as `GROUP BY`

```sql
SELECT DISTINCT department
FROM products;

SELECT COUNT(DISTINCT department)
FROM products;
```

#### Greatest  and least function
- GREATEST Is a function in postgresql that return the greatest value in a list
- LEAST is the opposite of greatest

```sql
SELECT GREATEST(200, 10, 30);

SELECT LEAST(100, 20, 50 90);
```

#### case clause
- Is used in printing out a string 
- Not commonly used
```sql
SELECT name, price
CASE
	WHEN price > 600 THEN 'high'
	WHEN price > 300 THEN 'medium'
	ELSE 'cheap'
END
FROM products;
```

128 - 129 **Data types**

---

Go to the fist page: [[Custom postgresql notes#Creating a database]]
