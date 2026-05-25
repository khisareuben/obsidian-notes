
**20 exercises, each explained and solved**. We’ll use the **Iris dataset** (classic dataset with sepal length, sepal width, petal length, petal width, and species). This dataset is perfect for visualization practice.

# 📈 Matplotlib Comprehensive Workbook (with Explanations)

### 1. **Basic scatter**

**Entails:** Plot two variables against each other.

python

```
import matplotlib.pyplot as plt

plt.scatter(df['sepal_length'], df['sepal_width'])
plt.xlabel("Sepal Length")
plt.ylabel("Sepal Width")
plt.title("Sepal Length vs Width")
plt.show()
```

👉 Scatter plots show relationships between variables.

### 2. **Line plot**

**Entails:** Plot trends over time or ordered data.

python

```
years = [2000,2005,2010,2015,2020]
gdp = [5,7,9,12,15]
plt.plot(years, gdp, marker='o')
plt.title("GDP Growth Over Years")
plt.xlabel("Year")
plt.ylabel("GDP (Trillions)")
plt.show()
```

👉 Line plots are best for trends.

### 3. **Histogram**

**Entails:** Show distribution of a variable.

python

```
plt.hist(df['petal_length'], bins=20, color='skyblue')
plt.title("Distribution of Petal Length")
plt.show()
```

👉 Histograms reveal frequency distributions.

### 4. **Bar chart**

**Entails:** Compare categories.

python

```
avg_sepal = df.groupby('species')['sepal_length'].mean()
avg_sepal.plot(kind='bar')
plt.title("Average Sepal Length by Species")
plt.show()
```

👉 Bar charts compare categorical averages.

### 5. **Pie chart**

**Entails:** Show proportions.

python

```
species_counts = df['species'].value_counts()
plt.pie(species_counts, labels=species_counts.index, autopct='%1.1f%%')
plt.title("Species Distribution")
plt.show()
```

👉 Pie charts visualize proportions.

### 6. **Box plot**

**Entails:** Show spread and outliers.

python

```
plt.boxplot(df['petal_length'])
plt.title("Boxplot of Petal Length")
plt.show()
```

👉 Boxplots highlight variability and outliers.

### 7. **Subplots**

**Entails:** Multiple plots in one figure.

python

```
fig, axs = plt.subplots(2,2)
axs[0,0].hist(df['sepal_length'])
axs[0,1].hist(df['sepal_width'])
axs[1,0].hist(df['petal_length'])
axs[1,1].hist(df['petal_width'])
plt.tight_layout()
plt.show()
```

👉 Subplots let you compare multiple variables.

### 8. **Customization**

**Entails:** Add labels, titles, legends.

python

```
plt.scatter(df['sepal_length'], df['sepal_width'], label='Sepal')
plt.legend()
plt.title("Customized Scatter Plot")
plt.xlabel("Length")
plt.ylabel("Width")
plt.show()
```

👉 Customization makes plots readable.

### 9. **Colors**

**Entails:** Different colors for categories.

python

```
for species, group in df.groupby('species'):
    plt.scatter(group['sepal_length'], group['sepal_width'], label=species)
plt.legend()
plt.show()
```

👉 Colors distinguish categories.

### 10. **Markers**

**Entails:** Different marker styles.

python

```
plt.plot(df['sepal_length'], marker='o', linestyle='None')
plt.plot(df['sepal_width'], marker='x', linestyle='None')
plt.show()
```

👉 Markers add clarity in scatter plots.

### 11. **Annotations**

**Entails:** Highlight specific points.

python

```
max_val = df['sepal_length'].max()
plt.scatter(df['sepal_length'], df['sepal_width'])
plt.annotate("Max Sepal Length", xy=(max_val, df['sepal_width'].iloc[df['sepal_length'].idxmax()]))
plt.show()
```

👉 Annotations call attention to key data.

### 12. **Grid**

**Entails:** Add gridlines.

python

```
plt.plot(df['sepal_length'])
plt.grid(True)
plt.show()
```

👉 Grids improve readability.

### 13. **Styles**

**Entails:** Use built-in style sheets.

python

```
plt.style.use('ggplot')
plt.hist(df['sepal_length'])
plt.show()
```

👉 Styles make plots visually appealing.

### 14. **Save figure**

**Entails:** Export plots.

python

```
plt.plot(df['sepal_length'])
plt.savefig("sepal_plot.png")
```

👉 Save plots for reports.

### 15. **Multiple figures**

**Entails:** Create separate figures.

python

```
plt.figure()
plt.plot(df['sepal_length'])
plt.figure()
plt.plot(df['sepal_width'])
plt.show()
```

👉 Useful when comparing different plots.

### 16. **Stacked bar**

**Entails:** Show multiple values stacked.

python

```
df.groupby('species')[['sepal_length','sepal_width']].mean().plot(kind='bar', stacked=True)
plt.show()
```

👉 Stacked bars show composition.

### 17. **Heatmap**

**Entails:** Visualize correlation matrix.

python

```
import numpy as np
corr = df.corr()
plt.imshow(corr, cmap='coolwarm', interpolation='none')
plt.colorbar()
plt.xticks(range(len(corr)), corr.columns, rotation=90)
plt.yticks(range(len(corr)), corr.columns)
plt.show()
```

👉 Heatmaps reveal relationships.

### 18. **3D plot**

**Entails:** Plot in 3D space.

python

```
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['sepal_length'], df['sepal_width'], df['petal_length'])
plt.show()
```

👉 3D plots show multi-variable relationships.

### 19. **Interactive**

**Entails:** Enable zoom/pan.

python

```
plt.plot(df['sepal_length'])
plt.show()  # interactive by default in Jupyter
```

👉 Interactivity helps explore data.

### 20. **Advanced**

**Entails:** Combine multiple plot types.

python

```
plt.scatter(df['sepal_length'], df['sepal_width'], label='Scatter')
plt.plot(df['sepal_length'], color='red', label='Line')
plt.legend()
plt.show()
```

👉 Advanced plots mix styles for richer insights.

✅ That’s **20 Matplotlib exercises with explanations + solutions** — covering scatter, line, histograms, bar, pie, box, subplots, customization, colors, annotations, grids, styles, saving, stacked bars, heatmaps, 3D, and advanced combinations.