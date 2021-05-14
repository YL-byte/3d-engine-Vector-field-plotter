from math import acos, degrees
import numpy as np
class Vector:
    def __init__(self,start_point=np.array([0,0,0]), end_point=np.array([0,0,0]),
                 display_on_screen=True, color='black', arrow=False, line_width=1, temp_vector = False):
        self.start_point = np.array(start_point, dtype='float64')
        self.end_point= np.array(end_point, dtype='float64')
        self.screen_start_point = np.array([start_point[0], start_point[0]]) #This is the starting point of the vector on the screen
        self.screen_end_point = np.array([end_point[0], end_point[0]]) #This is the ending point of the vector on the screen
        self.display_on_screen = display_on_screen
        self.vector = np.array(self.end_point -self.start_point) #This vector does not change
        self.length = self.calculateLength()
        self.canvas_object = None #This is the line on the app
        self.color = color
        self.arrow = arrow
        self.line_width = line_width
        if (temp_vector):
            Vector.temp_vectors.append(self)
        else:
            Vector.all_vectors.append(self)

    def countAllVectors(self):
        counter = 0
        for _ in self.all_vectors:
            counter += 1
        return counter

    def calculateLength(self):
        return (sum(self.vector ** 2)) ** 0.5

    def updateVector(self):
        self.vector = np.array(self.end_point -self.start_point)

    def calculateAngle(self, compared_vector):
        dot_product = np.dot(self.vector, compared_vector.vector)
        return acos(dot_product / (self.length * compared_vector.length))

    def projectOnVector(self, compared_vector):
        compared_vector.length = compared_vector.calculateLength()
        projected_vector = (np.dot(self.vector, compared_vector.vector) / compared_vector.length ** 2) * compared_vector.vector
        return projected_vector

    def projectOnPlane(self, x_vector, y_vector):
        #Get the normal vector -> perpendicular to the pla e
        normal_vector = np.cross(x_vector.vector, y_vector.vector)
        normal_vector = Vector([0,0,0], normal_vector, temp_vector=True)
        normal_vector.length = normal_vector.calculateLength()

        #The projected vector is the original vector - the perpendicular vetor
        projected_vector = self.projectOnVector(normal_vector)

        return self.vector - projected_vector

    def get2dCoordinates(self, x_unit_vector, y_unit_vector):

        #Project the vector on the screen and get the projected vector
        screen_vector = self.projectOnPlane(x_unit_vector, y_unit_vector)

        #If the screen vector is ZERO vector
        if (screen_vector == np.array([0,0,0])).all():
            return np.array([0, 0])

        #project screen_vector on X and Y
        x_vector = self.projectOnVector(x_unit_vector)
        y_vector = self.projectOnVector(y_unit_vector)

        #How many units to travel on each axis depends on the scale
        x_position = (x_vector[0] / x_unit_vector.vector[0])
        y_position = (y_vector[1] / y_unit_vector.vector[1])

        return np.array([x_position, y_position])

    def normalizeVector(self):
        #A normalized vector is a unit vector with length 1
        self.length = self.calculateLength()

        if (self.length != 0):
            self.vector[0] /= self.length
            self.vector[1] /= self.length
            self.vector[2] /= self.length
            self.length = self.calculateLength()

    def rotateAroundAnotherVector(self, axis_vector, angle_of_rotation=0):
        axis_vector.normalizeVector()
        ux = axis_vector.vector[0]
        uy = axis_vector.vector[1]
        uz = axis_vector.vector[2]
        a = degreesToRadians(angle_of_rotation)
        rotating_matrix = np.array([

[np.cos(a) + ux*ux * (1 - np.cos(a)),    ux*uy*(1 - np.cos(a)) - uz*np.sin(a),    ux*uz*(1 - np.cos(a)) + uy*np.sin(a)],
[uy*ux*(1 - np.cos(a)) + uz*np.sin(a),   np.cos(a) + uy*uy*(1 - np.cos(a)),       uy*uz*(1 - np.cos(a)) - ux*np.sin(a)],
[uz*ux*(1 - np.cos(a)) - uy*np.sin(a),   uz*uy*(1 - np.cos(a)) + ux*np.sin(a),    np.cos(a) + uz*uz*(1 - np.cos(a))],

                                    ])
        self.vector = self.vector.dot(rotating_matrix)

    def rotateVector(self, x=0, y=0, z=0):
        if x != 0:
            x = degreesToRadians(x)
            self._rotateVectorX(x)
        if y != 0:
            y = degreesToRadians(y)
            self._rotateVectorY(y)
        if z != 0:
            z = degreesToRadians(z)
            self._rotateVectorZ(z)

        #Update end points of the vector
        self.end_point = self.start_point + self.vector

    def _rotateVectorX(self, angle_of_rotation):
        a = angle_of_rotation
        rotating_matrix = np.array([
                                    [1,     0,              0],
                                    [0,     np.cos(a),      -1 * np.sin(a)],
                                    [0,     np.sin(a),      np.cos(a)]
                                    ])
        self.vector = self.vector.dot(rotating_matrix)

    def _rotateVectorY(self, angle_of_rotation):
        a = angle_of_rotation
        rotating_matrix = np.array([
                                    [np.cos(a),      0,     np.sin(a)],
                                    [0,              1,     0],
                                    [-1 * np.sin(a), 0,     np.cos(a)]
                                    ])
        self.vector = self.vector.dot(rotating_matrix)

    def _rotateVectorZ(self, angle_of_rotation):
        a = angle_of_rotation
        rotating_matrix = np.array([
                                    [np.cos(a), -1 * np.sin(a), 0],
                                    [np.sin(a), np.cos(a),      0],
                                    [0,         0,              1]
                                    ])
        self.vector = self.vector.dot(rotating_matrix)

    def deleteAllTempVecotrs(self):
        for v in Vector.temp_vectors:
            del v

    all_vectors = []

    temp_vectors = []

def degreesToRadians(degrees):
    return (degrees * np.pi ) / 180

def radiansToDegrees(radians):
    return (radians * 180) / np.pi