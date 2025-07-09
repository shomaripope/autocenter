
import time
import csv
import os
from nissan_interface import NissanSteering, NissanVehicle
import matplotlib.pyplot as plt
import matplotlib.animation as animation

STEERING_THRESHOLD = 2.0  # Degrees
RESET_SPEED = 0.5         # Degrees per cycle
MAX_DRIVER_TORQUE = 2.0   # Degrees (simulated override limit)
LOG_FILE_CSV = "steering_log.csv"
LOG_FILE_TXT = "steering_log.txt"

class SteeringResetController:
    def __init__(self, mock=False):
        self.vehicle = NissanVehicle(mock=mock)
        self.steering = NissanSteering(mock=mock)
        self.mock = mock
        self.csv_writer = None
        self.txt_file = None
        self.angle_data = []
        self.time_data = []

        if not os.path.exists(LOG_FILE_CSV):
            with open(LOG_FILE_CSV, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Steering Angle", "Vehicle Speed", "Gear", "Driver Torque", "Status"])

        self.txt_file = open(LOG_FILE_TXT, "a")

    def log(self, status, angle, speed, gear, torque):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE_CSV, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, angle, speed, gear, torque, status])
        self.txt_file.write(f"{timestamp} | Angle: {angle:.2f}° | Speed: {speed:.2f} km/h | Gear: {gear} | Torque: {torque:.2f} | {status}\n")
        self.txt_file.flush()

    def is_parked(self):
        return self.vehicle.speed() == 0 and self.vehicle.gear() in ['P', 'R']

    def should_reset(self, angle):
        return abs(angle) > STEERING_THRESHOLD

    def reset(self):
        angle = self.steering.get_angle()
        speed = self.vehicle.speed()
        gear = self.vehicle.gear()
        torque = self.steering.get_driver_override_torque()

        print(f"[INFO] Angle: {angle:.2f}°, Speed: {speed:.2f}, Gear: {gear}, Torque: {torque:.2f}")
        self.log("Start Reset", angle, speed, gear, torque)

        if not self.should_reset(angle):
            self.log("No Reset Needed", angle, speed, gear, torque)
            return

        direction = -1 if angle > 0 else 1

        while abs(angle) > 0.5:
            speed = self.vehicle.speed()
            gear = self.vehicle.gear()
            torque = self.steering.get_driver_override_torque()

            if not self.is_parked():
                self.log("ABORT: Vehicle moved or gear changed", angle, speed, gear, torque)
                break

            if abs(torque) > MAX_DRIVER_TORQUE:
                self.log("ABORT: Driver override", angle, speed, gear, torque)
                break

            self.steering.send_torque(direction * RESET_SPEED)
            time.sleep(0.1)
            angle = self.steering.get_angle()
            self.log("Adjusting", angle, speed, gear, torque)
            self.angle_data.append(angle)
            self.time_data.append(time.time())

        self.steering.stop()
        self.log("Reset Complete", angle, speed, gear, torque)

    def run(self):
        print("[INIT] Logging and Reset Controller Running")
        while True:
            if self.is_parked():
                self.reset()
            time.sleep(2)

if __name__ == "__main__":
    import sys
    mock_mode = "--mock" in sys.argv
    try:
        controller = SteeringResetController(mock=mock_mode)
        controller.run()
    except KeyboardInterrupt:
        print("[EXIT] Controller Stopped")
