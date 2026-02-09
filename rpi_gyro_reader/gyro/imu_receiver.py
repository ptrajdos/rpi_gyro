import struct
import numpy as np
import zmq
from rpi_gyro_reader.gyro.iimu import IMU
import threading as th
import logging


class IMUReceiver(IMU):

    def __init__(self, address="*", port="7734", timeout=1000):
        self.address = address
        self.port = port
        self.timeout = timeout

        self.ax, self.ay, self.az, self.gx, self.gy, self.gz = (
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        )

        self._init_context()
        self._init_thread()


    def _init_context(self):
        self.context = zmq.Context()
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.setsockopt(zmq.RCVTIMEO, self.timeout)
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, b"")

        self.sub_socket.connect(f"tcp://{self.address}:{self.port}")

    def _runner(self):
        while self._is_thread_running:
            try:
                payload = self.sub_socket.recv()
                self.ax, self.ay, self.az, self.gx, self.gy, self.gz = struct.unpack(
                    "<ffffff", payload
                )
            except zmq.Again:
                pass
            except Exception as ex:
                logging.error("Unknown exception: %s", ex, exc_info=True)

    def _init_thread(self):
        self._is_thread_running = True
        self._thread = th.Thread(target=self._runner, daemon=True)
        self._thread.start()

    def read_accel(self):
        return np.array([self.ax, self.ay, self.az])

    def read_gyro(self):
        return np.array([self.gx, self.gy, self.gz])

    def read_motion(self):
        return np.array([self.ax, self.ay, self.az, self.gx, self.gy, self.gz])

    def stop(self):
        self._is_thread_running = False
        self._thread.join()
        self.sub_socket.close()
        self.context.term()
