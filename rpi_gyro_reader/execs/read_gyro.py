import smbus2
import RPi.GPIO as GPIO
import time

I2C_BUS = 1
BMI160_ADDR = 0x68
INT_PIN = 17

bus = smbus2.SMBus(I2C_BUS)

# ---------- BMI160 registers ----------
CMD = 0x7E
ACC_CONF = 0x40
GYR_CONF = 0x42
INT_EN_1 = 0x51
INT_OUT_CTRL = 0x53
INT_MAP_1 = 0x56
DATA_START = 0x12

def write(reg, val):
    bus.write_byte_data(BMI160_ADDR, reg, val)

def read_block(reg, length):
    return bus.read_i2c_block_data(BMI160_ADDR, reg, length)

def twos(val):
    return val - 65536 if val & 0x8000 else val



def imu_interrupt(channel):
    data = read_block(DATA_START, 12)

    ax = twos(data[1] << 8 | data[0])
    ay = twos(data[3] << 8 | data[2])
    az = twos(data[5] << 8 | data[4])

    gx = twos(data[7] << 8 | data[6])
    gy = twos(data[9] << 8 | data[8])
    gz = twos(data[11] << 8 | data[10])

    print(f"A: {ax:6d} {ay:6d} {az:6d} | G: {gx:6d} {gy:6d} {gz:6d}")

def main():
    # ---------- Init ----------
    write(CMD, 0x11)    # accel normal
    time.sleep(0.05)
    write(CMD, 0x15)    # gyro normal
    time.sleep(0.05)

    write(ACC_CONF, 0x28)   # accel 100 Hz
    write(GYR_CONF, 0x28)   # gyro 100 Hz

    write(INT_EN_1, 0x10)   # data-ready enable
    write(INT_OUT_CTRL, 0x0A)  # push-pull, active-high
    write(INT_MAP_1, 0x01)  # map data-ready to INT1

    # ---------- GPIO ----------
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(INT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.add_event_detect(INT_PIN, GPIO.RISING, callback=imu_interrupt)

    print("Running…")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    main()