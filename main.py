import math
import random
import pygame
from pygame import mixer
import pygame_gui
import re

from GameModeConstraints import GameModeConstraints
from Client import Client

pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.Font(None, 36)
background = pygame.image.load('background.png')

mixer.music.load("background.wav")
# mixer.music.play(-1)

pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo-flying.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('final-boss.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

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
    global game_mode, SERVER

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
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == buttonPractice:
                    game_mode = GameModeConstraints.PRACTICE
                    if playerNameEntry.text == "":
                        playerNameEntry.focus()
                        ipEntry.unfocus()
                    else:
                        return playerNameEntry.text.strip()
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
                            return playerNameEntry.text.strip()
                elif event.ui_element == buttonQuit:
                    pygame.quit()
                    quit()
            manager.process_events(event)

        manager.update(time_delta)
        screen.blit(background, (0, 0))
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


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# player name
start = True
running = True
# Game Loop
if start:
    name_player = start_screen(screen)
    if game_mode == GameModeConstraints.TWO_PLAYERS:
        client = Client(SERVER)
        client.send(name_player)
        client.receive()
    time = 60
    start_ticks=pygame.time.get_ticks()
    while running:
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000

        screen.fill((0, 0, 0))

        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -3
                if event.key == pygame.K_RIGHT:
                    playerX_change = 3
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletSound = mixer.Sound("laser.wav")
                        bulletSound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        for i in range(num_of_enemies):
            if enemyY[i] > 440 or seconds >= time:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                msg = "GAME OVER!"
                if game_mode == GameModeConstraints.TWO_PLAYERS:
                    client.send(str(score_value))
                    result = client.receive()
                    msg = result
                    client.send(Client.DISCONNECT_MESSAGE)
                back_screen(screen, msg)
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 2
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -2
                enemyY[i] += enemyY_change[i]

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, testY)
        show_time(time - seconds)
        pygame.display.update()

