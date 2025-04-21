
import matplotlib.pyplot as plt
from wordcloud import WordCloud

class LearningPathAnalyzer:
    def __init__(self, data):
        self.data = data
        self.type_of_activity = {}
        self.type_of_assignment = {}
        self.topics = {}
        self.activity_time = {}

    def extract_data(self):
        for doc in self.data:
            lessons = doc.get("Path", {}).get("LessonPlan", [])
            for lesson in lessons:
                toa = lesson.get("TypeOfActivity")
                if toa:
                    self.type_of_activity[toa] = self.type_of_activity.get(toa, 0) + 1
                    self.activity_time[toa] = self.activity_time.get(toa, 0) + lesson.get("Time", 0)

                assign = lesson.get("TypeOfAssignment")
                if assign:
                    self.type_of_assignment[assign] = self.type_of_assignment.get(assign, 0) + 1

                topic = lesson.get("Topic")
                if topic:
                    self.topics[topic] = self.topics.get(topic, 0) + 1

    def create_figure(self):
        self.extract_data()
        fig, axes = plt.subplots(2, 2, figsize=(18, 12))

        def plot_pie(ax, data, title):
            data = {k: v for k, v in data.items() if k}
            if not data:
                ax.set_title(f"{title} (no data)")
                ax.axis("off")
                return
            labels, values = zip(*sorted(data.items(), key=lambda x: x[1], reverse=True))
            ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
            ax.set_title(title)

        def plot_bar(ax, data, title, xlabel):
            data = {k: v for k, v in data.items() if k}
            if not data:
                ax.set_title(f"{title} (no data)")
                ax.axis("off")
                return
            labels, values = zip(*sorted(data.items(), key=lambda x: x[1], reverse=True))
            ax.barh(labels, values)
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.invert_yaxis()

        plot_pie(axes[0, 0], self.type_of_activity, "Activity Types Distribution")
        plot_bar(axes[0, 1], self.activity_time, "Total Time by Activity Type", "Minutes")
        plot_bar(axes[1, 0], self.type_of_assignment, "Assignment Types Distribution", "Count")

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
