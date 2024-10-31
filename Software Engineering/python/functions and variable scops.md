
## Functions and variables Scopes

The are 4 scopes of variables that are associated with python functions namely:

- Local scope
- Enclosing scope
- Global scope
- Built-in scope

## Local Scope

- Local scope refers to a variable declared inside a function. For example, in the code below, the variable total is only available to the code within the get_total function. Anything outside of this function will not have access to it.

## ![](https://lh3.googleusercontent.com/ATG31BVKlCnd3rwvGLphn9TQSvtGwKiOIhBo8QYTMViKGnPuZrEd4aGAuSuUm0hzH5c5AmL-WmOpS7-RDw_4RQVZP15naBt1ddN9Vd-lWK222NzdDFR4JWjz_VHjQ1XupWwJ8zk7EgKjvpqPCPXeJ8Y)

## Enclosing scope

- Enclosing scope refers to a function inside another function or what is commonly called a nested function. 
- In the code below, I added a nested function called double_it to the get_total function.
-  As double_it is inside the scope for the add_nums function it can then access the variable. However, the enclosed variable inside the double_it function cannot be accessed from inside the add_nums function.

![](https://lh6.googleusercontent.com/_Ua1gK0n1sLIei3jM8boXkBZBXG5_vDi1fiERcDyhthIMbvablHNSaBheZPBi5cfNNPAkdpRyOs3WQ8JRNIKfkCanD3E-x2onccUsaefHh2ohcbFosHE1Phagcu42CXUMcbkTGrfHiSzl_FsbUEouBE)

### 3. Global scope

Global scope is when a variable is declared outside of a function. This means it can be accessed from anywhere.

In the code below, I added a global variable called global_var. This can then be accessed from both functions add_nums and double_it:

![](https://lh3.googleusercontent.com/0RtNwx5Lmn-M5TvsOaKnSFuSUcUD7Iko7FlffjaeqkxqAzu0qqW1SDiwTnpVYZYcH2UYu4rRY8Gpq_VGylnstuBF6zUwKxOzI3VB9MIm6UyijbFs5mTPpYmQkkOUimqJ_6ZG170VWCMVhB-46Ye71DU)

### 4. Built-in scope

Built-in scope refers to the reserved keywords that Python uses for its built-in functions, such as print, def, for, in, and so forth. Functions with built-in scope can be accessed at any level.