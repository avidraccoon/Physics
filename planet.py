from dataclasses import dataclass
import numpy as np

@dataclass
class Planet:
    name: str
    position: np.ndarray
    velocity: np.ndarray
    acceleration: np.ndarray
    mass: float
    radius: float
    color: str


