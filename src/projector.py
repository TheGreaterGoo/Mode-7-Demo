import pygame
pygame.init()

w = pygame.display.set_mode([400, 400])

drawing = True
while drawing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            drawing = False

    pygame.display.flip()