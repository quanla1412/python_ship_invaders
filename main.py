
import random
import sys

import pygame
from pygame import mixer
import pygame_gui
import re

from Enemy import Enemy
from Bullet import Bullet
from Message import Message
from Player import Player
from ThienThach import ThienThach
from GameModeConstraints import GameModeConstraints
from Client import Client

pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.Font(None, 36)
background = pygame.image.load('resources/images/background.png')

# Kích thước của hình chữ nhật
rect_width = 50
rect_height = 50

# Tạo hình chữ nhật
rect = pygame.Rect(0, 0, rect_width, rect_height)

# Đặt tọa độ cho hình chữ nhật
rect.x = 740 # Tọa độ x
rect.y = 5 # Tọa độ y

pygame.mixer.music.load("resources/sounds/background.wav")
volumeImg = pygame.image.load('resources/images/mute.png')
# pygame.mixer.music.play(-1)
music_playing = False
explosionSound = mixer.Sound("resources/sounds/explosion.wav")
bulletSound = mixer.Sound("resources/sounds/laser.wav")

pygame.display.set_caption("Space Invader")
icon = pygame.image.load('resources/images/ufo-flying.png')
pygame.display.set_icon(icon)


def khoiTaoEnemy():
    enemy = []
    num_of_enemies = 6
    for i in range(num_of_enemies):
        enemyTam = Enemy(pygame.image.load('resources/images/final-boss.png'), random.randint(0, 736), random.randint(50, 150), 4, 40)
        enemy.append(enemyTam)
    return enemy

def khoiTaoThienThach():
    # khoi tao thien thach
    thienThach = []
    num_of_meteorite = 2

    for i in range(num_of_meteorite):
        thienThachTam = ThienThach(pygame.image.load('resources/images/meteorite.png'), random.randint(0, 480), 0, 2)
        thienThach.append(thienThachTam)
    return thienThach


score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)

#Configure game
SERVER = ""
game_mode = 1
client = None


# start
def start_screen(screen):
    global game_mode, SERVER, volumeImg, music_playing

    manager = pygame_gui.UIManager((800, 600))

    # Create input
    playerNameEntry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((800 / 2 - 100, 600 / 2 - 70), (200, 50)),
        manager=manager,
        placeholder_text="Type your name"
    )
    ipEntry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((800 / 2 - 100, 600 / 2 - 20), (200, 50)),
        manager=manager,
        placeholder_text="Type IP"
    )

    # Create start button
    buttonPractice = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((800 / 2 - 75, 600 / 2 + 30), (150, 50)),
        text="Practice",
        manager=manager,
    )

    buttonCompete = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((800 / 2 - 75, 600 / 2 + 80), (150, 50)),
        text="2 Players",
        manager=manager,
    )

    buttonThreePlayer = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((800 / 2 - 75, 600 / 2 + 130), (150, 50)),
        text="3 Players",
        manager=manager,
    )

    buttonFourPlayer = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((800 / 2 - 75, 600 / 2 + 180), (150, 50)),
        text="4 Players",
        manager=manager,
    )
    # Create clock to control frame rate
    clock = pygame.time.Clock()

    while True:

        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Kiểm tra xem click vào hình chữ nhật chứa biểu tượng loa hay không
                if rect.collidepoint(event.pos):
                    # Nếu đang phát âm thanh, tạm ngừng phát
                    if not music_playing:
                        volumeImg = pygame.image.load('resources/images/volume-up.png')
                        pygame.mixer.music.play(-1)
                        music_playing = True
                    else:
                        pygame.mixer.music.stop()
                        volumeImg = pygame.image.load('resources/images/mute.png')
                        music_playing = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == buttonPractice:
                    game_mode = GameModeConstraints.PRACTICE
                    if playerNameEntry.text == "":
                        playerNameEntry.focus()
                        ipEntry.unfocus()
                    else:
                        return startGame(playerNameEntry.text.strip())
                else:
                    if event.ui_element == buttonCompete:
                        game_mode = GameModeConstraints.TWO_PLAYERS
                    elif event.ui_element == buttonThreePlayer:
                        game_mode = GameModeConstraints.THREE_PLAYERS
                    elif event.ui_element == buttonFourPlayer:
                        game_mode = GameModeConstraints.FOUR_PLAYERS

                    if playerNameEntry.text == "":
                        playerNameEntry.focus()
                        ipEntry.unfocus()
                    elif ipEntry.text == "":
                        playerNameEntry.unfocus()
                        ipEntry.focus()
                    else:
                        txt = ipEntry.text
                        x = re.search(
                            "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
                            txt)
                        if not x:
                            playerNameEntry.unfocus()
                            ipEntry.focus()
                        else:
                            SERVER = txt
                            print(SERVER)
                            return startGame(playerNameEntry.text.strip())
            manager.process_events(event)

        manager.update(time_delta)
        screen.blit(background, (0, 0))
        screen.blit(volumeImg, (760, 15))
        title = pygame.image.load('resources/images/spacelogo-image.png')
        screen.blit(title, (255, 60))
        manager.draw_ui(screen)
        pygame.display.update()


