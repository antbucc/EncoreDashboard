
class GlobalAnalyzer:
    def __init__(self, keyword_data, scenario_data, path_data):
        self.keyword_data = keyword_data
        self.scenario_data = scenario_data
        self.path_data = path_data

    def summarize(self):
        summary = {
            "Total Keywords": len(self.keyword_data),
            "Total Learning Scenarios": len(self.scenario_data),
            "Total Learning Paths": len(self.path_data),
            "Total Learning Activities": 0,
            "Total OERs used in Learning Paths": 0
        }

        for path in self.path_data:
            lessons = path.get("Path", {}).get("LessonPlan", [])
            summary["Total Learning Activities"] += len(lessons)
            for lesson in lessons:
                content = lesson.get("Content", {})
                oers = content.get("OERs", [])
                summary["Total OERs in Learning Paths"] += len(oers)

        return summary

    def print_summary(self):
        summary = self.summarize()
        print("📊 Global Summary Report:")
        for key, value in summary.items():
            print(f"- {key}: {value}")
