
import matplotlib.pyplot as plt
import re

class LearningScenarioAnalyzer:
    def __init__(self, data):
        self.data = data
        self.bloom_levels = {}
        self.verbs = {}
        self.educator_experience = {}
        self.education_context = {}
        self.dimension = {}
        self.learner_experience = {}

        self.allowed_learner_experience = {"Beginner", "Intermediate", "Advanced"}
        self.allowed_educator_experience = {"Junior", "Intermediate", "Senior"}
        self.allowed_education_context = {"School", "VET", "University"}

    def normalize_text(self, text):
        if not text or not isinstance(text, str):
            return None
        text = text.strip().capitalize()
        text = re.sub(r'[^a-zA-Z ]+', '', text)
        return text if text else None

    def normalize_education_context(self, context):
        context = self.normalize_text(context)
        if context in self.allowed_education_context:
            return context
        return "University" if context else None

    def normalize_learner_experience(self, experience):
        exp = self.normalize_text(experience)
        if exp and exp.lower() == "line":
            return "Beginner"
        return exp if exp in self.allowed_learner_experience else None

    def normalize_educator_experience(self, experience):
        exp = self.normalize_text(experience)
        return exp if exp in self.allowed_educator_experience else None

    def extract_data(self):
        for doc in self.data:
            bloom = self.normalize_text(doc.get("Objective", {}).get("BloomLevel", {}).get("name"))
            if bloom:
                self.bloom_levels[bloom] = self.bloom_levels.get(bloom, 0) + 1

            for verb in doc.get("Objective", {}).get("BloomLevel", {}).get("verbs", []):
                norm_verb = self.normalize_text(verb)
                if norm_verb:
                    self.verbs[norm_verb] = self.verbs.get(norm_verb, 0) + 1

            context = doc.get("Context", {})

            educator_exp = self.normalize_educator_experience(context.get("EducatorExperience"))
            if educator_exp:
                self.educator_experience[educator_exp] = self.educator_experience.get(educator_exp, 0) + 1

            normalized_context = self.normalize_education_context(context.get("EducationContext"))
            if normalized_context:
                self.education_context[normalized_context] = self.education_context.get(normalized_context, 0) + 1

            dim = self.normalize_text(context.get("Dimension"))
            if dim:
                self.dimension[dim] = self.dimension.get(dim, 0) + 1

            learner_exp = self.normalize_learner_experience(context.get("LearnerExperience"))
            if learner_exp:
                self.learner_experience[learner_exp] = self.learner_experience.get(learner_exp, 0) + 1

    def create_figure(self):
        self.extract_data()
        fig, axes = plt.subplots(3, 2, figsize=(16, 14))

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

        plot(axes[0, 0], self.bloom_levels, "Bloom's Levels")
        plot(axes[0, 1], self.verbs, "Bloom Verbs")
        plot(axes[1, 0], self.educator_experience, "Educator Experience")
        plot(axes[1, 1], self.education_context, "Education Context")
        plot(axes[2, 0], self.dimension, "Dimension")
        plot(axes[2, 1], self.learner_experience, "Learner Experience")

        fig.tight_layout()
        return fig
