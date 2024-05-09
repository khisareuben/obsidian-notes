# Trees

Is a hierarchical data structure, the top most element is known as root of tree. Every node can have at most 2 children.
common traversal methods:
- preorder - starts from root, then goes to left side and lastly the right side
- Inorder - starts from left side, then root and finally the right side
- Postorder - starts from left side, then the right side and finally the root

#### Tree traversal methods

```python
class Node:
	def __init(self, key):
		self.left = None
		self.right = None
		self.val = key

	def visit(self, node):
		print(node.val, end=" ")

	def preoder(self, current):
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

root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)

print("preorder: ", end=" ")
root.preorder(root)
print()
print("Inorder: ", end=" ")
root.inorder(root)
print()
print("Postorder: ", end=" ")
root.postorder(root)
```


Next topic: [[Binary Search Tree]]

previous topic: [[Doubly Linked List]]