
# 🧠 Kotlin Data Structures – Master Notes

## 📦 Stack (LIFO)



```kotlin

class Stack<T> {
    private val items = mutableListOf<T>()

    fun push(item: T) = items.add(item)
    fun pop(): T? = if (items.isNotEmpty()) items.removeAt(items.size - 1) else null
    fun peek(): T? = items.lastOrNull()
    fun isEmpty() = items.isEmpty()
    fun size() = items.size
    fun printAll() = println("Stack contents: ${items.joinToString(" -> ")}")
}

fun main() {
    val stack = Stack<Int>()
    stack.push(10)
    stack.push(20)
    stack.push(30)

	stack.printAll()
    println("Top: ${stack.peek()}")     // 30
    println("Pop: ${stack.pop()}")      // 30
    println("Size: ${stack.size()}")    // 2
}


```

## 🚶 Queue (FIFO)



```kotlin

class Queue<T> {
    private val items = mutableListOf<T>()

    fun enqueue(item: T) = items.add(item)
    fun dequeue(): T? = if (items.isNotEmpty()) items.removeAt(0) else null
    fun peek(): T? = items.firstOrNull()
    fun isEmpty() = items.isEmpty()
    fun size() = items.size
    fun printAll() = println("Queue contents: ${items.joinToString(" -> ")}")
}

fun main() {
    val queue = Queue<String>()
    queue.enqueue("A")
    queue.enqueue("B")
    queue.enqueue("C")

	println("Size: ${queue.size()}")
    println("Front: ${queue.peek()}")   // A
    println("Dequeue: ${queue.dequeue()}") // A
    queue.printAll() // Queue contents: B -> C
    println("Size: ${queue.size()}")    // 2
}


```

## 🌳 Binary Tree (Inorder Traversal)



```kotlin

class TreeNode<T>(val data: T) {
    var left: TreeNode<T>? = null
    var right: TreeNode<T>? = null
}

fun inorderTraversal(node: TreeNode<Int>?) {
    if (node == null) return
    inorderTraversal(node.left)
    print("${node.data} ")
    inorderTraversal(node.right)
}

fun main() {
    val root = TreeNode(10)
    root.left = TreeNode(5)
    root.right = TreeNode(15)
    root.left?.left = TreeNode(2)
    root.left?.right = TreeNode(7)

    println("Inorder Traversal:")
    inorderTraversal(root) // 2 5 7 10 15
}


```

## 🔗 Graph (Adjacency List + DFS/BFS)

### Graph Class



```kotlin
class Graph {
    private val adjList = mutableMapOf<String, MutableList<String>>()

    fun addVertex(vertex: String) {
        adjList.putIfAbsent(vertex, mutableListOf())
    }

    fun addEdge(src: String, dest: String) {
        adjList[src]?.add(dest)
        adjList[dest]?.add(src) // Undirected graph
    }

    fun getAdjList(): Map<String, List<String>> = adjList
}
```

### Depth-First Search (DFS)



```kotlin
fun dfs(graph: Graph, start: String, visited: MutableSet<String> = mutableSetOf()) {
    if (start in visited) return
    println(start)
    visited.add(start)

    for (neighbor in graph.getAdjList()[start].orEmpty()) {
        dfs(graph, neighbor, visited)
    }
}
```

### Breadth-First Search (BFS)



```kotlin
fun bfs(graph: Graph, start: String) {
    val visited = mutableSetOf<String>()
    val queue = ArrayDeque<String>()

    visited.add(start)
    queue.add(start)

    while (queue.isNotEmpty()) {
        val current = queue.removeFirst()
        println(current)

        for (neighbor in graph.getAdjList()[current].orEmpty()) {
            if (neighbor !in visited) {
                visited.add(neighbor)
                queue.add(neighbor)
            }
        }
    }
}
```

### Sample Usage



```kotlin
fun main() {
    val graph = Graph()
    listOf("A", "B", "C", "D", "E").forEach { graph.addVertex(it) }

    graph.addEdge("A", "B")
    graph.addEdge("A", "C")
    graph.addEdge("B", "D")
    graph.addEdge("C", "E")

    println("DFS from A:")
    dfs(graph, "A")

    println("\nBFS from A:")
    bfs(graph, "A")
}
```



