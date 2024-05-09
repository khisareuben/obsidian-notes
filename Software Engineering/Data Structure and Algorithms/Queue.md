# Queue
Is a linear data structure which follows the FIFO order(First In First Out).

we will write everything in one class.

---

```python
class Queue:
	def __init__(self):
		self.queue = []

	def enque(self, data):
		self.queue.append(data)

	def deque(self):
		if len(self.queue) < 1:
			print("The list is empty")
			return
		return self.queue.pop(0)

	def size(self):
		print(len(self.queue))

	def display(self):
		print(self.queue)

q = Queue()
q.enque(1)
q.enque(2)
q.enque(3)
q.enque(4)
q.display()
q.size()
q.deque()
q.display()
```


Next topic: [[Doubly Linked List]]
Previous topic: [[Stack]]