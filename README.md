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
The "delta_t" variable defines how frequently the motion of the bodies' positions/velocities are updated in time, while "steps" defines the total number of these steps taken over the course of the simulation. The purpose of "variations" is to generate an array of 10, even spaced values which can be added to the initial positions of the bodies, producing 10 unique trajectory simulations. Note that the variations values range from -0.1 to 0.1, ensuring only small changes are made to the initial system of bodies, while the first two variables can be defined according to user preference, though increasing steps will result in longer computation time.

The code will produce 10 simulations of a 3-body system, storing the positions of the bodies at each time step in 3 distinct NumPy arrays ('p_1', 'p_2', 'p_3') and appending these arrays into a list ('all_simulations'):

```python
for variation in variations:
    p_1, p_2, p_3 = run_simulation_with_variation(variation, steps, delta_t)
    all_simulations.append((p_1, p_2, p_3, variation))
```
At this point, the user will be prompted to decide whether they want visualise any of the simulation trajectories (yes/no), followed by how many of the simulations they wish to visualise if they entered 'yes'. This option allows the user to control the computation time allocated to animating trajectories, as this step not necessary to the statistical analysis of the trajectories. Any invalid inputs will result in continual prompts until a valid entry is made by the user.

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

Upon completion of the animation step, the data within the 'all_simulations' list is reorganised into Pandas structures, with each simulation's data being stored in a data frame, then all 10 data frames themselves are stored in a dictionary ('data_frames'). Pandas provides more intuitive methods for grouping and aggregating the data, which will prove useful for comparing the 10 simulations.

```python
data_frames = {}

for idx, (p_1, p_2, p_3, variation) in enumerate(all_simulations):
    data = []
    for t in range(steps):
        data.append(['Body A', t, p_1[t, 0], p_1[t, 1], p_1[t, 2], variation])
        data.append(['Body B', t, p_2[t, 0], p_2[t, 1], p_2[t, 2], variation])
        data.append(['Body C', t, p_3[t, 0], p_3[t, 1], p_3[t, 2], variation])
    df = pd.DataFrame(data, columns=['Body', 'Time', 'X', 'Y', 'Z', 'Variation'])
    data_frames[f'variation_{idx}'] = df
```
The program filters the trajectory data into 3 separate dictionaries for each of the 3 bodies, allowing us to visualise the differing trajectories of an indiviual body for all 10 variations: 
``` python
# Separate the position data for each body into different dictionariesbody_A_data_frames = {}
body_B_data_frames = {}
body_C_data_frames = {}

for key, df in data_frames.items():
    body_A_data_frames[key] = df[df['Body'] == 'Body A']
    body_B_data_frames[key] = df[df['Body'] == 'Body B']
    body_C_data_frames[key] = df[df['Body'] == 'Body C']

# Create 3D plots for each variation for Body A, Body B, and Body C
for body_data_frames, body_name in zip([body_A_data_frames, body_B_data_frames, body_C_data_frames], ['Body A', 'Body B', 'Body C']):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.set_zlim(-8, 8)

    style_3d_plot(ax)  # Apply styling to the plot

    colors = plt.cm.viridis(np.linspace(0, 1, len(body_data_frames)))

    for idx, (key, df) in enumerate(body_data_frames.items()):
        ax.plot(df['X'], df['Y'], df['Z'], label=f'Variation {key}', color=colors[idx])

    ax.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), title=f'{body_name} Variations')
    ax.set_title(f'Trajectories for {body_name}')

    plt.show()
```

These are some examples of plots produced, demonstrating the variety of trajectories of each body, even with relatively small alterations to the system's initial conditions:

