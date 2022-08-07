import math

class Entity(object):
    def __init__(self, coords, velocity, mass, radius, color, entityType):
        self.coords = coords
        self.velocity = velocity
        self.mass = mass
        self.radius = radius
        self.color = color
        self.entityType = entityType
        self.vcoords = coords[:]
        self.movable = True
        self.alive = True
        self.selected = False
        self.clickRad = 0
