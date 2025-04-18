
import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")

from config import MONGO_URI, DB_NAME
from utils.db_client import MongoDBClient
from analyzers.keyword_analyzer import KeywordAnalyzer
from analyzers.scenario_analyzer import LearningScenarioAnalyzer
from analyzers.path_analyzer import LearningPathAnalyzer
from ui.dashboard_app import DashboardApp

def main():
    keyword_data = MongoDBClient(MONGO_URI, DB_NAME, "keywords")
    keyword_data.connect()
    keywords = keyword_data.fetch_data()

    scenario_data = MongoDBClient(MONGO_URI, DB_NAME, "learningscenarios")
    scenario_data.connect()
    scenarios = scenario_data.fetch_data()

    path_data = MongoDBClient(MONGO_URI, DB_NAME, "learningpaths")
    path_data.connect()
    paths = path_data.fetch_data()

    root = tk.Tk()
    analyzers = {
        "keywords": KeywordAnalyzer,
        "scenarios": LearningScenarioAnalyzer,
        "paths": LearningPathAnalyzer
    }
    app = DashboardApp(root, keywords, scenarios, paths, analyzers)
    root.mainloop()

if __name__ == "__main__":
    main()
