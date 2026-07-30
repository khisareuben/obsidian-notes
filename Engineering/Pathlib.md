
The `pathlib` module is Python's standard library for handling file system paths using an **object-oriented approach** instead of awkward string manipulation (`os.path`). It treats paths as intelligent concrete objects, automatically managing platform-specific variations (such as Windows `\` backslashes vs. Unix `/` forward slashes) seamlessly under the hood.


---

1. Importing and Core Architecture

Always import the `Path` class, which handles your system's path logic automatically.


```python
from pathlib import Path
```

Use code with caution.

The Class Hierarchy

- **`PurePath`**: Does purely computational path manipulation without making system/network I/O calls.
- **`Path`**: Inherits from `PurePath` and adds concrete system execution actions (reading, writing, creating files/directories).
---

2. Instantiating Paths

```python
# 1. Instantiate via arbitrary path strings
path1 = Path("usr/local/bin")
path2 = Path("usr", "local", "bin")  # Automatically joins segments

# 2. Get Current Working Directory (CWD)
current_dir = Path.cwd()

# 3. Get User Home Directory
home_dir = Path.home()

# 4. Use __file__ for scripts relative to current module execution
script_dir = Path(__file__).resolve().parent
```

Use code with caution.

> [!TIP]  
> Always use `.resolve()` to clean up relative paths, step past double dots (`..`), and evaluate underlying symbolic links. [[1](https://www.youtube.com/watch?v=yxa-DJuuTBI)]

---

3. The Power of the `/` Join Operator

`pathlib` overloads the division operator (`/`) to cleanly mimic typical file paths, replacing `os.path.join()`. 
python

```python
base_dir = Path.home() / "Documents"
project_config = base_dir / "projects" / "config.json"
```

Use code with caution.

---

4. Extracting Path Elements

Given the path object: `p = Path("/home/user/data/sales.csv")`: 

|Property|Description|Output|
|---|---|---|
|`p.name`|Complete filename|`"sales.csv"`|
|`p.stem`|Filename without extension|`"sales"`|
|`p.suffix`|Extension including dot|`".csv"`|
|`p.parent`|Immediate parent directory|`Path("/home/user/data")`|
|`p.anchor`|Root filesystem marker|`"/"` (Unix) or `"C:\"` (Windows)|
|`p.parts`|Individual elements tuple|`('/', 'home', 'user', 'data', 'sales.csv')`|

---

5. File System Introspection

Check attributes of a local file system element without triggering dangerous runtime crashes:

```python
p = Path("data/report.json")

print(p.exists())  # True if target directory/file exists
print(p.is_file()) # True if object points to a file
print(p.is_dir())  # True if object points to a directory
```

Use code with caution.

---

6. Directory Iteration and Pattern Matching

python

```python
docs = Path.home() / "Documents"

# 1. Non-recursive exploration (shallow list)
for item in docs.iterdir():
    if item.is_file():
        print(f"File found: {item.name}")

# 2. Shallow pattern matching (Only .txt inside Documents)
for text_file in docs.glob("*.txt"):
    print(text_file)

# 3. Deep recursive search (Find all .py files in child folders)
for python_file in docs.rglob("*.py"):
    print(python_file)
```

Use code with caution.

---

7. Reading and Writing Files Directly

Skip explicit `open()`, `close()`, or context-manager loops when dealing with lightweight text or binary formats.

```python
notes_file = Path.home() / "todo.txt"

# Direct Text Writing
notes_file.write_text("1. Complete Pathlib tutorial\n2. Update Obsidian Vault")

# Direct Text Reading
content = notes_file.read_text()
print(content)
```

Use code with caution.

---

8. File and Directory Operations

Creating Folders Safely

```python
new_dir = Path.home() / "Workspace" / "python" / "scripts"

# parents=True creates missing parent folders; exist_ok=True prevents crashes if folder exists
new_dir.mkdir(parents=True, exist_ok=True)
```

Use code with caution.

Renaming and Modifying Extensions

```python
old_file = Path("data/raw_metrics.txt")

# 1. Modify the filename entirely
old_file.rename("data/final_metrics.txt")

# 2. Modify only the file suffix extension
new_extension = old_file.with_suffix(".csv")
old_file.rename(new_extension)
```

Use code with caution.

Deleting Elements

```python
target_file = Path("data/temp_log.txt")
target_dir = Path("data/temp_folder")

# Delete file
target_file.unlink(missing_ok=True)

# Delete directory (Folder must be completely empty)
target_dir.rmdir()
```

Use code with caution.

---

🛠️ Quick Comparison: `os.path` vs `pathlib`

|Operation|Legacy `os` Module|Modern `pathlib` Module|
|---|---|---|
|**Join Paths**|`os.path.join(a, b)`|`a / b`|
|**Get CWD**|`os.getcwd()`|`Path.cwd()`|
|**Get Name**|`os.path.basename(path)`|`path.name`|
|**Get Stem**|`os.path.splitext(os.path.basename(p))[0]`|`path.stem`|
|**Make Dirs**|`os.makedirs(path, exist_ok=True)`|`path.mkdir(parents=True, exist_ok=True)`|
|**Test Existence**|`os.path.exists(path)`|`path.exists()`|

---