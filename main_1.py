import pygame
import random

from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

screen = width, height = 1100, 900

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
ROSE = 155, 0, 100

font = pygame.font.SysFont('Verdana', 20)

main_surface = pygame.display.set_mode(screen)

player = pygame.Surface((13, 13))
player.fill(WHITE)
player_rect = player.get_rect()
player_speed = 4


def create_enemy():
    enemy = pygame.Surface((20, 20))
    enemy.fill(RED)
    enemy_rect = pygame.Rect(width, random.randint(0, height), *enemy.get_size())
    enemy_speed = random.randint(2, 5)
    return [enemy, enemy_rect, enemy_speed]


def create_award():
    award = pygame.Surface((15, 15))
    award.fill(GREEN)
    award_rect = pygame.Rect(random.randint(0, width), 0, *award.get_size())
    award_speed = random.randint(2, 3)
    return [award, award_rect, award_speed]


def create_life():
    life = pygame.Surface((12, 12))
    life.fill(ROSE)
    life_rect = pygame.Rect(random.randint(0, width), height, *life.get_size())
    life_speed = random.randint(5, 7)
    return [life, life_rect, life_speed]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_AWARD = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_AWARD, 2500)

CREATE_LIFE = pygame.USEREVENT + 3
pygame.time.set_timer(CREATE_LIFE, 10000)

scores = 0
lifes_qty = 3

enemies = []
awards = []
lifes = []

is_working = True

while is_working:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_AWARD:
            awards.append(create_award())
        if event.type == CREATE_LIFE:
            lifes.append(create_life())

    if random.randint(1,7) == 1:
        enemies.append(create_enemy()) #GOD MODE

    pressed_keys = pygame.key.get_pressed()

    main_surface.fill(BLACK)

    main_surface.blit(player, player_rect)

    main_surface.blit(font.render(str(scores), True, GREEN), (width - 25, 10))
    main_surface.blit(font.render(str(lifes_qty), True, ROSE), (30, 10))

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
            enemies.pop(enemies.index(enemy))
            print('WTF! CAREFUL')
            lifes_qty -= 1
            if lifes_qty == 0:
                print('ДА СОСУ!')
                is_working = False
                print('Your result is: ' + str(scores))

    for award in awards:
        award[1] = award[1].move(0, award[2])
        main_surface.blit(award[0], award[1])

        if award[1].bottom > height:
            awards.pop(awards.index(award))

        if player_rect.colliderect(award[1]):
            awards.pop(awards.index(award))
            scores += 1
            print('ZAIBIS')

    for life in lifes:
        life[1] = life[1].move(0, -life[2])
        main_surface.blit(life[0], life[1])

        if life[1].top < 0:
            lifes.pop(lifes.index(life))

        if player_rect.colliderect(life[1]):
            lifes.pop(lifes.index(life))
            lifes_qty += 1
            print('NOW YOU FILLING BETTER')

    if pressed_keys[K_DOWN] and not player_rect.bottom >= height:
        player_rect = player_rect.move(0, player_speed)

    if pressed_keys[K_UP] and not player_rect.top <= 0:
        player_rect = player_rect.move(0, -player_speed)

    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed, 0)

    if pressed_keys[K_LEFT] and not player_rect.left <= 0:
        player_rect = player_rect.move(-player_speed, 0)

    # if ball_rect.right >= width:
    #     print('КІБОРГ УБІЙЦА')

    #main_surface.fill((155, 155, 155))
    pygame.display.flip()
