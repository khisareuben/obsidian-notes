## **Python Loops**

In computer programming, loops are used to repeat a block of code. We perform a process of _iteration_ (repeating tasks).

There are 2 types of loops in Python:

- [for loop](https://www.programiz.com/python-programming/for-loop)
- [while loop](https://www.programiz.com/python-programming/while-loop)

Programming languages like Python implement two types of iteration:

1. _Indefinite iteration_, where the number of times the loop is executed depends on how many times a condition is met.
2. _Definite iteration_, where the number of times the loop will be executed is defined in advance (usually based on the collection size).

In a for loop, we will know in advance how many times the loop will need to iterate because we will be working on a collection with a predefined length.

With for loops, on each iteration, we will be able to perform an action on each element of the collection.

For loop syntax:

![](https://lh3.googleusercontent.com/LnVxJ4pq9vwhB0wvL0r9R7I5rkRfZ1exQ_bxQQuab8GyX3A8Zlq1jcZxiD5koQgA5pizHngvWqs0xY7Tm9iliXSeY4ld-iDyrFYcilDncJn9w6rTJ4A2_3g7NvZH7biMIu4IkLXqAXu2cF4mwvYyww)

Let’s break down each of these components:

1. A for keyword indicates the start of a for loop.
2. A <temporary variable> that is used to represent the value of the element in the collection the loop is currently on.
3. An in keyword separates the temporary variable from the collection used for iteration.
4. A <collection> to loop over. In our examples, we will be using a list.
5. An <action> to do anything on each iteration of the loop.

Let’s link these concepts back to our names example. This for loop prints each names in names list:

![](https://lh5.googleusercontent.com/NzrihmTNypXsDSR1tBsVliwiMjc_3fHSjI0w2_KxP_RRPEYCB42cQJ2EUaaIvOJAnQCKL9daBEvzJBUaqVmfYt5FaTTmVO4FeOfe6tr9G0jvCPaQcR5UHIinORQo8RKk5wo3o3Q4qL3aJMlyvbmIfA)

In above example:

1. name is the <temporary variable>.
2. names is our <collection>.
3. print(name) was the <action> performed on every iteration using the temporary variable of name.

**For Loops: Using Range**

A [range](https://www.programiz.com/python-programming/methods/built-in/range) is a series of values between two numeric intervals.

We use Python's built-in function range() to define a range of values.

For example,

five_steps = range(5)

# five_steps is now a collection with 5 elements:

# 0, 1, 2, 3, 4

Let's say we want to print “**_Welcome to PLP”_** five times efficiently.

![](https://lh5.googleusercontent.com/8ZE8BlH1kWCZiPpw6cVFAxrrEgJKn2GpgNlvzyUo9dOmTBmIE5EBC5N0eEkmYc9Yi4xjkXAtvCnOkK4KWohJ0DOyWSADVfLV-hepPnHBtCP1a1mcNzQ52eb-RTomLDpIYRRMzI3bPfTJOV-m2tpYb00)

**While Loops**

A while loop performs a set of instructions as long as a given condition is true.

While loop structure

![](https://lh4.googleusercontent.com/jTxAUUd1GYOyzCAZ0XsN0Hd7PJOG6Qc7_oTyYXH2aB-SO7voASQ3AUCDQag6YYqdAS4lAoXeSvmfZ8IMx-k75ldAbBoc5JA3iUaFIeDTaBY3AZejCd3B176w-MvaB11ErGVOWH_b9OxrHc7utNrhYeE)

Let’s examine this example, where we print the integers 0 through 2:

![](https://lh5.googleusercontent.com/9jnfrC71uwdzitrhCeC3o2RI1tVvzGx_sdeJVQzrCZJao9zxTQ8_17BZMG82sdm736B3R4BtX-ag0-VNF2iU8JSwQXV95ojvQC4ZV6pakMymx13wjrS8sbE4k95fbjtFDw7i90Pum7RT7ZIeoGaIpGI)

Let’s break the loop down:

1. count is initially defined with the value of 0. The conditional statement in the while loop is count <= 2, which is true at the initial iteration of the loop, so the loop body executes.
2. Inside the loop body, count is printed and then incremented by 1.
3. When the first iteration of the loop has finished, Python returns to the top of the loop and checks the conditional again. After the first iteration, count would be equal to 1 so the conditional still evaluates to True and so the loop continues.
4. This continues until the count variable becomes 3. At that point, when the conditional is tested it will no longer be True and the loop will stop.

### **Loop controls: Break and continue**

The **break** statement is used to terminate the loop immediately when it is encountered.

**Example**: Assume we are looping through a list of clothes with listed colors and you want a white cloth and when you locate it, you don’t bother looping through the list of colors.

**Break** comes in handy in such situations, it assumes everything after locating white and the loop stops.

**_Using for loop_**

![](https://lh4.googleusercontent.com/rxR-jfZfc7X-vZKRJggT0CZYO1bHux3Xz6FZNgaLCfQfb8cayHCSRWwWXONixeyQvQRQO0KBTP1Ma_fWwfIKcL2kM9iywD2oQkPBBaEZipxeCv7182F_ZifVBCc-WtgX4I41l7VlFpqSmZiqQThPj5s)

**_Using while loop_**

**_![](https://lh5.googleusercontent.com/vGLkYqovD5VQkf2NC400uHXZuu06o_fTU9zCdle9G46N4pNEM4BE7MzzZHbJFUQJMH2LN7jyx6_K01KVlAPXe6YVjlOSkaAnFlDeugBxVsa53Yg7E8jTMYRJZqeb9sL1bGKd_lVId4CnN1rhdWtuu8E)_**

## **Python continue Statement**

The continue statement is used to skip the current iteration of the loop and the control flow of the program goes to the next iteration.

While the break control statement will come in handy, there are other situations where we don’t want to end the loop entirely. What if we only want to skip the current iteration of the loop?

**Example:**

Let's say you want to automate a gate entrance process, where the age of people entering is limited to 21 years. Loop through the ages list. If an entry is less than 21, skip it and move to the next entry. Otherwise, print() the age.

![](https://lh5.googleusercontent.com/m-HVWNQpmpM8EBRwNKF4w5vtJbm5YHJdsdcyS0WKj_rvJGbdlVKBQ8EvyfUdyqqPLWL2CJz8zfJJb4GQA_Kw63GsKtfwSP85C9hjL_jBv63sVIe2CrsbHoujI4Aw4mNVVq9jjg0j9xn15gUqCMATnb8)

**Nested Loops**

In Python, loops can be nested inside other loops. Nested loops can be used to access items of lists which are inside other lists. The item selected from the outer loop can be used as the list for the inner loop to iterate over.

![](https://lh3.googleusercontent.com/epkLsyEKgJcuBrR3w0_fivBjeeOo7LJAS6QFGAiliyOVtiePUF2AF45B7msYWsKQ50OeXayCmgCOmuE1MqHstv2lYvnE2cViqacZ4n6wX6XjWPfMhNKQ3-TTj9_UOQ_rbEv9m-Tg-ACsBGLAAs1iP7o)

**List comprehensions**

**coming soon ....**

## **More Resources for loops**

[**https://www.codecademy.com/resources/docs/python/loops**](https://www.codecademy.com/resources/docs/python/loops)

[**https://www.programiz.com/python-programming/if-elif-else**](https://www.programiz.com/python-programming/if-elif-else)

[**https://www.programiz.com/python-programming/for-loop**](https://www.programiz.com/python-programming/for-loop)

[**https://www.programiz.com/python-programming/while-loop**](https://www.programiz.com/python-programming/while-loop)

[**https://www.programiz.com/python-programming/break-continue**](https://www.programiz.com/python-programming/break-continue)