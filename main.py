from functions import *

delta_t = 0.1
steps = 200
variations = np.linspace(-1.0, 1.0, 10)
all_simulations = []

for variation in variations:
    p_1, p_2, p_3 = run_simulation_with_variation(variation, steps, delta_t)
    all_simulations.append((p_1, p_2, p_3, variation))

# Ask the user if they want to visualize the trajectories
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

    for idx in range(min(num_variations, len(all_simulations))):
        p_1, p_2, p_3, variation = all_simulations[idx]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        def update_plot(frame):
            ax.clear()
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_xlim(-8, 8)
            ax.set_ylim(-8, 8)
            ax.set_zlim(-8, 8)

            style_3d_plot(ax)

            ax.plot(p_1[:frame, 0], p_1[:frame, 1], p_1[:frame, 2], color='darkorange')
            ax.plot(p_2[:frame, 0], p_2[:frame, 1], p_2[:frame, 2], color='green')
            ax.plot(p_3[:frame, 0], p_3[:frame, 1], p_3[:frame, 2], color='blue')

            ax.scatter(p_1[frame, 0], p_1[frame, 1], p_1[frame, 2], color='darkorange', label='Body A')
            ax.scatter(p_2[frame, 0], p_2[frame, 1], p_2[frame, 2], color='green', label='Body B')
            ax.scatter(p_3[frame, 0], p_3[frame, 1], p_3[frame, 2], color='blue', label='Body C')

            ax.legend()

        frames_per_sec = 60
        frame_interval = 1000 / frames_per_sec
        ani = FuncAnimation(fig, update_plot, frames=steps, interval=frame_interval)

        writer = FFMpegWriter(fps=frames_per_sec, metadata=dict(artist='Me'), bitrate=1800)
        ani.save(f'three_body_simulation_variation_{idx}.mp4', writer=writer)

        plt.show()

# Data processing after animation
data_frames = {}

for idx, (p_1, p_2, p_3, variation) in enumerate(all_simulations):
    data = []
    for t in range(steps):
        data.append(['Body A', t, p_1[t, 0], p_1[t, 1], p_1[t, 2], variation])
        data.append(['Body B', t, p_2[t, 0], p_2[t, 1], p_2[t, 2], variation])
        data.append(['Body C', t, p_3[t, 0], p_3[t, 1], p_3[t, 2], variation])
    df = pd.DataFrame(data, columns=['Body', 'Time', 'X', 'Y', 'Z', 'Variation'])
    data_frames[f'variation_{idx}'] = df

# Separate the position data for each body into different dictionaries
body_A_data_frames = {}
body_B_data_frames = {}
body_C_data_frames = {}

for key, df in data_frames.items():
    body_A_data_frames[key] = df[df['Body'] == 'Body A']
    body_B_data_frames[key] = df[df['Body'] == 'Body B']
    body_C_data_frames[key] = df[df['Body'] == 'Body C']

# Print the filtered DataFrame for Body A, Body B, and Body C for the first variation
print("Filtered DataFrame for Body A (Variation 0):")
print(body_A_data_frames['variation_0'])
print("\nFiltered DataFrame for Body B (Variation 0):")
print(body_B_data_frames['variation_0'])
print("\nFiltered DataFrame for Body C (Variation 0):")
print(body_C_data_frames['variation_0'])

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

# Concatenate all data frames for each body to calculate the mean path
body_A_data = pd.concat(body_A_data_frames.values())
body_B_data = pd.concat(body_B_data_frames.values())
body_C_data = pd.concat(body_C_data_frames.values())

# Group each data set by time and calculate the mean
body_A_grp = body_A_data.groupby('Time')
body_B_grp = body_B_data.groupby('Time')
body_C_grp = body_C_data.groupby('Time')

mean_path_A = body_A_grp[['X', 'Y', 'Z']].mean()
mean_path_B = body_B_grp[['X', 'Y', 'Z']].mean()
mean_path_C = body_C_grp[['X', 'Y', 'Z']].mean()

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

# Plot the mean path for Body B
fig_B = plt.figure()
ax_B = fig_B.add_subplot(111, projection='3d')
ax_B.plot(mean_path_B['X'], mean_path_B['Y'], mean_path_B['Z'], color='green')
ax_B.set_xlabel('X')
ax_B.set_ylabel('Y')
ax_B.set_zlabel('Z')
ax_B.set_title('Mean Path for Body B')
style_3d_plot(ax_B)  # Apply the styling
plt.show()

# Plot the mean path for Body C
fig_C = plt.figure()
ax_C = fig_C.add_subplot(111, projection='3d')
ax_C.plot(mean_path_C['X'], mean_path_C['Y'], mean_path_C['Z'], color='blue')
ax_C.set_xlabel('X')
ax_C.set_ylabel('Y')
ax_C.set_zlabel('Z')
ax_C.set_title('Mean Path for Body C')
style_3d_plot(ax_C)  # Apply the styling
plt.show()

# Function to calculate deviation from the mean path
def calculate_deviation(df, mean_path):
    df = df.copy()
    df = df.merge(mean_path, on='Time', suffixes=('', '_mean'))
    df['deviation'] = np.sqrt((df['X'] - df['X_mean'])**2 + (df['Y'] - df['Y_mean'])**2 + (df['Z'] - df['Z_mean'])**2)
    return df

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

