# 3-Body_Problem_Analysis

## Overview
This program runs multiple simulations of the three-body problem with varying initial conditions. For each variation,the trajectories of the three bodies are stored, allowing  the user to animate each simulation using matplotlib's animation module. Utilising Pandas, data analysis is then performed (calculating the mean path, variance and deviation), along with a statistical summary (mean and standard deviation) to compare the trajectories across all simulations.

## Table of Contents
1. Installation
2. Usage
3. Functions
4. Examples
5. Contributing
6. License

## Installation 
Use the package manager pip to install the matplotlib,numPy and Panas libraries:
```bash
pip install matplotlib pandas numpy
```
## Usage

The program begins by defining some initial variables: 
```python
delta_t = 0.1
steps = 200
variations = np.linspace(-1.0, 1.0, 10)
```
The "delta_t" variable defines how frequently the motion of the bodies' positions/velocities are updated in time, while "steps" defines the total number of these steps taken over the course of the simulation. The purpose of "variations" is to generate an array of 10, even spaced values which can be added to the initial positions of the bodies, to produce 10 unique trajectory simulation. Note that the variations values range from -0.1 to 0.1, ensuring only small changes are made to the initial system of bodies, while the first two variables can be defined according to user preference, though increasing steps will result in longer computation time.

The code will produce 10 variations of a 3-body simulation, storing the positions of the bodies at each time step in 3 NumPy arrays ('p_1', 'p_2', 'p_3') and appending these arrays into a list ('all_simulations'):

```python
for variation in variations:
    p_1, p_2, p_3 = run_simulation_with_variation(variation, steps, delta_t)
    all_simulations.append((p_1, p_2, p_3, variation))
```

At this point, the user will be prompted to decide whether they want visualise any of the simulation trajectories (yes/no), followed by how many of the simulations they wish to visualise if they entered 'yes'. This option allows the user to control the computation time allocated to animating trajectories, as this step not necessary to the statistical analysis of the trajectories. Any invalid inputs will result in continual prompts until a valid entry is made by the user .


```python
while True:
    visualize = input("Do you want to visualize the trajectories for the variations? (yes/no): ").strip().lower()
    if visualize in ['yes', 'no']:
        break
    print("Invalid input. Please enter 'yes' or 'no'.")

if visualize == 'yes':
    while True:
        try:
            num_variations = int(input("How many variations do you want to animate? (1-10): ").strip())
            if 1 <= num_variations <= 10:
                break
            else:
                print("Invalid number. Please enter a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
```
Note that the animation settings can also be adjusted prior to running the code, however, the presets should produce sufficiently smooth visualisation of the bodies' motion.
```python
        frames_per_sec = 60
        frame_interval = 1000 / frames_per_sec
```

The resulting animation(s) will appear as mp4 files in the same directory as the python file. Three example animations produced by the program are provided in the main branch of the repository.

Upon completion of the animation step, 






