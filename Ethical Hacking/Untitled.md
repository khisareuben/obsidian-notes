
## 💀 Evil Limiter: Installation & Usage

Evil Limiter is a command-line tool that allows you to scan your network and limit or block the bandwidth of connected devices using ARP spoofing. It is ideal for the temporary blocking you require [](https://github.com/mie-kali/Evillimiter)[](https://rutube.ru/video/249697bbbe6965e474785ebd9588cbca/).

### System Requirements

- A **Linux** distribution.
    
- **Python 3** or greater [](https://github.com/mie-kali/Evillimiter).
    

### Installation Steps

Open a terminal and run the following commands:

bash

# 1. Clone the repository from GitHub
`git clone https://github.com/bitbrute/evillimiter.git`
# 2. Navigate into the tool's directory
`cd evillimiter`
# 3. Run the installation script (requires sudo)
`sudo python3 setup.py install`

Once the installation is complete, you can start the tool by simply typing `sudo evillimiter` in your terminal [](https://cocalc.com/github/bitbrute/evillimiter/blob/master/README.md)[](https://rutube.ru/video/249697bbbe6965e474785ebd9588cbca/).

### How to Use Evil Limiter

After starting the tool with `sudo evillimiter`, you will be in its interactive command-line interface. Here are the essential commands you need:

#### 1. Discover Devices (Scan)

The first thing you must do is scan your network to find connected devices.

```
scan
```


This command will list all active hosts on your network [](https://cocalc.com/github/bitbrute/evillimiter/blob/master/README.md)[](https://deepwiki.com/bitbrute/evillimiter/4-command-reference).

#### 2. View Hosts

After a scan, use this command to display a table of found devices. Each device will have an **ID number** that you will use to control it.

```
hosts
```

#### 3. Block a Device

To completely cut off a device's internet access, use the `block` command followed by its ID number. You can block multiple devices at once by separating IDs with commas.


```
block 1
block 2,3,4
block all
```

#### 4. Unblock a Device

To restore internet access to a device you previously blocked, use the `free` command.


```
free 1
free 2,3,4
free all
```

#### 5. Limit Bandwidth (Optional)

If you want to slow down a device instead of fully blocking it, use the `limit` command with a speed (e.g., `100kbit` for 100 kilobits per second).

text

```
limit 5 100kbit
```

#### 6. Exit the Tool

When you are finished, type `quit` to close Evil Limiter. **Important:** All blocks and limits will be removed once you quit the tool [](https://cocalc.com/github/bitbrute/evillimiter/blob/master/README.md).