import socket
import sys
from select import select


HOST = "localhost"
PORT = 5050
max_users = 10


def create_serversocket():
    """Создание сокета сервера, привязка к порту и хосту"""
    serversocket = socket.socket()
    serversocket.bind((HOST, PORT))
    print(f'Chat server started on port {PORT}.')
    serversocket.listen(max_users)
    return serversocket


def data_processor(message, users_online):
    """Парсинг входящих запросов и формирование ответа на запрос"""
    if message[1] == 'welcome_request':
        nick = '>>>' + message[0]
        context = ' вошел в чат.\n'
        flag = 'wc'
    elif message[1] in ['Q', 'q']:
        nick = '>>>' + message[0]
        context = ' покинул чат.\n'
        flag = 'quit'
    elif message[1] in ['h', 'H']:
        nick = 'Справка по командам:\n'
        context = 'online - посмотреть кто онлайн.\n' \
                  '@nick - отправить личное сообщение участнику.\n'
        flag = 'help'
    elif message[1] == 'online':
        nick = 'Список пользователей онлайн:\n'
        context = '\n'.join(list(users_online.values())) + '\n'
        flag = 'on'
    elif '@' in message[1][0]:
        nick = message[0] + '(Вам)' + ': '
        context = message[1]
        flag = 'personal'
    else:
        nick = message[0] + ': '
        context = message[1]
        flag = 'msg'
    lenght = str(len(context + nick) + 3)
    return lenght, nick, context, flag


def broadcast_processor(data, client, connection_list, users, addr):
    """Рассылка ответов на запрос клиентским сокетам"""
    flag = data[3]
    for socket_ in connection_list:
        if socket_ != serversocket:     #все сокеты кроме сервера
            if flag is 'wc':
                socket_.send(f"{data[0]}`{data[1]}`{data[2]}".encode())
                if socket_ not in users:
                    users[socket_] = data[1][3:]
            elif flag is 'quit':
                if socket_ != client:   #кроме сервера и клиента-отправителя
                    socket_.send(f"{data[0]}`{data[1]}`{data[2]}".encode())
                else:
                    del users[socket_]
                    to_remove = socket_
                    socket_.close()
                    print(f"Client {addr} disconnected")
            elif flag == 'msg':
                if socket_ != client:
                    socket_.send(f"{data[0]}`{data[1]}`{data[2]}".encode())
            elif flag in ['help', 'on']:
                if socket_ == client:
                    socket_.send(f"{data[0]}`{data[1]}`{data[2]}".encode())
                    return
            elif flag == 'personal':
                recipient_nick = data[2].split()[0][1:]
                if recipient_nick in users.values():
                    new_data = " ".join(data[2].split()[1:])
                    for socket, nick in users.items():
                        if nick == recipient_nick:
                            socket_ = socket
                            break
                else:
                    new_data = "Ошибка имени пользователя"
                    socket_ = client
                    nick = ""
                    socket_.send(f"{data[0]}`{nick}`{new_data}".encode())
                    return
                socket_.send(f"{data[0]}`{data[1]}`{new_data}".encode())
                return


def run():
    """Основной цикл обработки запросов и ответов"""
    connection_list = [serversocket]
    users_online = {}
    while True:
        try:
            read_sockets, _, _ = select(connection_list, [], [], 1)
            for sock in read_sockets:
                if sock == serversocket:
                    client, addr = serversocket.accept()
                    connection_list.append(client)
                    print(f"Client {addr} connected")
                    data = client.recv(4096)
                    if data:
                        respond = data_processor(data.decode().split('`'),
                                                 users_online)
                        broadcast_processor(respond,
                                            client,
                                            connection_list,
                                            users_online, addr)
                    else:
                        client.close()
                        connection_list.remove(client)
                        print(f"Connection with {addr} closed")
                else:
                    data = sock.recv(4096)
                    if data:
                        respond = data_processor(data.decode().split('`'),
                                                 users_online)
                        broadcast_processor(respond,
                                            sock,
                                            connection_list,
                                            users_online, addr)
        except KeyboardInterrupt:
            serversocket.close()
            sys.exit(0)


if __name__ == "__main__":
    serversocket = create_serversocket()
    run()
