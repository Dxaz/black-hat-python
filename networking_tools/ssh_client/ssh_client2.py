from getpass import getpass
import paramiko
import interactive

def ssh_client(ip, port, user, passwd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, port=port, username=user, password=passwd)

    channel = client.invoke_shell()
    interactive.interactive_shell(channel)

def main():
    hostanme = input('IP: ')
    port = input('Port: ')
    username = input('User: ')
    password = getpass('Enter Password: ')
    ssh_client(hostanme, port, username, password)


if __name__ == '__main__':
    main()