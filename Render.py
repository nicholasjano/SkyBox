import math, pygame, random
import Planets
# angles are all in radians

def sortByDistance(newThing):
    return newThing[2].vcoords[1]

def rotate2(v1, v2, angle):
    if angle < 0:
        angle = math.pi*2+angle%(math.pi*2)
    elif angle >= math.pi*2:
        angle = angle%(math.pi*2)
    
    v11 = math.cos(angle)*v1
    v12 = math.sin(angle)*v1
    v21 = math.cos(angle)*v2
    v22 = math.sin(angle)*v2
    return v11-v22, v12+v21


class Grid(object):
    def __init__(self):
        self.stuff = []
    def translate(self, translation):
        for thing in self.stuff:
            thing.vcoords[0] += translation[0]
            thing.vcoords[1] += translation[1]
            thing.vcoords[2] += translation[2]
    def rotate(self, anglex, angley):
        for thing in self.stuff:
            thing.vcoords[1], thing.vcoords[0] = rotate2(thing.vcoords[1], thing.vcoords[0], anglex)
            thing.vcoords[1], thing.vcoords[2] = rotate2(thing.vcoords[1], thing.vcoords[2], angley)
            
        


class perspective(object):
    def __init__(self, ratio, anglex, angley, coords, size):
        self.ratio = ratio
        self.anglex = anglex
        self.angley = angley
        self.coords = coords
        self.size = size
        self.grid = Grid()
        self.newThings = []
        self.starChunk = []
        for i in range(100):
            self.starChunk.append([random.randrange(1000), random.randrange(1000)])
        self.starx = 0
        self.stary = 0

    def loadFromFile(self, file):
        f = open(file, "r")
        planetStats = eval(f.read())
        f.close()
        self.grid.stuff = []
        for stat in planetStats:
            thing = Planets.Entity(stat[0], stat[1], stat[2], stat[3], stat[4], stat[5])
            thing.movable = stat[6]
            self.grid.stuff.append(thing)
    def saveToFile(self, file):
        planetStats = []
        for thing in self.grid.stuff:
            planetStats.append([thing.coords, thing.velocity, thing.mass, thing.radius, thing.color, thing.entityType, thing.movable])
        f = open(file, "w+")
        f.write(str(planetStats))
        f.close
        
    def getFlatCoords(self, EntityList):
        newThings = []
        for thing in self.grid.stuff:
            if thing.vcoords[1] < -0.1:
                newThings.append([thing.vcoords[0] * (self.ratio / (thing.vcoords[1]*-1)), thing.vcoords[2] * (self.ratio / (thing.vcoords[1]*-1)), thing])
        newThings.sort(key = sortByDistance)
        self.newThings = newThings
        return newThings
    def draw(self, win, newThings):
        if self.starx > 1000:
            self.starx -= 1000
        elif self.starx < -1000:
            self.starx += 1000
        if self.stary > 1000:
            self.stary -= 1000
        elif self.stary < -1000:
            self.stary += 1000

        for x in range(3):
            for y in range(3):
                for star in self.starChunk:
                    win.fill((255, 255, 255), pygame.Rect(x*1000+star[0]+self.starx-1000, y*1000+star[1]+self.stary-1000, 1, 1))
        
        for thing in newThings:
            x = thing[0]*self.size[0]/2 + self.size[0]/2
            y = (-thing[1])*self.size[0]/2 + self.size[1]/2
            rad = (thing[2].radius / (-thing[2].vcoords[1]))*self.size[0]/2
            
            pygame.draw.circle(win, (round(thing[2].color[0]), round(thing[2].color[1]), round(thing[2].color[2])), (int(x), int(y)), int(rad))
            if thing[2].entityType == 1:
                pygame.draw.line(win,(255-round(thing[2].color[0]), 255-round(thing[2].color[1]), 255-round(thing[2].color[2])),(int(x), int(y)), (int(x+math.sin(math.pi/2)*rad*1/3), int(y+math.sin(math.pi/2)*rad*1/3)))
                pygame.draw.line(win,(255-round(thing[2].color[0]), 255-round(thing[2].color[1]), 255-round(thing[2].color[2])),(int(x), int(y)), (int(x-math.sin(math.pi/2)*rad*1/3), int(y+math.sin(math.pi/2)*rad*1/3)))
                pygame.draw.line(win,(255-round(thing[2].color[0]), 255-round(thing[2].color[1]), 255-round(thing[2].color[2])),(int(x), int(y)), (int(x+math.sin(math.pi/2)*rad*1/3), int(y-math.sin(math.pi/2)*rad*1/3)))
                pygame.draw.line(win,(255-round(thing[2].color[0]), 255-round(thing[2].color[1]), 255-round(thing[2].color[2])),(int(x), int(y)), (int(x-math.sin(math.pi/2)*rad*1/3), int(y-math.sin(math.pi/2)*rad*1/3)))
                pygame.draw.line(win,(255-round(thing[2].color[0]), 255-round(thing[2].color[1]), 255-round(thing[2].color[2])),(int(x), int(y)), (int(x), int(y+rad*4/5)))
                pygame.draw.line(win,(255-round(thing[2].color[0]), 255-round(thing[2].color[1]), 255-round(thing[2].color[2])),(int(x), int(y)), (int(x), int(y-rad*4/5)))
                pygame.draw.line(win,(255-round(thing[2].color[0]), 255-round(thing[2].color[1]), 255-round(thing[2].color[2])),(int(x), int(y)), (int(x+rad*4/5), int(y)))
                pygame.draw.line(win,(255-round(thing[2].color[0]), 255-round(thing[2].color[1]), 255-round(thing[2].color[2])),(int(x), int(y)), (int(x-rad*4/5), int(y)))
            if thing[2].selected:
                pygame.draw.circle(win, (255-round(thing[2].color[0]), 255-round(thing[2].color[1]), 255-round(thing[2].color[2])), (int(x), int(y)), int(rad/3))
            thing[2].clickRad = int(rad)
            thing[0] = int(x)
            thing[1] = int(y)
    def drawPerspective(self, win):
        for thing in self.grid.stuff:
            thing.vcoords = thing.coords[:]
        self.grid.translate([-self.coords[0], -self.coords[1], -self.coords[2]])
        
        self.grid.rotate(self.anglex, self.angley)
        self.draw(win, self.getFlatCoords(self.grid.stuff))
    def move(self, direction, n):
        lookVector = [0, 0, 0]
        if direction == "forward":
            lookVector[1] -= n
        elif direction == "backward":
            lookVector[1] += n
        elif direction == "right":
            lookVector[0] += n
        elif direction == "left":
            lookVector[0] -= n
        elif direction == "up":
            lookVector[2] += n
        elif direction == "down":
            lookVector[2] -= n
        lookVector[1], lookVector[0] = rotate2(lookVector[1], lookVector[0], self.anglex)
        lookVector[1], lookVector[2] = rotate2(lookVector[1], lookVector[2], self.angley)
        if direction == "forward" or direction == "backward":
            self.coords[0] -= lookVector[0]

            self.coords[1] += lookVector[1]
            self.coords[2] -= lookVector[2]
        else:
            self.coords[0] += lookVector[0]

            self.coords[1] -= lookVector[1]
            self.coords[2] += lookVector[2]
    def checkLook(self):
        lookVector = [0, -1, 0]
        lookVector[1], lookVector[0] = rotate2(lookVector[1], lookVector[0], self.anglex)
        lookVector[1], lookVector[2] = rotate2(lookVector[1], lookVector[2], self.angley)
        return lookVector
    def turn(self, pos1, pos2):
        x = pos2[0] - pos1[0]
        y = - pos2[1] + pos1[1]
        self.anglex += x/1000*1.5
        self.angley += y/1000*1.5
        if self.anglex >= math.pi*2:
            self.anglex -= math.pi*2
        if self.angley >= math.pi*2:
            self.angley -= math.pi*2
        self.starx += -x
        self.stary += y
        
            
    
        
