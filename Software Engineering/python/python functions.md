
### Python Functions

Python function is a modular piece of code that can be used repeatedly. Generally a function is a block of code which is executed when it is called from somewhere in the program. A function has a return value.

Functions are perfect for abstraction. They allow us to write blocks of code which can be reused in different ways and in different programs.

# **Function Syntax:**

![](https://lh5.googleusercontent.com/7sB8ud3rV7zffrRsN7JXJqiVt7CYyWNe9nw4ZI2tAKPXjTXWRtntVzZL8-CFrLnYgysxfDelVB7FuSXPHUL3P6EQdourl-jACq2_ppq3lXDNDnruc_uIb31Q867R3ZB9mgdEyWfTt0XStMdwNzglqF8)

# **Creating a Function**

Lets create a function add_nums that adds two numbers.

In Python a function is defined using the def keyword:

![](https://lh5.googleusercontent.com/b3Jaf9dj7-jUG2u7jYdwh6pYZy1REQPXxoXTwkZadbPLR21KCbJbMSX_8XkK4inzg-cOUBiTOVu1XerarMkoCsqqnjPwncufN_KaVr6sTr_V6rkBCNsUWoHBEexqxtKFHpi5PGSCNig6NhVL07jixQs)

# **Calling a Function**

To get the function (add_nums) output, you must call it. To call a function, use the function name followed by parenthesis:

![](https://lh5.googleusercontent.com/-3E3vbx1UCuR6Num6BtTBN9P_EHZGp4Mp6LvClxDnZYk18aHns0ODN5a8MmgmMvUkcchSJPyRyMOhezXo9FY9TXMMyi5hMc4NAAtHatregnXgtlmcMJbL_kJ-HqQxjTNqtVuCE6nT2jDNg4OmKt8zj4)

# **Function Arguments/ Parameters**

Information can be passed into functions as arguments. Arguments make our functions more dynamic and reusables.

Arguments are specified after the function name, inside the parentheses. You can add as many arguments as you want, just separate them with a comma.

![](https://lh5.googleusercontent.com/MkJ5Z60jrjfcgQDN_k8yR7twZyonU8_o_turgE2oQlVcuod9BjJDOxYDkbngR3HW2ToPbOXLo2ZGldcHMT_ZOBD9J6oDPCX52GvJVchGa1TMZcFK1zzy8jspx-qaPVyBi9iYmx0D8Ns-_ebjH11jDLo)

# ***args and **kwargs**

## **Arbitrary Arguments, *args**

If you do not know how many arguments that will be passed into your function, add a * before the parameter name in the function definition.

This way the function will receive a _tuple_ of arguments, and can access the items accordingly:

Lets see our above example, when number of arguments is unknown

![](https://lh4.googleusercontent.com/ovjYAwYf6rWr0bn4F6qYW5o7lXzHUw16AHajg2INiiuJmO-5-9oX5l0f8yEPSHuig5QS4pgrsH2y9txYdj3B0jksiwsFzkVtmLRUUipPhVZjAmW8Id7klrcuNXqigv5nK7SCgMA8jXXJQTQylHJ-wxM)

## **Arbitrary Keyword Arguments, **kwargs**

If the keyword arguments to be passed in a function are not known, you should add ** before the parameter name in the function definition. Example: **age

Example below demonstrates a function add_age() taking kwargs **age to calculate the sum of different people's ages.