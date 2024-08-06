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







