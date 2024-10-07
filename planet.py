import math, tools
from dataclasses import dataclass
import numpy as np
import PhysicsObjects, pygame


@dataclass
class Planet:
    name: str
    verlet_object: PhysicsObjects.PhysicsObject
    mass: float
    radius: float
    color: str

    def update(self, delta_time):
        self.verlet_object.update(delta_time)

    def draw(self, distance_multi, zoom = 1, movement = np.array([0, 0, 0])):
        screen_dimensions = pygame.display.get_surface().get_size()
        screen_pos = tools.world_to_screen(self.verlet_object.position, distance_multi, screen_dimensions, zoom, movement)
        pygame.draw.circle(pygame.display.get_surface(), self.color, [screen_pos[0], screen_pos[1]], math.ceil(self.radius*zoom))


