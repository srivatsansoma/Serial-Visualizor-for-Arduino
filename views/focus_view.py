"""
Focus view - displays a single sensor in fullscreen with a large graph.
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class FocusView:
    """
    Mode 2: Shows one sensor at a time with a large display.
    Includes a dropdown to switch between sensors.
    """

    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.focus_sensor = 0
        self.focus_label = None
        self.fig = None
        self.ax = None
        self.line = None
        self.canvas = None

        # References to shared data (set by build())
        self.time_data = None
        self.history = None

    def build(self, sensor_index, time_data, history):
        """Creates the focus view UI for a single sensor."""
        self.focus_sensor = sensor_index
        self.time_data = time_data
        self.history = history

        # Header
        title = tk.Label(
            self.parent,
            text=f"Sensor {sensor_index + 1} Fullscreen",
            font=("Arial", 32),
            fg="red"
        )
        title.pack(pady=20)

        # Big value display
        self.focus_label = tk.Label(
            self.parent,
            text="--",
            font=("Arial", 80),
            fg="red"
        )
        self.focus_label.pack(pady=20)

        # Large graph
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.line, = self.ax.plot([], [], "r-", linewidth=2)
        self.ax.set_title(f"Sensor {sensor_index + 1} History")
        self.ax.set_xlabel("Time (samples)")
        self.ax.set_ylabel("Value")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        NavigationToolbar2Tk(self.canvas, self.parent)

        # Sensor selector dropdown
        selector = ttk.Combobox(
            self.parent,
            values=[f"Sensor {i + 1}" for i in range(4)]
        )
        selector.current(sensor_index)
        selector.pack(pady=10)
        selector.bind("<<ComboboxSelected>>", self._on_sensor_change)
        self.selector = selector

    def _on_sensor_change(self, event):
        """Handles sensor selection change from dropdown."""
        self.focus_sensor = self.selector.current()
        self.ax.set_title(f"Sensor {self.focus_sensor + 1} History")
        self.line.set_data(self.time_data, self.history[self.focus_sensor])
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

        if self.history[self.focus_sensor]:
            self.focus_label.config(text=str(self.history[self.focus_sensor][-1]))

    def get_focus_sensor(self):
        """Returns the currently focused sensor index."""
        return self.focus_sensor

    def update(self, values, time_data, history, window_size):
        """Updates the focused sensor display with new values."""
        self.time_data = time_data
        self.history = history

        sensor_val = values[self.focus_sensor]
        self.focus_label.config(text=str(sensor_val))

        self.line.set_data(time_data, history[self.focus_sensor])
        self.ax.set_xlim(max(0, time_data[-1] - window_size), time_data[-1])
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)
        self.canvas.draw()

