import math
from dataclasses import dataclass
import numpy as np
import whoKnowsWhatNow, pygame, positioning
from positioning import world_to_screen


@dataclass
class Planet:
    name: str
    verlet_object: whoKnowsWhatNow.PhysicsObject
    force: np.ndarray
    mass: float
    radius: float
    color: str

    def update(self, delta_time):
        self.verlet_object.acceleration = self.force
        self.verlet_object.update(delta_time)
        self.force = np.zeros_like(self.force)


    def draw(self, distance_multi, zoom = 1, movement = np.array([0, 0])):
        screen_dimensions = pygame.display.get_surface().get_size()
        screen_pos = world_to_screen(self.verlet_object.current_position, distance_multi, screen_dimensions, zoom, movement)
        pygame.draw.circle(pygame.display.get_surface(), self.color, screen_pos, math.ceil(self.radius*zoom))


