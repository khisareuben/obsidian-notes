
### Integer types

- **SMALLINT** -  -32768 to 32767
- **INT or INTEGER** - -2 billion to 2billion
- **BIGINT** - huge numbers

### Decimal / Floating point types

- **NUMERIC(p, s)** - exact decimal numbers(like money)
- **REAL/ DOUBLE PRECISION** - approximate numbers

### Character / String types

- **VARCHAR(n)** - variable-length text, max n characters
- **CHAR(n)** - fixed-length text
- **TEXT** - unlimited length text

### Date & Time types 

- **DATE** - stores date only (accepts and converts any format you can imagine)
- **TIME** - stores time only (same)
- **TIMESTAMP** - stores date + time

### Boolean types

- **BOOLEAN** - stores TRUE or FALSE

### JSON / JSONB

- Stores unstructured data (like NoSQL)



1. **Terminate active connections** From the `postgres` database (not `shopdb`), run:
    
    
    
    ```sql
    SELECT pg_terminate_backend(pid)
    FROM pg_stat_activity
    WHERE datname = 'shopdb';
    ```
    
    - This force‑kills all sessions using `shopdb`.
        
2. **Drop the database**
    
    
    
    ```sql
    DROP DATABASE shopdb;
    ```