import pandas as pd
import matplotlib.pyplot as plt

def plot_data(gyro_csv, accel_csv, rgb_csv, depth_csv, sensor_type):
    # Load the CSV data into DataFrames
    gyro_data = pd.read_csv(gyro_csv)
    accel_data = pd.read_csv(accel_csv)
    rgb_data = pd.read_csv(rgb_csv)
    depth_data = pd.read_csv(depth_csv)

    # Set up the plot with six subplots: timestamps, timestamp differences, global timestamps for all sensors
    fig, ax = plt.subplots(5, 1, figsize=(12, 24), sharex=True)

    # Plot timestamps for gyro and accelerometer
    ax[0].plot(gyro_data['Index'], gyro_data['Timestamp'], label='Gyro Timestamp', color='blue')
    ax[0].plot(accel_data['Index'], accel_data['Timestamp'], label='Accelerometer Timestamp', color='orange')
    ax[0].set_title('IMU Timestamps')
    ax[0].set_ylabel('Timestamp (us)')
    ax[0].legend()

    # Plot timestamps for RGB and depth sensors
    ax[1].plot(rgb_data['Index'], rgb_data['Timestamp'], label='RGB Timestamp', color='red')
    ax[1].plot(depth_data['Index'], depth_data['Timestamp'], label='Depth Timestamp', color='green')
    ax[1].set_title('Camera Timestamps')
    ax[1].set_ylabel('Timestamp (us)')
    ax[1].legend()

    # Plot timestamp differences for all sensors if the column exists
    if 'Timestamp Difference' in gyro_data.columns:
        ax[2].plot(gyro_data['Index'], gyro_data['Timestamp Difference'], label='Gyro Timestamp Difference', color='purple')
        ax[2].plot(accel_data['Index'], accel_data['Timestamp Difference'], label='Accelerometer Timestamp Difference', color='magenta')
        ax[2].plot(rgb_data['Index'], rgb_data['Timestamp Difference'], label='RGB Timestamp Difference', color='black')
        ax[2].plot(depth_data['Index'], depth_data['Timestamp Difference'], label='Depth Timestamp Difference', color='grey')
        ax[2].set_title('Timestamp Differences')
        ax[2].set_ylabel('Timestamp Difference (us)')
        ax[2].legend()

    # Plot global timestamps for all sensors if the column exists
    if 'Global Timestamp' in gyro_data.columns:
        ax[3].plot(gyro_data['Index'], gyro_data['Global Timestamp'], label='Gyro Global Timestamp', color='cyan')
        ax[3].plot(accel_data['Index'], accel_data['Global Timestamp'], label='Accelerometer Global Timestamp', color='yellow')
        ax[3].plot(rgb_data['Index'], rgb_data['Global Timestamp'], label='RGB Global Timestamp', color='brown')
        ax[3].plot(depth_data['Index'], depth_data['Global Timestamp'], label='Depth Global Timestamp', color='orange')
        ax[3].set_title('Global Timestamps')
        ax[3].set_ylabel('Global Timestamp (us)')
        ax[3].legend()

    # Plot global timestamp differences for all sensors if the column exists
    if 'Global Timestamp Difference' in gyro_data.columns:
        ax[4].plot(gyro_data['Index'], gyro_data['Global Timestamp Difference'], label='Gyro Global Timestamp Difference', color='orange')
        ax[4].plot(accel_data['Index'], accel_data['Global Timestamp Difference'], label='Accelerometer Global Timestamp Difference', color='brown')
        ax[4].plot(rgb_data['Index'], rgb_data['Global Timestamp Difference'], label='RGB Global Timestamp Difference', color='purple')
        ax[4].plot(depth_data['Index'], depth_data['Global Timestamp Difference'], label='Depth Global Timestamp Difference', color='magenta')
        ax[4].set_title('Global Timestamp Differences')
        ax[4].set_ylabel('Global Timestamp Difference (us)')
        ax[4].legend()

    # Adjust layout and show plot
    plt.tight_layout()
    plt.show()

def main():
    # Path to the gyro, accel, RGB, and depth CSV files
    gyro_csv = 'gyro_data.csv'
    accel_csv = 'accel_data.csv'
    rgb_csv = 'color_data.csv'
    depth_csv = 'depth_data.csv'

    # Plot all sensor data
    plot_data(gyro_csv, accel_csv, rgb_csv, depth_csv, 'Sensor Data')

if __name__ == "__main__":
    main()
