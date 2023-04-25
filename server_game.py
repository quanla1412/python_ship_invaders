import socket
import threading

from Player import Player

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

START_GAME_MESSAGE = 'START'
DISCONNECT_MESSAGE = 'DISCONNECT'

start_game = False
players = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def checkSuccess():
    global players

    for player in players:
        if player.score == -1:
            return False
    return True


def setScore(name: str, score: int):
    global players

    for player in players:
        if player.name == name:
            player.score = score


def getWinner():
    global players

    for player in players:
        if player.score == max(players[0].score, players[1].score):
            return player


def handle_client(conn, addr):
    global players

    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        name_player = receive(conn, addr)
        players.append(Player(name_player))

        while len(players) != 2:
            pass

        send(conn, START_GAME_MESSAGE)

        score = int(receive(conn, addr))
        setScore(name_player, score)
        while not checkSuccess():
            pass

        if getWinner().name == name_player:
            send(conn, "You win!")
        else:
            send(conn, "You lose!")

        players.clear()

        msg = receive(conn, addr)
        if msg == DISCONNECT_MESSAGE:
            connected = False
    conn.close()


def receive(conn, addr):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    msg = ""
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)

        print(f"[{addr}] {msg}")
    return msg

def send(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


def start():
    global start_game

    server.listen()
    print(f'[LISTENING] Server is listening on {SERVER}')
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        if threading.active_count() == 3:
            start_game = True


print("[STARTING] Server is starting...")
start()

