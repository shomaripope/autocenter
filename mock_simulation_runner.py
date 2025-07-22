import time
from threading import Thread

# Mock signal data to simulate OpenPilot's CarState interface
class MockCarState:
    def __init__(self):
        self.gearShifter = 'park'
        self.vEgo = 0.0  # Vehicle stopped
        self.steeringAngle = 25.0  # Start with the wheel turned

class MockActuators:
    def __init__(self):
        self.steer = 0.0  # No lane-keeping input

class MockPacker:
    def make_can_msg(self, msg_name, bus, values):
        print(f"CAN MSG -> {msg_name} | Bus {bus} | {values}")
        return (msg_name, bus, values)

# Stand-in for create_steering_control if not importing nissancan
create_steering_control = lambda packer, frame, steer, enabled: packer.make_can_msg(
    "STEERING_CONTROL", 0, {
        "COUNTER": frame % 4,
        "STEER_TORQUE_CMD": abs(steer),
        "STEER_DIRECTION": 1 if steer >= 0 else 0,
        "STEER_REQUEST": 1 if enabled else 0,
    }
)

class CarController:
    def __init__(self):
        self.packer = MockPacker()
        self.frame = 0

    def update(self, enabled, CS, actuators):
        if CS.gearShifter == 'park' and CS.vEgo < 0.1:
            angle_error = -CS.steeringAngle
            torque_cmd = int(max(min(angle_error * 5, 1024), -1024))
        else:
            torque_cmd = int(actuators.steer * 1024)

        return [create_steering_control(self.packer, self.frame, torque_cmd, enabled)]

# Run mock simulation
if __name__ == "__main__":
    CS = MockCarState()
    actuators = MockActuators()
    controller = CarController()

    def simulate():
        for _ in range(10):
            msgs = controller.update(True, CS, actuators)
            CS.steeringAngle -= 1.5  # Simulate centering per frame
            for msg in msgs:
                print(msg)
            time.sleep(0.1)

    Thread(target=simulate).start()
