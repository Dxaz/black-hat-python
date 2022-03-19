import socket
import sys
import threading

IP = '127.0.0.1'
PORT = 4444
SOCKET = IP, PORT

def main():
    try:
        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.bind((SOCKET))
        tcp_server.listen(5)
        print(f'[*] Listening on {IP}:{PORT}')

        while True:
            client, address = tcp_server.accept()
            print(f'[*] Accepted request from {address[0]}:{address[1]}')
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.start()
    except KeyboardInterrupt:
            print('\nUser Terminated')
            tcp_server.close()
            sys.exit()


def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(4096)
        print(f'[*] Recieved: {request.decode("utf-8")}')
        sock.send(b'ACK')


if __name__ == '__main__':
    main()