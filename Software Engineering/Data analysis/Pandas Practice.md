
**20 exercises, each explained and solved** using the **World Bank GDP dataset** (CSV format). This will give you a full workbook to practice offline.

# 📑 Pandas Comprehensive Workbook (with Explanations)

We’ll assume you have a dataset like `gdp.csv` with columns:

- `Country`
    
- `Continent`
    
- `Year`
    
- `GDP` (in USD)
    
- `Population` (optional, for merging later)
    

### 1. **Data loading**

**Entails:** Reading CSV files and inspecting structure.


```python
import pandas as pd

df = pd.read_csv("gdp.csv")
print(df.shape)   # rows, columns
print(df.info())  # column types
print(df.describe())  # summary stats
```

👉 First step in any analysis: know your data.

### 2. **Column selection**

**Entails:** Accessing specific columns.


```python
gdp_only = df['GDP']
```

👉 Useful when focusing on one variable.

### 3. **Row filtering**

**Entails:** Select rows based on conditions.


```python
trillion_plus = df[df['GDP'] > 1e12]
```

👉 Filtering is the bread and butter of analysis.

### 4. **Indexing**

**Entails:** Setting a meaningful index.


```python
df_indexed = df.set_index('Country')
```

👉 Makes lookups faster and more intuitive.

### 5. **Sorting**

**Entails:** Ordering data.


```python
sorted_df = df.sort_values('GDP', ascending=False)
```

👉 Ranking countries by GDP.

### 6. **GroupBy**

**Entails:** Aggregating by categories.


```python
avg_gdp_continent = df.groupby('Continent')['GDP'].mean()
```

👉 Summarize by continent.

### 7. **Aggregation**

**Entails:** Multiple summary stats at once.


```python
agg_stats = df['GDP'].agg(['min','max','mean'])
```

👉 Quick overview of extremes.

### 8. **Merging**

**Entails:** Combine datasets.


```python
population_df = pd.read_csv("population.csv")
merged = pd.merge(df, population_df, on='Country')
```

👉 Essential when combining multiple sources.

### 9. **New columns**

**Entails:** Create derived metrics.


```python
merged['GDP_per_capita'] = merged['GDP'] / merged['Population']
```

👉 Derived features are often more insightful.

### 10. **Missing values**

**Entails:** Handle NaN values.


```python
df['GDP'] = df['GDP'].fillna(df['GDP'].median())
```

👉 Prevents errors in calculations.

### 11. **Pivot tables**

**Entails:** Reshape data for analysis.


```python
pivot = df.pivot_table(values='GDP', index='Continent', columns='Year', aggfunc='mean')
```

👉 Great for comparing across years.

### 12. **MultiIndex**

**Entails:** Hierarchical indexing.


```python
multi = df.set_index(['Continent','Country'])
```

👉 Useful for complex datasets.

### 13. **Apply function**

**Entails:** Apply custom transformations.


```python
df['log_GDP'] = df['GDP'].apply(lambda x: np.log(x))
```

👉 Flexible way to transform columns.

### 14. **String operations**

**Entails:** Manipulate text columns.


```python
df['Country_Code'] = df['Country'].str[:3].str.upper()
```

👉 Handy for cleaning categorical data.

### 15. **Datetime**

**Entails:** Work with dates.


```python
df['Year'] = pd.to_datetime(df['Year'], format='%Y')
```

👉 Enables time-series analysis.

### 16. **Resampling**

**Entails:** Change frequency of time-series.


```python
df_time = df.set_index('Year')
annual = df_time.resample('A').mean()
```

👉 Useful for trend analysis.

### 17. **Window functions**

**Entails:** Rolling statistics.


```python
df['GDP_rolling'] = df['GDP'].rolling(window=3).mean()
```

👉 Smooths noisy data.

### 18. **Categoricals**

**Entails:** Optimize categorical data.


```python
df['Continent'] = df['Continent'].astype('category')
```

👉 Saves memory and speeds up operations.

### 19. **Export**

**Entails:** Save results.


```python
df.to_csv("cleaned_gdp.csv", index=False)
```

👉 Always export cleaned data for reuse.

### 20. **Visualization**

**Entails:** Quick plots with Pandas.


```python
df.groupby('Year')['GDP'].sum().plot(kind='line')
```

👉 Fast way to visualize trends.

✅ That’s **20 Pandas exercises with explanations + solutions** — covering loading, cleaning, transforming, aggregating, and visualizing.