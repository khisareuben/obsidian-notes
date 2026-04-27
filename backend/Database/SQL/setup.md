
# Correct MySQL Installation and Setup on Ubuntu 24.04 LTS

This guide provides a complete and accurate process to install, configure, and prepare MySQL for use on Ubuntu 24.04 LTS.

---

## 1. Update System Packages

```
sudo apt update && sudo apt upgrade -y
```

---

## 2. Install MySQL Server

```
sudo apt install mysql-server -y
```

This installs the latest MySQL server available in Ubuntu repositories.

---

## 3. Verify MySQL Service

Check if MySQL is running:

```
systemctl status mysql
```

If not running, start and enable it:

```
sudo systemctl start mysql
sudo systemctl enable mysql
```

---

## 4. Secure MySQL Installation

Run the security script:

```
sudo mysql_secure_installation
```

On Ubuntu 24.04, this script focuses on removing insecure defaults:

- Remove anonymous users
    
- Disallow remote root login
    
- Remove test database
    
- Reload privilege tables
    

**Note:** It no longer prompts for a root password because MySQL uses the `auth_socket` plugin by default.

---

## 5. Set Root Password (Manual)

To set a root password, log in with sudo:

```
sudo mysql
```

Then run:

```
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'NewPassword';
FLUSH PRIVILEGES;
```

Replace `NewPassword` with your chosen password.

Exit:

```
EXIT;
```

---

## 6. Log In to MySQL

```
mysql -u root -p
```

Enter the root password you set.

---

## 7. Create a New Database

```
CREATE DATABASE example_db;
```

---

## 8. Create a New User

```
CREATE USER 'example_user'@'localhost' IDENTIFIED BY 'password';
```

---

## 9. Grant Privileges to User

```
GRANT ALL PRIVILEGES ON example_db.* TO 'example_user'@'localhost';
FLUSH PRIVILEGES;
```

---

## 10. Test Database and User

Log in with the new user:

```
mysql -u example_user -p
```

Then select the database:

```
USE example_db;
```

---

## 11. Check MySQL Version

```
mysql --version
```

---

# Summary

By following these steps, you have:

- Installed MySQL Server
    
- Secured the installation
    
- Configured root access with a password
    
- Created a new database and user
    
- Granted privileges
    
- Verified functionality
    

Your MySQL setup is now complete and ready for use in applications or development.