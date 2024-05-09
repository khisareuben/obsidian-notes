# Binary search tree

Is a tree with additional restrictions:
1. Left child must always be less than root node
2. Right child must always be greater than root node
3. There is also insertion, deletion and search operations

#### 1. Traversal through the tree

```python
class Node:
	def __init__(self, key):
		self.left = None
		self.right = None
		self.val = key

	def visit(self, node):
		print(node.val, end=" ")

	def preorder(self, current):
		if self.val is None:
			print("The list is empty")
			return
		self.visit(current)
		self.preorder(current.left)
		self.preorder(current.right)

	def inorder(self, current):
		if self.val is None:
			print("The list is empty")
			return
		self.inorder(current.left)
		self.visit(current)
		self.inorder(current.right)

	def postorder(self, current):
		if self.val is None:
			print("The list is empty")
			return
		self.postorder(current.left)
		self.postorder(current.right)
		self.visit(current)


```


#### 3. Insertion in the list

```python
def insert(self, data):
	if self.val:
		if data < self.val:
			if self.left is None:
				self.left = Node(data)
			else:
				self.left.insert(data)
		elif data > self.val:
			if self.right is None:
				self.right = Node(data)
			else:
				self.right.insert(data)
	else:
		self.val = data
```


#### 4. Searching through the list

```python
def search(self, target):
	if target < self.val:
		if self.left is None:
			print(str(target) + " is not found")
			return
		else:
			return self.left.search(target)
	elif target > self.val:
		if self.right is None:
			print(str(target) + " is not found")
			return
		else:
			return self.right.search(target)
	else:
		print(str(target) + " is found")
		return
```


#### 5. Deleting a node in the tree

**Deletion in a BST**:
    
When we want to remove a node with a specific key from the BST, we need to consider three cases:
        
**Case 1**: The node to be deleted has **no children** (it’s a leaf node). In this case, we can simply remove the node.
            
**Case 2**: The node has **one child** (either left or right). We replace the node with its child.
            
**Case 3**: The node has **two children**. This is the most complex scenario. We need to find a suitable replacement for the node. This replacement should maintain the BST properties.
            
- **Choosing the In-Order Successor**:
    
    - When deleting a node with two children, we look for the **in-order successor** (also known as the **minimum value node** in the right subtree).
        
    - The in-order successor is the smallest node that is greater than the node to be deleted.
        
    - Why do we choose the in-order successor?
        
        - It ensures that the BST structure remains intact after deletion.
            
        - The in-order successor will be the next node visited during an **in-order traversal** of the tree.
            
        - By replacing the node to be deleted with the in-order successor, we maintain the order of elements in the BST.
            
- **Finding the In-Order Successor**:
    
    - We start from the node’s right child (since the in-order successor must be in the right subtree).
        
    - Then, we keep moving to the left child until we reach the leftmost leaf node (which has the smallest value).
        
    - This leftmost leaf node is the in-order successor.
        
4. **Example**:
    
    - Suppose we want to delete the node with value 40 from the following BST:
        
        40 50/  30 70 /  60 80
    
    `- The in-order successor of 40 is 50 (the smallest node in the right subtree).`
    `- We replace 40 with 50, and then recursively delete 50 (which falls into either Case 1 or Case 2).`
    

In summary, finding the minimum value (in-order successor) ensures that the BST remains valid and maintains its sorted order after node deletion. 🌳🔍

```python
def findMinValue(self, node):
	current = node
	while current.left:
		current = current.left
	return current
```

```python
def delete(self, key):
	if self is None:
		return self
	if key < self.val:
		if self.left:
			self.left = self.left.delete(key)
	elif key > self.val:
		if self.right:
			self.right = self.right.delete(key)
	else:
		if self.right is None:
			temp = self.left
			self = None
			return temp
		elif self.left is None:
			temp = self.right
			self = None
			return temp
		temp = self.findMinValue(self.right)
		self.val = temp.val
		self.right = self.right.delete(temp.val)
	return self
```


#### This is all the code combined to make a complete BST program

```python
class Node:
	def __init__(self, key):
		self.left = None
		self.right = None
		self.val = key

	def visit(self, node):
		print(node.val, end=" ")

	def preorder(self, current):
		if current is None:
			return
		self.visit(current)
		self.preorder(current.left)
		self.preorder(current.right)

	def inorder(self, current):
		if current is None:
			return
		self.inorder(current.left)
		self.visit(current)
		self.inorder(current.right)

	def postorder(self, current):
		if current is None:
			return
		self.postorder(current.left)
		self.postorder(current.right)
		self.visit(current)

	def insert(self, data):
		if self.val:
			if data < self.val:
				if self.left is None:
					self.left = Node(data)
				else:
					self.left.insert(data)
			elif data > self.val:
				if self.right is None:
					self.right = Node(data)
				else:
					self.right.insert(data)
		else:
			self.val = data


	def search(self, target):
		if target < self.val:
			if self.left is None:
				print(str(target) + " is not found")
				return
			else:
				return self.left.search(target)
		elif target > self.val:
			if self.right is None:
				print(str(target) + " is not found")
				return
			else:
				return self.right.search(target)
		else:
			print(str(target) + " is found")
			return


	def findMinValue(self, node):
		current = node
		while current.left:
			current = current.left
		return current


	def delete(self, key):
		if self is None:
			return self
		if key < self.val:
			if self.left:
				self.left = self.left.delete(key)
		elif key > self.val:
			if self.right:
				self.right = self.right.delete(key)
		else:
			if self.right is None:
				temp = self.left
				self = None
				return temp
			elif self.left is None:
				temp = self.right
				self = None
				return temp
			temp = self.findMinValue(self.right)
			self.val = temp.val
			self.right = self.right.delete(temp.val)
		return self

root = Node(50)
root.insert(30)
root.insert(70)
root.insert(20)
root.insert(40)
root.insert(60)
root.insert(80)

print("preorder: ", end=" ")
root.preorder(root)
print()
print("Inorder: ", end=" ")
root.inorder(root)
print()

root.search(30)
root.search(100)
root.delete(80)

print("Postorder: ", end=" ")
root.postorder(root)
print()

```