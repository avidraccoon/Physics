# Example file showing a basic pygame "game loop"
import math

import pygame
import numpy as np


# pygame setup

gravity = 9.6
delta_time = 50
distance_multi = 1000
planets = [
    [0, 0, 0, 0, 1000],
    [0, 30*distance_multi, -0.5, 0, 1000],
    [0, -30*distance_multi, 0.5, 0, 1000]
]
total_mass = sum(map(lambda planet: planet[4], planets))
center_of_gravity = [0, 0]
for planet in planets:
    center_of_gravity[0] += planet[0]*planet[4]
    center_of_gravity[1] += planet[1]*planet[4]
center_of_gravity[0] /= total_mass
center_of_gravity[1] /= total_mass
print(center_of_gravity, total_mass)
pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    forces = []
    screen.fill((0, 0, 0))
    #print(planets)
    for index1 in range(len(planets)):
        planet1 = planets[index1]
        pos1 = np.array([planet1[0], planet1[1]])
        planetForce = np.array([0.0, 0.0])
        for index2 in range(len(planets)):
            if index1 == index2:
                continue
            planet2 = planets[index2]
            pos2 = np.array([planet2[0], planet2[1]])
            difference = pos1 - pos2
            cubedAbs = np.linalg.norm(difference)**3
            planetForce -= gravity * planet2[4] * (difference/cubedAbs)
        planet1[2] += planetForce[0] * delta_time
        planet1[3] += planetForce[1] * delta_time
    # RENDER YOUR GAME HERE

    for planet in planets:
        planet[0]+=planet[2] * delta_time
        planet[1]+=planet[3] * delta_time
        #print(planet[2])
        pygame.draw.circle(screen, (255, 0, 0), [planet[0]/distance_multi+200, planet[1]/distance_multi+200], 5)
    pygame.draw.circle(screen, (255, 0, 0), center_of_gravity, 3)
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()