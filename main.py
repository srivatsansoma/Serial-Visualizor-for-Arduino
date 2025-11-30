"""
Arduino Sensor Monitor - Entry Point

A real-time sensor monitoring dashboard for Arduino.
Run this file to start the application.
"""

import tkinter as tk
from app import SensorApp


def main():
    """Creates and runs the sensor monitoring application."""
    root = tk.Tk()
    app = SensorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
