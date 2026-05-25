```python
import os

os.getcwd() #check the present working directory

help(os.listdir)
os.listdir('.') #to get the list of files in a directory
os.listdir('/user') # absolute path

os.makedirs('./data', exist_ok=True) #to make a new directory

#opening files
file1 = open('./data/loans1.txt', mode='r')
file1_contents = file1.read()
print(file1_contents)
file1.close()

#closing files automatically 
with open('./data/load1.txt') as file2;
file2_contents = file2.read()
print(file2_contents)

# read line by line
with open('./data/load1.txt') as file2:
file2_lines = file2.readlines()
file2_lines 
file2_lines[0].strip() # to remove /n character
```