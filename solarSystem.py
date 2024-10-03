import math
import numpy as np
import pygame
import nBodyProblem, trailHandler, whoKnowsWhatNow
import planet as planetLib
import positioning

gravity = 6674.3
delta_time = 1
totalTime = 0
yearDivider = 16384*60*6.42/2
monthDivider = yearDivider/12
dayDivider = yearDivider/365
hourDivider = dayDivider/24
minuteDivider = hourDivider/60
distance_multi = 400000
divider = distance_multi/100000
#divider = 1
speed_divider = 1
radius_divider = distance_multi
pos = [0, 0]
zoom = 1
settings = {
    "paused": False
}
old_planets = [
    [0.0, 0.0, 0.0, 0.0, 1988400.0, 1400000/2/radius_divider, "yellow"],
    [57.9*distance_multi/divider, 0.0, 0.0, 47.4/speed_divider, 0.33, 4879/2/radius_divider, "tan"],
    [108.2*distance_multi/divider, 0.0, 0.0, 35/speed_divider, 4.87, 12104/2/radius_divider, "brown"],
    [149.6*distance_multi/divider, 0.0, 0.0, 29.8/speed_divider, 5.97, 12756/2/radius_divider, "forestgreen"],
    [228.0*distance_multi/divider, 0.0, 0.0, 24.1/speed_divider, 0.642, 6792/2/radius_divider, "red"],
    [778.5*distance_multi/divider, 0.0, 0.0, 13.1/speed_divider, 1898.0, 142984/2/radius_divider, "orange"],
    [1432.0*distance_multi/divider, 0.0, 0.0, 9.7/speed_divider, 568.0, 120536/2/radius_divider, "maroon"],
    [2867.0*distance_multi/divider, 0.0, 0.0, 6.8/speed_divider, 86.8, 51118/2/radius_divider, "blue"]
]
planets = []
for planet in old_planets:
    new_verlet_object = whoKnowsWhatNow.PhysicsObject(np.array([planet[0], planet[1]]), np.array([planet[2], planet[3]]), np.array([0.0, 0.0]))
    new_planet = planetLib.Planet("0", new_verlet_object, np.array([0.0, 0.0]), planet[4], planet[5], planet[6])
    planets.append(new_planet)
center_of_mass = nBodyProblem.get_center_of_mass(planets)
pygame.init()
screen = pygame.display.set_mode((1600, 800))
clock = pygame.time.Clock()
running = True
pygame.display.toggle_fullscreen()
my_font = pygame.font.SysFont('Comic Sans MS', 25)

while running:
    global paused
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                zoom/=2
            if event.key == pygame.K_UP:
                mouse = pygame.mouse.get_pos()
                zoom*=2
                pos[0] -= (mouse[0]-800)/zoom*distance_multi
                pos[1] -= (mouse[1]-400)/zoom*distance_multi
            if event.key == pygame.key.key_code("p"):
                settings["paused"] = not settings["paused"]
            if event.key == pygame.K_LEFT:
                delta_time /= 2
            if event.key == pygame.K_RIGHT:
                delta_time *= 2

    screen.fill((0, 0, 0))

    if not settings["paused"]:
        nBodyProblem.update(planets, gravity, delta_time)
    center_of_mass = nBodyProblem.get_center_of_mass(planets)
    for planet in planets:
        if not settings["paused"]:
            planet.update(delta_time)
        planet.draw(distance_multi, zoom, pos)
    pygame.draw.circle(screen, (0, 255, 0),
                        positioning.world_to_screen(center_of_mass, distance_multi, (1600, 800), zoom, pos), 1)
    # flip() the display to put your work on screen
    timeText = my_font.render('Delta Time: '+str(delta_time), False, (255, 255, 255))
    zoomText = my_font.render('Zoom: '+str(zoom), False, (255, 255, 255))
    totalText = my_font.render('Total Time: '+str(totalTime), False, (255, 255, 255))
    yearEstimateText = my_font.render('Estimated Years: '+str(round(totalTime/yearDivider, 4)), False, (255, 255, 255))
    monthEstimateText = my_font.render('Estimated Months: '+str(round(totalTime/monthDivider, 4)), False, (255, 255, 255))
    dayEstimateText = my_font.render('Estimated Days: '+str(round(totalTime/dayDivider, 4)), False, (255, 255, 255))
    hourEstimateText = my_font.render('Estimated Hours: '+str(round(totalTime/hourDivider, 4)), False, (255, 255, 255))
    if not settings["paused"]: totalTime+=delta_time
    screen.blit(timeText, (0, 0))
    screen.blit(zoomText, (0, 40))
    screen.blit(totalText, (0, 80))
    screen.blit(yearEstimateText, (0, 120))
    screen.blit(monthEstimateText, (0, 150))
    screen.blit(dayEstimateText, (0, 180))
    screen.blit(hourEstimateText, (0, 210))
    print(planets[1])
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()