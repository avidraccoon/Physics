from dataclasses import dataclass
import numpy as np

@dataclass
class VerletObject:
    current_position: np.ndarray
    old_position: np.ndarray
    acceleration: np.ndarray

    def update(self, delta_time):
        velocity = self.current_position - self.old_position
        self.old_position = self.current_position
        self.current_position += velocity * delta_time + self.acceleration * delta_time * delta_time
        self.acceleration = np.zeros_like(self.current_position)