# Data analysis

A process of inspecting, cleansing, transforming and modeling data with the goal of discovering useful information, informing conclusion and supporting decision-making


### 🚀 Step 1: Launch JupyterLab

Open your terminal and run:

bash

```
jupyter lab
```

This will start a local server and open JupyterLab in your browser (usually at `http://localhost:8888`). You’ll see a workspace where you can create notebooks.

### 📓 Step 2: Create a Notebook

- In JupyterLab, click **Notebook → Python 3**.
    
- You’ll get a blank notebook where you can write Python code in cells.
    

### 🛠 Step 3: Load a Dataset

You can practice with any CSV file you have offline. For example, if you have `data.csv` in your Downloads folder:

python

```
import pandas as pd

df = pd.read_csv("/home/hrmoose/Downloads/data.csv")
df.head()
```

This loads the dataset and shows the first 5 rows.

### 📊 Step 4: Do Some Analysis

Try simple operations:

python

```
# Summary statistics
df.describe()

# Count missing values
df.isnull().sum()

# Group by a column
df.groupby("Category")["Sales"].mean()
```

### 🎨 Step 5: Visualize Data

Use matplotlib or seaborn:

python

```
import matplotlib.pyplot as plt
import seaborn as sns

# Histogram
df["Sales"].hist()
plt.show()

# Scatter plot
sns.scatterplot(x="Sales", y="Profit", data=df)
plt.show()
```

### ✅ Practice Ideas

- Clean messy data (remove duplicates, fill missing values).
    
- Explore correlations between columns.
    
- Create bar charts, line plots, and scatter plots.
    
- Analyze your own offline data (expenses, car fuel logs, cooking recipes).