"""
Main application class that orchestrates the sensor monitoring app.
Handles menu setup, mode switching, and data updates.
"""

import tkinter as tk
from tkinter import ttk

from serial_handler import SerialHandler, get_available_ports, is_serial_available
from views.dashboard import DashboardView
from views.focus_view import FocusView


class SensorApp:
    """
    Arduino Sensor Monitor Application.
    Displays 4 sensor values with live-updating graphs.
    Supports two viewing modes: Dashboard and Focus view.
    """

    # View mode constants
    MODE_DASHBOARD = 1
    MODE_FOCUS = 2

    def __init__(self, root):
        self.root = root
        self.root.title("Arduino Sensor Monitor")
        self.root.geometry("1400x900")

        # Data storage for sensor readings
        self.history = [[] for _ in range(4)]
        self.time = []
        self.window_size = 30

        # Serial communication handler
        self.serial = SerialHandler()

        # Main container for all views
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # View instances
        self.dashboard_view = None
        self.focus_view = None
        self.current_mode = None

        # Build the UI
        self._setup_menu()
        self.switch_to_dashboard()

        # Start the update loop
        self._update_loop()

    def _setup_menu(self):
        """Creates the application menu bar."""
        menubar = tk.Menu(self.root)

        # Mode switching menu
        mode_menu = tk.Menu(menubar, tearoff=0)
        mode_menu.add_command(label="Dashboard (Mode 1)", command=self.switch_to_dashboard)
        mode_menu.add_command(label="Focus View (Mode 2)", command=self.switch_to_focus)
        menubar.add_cascade(label="Modes", menu=mode_menu)

        # Serial connection menu
        serial_menu = tk.Menu(menubar, tearoff=0)
        serial_menu.add_command(label="Setup Serial", command=self._show_serial_dialog)
        menubar.add_cascade(label="Serial", menu=serial_menu)

        self.root.config(menu=menubar)

    def _show_serial_dialog(self):
        """Opens the serial connection setup dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Serial Setup")
        dialog.geometry("400x200")

        # Port selection
        tk.Label(dialog, text="Serial Port:").pack(pady=5)
        ports = get_available_ports()
        port_var = tk.StringVar(value=ports[0] if ports else "")
        port_dropdown = ttk.Combobox(dialog, textvariable=port_var, values=ports, width=30)
        port_dropdown.pack(pady=5)

        # Baudrate input
        tk.Label(dialog, text="Baudrate:").pack(pady=5)
        baud_var = tk.StringVar(value="9600")
        baud_entry = tk.Entry(dialog, textvariable=baud_var)
        baud_entry.pack(pady=5)

        def on_connect():
            if self.serial.connect(port_var.get(), int(baud_var.get())):
                dialog.destroy()

        tk.Button(dialog, text="Connect", command=on_connect).pack(pady=10)

    def _clear_frame(self):
        """Removes all widgets from the main frame."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def switch_to_dashboard(self):
        """Switches to the dashboard view (Mode 1)."""
        self._clear_frame()
        self.current_mode = self.MODE_DASHBOARD
        self.dashboard_view = DashboardView(self.main_frame)
        self.dashboard_view.build()

    def switch_to_focus(self, sensor_index=0):
        """Switches to the focus view (Mode 2)."""
        self._clear_frame()
        self.current_mode = self.MODE_FOCUS
        self.focus_view = FocusView(self.main_frame)
        self.focus_view.build(sensor_index, self.time, self.history)

    def _update_loop(self):
        """Fetches sensor data and updates the display. Runs every second."""
        values = self.serial.read_sensors()

        # Update time axis
        t = (self.time[-1] + 1) if self.time else 0
        self.time.append(t)
        if len(self.time) > self.window_size:
            self.time = self.time[-self.window_size:]

        # Update sensor history
        for i in range(4):
            self.history[i].append(values[i])
            if len(self.history[i]) > self.window_size:
                self.history[i] = self.history[i][-self.window_size:]

        # Update the active view
        if self.current_mode == self.MODE_DASHBOARD and self.dashboard_view:
            self.dashboard_view.update(values, self.time, self.history, self.window_size)
        elif self.current_mode == self.MODE_FOCUS and self.focus_view:
            self.focus_view.update(values, self.time, self.history, self.window_size)

        # Schedule next update
        self.root.after(1000, self._update_loop)

