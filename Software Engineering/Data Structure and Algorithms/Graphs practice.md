# Graph practice
we will write the coding implementation of the **BFS** and **DFS** algorithms

#### 1. Depth First Search (DFS) [stack]

```python

graph = {
	"a" : ["b", "d"],
	"b" : [],
	"c" : [],
	"d" : ["e", "g"],
	"e" : ["c"],
	"f" : [],
	"g" : ["f"],
		
}

def dfs(graph, source):
	stack = []
	stack.append(source)
	while stack:
		node = stack.pop(-1)
		print(node, end= " ")
		for neighbour in graph[node]:
			stack.append(neighbour)

dfs(graph, "a")
	
```