import pygame
from pygame.locals import *
from random import *

pygame.init()

SCREEN_SIZE = pygame.display.list_modes()[0]
screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN)

font = pygame.font.SysFont(pygame.font.get_default_font(), 32)
clock = pygame.time.Clock()

size = 8

labImage = pygame.Surface(SCREEN_SIZE)

dsu = []
left = []
down = []
for i in range(size):
    dsu.append([])
    left.append([])
    down.append([])
    for j in range(size):
        dsu[-1].append(i * size + j)
        left[-1].append(False)
        down[-1].append(False)
def merge(x, y):
    for i in range(size):
        for j in range(size):
            if dsu[i][j] == y:
                dsu[i][j] = x

scale = (SCREEN_SIZE[1] - 100) / size

while True:
    poss = []
    for i in range(size):
        for j in range(size - 1):
            if dsu[i][j] != dsu[i][j + 1]:
                poss.append(((i, j), (i, j + 1)))
    for i in range(size - 1):
        for j in range(size):
            if dsu[i][j] != dsu[i + 1][j]:
                poss.append(((i, j), (i + 1, j)))
    if len(poss) == 0:
        break
    d = choice(poss)
    merge(dsu[d[0][0]][d[0][1]], dsu[d[1][0]][d[1][1]])
    if d[0][0] == d[1][0]:
        left[d[1][0]][d[1][1]] = True
    else:
        down[d[1][0]][d[1][1]] = True

def transform(x, y):
    return (int(SCREEN_SIZE[0] / 2 + (x - size / 2) * scale),
            int(SCREEN_SIZE[1] / 2 + (y - size / 2) * scale))

def transformBack(x, y):
    return (size / 2 + (x - SCREEN_SIZE[0] / 2) / scale,
            size / 2 + (y - SCREEN_SIZE[1] / 2) / scale)

def line(screen, x1, y1, x2, y2):
    x1, y1 = transform(x1, y1)
    x2, y2 = transform(x2, y2)
    pygame.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2), 2)

labImage.fill((0, 0, 0))
for i in range(size + 1):
    for j in range(size + 1):
        if ((i == 0 or i == size) and j < size) or (j < size and not down[i][j]):
            line(labImage, i, j, i, j + 1)
        if ((j == 0 or j == size) and i < size) or (i < size and not left[i][j]):
            line(labImage, i, j, i + 1, j)

player = (0, 0)
pygame.mouse.set_visible(False)
pygame.mouse.set_pos(transform(*player))

running = True
while running:
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                running = False
        elif e.type == MOUSEMOTION:
            player = transformBack(*e.pos)
    dt = clock.tick()

    screen.blit(labImage, (0, 0))
    pygame.draw.circle(screen, (255, 0, 0), transform(*player), int(scale / 10))

    screen.blit(font.render("FPS: " + str(int(clock.get_fps())), True, (255, 255, 255)), (0, 0))
    pygame.display.flip()


