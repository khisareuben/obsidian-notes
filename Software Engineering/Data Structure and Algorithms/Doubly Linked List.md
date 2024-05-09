# Doubly Linked List

- Its a collection of nodes in which each node contains data field and having two pointers, one pointer is for previous node and the other for next node.
- Traversal is in forward direction as well as backward direction
---

#### 1.  Creating a node class

```python
class Node:
	def __init__(self, data):
		self.data = data
		self.prev = None
		self.next = None
```

#### 2. Creating a boubly Linked List class

```python
class Dll:
	def __init__(self):
		self.head = None

	#verything else will appear here  including  all the next functions below
```


#### 3.  Check if the list is empty

```python
def is_empty(self):
	if self.head is None:
		print("The list is empty")
	else:
		print("The list is not empty")
```


#### 4. Check the size of the list

```python
def size(self):
	current = self.head
	count = 0
	while current:
		count += 1
		current = current.next
	print(count)
```


#### 5.  Insertion at the beginning of the list

```python
def add_at_begin(self, data):
	new = Node(data)
	if self.head is None:
		self.head = new
	else:
		current = self.head
		new.next = current
		current.prev = new
		self.head = new
```


#### 6.  Insertion at the end of the list

```python
def add_at_end(self, data):
	new = Node(data)
	if self.head is None:
		self.head = new
	else:
		current = self.head
		while current.next:
			current = current.next
		current.next = new
		new.prev = current
```


#### 7.  Insertion at a specific position of the in the list

```python
def add_at_spec_pos(self, data, position):
	new = Node(data)
	current = self.head
	for i in range(1, position-1):
		current = current.next
	new.next = current.next
	current.next.prev = new
	current.next = new
	new.prev = current
```


#### 8.  Deletion at the beginning of the list

```python
def del_at_begin(self):
	if self.head is None:
		print("The list is empty")
		return
	current = self.head
	self.head = current.next
	current.next = None
	self.head.prev = None
```


#### 9.  Deletion at the end of the list

```python
def del_at_end(self):
	if self.head is None:
		print("The list is empty")
		return
	before = self.head
	current = self.head.next
	while current.next:
		current = current.next
		before = before.next
	before.next = None
	current.prev = None
```


#### 10.  Deletion at a specific position in the list

```python
def del_at_spec_pos(self):
	before = self.head
	current = self.head.next
	for i in range(1, position-1):
		current = current.next
		before = before.next
	before.next = current.next
	current.next.prev = before
	current.next = None
	current.prev = None
```


#### 11.  Forward Traversal through the list

Traversal means traveling through the list and print what is in the list

```python
def traversal(self):
	if self.head is None:
		print("List is empty")
	else:
		 current = self.head
		 while current:
			 print(current.data, end=" ")
			 current = current.next
```


#### 12. Backward traversal through the list

```python
def backward_traversal(self):
	if self.head is None:
		print("The list is empty")
	else:
		current = self.head
		while current.next:
			current = current.next

		while current:
			print(current.data, end=" ")
			current = current.prev
```


#### 13.  Printing everything in the list on the screen

```python
def display(self):
	lists = []
	current = self.head
	while current:
		lists.append(str(current.data))
		current = current.next
	print(" <-> ".join(lists))
```

#### 14.  Using all we learned and the functions we wrote 

```python
dll = Dll()
dll.add_at_end(2)
dll.add_at_end(3)
dll.add_at_end(4)
dll.add_at_end(5)
dll.add_at_begin(1)
dll.is_empty()
dll.size()
dll.display()
dll.del_at_end()
dll.display()
```


Next topic: [[Trees]]
previous topic: [[Queue]]