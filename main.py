
import random
import pygame
from pygame import mixer
import pygame_gui
import re

from Enemy import Enemy
from Bullet import Bullet
from Player import Player
from ThienThach import ThienThach
from GameModeConstraints import GameModeConstraints
from Client import Client

pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.Font(None, 36)
background = pygame.image.load('background.png')


# Kích thước của hình chữ nhật
rect_width = 50
rect_height = 50

# Tạo hình chữ nhật
rect = pygame.Rect(0, 0, rect_width, rect_height)

# Đặt tọa độ cho hình chữ nhật
rect.x = 740 # Tọa độ x
rect.y = 5 # Tọa độ y

pygame.mixer.music.load("background.wav")
volumeImg = pygame.image.load('volume-up.png')
pygame.mixer.music.play(-1)
music_playing = True

pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo-flying.png')
pygame.display.set_icon(icon)
def khoiTaoEnemy():
    enemy = []
    num_of_enemies = 6
    for i in range(num_of_enemies):
        enemyTam = Enemy(pygame.image.load('final-boss.png'), random.randint(0, 736), random.randint(50, 150), 4, 40)
        enemy.append(enemyTam)
    return enemy

def khoiTaoThienThach():
    # khoi tao thien thach
    thienThach = []
    num_of_meteorite = 2

    for i in range(num_of_meteorite):
        thienThachTam = ThienThach(pygame.image.load('meteorite.png'),random.randint(0, 480), 0, 2)
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

# start
def start_screen(screen):
    global game_mode, SERVER, volumeImg, music_playing

    manager = pygame_gui.UIManager((800, 600))

    # Create input
    title = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((800 / 2 - 100, 600 / 2 - 150), (200, 50)),
        text="Space Invader",
        manager=manager,
    )

    playerNameEntry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((800 / 2 - 100, 600 / 2 - 50), (200, 50)),
        manager=manager,
        placeholder_text="Type your name"
    )

    ipEntry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((800 / 2 - 100, 600 / 2), (200, 50)),
        manager=manager,
        placeholder_text="Type IP"
    )

    # Create start button
    buttonPractice = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((800 / 2 - 50, 600 / 2 + 50), (100, 50)),
        text="Practice",
        manager=manager,
    )

    buttonCompete = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((800 / 2 - 50, 600 / 2 + 100), (100, 50)),
        text="Fight",
        manager=manager,
    )

    buttonThreeplayer = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((800 / 2 - 200, 600 / 2 + 100), (100, 50)),
        text="ThreePlayer",
        manager=manager,
    )

    buttonFourplayer = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((800 / 2 - 200, 600 / 2 + 150), (100, 50)),
        text="FourPlayer",
        manager=manager,
    )

    buttonQuit = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((800 / 2 - 50, 600 / 2 + 150), (100, 50)),
        text="Quit",
        manager=manager,
    )
    # Create clock to control frame rate
    clock = pygame.time.Clock()

    while True:

        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Kiểm tra xem click vào hình chữ nhật chứa biểu tượng loa hay không
                if rect.collidepoint(event.pos):
                    # Nếu đang phát âm thanh, tạm ngừng phát
                    if not music_playing:
                        volumeImg = pygame.image.load('volume-up.png')
                        pygame.mixer.music.play(-1)
                        music_playing = True
                    else:
                        pygame.mixer.music.stop()
                        volumeImg = pygame.image.load('mute.png')
                        music_playing = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == buttonPractice:
                    game_mode = GameModeConstraints.PRACTICE
                    if playerNameEntry.text == "":
                        playerNameEntry.focus()
                        ipEntry.unfocus()
                    else:
                        return startGame(playerNameEntry.text.strip())
                elif event.ui_element == buttonCompete:
                    game_mode = GameModeConstraints.TWO_PLAYERS
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
                elif event.ui_element == buttonThreeplayer:
                    game_mode = GameModeConstraints.THREE_PLAYERS
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
                elif event.ui_element == buttonFourplayer:
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
                elif event.ui_element == buttonQuit:
                    pygame.quit()
                    quit()
            manager.process_events(event)

        manager.update(time_delta)
        screen.blit(background, (0, 0))
        screen.blit(volumeImg, (760, 15))
        manager.draw_ui(screen)
        title.show()
        pygame.display.update()


# back
def back_screen(screen, msg):

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
                quit()
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


