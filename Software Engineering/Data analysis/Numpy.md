
# Numerical computing with python and numpy

```python
import numpy as np

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

np.dot(arr1, arr2) 
''' this multiplies the elements in each array sequetially eg (1 * 4), (2 * 5)... then adds the results to get the total sum
```


```python
import numpy as np
data = np.array([[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]])
data.shape # to find the raw and colum of the array
data.dtype # to find data type of the array

data2 = np.array([[10, 11, 12],
				 [13, 14, 15],
				 [16, 17, 18]])

np.matmul(data, data2) # mulitiplies two matrix together or you can use '@' character eg data @ data2
```

working with files (CSV)
```python
import numpy as np

data = np.genfromtxt('file_path/..', delimiter=',', skip_header=1)
# 1. provide the file path
# 2. what seperates the values in the file eg ',' or ':'
# 3. The number of headings that should be skipped 

```

Adding a column in the file

```python
import numpy as np
# to add a column or a raw we use
np.concatenate and np.reshape
# for more information go to documentation

np.savetxt(...) # this save the file 
```