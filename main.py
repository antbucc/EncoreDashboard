
import streamlit as st
from config import MONGO_URI, DB_NAME
from utils.db_client import MongoDBClient
from analyzers.keyword_analyzer import KeywordAnalyzer
from analyzers.scenario_analyzer import LearningScenarioAnalyzer
from analyzers.path_analyzer import LearningPathAnalyzer
from analyzers.global_analyzer import GlobalAnalyzer
from analyzers.advanced_analyzer import AdvancedLearningAnalytics
import json
import csv
import io

def fetch_data():
    keyword_data = MongoDBClient(MONGO_URI, DB_NAME, "keywords")
    keyword_data.connect()
    keywords = keyword_data.fetch_data()

    scenario_data = MongoDBClient(MONGO_URI, DB_NAME, "learningscenarios")
    scenario_data.connect()
    scenarios = scenario_data.fetch_data()

    path_data = MongoDBClient(MONGO_URI, DB_NAME, "learningpaths")
    path_data.connect()
    paths = path_data.fetch_data()

    return keywords, scenarios, paths

def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def to_csv(data):
    output = io.StringIO()
    if data:
        writer = csv.writer(output)
        writer.writerow(["Field", "Value"])
        for doc in data:
            flat_doc = flatten_dict(doc)
            for field, value in flat_doc.items():
                writer.writerow([field, value])
    return output.getvalue()

def to_json(data):
    return json.dumps(data, indent=2, default=str)

def main():
    st.set_page_config(page_title="ENCORE Analytics Dashboard", layout="wide")
    st.title("ENCORE Analytics Dashboard")

    keywords, scenarios, paths = fetch_data()

    tab = st.selectbox("Select View", ["Global Summary", "Keyword Analysis", "Learning Scenarios", "Learning Paths", "Advanced Insights"])

    if tab == "Global Summary":
        analyzer = GlobalAnalyzer(keywords, scenarios, paths)
        summary = analyzer.summarize()
        st.subheader("Summary")
        for key, value in summary.items():
            st.markdown(f"**{key}**: {value}")

        st.subheader("Export Datasets")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button("Download Keywords CSV", to_csv(keywords), "keywords.csv", "text/csv")
            st.download_button("Download Keywords JSON", to_json(keywords), "keywords.json", "application/json")
        with col2:
            st.download_button("Download Scenarios CSV", to_csv(scenarios), "scenarios.csv", "text/csv")
            st.download_button("Download Scenarios JSON", to_json(scenarios), "scenarios.json", "application/json")
        with col3:
            st.download_button("Download Paths CSV", to_csv(paths), "paths.csv", "text/csv")
            st.download_button("Download Paths JSON", to_json(paths), "paths.json", "application/json")

    elif tab == "Keyword Analysis":
        analyzer = KeywordAnalyzer(keywords)
        fig = analyzer.create_figure()
        if fig:
            st.pyplot(fig)

    elif tab == "Learning Scenarios":
        analyzer = LearningScenarioAnalyzer(scenarios)
        fig = analyzer.create_figure()
        if fig:
            st.pyplot(fig)

    elif tab == "Learning Paths":
        analyzer = LearningPathAnalyzer(paths)
        fig = analyzer.create_figure()
        if fig:
            st.pyplot(fig)

    elif tab == "Advanced Insights":
        analyzer = AdvancedLearningAnalytics(paths, scenarios)
        fig = analyzer.create_figure()
        if fig:
            st.pyplot(fig)

if __name__ == "__main__":
    main()