![Figure 2024-08-06 160628 (1)](https://github.com/user-attachments/assets/7f926cd2-9eee-457e-a041-e863939eb779)
![Figure 2024-08-06 160628 (2)](https://github.com/user-attachments/assets/34480bc5-8558-42f5-b594-ea1ec200e1d8)
![Figure 2024-08-06 160628 (3)](https://github.com/user-attachments/assets/e90d2143-73d4-4323-bcc9-38d9c08c2516)

The dictionaries for each body are then concatenated into data frames and grouped by time, allowing for the calculation of the average position of each body at a given time across all 10 variations. 

```python
# Concatenate all data frames for each body to calculate the mean path
body_A_data = pd.concat(body_A_data_frames.values())
body_B_data = pd.concat(body_B_data_frames.values())
body_C_data = pd.concat(body_C_data_frames.values())

# Group each data set by time and calculate the mean
body_A_grp = body_A_data.groupby('Time')
body_B_grp = body_B_data.groupby('Time')
body_C_grp = body_C_data.groupby('Time')
```
Plotting the average position over time visualises the mean path taken by each body, take body A for example:

```python
mean_path_A = body_A_grp[['X', 'Y', 'Z']].mean()

# Plot the mean path for Body A
fig_A = plt.figure()
ax_A = fig_A.add_subplot(111, projection='3d')
ax_A.plot(mean_path_A['X'], mean_path_A['Y'], mean_path_A['Z'], color='darkorange')
ax_A.set_xlabel('X')
ax_A.set_ylabel('Y')
ax_A.set_zlabel('Z')
ax_A.set_title('Mean Path for Body A')
style_3d_plot(ax_A)  # Apply the styling
plt.show()
```

![Figure 2024-08-06 160628 (4)](https://github.com/user-attachments/assets/d8a141bc-2df6-46f9-aebf-66a5971be5b3)

The deviation from the mean path over time for all 10 trajectories of a given body are calculated and plotted. Demonstrating how the trajectories diverge over the course of each simulation.

```python
# Calculate deviation for each variation for Body A
deviation_data_frames_A = {}
for key, df in body_A_data_frames.items():
    deviation_df = calculate_deviation(df, mean_path_A)
    deviation_data_frames_A[key] = deviation_df

# Plot the deviation over time for each variation for Body A
plt.figure(figsize=(10, 6))
for key, df in deviation_data_frames_A.items():
    plt.plot(df['Time'], df['deviation'], label=key)

plt.xlabel('Time')
plt.ylabel('Deviation from Mean Path')
plt.title('Deviation from Mean Path Over Time for Body A')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()
```
![Figure 2024-08-06 160628 (7)](https://github.com/user-attachments/assets/f663281a-0d13-4e69-9847-421bc93e49f6)

The code then determines the variance of the position data for each body at a given time step. The resulting graphs demonstrate the increasing unpredictability in the behaviour of the 3-body system over time, as all 3 show a clear trend of increasing variance with respect to time.

# Calculate variance over time for Body A
variance_A = body_A_data.groupby('Time')[['X', 'Y', 'Z']].var().mean(axis=1)

```python
plt.figure(figsize=(10, 6))
plt.plot(variance_A.index, variance_A, label='Body A', color='darkorange')
plt.xlabel('Time')
plt.ylabel('Variance of Position')
plt.title('Variance of Position Over Time for Body A')
plt.grid(True)
plt.legend()
plt.show()
```

![Figure 2024-08-06 160628 (10)](https://github.com/user-attachments/assets/94405fe2-a85b-4417-b6c1-ac222da37ef5)

The program will then determine the mean and standard deviations for the trajectories each body, storing this within a new data frame and outputing these values for the user.

```python
# Mean and standard deviation of deviations for Body A
mean_deviation_A = pd.DataFrame({key: df['deviation'].mean() for key, df in deviation_data_frames_A.items()}, index=['Mean']).T
std_deviation_A = pd.DataFrame({key: df['deviation'].std() for key, df in deviation_data_frames_A.items()}, index=['Std']).T

print("Mean Deviation for Body A:")
print(mean_deviation_A)
print("\nStandard Deviation of Deviation for Body A:")
print(std_deviation_A)
```

The final example of data analysis performed by the code is the calcultion of the cumulative summation of the deviation from the mean path for each body across all simulations. Where the resulting plot shows a predictable trend of increasing cumulative deviation with respect to time.

```python
# Cumulative sum of deviations for Body A
cumsum_deviation_A = pd.DataFrame({key: df['deviation'].cumsum() for key, df in deviation_data_frames_A.items()})

plt.figure(figsize=(10, 6))
for key in cumsum_deviation_A.columns:
    plt.plot(cumsum_deviation_A.index, cumsum_deviation_A[key], label=key)

plt.xlabel('Time')
plt.ylabel('Cumulative Sum of Deviation')
plt.title('Cumulative Sum of Deviation Over Time for Body A')
plt.grid(True)
plt.legend()
plt.show()
```
![Figure 2024-08-06 160628 (13)](https://github.com/user-attachments/assets/c162b0fc-6332-4a58-aefb-cf64bddf4297)




## Functions


## Examples

## Contributing 

## License
