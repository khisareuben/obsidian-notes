# 1. Server side

```python
# importing a socket

import socket

# defining the variables
HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 8080
ENCODER = "utf-8"
BYTESIZE = 1024

# creating a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# binding
server_socket.bind((HOST_IP, HOST_PORT))

# listening
server_socket.listen()
client_socket, client_address = server_socket.accept()
print("A client is connected")
client_socket.send("You are now connected".encode(ENCODER))

# sending/receiving messages
while True:
	# receiving information from the client
	message = client_socket.recv(BYTESIZE).decode(ENCODER)
	
	# Quit if the client wants to quit else display the message
	if message == "quit":
		client_socket.send("quit".encode(ENCODER))
		print("Ending the chat... chaos/goodbye")
		break
	
	else:
	print(f"{message}")
	message = input("Server: ")
	client_socket.send(message.encode(ENCODER))

# closing the socket
server_socket.close()
```


# 2. client side

```python
# importin the module
import socket

# defining the variable
HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 8080
ENCODER = "utf-8"
BYTESIZE = 1024

# creating the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connecting to the server
client_socket.connect((HOST_IP, HOST_PORT))

# sending and receiving the message
while True:

	message = client_socket.recv(BYTESIZE).decode(ENCODER)
	
	# quit if the connected server wants to quit else keep on receiving
	
	if message == "quit":
		client_socket.send("quit".encode(ENCODER))
		print("Ending the chat...chaos/goodbye")
		break
	
	else:
		print(f"\n{message}")
		message = input("Client: ")
		client_socket.send(message.encode(ENCODER))
 
# closing the client socket
client_socket.close()
```