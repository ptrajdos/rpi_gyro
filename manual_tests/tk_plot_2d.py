#!/usr/bin/env python
import tkinter as tk
from collections import deque
import random

import matplotlib
import numpy as np

from rpi_gyro_reader.gyro.accel_circle_imu import AccelCircleIMU
from rpi_gyro_reader.gyro.imu_receiver import IMUReceiver
from rpi_gyro_reader.transformers.av_transformer import AVTransformer
from rpi_gyro_reader.transformers.cursor_movers.acc_velocity_mover import AccVelocityMover
from rpi_gyro_reader.transformers.madgwick_transformer import MadgwickTransformer
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

CHANNELS = 2
MAX_POINTS = 200
UPDATE_MS = 10
W,H = 300,300

imu = IMUReceiver(address="localhost") #AccelCircleIMU(radius=0.1, freq=0.5) # IMUReceiver(address="localhost")
av_trans = AVTransformer(alpha=0.9)
madg_trans = MadgwickTransformer()
vel_mover = AccVelocityMover(dt=1.0, alpha=0.7, threshold=0.4)
delta_pix = 0.5

def generate_sample():
    v = imu.read_motion()
    # v = av_trans.transform_sample(np.asanyarray(v))
    v = madg_trans.transform_sample(v)
    delta = vel_mover.transform_sample(np.asanyarray(v))
    delta*=delta_pix
    print(f"Generated sample: {delta}")
    return delta[0:2]

y_limits = (-5,5)

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
        self.axes = self.fig.subplots()
        self.axes.set_xlim(0, W)
        self.axes.set_ylim(0, H)

        # Lines
        self.lines = []
        

        self.line, = self.axes.plot([], [])
        

        # Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.x_pos, self.y_pos = W/2, H/2

        self.update_plot()

    def update_buffers(self, sample):
        ax, ay = sample[0], sample[1]
        self.x_pos += ax
        self.y_pos += ay

        self.x_pos = max(0, min(W, self.x_pos))
        self.y_pos = max(0, min(H, self.y_pos))

        self.buffers[0].append(self.x_pos)
        self.buffers[1].append(self.y_pos)

    def update_plot(self):
        sample = generate_sample()
        self.update_buffers(sample)

        x = range(MAX_POINTS)

        self.line.set_data(self.buffers[0], self.buffers[1])

        self.canvas.draw_idle()
        self.root.after(UPDATE_MS, self.update_plot)


if __name__ == "__main__":
    root = tk.Tk()
    app = RealtimePlotApp(root)
    root.mainloop()
