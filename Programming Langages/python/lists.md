
A list is created in Python by placing items inside [], separated by commas. For example,

![](https://lh5.googleusercontent.com/WgiELuhy7AJyqsIJulrC2_6LxPhUeBIA4fx3gn8Aq_jqrCyCdZLReMrWSK8FzyXuDVw4s8Tv4Fnei9esBXJiQT2CxIWMR6NrIlrV_YY4qhv7y1x7oYaUIvILFp5puR90qaEf6jMO7PnBjRv7hBSrFVg)

Here, we have created a list named numbers with **3** integer items.

A list can have any number of items and they may be of different types (integer, float, string, etc.). For example,

![](https://lh5.googleusercontent.com/DvCGvSd6ZLG4A8CjLNHcoZmkY3qRJ71Pd38F69E1AnfICND36zveNhIk-yoRFk59MFZreyqb2jLP_wLrOzsgZ0kGzlliJISasZFWDxr84BqC-OzuuKZUgSmgLf49-pnYNSiQA6J3i24ig9I_UXutNcc)

## **Access Python List Elements**

In Python, each item in a list is associated with a number. The number is known as a list index.

We can access elements of an array using the index number **(0, 1, 2 …)**. For example,

![](https://lh6.googleusercontent.com/kg8-tXb1DoNZw4JYA-Zb9QhABPCUzl2cIjbt66vhfd_mSTdk3Vqf1iHcwcc1HvCUzU640HiIcwblecEtiAUhiB6yDkiE1tmpn6PMeXZRf3udlwH0oa6k_9r8w564Fj2IHLSqXXtJpK5MvpojUeiXKRk)

In the above example, we have created a list named languages.

![](https://lh3.googleusercontent.com/dZKgreffxrbOy6ilG-UWpQ44bnMkDqNOHJ5dEwbtom8vPh2ccRe_3beUQFIEAiw8X0UIEmRXkO8QGN8pbPgFymo4sadxQ_jRCr1h99upLJR4yok_tqPgGrGr3gb-J3hMX5bOke-POHLJw_PuyX9hMbc)

List Indexing in Python

Here, we can see each list item is associated with the index number. And, we have used the index number to access the items.

**Note:** The list index always starts with **0**. Hence, the first element of a list is present at index **0**, not **1**.

## **Slicing of a Python List**

In Python, it is possible to access a section of items from the list using the slicing operator :, not just a single item. For example,

![](https://lh5.googleusercontent.com/koUnPPjOL0XCc3FBZDoiEIKlyD-tZpgtLrGgHlre1j1hHekk3U7OE-_6_JBnjnwAQ38FgQ11NFgb-_wXW76BlAnvxaU3F25d8vlY56fF0m2t34iv7mmvMFFPTfCB6pIaA0cA5cyC9HTTMlOafr449EA)

Here,

- my_list[2:5] returns a list with items from index **2** to index **4**.
- my_list[5:] returns a list with items from index **1** to the end.
- my_list[:] returns all list items

**Note**: When we slice lists, the start index is inclusive but the end index is exclusive.

## **Add Elements to a Python List**

Python List provides different methods to add items to a list.

**1. Using append()**

The append() method adds an item at the end of the list.

For example,

![](https://lh6.googleusercontent.com/X4rNJ33wUNfVbvvVxe8bRT-R9bbKtYbSsq_F8PJQDSJyDruF4nG1WQBnNe42t2cmeelUG_Ta8q7qLKmi5U9H6u-X4C2LoUGMO7YaWcB_fcBVfbCAWNrCdzub-i-cwDoQkJ9njqf9EHUnvMNwQ192PsE)

Here, append() adds **32** at the end of the array.

**2. Using extend()**

We use the extend() method to add all items of one list to another. For example,

![](https://lh5.googleusercontent.com/-svYi4YBTQVrRShsiSGgJM2yuY6ZSLGPHBf6fAQ0yxBRcaQRHWO4Mx2sHN5v5MR5Vfuu5dnOA4Gzi59cylK5SVXUpS-5ux2AZoRSrDjPabKk0Mnr7u2Nsr9-M1ENxu9DQeJ_S45Baukj2KaUtid0EKU)

In the above example, we have two lists named prime_numbers and even_numbers. Notice the statement,

## **Change List Items**

Python lists are mutable. Meaning lists are changeable. And, we can change items of a list by assigning new values using = operator. For example,

![](https://lh6.googleusercontent.com/JOxZT8IiHsSNvcpg-ISN49ixB6n2kbrio6v1XXrjckRU_aLNoHjpHcbNHM5srMVYxC3-xqnkMvbXbFGllTh2JWl8_RiPZIQEIe1DA0BikUFuugX666XRqJjsLUZxVUWjTOSkXxudFq7XLhGLhnRAFi4)

## **Remove an Item From a List**

**1. Using del()**

In Python, we can use the del statement to remove one or more items from a list. For example,

![](https://lh6.googleusercontent.com/oCt3HNHFWoeem1GS59_B50bZgZMMJ4YTfi0zrfgqd4-MjD73WbQRAv95RhhHIV3R_83pRCyDkmpbsPyySEgxz-AR02xOgAiaW6lgwNVWGWGm_S7bD0o9ZWYFdHCLuHRP9YyoDN82_ffoY8fYhsw_bMg)

**2. Using remove()**

We can also use the remove() method to delete a list item.

For example:

![](https://lh4.googleusercontent.com/cSU--XlcYrcJWI3Z6eEV5OVk6qmCl17wwPM1fJnZm6waSWZPT9bvnzf8dc6FgIYAi-zW2MJRNv2XjVPToQTz1h_tPbnCXQEVOCnPBiOx1ndNN0r7_Xmpkqahe8Z3vyM2c5tnPS8p22cD8X4dOMotqOQ)

Here, languages.remove('Python') removes 'Python' from the languages list.

## **Python List Methods**

Python has many useful list methods that make it really easy to work with lists.

![](https://lh6.googleusercontent.com/YjQDn2cwdhBal4CtyusjwiFCZUiRWDwEl4OQ9Zr9J8eTkXESC9FSbBGUgWnblxOt6TnE7_m4qVLBLneud6Lj8HnoH5FGVWVatgcxy1HPCi5yteE8TrZ1HH8oKYAtLaY8QLtqgoWFh_LiAjoAfb3uWWw)

## **Iterating through a List**

We can use the for loop to iterate over the elements of a list. For example,

![](https://lh4.googleusercontent.com/kcRQgXGT7HvrsYWF_0iFdiYkzzp9IfwHzERcmJ0KB353FcQWrjv9szlpHIOgZSdB9H0W-xX7v-an-lWY3msXuFq6D8KsE7FM6Jmf4tN7riWKRRyAgid5-dqUj1BhAk_I8iKDLiutV54Xgz1pHGxCSKQ)

## **Python List Comprehension**

List comprehension is a concise and elegant way to create lists.

A list comprehension consists of an expression followed by the for statement inside square brackets.

Here is an example to make a list with each item being increasing by power of **2.**

**![](https://lh6.googleusercontent.com/h_ievMml-KhYT9LRGorZQm_M5K4-2GphiG1Xx3Gf8kK8ZF14vV_64oDQVIkjdpCs0Ole7lh5QzL8KqT7bTpHcwIkKP15bVTGzKXWmQ4sZb2Za3BkfTlU0mUQS6T7fyAp_nNXgWAERC8p_naf9pudit8)**

In the above example, we have used the list comprehension to make a list with each item being increased by power of **2.** Notice the code,

![](https://lh5.googleusercontent.com/f-YQgn7fO0DOtKy0FEhwmDcKZAm70_SuQycZld6QbvDu8W6mKyGnOMEbu9mLj1yCjBGQeaHtioRhSp9rO8Xlo5hrGBhjZvDbyNsiPn99ksqEJrBjcoLUUv3v3eAufmiZN2LTni3xx4MeeUxgzVjZzqI)

# **Tuples**

A tuple in Python is similar to a list. The difference between the two is that we cannot change the elements of a tuple once it is assigned whereas we can change the elements of a list.

## **Creating a Tuple**

A tuple is created by placing all the items (elements) inside parentheses (), separated by commas. The parentheses are optional, however, it is a good practice to use them.

A tuple can have any number of items and they may be of different types (integer, float, list, string, etc.).

## **Create a Python Tuple With one Element**

In Python, creating a tuple with one element is a bit tricky. Having one element within parentheses is not enough.

We can use the type() function to know which class a variable or a value belongs to.

![](https://lh3.googleusercontent.com/6qwUnAHBGGLZCrIy3WESuiLHjtd8Iyr59pOP3s-QZRjvQpDNT_vQpme6kdOqUBMGZlu2fjSW2mvOVtE8JPmXYy7Xg8AeZHUiEjULOZiheJpgOIH3M7T-4pAAKhs3l3WSggweCxs_8QT93U3cUUrbKUE)

Here,

- ("hello") is a string so type() returns str as class of var1 i.e. <class 'str'>
- ("hello",) and "hello", both are tuples so type() returns tuple as class of var1 i.e. <class 'tuple'>

## **Access Python Tuple Elements**

Like a list, each element of a tuple is represented by index numbers **(0, 1, ...)** where the first element is at index **0**.

We use the index number to access tuple elements. For example,

### **1. Indexing**

We can use the index operator [] to access an item in a tuple, where the index starts from 0.

So, a tuple having **6** elements will have indices from **0** to **5**. Trying to access an index outside of the tuple index range( **6,7,...** in this example) will raise an IndexError.

The index must be an integer, so we cannot use float or other types. This will result in TypeError.

Likewise, nested tuples are accessed using nested indexing, as shown in the example below.

![](https://lh6.googleusercontent.com/xGGu1J2gKadz556MVL90YTr5DB6uI9gxlWLh6wFE1XEYGRYo92TES65S5x6HKFhbHk4ruc_j46FUtB7FPKd042ngy9nECAS1yQqnyLvQnYSOHnzp9WL3f88IfQkYHzUrXn7r9HWJQeGn9G8EgoY-ntU)

In the above example,

- letters[0] - accesses the first element
- letters[5] - accesses the sixth element

### **2. Negative Indexing**

Python allows negative indexing for its sequences.

The index of **-1** refers to the last item, **-2** to the second last item and so on. For example,

![](https://lh6.googleusercontent.com/wKoChMZimtf9euZfBTAcNSH-mYP8xR2wfmmw5AyM5MraCR1WWKkHVUcgDKSuP_-3ACJxFZhPfDC-u4zhSQgz5hqOkJptb5USbx_VKqAsHoWWg35Rt4GOCF4TbAFN_G_Kezxpw5OOq1DaSECY0983-jE)

In the above example,

- letters[-1] - access last element
- letters[-3] - access third last element

## **Python Tuple Methods**

In Python, methods that add items or remove items are not available with tuples. Only the following two methods are available.

Some examples of Python tuple methods:

![](https://lh6.googleusercontent.com/kNqMhQcZGZ8mscxNDr8daKe2_UGdelZKnHAx_ynpLf-0yAgQrZ9UnhOo9EQurip-K_29FSwYZuPnqXHzu_87SXZzI4uVL5kda7meKZZ9lk0_mDer-wwjWkS1ybyJW3pRUYK_Jd1_hDmWeUGj_0UaajI)

Here,

- my_tuple.count('p') - counts total number of 'p' in my_tuple
- my_tuple.index('l') - returns the first occurrence of 'l' in my_tuple