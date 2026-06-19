
### 2. Use modern commands (preferred way)

- **Show all interfaces + IPs**
    
    
    
    ```bash
    ip addr show
    ```
    
- **Quick IP only**
    
    
    ```bash
    hostname -I
    ```
    
- **Default gateway**
    
    
    ```bash
    ip route
    ```
    
- **Detailed info via NetworkManager**
    
    
    ```bash
    nmcli device show
    ```
    

## ✅ Key Takeaway

- `ifconfig` isn’t installed by default → install `net-tools` if you want it.
    
- Modern Linux uses `ip` and `nmcli` commands, which give more detailed and reliable info.