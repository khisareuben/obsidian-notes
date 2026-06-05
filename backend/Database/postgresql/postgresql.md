
## 🔹 Step 1: Install PostgreSQL



```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

- `postgresql` → main server package
    
- `postgresql-contrib` → extra utilities (like `pg_dump`, `pg_restore`)
    

## 🔹 Step 2: Service Management


```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo systemctl status postgresql
```

- **Start** → launches the service
- **Enable** → auto-start at boot
- **Status** → check if running

## 🔹 Step 3: Access PostgreSQL Shell

PostgreSQL creates a default `postgres` **user**. Switch to it:



```bash
sudo -u postgres psql
```

You’ll enter the interactive SQL shell (`psql`). Exit with:



```sql
\q
```

## 🔹 Step 4: Create Roles and Databases

PostgreSQL uses **roles** instead of “users.”

- Create a role:


```bash
sudo -u postgres createuser --interactive
```

Or inside `psql`:


```sql
#normal user
CREATE ROLE myuser WITH LOGIN PASSWORD 'mypassword';

#superuser
CREATE ROLE myuser WITH LOGIN SUPERUSER PASSWORD 'mypassword';

\du
```

- Create a database:


```bash
sudo -u postgres createdb mydb
```

Or inside `psql`:


```sql
CREATE DATABASE mydb OWNER myuser;
```

```sql
ALTER DATABASE mydb OWNER TO postgres;
```

## 🔹 Step 5: Connect to Database



```bash
psql -U myuser -d mydb

> sudo -u myuser psql -d mydb

```

- `-U` → username
    
- `-d` → database name
    

## 🔹 Step 6: Basic SQL Commands

Inside `psql`:


```sql
-- Create table
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    age INT
);

-- Insert data
INSERT INTO students (name, age) VALUES ('Alice', 20);

-- Query data
SELECT * FROM students;
```

## 🔹 Step 7: Configuration (Optional)

- Config files: `/etc/postgresql/<version>/main/`
    
- Enable remote connections: edit `postgresql.conf` →
    
    
    ```
    listen_addresses = '*'
    ```
    
- Update `pg_hba.conf` for authentication rules (e.g., `scram-sha-256`).
    

## 🔹 Step 8: Backup & Restore

- Logical backup:


```bash
pg_dump mydb > mydb.sql
```

- Restore:


```bash
psql mydb < mydb.sql
```

- Physical backups: use **WAL logs** for point-in-time recovery.


## ✅ Quick Reference Table

|Task|Command/SQL|
|---|---|
|Start service|`sudo systemctl start postgresql`|
|Enter shell|`sudo -u postgres psql`|
|Create role|`CREATE ROLE user WITH LOGIN PASSWORD 'pass';`|
|Create database|`CREATE DATABASE db OWNER user;`|
|Connect to database|`psql -U user -d db`|
|Backup database|`pg_dump db > db.sql`|
|Restore database|`psql db < db.sql`|
