from operations import App, Vector, cos, sin, tan, pi, e, curve, ode_solution, vector_field

def myCurve(t):
    try:
        return cos(t), sin(t), t/5
    except:
        return 0,0,0

def myOde(x, y, z, small_step = 0.2):
    return small_step, (1-x**2)*(1-y**2), 0

def myField(x, y, z, small_step = 0.2):
    return x**2 - y**2, x*y, 0

app = App(
    width=1000, height=700,
    x_axis_scale=25, y_axis_scale=25,
    drag_scale=1, scroll_scale=0.1,
    lower_bound = -10, upper_bound = 10,
    generate_axis=True, generate_markings=True, z_marking=False, markings_space=0.5
)


curve(myCurve, t_start=0, t_end=10, arrow=False, color="pink")
vector_field(myField, x_start=-4, x_end=4, y_start=-4 ,y_end=4, z_start=-0, z_end=0,
             x_jumps = 1, y_jumps=1, color="black", line_width=3, small_step=10)
# Vector([-10,-10,0],[10,10,0])
#ode_solution(myOde,0, 0, 0, small_step=5,end=100, arrow=True, color="yellow")

app.generateVectors()
app.packObjects()
app.modifyVectors()
app.mainloop()