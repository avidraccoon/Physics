from dataclasses import dataclass
import numpy as np
import verlet

@dataclass
class Planet:
    name: str
    verlet_object: verlet.VerletObject
    mass: float
    radius: float
    color: str


