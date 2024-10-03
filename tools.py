import numpy as np
import constants

def distance(point1, point2):
    return np.sqrt(pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2))

def get_gravitational_force(position1, position2, mass1, mass2):
    difference = position2 - position1
    distance = np.sqrt(difference[0] ** 2 + difference[1] ** 2)
    if (distance <= 1): return 0
    return constants.gravity * mass1 * mass2 / (distance**2)

def force_to_velocity(force, mass):
    return force / mass

def give_velocity_direction(velocity, position1, position2):
    difference = position2 - position1
    distance = np.sqrt(difference[0] ** 2 + difference[1] ** 2)
    return velocity * difference / distance