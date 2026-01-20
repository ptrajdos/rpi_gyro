from BMI160_i2c import Driver
from rpi_gyro_reader.gyro.iimu import IMU

BMI160_ACC_LSB_PER_G = {
    0x03: 16384,  # ±2g
    0x05: 8192,   # ±4g
    0x08: 4096,   # ±8g
    0x0C: 2048,   # ±16g
}

BMI160_GYR_LSB_PER_DPS = {
    0x00: 16.4,   # ±2000 dps
    0x01: 32.8,   # ±1000 dps
    0x02: 65.6,   # ±500 dps
    0x03: 131.2,  # ±250 dps
    0x04: 262.4,  # ±125 dps
}


class IMUBMI160(IMU):
    def __init__(self, address=0x69):
        self.sensor = Driver(address)

    def read_accel(self) -> tuple[float, float, float]:
        _, _, _, rax, ray, raz = self.sensor.getMotion6()
        mode = self.sensor.getFullScaleAccelRange()
        ax, ay, az = rax / BMI160_ACC_LSB_PER_G[mode], ray / BMI160_ACC_LSB_PER_G[mode], raz / BMI160_ACC_LSB_PER_G[mode]
        ax*=9.80665
        ay*=9.80665
        az*=9.80665
        return float(ax), float(ay), float(az)

    def read_gyro(self) -> tuple[float, float, float]:
        rgx, rgy, rgz, _, _, _ = self.sensor.getMotion6()
        mode = self.sensor.getFullScaleGyroRange()
        gx, gy, gz = rgx / BMI160_GYR_LSB_PER_DPS[mode], rgy / BMI160_GYR_LSB_PER_DPS[mode], rgz / BMI160_GYR_LSB_PER_DPS[mode]
        return float(gx), float(gy), float(gz)

    def read_motion(self) -> tuple[float, float, float, float, float, float]:
        rgx, rgy, rgz, rax, ray, raz = self.sensor.getMotion6()
        mode_g = self.sensor.getFullScaleGyroRange()
        mode_a = self.sensor.getFullScaleAccelRange()
        gx, gy, gz = rgx / BMI160_GYR_LSB_PER_DPS[mode_g], rgy / BMI160_GYR_LSB_PER_DPS[mode_g], rgz / BMI160_GYR_LSB_PER_DPS[mode_g]
        ax, ay, az = rax / BMI160_ACC_LSB_PER_G[mode_a], ray / BMI160_ACC_LSB_PER_G[mode_a], raz / BMI160_ACC_LSB_PER_G[mode_a]

        ax*=9.80665
        ay*=9.80665
        az*=9.80665

        return float(ax), float(ay), float(az), float(gx), float(gy), float(gz)