# Analyzing tabular data using pandas

reading files
```python
import pandas as pd

name = pd.read_csv("path of csv")

```

```python
type(name) # to check the type of file 

name # to check the data in the file

name.info() # to get the info in the csv file

name.describe() # to get the statistical data like mean, std, min and max

name.columns # to get the list of columns

name.shape # to get the number of raws and columns

name.dtypes # shows the data type of all columns


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
# addng a new column in the file using the results of other file operations
name['name_of_new_column'] = another / another

# how to remove a column
name.drop(columns=['column_name'], inplace=True)

# renaming
name.rename(columns={"oldName": "newName"}, inplace=True)

#checking duplicates
data.duplicated()
data.duplicated().sum()
data.duplicated().value_counts()
data.duplicated(subset=["col1", "col2"], keep="first")
#`subset` → list of column names to check for duplicates.
#`keep` → decides which duplicate is marked as unique (`'first'`, `'last'`, or `False`).

data.drop_duplicates(inplace = True) #to remove duplicates

# to check NaN values
data.isna().sum()
data.dropna(inplace=True) #drops NaN in all columns
Data.dropna(subset=["ColumnName"], inplace=True) #drops NaN for a specific column
# isna() only recognizes these `None`, `NaN`, or `NaT`

#reassigning the index values
data.reset_index(drop=True)
# data.reset_index(inplace=True)

#returning the number of unique elements exluding NaN values
data["ColumnName"].nunique()

#changing data types of a column
data["columnName"] = data["columnName"].astype(int)

# sorting
name.sort_values('column_name', ascending=False,).head(10)
#the .head() allows you to choose the number of rows you want to get

# saving data to a file
name.to_csv('file_name', index=None) # the index is to remove the index section as a column

name.merge(...) # to merge two columns or rows

#setting a column as an index
result_df.set_index('columnName', inplace=True)


```

```python
# to replace something in a string
df['price'] = df['price'].str.replace('$', '') \
                         .str.replace(',', '') \
                         .str.replace(' ', '')
                         

data["Name"] = data["Name"].str.replace(r'[^\x00-\x7F]+', '', regex=True)

# changing the data type                         
df['price'] = df['price'].astype(int)
type(df['price'][2])

# np.nan 

"""this excludes(~) 'UNKNOWN' 'ERROR' from all the rows(axis=1) """
data = data[~data.isin(["UNKNOWN", "ERROR"]).any(axis=1)]
```

#### Working with dates
```python
#to convert a data type object to date
covid_df.date #lets say this column contains the dates but the datatype is not a date

#this creates a new column where we will put the converted date data
covid_df['date'] = pd.to_datetime(covid_df.date)

#now we can seperate them into year, month, day, weekday etc
covid_df['year'] = pd.DatetimeIndex(covid_df.date).year
covid_df['month'] = pd.DatetimeIndex(covid_df.date).month
covid_df['day'] = pd.DatetimeIndex(covid_df.date).day
covid_df['weekday'] = pd.DatetimeIndex(covid_df.date).weekday
#monday is zero and sunday is 6
```

#### Grouping and aggregation
```python
covid_df.groupby('month') 

monthly_groups = covid_df.groupby('month')
monthly_groups[('column1', 'column2', 'column3')].sum()

#for total sum of the data upto the current date for each row
covid_df['total_cases'] = covid_df.new_cases.cumsum()
```

#### Merging data from multiple sources
```python
#we will take 2 data set location_df and covid_df
locations_df = pd.read_csv('path/location.csv')
locations_df
loacations_df[locations_df.location == "Italy"]

covid_df['location'] = "Italy"
covid_df

# merging the location column on both sides
merged_df = covid_df.merge(locations_df, on="location")
merged_df

```


#### Basic plotting with pandas
This is just creating basic graphs in pandas

```python
name.column_name.plot() # to plot a column
name.column_name.plot(title='title_name') # adding a title name for the graph
name.column_name.plot(kind='bar') # to specify the kind of graph you want to plot

# setting the date column as the index column
name.set_index('column_name', inplace=True)

#combine two columns to plot
name.column1.plot()
name.column2.plot();

```


### Core categories and representative functions

#### General purpose functions

- **clean_names** — _Normalize column names to snake_case, remove special characters._ **Example**
    
    
    
    ```python
    df = df.clean_names()
    ```
    
    Use when you want consistent column identifiers.
    
- **add_column** _(deprecated; prefer_ `DataFrame.assign`_)_ — _Add a column by name with scalar, list, or iterator._ **Example**
    
    
    ```python
    df = df.add_column(column_name="c", value=1)
    ```
    
    Raises if lengths mismatch.
    
- **remove_columns / drop_constant_columns / drop_duplicate_columns** — _Remove unwanted or redundant columns quickly._ **Example**
    
    
    ```python
    df = df.remove_columns(["tmp"]).drop_constant_columns().drop_duplicate_columns()
    ```
    

#### Missing data and imputation

- **fill / impute / flag_nulls** — _Fill missing values, impute by strategy, or create boolean flags for nulls._ **Example**
    
    ```python
    df = df.fillna(0)            # pandas native
    df = df.impute("age", strategy="median")
    df = df.flag_nulls("income")
    ```
    

#### Reshaping and splitting

- **deconcatenate_column / expand_column / explode_index / pivot / row_to_names** — _Split combined columns, expand nested structures, pivot tables, or promote a row to header._ **Example**
        
    ```python
    df = df.deconcatenate_column("full_name", into=["first","last"], sep=" ")
    ```
    

#### Column transforms and feature engineering

- **mutate / transform_columns / min_max_scale / label_encode / encode_categorical** — _Create or transform features with chaining-friendly syntax._ **Example**
    
    
    ```python
    df = df.mutate(age_years = df.age / 365)
    df = df.min_max_scale("score")
    ```
    

#### Joins, grouping, and aggregation

- **conditional_join / groupby_agg / groupby_topk / join_apply** — _Advanced joins and grouped summaries._ **Example**
    
    ```python
    df_summary = df.groupby_agg(["id"], {"score":"mean"})
    ```