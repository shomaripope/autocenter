# -*- coding: utf-8 -*-

import tkinter as tk
import subprocess
import sys
import os

def run_main(mode):
    cmd = [sys.executable, "main.py"]
    if mode == "Mock":
        cmd.append("--mock")
    subprocess.Popen(cmd)

def run_dashboard():
    subprocess.Popen([sys.executable, "dashboard.py", "--mock"])

def open_log():
    log_file = "steering_log.txt"
    if os.path.exists(log_file):
        if sys.platform == "darwin":
            subprocess.run(["open", log_file])
        elif sys.platform == "win32":
            os.startfile(log_file)
        else:
            subprocess.run(["xdg-open", log_file])
    else:
        print("No log file found.")

def create_gui():
    root = tk.Tk()
    root.title("Nissan Steering Reset Launcher")
    root.geometry("300x260")
    root.resizable(False, False)

    title = tk.Label(root, text="Steering Reset Control", font=("Helvetica", 16, "bold"))
    title.pack(pady=10)

    tk.Button(root, text="Start (Live Mode)", width=25, command=lambda: run_main("Live")).pack(pady=5)
    tk.Button(root, text="Start (Mock Mode)", width=25, command=lambda: run_main("Mock")).pack(pady=5)
    tk.Button(root, text="Open Dashboard", width=25, command=run_dashboard).pack(pady=5)
    tk.Button(root, text="Open Log File", width=25, command=open_log).pack(pady=5)

    tk.Label(root, text="© shomaripope.com", fg="gray").pack(side="bottom", pady=8)

    root.mainloop()

if __name__ == "__main__":
    create_gui()