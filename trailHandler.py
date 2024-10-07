
import numpy as np

def updateTrail(trail, pos, max_length):
    trail.append(np.array(pos))
    if len(trail) > max_length:
        trail.pop(0)

def updatePlanetTrails(trails, planets, max_length):
    for i in range(len(trails)):
        updateTrail(trails[i], planets[i].verlet_object.position, max_length)