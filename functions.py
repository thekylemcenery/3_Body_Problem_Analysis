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
    '''
    Update the position of a body based on its velocity and time step.

    Parameters:
    - body: The object representing the celestial body, which has attributes for position (x, y, z) and velocity (vx, vy, vz).
    - dt: The time step for the simulation.

    Returns:
    - None (The function updates the position of the body in place).
    '''
    body.x += body.vx * dt
    body.y += body.vy * dt
    body.z += body.vz * dt

def update_velocity(body, force, dt):
    '''
    Update the velocity of a body based on the applied force and time step.

    Parameters:
    - body: The object representing the celestial body, which has attributes for mass and velocity (vx, vy, vz).
    - force: A list or array representing the force applied to the body in the x, y, and z directions.
    - dt: The time step for the simulation.

    Returns:
    - None (The function updates the velocity of the body in place).
    '''
    ax = force[0] / body.mass
    ay = force[1] / body.mass
    az = force[2] / body.mass
    body.vx += ax * dt
    body.vy += ay * dt
    body.vz += az * dt

def gravitational_force(body1, body2):
    '''
    Calculate the gravitational force exerted on body1 by body2.

    Parameters:
    - body1: The object representing the first celestial body.
    - body2: The object representing the second celestial body.

    Returns:
    - force: A numpy array representing the force exerted on body1 by body2 in the x, y, and z directions.
    '''
    G = 1.0  # Gravitational constant (set to 1.0 for simplicity)
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
    '''
    Simulate the movement of a list of celestial bodies over a single time step.

    Parameters:
    - bodies: A list of objects representing the celestial bodies in the simulation.
    - dt: The time step for the simulation.

    Returns:
    - None (The function updates the position and velocity of each body in place).
    '''
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
    '''
    Generate position data for multiple steps in the simulation.

    Parameters:
    - bodies: A list of objects representing the celestial bodies in the simulation.
    - dt: The time step for the simulation.
    - steps: The number of steps to simulate.

    Returns:
    - p_1, p_2, p_3: Numpy arrays containing the position data for the first, second, and third bodies at each time step.
    '''
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
    '''
    Run a simulation with a specific variation in the initial conditions.

    Parameters:
    - variation: A scalar value to vary the initial conditions of the bodies.
    - steps: The number of steps to simulate.
    - delta_t: The time step for the simulation.

    Returns:
    - p_1, p_2, p_3: Numpy arrays containing the position data for the first, second, and third bodies at each time step.
    '''
    v = 3 + variation
    L = 1
    body_A = Body(1 + variation * 0.5, 1, 2, 0.1, 'darkorange', 10, 0, 0, 0)
    body_B = Body(L * 2, 1 + variation * 0.5, 3, 0.1, 'green', 3, -v / 2, v * math.sqrt(3) / 2, 0)
    body_C = Body(0, 0, 2 + variation * 0.5, 0.1, 'blue', 3, v, -v * math.sqrt(3) / 2, 0)

    bodies = [body_A, body_B, body_C]

    p_1, p_2, p_3 = frames(bodies, delta_t, steps)

    return p_1, p_2, p_3

def style_3d_plot(ax):
    '''
    Apply custom styling to a 3D plot.

    Parameters:
    - ax: The matplotlib Axes object representing the 3D plot.

    Returns:
    - None (The function applies styling directly to the provided Axes object).
    '''
    ax.set_facecolor('black')  # Set background color to black
    ax.grid(color='grey', linestyle='--')  # Set grid color and style
    ax.xaxis.set_pane_color((0, 0, 0, 0))  # Set x-axis pane color to black (transparent)
    ax.yaxis.set_pane_color((0, 0, 0, 0))  # Set y-axis pane color to black (transparent)
    ax.zaxis.set_pane_color((0, 0, 0, 0))  # Set z-axis pane color to black (transparent)

def calculate_deviation(df, mean_path):
    '''
    Calculate the deviation of each position from the mean path.

    Parameters:
    - df: A pandas DataFrame containing the position data for a body, with columns 'X', 'Y', 'Z', and 'Time'.
    - mean_path: A pandas DataFrame containing the mean positions for the body at each time step.

    Returns:
    - df: A pandas DataFrame with an additional column 'deviation', representing the deviation from the mean path at each time step.
    '''
    df = df.copy()
    df = df.merge(mean_path, on='Time', suffixes=('', '_mean'))
    df['deviation'] = np.sqrt((df['X'] - df['X_mean'])**2 + (df['Y'] - df['Y_mean'])**2 + (df['Z'] - df['Z_mean'])**2)
    return df
