import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('dark_background')
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, FFMpegWriter

class Body:
    def __init__(self, x, y, z, radius, color, mass, vx=0, vy=0, vz=0):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.color = color
        self.mass = mass
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.r = np.array([x, y, z])

def update_position(body, dt):
    body.x += body.vx * dt
    body.y += body.vy * dt
    body.z += body.vz * dt

def update_velocity(body, force, dt):
    ax = force[0] / body.mass
    ay = force[1] / body.mass
    az = force[2] / body.mass
    body.vx += ax * dt
    body.vy += ay * dt
    body.vz += az * dt

def gravitational_force(body1, body2):
    G = 1.0
    dx = body2.x - body1.x
    dy = body2.y - body1.y
    dz = body2.z - body1.z
    distance_squared = dx**2 + dy**2 + dz**2
    distance = math.sqrt(distance_squared)
    force_magnitude = G * body1.mass * body2.mass / distance_squared
    force_x = force_magnitude * dx / distance
    force_y = force_magnitude * dy / distance
    force_z = force_magnitude * dz / distance
    force = np.array([force_x, force_y, force_z])
    return force

def simulate(bodies, dt):
    for body in bodies:
        net_force = [0, 0, 0]
        for other_body in bodies:
            if body != other_body:
                force = gravitational_force(body, other_body)
                net_force[0] += force[0]
                net_force[1] += force[1]
                net_force[2] += force[2]
        update_velocity(body, net_force, dt)
    for body in bodies:
        update_position(body, dt)
        body.r = np.array([body.x, body.y, body.z])

def frames(bodies, dt, steps):
    p_1 = np.zeros((steps, 3))
    p_2 = np.zeros((steps, 3))
    p_3 = np.zeros((steps, 3))
    body1 = bodies[0]
    body2 = bodies[1]
    body3 = bodies[2]
    p_1[0] = body1.r
    p_2[0] = body2.r
    p_3[0] = body3.r
    for i in range(1, steps):
        simulate(bodies, dt)
        p_1[i] = bodies[0].r
        p_2[i] = bodies[1].r
        p_3[i] = bodies[2].r
    return p_1, p_2, p_3

def run_simulation_with_variation(variation, steps, delta_t):
    v = 3 + variation
    L = 1
    body_A = Body(1 + variation * 0.5, 1, 2, 0.1, 'darkorange', 10, 0, 0, 0)
    body_B = Body(L * 2, 1 + variation * 0.5, 3, 0.1, 'green', 3, -v / 2, v * math.sqrt(3) / 2, 0)
    body_C = Body(0, 0, 2 + variation * 0.5, 0.1, 'blue', 3, v, -v * math.sqrt(3) / 2, 0)

    bodies = [body_A, body_B, body_C]

    p_1, p_2, p_3 = frames(bodies, delta_t, steps)

    return p_1, p_2, p_3

def style_3d_plot(ax):
    ax.set_facecolor('black')  # Set background color to black
    ax.grid(color='grey', linestyle='--')  # Set grid color and style
    ax.xaxis.set_pane_color((0, 0, 0, 0))  # Set x-axis pane color to black (transparent)
    ax.yaxis.set_pane_color((0, 0, 0, 0))  # Set y-axis pane color to black (transparent)
    ax.zaxis.set_pane_color((0, 0, 0, 0))  # Set z-axis pane color to black (transparent)

def calculate_deviation(df, mean_path):
    df = df.copy()
    df = df.merge(mean_path, on='Time', suffixes=('', '_mean'))
    df['deviation'] = np.sqrt((df['X'] - df['X_mean'])**2 + (df['Y'] - df['Y_mean'])**2 + (df['Z'] - df['Z_mean'])**2)
    return df

