import socket
import threading

import pygame

from Player import Player
from GameModeConstraints import GameModeConstraints
from Message import Message
from PlayerServer import PlayerServer

HEADER = 128
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

START_GAME_MESSAGE = 'START'
DISCONNECT_MESSAGE = 'DISCONNECT'

start_game = False
players = []
amount_player = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def start_game_function(conn, addr):
    global amount_player, players, start_game
    name_player = receive(conn, addr)
    player = PlayerServer(name_player)
    players.append(player)

    amount_player = int(receive(conn, addr))

    while len(players) != amount_player:
        pass

    start_game = True

    send(conn, START_GAME_MESSAGE)
    return player


def finish_game(conn, addr, player):
    global amount_player, players
    score = int(receive(conn, addr))
    player.score = score

    while not check_success():
        pass

    players.sort(key=lambda item: item.score, reverse=True)
    players[0].ranking = 1
    for i in range(1, len(players)):
        players[i].ranking = players[i-1].ranking if players[i].score == players[i-1].score else players[i-1].ranking + 1

    send(conn, str(player.ranking))


def check_success():
    global players

    for player in players:
        if player.score == -1:
            return False
    return True


def handle_client(conn, addr):
    global players, start_game
    player = None

    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True

    if start_game:
        print("Server is full.")
        connected = False

    while connected:
        message = receive(conn, addr)

        if message == Message.START_GAME:
            player = start_game_function(conn, addr)
        elif message == Message.FINISH_GAME:
            finish_game(conn, addr, player)
        elif message == DISCONNECT_MESSAGE:
            connected = False
            start_game = False
            players.clear()
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


print("[STARTING] Server is starting...")
start()
