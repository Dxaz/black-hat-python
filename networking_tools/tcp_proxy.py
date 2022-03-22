'''
ToDo:
    * Make pep-8 compliant
    * Add argparse vs argv
    * Add functionality to request_handler()
    * Add functionality to response_handler()
    * Clean code up somethings are done messy in the book
    * Modulate as needed
'''
import sys
import socket
import threading

ARRAY = [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)]
HEX_FILTER = ''.join(ARRAY)

def hexdump(src, length=16, show=True):
    '''Test'''
    if isinstance(src, bytes):
        src = src.decode()

    results = []

    for i in range(0, len(src), length):
        word = str(src[i:i+length])
        printable = word.translate(HEX_FILTER)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = length*3
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')

    if show:
        for line in results:
            print(line)
        return results

def recieve_from(connection):
    '''Test'''
    buffer = b''
    connection.settimeout(60)
    while True:
        data = connection.recv(4096)
        if not data:
            break
        buffer += data
    return buffer

def request_handler(buffer):
    '''Test'''
    return

def response_handler(buffer):
    '''Test'''
    return

def proxy_handler(client_socket, remote_host, remote_port, recieve_first):
    '''Test'''
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if recieve_first:
        remote_buffer = recieve_from(remote_socket)
        hexdump(remote_buffer)

    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print(f'[<==] Sending {len(remote_buffer)} bytes to localhost.')
        client_socket.send(remote_buffer)

    while True:
        local_buffer = recieve_from(client_socket)
        if len(local_buffer):
            print(f'[==>] Recieved {len(local_buffer)} bytes from localhost.')
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print('[==>] Sent to remote.')

        remote_buffer = recieve_from(remote_socket)
        if len(remote_buffer):
            print(f'[<==] Recieved {len(remote_buffer)} bytes from remote.')
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print('[<==] Sent to localhost.')

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print('[*] No more data. Closing connections.')
            break

def server_loop(local_host, local_port,
                remote_host, remote_port, recieve_first):
    '''Test'''
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((local_host, local_port))

    print(f'[*] Listening on {local_host}:{local_port}')
    server.listen(5)
    while True:
        client_socket, addr = server.accept()
        print(f'> Recieved incoming connection from {addr[0]}:{addr[1]}')

        proxy_thread = threading.Thread(
            target = proxy_handler,
            args=(client_socket, remote_host,
            remote_port, recieve_first))
        proxy_thread.start()

def main():
    '''Test'''
    if len(sys.argv[1:]) != 5:
        print('Usage: ./proxy.py [localhost] [localport]', end='')
        print('[remotehost] [remoteport] [recieve_first]')
        print('Example: ./tcp_proxy.py 127.0.0.1 9000 10.12.132.1 9000 True')
        sys.exit(0)

    local_host = str(sys.argv(1))
    local_port = int(sys.argv(2))
    remote_host = str(sys.argv(3))
    remote_port = int(sys.argv(4))
    recieve_first = bool(sys.argv(5))

    server_loop(local_host, local_port,
                remote_host, remote_port, recieve_first)

if __name__ == '__main__':
    main()
