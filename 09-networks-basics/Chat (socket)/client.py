import socket
import sys
from select import select


host = 'localhost'
port = 5050


class Client:

    def __init__(self):
        self.sock = socket.socket()
        self.name = input("Ваше имя пользователя: ")

    def connect(self, host, port):
        self.sock.connect((host, port))
        print("Для просмотра команд нажмите h. Enter - для отправки сообщения,"
              " q(Q) - чтобы выйти.\n")
        self.mysend(f"{self.name}`welcome_request")
        try:
            print(self.myreceive())
        except ConnectionResetError:
            print('Соединение прервано')
            sys.exit(1)

    def mysend(self, msg):
        msg = msg.encode()
        totalsent = 0
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("Соединение с сервером прервано.")
            totalsent = totalsent + sent
        return totalsent

    def myreceive(self):
        chunk = self.sock.recv(4096).decode()
        chunk = chunk.split('`')
        return ''.join("\r" + chunk[1] + chunk[2])

    @staticmethod
    def prompt():
        sys.stdout.write('Вы: ')
        sys.stdout.flush()

    def disconnect(self, message):
        self.mysend(self.name + '`' + message)
        print('Вы покинули чат.')
        self.sock.close()

    def run(self):
        socket_list = [sys.stdin, self.sock]
        while True:
            self.prompt()
            read_sockets, _, _ = select(socket_list, [], [])
            for sock in read_sockets:
                if sock == self.sock:
                    data = self.myreceive()
                    if not data:
                        print('\nСоединение с сервером прервано')
                        sys.exit(1)
                    else:
                        print(data)
                else:
                    message = sys.stdin.readline().rstrip()
                    if message in ['Q', 'q']:
                        self.disconnect(message)
                        sys.exit(0)
                    else:
                        self.mysend(self.name + '`' + message)


if __name__ == "__main__":
    client = Client()
    client.connect(host, port)
    client.run()
