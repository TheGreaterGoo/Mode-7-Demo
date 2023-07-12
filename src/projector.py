import pygame
import numpy
from numba import njit
import asyncio

def game():
    pygame.init()

    w = pygame.display.set_mode([800, 600])
    clock = pygame.time.Clock()

    # define floor specifications
    hres = 120
    half_vres = 100

    mod = hres / 60 # scaling factor (60 degree FOV)
    posx, posy, rot = 0, 0, 0 # player
    posz, vz, az = 1, -0.01, 0.0004
    going_up = False

    frame = numpy.random.uniform(0, 1, (hres, half_vres * 2, 3))
    bg = pygame.image.load("assets/mountains.png")
    bg = pygame.surfarray.array3d(pygame.transform.scale(bg, (360, half_vres * 2)))

    floor_assets = ["assets/grass.png", "assets/rocks.png", "assets/dirt.png"]
    floor = pygame.surfarray.array3d(pygame.image.load(floor_assets[2]))

    drawing = True
    while drawing:

        pygame.display.set_caption(f"FPS: {clock.get_fps():.2f}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                drawing = False

        frame = new_frame(posx, posy, rot, frame, bg, floor, hres, half_vres, mod, posz)


        surface = pygame.surfarray.make_surface(frame * 255)
        surface = pygame.transform.scale(surface, (800, 600))
        w.blit(surface, (0, 0))

        going_up = not is_touching_ground(posz, going_up)
        if (vz > 0): going_up = False

        pygame.display.update()
        posx, posy, rot, vz, going_up = movement(posx, posy, posz, rot, pygame.key.get_pressed(), clock.tick(), vz, going_up)

        if not is_touching_ground(posz, going_up):
            vz += az
            posz += vz
        else:
            vz = 0

def movement(posx, posy, posz, rot, keys, et, vz, going_up):
    if keys[pygame.K_LEFT]:
        rot -= 0.002 * et

    if keys[pygame.K_RIGHT]:
        rot += 0.002 * et

    if keys[pygame.K_UP]:
        posx += numpy.cos(rot) * 0.002 * et
        posy += numpy.sin(rot) * 0.002 * et

    if keys[pygame.K_DOWN]:
        posx -= numpy.cos(rot) * 0.002 * et
        posy -= numpy.sin(rot) * 0.002 * et

    if keys[pygame.K_SPACE] and is_touching_ground(posz, going_up):
        going_up = True
        vz = -0.02

    return posx, posy, rot, vz, going_up

def is_touching_ground(posz, going_up):
    if going_up: return False
    if posz >= 1: return True
    return False

@njit()
def new_frame(posx, posy, rot, frame, bg, floor, hres, half_vres, mod, z):
    for i in range(hres):  # iterating through the columns in the screen
        # rot_i is the direction of each column part of the fov in the frame
        rot_i = rot + numpy.deg2rad(i / mod - 30)  # fov represented by rot +/- 30 degrees
        sin, cos, cos2 = numpy.sin(rot_i), numpy.cos(rot_i), numpy.cos(numpy.deg2rad(i / mod - 30))

        # Extracting and setting an entire column of the background to the frame
        frame[i][:] = bg[int(numpy.rad2deg(rot_i) % 359)][:] / 255

        # iterating through the bottom half rows in the screen (floor doesn't go past halfway point)
        # distance from player to screen is inversely proportional to the perception of floor distance
        # basically the higher the player looks on the screen, the further away the floor is projected
        for j in range(half_vres):
            n = (half_vres / (half_vres - j)) / (cos2 * z)
            x, y = posx + cos * n, posy + sin * n

            # Drawing the floor
            shade = 0.25 + 0.8 * (1 - j / half_vres)

            floor_x, floor_y = int(x * 2 % 1 * 100), int(y * 2 % 1 * 100)
            frame[i][half_vres * 2 - j - 1] = shade * floor[floor_x][floor_y] / 255

    return frame
            # if int(x) % 2 == int(y) % 2:
            #     frame[i][half_vres * 2 - j - 1] = [0, 0, 0]
            # else:
            #     frame[i][half_vres * 2 - j - 1] = [1, 1, 1]

if __name__ == "__main__":
    game()
