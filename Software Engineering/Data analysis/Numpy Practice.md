
# 📊 NumPy Comprehensive Workbook (with Explanations)

We’ll use the **MNIST dataset** (handwritten digits, 70,000 samples, each image is 28×28 pixels flattened into 784 values). This dataset is great for practicing array operations.

### 1. **Array creation**

**Question entails:** Learn how to create different types of arrays (zeros, ones, identity, random).



```python
import numpy as np

zeros = np.zeros((3,3))        # 3x3 matrix of zeros
ones = np.ones((3,3))          # 3x3 matrix of ones
identity = np.eye(3)           # identity matrix
rand_ints = np.random.randint(0, 10, (3,3))  # random integers 0–9
```

👉 This builds your foundation: knowing how to initialize arrays for later computations.

### 2. **Indexing and slicing**

**Question entails:** Extract subsets of data, reverse arrays, and select every nth element.


```python
subset = mnist_data[:10, :5]   # first 10 rows, first 5 columns
reverse_rows = mnist_data[::-1]  # reverse rows
every_2nd = mnist_data[:, ::2]  # every 2nd column
```

👉 Essential for selecting parts of datasets efficiently.

### 3. **Reshaping**

**Question entails:** Convert between flat arrays and 2D images.


```python
img = mnist_data[0]            # one image (784,)
reshaped = img.reshape(28,28)  # back to 28x28
```

👉 Critical when working with image data — you often need to reshape.

### 4. **Broadcasting**

**Question entails:** Apply operations across arrays of different shapes.


```python
matrix = np.ones((3,3))
vector = np.array([1,2,3])
result = matrix + vector   # vector added to each row
```

👉 Broadcasting saves you from writing loops.

### 5. **Mathematical operations**

**Question entails:** Perform math directly on arrays.


```python
normalized = mnist_data / 255.0   # scale pixels to [0,1]
variance = np.var(normalized)
std_dev = np.std(normalized)
```

👉 You’ll often normalize data before training models.

### 6. **Boolean masking**

**Question entails:** Select elements based on conditions.


```python
mask = mnist_data > 128
bright_pixels = mnist_data[mask]
```

👉 Useful for filtering data without loops.

### 7. **Sorting**

**Question entails:** Sort arrays and get sorted indices.


```python
arr = np.array([5,2,9,1])
sorted_arr = np.sort(arr)
indices = np.argsort(arr)
```

👉 Sorting is key for ranking or ordering data.

### 8. **Linear algebra**

**Question entails:** Matrix multiplication and eigen decomposition.


```python
A = np.random.rand(3,3)
B = np.random.rand(3,3)
dot = np.dot(A,B)
eigenvalues, eigenvectors = np.linalg.eig(A)
```

👉 Core for machine learning and scientific computing.

### 9. **Random sampling**

**Question entails:** Select random samples from dataset.


```python
sample = np.random.choice(mnist_data.shape[0], 100, replace=False)
subset = mnist_data[sample]
```

👉 Helps when you want to test on smaller subsets.

### 10. **Statistics**

**Question entails:** Compute mean, median, mode.


```python
mean_val = np.mean(mnist_data)
median_val = np.median(mnist_data)
unique, counts = np.unique(mnist_data, return_counts=True)
mode_val = unique[np.argmax(counts)]
```

👉 Statistical summaries are vital for understanding data.

### 11. **Stacking**

**Question entails:** Combine arrays horizontally or vertically.


```python
a = np.array([1,2,3])
b = np.array([4,5,6])
h_stack = np.hstack((a,b))
v_stack = np.vstack((a,b))
```

👉 Useful for merging datasets.

### 12. **Unique values**

**Question entails:** Find distinct values in dataset.


```python
unique_vals = np.unique(mnist_data)
```

👉 Helps check data integrity.

### 13. **Advanced indexing**

**Question entails:** Select specific rows/columns using lists.


```python
indices = [0,2,4,6]
selected = mnist_data[indices]
```

👉 Handy for custom sampling.

### 14. **Mask operations**

**Question entails:** Modify array values based on condition.


```python
mnist_copy = mnist_data.copy()
mnist_copy[mnist_copy < 50] = 0
```

👉 Often used for cleaning or thresholding.

### 15. **Vectorization**

**Question entails:** Replace loops with fast array operations.


```python
squared = mnist_data ** 2
```

👉 Vectorization is why NumPy is fast.

### 16. **Performance**

**Question entails:** Compare Python loops vs NumPy.


```python
import time
arr = np.random.rand(1000000)

start = time.time()
result = [x**2 for x in arr]
print("Loop:", time.time()-start)

start = time.time()
result = arr**2
print("NumPy:", time.time()-start)
```

👉 Shows why NumPy is preferred for large data.

### 17. **FFT**

**Question entails:** Transform signals to frequency domain.


```python
signal = np.sin(np.linspace(0, 2*np.pi, 100))
fft_result = np.fft.fft(signal)
```

👉 Used in audio/image processing.

### 18. **Polynomials**

**Question entails:** Fit polynomial to data.


```python
x = np.linspace(-3,3,100)
y = x**2 + 2*x + 1
coeffs = np.polyfit(x,y,2)
```

👉 Useful for curve fitting.

### 19. **Meshgrid**

**Question entails:** Generate coordinate grids.


```python
x = np.linspace(-5,5,10)
y = np.linspace(-5,5,10)
X,Y = np.meshgrid(x,y)
Z = X**2 + Y**2
```

👉 Common in plotting surfaces.

### 20. **Simulation**

**Question entails:** Monte Carlo simulation.


```python
N = 100000
x = np.random.rand(N)
y = np.random.rand(N)
inside_circle = (x**2 + y**2) <= 1
pi_estimate = 4 * np.sum(inside_circle) / N
```

👉 Demonstrates how NumPy can simulate probability problems.

✅ That’s **20 NumPy exercises with explanations + solutions**. This should feel like a proper workbook now.