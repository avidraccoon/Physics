import numpy as np
from dataclasses import dataclass
import tools
import constants
import planet as planetLib

def maximum_possible_radius(time):
    #print(time)
    #print(constants.speed_of_gravity*time)
    return constants.speed_of_gravity * time

@dataclass
class GravityField:
    center: np.ndarray
    mass: float
    max_radius: float
    decaying: bool
    decay_start: float
    time: float

    def contains_point(self, point):
        distance = tools.distance(self.center, point)
        if distance < self.get_current_decay_radius(): return False
        return distance/2 <= self.get_current_radius()

    def get_current_decay_radius(self):
        if not self.decaying: return 0
        return maximum_possible_radius(self.time-self.decay_start)

    def get_current_radius(self):
        current_radius = self.max_radius
        if maximum_possible_radius(self.time) < self.max_radius:
            current_radius = maximum_possible_radius(self.time)
        return current_radius

    def get_affect(self, point, mass):
        if not self.contains_point(point): return 0
        return tools.get_gravitational_force(self.center, point, self.mass, mass)

    def get_force(self, point):
        if not self.contains_point(point): return 0
        return tools.get_gravitational_force(self.center, point, self.mass, 1)

    def is_decayed(self):
        if not self.decaying: return False
        return self.get_current_decay_radius() > self.max_radius

@dataclass
class GravityFieldCluster:
    fields: list[GravityField]
    orgin_planet: planetLib.Planet
    time: float
    disabled: bool = False

    def add_field(self, field: GravityField):
        self.fields.append(field)
        #print(len(self.fields))
        if (len(self.fields)>1):
            if not self.fields[len(self.fields)-2].decaying:
                self.fields[len(self.fields)-2].decaying = True
                self.fields[len(self.fields)-2].decay_start = self.fields[len(self.fields)-2].time
            while self.fields[0].is_decayed():
            #while len(self.fields)>10:
                self.fields.pop(0)

    def update_time(self, time):
        for field in self.fields:
            field.time += time
        self.time += time

    def get_force(self, point):
        if self.disabled: return 0
        largest = 0
        largest_index = -1
        for index in range(len(self.fields)):
            affect = self.fields[index].get_force(point)
            if affect > largest:
                largest = affect
                largest_index = index
        if largest_index == -1: return 0
        return largest


    def get_affect(self, point, mass):
        if self.disabled: return -100
        largest = 0
        largest_index = -1
        for index in range(len(self.fields)):
            affect = self.fields[index].get_affect(point, mass)
            if affect > largest:
                largest = affect
                largest_index = index
        if largest_index == -1: return 0
        return tools.give_velocity_direction(tools.force_to_velocity(largest, mass), point, self.fields[largest_index].center)

@dataclass
class TimeSpaceCurvature:
    clusters: list[GravityFieldCluster]

    def add_cluster(self, cluster: GravityFieldCluster):
        self.clusters.append(cluster)

    def get_force(self, point):
        force = 0.0
        for cluster in self.clusters:
            force += cluster.get_force(point)
        return force

    def get_affect(self, point, mass):
        acceleration = np.array([0.0, 0.0])
        for cluster in self.clusters:
            acceleration += cluster.get_affect(point, mass)
        return acceleration

    def update_time(self, time):
        for cluster in self.clusters:
            cluster.update_time(time)