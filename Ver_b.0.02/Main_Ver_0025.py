import tkinter as tk
from tkinter import filedialog, ttk
import xml.etree.ElementTree as ET
from PIL import Image, ImageTk
from ttkthemes import ThemedTk
import os
import obspy
import matplotlib.pyplot as plt

class DateTimePopup:
    def __init__(self, parent, title, prefix):
        self.parent = parent
        self.title = title
        self.prefix = prefix
        self.result = None

        self.top = tk.Toplevel(parent)
        self.top.title(self.title)

        self.create_date_time_input()

        self.confirm_button = ttk.Button(self.top, text="Confirm Time Selection", command=self.confirm_selection)
        self.confirm_button.pack(pady=10)

    def create_date_time_input(self):
        # Year Input
        self.year_label = ttk.Label(self.top, text="Year:")
        self.year_label.pack(side=tk.LEFT)
        self.year_combobox = ttk.Combobox(self.top, values=[str(year) for year in range(2000, 2031)])
        self.year_combobox.pack(side=tk.LEFT)

        # Month Input
        self.month_label = ttk.Label(self.top, text="Month:")
        self.month_label.pack(side=tk.LEFT)
        self.month_combobox = ttk.Combobox(self.top, values=[str(month) for month in range(1, 13)])
        self.month_combobox.pack(side=tk.LEFT)

        # Day Input
        self.day_label = ttk.Label(self.top, text="Day:")
        self.day_label.pack(side=tk.LEFT)
        self.day_combobox = ttk.Combobox(self.top, values=[str(day) for day in range(1, 32)])
        self.day_combobox.pack(side=tk.LEFT)

        # Hour Input
        self.hour_label = ttk.Label(self.top, text="Hour:")
        self.hour_label.pack(side=tk.LEFT)
        self.hour_combobox = ttk.Combobox(self.top, values=[str(hour) for hour in range(24)])
        self.hour_combobox.pack(side=tk.LEFT)

        # Minute Input
        self.minute_label = ttk.Label(self.top, text="Minute:")
        self.minute_label.pack(side=tk.LEFT)
        self.minute_combobox = ttk.Combobox(self.top, values=[str(minute) for minute in range(60)])
        self.minute_combobox.pack(side=tk.LEFT)

        # Second Input
        self.second_label = ttk.Label(self.top, text="Second:")
        self.second_label.pack(side=tk.LEFT)
        self.second_combobox = ttk.Combobox(self.top, values=[str(second) for second in range(60)])
        self.second_combobox.pack(side=tk.LEFT)

    def confirm_selection(self):
        year = self.year_combobox.get()
        month = self.month_combobox.get()
        day = self.day_combobox.get()
        hour = self.hour_combobox.get()
        minute = self.minute_combobox.get()
        second = self.second_combobox.get()
        self.result = f"{year}-{month}-{day} {hour}:{minute}:{second}"
        self.top.destroy()

