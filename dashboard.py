
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from nissan_interface import NissanSteering, NissanVehicle

class LiveDashboard:
    def __init__(self, mock=False):
        self.vehicle = NissanVehicle(mock=mock)
        self.steering = NissanSteering(mock=mock)
        self.mock = mock
        self.angle_data = []
        self.torque_data = []
        self.time_data = []
        self.start_time = time.time()

        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1)
        self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=500)

    def update_plot(self, frame):
        t = time.time() - self.start_time
        angle = self.steering.get_angle()
        torque = self.steering.get_driver_override_torque()

        self.angle_data.append(angle)
        self.torque_data.append(torque)
        self.time_data.append(t)

        if len(self.time_data) > 100:
            self.time_data.pop(0)
            self.angle_data.pop(0)
            self.torque_data.pop(0)

        self.ax1.clear()
        self.ax2.clear()

        self.ax1.plot(self.time_data, self.angle_data, label="Steering Angle (°)")
        self.ax2.plot(self.time_data, self.torque_data, label="Driver Torque")

        self.ax1.set_ylabel("Angle (°)")
        self.ax2.set_ylabel("Torque")
        self.ax2.set_xlabel("Time (s)")

        self.ax1.legend()
        self.ax2.legend()

    def run(self):
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    import sys
    mock_mode = "--mock" in sys.argv
    dash = LiveDashboard(mock=mock_mode)
    dash.run()
