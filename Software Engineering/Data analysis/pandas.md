# Analyzing tabular data using pandas

reading files
```python
import pandas as pd

name = pd.read_csv("path of csv")

```

```python
type(name) # to check the type of file 

name.info() # to get the info in the csv file

name.describe() # to get the statistical data like mean, std, min and max

name.columns # to get the list of columns

name.shape # to get the number of raws and columns

```

#### How to retrieve data in a file

```python
name['name of column'] or
name.name_of_column

name['name of column'][245] # retrieve data from a specific line/row

name.at[245, 'name of column'] # same as the one above

name2 = name.copy() # to create a separate copy of the data

name.loc[245] # to access a specific row

name.head(5) #to get the first 5 rows
name.tail(5) #to get the last 5 rows

name.name_of_column.first_valid_index() #it check where the first input of that column begins, coz there are some columns which begin with NaN/none

name.sample(10) # to retrieve random samples of rows
```