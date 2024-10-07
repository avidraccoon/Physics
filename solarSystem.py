import math, pygame, tools, nBodyProblem, trailHandler, PhysicsObjects

import numpy
import numpy as np

import constants
import gravityFields
import planet as planetLib
from gravityFields import TimeSpaceCurvature, GravityFieldCluster
from concurrent.futures import ThreadPoolExecutor
km_to_meter = 1000
distance_multi = math.pow(10, 6)*km_to_meter
#divider = distance_multi/100000
divider = 1
substeps = 8
totalTime = 1000
max_radius = 10000000000000
print(max_radius/60/60/constants.speed_of_gravity)

radius_divider = distance_multi
position_offset = np.array([0, 0])
settings = {
    "paused": False,
    "zoom": 1,
    "delta_time": 1,
    "gravity": 6.674*math.pow(10, -11)
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
trails = [[] for i in range(8)]
time_space_curvature = gravityFields.TimeSpaceCurvature([])
clusters: list[GravityFieldCluster] = [[] for i in range(8)]
for index in range(len(planets)):
    planet = planets[index]
    new_verlet_object = PhysicsObjects.EulerPhysicsObject(np.array([planet[0], planet[1]]), np.array([planet[2] * km_to_meter, planet[3] * km_to_meter]), np.array([0.0, 0.0]))
    new_planet = planetLib.Planet("0", new_verlet_object, planet[4]*math.pow(10, 24), planet[5], planet[6])
    planets[index] = new_planet
    clusters[index] = gravityFields.GravityFieldCluster([], new_planet, 0)
    time_space_curvature.add_cluster(clusters[index])
width, height = 10, 10
#clusters[1].disabled = False
#for index in range(len(planets)):
#    planet = planets[index]
#    new_field = gravityFields.GravityField(np.array(planet.verlet_object.current_position), planet.mass, 2000000000000, False, 0, 0)
#    clusters[index].add_field(new_field)
pygame.init()
screen = pygame.display.set_mode((1600, 800))
clock = pygame.time.Clock()
running = True
my_font = pygame.font.SysFont('Comic Sans MS', 25)

def task(planet):
    accel = time_space_curvature.get_affect(planet.verlet_object.position,
                                            planet.mass)
    planet.verlet_object.acceleration = accel

hSections = 4

wSections = 4

section = 0
updateTime = False

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

    if (section == 0):
        screen.fill((0, 0, 0))
        pass
    updateTime = section == 0
    pygame.draw.rect(screen, (0,0,0), (0, 0, 300, 90))

    if not settings["paused"] and updateTime:
        for i in range(substeps):
            #nBodyProblem.update(planets, settings["gravity"], settings["delta_time"]/substeps)
            with ThreadPoolExecutor(max_workers=8) as executor:
                futures = [executor.submit(task, planet) for planet in planets]
                results = [future.result() for future in futures]

            for index in range(len(planets)):
                planet = planets[index]
                new_field = gravityFields.GravityField(planet.verlet_object.position, planet.mass, 8000000000000, False, 0, 0)
                clusters[index].add_field(new_field)
                planet.update(settings["delta_time"]/substeps)
            time_space_curvature.update_time(settings["delta_time"]/substeps)

        """
        for index in range(len(planets)):
            planet = planets[index]
            new_field = gravityFields.GravityField(np.array(planet.verlet_object.current_position), planet.mass, 2000000000000,
                                                   False, 0, 0)
            clusters[index].add_field(new_field)
            planet.update(settings["delta_time"] / substeps)
        #for planet in planets:
        #    planet.update(settings["delta_time"])
        time_space_curvature.update_time(settings["delta_time"])
        """
        trailHandler.updatePlanetTrails(trails, planets, 100000)
        totalTime += settings["delta_time"]


    center = [-position_offset[0], -position_offset[1]]
    #print("sec", section%4, math.floor(section/4))
    if (wSections == 1):
        center[0] -= distance_multi * 800 / settings["zoom"]
    elif wSections > 0:
        center[0] += distance_multi*800/settings["zoom"]/wSections*2*(math.floor(wSections/2)-1-(section%wSections))
    if (hSections == 1):
        center[1] -= distance_multi * 400 / settings["zoom"]
    elif hSections > 0:
        center[1] += distance_multi*400/settings["zoom"]/hSections*2*(math.floor(hSections/2)-1-math.floor(section/wSections))
    if hSections > 0 and wSections > 0:
        for x in range(int(1600/width/wSections)):
            for y in range(int(800/height/hSections)):
                pos = [center[0] + x*width*distance_multi/settings["zoom"], center[1] + y*height*distance_multi/settings["zoom"]]
                screen_pos = tools.world_to_screen(pos, distance_multi, (1600, 800), settings["zoom"],
                                                         position_offset)
                value = time_space_curvature.get_force(pos)
                affect = time_space_curvature.get_affect(pos, 1)
                proportions = [affect[0]/value, affect[1]/value]
                if value == 0:
                    proportions = [0, 0]
                value = max(min(value*16384*1024, 16384*1024*64-1), 0)
                r = 0
                ranges = [10**(i/8) for i in range(-64, 64)]
                for i in range(len(ranges)):
                    if value == 0:
                        break
                    if value < ranges[i]:
                        r = (i+1) * 256/len(ranges) - 1
                        break
                    elif i == len(ranges)-1:
                        r = 255
                value=value/4096
                g = (128 + 127*proportions[0])
                b = (128 + 127*proportions[1])
                #g = 0
                #b = 0
                pygame.draw.rect(screen, (r, g, b), [screen_pos[0], screen_pos[1], width, height])
        section=(section+1)%(hSections*wSections)

    #for cluster in clusters:
    #    field = cluster.fields[0]
    #    screen_pos = tools.world_to_screen(field.center, distance_multi, (1600, 800), settings["zoom"], position_offset)
    #    pygame.draw.circle(screen, (0,255,0), screen_pos, field.time*constants.speed_of_gravity/distance_multi*settings["zoom"])

    for trail in trails:
        for index in range(len(trail)-1):
            point1 = trail[index]
            point2 = trail[index+1]
            screen_pos1 = tools.world_to_screen(point1, distance_multi, (1600, 800), settings["zoom"], position_offset)
            screen_pos2 = tools.world_to_screen(point2, distance_multi, (1600, 800), settings["zoom"], position_offset)

            pygame.draw.line(screen, (255, 0, 0), screen_pos1, screen_pos2, 2)

    for planet in planets:
        planet.draw(distance_multi, settings["zoom"], position_offset)
        pass


    center_of_mass = nBodyProblem.get_center_of_mass(planets)
    screen_pos = tools.world_to_screen(center_of_mass, distance_multi, (1600, 800), settings["zoom"], position_offset)
    pygame.draw.circle(screen, (0, 255, 0),
                       [screen_pos[0], screen_pos[1]], 1)

    timeText = my_font.render('Delta Time: '+str(settings["delta_time"]), False, (255, 255, 255))
    zoomText = my_font.render('Zoom: '+str(settings["zoom"]), False, (255, 255, 255))
    totalTimeText = my_font.render('Total Time: '+str(round(totalTime/60/60/24,8)), False, (255, 255, 255))
    screen.blit(timeText, (0, 0))
    screen.blit(zoomText, (0, 30))
    screen.blit(totalTimeText, (0, 60))


    pygame.display.flip()


    clock.tick(240)  # limits FPS to 60

pygame.quit()