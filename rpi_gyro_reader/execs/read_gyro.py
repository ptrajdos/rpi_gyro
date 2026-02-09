import time
from BMI160_i2c import Driver


def main():
    # Initialize sensor (default I2C address 0x68)
    sensor = Driver(0x69)
    print("BMI160 initialized, starting polling loop...")

    # Optional: define your polling interval (in seconds)
    interval = 0.1 

    try:
        while True:
            # Read accelerometer and gyro (6 axes)
            motion = sensor.getMotion6()
            ax, ay, az, gx, gy, gz = motion
    
            # Print readings
            print(f"A: {ax:6d} {ay:6d} {az:6d} | G: {gx:6d} {gy:6d} {gz:6d}")

            # Wait until next sample
            time.sleep(interval)

    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == '__main__':
    main()
