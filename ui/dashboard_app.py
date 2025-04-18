
import tkinter as tk
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from analyzers.global_analyzer import GlobalAnalyzer
from bson import json_util
import json
import csv
import os

class DashboardApp:
    def __init__(self, root, keyword_data, scenario_data, path_data, analyzers):
        self.root = root
        self.root.title("ENCORE Analytics Dashboard")
        self.tab_control = ttk.Notebook(root)

        self.tabs = {
            "Global Summary": (None, None),
            "Keyword Analysis": (keyword_data, analyzers["keywords"]),
            "Learning Scenarios": (scenario_data, analyzers["scenarios"]),
            "Learning Paths": (path_data, analyzers["paths"]),
        }

        self.tab_frames = {}

        for tab_name in self.tabs:
            tab = ttk.Frame(self.tab_control)
            self.tab_control.add(tab, text=tab_name)
            self.tab_frames[tab_name] = tab

        self.tab_control.pack(expand=1, fill="both")

        self.keyword_data = keyword_data
        self.scenario_data = scenario_data
        self.path_data = path_data

        self.show_global_summary()
        self.show_analysis("Keyword Analysis", analyzers["keywords"], keyword_data)
        self.show_analysis("Learning Scenarios", analyzers["scenarios"], scenario_data)
        self.show_analysis("Learning Paths", analyzers["paths"], path_data)

    def show_analysis(self, tab_name, analyzer_class, data):
        analyzer = analyzer_class(data)
        fig = analyzer.create_figure()
        if fig:
            frame = ttk.Frame(self.tab_frames[tab_name])
            frame.pack(fill=tk.BOTH, expand=1)

            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            toolbar = NavigationToolbar2Tk(canvas, frame)
            toolbar.update()
            toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    def show_global_summary(self):
        analyzer = GlobalAnalyzer(self.keyword_data, self.scenario_data, self.path_data)
        summary = analyzer.summarize()

        frame = ttk.Frame(self.tab_frames["Global Summary"])
        frame.pack(fill=tk.BOTH, expand=1)

        for idx, (key, value) in enumerate(summary.items()):
            label = ttk.Label(frame, text=f"{key}: {value}", font=("Arial", 12))
            label.grid(row=idx, column=0, sticky=tk.W, padx=20, pady=5)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=len(summary) + 1, column=0, pady=10, padx=20, sticky=tk.W)

        csv_button = ttk.Button(button_frame, text="Export Datasets as CSV", command=self.export_csvs)
        csv_button.pack(side=tk.LEFT, padx=5)

        json_button = ttk.Button(button_frame, text="Export Datasets as JSON", command=self.export_jsons)
        json_button.pack(side=tk.LEFT, padx=5)

    def export_csvs(self):
        dir_path = filedialog.askdirectory(title="Select Directory to Save CSV Files")
        if dir_path:
            datasets = {
                "keywords": self.keyword_data,
                "learningscenarios": self.scenario_data,
                "learningpaths": self.path_data
            }
            for name, data in datasets.items():
                try:
                    file_path = os.path.join(dir_path, f"{name}.csv")
                    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                        writer = csv.writer(file)
                        writer.writerow(["Field", "Value"])
                        for doc in data:
                            flat_doc = self.flatten_dict(json.loads(json_util.dumps(doc)))
                            for field, value in flat_doc.items():
                                writer.writerow([field, value])
                except Exception as e:
                    print(f"❌ Failed to export {name}.csv: {e}")

    def export_jsons(self):
        dir_path = filedialog.askdirectory(title="Select Directory to Save JSON Files")
        if dir_path:
            datasets = {
                "keywords": self.keyword_data,
                "learningscenarios": self.scenario_data,
                "learningpaths": self.path_data
            }
            for name, data in datasets.items():
                try:
                    file_path = os.path.join(dir_path, f"{name}.json")
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(json_util.dumps(data, indent=2))
                except Exception as e:
                    print(f"❌ Failed to export {name}.json: {e}")

    def flatten_dict(self, d, parent_key='', sep='.'):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
