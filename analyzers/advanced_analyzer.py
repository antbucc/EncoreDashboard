
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
import numpy as np

class AdvancedLearningAnalytics:
    def __init__(self, paths, scenarios):
        self.paths = paths
        self.scenarios = scenarios

        self.lesson_durations = []
        self.bloom_levels = defaultdict(int)
        self.assignment_time = {"Learning": 0, "Assessment": 0}
        self.assignment_count = {"Learning": 0, "Assessment": 0}
        self.oer_usage = Counter()
        self.topic_distribution = Counter()
        self.question_types = Counter()
        self.educator_experience = defaultdict(lambda: defaultdict(int))
        self.path_branching = []

        self.valid_bloom_levels = {"Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"}
        self.valid_experience_levels = {"Junior", "Intermediate", "Senior"}

    def normalize_text(self, text):
        if not text or not isinstance(text, str):
            return None
        return text.strip().capitalize()

    def extract(self):
        for doc in self.paths:
            lessons = doc.get("Path", {}).get("LessonPlan", [])
            self.path_branching.append(sum(1 for l in lessons if l.get("Conditions", {}).get("Pass") or l.get("Conditions", {}).get("Fail")))

            for lesson in lessons:
                time = lesson.get("Time", 0)
                self.lesson_durations.append(time)

                topic = lesson.get("Topic")
                if topic:
                    self.topic_distribution[topic.strip()] += 1

                assign = lesson.get("TypeOfAssignment")
                if assign in self.assignment_time:
                    self.assignment_time[assign] += time
                    self.assignment_count[assign] += 1

                oers = lesson.get("Content", {}).get("OERs", [])
                if oers:
                    self.oer_usage[lesson.get("Topic", "Unspecified")] += len(oers)

                activity = lesson.get("TypeOfActivity", "").strip().lower()
                if activity in ["multiple choice", "true or false", "short answer question", "fill in the blanks"]:
                    self.question_types[activity] += 1

        for scenario in self.scenarios:
            bloom = self.normalize_text(scenario.get("Objective", {}).get("BloomLevel", {}).get("name"))
            exp = self.normalize_text(scenario.get("Context", {}).get("EducatorExperience"))

            if bloom in self.valid_bloom_levels and exp in self.valid_experience_levels:
                self.bloom_levels[bloom] += 1
                self.educator_experience[exp][bloom] += 1

    def create_figure(self):
        self.extract()
        fig, axes = plt.subplots(3, 2, figsize=(18, 16))

        # 1. Completion Time Distribution
        axes[0, 0].hist(self.lesson_durations, bins=10, color="skyblue", edgecolor="black")
        axes[0, 0].set_title("Lesson Duration Distribution")
        axes[0, 0].set_xlabel("Minutes")
        axes[0, 0].set_ylabel("Number of Lessons")

        # 2. Bloom Levels
        labels, values = zip(*sorted(self.bloom_levels.items(), key=lambda x: x[1], reverse=True))
        axes[0, 1].bar(labels, values, color="lightgreen")
        axes[0, 1].set_title("Bloom's Taxonomy Level Coverage")

        # 3. Time vs Assignment Type
        axes[1, 0].bar(self.assignment_time.keys(), self.assignment_time.values(), color="orange")
        axes[1, 0].set_title("Total Time Spent on Assignments")
        axes[1, 0].set_ylabel("Minutes")

        # 4. OER Usage
        if self.oer_usage:
            labels, values = zip(*self.oer_usage.most_common(6))
            axes[1, 1].barh(labels, values, color="purple")
            axes[1, 1].invert_yaxis()
            axes[1, 1].set_title("Top Topics by OER Usage")
        else:
            axes[1, 1].set_title("Top Topics by OER Usage (no data)")
            axes[1, 1].axis("off")

        # 5. Question Types Variety
        if self.question_types:
            labels, values = zip(*self.question_types.items())
            axes[2, 0].pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
            axes[2, 0].set_title("Assessment Question Types Distribution")
        else:
            axes[2, 0].set_title("Assessment Question Types (no data)")
            axes[2, 0].axis("off")

        # 6. Educator Experience vs Bloom Level (Heatmap)
        exp_levels = sorted(self.valid_experience_levels)
        bloom_keys = sorted(self.valid_bloom_levels)
        data = np.array([[self.educator_experience[exp].get(bloom, 0) for bloom in bloom_keys] for exp in exp_levels])

        im = axes[2, 1].imshow(data, cmap="Blues", aspect="auto")
        axes[2, 1].set_xticks(range(len(bloom_keys)))
        axes[2, 1].set_yticks(range(len(exp_levels)))
        axes[2, 1].set_xticklabels(bloom_keys, rotation=45)
        axes[2, 1].set_yticklabels(exp_levels)
        axes[2, 1].set_title("Educator Experience vs Bloom Level")
        fig.colorbar(im, ax=axes[2, 1])

        fig.tight_layout()
        return fig
