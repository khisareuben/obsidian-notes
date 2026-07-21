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