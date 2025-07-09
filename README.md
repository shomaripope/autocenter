
# Nissan Steering Reset Program

This Python program resets the steering wheel angle to 0° after the vehicle is parked, for Nissan vehicles with EPS or steer-by-wire systems.

## Features
- Monitors gear and speed via CAN bus.
- Automatically centers steering when parked.
- Mock mode for safe testing without a car.
- Safety checks to abort if vehicle starts moving.

## Files
- `main.py` – Main controller script
- `nissan_interface.py` – CAN bus and mock interface
- `README.md` – This documentation

## Usage

### Live Vehicle Mode:
```bash
python3 main.py
```

### Mock Test Mode:
```bash
python3 main.py --mock
```

Make sure your CAN interface is connected and enabled (`can0`).

## Safety Notes
- Test only on private property.
- Use mock mode before live deployment.
- Always monitor for errors.

