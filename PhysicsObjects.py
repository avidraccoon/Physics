from dataclasses import dataclass, field
import numpy as np


@dataclass
class PhysicsObject:
    _position: np.ndarray
    _velocity: np.ndarray
    _acceleration: np.ndarray

    @property
    def position(self):
        return self._position

    @property
    def velocity(self):
        return self._velocity

    @property
    def acceleration(self):
        return self._acceleration

    @position.setter
    def position(self, position):
        self._position = position

    @velocity.setter
    def velocity(self, velocity):
        self._velocity = velocity

    @acceleration.setter
    def acceleration(self, acceleration):
        self._acceleration = acceleration

    def update(self, delta_time):
        pass

class EulerPhysicsObject(PhysicsObject):

    def update(self, delta_time):
        self.position += self.velocity * delta_time
        self.velocity += self.acceleration * delta_time
        self.acceleration = np.zeros_like(self.acceleration)

@dataclass
class VerletPhysicsObject(PhysicsObject):
    _old_position: np.ndarray = field(init=False)

    def __post_init__(self):
        self._old_position = self.position

    @property
    def old_position(self):
        return self._old_position

    @old_position.setter
    def old_position(self, position):
        self._old_position = position

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, velocity):
        self.position = self.position + velocity

    def update(self, delta_time):
        self.velocity = self.position - self.old_position
        self.old_position = np.array(self.position)
        self.position = self.position + self.velocity * delta_time + self.acceleration * delta_time
        self.acceleration = np.zeros_like(self.acceleration)
