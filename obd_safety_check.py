
# obd_safety_check.py
import time
import can

def detect_obd_conflict():
    print("[INFO] Scanning OBD-II bus for critical messages...")
    bus = can.interface.Bus(channel='can0', bustype='socketcan')
    timeout = time.time() + 3
    while time.time() < timeout:
        msg = bus.recv(timeout=0.1)
        if msg:
            if msg.arbitration_id in [0x7E0, 0x7DF, 0x7E8]:  # ECU diag IDs
                print("[WARNING] OBD-II communication detected. Aborting...")
                return True
    print("[SAFE] No OBD diagnostics detected.")
    return False

if __name__ == "__main__":
    if detect_obd_conflict():
        print("[BLOCKED] Steering reset will not run during diagnostics.")
    else:
        print("[READY] Safe to run steering reset script.")
