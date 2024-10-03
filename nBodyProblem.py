# Example file showing a basic pygame "game loop"
import math

import numpy as np


def update(planets, gravity, delta_time):
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
            planetForce -= gravity * planet2[4] * (difference/cubedAbs) / planet1[4]
        planet1[2] += planetForce[0] * delta_time
        planet1[3] += planetForce[1] * delta_time