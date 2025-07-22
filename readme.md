# Nissan Auto-Centering Steering Control (OpenPilot Add-on)

This module adds automatic steering wheel centering functionality to OpenPilot-compatible Nissan vehicles when the vehicle is parked and stationary. It is designed to prevent tire wear, curb damage, and unexpected vehicle movement due to misaligned steering wheels.

---

## 🚘 Features

- Detects when the vehicle is in Park and at rest
- Applies proportional steering torque to center the wheel back to 0°
- Fully integrated with OpenPilot’s control stack
- Safe, non-invasive: Respects EPS limits, CAN message checks, and gear state
- Includes simulation/test harness for use without a real vehicle

---

## 🧱 File Structure

| File                        | Purpose                                                |
| --------------------------- | ------------------------------------------------------ |
| `carcontroller.py`          | Injects auto-centering torque into EPS CAN stream      |
| `nissancan.py`              | Builds valid CAN messages for Nissan EPS               |
| `carstate.py`               | Decodes gear state, speed, and steering angle from CAN |
| `mock_simulation_runner.py` | CLI simulation tool that mimics a parked Nissan        |

---

## 🖥️ Requirements

### ✅ For Simulation

- Python 3.8+
- Git
- pip
- Linux, macOS, or Windows (for mock test only)

### ✅ For Real Vehicle Integration

- [OpenPilot](https://github.com/commaai/openpilot) fork installed
- Supported Nissan vehicle (see OpenPilot wiki)
- Panda or Comma device (e.g., Comma 3)

---

## 🧪 Quick Start (Simulation Mode)

1. Clone or download this repo
2. Run the simulation:

```bash
python3 mock_simulation_runner.py
```

3. Watch the console print CAN messages as the steering centers

---

## 🔧 Installation (Real Vehicle / OpenPilot Integration)

1. **Fork OpenPilot**

```bash
git clone https://github.com/commaai/openpilot.git
cd openpilot/selfdrive/car/nissan
```

2. **Replace Files** Copy these updated files into the Nissan car folder:

- `carcontroller.py`
- `carstate.py`
- `nissancan.py`

3. **Verify .dbc Signals** Ensure your Nissan `.dbc` file includes:

- `STEERING_CONTROL`
- `GEARBOX`
- `STEER_ANGLE_SENSOR`
- `WHEEL_SPEEDS`

4. **Rebuild and Flash** Use OpenPilot dev tools or Comma connect interface to test in your vehicle.

---

## 🛠️ Debugging Tools

| Tool          | Usage                              |
| ------------- | ---------------------------------- |
| `PlotJuggler` | Plot steering angle, torque, speed |
| `Cabana`      | Visualize CAN logs online          |
| `candump`     | Watch real CAN traffic             |
| `replay.py`   | Inject logs into OpenPilot stack   |

---

## 🧠 How It Works

- When the car is in Park (`gearShifter == 'park'`) and speed is \~0, the system calculates:
  ```
  angle_error = 0 - current_steering_angle
  torque = clamp(angle_error * k_p, ±1024)
  ```
- This torque is sent to the steering controller until the wheel returns to center.

---

## 🔐 Licensing & Patent Notice

This project implements novel behavior that may be eligible for patent protection. Do not commercialize without permission from the author.

© 2025 Ari Pope. All rights reserved.

---

## 🙋 Need Help?

- GitHub: [https://github.com/shomaripope](https://github.com/shomaripope)
- Email: [shomari@shomaripope.com](mailto\:shomari@shomaripope.com)

