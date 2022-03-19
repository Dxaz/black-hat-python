import socket

ip = '127.0.0.1'
port = 4444
SOCKET = ip, port
udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udp_client.sendto(b'Yo\r\n', (SOCKET))

__data, _ = udp_client.recvfrom(4096)

print(__data.decode('utf-8'))
udp_client.close()
