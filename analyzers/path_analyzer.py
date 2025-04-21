
import matplotlib.pyplot as plt
from wordcloud import WordCloud

class LearningPathAnalyzer:
    def __init__(self, data, max_activity_types=10):
        self.data = data
        self.max_activity_types = max_activity_types
        self.type_of_activity = {}
        self.type_of_assignment = {}
        self.topics = {}
        self.activity_time = {}
        self.assignment_category_count = {"Learning": 0, "Assessment": 0}

    def extract_data(self):
        for doc in self.data:
            lessons = doc.get("Path", {}).get("LessonPlan", [])
            for lesson in lessons:
                activity = lesson.get("TypeOfActivity", "").strip()
                if activity:
                    self.type_of_activity[activity] = self.type_of_activity.get(activity, 0) + 1
                    self.activity_time[activity] = self.activity_time.get(activity, 0) + lesson.get("Time", 0)

                assignment = lesson.get("TypeOfAssignment", "").strip()
                if assignment:
                    self.type_of_assignment[assignment] = self.type_of_assignment.get(assignment, 0) + 1
                    if assignment in self.assignment_category_count:
                        self.assignment_category_count[assignment] += 1

                topic = lesson.get("Topic", "").strip()
                if topic:
                    self.topics[topic] = self.topics.get(topic, 0) + 1

    def get_top_items(self, data_dict):
        return dict(sorted(data_dict.items(), key=lambda x: x[1], reverse=True)[:self.max_activity_types])

    def create_figure(self):
        self.extract_data()
        fig, axes = plt.subplots(2, 2, figsize=(18, 12))

        def plot_pie(ax, data, title):
            if not data:
                ax.set_title(f"{title} (no data)")
                ax.axis("off")
                return
            labels, values = zip(*data.items())
            ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
            ax.set_title(title)

        def plot_bar(ax, data, title, xlabel):
            if not data:
                ax.set_title(f"{title} (no data)")
                ax.axis("off")
                return
            labels, values = zip(*data.items())
            ax.barh(labels, values)
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.invert_yaxis()

        # Top N activity types (all combined, regardless of assignment type)
        top_activities = self.get_top_items(self.type_of_activity)
        top_activity_times = {k: self.activity_time[k] for k in top_activities}

        # Chart 1: All unique activity types
        plot_bar(axes[0, 0], top_activities, "Most Common Activity Types", "Count")

        # Chart 2: Aggregated time per activity type
        plot_bar(axes[0, 1], top_activity_times, "Total Time by Activity Type", "Minutes")

        # Chart 3: Learning vs Assessment overview
        plot_pie(axes[1, 0], self.assignment_category_count, "Learning vs Assessment Distribution")

        # Chart 4: Word cloud of topics
        if self.topics:
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(self.topics)
            axes[1, 1].imshow(wordcloud, interpolation="bilinear")
            axes[1, 1].axis("off")
            axes[1, 1].set_title("Topic Word Cloud")
        else:
            axes[1, 1].set_title("Topic Word Cloud (no data)")
            axes[1, 1].axis("off")

        fig.tight_layout()
        return fig
