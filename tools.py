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

def apply_movement(pos, movement):
    return pos + movement

def apply_zoom(pos, zoom):
    return pos * zoom

def to_screen(pos, distance_multi, screen_dimensions):
    return (pos / distance_multi) + (np.array([screen_dimensions[0], screen_dimensions[1]]) / 2.0)

def world_to_screen(pos, distance_multi, screen_dimensions, zoom = 1, movement = np.array([0,0])):
    return to_screen(apply_zoom(apply_movement(pos, movement), zoom), distance_multi, screen_dimensions)