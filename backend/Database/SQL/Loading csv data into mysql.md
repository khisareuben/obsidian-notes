The `LOAD DATA INFILE` statement is one of the fastest ways to import CSV data into MySQL. Here’s the clean, working structure you can use 👇

## 🔹 Basic Syntax



```sql
LOAD DATA INFILE '/path/to/your/file.csv'
INTO TABLE your_table_name
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

### 🧩 Explanation

|Clause|Purpose|
|---|---|
|`LOAD DATA INFILE`|Tells MySQL to read data from a file.|
|`'/path/to/your/file.csv'`|Full path to your CSV file (use forward slashes `/` on Windows too).|
|`INTO TABLE your_table_name`|The target table where data will be inserted.|
|`FIELDS TERMINATED BY ','`|Defines the column separator (comma for CSV).|
|`ENCLOSED BY '"'`|Handles quoted text values.|
|`LINES TERMINATED BY '\n'`|Marks the end of each row.|
|`IGNORE 1 ROWS`|Skips the header line in your CSV.|

## 🔹 Example


```sql
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/weather_data.csv'
INTO TABLE weather_obs
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

## ⚙️ Notes

- Ensure the file is **inside MySQL’s secure directory** (often `Uploads/` under the MySQL data folder).
    
- If you get a _“The MySQL server is running with the --secure-file-priv option”_ error, move your CSV file into that directory or disable the option in `my.ini`.
    
- You can also use `LOCAL` if the file is on your client machine:
    
    
    
    ```sql
    LOAD DATA LOCAL INFILE '/path/to/file.csv' INTO TABLE weather_obs ...
    ```


On Zorin OS (which is Linux‑based), the `LOAD DATA INFILE` command works the same way as on other systems — but you need to handle file permissions and MySQL’s secure‑file settings carefully.

Here’s how to do it step‑by‑step 👇

## 🧩 1. Check the secure‑file directory

Run this in your terminal:



```bash
mysql -u root -p -e "SHOW VARIABLES LIKE 'secure_file_priv';"
```

This shows the directory where MySQL allows file imports. If it returns something like `/var/lib/mysql-files/`, move your CSV file there:



```bash
sudo mv ~/Downloads/data.csv /var/lib/mysql-files/
```

## 🧩 2. Set file permissions

Make sure MySQL can read the file:



```bash
sudo chmod 644 /var/lib/mysql-files/data.csv
```

## 🧩 3. Run the import command

Inside the MySQL shell:



```sql
LOAD DATA INFILE '/var/lib/mysql-files/data.csv'
INTO TABLE your_table_name
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

## 🧩 4. If you prefer importing from your home folder

Use the `LOCAL` keyword:



```sql
LOAD DATA LOCAL INFILE '/home/harold/Documents/data.csv'
INTO TABLE your_table_name
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

Then start MySQL with:


```bash
mysql --local-infile=1 -u root -p
```

## ✅ Quick tips

- Always match your CSV column order to the table’s column order.
    
- If you get a “permission denied” error, check ownership and SELinux/AppArmor restrictions.
    
- You can specify columns explicitly:
    
    
    
    ```sql
    LOAD DATA INFILE '/var/lib/mysql-files/data.csv'
    INTO TABLE weather_obs
    FIELDS TERMINATED BY ',' 
    LINES TERMINATED BY '\n'
    (station_id, temperature, humidity, recorded_at);
    ```