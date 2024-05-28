# Graphs practice problems

once you understand how to tackle these questions the you'll have no problem tackling more advance problems

## Question One

check if path exists through source and destination (directed acyclic graph).

The graph/map
```python
graph = {
	"a" : ["b", "c"],
	"b" : ["f", "d"],
	"c" : [],
	"d" : ["g", "i"],
	"e" : ["h"],
	"f" : ["e"],
	"g" : ["h"],
	"h" : [],
	"i" : []
}

```


#### These are the steps we are gonna use

1. If source becomes destination the return true
2. Use a bool variable to keep track of dfs call response
3. Make calls to the neighbours
4. Return ans

```python
def has_path(src, dst, graph):
	if src == dst:
		return True
	ans = False
	for neighbours in graph[src]:
		ans = ans or has_path(neighbours, dst, graph)

	return ans

src = input("Enter the source: ")
dst = input("Enter the destination: ")
print(has_path(src, dst, graph))
```


## Question Two

check if path exists between the source and destination (undirected graph).

The graph/map
```python
graph = {
	"a" : ["b", "c"],
	"b" : ["a", "f", "d"],
	"c" : ["a"],
	"d" : ["b", "g", "i"],
	"e" : ["f", "h"],
	"f" : ["b", "e"],
	"g" : ["d", "h"],
	"h" : ["e", "g"],
	"i" : ["d"]
}
```


* we need to keep track of the visited node, this is done using a data structure called **visited** e.g sets, vectors
* This help to prevent going back to the previous node 

#### These are the steps to be followed

1. If src becomes dst return True
2. *Mark the node visited*
3. Use the bool variable to keep track of dfs call response
4. Make calls to the neighbors ( *while checking for not visited*)
5. Return ans

```python
def has_path(src, dst, graph, visited):
	if src == dst:
		return True
	visted.add(src)
	ans = False
	for neighbors in graph[src]:
		if neighbors not in visited:
			ans = ans or has_path(neighbors, dst, graph, visited)

	return ans

visited = set()
src = input("Enter the source: ")
dst = input("Enter the destination: ")
print(has_path(src, dst, graph, visited))
```


Next topic : [[Hash tables]]

previous topic : [[Graphs practice]]