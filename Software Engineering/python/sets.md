
In Python, we create sets by placing all the elements inside curly braces {}, separated by comma.

A set can have any number of items and they may be of different types (integer, float, tuple, string etc.). But a set cannot have mutable elements like lists, sets or dictionaries as its elements.

Let's see an example,

![](https://lh5.googleusercontent.com/doh9D6aXyAmbungECNZQ_2YtAfWz0dCBpYyZ_k7F0RDl7PgruHO25jHwBsNhe6LMIJrba7eTd4LGEfydE9LXwpGwos4XknOnQeTw00bZrUprQU7rDD4-ivA6gx5CPoTIkhdDM_WfwS3Ggp-hk5cHB1s)

In the above example, we have created different types of sets by placing all the elements inside the curly braces {}.

**Note:** When you run this code, you might get output in a different order. This is because the set has no particular order.

## **Create an Empty Set in Python**

Creating an empty set is a bit tricky. Empty curly braces {} will make an empty dictionary in Python.

To make a set without any elements, we use the set() function without any argument.

For example,

![](https://lh5.googleusercontent.com/M_hd_VULL-jHXuMu07_DTwTqJudFJEthI6HfUrNwCowYxoKOjHny1XpYoppN9Vr658WrlcWbYHHp_hfza2TDKc54546h9hCEwBRCiK4vPlXa5uWEUHsc_6M45RSHjc9R7HCF-ARo0IL7mp1P-JkeWmw)

Here,

- empty_set - an empty set created using set()
- empty_dictionary - an empty dictionary created using {}

Finally we have used the type() function to know which class empty_set and empty_dictionary belong to.

## **Duplicate Items in a Set**

Let's see what will happen if we try to include duplicate items in a set.

![](https://lh5.googleusercontent.com/QF0OrLLcXURxsHNzIiRVvY0GsdC9DeyPS72-7F61Bbrp4NlGhkVWq2uQfo9ngc47cnjAK8yFwEPLhQtKuD31fDW5lUwYFUSmtnXeSU06eF4Q7MnFq7nRd5FTHpQCu5GwvFf6mVcYoCxctAXG5O0shbM)

Here, we can see there are no duplicate items in the set as a set cannot contain duplicates.

## **Add and Update Set Items in Python**

Sets are mutable. However, since they are unordered, indexing has no meaning.

We cannot access or change an element of a set using indexing or slicing. Set data type does not support it.

### **Add Items to a Set in Python**

In Python, we use the add() method to add an item to a set. For example,

![](https://lh4.googleusercontent.com/1rgBFEUkoEo2y-TaLqUyjn0KEcIukNqZ9KOGlkB35KKOnERX5e8N1iN_E37_nU0waCPObMw0Cg7tRsK_-WJnLyOu4IfemW2qJIO-ZRpJrHmzrvggS4YH3h60CkM84KsZ5f3rRIDah7jWIsFNLJ9UzO4)

In the above example, we have created a set named numbers. Notice the line,

![](https://lh4.googleusercontent.com/r4hews_qv78D4EAtr9qtBaKWhfO_9Ywcgx6sNYrRoK5uFJrmHRUWKH26tjuBLMhKLEUk5Iv88ok5BabYQlzlOjwsEZprSQQUolhlqWnLSwB_PCTDH-L4ZFDzvba7E1IPzaMtwJR0EypMBoZRujDNnog)

Here, add() adds **32** to our set.

### **Update Python Set**

The update() method is used to update the set with items other collection types (lists, tuples, sets, etc).

For example,

![](https://lh5.googleusercontent.com/lBbyAKh8KeWzuHxyIrl_tTC9hfM93Fke9ATWJ-EohZafKuLdjB0ADSn3RUD8ukaGayVybpOE_bJjQ_XCjTTHePgmEqQTBi-ikk8O6fGUDfQmYUuTg-GE8mdyWvHbYIeEr0i1jzZvr_8VxZk3l4Met9k)

Here, all the unique elements of tech_companies are added to the company's set.

## **Remove an Element from a Set**

We use the discard() method to remove the specified element from a set.

For example,

![](https://lh3.googleusercontent.com/doDj9X9S_CGmk535cO1zVNWf0mL109pQLjcKbR2tH-_WLYuz7r4WMcDbIdhKe8Zm0JRqO18VarUW09yIM81weKH7p4cVV8d83nau6mJmgQiC3l0zrezUCLy_YEMKMZLWDJQ7wxO4AdU0m7R94AoMgAQ)

Here, we have used the discard() method to remove 'Java' from the languages set.

## **Built-in Functions with Set**

Built-in functions like all(), any(), enumerate(), len(), max(), min(), sorted(), sum() etc. are commonly used with sets to perform different tasks.

![](https://lh4.googleusercontent.com/-dekJ6uAIP0cvIWui-ivtntHMBt9lQkTPXo-WFviq878OFovgr3pVl3vDOgwrXzzPxWJlPwGcdDZ8UjkBUPjSLPUXP5DPN61fqi39S6TV8pV8rnqlPHVsMbiiI1LlXm5Bby3YFH6a5qrVT3jp5JkyIw)

## **Iterate Over a Set in Python**

**![](https://lh4.googleusercontent.com/3ASeQMlQlOCMeXWSlNJ4omF-GGnuCVx3aNE7r6eR7nEEVn9C4t8-Y7fRgNQVrbEKDGALWydLA2tXjHY315FIZiS7AY3k0LynnFKYEjRfmocaAovNCcAhzJCGBv8Iw5-Njx9iMPruTnWNtqMsYITjUbc)**

## **Find Number of Set Elements**

We can use the len() method to find the number of elements present in a Set.

For example,

![](https://lh6.googleusercontent.com/dmWT8g1ZUZalJKTqrrT6TImArLWHh0QK8Es4uxsp8fi1rT4BmrXng7hVZMQucywQ-mCur7uJ0Rjy2Ir0JCfQNGlm2s5MSFoC___KG4Rw2s_KpE3tVI-cupB2m7Kd2lEek0o1aDJhhvf5_vDSfvdtChY)

Here, we have used the len() method to find the number of elements present in a Set.

## **Python Set Operations**

Python Set provides different built-in methods to perform mathematical set operations like union, intersection, subtraction, and symmetric difference.

## **Union of Two Sets**

The union of two sets **A** and **B** include all the elements of set **A** and **B**.

![](https://lh5.googleusercontent.com/xtP2C0wgO7FoCftyZbUSCa4vRj2Ixo96RNTUyb6l8UVJoX2TJyIG3nb5YSMhyj0qnGRi3QfQSIxatA7f3N7ykoUYWipZSzVT8BUnuulCvWD5HsRJCJDw3xb-6GCa5wbMn6d-XLEuEXEDuzOgJho3w0I)

Set Union in Python

We use the | operator or the union() method to perform the set union operation.

For example,

![](https://lh5.googleusercontent.com/jkOKx1SYeeJNKWWYBEoyF62BcS1nd4nIiTRrhZUIcotap5u_5hbF6d19nFxB1--f3UbLcCNOy9GepLfb5E2ui5cpUlxp2ntBLX3OJy6hZBzgQqv12btEzHBmqEY8yD_7X1f2JrB4JCWcxhZo6AB2J_Q)

**Note**: A|B and union() is equivalent to A ⋃ B set operation.

## **Set Intersection**

The intersection of two sets **A** and **B** include the common elements between set **A** and **B**.

![](https://lh5.googleusercontent.com/JnzQOI6r-MX7IOD0JCU7vrJnYgB-fJ8otNEsaxtvuubcbpsr1_UQPp5wMGcbtxeTdf25y6trXk5UurXgnwEDkuFRp3v4M-cvP9bhUhLw31L4ScLKAL9tGRPoQgB74LVKkErGzXyYcV1zY2t_c-GCQC8)

Set Intersection in Python

In Python, we use the & operator or the intersection() method to perform the set intersection operation.

For example,

![](https://lh6.googleusercontent.com/xDgs8PlNIH3pCd_KXpnQo1WWyNLhVxM-OgL9vMRQVXkGvwrmQgtJGimlmAgs78Hs0Sd1rG-_9NDZI3tK3d8DsW67-fJ3VJOviW929xEjdGz8dvcuy3yC7v-mIQ0rpWBc2_MThNEmJ0ordQEuyzdQ6gw)

**Note**: A&B and intersection() is equivalent to A ⋂ B set operation.

## **Difference between Two Sets**

The difference between two sets **A** and **B** include elements of set **A** that are not present on set **B**.

![](https://lh6.googleusercontent.com/h_9mG46QI9GGILZgZfpc-Nrgz2OnUWNpKsOAYtdhBXMhqA7ImbSih-ZQpxgnrv1DZhd4emL96e44wfCTomPY0enx-ePEU27gqebeYHS061ZCbhfpKxCIMXXoKh8nR-s06E_W9-gE1bpL1XBPEjGjN5c)

Set Difference in Python

We use the - operator or the difference() method to perform the difference between two sets.

For example,

![](https://lh6.googleusercontent.com/xeP03O8-WiP-weh-57F8vDkfxhOrdhq7JMScepKgb0qWE732ZHK9tX-8haq9EHB_DJSB46q5-zdcDXngP0_uZUf7tJTgM95v4ZpxTqZD-eAxyGjowxRBptciJlcS-0XdCGBSt3zwQ10kEYLSw7M7fr4)

**Note**: A - B and A.difference(B) is equivalent to A - B set operation.

## **Set Symmetric Difference**

The symmetric difference between two sets **A** and **B** includes all elements of **A** and **B** without the common elements.

![](https://lh6.googleusercontent.com/6AwqF9TgsJ_azCAkl_WF_hm1tpFoC-60QtCwe0yY8Z6uQ1rw0Q7D4K4IJNzXzA7PiZVita3OhEaTq0zG7peLlt6kbwzYXiZe7CjYKpYRLWxix0QmHQhoQEeYhAVdbqszNnfoD5nAUitw3QvrO_svjuo)

Set Symmetric Difference in Python

In Python, we use the ^ operator or the symmetric_difference() method to perform symmetric difference between two sets.

For example,

![](https://lh6.googleusercontent.com/wMxqzeUhM5LqwiWf5_AOULJbH4ACAHYhwZQWV7xzKegc0DG9EeG6uS1kA6iLYRso3PhdAGrBv8jVALEL8eht9OK3Mq4TAYcsEDwJ7DDx9SeMO0suPRMpWMUFrnySS8Y_xvBemB5mCne2wI3ac9fT4WI)

## **Check if two sets are equal**

We can use the == operator to check whether two sets are equal or not.

For example,

![](https://lh4.googleusercontent.com/qTqhXhjo5HZkG-EtbVWGIsyO-_RZQxdXNEZCh5IFFIXXa_Isl0mUHUIRzI9J4g3sM2bpdxveO5_3Tr0to4F_bLDljgp2MqvtOZUoUrl59uADq5xYsvsQ0MGgfh3lLlEVu-SvSERW6Wl2-Bohir-LOAQ)

In the above example, A and B have the same elements, so the condition

![](https://lh3.googleusercontent.com/BHIL0cpyxjqVU51d2Cx5ah7cQRVI2wppMqDJMndBN5aSccENh4BqkPx9PHyt1r6qW0T6IjsyhQj8fM1kgxwKHT0W5LME7S9nMC3A_FiGi8ZGH0He9W3cEaRZThg9ATKF9aGqIeNgpLAn5ScMqsue_9Q)

evaluates to True. Hence, the statement print('Set A and Set B are equal') inside the if is executed.

## **Other Python Set Methods**

There are many set methods, some of which we have already used above. Here is a list of all the methods that are available with the set objects:

![](https://lh6.googleusercontent.com/n5vdahw4Sjx6W-_SCPGSkpOlNrCMxjLj7GvAj5PARY1cwIMGmkTt8d7VoHZUMpIJwoVp0zjMCgj2actdcNG2po1nIqUw_DLHCsP8Iy1_CPVvoqhLTJ0irlJWomrTH2URxNBsyJmBnfl0YFeSiDVRCG8)

![](https://lh5.googleusercontent.com/nMEvX4blQ1nmjcq7mJHQCOCkwHiSauJlz7dwtyOkTTODgZcCwyN0uqio8en1LWa4b97WB1lV2YYdit-X2m0_RtOi6jyaGZ7LrPjPzlizxPEbNKZ_29TvsV8YSRFEhvqsG4jFYc8XiQ7PGSRGQXTd8Oo)