# back
def game_over_screen(screen):
    global client
    msg = "Game over!"
    if game_mode != GameModeConstraints.PRACTICE:
        client.send(Message.FINISH_GAME)
        client.send(str(score_value))
        msg = client.receive()
        client.send(Client.DISCONNECT_MESSAGE)

    manager = pygame_gui.UIManager((800, 600))

    buttonBack = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((800 / 2 - 50, 600 / 2 + 110), (100, 50)),
        text="Back",
        manager=manager,
    )

    # Create clock to control frame rate
    clock = pygame.time.Clock()

    while True:

        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == buttonBack:
                    start_screen(screen)
            manager.process_events(event)
        manager.update(time_delta)
        screen.blit(background, (0, 0))
        screen.blit(volumeImg, (760, 15))
        manager.draw_ui(screen)
        game_over_text(msg)
        show_score(320, 300)
        pygame.display.update()


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_time(time):
    score = font.render("Time : " + str(round(time)), True, (255, 255, 255))
    screen.blit(score, (10, 50))


def game_over_text(msg):
    over_text = over_font.render(msg, True, (255, 255, 255))
    screen.blit(over_text, (200, 150))


def load_thanh_mau(screen, hp):
    if hp == 5:
        playerHPImg = pygame.image.load('resources/images/Asset 1.png')
    elif hp == 4:
        playerHPImg = pygame.image.load('resources/images/Asset 2.png')
    elif hp == 3:
        playerHPImg = pygame.image.load('resources/images/Asset 3.png')
    elif hp == 2:
        playerHPImg = pygame.image.load('resources/images/Asset 4.png')
    else:
        playerHPImg = pygame.image.load('resources/images/Asset 5.png')

    screen.blit(playerHPImg, (540, 10))


# player name
# Game Loop
def startGame(name_player):
    global score_value, volumeImg, music_playing, client
    player = Player('', 'resources/images/spaceship.png', 370, 480, 0, 5, 0)
    bullet = Bullet(pygame.image.load('resources/images/bullet.png'), 0, 480, 0, 10, "ready")
    enemy = khoiTaoEnemy()
    thienThach = khoiTaoThienThach()
    start = True
    running = True
    score_value = 0
    # Bấm giờ
    time = 60
    start_ticks = pygame.time.get_ticks()

    if start:
        if game_mode != GameModeConstraints.PRACTICE:
            client = Client(SERVER)
            client.send(Message.START_GAME)
            client.send(name_player)
            client.send(str(game_mode))
            client.receive()

        while running:
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000

            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))

            load_thanh_mau(screen, player.hp)

            # Xử lý va chạm thiên thạch
            for i in range(len(thienThach)):
                if thienThach[i].y > 600:
                    thienThach[i].x = random.randint(0, 736)
                    thienThach[i].y = 0

                if thienThach[i].y >= 0 :
                    thienThach[i].show(screen)
                    thienThach[i].y += thienThach[i].y_change

                collide = thienThach[i].isCollide(player)
                if collide:
                    if music_playing:
                        explosionSound.play()
                    thienThach[i].x = random.randint(0, 480)
                    thienThach[i].y = 0
                    player.hp -= 1

                    if player.hp <= 0:
                        game_over_screen(screen)
                        return

            #Xử lý button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Kiểm tra xem click vào hình chữ nhật chứa biểu tượng loa hay không
                    if rect.collidepoint(event.pos):
                        # Nếu đang phát âm thanh, tạm ngừng phát
                        if not music_playing:
                            volumeImg = pygame.image.load('resources/images/volume-up.png')
                            pygame.mixer.music.play(-1)
                            music_playing = True
                        else:
                            pygame.mixer.music.stop()
                            volumeImg = pygame.image.load('resources/images/mute.png')
                            music_playing = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.x_change = -3
                    if event.key == pygame.K_RIGHT:
                        player.x_change = 3
                    if event.key == pygame.K_SPACE:
                        if bullet.state == "ready":
                            if music_playing:
                                bulletSound.play()
                            bullet.x = player.x
                            bullet.fire_bullet(screen)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player.x_change = 0

            #Di chuyển nhân vật
            player.x += player.x_change
            if player.x <= 0:
                player.x = 0
            elif player.x >= 736:
                player.x = 736

            for i in range(len(enemy)):
                if enemy[i].y > 440 or seconds >= time:
                    for j in range(len(enemy)):
                        enemy[j].y = 2000
                    game_over_screen(screen)

                    break

                enemy[i].x += enemy[i].x_change
                if enemy[i].x <= 0:
                    enemy[i].x_change = 2
                    enemy[i].y += enemy[i].y_change
                elif enemy[i].x >= 736:
                    enemy[i].x_change = -2
                    enemy[i].y += enemy[i].y_change

                collision = enemy[i].isCollision(bullet)
                if collision:
                    if music_playing:
                        explosionSound.play()
                    bullet.y = 480
                    bullet.state = "ready"
                    score_value += 1
                    enemy[i].x = random.randint(0, 736)
                    enemy[i].y = random.randint(50, 150)

                enemy[i].show(screen)

            if bullet.y <= 0:
                bullet.y = 480
                bullet.state = "ready"

            if bullet.state == "fire":
                bullet.fire_bullet(screen)
                bullet.y -= bullet.y_change

            screen.blit(volumeImg, (760, 15))
            player.show(screen)
            show_score(textX, testY)
            show_time(time - seconds)
            pygame.display.update()


start_screen(screen)
