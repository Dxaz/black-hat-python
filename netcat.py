import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

class NetCat():
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)

        try:
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                if response:
                    print(response)
                    buffer = input('BHP #> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print('\r\nUser terminated session.')
            self.socket.close()
            sys.exit()

    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        print(f'[*] Listening on {self.args.target}:{self.args.port}')
        try:
            while True:
                client_socket, address = self.socket.accept()
                print(f'[*] Accepted request from {address[0]}:{address[1]}')
                client_thread = threading.Thread(
                    target=self.handle, args=(client_socket,),
                    daemon=True
                )
                client_thread.start()
        except KeyboardInterrupt:
            print('\r\nSIGINT recieved. Server killed!')
            self.socket.close()
            sys.exit()

    def handle(self, client_socket):
        with client_socket as sock:
            if self.args.execute:
                command = execute(self.args.execute)
                sock.send(command.encode())

            elif self.args.upload:
                file_buffer = b''
                while True:
                    data = sock.recv(4096)
                    if data:
                        file_buffer += data
                    else:
                        break

                with open(self.args.upload, 'wb') as f:
                    f.write(file_buffer)
                message = f'Saved file {self.args.upload}'
                sock.send(message.encode())

            elif self.args.command:
                cmd_buffer = b''
                while True:
                    try:
                        sock.send(b'\r')
                        while '\n' not in cmd_buffer.decode():
                            cmd_buffer += sock.recv(64)
                        response = execute(cmd_buffer.decode())
                        if response:
                            sock.send(response.encode())
                        cmd_buffer = b''
                    except Exception as exception:
                        print(f'\r\nserver killed {exception}')
                        self.socket.close()
                        sys.exit()


def execute(cmd):
    cmd = cmd.strip()
    if cmd:
        output = subprocess.check_output(shlex.split(cmd),
                                    stderr = subprocess.STDOUT)
        return output.decode()
    return None

def main():
    try:
        if args.listen:
            buffer = ''
        else:
            buffer = sys.stdin.read()

        nc = NetCat(args, buffer.encode())
        nc.run()
    except KeyboardInterrupt:
        print('\r\nNo session created. User terminated session.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=lambda prog: argparse.RawDescriptionHelpFormatter(prog,
            max_help_position=35),
        epilog=textwrap.dedent('''Example:
            netcat.py -t 127.0.0.1 -p 5555 -l -c                        # command shell
            netcat.py -t 127.0.0.1 -p 5555 -l -u=mytest.txt             # upload a file
            netcat.py -t 127.0.0.1 -p 5555 -l -e=\"cat /etc/passwd\"      # execute command
            echo 'ABC' | ./netcat.py -t 127.0.0.1 -p 135                # echo text to server port 135
            netcat.py -t 127.0.0.1 -p 5555                              # connect to server
        '''))
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='0.0.0.0', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')

    args = parser.parse_args()
    main()
