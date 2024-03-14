# ******************************************************************************
#  Copyright (c) 2023 Orbbec 3D Technology, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http:# www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import os
from pathlib import Path

def plot_time_series(data, save_path):
    """Plot the time series of accelerometer and gyroscope data."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    sensors = ["accel", "gyro"]
    axes = axes.flatten()

    for i, sensor in enumerate(sensors):
        for j, axis in enumerate(["x", "y", "z"]):
            ax = axes[i * 3 + j]
            sensor_data = data[data["type"] == sensor]
            timestamps = sensor_data["timestamp"].values - sensor_data["timestamp"].iloc[0]
            measurements = sensor_data[axis].values
            ax.plot(timestamps, measurements, label=f"{sensor} {axis}")
            ax.set_title(f"{sensor.upper()} {axis.upper()}")
            ax.set_xlabel("Time (ms)")
            ax.set_ylabel("Measurements")
            ax.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(save_path, 'time_series_plots.png'))
    plt.show()


def noise_and_bias_analysis(data):
    """Calculate and print the mean and standard deviation for accelerometer and gyroscope data."""
    types = ["accel", "gyro"]

    for sensor_type in types:
        for axis in ["x", "y", "z"]:
            sensor_data = data[data["type"] == sensor_type][axis]
            print(f"{sensor_type} {axis} - Mean: {sensor_data.mean():.3f}, Std: {sensor_data.std():.3f}")


def plot_frequency_domain(data, save_path, sampling_rate=100):
    """Plot the frequency domain representation of accelerometer and gyroscope data."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.flatten()
    sensors = ["accel", "gyro"]

    for i, sensor in enumerate(sensors):
        for j, axis in enumerate(["x", "y", "z"]):
            ax = axes[i * 3 + j]
            sensor_data = data[data["type"] == sensor]
            yf = fft(sensor_data[axis].values)
            xf = fftfreq(len(sensor_data), 1 / sampling_rate)[: len(sensor_data) // 2]
            ax.plot(xf, 2.0 / len(sensor_data) * np.abs(yf[:len(sensor_data) // 2]))
            ax.set_title(f"FFT {sensor.upper()} {axis.upper()}")
            ax.set_xlabel("Frequency (Hz)")
            ax.set_ylabel("Amplitude")

    plt.tight_layout()
    plt.savefig(os.path.join(save_path, 'frequency_domain_plots.png'))
    plt.show()


def main():
    # Define the path to save plots
    save_path = 'plot_output'
    os.makedirs(save_path, exist_ok=True)

    # Load IMU data
    data_path = os.path.join(Path(__file__).parent, "imu_data.csv")
    imu_data = pd.read_csv(data_path)

    # Perform time series analysis
    plot_time_series(imu_data, save_path)

    # Perform noise and bias analysis
    noise_and_bias_analysis(imu_data)

    # Perform frequency domain analysis
    plot_frequency_domain(imu_data, save_path, sampling_rate=100)


if __name__ == "__main__":
    main()
