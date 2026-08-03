Changing wifi adapter name
```zsh
sudo ip link set dev wlxd03745297eda down
sudo ip link set dev wlxd03745297eda name wlan0
sudo ip link set dev wlan0 up

```

Changing the MAC address
```zsh
sudo ip link set dev wlan0 address 50:da:d6:10:87:75

```

if it still cut off 
```zsh
sudo iptables -t mangle -A POSTROUTING -o wlan0 -j TTL --ttl-set 64
//run once after you connect the wifi
```

```
08:B3:39:CA:18:6A
3C:13:5A:E6:61:CD
18:F0:E4:26:1C:35
50:8E:49:BF:57:4B
20:82:C0:7A:95:DA
08:25:25:3F:EE:CA
04:E5:98:ED:E0:0D
50:8F:4C:E1:B3:51
20:3B:34:BC:E1:A4
4C:63:71:21:DA:B7
```