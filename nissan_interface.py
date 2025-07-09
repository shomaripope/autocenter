
import random

try:
    import can
except ImportError:
    can = None  # Allow mock mode to run without python-can

class NissanVehicle:
    def __init__(self, mock=False):
        self.mock = mock
        if not self.mock and can:
            self.bus = can.interface.Bus(channel='can0', bustype='socketcan')

    def speed(self):
        if self.mock:
            return 0
        msg = self._recv_msg(0x1F9)
        if msg:
            speed = ((msg.data[0] << 8) + msg.data[1]) * 0.01
            return speed
        return 0

    def gear(self):
        if self.mock:
            return 'P'
        msg = self._recv_msg(0x1C2)
        if msg:
            gear_byte = msg.data[1]
            gear_map = {0x0: 'P', 0x1: 'R', 0x2: 'N', 0x3: 'D'}
            return gear_map.get(gear_byte, 'UNKNOWN')
        return 'UNKNOWN'

    def _recv_msg(self, arbitration_id, timeout=0.2):
        if self.mock:
            return None
        try:
            msg = self.bus.recv(timeout)
            if msg and msg.arbitration_id == arbitration_id:
                return msg
        except Exception as e:
            print(f"[ERROR] CAN read failed: {e}")
        return None

class NissanSteering:
    def __init__(self, mock=False):
        self.mock = mock
        self.mock_angle = 15.0
        self.mock_driver_torque = 0.0
        if not self.mock and can:
            self.bus = can.interface.Bus(channel='can0', bustype='socketcan')

    def get_angle(self):
        if self.mock:
            return self.mock_angle
        msg = self._recv_msg(0x2C4)
        if msg:
            raw = (msg.data[0] << 8) + msg.data[1]
            angle = (raw - 32768) * 0.1
            return angle
        return 0

    def get_driver_override_torque(self):
        if self.mock:
            return self.mock_driver_torque
        msg = self._recv_msg(0x2C4)
        if msg:
            torque_raw = msg.data[2]
            torque = (torque_raw - 127) * 0.1  # Simulated scale
            return torque
        return 0

    def send_torque(self, value):
        if self.mock:
            self.mock_angle += -value
            print(f"[MOCK] Simulated steering torque applied: {value}")
            return

        torque = int(value * 10) & 0xFF
        msg = can.Message(arbitration_id=0x2D4, data=[torque, 0x00, 0x00, 0, 0, 0, 0, 0], is_extended_id=False)
        try:
            self.bus.send(msg)
            print(f"[TX] Torque Command: {value}")
        except can.CanError:
            print("[ERROR] Failed to send torque command.")

    def stop(self):
        self.send_torque(0)

    def _recv_msg(self, arbitration_id, timeout=0.2):
        if self.mock:
            return None
        try:
            msg = self.bus.recv(timeout)
            if msg and msg.arbitration_id == arbitration_id:
                return msg
        except Exception as e:
            print(f"[ERROR] CAN read failed: {e}")
        return None
