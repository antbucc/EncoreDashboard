
from bson import ObjectId
from datetime import datetime
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class KeywordAnalyzer:
    def __init__(self, data):
        self.data = data
        self.filtered_keywords = []

    def filter_keywords(self):
        for doc in self.data:
            if (
                isinstance(doc.get("_id"), ObjectId) and
                isinstance(doc.get("value"), str) and
                isinstance(doc.get("__v"), int) and
                isinstance(doc.get("dateSaved"), datetime) and
                isinstance(doc.get("lastUpdated"), datetime) and
                isinstance(doc.get("usageCount"), int)
            ):
                self.filtered_keywords.append(doc)

    def get_counts(self):
        counts = {}
        for doc in self.filtered_keywords:
            keyword = doc["value"]
            count = doc.get("usageCount", 0)
            counts[keyword] = counts.get(keyword, 0) + count
        return counts

    def create_figure(self):
        self.filter_keywords()
        keyword_counts = self.get_counts()
        if not keyword_counts:
            return None

        sorted_items = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
        keywords, counts = zip(*sorted_items)

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        bars = axes[0].barh(keywords, counts, color="skyblue")
        axes[0].set_title("Keyword Occurrences")
        axes[0].invert_yaxis()

        for bar, count in zip(bars, counts):
            axes[0].text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, str(count), va='center')

        wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(keyword_counts)
        axes[1].imshow(wordcloud, interpolation="bilinear")
        axes[1].axis("off")
        axes[1].set_title("Keyword Word Cloud")

        fig.tight_layout()
        return fig
