from selfdrive.car.interfaces import CarStateBase

GEAR_MAP = {
  0x0: 'park',
  0x1: 'reverse',
  0x2: 'neutral',
  0x3: 'drive'
}

class CarState(CarStateBase):
    def __init__(self, CP):
        super().__init__(CP)

    def update(self, cp, cp_cam):
        ret = self.cp_state.copy()

        # Gear position from CAN ID 0x1C2, byte 1
        gear_raw = cp.vl["GEARBOX"].get("GEAR_STATE", 0)
        ret.gearShifter = GEAR_MAP.get(gear_raw, 'unknown')

        # Steering angle from EPS (CAN ID 0x2E4 or similar)
        ret.steeringAngle = cp.vl["STEER_ANGLE_SENSOR"]["STEERING_ANGLE"]

        # Vehicle speed (vEgo) from CAN ID 0x1F9, bytes 0 and 1
        speed_raw = cp.vl["WHEEL_SPEEDS"]["VEHICLE_SPEED"]
        ret.vEgo = speed_raw * 0.01  # scale to m/s

        return ret