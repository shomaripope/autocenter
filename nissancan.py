def create_steering_control(packer, frame, apply_steer, enabled):
    # Constants for Nissan EPS (these must match your DBC)
    STEER_MSG_ID = 0x2E4
    MAX_TORQUE = 1024

    steer = max(min(apply_steer, MAX_TORQUE), -MAX_TORQUE)
    steer_direction = 1 if steer >= 0 else 0
    steer_value = abs(steer)

    # Simple counter and checksum
    idx = frame % 4

    values = {
        "COUNTER": idx,
        "STEER_TORQUE_CMD": steer_value,
        "STEER_DIRECTION": steer_direction,
        "STEER_REQUEST": 1 if enabled else 0,
    }

    return packer.make_can_msg("STEERING_CONTROL", 0, values)