class App:
    def __init__(self, root):
        self.root = root
        root.title("Sprit HVSR Data Visualization")
        root.geometry("1200x800")

        # Create left panel for information input
        self.left_panel = ttk.Frame(root)
        self.left_panel.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Row for file loading options
        self.file_options_frame = ttk.Frame(self.left_panel)
        self.file_options_frame.pack(pady=(0, 10), padx=10, anchor="w")

        ttk.Style().configure("TButton", padding=10)

        self.load_sac_button = ttk.Button(self.file_options_frame, text="Load SAC File", command=self.load_sac_file)
        self.load_sac_button.pack(side=tk.LEFT, padx=(0, 10))

        self.load_miniseed_button = ttk.Button(self.file_options_frame, text="Load MiniSEED File", command=self.load_miniseed_file)
        self.load_miniseed_button.pack(side=tk.LEFT, padx=(0, 10))

        self.load_saseme_button = ttk.Button(self.file_options_frame, text="Load SASEME File", command=self.load_saseme_file)
        self.load_saseme_button.pack(side=tk.LEFT)

        # Start Time Input Area
        self.start_time_frame = ttk.Frame(self.left_panel)
        self.start_time_frame.pack(pady=(10, 0), padx=10, anchor="w")

        self.start_time_popup_button = ttk.Button(self.start_time_frame, text="Select Start Time", command=lambda: self.open_date_time_popup("Start Time", "start"))
        self.start_time_popup_button.pack(side=tk.LEFT)

        self.start_time_display_label = ttk.Label(self.start_time_frame, text="")
        self.start_time_display_label.pack(side=tk.LEFT, padx=(10, 0))

        # End Time Input Area
        self.end_time_frame = ttk.Frame(self.left_panel)
        self.end_time_frame.pack(pady=(10, 0), padx=10, anchor="w")

        self.end_time_popup_button = ttk.Button(self.end_time_frame, text="Select End Time", command=lambda: self.open_date_time_popup("End Time", "end"))
        self.end_time_popup_button.pack(side=tk.LEFT)

        self.end_time_display_label = ttk.Label(self.end_time_frame, text="")
        self.end_time_display_label.pack(side=tk.LEFT, padx=(10, 0))

        # Network Input
        self.network_label = ttk.Label(self.left_panel, text="Network:")
        self.network_label.pack(anchor="w", pady=(10, 0))
        self.network_entry = ttk.Entry(self.left_panel, width=30)
        self.network_entry.pack(pady=(0, 10), padx=(10, 0), anchor="w")

        # Station Input
        self.station_label = ttk.Label(self.left_panel, text="Station:")
        self.station_label.pack(anchor="w", pady=(10, 0))
        self.station_entry = ttk.Entry(self.left_panel, width=30)
        self.station_entry.pack(pady=(0, 10), padx=(10, 0), anchor="w")

        # Location Input
        self.location_label = ttk.Label(self.left_panel, text="Location:")
        self.location_label.pack(anchor="w", pady=(10, 0))
        self.location_entry = ttk.Entry(self.left_panel, width=30)
        self.location_entry.pack(pady=(0, 10), padx=(10, 0), anchor="w")

        # Channel Input
        self.channel_label = ttk.Label(self.left_panel, text="Channel:")
        self.channel_label.pack(anchor="w", pady=(10, 0))
        self.channel_entry = ttk.Entry(self.left_panel, width=30)
        self.channel_entry.pack(pady=(0, 10), padx=(10, 0), anchor="w")

        # New Input Fields
        self.ymax_label = ttk.Label(self.left_panel, text="Y Max Limit:")
        self.ymax_label.pack(anchor="w", pady=(10, 0))
        self.ymax_entry = ttk.Entry(self.left_panel, width=30)
        self.ymax_entry.pack(pady=(0, 10), padx=(10, 0), anchor="w")

        self.xtype_label = ttk.Label(self.left_panel, text="X Axis Type:")
        self.xtype_label.pack(anchor="w", pady=(10, 0))
        self.xtype_combobox = ttk.Combobox(self.left_panel, values=["frequency", "period"])
        self.xtype_combobox.pack(pady=(0, 10), padx=(10, 0), anchor="w")

        self.n_label = ttk.Label(self.left_panel, text="Number of Segments:")
        self.n_label.pack(anchor="w", pady=(10, 0))
        self.n_entry = ttk.Entry(self.left_panel, width=30)
        self.n_entry.pack(pady=(0, 10), padx=(10, 0), anchor="w")

        self.removeoutliers_label = ttk.Label(self.left_panel, text="Remove Outliers:")
        self.removeoutliers_label.pack(anchor="w", pady=(10, 0))
        self.removeoutliers_combobox = ttk.Combobox(self.left_panel, values=["yes", "no"])
        self.removeoutliers_combobox.pack(pady=(0, 10), padx=(10, 0), anchor="w")

        self.method_label = ttk.Label(self.left_panel, text="Method:")
        self.method_label.pack(anchor="w", pady=(10, 0))
        self.method_combobox = ttk.Combobox(self.left_panel, values=[str(i) for i in range(1, 7)])
        self.method_combobox.pack(pady=(0, 10), padx=(10, 0), anchor="w")

        # Calculate HVSR Button
        self.calculate_hvsr_button = ttk.Button(self.left_panel, text="Calculate HVSR", command=self.calculate_hvsr)
        self.calculate_hvsr_button.pack(pady=10, anchor="w")

        # Label to display the selected file path
        self.selected_file_label = ttk.Label(self.left_panel, text="", font=("Arial", 10, "italic"))
        self.selected_file_label.pack(pady=5, padx=(10, 0), anchor="w")

        # Create right panel for visualization (unchanged)
        self.right_panel = ttk.Frame(root)
        self.right_panel.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.visualization_label = ttk.Label(self.right_panel, text="HVSR Simple Program")
        self.visualization_label.pack(fill=tk.X)

        # Load and display the default image
        self.default_image = Image.open("img/HVSR_GUI_1.jpg")
        self.default_image = ImageTk.PhotoImage(self.default_image)
        self.visualization_canvas = tk.Canvas(self.right_panel, width=600, height=600)  # Updated canvas size
        self.visualization_canvas.create_image(0, 0, anchor=tk.NW, image=self.default_image)
        self.visualization_canvas.pack(fill=tk.BOTH, expand=True)

    def open_date_time_popup(self, title, prefix):
        popup = DateTimePopup(self.root, title, prefix)
        self.root.wait_window(popup.top)
        result = popup.result
        if result:
            if prefix == "start":
                self.start_time_display_label.config(text=result)
            elif prefix == "end":
                self.end_time_display_label.config(text=result)

    def load_sac_file(self):
        self.sac_file_path = filedialog.askopenfilename(filetypes=[("SAC Files", "*.sac")])
        if self.sac_file_path:
            confirmation_message = f"Selected SAC file: {self.sac_file_path}"
            self.selected_file_label.config(text=confirmation_message)
            self.show_confirmation(confirmation_message)

    def load_miniseed_file(self):
        self.miniseed_file_path = filedialog.askopenfilename(filetypes=[("MiniSEED Files", "*.mseed")])
        if self.miniseed_file_path:
            confirmation_message = f"Selected MiniSEED file: {self.miniseed_file_path}"
            self.selected_file_label.config(text=confirmation_message)
            self.show_confirmation(confirmation_message)

    def load_saseme_file(self):
        self.saseme_file_path = filedialog.askopenfilename(filetypes=[("SASEME Files", "*.saseme")])
        if self.saseme_file_path:
            confirmation_message = f"Selected SASEME file: {self.saseme_file_path}"
            self.selected_file_label.config(text=confirmation_message)
            self.show_confirmation(confirmation_message)

    def show_confirmation(self, message):
        confirmation_window = tk.Toplevel(self.root)
        confirmation_window.title("Confirmation")
        confirmation_label = ttk.Label(confirmation_window, text=message)
        confirmation_label.pack(padx=20, pady=20)

    def calculate_hvsr(self):
        # Get all user input information, including file paths and variables
        sac_file_path = self.sac_file_path if hasattr(self, "sac_file_path") else ""
        miniseed_file_path = self.miniseed_file_path if hasattr(self, "miniseed_file_path") else ""
        saseme_file_path = self.saseme_file_path if hasattr(self, "saseme_file_path") else ""
        start_time = self.start_time_display_label.cget("text")
        end_time = self.end_time_display_label.cget("text")
        network = self.network_entry.get()
        station = self.station_entry.get()
        location = self.location_entry.get()
        channel = self.channel_entry.get()
        ymax = self.ymax_entry.get()
        xtype = self.xtype_combobox.get()
        n = self.n_entry.get()
        removeoutliers = self.removeoutliers_combobox.get()
        method = self.method_combobox.get()

        # Create an XML structure with the user's input
        root = ET.Element("data")
        ET.SubElement(root, "start_time").text = start_time
        ET.SubElement(root, "end_time").text = end_time
        ET.SubElement(root, "network").text = network
        ET.SubElement(root, "station").text = station
        ET.SubElement(root, "location").text = location
        ET.SubElement(root, "channel").text = channel
        ET.SubElement(root, "ymax").text = ymax
        ET.SubElement(root, "xtype").text = xtype
        ET.SubElement(root, "n").text = n
        ET.SubElement(root, "removeoutliers").text = removeoutliers
        ET.SubElement(root, "method").text = method
        ET.SubElement(root, "sac_file_path").text = sac_file_path
        ET.SubElement(root, "miniseed_file_path").text = miniseed_file_path
        ET.SubElement(root, "saseme_file_path").text = saseme_file_path

        # Save the XML to a file in the current directory
        xml_file_path = "user.xml"
        tree = ET.ElementTree(root)
        tree.write(xml_file_path)

        # Display a confirmation message
        confirmation_message = f"User Input Information Saved to {xml_file_path}"
        self.show_information(confirmation_message)

        # Plot the SAC file (if selected)
        if sac_file_path:
            st = obspy.read(sac_file_path)
            if len(st) > 0:
                st.plot()
                plt.show()
            else:
                self.show_information("No data found in the selected SAC file.")

    def show_information(self, message):
        information_window = tk.Toplevel(self.root)
        information_window.title("User Input Information")
        information_label = ttk.Label(information_window, text=message, font=("Arial", 10))
        information_label.pack(padx=20, pady=20)

def main():
    root = ThemedTk(theme="winthemes")
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()

