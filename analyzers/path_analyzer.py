
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
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))

        def plot(ax, data, title):
            data = {k: v for k, v in data.items() if k}
            if not data:
                ax.set_title(f"{title} (no data)")
                ax.axis("off")
                return
            items = sorted(data.items(), key=lambda x: x[1], reverse=True)
            labels, values = zip(*items)
            ax.barh(labels, values)
            ax.set_title(title)
            ax.invert_yaxis()

        plot(axes[0, 0], self.type_of_activity, "Type of Activity")
        plot(axes[0, 1], self.type_of_assignment, "Type of Assignment")
        plot(axes[1, 0], self.activity_time, "Total Time by Activity Type")

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
