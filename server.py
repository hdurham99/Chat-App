import select
import socket
import threading
import time

from random import randint

from common import *

SOCKET_LIST = []

conns_dict = {}


class Server(Yummy):
    def __init__(self):
        super().__init__()

    def listen(self):
        self.sock.bind(ADDR)
        self.sock.listen()
        while True:
            conn, addr = self.sock.accept()
            thread = threading.Thread(target=self.handle_connection, args=(conn, addr))
            thread.start()

    def create_id(self):
        r = -1
        x = 2
        while r < 1 or str(r) in conns_dict:
            r = randint(0, x)
            x *= 2
        return str(r)

    def send_list(self):
        for person in conns_dict:
            tmp = ''
            for key in conns_dict:
                if key != person:
                    tmp += str(key) + '\n'
            if tmp != '':
                self.send(f'Available connections as IDs:\n{tmp}', conns_dict[person])

    def handle_connection(self, conn, addr=None):
        print(f"[NEW CONNECTIONS] {addr} connected.")
        conn_id = self.create_id()
        conns_dict[conn_id] = conn
        print(f'[ID GENERATED]: {conn_id} for {addr}')
        self.send(f'Your ID is {conn_id}.', conn)
        self.send_list()
        talking_to = []
        while True:
            try:
                message = receive(conn)
            except ConnectionResetError:
                break
            if message:
                if message == DISCONNECT_MESSAGE:
                    try:
                        send(DISCONNECT_MESSAGE, conn)
                        del conns_dict[conn_id]
                        print(f'[CONNECTION REMOVED]: {conn_id}')
                        conn.close()
                    except:
                        'placeholder'
                    break
                if len(talking_to) == 0:
                    if message in conns_dict:
                        talking_to.append(conns_dict[message])
                        self.send(f'You are now talking in/to ID {message}.', conn)
                    else:
                        if message == 'help':
                            self.send(DISCONNECT_MESSAGE, conn)
                        else:
                            self.send(message, conn)
                else:
                    for person in talking_to:
                        self.send(f'[{conn_id}]:\t{message}', person)


if __name__ == '__main__':
    print("Welcome! Server is starting now!")
    # start()
    Server()