# player name
# Game Loop
def startGame(name_player):
    global score_value, volumeImg, music_playing
    player = Player('', 'spaceship.png', 370, 480, 0, 5, 0)
    bullet = Bullet(pygame.image.load('bullet.png'), 0, 480, 0, 10, "ready")
    enemy = khoiTaoEnemy()
    thienThach = khoiTaoThienThach()
    start = True
    running = True

    if start:
        if game_mode == GameModeConstraints.TWO_PLAYERS:
            client = Client(SERVER)
            client.send(name_player)
            client.send(str(game_mode))
            client.receive()
        elif game_mode == GameModeConstraints.THREE_PLAYERS:
            client = Client(SERVER)
            client.send(name_player)
            client.send(str(game_mode))
            client.receive()
        elif game_mode == GameModeConstraints.FOUR_PLAYERS:
            client = Client(SERVER)
            client.send(name_player)
            client.send(str(game_mode))
            client.receive()
        time = 60
        start_ticks = pygame.time.get_ticks()
        while running:
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000

            screen.fill((0, 0, 0))

            screen.blit(background, (0, 0))
            for i in range(len(thienThach)):
                if player.hp == 5:
                    playerHPImg = pygame.image.load('Asset 1.png')
                elif player.hp == 4:
                    playerHPImg = pygame.image.load('Asset 2.png')
                elif player.hp == 3:
                    playerHPImg = pygame.image.load('Asset 3.png')
                elif player.hp == 2:
                    playerHPImg = pygame.image.load('Asset 4.png')
                else:
                    playerHPImg = pygame.image.load('Asset 5.png')

                screen.blit(playerHPImg, (540, 10))

                if thienThach[i].y > 600:
                    thienThach[i].x = random.randint(0, 736)
                    thienThach[i].y = 0

                if thienThach[i].y >= 0 :
                    thienThach[i].show(screen)
                    thienThach[i].y += thienThach[i].y_change

                collide = thienThach[i].isCollide(player)
                if collide:
                    thienThach[i].x = random.randint(0, 480)
                    thienThach[i].y = 0
                    player.hp -= 1

                    if player.hp <= 0:
                        msg = "GAME OVER!"
                        if game_mode == GameModeConstraints.TWO_PLAYERS:
                            client.send(str(score_value))
                            result = client.receive()
                            msg = result
                            client.send(Client.DISCONNECT_MESSAGE)
                        elif game_mode == GameModeConstraints.THREE_PLAYERS:
                            client.send(str(score_value))
                            result = client.receive()
                            msg = result
                            client.send(Client.DISCONNECT_MESSAGE)
                        elif game_mode == GameModeConstraints.FOUR_PLAYERS:
                            client.send(str(score_value))
                            result = client.receive()
                            msg = result
                            client.send(Client.DISCONNECT_MESSAGE)
                        back_screen(screen, msg)
                        break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Kiểm tra xem click vào hình chữ nhật chứa biểu tượng loa hay không
                    if rect.collidepoint(event.pos):
                        # Nếu đang phát âm thanh, tạm ngừng phát
                        if not music_playing:
                            volumeImg = pygame.image.load('volume-up.png')
                            pygame.mixer.music.play(-1)
                            music_playing = True
                        else:
                            pygame.mixer.music.stop()
                            volumeImg = pygame.image.load('mute.png')
                            music_playing = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.x_change = -3
                    if event.key == pygame.K_RIGHT:
                        player.x_change = 3
                    if event.key == pygame.K_SPACE:
                        if bullet.state == "ready":
                            bulletSound = mixer.Sound("laser.wav")
                            bulletSound.play()
                            bullet.x = player.x
                            bullet.fire_bullet(screen )

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player.x_change = 0

            player.x += player.x_change
            if player.x <= 0:
                player.x = 0
            elif player.x >= 736:
                player.x = 736

            for i in range(len(enemy)):
                if enemy[i].y > 440 or seconds >= time:
                    for j in range(len(enemy)):
                        enemy[j].y = 2000
                    msg = "GAME OVER!"
                    if game_mode == GameModeConstraints.TWO_PLAYERS:
                        client.send(str(score_value))
                        result = client.receive()
                        msg = result
                        client.send(Client.DISCONNECT_MESSAGE)
                    elif game_mode == GameModeConstraints.THREE_PLAYERS:
                        client.send(str(score_value))
                        result = client.receive()
                        msg = result
                        client.send(Client.DISCONNECT_MESSAGE)
                    elif game_mode == GameModeConstraints.FOUR_PLAYERS:
                        client.send(str(score_value))
                        result = client.receive()
                        msg = result
                        client.send(Client.DISCONNECT_MESSAGE)
                    back_screen(screen, msg)

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
                    explosionSound = mixer.Sound("explosion.wav")
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
