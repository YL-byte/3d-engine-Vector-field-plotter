from gui import App, Vector
from math import cos, sin, tan, pi, e

def curve(curve_function, t_start = 0, t_end = 0, small_step = 0.1, arrow = False, color="black"):
    t = t_start
    while (t < t_end):
        x, y, z = curve_function(t)
        dx, dy, dz = curve_function(t + small_step)
        dx = (dx - x) / small_step
        dy = (dy - y) / small_step
        dz = (dz - z) / small_step
        size = (dx ** 2 + dy ** 2 + dz ** 2) ** 0.5
        if (size != 0):
            Vector([x, y, z], [x + dx / (2 * size), y + dy / (2 * size), z + dz / (2 * size)], arrow=arrow, color=color)
        t += small_step

def ode_solution(ode_derivative, x_start=0, y_start=0, z_start=0, end = 0, small_step = 0.5, arrow = False, color="black"):
    counter = 0
    x, y, z = x_start, y_start, z_start
    while (counter < end):
        dx, dy, dz = ode_derivative(x, y, z, small_step)
        size = (dx ** 2 + dy ** 2 + dz ** 2) ** 0.5
        if (size != 0):
            Vector([x, y, z], [x + dx / (2 * size), y + dy / (2 * size), z + dz / (2 * size)], arrow=arrow, color=color)
        x, y, z = x + dx / (2 * size), y + dy / (2 * size), z + dz / (2 * size)
        counter += 1

def vector_field(vector_field, small_step = 0.5,
                 x_start=0, x_end=0, x_jumps = 1,
                 y_start=0, y_end=0, y_jumps = 1,
                 z_start=0, z_end=0, z_jumps = 1,
                 vector_length = 1, arrow = True, color="black", line_width=1):
    x = x_start
    while (x >= x_start and x <= x_end):
        y = y_start
        while (y >= y_start and y <= y_end):
            z = z_start
            while (z >= z_start and z <= z_end):
                dx, dy, dz = vector_field(x, y, z, small_step)
                size = (dx ** 2 + dy ** 2 + dz ** 2) ** 0.5
                size *= vector_length
                if (size != 0):
                    Vector([x, y, z], [x + dx / (2 * size), y + dy / (2 * size), z + dz / (2 * size)], arrow=arrow,
                           color=color, line_width=line_width)
                z += z_jumps
            y += y_jumps
        x += x_jumps