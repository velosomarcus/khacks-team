import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading

from openlch.hal import HAL


robot = HAL("192.168.42.1")


class DynamicGraphPlotter:
    def __init__(self, master):
        self.master = master
        master.title("Dynamic Dictionary Graph")
        master.geometry("800x600")

        # Initial dictionary
        self.data_dict = {}
        positions = robot.servo.get_positions()
        for item in positions:
            self.data_dict[str(item[0])] = int(item[1])

        # relax upper body servos
        robot.servo.set_torque_enable([(i, False) for i in range(11, 17)])

        # Create Matplotlib figure and canvas
        self.figure, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Button to manually update graph
        self.update_button = ttk.Button(master, text="Update Graph", command=self.update_graph)
        self.update_button.pack(pady=10)

        # Add key binding for quitting
        master.bind('q', self.quit_application)
        master.bind('Q', self.quit_application)

        # Start automatic update thread
        self.stop_event = threading.Event()
        self.update_thread = threading.Thread(target=self.auto_update, daemon=True)
        self.update_thread.start()

        # Initial graph plot
        self.plot_graph()

    def quit_application(self, event=None):
        """Quit the application"""
        self.stop_event.set()
        self.master.quit()
        self.master.destroy()

    def plot_graph(self):
        """Plot the graph based on current dictionary data"""
        # Clear previous plot
        self.ax.clear()

        # Extract keys and values from dictionary
        keys = list(self.data_dict.keys())
        values = list(self.data_dict.values())

        # Create bar plot
        self.ax.bar(keys, values)
        self.ax.set_title("Dynamic Servo Visualization")
        self.ax.set_xlabel("Keys")
        self.ax.set_ylabel("Values")

        # Refresh canvas
        self.canvas.draw()

    def update_graph(self):
        """Update graph with modified or new data"""
        # modify existing values
        positions = robot.servo.get_positions()
        for item in positions:
            self.data_dict[str(item[0])] = int(item[1])

        # Replot the graph
        self.plot_graph()

    def auto_update(self):
        """Automatically update graph every 10 seconds"""
        while not self.stop_event.is_set():
            # Use after method to update UI thread safely
            self.master.after(0, self.update_graph)
            time.sleep(0.25)

    def on_closing(self):
        """Handle window closing"""
        self.stop_event.set()
        self.master.destroy()


def main():
    root = tk.Tk()
    app = DynamicGraphPlotter(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()