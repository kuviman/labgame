import pygame
from pygame.locals import *
from random import *

pygame.init()
SCREEN_SIZE = pygame.display.list_modes()[0]

def transform(x, y):
    return (int(SCREEN_SIZE[0] / 2 + (x - Lab.size / 2) * Lab.scale),
            int(SCREEN_SIZE[1] / 2 + (y - Lab.size / 2) * Lab.scale))

def transformBack(x, y):
    return (Lab.size / 2 + (x - SCREEN_SIZE[0] / 2) / Lab.scale,
            Lab.size / 2 + (y - SCREEN_SIZE[1] / 2) / Lab.scale)


class Lab:
    size = 8
    scale = (SCREEN_SIZE[1] - 100) / size

    def __init__(self):
        dsu = []
        left = []
        down = []
        for i in range(self.size):
            dsu.append([])
            left.append([])
            down.append([])
            for j in range(self.size):
                dsu[-1].append(i * self.size + j)
                left[-1].append(False)
                down[-1].append(False)
        def merge(x, y):
            for i in range(self.size):
                for j in range(self.size):
                    if dsu[i][j] == y:
                        dsu[i][j] = x
        while True:
            poss = []
            for i in range(self.size):
                for j in range(self.size - 1):
                    if dsu[i][j] != dsu[i][j + 1]:
                        poss.append(((i, j), (i, j + 1)))
            for i in range(self.size - 1):
                for j in range(self.size):
                    if dsu[i][j] != dsu[i + 1][j]:
                        poss.append(((i, j), (i + 1, j)))
            if len(poss) == 0:
                break
            d = choice(poss)
            merge(dsu[d[0][0]][d[0][1]], dsu[d[1][0]][d[1][1]])
            if d[0][0] == d[1][0]:
                down[d[1][0]][d[1][1]] = True
            else:
                left[d[1][0]][d[1][1]] = True
        self.left = left
        self.down = down

        self.image = pygame.Surface(SCREEN_SIZE)
        self.image.fill((0, 0, 0))

        backLines = 100
        for i in range(backLines):
            x = -self.size + self.size * 3 * i / backLines
            pygame.draw.aaline(self.image, (30, 30, 100), transform(x, -self.size), transform(x + self.size, 2 * self.size))
            pygame.draw.aaline(self.image, (30, 30, 100), transform(x, -self.size), transform(x - self.size, 2 * self.size))

        self.drawLab((0, 0, 255), 7)
        self.drawLab((100, 100, 255), 5)
        self.drawLab((255, 255, 255), 2)
        self.drawExits((255, 100, 100), 7)
        self.drawExits((255, 0, 0), 3)

    def drawExits(self, exitColor, exitWidth):
        pygame.draw.line(self.image, exitColor,
                         transform(0, self.size - 1), transform(0, self.size),
                         exitWidth)
        pygame.draw.line(self.image, exitColor,
                         transform(self.size, 0), transform(self.size, 1),
                         exitWidth)

    def drawLab(self, lineColor, lineWidth):
        for i in range(self.size + 1):
            for j in range(self.size + 1):
                if self.wallLeft(i, j):
                    pygame.draw.line(self.image, lineColor,
                                     transform(i, j), transform(i, j + 1),
                                     lineWidth)
                if self.wallDown(i, j):
                    pygame.draw.line(self.image, lineColor,
                                     transform(i, j), transform(i + 1, j),
                                     lineWidth)
        if lineWidth < 4:
            return
        for i in range(self.size + 1):
            for j in range(self.size + 1):
                pygame.draw.circle(self.image, lineColor, transform(i, j), lineWidth // 2)

    def wallLeft(self, i, j):
        return ((i == 0 or i == self.size) and j < self.size) or (j < self.size and not self.left[i][j])
    def wallDown(self, i, j):
        return ((j == 0 or j == self.size) and i < self.size) or (i < self.size and not self.down[i][j])

    def render(self, screen):
        screen.blit(self.image, (0, 0))

    def collideLeft(self, i, j, a, b):
        x1, y1 = a
        x2, y2 = b
        if x1 > x2:
            x1, y1, x2, y2 = x2, y2, x1, y1
        if x1 <= i < x2:
            y = y1 + (y2 - y1) * (i - x1) / (x2 - x1)
            if j <= y <= j + 1:
                return True
        return False

    def collideDown(self, i, j, a, b):
        x1, y1 = a
        x2, y2 = b
        if y1 > y2:
            x1, y1, x2, y2 = x2, y2, x1, y1
        if y1 <= j < y2:
            x = x1 + (x2 - x1) * (j - y1) / (y2 - y1)
            if i <= x <= i + 1:
                return True
        return False

    def collide(self, a, b):
        if self.collideLeft(0, self.size - 1, a, b):
            return "start"
        if self.collideLeft(self.size, 0, a, b):
            return "finish"
        for i in range(self.size + 1):
            for j in range(self.size + 1):
                if self.wallLeft(i, j) and self.collideLeft(i, j, a, b):
                    return "wall"
                if self.wallDown(i, j) and self.collideDown(i, j, a, b):
                    return "wall"
        return None

class Player:
    sens = 1
    def __init__(self):
        self.x, self.y = 0.1, Lab.size - 0.5
        self.alive = True
    def render(self, screen):
        pygame.draw.circle(screen, (0, 100, 0), transform(self.x, self.y), int(Lab.scale / 10))
        pygame.draw.circle(screen, (0, 255, 0), transform(self.x, self.y), int(Lab.scale / 20))

def main():
    screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN)

    font = pygame.font.SysFont(pygame.font.get_default_font(), 32)
    clock = pygame.time.Clock()

    lab = Lab()
    player = Player()

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    pygame.mouse.get_rel()

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == QUIT:
                running = False
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    running = False
                elif e.key == K_F2:
                    player = Player()
            elif e.type == MOUSEMOTION:
                dx, dy = pygame.mouse.get_rel()
                if player.alive:
                    nx = player.x + dx * Player.sens / Lab.scale
                    ny = player.y + dy * Player.sens / Lab.scale
                    col = lab.collide((player.x, player.y), (nx, ny))
                    if col is None:
                        player.x, player.y = nx, ny
                    elif col == "wall":
                        player.alive = False
        dt = clock.tick()

        lab.render(screen)
        player.render(screen)

        screen.blit(font.render("FPS: " + str(int(clock.get_fps())), True, (255, 255, 255)), (0, 0))
        pygame.display.flip()

if __name__ == "__main__":
    main()

