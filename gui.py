from tkinter import *
from PIL import ImageTk, Image
from vectors import Vector, radiansToDegrees
import numpy as np

def abs(a):
    return (a >= 0) * a + (a < 0) * (-1) * a

class App(Frame):
    def __init__(self, master=Tk(), width=500, height=500, x_axis_scale=100, y_axis_scale=100, drag_scale=0.01, scroll_scale = 0.1,
                 markings_space = 1, lower_bound = -1, upper_bound = 1, small_step = 0.05,
                 generate_axis = False, generate_markings = False, x_marking = True, y_marking = True, z_marking = True,
                 x_color = "red", y_color = "blue", z_color = "green", title="3D viewer - tkinter and numpy"
                 ):

        #App and windows settings
        Frame.__init__(self, master)
        self.master = master
        master.title(title)
        self.width = width
        self.height = height
        self.x_color = x_color
        self.y_color = y_color
        self.z_color = z_color

        self.lower_bound = lower_bound  # of axis
        self.upper_bound = upper_bound  # of axis
        self.small_step = small_step # defult value of dx/dy/dz
        self.generate_axis = generate_axis
        self.generate_markings = generate_markings
        self.markings_space = markings_space
        self.x_marking = x_marking
        self.y_marking = y_marking
        self.z_marking = z_marking

        #Bind Actions to keys
        self.master.bind('<Key>', lambda e: self.keyPress(e))
        self.master.bind('<KeyRelease>', lambda e: self.keyRelease(e))
        self.master.bind('<Button-1>', lambda e: self.clickScreen(e))
        self.master.bind('<B1-Motion>', lambda e: self.dragScreen(e))
        self.master.bind('<MouseWheel>', lambda e: self.scrollScreen(e))
        self.master.bind("<Escape>", lambda x: master.destroy())

        #Create canvas for 3d
        self.app_canvas = Canvas(master, height=self.height, width=self.width, bg='grey')
        self.all_vectors = []

        #3d person viewing settings
        self.x_axis_scale = x_axis_scale #How much to scale the screen X axis
        self.y_axis_scale = y_axis_scale #How much to scale the screen Y axis
        self.root_point = np.array([self.width / 2, self.height / 2]) #Where the (0,0) of the screen X and Y axis is located
        self.drag_scale = drag_scale #How Sensitive the changes to the mouse drag
        self.scroll_scale = scroll_scale

        #Where camera is located in the app world
        self.camera_vector = Vector([0,0,0],[0,0,1], display_on_screen=False, color='Blue')

        #Where player clicks on the screen canvas
        self.screen_x = 0
        self.screen_y = 0

        #What the X and Y vectors on the screen represent in the app
        self.screen_x_vector = Vector([0,0,0],[1,0,0], display_on_screen=False) #What the X axis of the monitor represents
        self.screen_y_vector = Vector([0,0,0],[0,1,0], display_on_screen=False) #What the Y axis of the monitor represents

        #Create Axis Lines X/Y/Z
        if (self.generate_axis == True):
            self.generateAxis()

        #Create Ticks on X/Y/Z
        if (self.generate_markings == True):
            self.generateMarkLines()

    def clickScreen(self, e):
        self.screen_x = e.x
        self.screen_y = e.y

    def scrollScreen(self, e):
        delta = e.delta / 120
        self.modifyVectors(scale= 1 + delta * self.scroll_scale)

    def dragScreen(self, e):
        diff_x = e.x - self.screen_x
        diff_y = e.y - self.screen_y

        #The camera vector rotates around the screen_x_vector with diff_y and around the screen_y_vector with diff_x

        #The camera is perpendicular to the XY plane
        self.camera_vector.vector = np.cross(self.screen_x_vector.vector, self.screen_y_vector.vector)

        #Modify all vectors according to the screen drage
        self.modifyVectors(diff_x, diff_y)

        #Assign current x, y to where the player last clicked
        self.screen_x = e.x
        self.screen_y = e.y

    def changeCameraAngle(self, x_vector, y_vector, camera_vector):

        if x_vector != [0,0,0]:
            self.screen_x_vector.end_point[0] = x_vector[0]
            self.screen_x_vector.end_point[1] = x_vector[1]
            self.screen_x_vector.end_point[2] = x_vector[2]

        if y_vector != [0,0,0]:
            self.screen_y_vector.end_point[0] = y_vector[0]
            self.screen_y_vector.end_point[1] = y_vector[1]
            self.screen_y_vector.end_point[2] = y_vector[2]

        if camera_vector != [0,0,0]:
            self.camera_vector.end_point[0] = camera_vector[0]
            self.camera_vector.end_point[1] = camera_vector[1]
            self.camera_vector.end_point[2] = camera_vector[2]

        screen_vectors = [self.screen_x_vector, self.screen_y_vector, self.camera_vector]

        for v in Vector.all_vectors:
            if v not in screen_vectors:
                pass


    def keyPress(self, e):
        #Walk Down
        if e.char == 's' or e.char == 'S':
            self.modifyVectors(move_y=1)

        #Walk Up
        elif e.char == 'w' or e.char == 'W':
            self.modifyVectors(move_y=-1)

        #Walk left
        elif e.char == 'a' or e.char == 'A':
            self.modifyVectors(move_x=1)

        #Walk right
        elif e.char == 'd' or e.char == 'D':
            self.modifyVectors(move_x=-1)

        elif e.char == 'z' or e.char == 'Z':
            self.changeCameraAngle([1,0,0], [0,1,0], [0,0,1])

    def keyRelease(self, e):
        #print (e.char, 'KeyRelease')
        pass

    def packObjects(self):
        self.app_canvas.pack(fill="both", expand=True)

    def modifyVectors(self, diff_x=0, diff_y=0, move_x=0, move_y=0, move_z=0, scale=1):
        screen_vectors = [self.screen_x_vector, self.screen_y_vector, self.camera_vector]

        #Start with screen_vectors
        for v in screen_vectors:
            self.modifySingleVector(v=v, diff_x=diff_x, diff_y=diff_y, move_x=move_x, move_y=move_y, move_z=move_z, screen_vectors=screen_vectors, scale=scale)

        #Then on to all other vectors
        for v in self.all_vectors:
            if v not in screen_vectors:
                self.modifySingleVector(v=v, diff_x=diff_x, diff_y=diff_y, move_x=move_x, move_y=move_y, move_z=move_z, screen_vectors=screen_vectors, scale=scale)


    def modifySingleVector(self, v=Vector([0,0,0], [0,0,0]), diff_x=0, diff_y=0, move_x=0, move_y=0, move_z=0, screen_vectors=[], scale = 1):
        #Scale vector if user scrolled mouse
        v.start_point[0] *= scale
        v.start_point[1] *= scale
        v.start_point[2] *= scale

        v.end_point[0] *= scale
        v.end_point[1] *= scale
        v.end_point[2] *= scale

        # Rotate Vector according to the current screen_x/y axis
        if diff_x != 0:
            v.rotateAroundAnotherVector(axis_vector=self.screen_y_vector, angle_of_rotation=diff_x)
        if diff_y != 0:
            v.rotateAroundAnotherVector(axis_vector=self.screen_x_vector, angle_of_rotation=diff_y)

        if v not in screen_vectors:
            #If objects are moving
            if move_x != 0:
                v.start_point += self.screen_x_vector.vector * move_x
                v.end_point += self.screen_x_vector.vector * move_x

            if move_y != 0:
                v.start_point += self.screen_y_vector.vector * move_y
                v.end_point += self.screen_y_vector.vector * move_y

            #Modify the 2d representation of the vector in a 3d space

            #Set start point and end point Vectors
            start_point_vector = Vector(end_point=v.start_point, temp_vector=True)
            end_point_vector = Vector(end_point=v.end_point, temp_vector=True)

            #Get 2d coordinates of the start and the end of the 2d vector on that plane
            v.screen_start_point = start_point_vector.get2dCoordinates(self.screen_x_vector, self.screen_y_vector)
            v.screen_end_point = end_point_vector.get2dCoordinates(self.screen_x_vector, self.screen_y_vector)

            scale_x = self.x_axis_scale
            scale_y = self.y_axis_scale
            root_point_x = self.root_point[0]
            root_point_y = self.root_point[1]
            x1 = -1 * v.screen_start_point [0]
            y1 = v.screen_start_point[1]
            x2 = -1 * v.screen_end_point[0]
            y2 = v.screen_end_point[1]
            self.app_canvas.coords(v.canvas_object,
                    #X1, Y1
                    root_point_x - x1 * scale_x, root_point_y - y1 * scale_y,

                    #X2, Y2
                    root_point_x - x2 * scale_x, root_point_y - y2 * scale_y
            )

            #Vector.deleteAllTempVecotrs(Vector)

    def generateVectors(self):
        for v in Vector.all_vectors:
            if v.display_on_screen == True:

                scale_x = self.x_axis_scale
                scale_y = self.y_axis_scale
                root_point_x = self.root_point[0]
                root_point_y = self.root_point[1]

                x1 = v.screen_start_point[0]
                y1 = v.screen_start_point[1]
                x2 = v.screen_end_point[0]
                y2 = v.screen_end_point[1]

                arrow_option = NONE
                if (v.arrow == True):
                    arrow_option = LAST

                #If the vector on this plane equals 0 create a little line
                if (x2 != x1 or y2 != y2):
                    v.canvas_object = self.app_canvas.create_line(
                        # X1, Y1
                        root_point_x - x1 * scale_x, root_point_y - y1 * scale_y,

                        # X2, Y2
                        root_point_x - x2 * scale_x, root_point_y - y2 * scale_y,

                        fill=v.color, arrow=arrow_option, width=v.line_width
                    )

                else:
                    v.canvas_object = self.app_canvas.create_line(0, 0, 1, 1, fill=v.color, arrow=arrow_option)

                self.all_vectors.append(v)

    def generateAxis(self):
        x_axis = Vector([self.lower_bound, 0, 0], [self.upper_bound, 0, 0], color=self.x_color, arrow=True)
        y_axis = Vector([0, self.lower_bound, 0], [0, self.upper_bound, 0], color=self.y_color, arrow=True)
        z_axis = Vector([0, 0, self.lower_bound], [0, 0, self.upper_bound], color=self.z_color, arrow=True)

    def generateMarkLines(self):
        small_step = self.small_step
        lower_bound = self.lower_bound
        upper_bound = self.upper_bound
        x = lower_bound
        y = lower_bound
        z = lower_bound

        smaller_axis_scaler = 1.5

        while (x != upper_bound and self.x_marking):
            if x != 0:
                if (x % 1 == 0):
                    Vector([x, small_step, 0], [x, (-1) * small_step, 0], color=self.x_color)
                    Vector([x, 0, small_step], [x, 0, (-1) * small_step], color=self.x_color)
                else:
                    Vector([x, small_step * smaller_axis_scaler, 0], [x, (-1) * small_step * smaller_axis_scaler , 0], color=self.x_color)
                    Vector([x, 0, small_step * smaller_axis_scaler], [x, 0, (-1) * small_step * smaller_axis_scaler ], color=self.x_color)

            x += self.markings_space

        while (y != upper_bound and self.y_marking):
            if y != 0:
                if (y % 1 == 0):
                    Vector([small_step, y, 0], [(-1) * small_step, y, 0], color=self.y_color)
                    Vector([0, y, small_step], [0, y, (-1) * small_step], color=self.y_color)
                else:
                    Vector([small_step * smaller_axis_scaler, y, 0], [(-1) * small_step * smaller_axis_scaler, y, 0], color=self.y_color)
                    Vector([0, y, small_step * smaller_axis_scaler], [0, y, (-1) * small_step * smaller_axis_scaler], color=self.y_color)

            y += self.markings_space

        while (z != upper_bound and self.z_marking):
            if z != 0:
                if (z % 1 == 0):
                    Vector([small_step, 0, z], [(-1) * small_step, 0, z], color=self.z_color)
                    Vector([0, small_step, z], [0, (-1) * small_step, z], color=self.z_color)
                else:
                    Vector([small_step * smaller_axis_scaler, 0, z], [(-1) * small_step * smaller_axis_scaler, 0, z], color=self.z_color)
                    Vector([0, small_step * smaller_axis_scaler, z], [0, (-1) * small_step * smaller_axis_scaler, z], color=self.z_color)

            z += self.markings_space
