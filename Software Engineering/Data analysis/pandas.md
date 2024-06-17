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


#### Querying and sorting rows
```python
higher_name = name.column_name > 1000 # this returns the bool values of true and false in the list of those numbers that are greater than or less than 1000

name[high_name] # now this only returns the valuse with greater than 1000 of the column name provide above

higher_name = name[name.column_name > 1000] # this is same as the two above but its a short form and returns the values greater than 1000

# this is to display the exact number of rows you want
from IPython.display import display with pd.option_context('display.max_rows', 100):
	display(covid_df[covid_df.new_cases > 1000])

```

#### complex operations
```python
# addng a new column in the file
name['name_of_new_column'] = another / another

# how to remove a column
name.drop(columns=['column_name'], inplace=True)

# sorting
name.sort_values('column_name', ascending=False,).head(10)
#the .head() allows you to choose the number of rows you want to get

# saving data to a file
name.to_csv('file_name', index=None) # the index is to remove the index section as a column

name.merge(...) # to merge two columns or rows


```


#### Basic plotting with pandas
This is just creating basic graphs in pandas

```python
name.column_name.plot() # to plot a column
name.column_name.plot(title='title_name') # adding a title name for the graph
name.column_name.plot(kind='bar') # to specify the kind of graph you want to plot

# setting the date column as the index column
name.set_index('column_name', inplace=True)

```