# Example file showing a basic pygame "game loop"
import math

import numpy as np
import planet as planetLib

def update(planets, gravity, delta_time):
    for index1 in range(len(planets)):
        planet1 = planets[index1]
        planet_force = np.array([0.0, 0.0])
        for index2 in range(len(planets)):
            if index1 == index2:
                continue
            planet2 = planets[index2]
            difference = planet1.verlet_object.current_position - planet2.verlet_object.current_position
            cubed_abs = np.linalg.norm(difference)**3
            planet_force -= gravity * planet2.mass * (difference/cubed_abs)
        planet1.force = planet_force[0]
        planet1.force = planet_force[1]
        print(planet_force)

def get_center_of_mass(planets):
    total_mass = 0
    total_pos = np.array([0.0, 0.0])
    for planet in planets:
        total_mass += planet.mass
        total_pos += planet.verlet_object.current_position * planet.mass
    return total_pos / total_mass