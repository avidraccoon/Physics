from dataclasses import dataclass
import numpy as np

@dataclass
class PhysicsObject:
    current_position: np.ndarray
    velocity: np.ndarray
    acceleration: np.ndarray

    def update(self, delta_time):
        self.current_position += self.velocity * delta_time
        self.velocity += self.acceleration * delta_time
        self.acceleration = np.zeros_like(self.acceleration)