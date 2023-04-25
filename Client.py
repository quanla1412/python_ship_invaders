import socket


class Client:
    HEADER = 64
    PORT = 5050
    SERVER = "172.20.10.2"
    FORMAT = 'utf-8'

    START_GAME_MESSAGE = 'START'
    DISCONNECT_MESSAGE = 'DISCONNECT'

    def __init__(self, SERVER):
        self.SERVER = SERVER
        self.ADDR = (SERVER, self.PORT)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)

    def send(self, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(msg)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def receive(self):
        msg_length = self.client.recv(self.HEADER).decode(self.FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = self.client.recv(msg_length).decode(self.FORMAT)
            return msg
