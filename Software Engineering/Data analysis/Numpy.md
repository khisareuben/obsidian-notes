
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
data.shape # returns the number of rows and columns in the array
data.dtype # to find data type of the array

data2 = np.array([[10, 11, 12],
				 [13, 14, 15],
				 [16, 17, 18]])

yields = np.matmul(data, data2) or # mulitiplies two matrix together or you can use '@' character eg data @ data2
data @ data2
```


working with files (CSV)
```python
import urllib.request
urllib.request.urlretrieve(
'https://hub.jovian.me/wp-content/uploads/2020/08/climate.csv', 'climate.txt')
# this imports a csv file online and then we put all the data in a txt file

data = np.genfromtxt('file_path/...txt/csv', delimiter=',', skip_header=1)
# 1. provide the file path for csv or txt file
# 2. what seperates the values in the file eg ',' or ':'
# 3. The number of headings that should be skipped

Note: # numpy mostly works with interger datatypes for calculations 

```

Adding a column in the file

```python
import numpy as np

# to add a column or a raw we use or join two arrays
np.concatenate # for joining two arrays
 and np.reshape # to change the shape or the array

results = np.concatenate((data, yields.reshape(3, 3))) #to add as a row
results = np.concatenate((data, yields)) #without reshape

results = np.concatenate((data, yields.reshape(3, 3)), axis=1) #to add as a column
results = np.concatenate((data, yields),1) #without reshape

#Combine arrays horizontally or vertically. same as concatenate
a = np.array([1,2,3])
b = np.array([4,5,6])
h_stack = np.hstack((a,b))
v_stack = np.vstack((a,b))

np.savetxt(...) # this save the file 
np.savetxt('results.txt/csv', results,
fmt='%.2f', header='column,names', comments='')
```

Indexing
```python
arr3 = np.array([
                [[11, 12, 13, 14], 
                 [23, 14, 15, 19]],
                
                [[15, 16, 17, 21],
                 [63, 92, 36, 18]],
                
                [[98, 32, 81, 23],
                 [17, 18, 19.5, 43]]])
                 
arr3[1, 1, 2] #returns 36

# subarray using ranges
arr3[1:, 0:1, :2] #experiment yourself
```

other ways of creating np arrays

```python
import numpy as np

np.zeros((3, 2))# this creates an array of zeros for 3 raws and 2 colums

np.ones((3, 2)) # this creates an array of ones ...

np.eye(3) #identity matrix whatever that means

rand_ints = np.random.randint(0, 10, (3,3))  # random integers 0–9

np.random.rand(5) #5 columns
np.random.randn(2, 3) #2 rows 3 columns randn also include -ve

np.full([2, 3], 42) # this creates and array of fixed values of 42 

np.linspace(3, 27, 9) #experiment yourself but in summary it returns nine colums with equal range jump/inervals e.g 3, 6, 9

np.arange(10, 90, 3)# this creates a range of arrays from start at 10 ending to 90, at inervals of 3
you can use it with the reshape function e.g
np.arange(10, 90, 3).reshape(3, 3, 3) # it must match the number of elements in the array


```