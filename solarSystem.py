import math, pygame, positioning, nBodyProblem, trailHandler, whoKnowsWhatNow
import numpy as np
import planet as planetLib

distance_multi = 400000
divider = distance_multi/100000
radius_divider = distance_multi
position_offset = [0, 0]
settings = {
    "paused": False,
    "zoom": 1,
    "delta_time": 1,
    "gravity": 6674.3
}
planets = [
    [0.0, 0.0, 0.0, 0.0, 1988400.0, 1400000/2/radius_divider, "yellow"],
    [57.9*distance_multi/divider, 0.0, 0.0, 47.4, 0.33, 4879/2/radius_divider, "tan"],
    [108.2*distance_multi/divider, 0.0, 0.0, 35, 4.87, 12104/2/radius_divider, "brown"],
    [149.6*distance_multi/divider, 0.0, 0.0, 29.8, 5.97, 12756/2/radius_divider, "forestgreen"],
    [228.0*distance_multi/divider, 0.0, 0.0, 24.1, 0.642, 6792/2/radius_divider, "red"],
    [778.5*distance_multi/divider, 0.0, 0.0, 13.1, 1898.0, 142984/2/radius_divider, "orange"],
    [1432.0*distance_multi/divider, 0.0, 0.0, 9.7, 568.0, 120536/2/radius_divider, "maroon"],
    [2867.0*distance_multi/divider, 0.0, 0.0, 6.8, 86.8, 51118/2/radius_divider, "blue"]
]


for index in range(len(planets)):
    planet = planets[index]
    new_verlet_object = whoKnowsWhatNow.PhysicsObject(np.array([planet[0], planet[1]]), np.array([planet[2], planet[3]]), np.array([0.0, 0.0]))
    new_planet = planetLib.Planet("0", new_verlet_object, np.array([0.0, 0.0]), planet[4]*math.pow(10, 24), planet[5], planet[6])
    planets[index] = new_planet


pygame.init()
screen = pygame.display.set_mode((1600, 800))
clock = pygame.time.Clock()
running = True
pygame.display.toggle_fullscreen()
my_font = pygame.font.SysFont('Comic Sans MS', 25)

while running:



    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN: settings["zoom"]/=2
            if event.key == pygame.K_UP:
                mouse = pygame.mouse.get_pos()
                settings["zoom"]*=2
                position_offset[0] -= (mouse[0] - 800) / settings["zoom"] * distance_multi
                position_offset[1] -= (mouse[1] - 400) / settings["zoom"] * distance_multi
            if event.key == pygame.key.key_code("p"): settings["paused"] = not settings["paused"]
            if event.key == pygame.K_LEFT: settings["delta_time"] /= 2
            if event.key == pygame.K_RIGHT: settings["delta_time"] *= 2



    screen.fill((0, 0, 0))


    if not settings["paused"]:
        nBodyProblem.update(planets, settings["gravity"], settings["delta_time"])


    for planet in planets:
        if not settings["paused"]:
            planet.update(settings["delta_time"])
        planet.draw(distance_multi, settings["zoom"], position_offset)


    center_of_mass = nBodyProblem.get_center_of_mass(planets)
    pygame.draw.circle(screen, (0, 255, 0),
                       positioning.world_to_screen(center_of_mass, distance_multi, (1600, 800), settings["zoom"], position_offset), 1)


    timeText = my_font.render('Delta Time: '+str(settings["delta_time"]), False, (255, 255, 255))
    zoomText = my_font.render('Zoom: '+str(settings["zoom"]), False, (255, 255, 255))
    screen.blit(timeText, (0, 0))
    screen.blit(zoomText, (0, 40))


    pygame.display.flip()


    clock.tick(60)  # limits FPS to 60

pygame.quit()