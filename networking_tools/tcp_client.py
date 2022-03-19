import socket

# Define variables
ip = "127.0.0.1"
port = 4444
SOCKET = ip, port
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create a socket
tcp_client.connect((SOCKET))

# Send some data
tcp_client.send(b'Yo\n')

# Recieve some data
response = tcp_client.recv(4096)

# Print response and close
print(response.decode())
tcp_client.close()
