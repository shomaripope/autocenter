from selfdrive.car.nissan.nissancan import create_steering_control
from opendbc.can.packer import CANPacker
from common.realtime import DT_CTRL

STEER_MAX = 1024
STEER_STEP = 1.0

class CarController:
    def __init__(self, dbc_name, CP, VM):
        self.packer = CANPacker(dbc_name)
        self.frame = 0
        self.last_steer = 0
        self.enabled_last = False

    def update(self, enabled, CS, actuators):
        can_sends = []

        # Auto-center when in Park and vehicle is stationary
        if CS.gearShifter == 'park' and CS.vEgo < 0.1:
            steering_angle = CS.steeringAngle
            angle_error = -steering_angle  # target is 0

            # Apply proportional control
            torque_cmd = int(max(min(angle_error * 5, STEER_MAX), -STEER_MAX))
        else:
            # Normal lateral control
            torque_cmd = int(actuators.steer * STEER_MAX)

        self.last_steer = torque_cmd
        steer_msg = create_steering_control(self.packer, self.frame, torque_cmd, enabled)
        if steer_msg:
            can_sends.append(steer_msg)

        self.frame += 1
        return can_sends