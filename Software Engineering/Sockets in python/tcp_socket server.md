# tcp_socket server

```python
# importing the socket module
import socket

# socket creation
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# see how to get the IP address dynamically
print(socket.gethostname())
print(socket.gethostbyname(socket.gethostname()))

# binding the IP and Port to the server
server_socket.bind((socket.gethostbyname(socket.gethostname()), 8080))

# listening at the port
server_socket.listen()

# accepting the connection from the client
while True:
	client_socket, client_address = server_socket.accept()
	print(f"connected to {client_address}\n")
	buff = "You are now connected"
	client_socket.send(buff.encode("utf-8"))

	# closing the socket
	server_socket.close()

```

#### client socket

```python
# importing the socket module
import socket

# creating a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connecting to the server socket
client_socket.connect((socket.gethostbyname(socket.gethostname()), 8080))
print("connected to the server")

# receiving message from the server socket
message = client_socket.recv(1024)
print(message.decode("utf-8"))

#close the client socket
client_socket.close()
```