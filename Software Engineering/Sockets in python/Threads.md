# Threads

- Allows us to speed up programs by executing multiple tasks at the same time.
- Each task will run on its own thread
- Each thread can run simultaneously and share data with each others.

```python
import threading

def function1():
	for i in range(10):
		print("One")

def function2():
	for i in range(10):
		print("Two")

def function3():
	for i in range(10):
		print("Three")

t1 = threading.Thread(target=function1)
t2 = threading.Thread(target=function2)
t3 = threading.Thread(target=function3)

t1.start()
t2.start()
t3.start()
```