```kotlin

class Graph {
    private val adjList = mutableMapOf<String, MutableList<String>>()

    fun addVertex(vertex: String) {
        adjList.putIfAbsent(vertex, mutableListOf())
    }

    fun addEdge(src: String, dest: String) {
        adjList[src]?.add(dest)
        adjList[dest]?.add(src) // Undirected
    }

    fun getAdjList(): Map<String, List<String>> = adjList
}

fun dfs(graph: Graph, start: String, visited: MutableSet<String> = mutableSetOf()) {
    if (start in visited) return
    println(start)
    visited.add(start)

    for (neighbor in graph.getAdjList()[start].orEmpty()) {
        dfs(graph, neighbor, visited)
    }
}

fun bfs(graph: Graph, start: String) {
    val visited = mutableSetOf<String>()
    val queue = ArrayDeque<String>()

    visited.add(start)
    queue.add(start)

    while (queue.isNotEmpty()) {
        val current = queue.removeFirst()
        println(current)

        for (neighbor in graph.getAdjList()[current].orEmpty()) {
            if (neighbor !in visited) {
                visited.add(neighbor)
                queue.add(neighbor)
            }
        }
    }
}

fun main() {
    val graph = Graph()
    listOf("A", "B", "C", "D", "E").forEach { graph.addVertex(it) }

    graph.addEdge("A", "B")
    graph.addEdge("A", "C")
    graph.addEdge("B", "D")
    graph.addEdge("C", "E")

    println("DFS from A:")
    dfs(graph, "A")

    println("\nBFS from A:")
    bfs(graph, "A")
}


```


## 🧠 Hashing (Basic HashMap)



```kotlin

fun main() {
    val map = mutableMapOf<String, Int>()
    map["apple"] = 3
    map["banana"] = 5

    println("Apple count: ${map["apple"]}")       // 3
    println("Has banana? ${map.containsKey("banana")}") // true
    println("Keys: ${map.keys}")                  // [apple, banana]
}


```


# Linked List

```kotlin

// Node class
class Node<T>(var data: T, var next: Node<T>? = null)

// LinkedList class
class LinkedList<T> {
    private var head: Node<T>? = null

    // Add element to end
    fun append(data: T) {
        val newNode = Node(data)
        if (head == null) {
            head = newNode
        } else {
            var current = head
            while (current?.next != null) {
                current = current.next
            }
            current?.next = newNode
        }
    }

    // Add element to beginning
    fun prepend(data: T) {
        val newNode = Node(data)
        newNode.next = head
        head = newNode
    }

    // Delete first occurrence of a value
    fun delete(data: T) {
        if (head == null) return

        if (head?.data == data) {
            head = head?.next
            return
        }

        var current = head
        while (current?.next != null) {
            if (current.next?.data == data) {
                current.next = current.next?.next
                return
            }
            current = current.next
        }
    }

    // Print all elements
    fun printList() {
        var current = head
        while (current != null) {
            print("${current.data} -> ")
            current = current.next
        }
        println("null")
    }
}

// Main function to test
fun main() {
    val list = LinkedList<Int>()
    list.append(10)
    list.append(20)
    list.append(30)
    list.printList() // 10 -> 20 -> 30 -> null

    list.prepend(5)
    list.printList() // 5 -> 10 -> 20 -> 30 -> null

    list.delete(20)
    list.printList() // 5 -> 10 -> 30 -> null
}



```


## 🔁 Doubly Linked List



```kotlin
class Node<T>(var data: T) {
    var next: Node<T>? = null
    var prev: Node<T>? = null
}

class DoublyLinkedList<T> {
    private var head: Node<T>? = null
    private var tail: Node<T>? = null

    fun append(data: T) {
        val newNode = Node(data)
        if (head == null) {
            head = newNode
            tail = newNode
        } else {
            tail?.next = newNode
            newNode.prev = tail
            tail = newNode
        }
    }

    fun prepend(data: T) {
        val newNode = Node(data)
        if (head == null) {
            head = newNode
            tail = newNode
        } else {
            newNode.next = head
            head?.prev = newNode
            head = newNode
        }
    }

    fun delete(data: T) {
        var current = head
        while (current != null) {
            if (current.data == data) {
                if (current.prev != null) {
                    current.prev?.next = current.next
                } else {
                    head = current.next
                }

                if (current.next != null) {
                    current.next?.prev = current.prev
                } else {
                    tail = current.prev
                }
                return
            }
            current = current.next
        }
    }

    fun printForward() {
        var current = head
        while (current != null) {
            print("${current.data} <-> ")
            current = current.next
        }
        println("null")
    }

    fun printBackward() {
        var current = tail
        while (current != null) {
            print("${current.data} <-> ")
            current = current.prev
        }
        println("null")
    }
}
```

## 🧪 Sample Linked List Usage



```kotlin
fun main() {
    val list = DoublyLinkedList<Int>()
    list.append(10)
    list.append(20)
    list.append(30)
    list.printForward()   // 10 <-> 20 <-> 30 <-> null
    list.printBackward()  // 30 <-> 20 <-> 10 <-> null

    list.prepend(5)
    list.printForward()   // 5 <-> 10 <-> 20 <-> 30 <-> null

    list.delete(20)
    list.printForward()   // 5 <-> 10 <-> 30 <-> null
    list.printBackward()  // 30 <-> 10 <-> 5 <-> null
}
```