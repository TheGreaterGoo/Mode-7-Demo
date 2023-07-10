import pygame
import numpy

def game():
    pygame.init()

    w = pygame.display.set_mode([800, 600])
    clock = pygame.time.Clock()

    # define floor specifications
    hres = 120
    half_vres = 100

    mod = hres / 60 # scaling factor (60 degree FOV)
    posx, posy, rot = 0, 0, 0 # player

    frame = numpy.random.uniform(0, 1, (hres, half_vres * 2, 3))

    drawing = True
    while drawing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                drawing = False

        for i in range(hres): # iterating through the columns in the screen
            # rot_i is the direction of each column part of the fov in the frame
            rot_i = rot + numpy.deg2rad(i/mod - 30) # fov represented by rot +/- 30 degrees
            sin, cos = numpy.sin(rot_i), numpy.cos(rot_i)

            # iterating through the bottom half rows in the screen (floor doesn't go past halfway point)
            # distance from player to screen is inversely proportional to the perception of floor distance
            # basically the higher the player looks on the screen, the further away the floor is projected
            for j in range(half_vres):
                n = half_vres / (half_vres - j)
                x, y = posx + cos * n, posy + sin * n

                if int(x) % 2 == int(y) % 2:
                    frame[i][half_vres * 2 - j - 1] = [0, 0, 0]
                else:
                    frame[i][half_vres * 2 - j - 1] = [1, 1, 1]

        surface = pygame.surfarray.make_surface(frame * 255)
        surface = pygame.transform.scale(surface, (800, 600))

        w.blit(surface, (0, 0))

        pygame.display.update()
        posx, posy, rot = movement(posx, posy, rot, pygame.key.get_pressed())

def movement(posx, posy, rot, keys):
    if keys[pygame.K_LEFT]:
        rot -= 0.1

    if keys[pygame.K_RIGHT]:
        rot += 0.1

    if keys[pygame.K_UP]:
        posx += numpy.cos(rot) * 0.1
        posy += numpy.sin(rot) * 0.1

    if keys[pygame.K_DOWN]:
        posx -= numpy.cos(rot) * 0.1
        posy -= numpy.sin(rot) * 0.1

    return posx, posy, rot

if __name__ == "__main__":
    game()
