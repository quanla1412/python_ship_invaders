import socket
import threading

import pygame

from Player import Player
from GameModeConstraints import GameModeConstraints

HEADER = 128
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
    if not players:
        return None
    max_score = max([player.score for player in players])
    winner = [player for player in players if player.score == max_score]
    if len(winner) == 1:
        return winner[0]
    else:
        return None


def handle_client(conn, addr):
    global players

    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        name_player = receive(conn, addr)
        players.append(Player(name_player))

        game_mode = int(receive(conn, addr))

        max_players = {
            GameModeConstraints.TWO_PLAYERS: 2,
            GameModeConstraints.THREE_PLAYERS: 3,
            GameModeConstraints.FOUR_PLAYERS: 4,
        }

        while len(players) != max_players[game_mode]:
            pass

        send(conn, START_GAME_MESSAGE)

        score = receive(conn, addr)
        if score != '':
            score = int(score)
        else:
            score = 0
        setScore(name_player, score)
        while not checkSuccess():
            pass
        winner = getWinner()
        if winner is not None and winner.name == name_player:
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
        elif threading.active_count() == 4:
            start_game = True
        elif threading.active_count() == 5:
            start_game = True
        elif threading.active_count() > 5:
            print("Server is full.")


print("[STARTING] Server is starting...")
start()

