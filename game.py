import pygame
from pygame.locals import *

pygame.init()

SCREEN_SIZE = pygame.display.list_modes()[0]
screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN)

font = pygame.font.SysFont(pygame.font.get_default_font(), 32)
clock = pygame.time.Clock()

running = True
while running:
    screen.fill((200, 200, 255))
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                running = False
    dt = clock.tick()
    screen.blit(font.render("FPS: " + str(int(clock.get_fps())), True, (0, 0, 0)), (0, 0))
    pygame.display.flip()


