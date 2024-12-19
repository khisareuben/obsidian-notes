
```python
# Get the length of a list, string, or other collection
length = len(my_list)

# Convert a string to uppercase
uppercase_text = my_string.upper()

# Convert a string to lowercase
lowercase_text = my_string.lower()

# Remove whitespace from the beginning and end of a string
stripped_text = my_string.strip()

# Split a string into a list of substrings
split_text = my_string.split()

# Join a list of strings into a single string with a specified delimiter
joined_text = ", ".join(my_list)

# Check if a string contains only digits
is_digits = my_string.isdigit()

# Replace a substring with another substring
replaced_text = my_string.replace("old", "new")

# Find the index of a substring
index = my_string.find("search")

# Add an element to the end of a list
my_list.append("new_element")

# Remove and return an element from a list by index
element = my_list.pop(index)

# Sort the elements of a list in ascending order
my_list.sort()

# Reverse the elements of a list
my_list.reverse()

# Get a copy of a list in reverse order
reversed_list = my_list[::-1]

# Check if a key is in a dictionary
is_key_in_dict = "key" in my_dict

# Get a value from a dictionary with a default if the key does not exist
value = my_dict.get("key", "default_value")

# Add a key-value pair to a dictionary
my_dict["new_key"] = "new_value"

```


### Using `termcolor`

`termcolor` is another library that provides colored terminal text.

1. **Install** `termcolor`:
    
    sh
    
    ```
    pip install termcolor
    ```
    
2. **Example Code**:
    
    python
    
    ```
    from termcolor import colored
    
    # Print colored text
    print(colored("This line is red", "red"))
    print("This line is default color")
    ```