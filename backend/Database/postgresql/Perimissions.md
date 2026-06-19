
## 🔹 Granting All Permissions

If you want `hrmoose` to have **full superuser‑like privileges**, connect as `postgres` and run:

```sql
ALTER ROLE hrmoose WITH SUPERUSER CREATEDB CREATEROLE REPLICATION;
```

If you only want `hrmoose` to control one database:

```sql
GRANT ALL PRIVILEGES ON DATABASE mydb TO hrmoose;
```

And for all tables inside that database:

```sql
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO hrmoose;
```

## 🔹 Quick Reference

|Task|Command|
|---|---|
|Create DB for user|`CREATE DATABASE hrmoose OWNER hrmoose;`|
|Connect to DB|`sudo -u hrmoose psql -d hrmoose`|
|Make superuser|`ALTER ROLE hrmoose WITH SUPERUSER;`|
|Grant DB privileges|`GRANT ALL PRIVILEGES ON DATABASE mydb TO hrmoose;`|
|Grant table privileges|`GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO hrmoose;`|


## 🔹 2. Export SQLite → Import into PostgreSQL

If you don’t want extra tools:

1. **Dump SQLite schema & data**:
    
    
    ```bash
    sqlite3 mydb.sqlite .dump > mydb.sql
    ```
    
2. **Edit the dump**:
    
    - SQLite and PostgreSQL syntax differ (e.g., `AUTOINCREMENT` vs `SERIAL`, type names).
        
    - You’ll need to adjust the SQL file manually.
        
3. **Load into PostgreSQL**:
    
        
    ```bash
    psql -U postgres -d mydb -f mydb.sql
    
    or
    sudo -u postgres psql -d jobs -f jobs.sql

    ```



## Steps to Delete a PostgreSQL Role

1. **Log in as the postgres superuser**
    
    
    
    ```bash
    sudo -u postgres psql
    ```
    
2. **Check existing roles**
    
    
    
    ```sql
    \du
    ```
    
    - This lists all accounts/roles.
        
    - Identify the one you want to remove (e.g., `hrmoose`).
        
3. **Drop the role**
    
    
    
    ```sql
    DROP ROLE hrmoose;
    ```
    
    - Replace `hrmoose` with the role name you want to delete.
        

## ⚠️ Important Notes

- If the role **owns databases or objects**, PostgreSQL will refuse to drop it.
    
- In that case, you must either:
    
    - **Reassign ownership**:
        
        
        
        ```sql
        REASSIGN OWNED BY hrmoose TO postgres;
        ```
        
    - **Drop owned objects**:
        
        
        
        ```sql
        DROP OWNED BY hrmoose;
        ```
        
- After that, you can safely run:
    
    
    
    ```sql
    DROP ROLE hrmoose;
    ```
    

## ✅ Key Takeaway

- Use `DROP ROLE` to delete the account.
    
- If it owns databases/tables, reassign or drop those first.
    
- The default `postgres` role will remain intact and is enough for administration.