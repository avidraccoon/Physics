# Example file showing a basic pygame "game loop"
import math

import numpy as np
from numpy.ma.core import absolute

import planet as planetLib

def force_to_velocity(force, mass):
    return force / mass

def get_gravitational_force(position1, position2, mass1, mass2, gravity):
    difference = position2 - position1
    distance = np.sqrt(difference[0] ** 2 + difference[1] ** 2 + difference[2] ** 2)
    return gravity * mass1 * mass2 / (distance**2)

def give_velocity_direction(velocity, position1, position2):
    difference = position2 - position1
    distance = np.sqrt(difference[0] ** 2 + difference[1] ** 2 + difference[2] ** 2)
    return velocity * difference / distance

def update(planets, gravity, delta_time):
    for index1 in range(len(planets)):
        planet1 = planets[index1]
        planet_force = np.array([0.0, 0.0, 0.0])
        for index2 in range(len(planets)):
            if index1 == index2:
                continue
            planet2 = planets[index2]
            force = get_gravitational_force(planet1.verlet_object.current_position, planet2.verlet_object.current_position, planet1.mass, planet2.mass, gravity)
            velocity = force_to_velocity(force, planet1.mass)
            velocity_with_direction = give_velocity_direction(velocity, planet1.verlet_object.current_position, planet2.verlet_object.current_position)
            planet_force += velocity_with_direction
        planet1.verlet_object.acceleration = planet_force
        #print(planet_force)

def get_center_of_mass(planets):
    total_mass = 0
    total_pos = np.array([0.0, 0.0, 0.0])
    for planet in planets:
        total_mass += planet.mass
        total_pos += planet.verlet_object.current_position * planet.mass
    return total_pos / total_mass