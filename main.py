
import time
from nissan_interface import NissanSteering, NissanVehicle
from obd_safety_check import detect_obd_conflict

STEERING_THRESHOLD = 2.0  # Degrees
RESET_SPEED = 0.5         # Degrees per cycle

class SteeringResetController:
    def __init__(self, mock=False):
        self.vehicle = NissanVehicle(mock=mock)
        self.steering = NissanSteering(mock=mock)
        self.mock = mock

    def is_parked(self):
        return self.vehicle.speed() == 0 and self.vehicle.gear() in ['P', 'R']

    def should_reset(self, angle):
        return abs(angle) > STEERING_THRESHOLD

    def reset(self):
        angle = self.steering.get_angle()
        print(f"[INFO] Current steering angle: {angle:.2f}°")

        if not self.should_reset(angle):
            print("[INFO] No steering reset needed.")
            return

        direction = -1 if angle > 0 else 1

        while abs(angle) > 0.5:
            if not self.is_parked():
                print("[ABORT] Vehicle moved or gear changed.")
                break

            self.steering.send_torque(direction * RESET_SPEED)
            time.sleep(0.1)
            angle = self.steering.get_angle()

        self.steering.stop()
        print("[SUCCESS] Steering reset complete.")

    def run(self):
        print("[INIT] Nissan Steering Reset Controller Running")
        while True:
            if self.is_parked():
                self.reset()
            time.sleep(2)

if __name__ == "__main__":
    import sys
    mock_mode = "--mock" in sys.argv

    # Run safety check first
    if not mock_mode and detect_obd_conflict():
        print("[BLOCKED] Steering reset will not run during diagnostics.")
        exit()

    try:
        SteeringResetController(mock=mock_mode).run()
    except KeyboardInterrupt:
        print("[EXIT] Controller Stopped")