# Calculate deviation for each variation for Body B
deviation_data_frames_B = {}
for key, df in body_B_data_frames.items():
    deviation_df_B = calculate_deviation(df, mean_path_B)
    deviation_data_frames_B[key] = deviation_df_B

# Plot the deviation for Body B
plt.figure(figsize=(10, 6))
for key, df in deviation_data_frames_B.items():
    plt.plot(df['Time'], df['deviation'], label=key)

plt.xlabel('Time')
plt.ylabel('Deviation from Mean Path')
plt.title('Deviation from Mean Path Over Time for Body B')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()

# Calculate deviation for each variation for Body C
deviation_data_frames_C = {}
for key, df in body_C_data_frames.items():
    deviation_df_C = calculate_deviation(df, mean_path_C)
    deviation_data_frames_C[key] = deviation_df_C

# Plot the deviation for Body C
plt.figure(figsize=(10, 6))
for key, df in deviation_data_frames_C.items():
    plt.plot(df['Time'], df['deviation'], label=key)

plt.xlabel('Time')
plt.ylabel('Deviation from Mean Path')
plt.title('Deviation from Mean Path Over Time for Body C')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()

# Calculate variance over time for Body A
variance_A = body_A_data.groupby('Time')[['X', 'Y', 'Z']].var().mean(axis=1)

plt.figure(figsize=(10, 6))
plt.plot(variance_A.index, variance_A, label='Body A', color='darkorange')
plt.xlabel('Time')
plt.ylabel('Variance of Position')
plt.title('Variance of Position Over Time for Body A')
plt.grid(True)
plt.legend()
plt.show()

# Calculate variance over time for Body B
variance_B = body_B_data.groupby('Time')[['X', 'Y', 'Z']].var().mean(axis=1)

plt.figure(figsize=(10, 6))
plt.plot(variance_B.index, variance_B, label='Body B', color='green')
plt.xlabel('Time')
plt.ylabel('Variance of Position')
plt.title('Variance of Position Over Time for Body B')
plt.grid(True)
plt.legend()
plt.show()

# Calculate variance over time for Body C
variance_C = body_C_data.groupby('Time')[['X', 'Y', 'Z']].var().mean(axis=1)

plt.figure(figsize=(10, 6))
plt.plot(variance_C.index, variance_C, label='Body C', color='blue')
plt.xlabel('Time')
plt.ylabel('Variance of Position')
plt.title('Variance of Position Over Time for Body C')
plt.grid(True)
plt.legend()
plt.show()

# Mean and standard deviation of deviations for Body A
mean_deviation_A = pd.DataFrame({key: df['deviation'].mean() for key, df in deviation_data_frames_A.items()}, index=['Mean']).T
std_deviation_A = pd.DataFrame({key: df['deviation'].std() for key, df in deviation_data_frames_A.items()}, index=['Std']).T

print("Mean Deviation for Body A:")
print(mean_deviation_A)
print("\nStandard Deviation of Deviation for Body A:")
print(std_deviation_A)

# Mean and standard deviation of deviations for Body B
mean_deviation_B = pd.DataFrame({key: df['deviation'].mean() for key, df in deviation_data_frames_B.items()}, index=['Mean']).T
std_deviation_B = pd.DataFrame({key: df['deviation'].std() for key, df in deviation_data_frames_B.items()}, index=['Std']).T

print("Mean Deviation for Body B:")
print(mean_deviation_B)
print("\nStandard Deviation of Deviation for Body B:")
print(std_deviation_B)

# Mean and standard deviation of deviations for Body C
mean_deviation_C = pd.DataFrame({key: df['deviation'].mean() for key, df in deviation_data_frames_C.items()}, index=['Mean']).T
std_deviation_C = pd.DataFrame({key: df['deviation'].std() for key, df in deviation_data_frames_C.items()}, index=['Std']).T

print("Mean Deviation for Body C:")
print(mean_deviation_C)
print("\nStandard Deviation of Deviation for Body C:")
print(std_deviation_C)

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

# Cumulative sum of deviations for Body B
cumsum_deviation_B = pd.DataFrame({key: df['deviation'].cumsum() for key, df in deviation_data_frames_B.items()})

plt.figure(figsize=(10, 6))
for key in cumsum_deviation_B.columns:
    plt.plot(cumsum_deviation_B.index, cumsum_deviation_B[key], label=key)

plt.xlabel('Time')
plt.ylabel('Cumulative Sum of Deviation')
plt.title('Cumulative Sum of Deviation Over Time for Body B')
plt.grid(True)
plt.legend()
plt.show()

# Cumulative sum of deviations for Body C
cumsum_deviation_C = pd.DataFrame({key: df['deviation'].cumsum() for key, df in deviation_data_frames_C.items()})

plt.figure(figsize=(10, 6))
for key in cumsum_deviation_C.columns:
    plt.plot(cumsum_deviation_C.index, cumsum_deviation_C[key], label=key)

plt.xlabel('Time')
plt.ylabel('Cumulative Sum of Deviation')
plt.title('Cumulative Sum of Deviation Over Time for Body C')
plt.grid(True)
plt.legend()
plt.show()
