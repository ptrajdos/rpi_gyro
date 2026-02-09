import zmq
import threading as th
import struct
import time

from rpi_gyro_reader.gyro.iimu import IMU


class IMUPublisher:

    def __init__(self, imu: IMU, address="*", port="7734", delay=0.01):
        self.imu = imu
        self.address = address
        self.port = port
        self.delay = delay

        self._init_context()
        self._init_thread()

    def _init_context(self):
        self.context = zmq.Context()
        self.publish_socket = self.context.socket(zmq.PUB)
        self.publish_socket.bind(f"tcp://{self.address}:{self.port}")

    def _init_thread(self):
        self._is_thread_running = True
        self._thread = th.Thread(target=self._runner, daemon=True)
        self._thread.start()

    def _runner(self):
        while self._is_thread_running:
            motion = self.imu.read_motion()
            ax, ay, az, gx, gy, gz, mx, my, mz = motion
            payload = struct.pack("<fffffffff", ax, ay, az, gx, gy, gz, mx, my, mz)
            self.publish_socket.send(payload)
            time.sleep(self.delay)

    def stop(self):
        self._is_thread_running = False
        self._thread.join()
        self.publish_socket.close()
        self.context.term()
