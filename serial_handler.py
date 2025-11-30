"""
Handles serial communication with Arduino.
Provides connection management and sensor data reading.
"""

import random
import time
from tkinter import messagebox

# Check if pyserial is available
try:
    import serial
    import serial.tools.list_ports
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False


def get_available_ports():
    """Returns a list of available serial port names."""
    if SERIAL_AVAILABLE:
        return [p.device for p in serial.tools.list_ports.comports()]
    return []


def is_serial_available():
    """Returns True if pyserial is installed."""
    return SERIAL_AVAILABLE


class SerialHandler:
    """Manages the serial connection to Arduino."""

    def __init__(self):
        self.connection = None

    def connect(self, port, baudrate):
        """
        Opens a serial connection to the specified port.
        Returns True on success, False on failure.
        """
        if not SERIAL_AVAILABLE:
            messagebox.showerror("Error", "pyserial not installed.")
            return False

        try:
            self.connection = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)  # Wait for Arduino to reset after connection
            messagebox.showinfo("Success", f"Connected to {port}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {e}")
            return False

    def disconnect(self):
        """Closes the serial connection if open."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def is_connected(self):
        """Returns True if a serial connection is active."""
        return self.connection is not None

    def read_sensors(self, num_sensors=4):
        """
        Reads sensor values from Arduino.
        Protocol: Send [0x02][0x05][0x03], receive [0x02][0x05]<csv data>[0x03]
        Returns random values if not connected or on error.
        """
        if not self.connection:
            return [random.randint(10, 100) for _ in range(num_sensors)]

        try:
            self.connection.reset_input_buffer()
            self.connection.write(b"\x02\x05\x03")
            raw = self.connection.read_until(expected=b"\x03", size=64)

            if raw and raw[0] == 0x02 and raw[1] == 0x05 and raw[-1] == 0x03:
                payload = raw[2:-1].decode("utf-8").strip()
                vals = [int(x) for x in payload.split(",")]
                if len(vals) == num_sensors:
                    return vals
        except Exception:
            pass

        return [random.randint(10, 100) for _ in range(num_sensors)]

