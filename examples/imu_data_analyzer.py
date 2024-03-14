import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

def plot_time_series(data):
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    sensors = ['accel', 'gyro']
    axes = axes.flatten()
    
    for i, sensor in enumerate(sensors):
        for j, axis in enumerate(['x', 'y', 'z']):
            ax = axes[i * 3 + j]
            sensor_data = data[data['type'] == sensor]
            ax.plot(sensor_data['normalized_time'], sensor_data[axis], label=f'{sensor} {axis}')
            ax.set_title(f'{sensor.upper()} {axis.upper()}')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Measurements')
            ax.legend()
    
    plt.tight_layout()
    plt.show()

def noise_and_bias_analysis(data):
    types = ['accel', 'gyro']
    metrics = ['mean', 'std']
    
    for sensor_type in types:
        for axis in ['x', 'y', 'z']:
            sensor_data = data[data['type'] == sensor_type][axis]
            print(f'{sensor_type} {axis} - Mean: {sensor_data.mean():.3f}, Std: {sensor_data.std():.3f}')

def plot_frequency_domain(data, sampling_rate=100):
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.flatten()
    sensors = ['accel', 'gyro']
    
    for i, sensor in enumerate(sensors):
        for j, axis in enumerate(['x', 'y', 'z']):
            ax = axes[i * 3 + j]
            sensor_data = data[data['type'] == sensor]
            yf = fft(sensor_data[axis])
            xf = fftfreq(len(sensor_data), 1 / sampling_rate)[:len(sensor_data) // 2]
            ax.plot(xf, 2.0 / len(sensor_data) * np.abs(yf[0:len(sensor_data) // 2]))
            ax.set_title(f'FFT {sensor.upper()} {axis.upper()}')
            ax.set_xlabel('Frequency (Hz)')
            ax.set_ylabel('Amplitude')
    
    plt.tight_layout()
    plt.show()

def main():
    # load data
    imu_data = pd.read_csv('imu_data.csv')
    imu_data['normalized_time'] = imu_data['timestamp'] - imu_data['timestamp'].iloc[0]
    
    # time series plot
    plot_time_series(imu_data)
    
    # noise and bias analysis
    noise_and_bias_analysis(imu_data)
    
    # frequency domain plot
    plot_frequency_domain(imu_data, sampling_rate=100)

if __name__ == "__main__":
    main()
