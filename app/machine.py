import datetime

import joblib
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier


class Machine:

    def __init__(self, df: DataFrame):
        self.name = "Random Forest Classifier"
        target = df["Rarity"]
        features = df.drop(columns=["Rarity"])
        self.model = RandomForestClassifier()
        self.model.fit(features, target)
        self.timestamp = datetime.datetime.now()

    def __call__(self, feature_basis: DataFrame):
        prediction, *_ = self.model.predict(feature_basis)
        probability, *_ = self.model.predict_proba(feature_basis)
        return prediction, max(probability)

    def save(self, filepath):
        joblib.dump(self, filepath)

    @staticmethod
    def open(filepath):
        return joblib.load(filepath)

    def info(self):
        output = (
            f"Base Model: {self.name}",
            f"Timestamp: {self.timestamp.strftime('%Y-%m-%d %-I:%M:%S %p')}",
        )
        return "<br>".join(output)
