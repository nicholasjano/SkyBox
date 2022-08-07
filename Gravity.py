
import math

def distanceTwoPoints(point1,point2):
    return (((point1[0]-point2[0])**2)+((point1[1]-point2[1])**2)+((point1[2]-point2[2])**2))**(1/2)



gravity = 0.0004

#self.coords = coords
#self.velocity = velocity
#self.mass = mass
#self.radius = radius
#self.color = color
#self.entityType = entityType
#self.movable = movable? (bool)

def newPositions(bodies, delete, gravityNew):
    if gravityNew != None:
        gravity = gravityNew

    else:
        gravity = 0.0004
        
    if not delete:
        for i in range(len(bodies)):
            if bodies[i].alive != False:
                for j in range (len(bodies)):
                    if i != j:
                        if distanceTwoPoints(bodies[i].coords, bodies[j].coords) >= (bodies[i].radius + bodies[j].radius):

                            forces = [0,[0,0]] #[Magnitude, Direction]
                            forces[0] = abs((gravity*bodies[i].mass*bodies[j].mass)/(distanceTwoPoints(bodies[i].coords, bodies[j].coords)**2)) #Magnitude
                            
                            if bodies[i].coords[1] == bodies[j].coords[1]:
                                forces[1][0] = math.pi/2
                            else:
                                forces[1][0] = math.atan((bodies[j].coords[0]-bodies[i].coords[0])/(bodies[j].coords[1]-bodies[i].coords[1]))

                            if ((((bodies[j].coords[0]-bodies[i].coords[0])**2) + ((bodies[j].coords[0]-bodies[i].coords[0])**2))**(1/2)) == 0:
                                forces[1][1] = math.pi/2
                            else:
                                forces[1][1] = math.atan((bodies[j].coords[2]-bodies[i].coords[2])/((((bodies[j].coords[0]-bodies[i].coords[0])**2) + ((bodies[j].coords[0]-bodies[i].coords[0])**2)))**(1/2))
                           
                            lowerHyp = forces[0] * math.cos(forces[1][1])
                            
                        
                            if bodies[i].coords[0] < bodies[j].coords[0]:
                                bodies[i].velocity[0] += abs(math.sin(forces[1][0]) * lowerHyp)/bodies[i].mass
                            elif bodies[i].coords[0] > bodies[j].coords[0]:
                                bodies[i].velocity[0] -= abs(math.sin(forces[1][0]) * lowerHyp)/bodies[i].mass
                        
                            if bodies[i].coords[1] < bodies[j].coords[1]:
                                bodies[i].velocity[1] += abs(math.cos(forces[1][0]) * lowerHyp)/bodies[i].mass
                            elif bodies[i].coords[1] > bodies[j].coords[1]:
                                bodies[i].velocity[1] -= abs(math.cos(forces[1][0]) * lowerHyp)/bodies[i].mass

                            if bodies[i].coords[2] < bodies[j].coords[2]:
                                bodies[i].velocity[2] += abs(math.sin(forces[1][1]) * forces[0])/bodies[i].mass
                            elif bodies[i].coords[2] > bodies[j].coords[2]:
                                bodies[i].velocity[2] -= abs(math.sin(forces[1][1]) * forces[0])/bodies[i].mass

                        else: #Collision
                            if bodies[j].movable == False and bodies[i].movable == True: #New body is not movable
                                temp = bodies[i]
                                bodies[i] = bodies[j]
                                bodies[j] = temp
                            bodies[i].radius = (bodies[i].radius**2 + bodies[j].radius**2)**(1/2)
                            bodies[i].velocity[0] = ((bodies[i].velocity[0]*(bodies[i].mass/(bodies[i].mass+bodies[j].mass))) + (bodies[j].velocity[0]*(bodies[j].mass/(bodies[i].mass+bodies[j].mass))))/2
                            bodies[i].velocity[1] = ((bodies[i].velocity[1]*(bodies[i].mass/(bodies[i].mass+bodies[j].mass))) + (bodies[j].velocity[1]*(bodies[j].mass/(bodies[i].mass+bodies[j].mass))))/2
                            bodies[i].velocity[2] = ((bodies[i].velocity[2]*(bodies[i].mass/(bodies[i].mass+bodies[j].mass))) + (bodies[j].velocity[2]*(bodies[j].mass/(bodies[i].mass+bodies[j].mass))))/2

                            if bodies[i].entityType == bodies[j].entityType:
                                bodies[i].color[0] = ((bodies[i].color[0]*bodies[i].mass/(bodies[i].mass + bodies[j].mass)) + (bodies[j].color[0]*bodies[j].mass/(bodies[i].mass + bodies[j].mass)))
                                bodies[i].color[1] = ((bodies[i].color[1]*bodies[i].mass/(bodies[i].mass + bodies[j].mass)) + (bodies[j].color[1]*bodies[j].mass/(bodies[i].mass + bodies[j].mass)))
                                bodies[i].color[2] = ((bodies[i].color[2]*bodies[i].mass/(bodies[i].mass + bodies[j].mass)) + (bodies[j].color[2]*bodies[j].mass/(bodies[i].mass + bodies[j].mass)))
                            elif bodies[i].entityType > bodies[j].entityType:
                                bodies[i].entityType = bodies[j].entityType
                                bodies[i].color = bodies[j].color[:]
                            
                            bodies[i].mass += bodies[j].mass
                            bodies[j].alive = False #marked for kill

        for i in range(len(bodies)): #Actual movement
            if bodies[i].alive != False and bodies[i].movable == True:

                bodies[i].coords[0] += bodies[i].velocity[0]
                bodies[i].coords[1] += bodies[i].velocity[1]
                bodies[i].coords[2] += bodies[i].velocity[2]

    for i in range(len(bodies)): #Clearing the dead (marked to kill)
        try:
            if bodies[i].alive == False:
                del bodies[i]
        except:
            pass

    for i in bodies: #Clearing the dead (too far)
        for j in range(3):
            if i.coords[j] > 50000 or i.coords[j] < -50000:
                del i
                break
  

