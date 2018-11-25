import pandas as pd
import json
import os
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from future_encoders import ColumnTransformer
from future_encoders import OneHotEncoder
from sklearn.preprocessing import Imputer
from sklearn.ensemble import RandomForestRegressor

# SELECTOR


class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.attribute_names].values


def file_exists(file):
    return os.path.exists(file)


def load_data(file):
    if file_exists("Data/data.pkl"):
        return pd.read_pickle("Data/data.pkl")

    data = json.load(open(file))
    list_of_series = []
    for key, user in data.items():
        for day in user:
            for activity, entries in day.items():
                for i in range(len(entries["time"])):
                    entry = [activity, entries["score"][i],
                             entries["time"][i],
                             entries["mood"][i],
                             entries["weather"][i],
                             entries["temperature"][i]]
                    series = pd.Series(entry, index=['activity', 'score', 'time', 'mood', 'weather', 'temperature'])
                    list_of_series.append(series)
    df = pd.DataFrame(list_of_series)
    df.to_pickle("Data/data.pkl")
    return df


if __name__ == "__main__":
    # Load the dataset
    df = load_data("Data/data.json")

    # Select features and target
    features = df.drop("score", axis=1)
    y = df["score"].copy()

    numeric_values = features.drop(["mood", "weather", "activity"], axis=1)  # returns a copy of the dataframe
    num_attribs = list(numeric_values)

    cat_attribs = ["mood", "weather", "activity"]

    num_pipeline = Pipeline([
        ('selector', DataFrameSelector(num_attribs)),  # Own transformation
        ('imputer', Imputer(strategy="median")),
        ('std_scaler', StandardScaler()),
    ])

    full_pipeline = ColumnTransformer([
        ("num_pipline", num_pipeline, num_attribs),
        ("cat_pipline", OneHotEncoder(), cat_attribs),
    ])

    X = full_pipeline.fit_transform(features)

    forest_reg = RandomForestRegressor()
    forest_reg.fit(X, y)
