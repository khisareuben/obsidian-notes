# udp_socket

#### 1. server

```python
# importing the socket module
import socket

# creating a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# binding IP and port
server_socket.bind((socket.gethostbyname(socket.gethostname()), 8080))

# we are not listening or accepting any connection since udp is a connenctionless protocol
message, address = server_socket.recvfrom(1024)

print(message.decode("utf-8"))
# printing the address where it came from
print(address)
```


#### 2. client

```python
# import the socket module

import socket

# creating the socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# senging a message
buff = "This is Reuben speaking"
client_socket.sendto(buff.encode("utf-8"), (socket.gethostbyname(socket.gethostname()), 8080))
```


