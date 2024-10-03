import numpy as np

def apply_movement(pos, movement):
    return pos + movement

def apply_zoom(pos, zoom):
    return pos * zoom

def to_screen(pos, distance_multi, screen_dimensions):
    return (pos / distance_multi) + (np.array([screen_dimensions[0], screen_dimensions[1], 800]) / 2.0)

def world_to_screen(pos, distance_multi, screen_dimensions, zoom = 1, movement = np.array([0,0, 0])):
    return to_screen(apply_zoom(apply_movement(pos, movement), zoom), distance_multi, screen_dimensions)