"""
Dashboard view - displays all 4 sensors in a 2x2 grid with mini graphs.
"""

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class DashboardView:
    """
    Mode 1: Shows all sensors at once in a grid layout.
    Each sensor has a value label and a mini graph.
    """

    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.sensor_labels = []
        self.mini_graphs = []
        self.mini_lines = []

    def build(self):
        """Creates the dashboard UI with 4 sensor panels."""
        self.sensor_labels = []
        self.mini_graphs = []
        self.mini_lines = []

        for i in range(4):
            # Each sensor gets its own panel
            frame = tk.Frame(self.parent, bd=4, relief="ridge", bg="black")
            frame.grid(row=i // 2, column=i % 2, padx=20, pady=20, sticky="nsew")

            # Current value display
            label = tk.Label(
                frame,
                text=f"Sensor {i + 1}: --",
                font=("Arial", 32),
                fg="red",
                bg="black"
            )
            label.pack(pady=10)
            self.sensor_labels.append(label)

            # Mini graph for recent history
            fig, ax = plt.subplots(figsize=(3, 2))
            line, = ax.plot([], [], "r-", linewidth=1.5)
            ax.set_title(f"S{i + 1}", fontsize=10)
            ax.set_xlabel("t", fontsize=8)
            ax.set_ylabel("val", fontsize=8)
            ax.tick_params(axis="both", labelsize=8)

            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            NavigationToolbar2Tk(canvas, frame)

            self.mini_graphs.append((fig, ax, canvas))
            self.mini_lines.append(line)

        # Make the grid cells expandable
        self.parent.rowconfigure([0, 1], weight=1)
        self.parent.columnconfigure([0, 1], weight=1)

    def update(self, values, time_data, history, window_size):
        """Updates all sensor displays with new values."""
        for i, label in enumerate(self.sensor_labels):
            label.config(text=f"Sensor {i + 1}: {values[i]}")

            line = self.mini_lines[i]
            fig, ax, canvas = self.mini_graphs[i]

            line.set_data(time_data, history[i])
            ax.set_xlim(max(0, time_data[-1] - window_size), time_data[-1])
            ax.relim()
            ax.autoscale_view(True, True, True)
            canvas.draw()

