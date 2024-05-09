# Stack

Is a linear data structure which follows the LIFO order(Last In First Out)

---

#### 1.  Implementing stack using list

```python
stack = []
stack.append("welcome")
stack.append("to")
stack.append("DSA")
print(stack)
stack.pop()
print(stack)
```

#### 2.  Implementing stack using collection.deque

This is much faster than the one shown above

```python
from collections import deque

stack = deque()
stack.append("welcome")
stack.append("to")
stack.append("DSA")
print(stack)
stack.pop()
print(stack)
```


Next topic: [[Queue]]
previous topic: [[Single linked list]]