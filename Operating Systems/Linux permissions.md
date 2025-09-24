
## Linux File Permissions: The Essentials

### 🧱 1. **Permission Types**

Each file or directory has three types of permissions:

- **Read (**`r`**)** – View contents
    
- **Write (**`w`**)** – Modify contents
    
- **Execute (**`x`**)** – Run as a program or enter a directory
    

### 👥 2. **Permission Categories**

Permissions apply to three user classes:

- **Owner (**`u`**)** – The user who owns the file
    
- **Group (**`g`**)** – Users in the file’s group
    
- **Others (**`o`**)** – Everyone else
    

### 📄 3. **Viewing Permissions**

Use `ls -l` to see permissions:



```bash
ls -l filename.txt
```

Example output:



```Code
-rwxr-xr-- 1 harold devs 1024 Sep 22 10:00 filename.txt
```

Breakdown:

- `-` → Regular file
    
- `rwx` → Owner: read, write, execute
    
- `r-x` → Group: read, execute
    
- `r--` → Others: read only
    

### 🛠️ 4. **Changing Permissions with** `chmod`

#### Symbolic Mode:



```bash
chmod u+x filename.txt     # Add execute for owner
chmod g-w filename.txt     # Remove write for group
chmod o=r filename.txt     # Set read-only for others
```

#### Numeric Mode:

Each permission has a value:

- `r = 4`, `w = 2`, `x = 1`
    

Combine them:



```bash
chmod 755 filename.txt     # rwx for owner, rx for group and others
chmod 644 filename.txt     # rw for owner, r for group and others
```

### 👑 5. **Changing Ownership with** `chown`



```bash
chown harold filename.txt         # Change owner
chown harold:devs filename.txt    # Change owner and group
```

### 📁 6. **Directory Permissions**

- **Read (**`r`**)** – List files
    
- **Write (**`w`**)** – Create/delete files
    
- **Execute (**`x`**)** – Enter the directory
    

Example:



```bash
chmod 700 myfolder     # Only owner can access
```

### 🧠 7. **Special Permission Bits**

|Bit|Symbol|Purpose|
|---|---|---|
|Setuid|`s` on owner|Run file with owner's privileges|
|Setgid|`s` on group|Run with group privileges or inherit group in directories|
|Sticky|`t` on others|Only owner can delete files in shared dir (e.g., `/tmp`)|

Example:



```bash
chmod +t /shared_folder
```

### 🧪 8. **Check Effective Permissions**



```bash
namei -l /path/to/file
```

Shows permissions at each level of the path.