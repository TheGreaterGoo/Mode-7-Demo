import pygame
import numpy
pygame.init()

w = pygame.display.set_mode([400, 400])

# define floor specifications
hres = 120
half_vres = 100

mod = hres / 60 # scaling factor (60° FOV)
posx, posy, rot = 0, 0, 0 # player

frame = numpy.random.uniform(0, 1, (80, 60, 3))

drawing = True
while drawing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            drawing = False

    for i in range(hres):
        rot_i = rot + numpy.deg2rad(i/mod - 30) # fov represented by rot +/- 30°
        sin, cos = numpy.sin(rot_i), numpy.cos(rot_i)

        for j in range(half_vres):
            n = half_vres / (half_vres - j)
            x, y = posx + cos * n, posy + sin * n

    surface = pygame.surfarray.make_surface(frame * 255)
    surface = pygame.transform.scale(surface, (400, 400))

    w.blit(surface, (0, 0))

    pygame.display.flip()