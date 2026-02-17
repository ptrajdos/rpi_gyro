#!/usr/bin/env python
import tkinter as tk
from collections import deque
import random

import matplotlib
import numpy as np

from rpi_gyro_reader.gyro.accel_circle_imu import AccelCircleIMU
from rpi_gyro_reader.gyro.imu_receiver import IMUReceiver
from rpi_gyro_reader.transformers.av_transformer import AVTransformer
from rpi_gyro_reader.transformers.madgwick_transformer import MadgwickTransformer
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

CHANNELS = 6
MAX_POINTS = 200
UPDATE_MS = 10

imu = IMUReceiver(address="raspberry") #AccelCircleIMU(radius=0.1, freq=0.5) # IMUReceiver(address="localhost")
av_trans = AVTransformer(alpha=0.9)
madg_trans = MadgwickTransformer(return_body_frame=True)

def generate_sample():
    v = imu.read_motion()
    # v = av_trans.transform_sample(np.asanyarray(v))
    # v = madg_trans.transform_sample(v)
    return v

y_limits = (-20,20)

class RealtimePlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Realtime 6-Channel Viewer")

        # Buffers
        self.buffers = [
            deque([0] * MAX_POINTS, maxlen=MAX_POINTS)
            for _ in range(CHANNELS)
        ]

        # Figure
        self.fig = Figure(figsize=(8, 10), dpi=100)
        self.axes = self.fig.subplots(CHANNELS, 1, sharex=True)

        # Lines
        self.lines = []
        for i, ax in enumerate(self.axes):
            ax.set_xlim(0, MAX_POINTS)
            ax.set_ylim(y_limits[0], y_limits[1])
            ax.grid(True)
            ax.set_ylabel(f"CH {i+1}")

            line, = ax.plot([], [])
            self.lines.append(line)

        self.axes[-1].set_xlabel("Samples")

        # Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.update_plot()

    def update_buffers(self, sample):
        for i, value in enumerate(sample[0:CHANNELS]):
            self.buffers[i].append(value)

    def update_plot(self):
        sample = generate_sample()
        self.update_buffers(sample)

        x = range(MAX_POINTS)

        for i, line in enumerate(self.lines):
            line.set_data(x, list(self.buffers[i]))

        self.canvas.draw_idle()
        self.root.after(UPDATE_MS, self.update_plot)


if __name__ == "__main__":
    root = tk.Tk()
    app = RealtimePlotApp(root)
    root.mainloop()
