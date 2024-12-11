
# mysql

change this in the `settings.py` file

```python
DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.mysql',

        'NAME': 'elderco', # database name

        'USER': 'root',

        'PASSWORD': 'your password',

        'HOST': 'localhost',

        'PORT': '3306',

    }

}
```

#### create a mydb.py file in the root folder

```python
# pip install mysql

# pip install mysql-connector

# pip install mysql-connector-python

  

import mysql.connector

  

dataBase = mysql.connector.connect(

  host = 'localhost',

  user = 'root',

  passwd = 'your password'

  

  )

  

# prepare a cursor object

cursorObject = dataBase.cursor()

  

# Create a database

cursorObject.execute("CREATE DATABASE elderco")

  

print("All Done!")
```


# PostgreSQL

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'elderco',
        'USER': 'root',
        'PASSWORD': 'your password',
        'HOST': 'localhost',
        'PORT': '5432',  # Default PostgreSQL port
    }
}

```

pip install psycopg2-binary

```python
import psycopg2
from psycopg2 import sql

# Connect to PostgreSQL
connection = psycopg2.connect(
    host="localhost",
    user="root",
    password="your password",
    port="5432"
)

# Create a cursor object
cursor = connection.cursor()

# Create a database
cursor.execute(sql.SQL("CREATE DATABASE elderco"))

# Commit and close connection
connection.commit()
cursor.close()
connection.close()

print("All Done!")


```

