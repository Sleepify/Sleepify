import sys
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
from os.path import dirname, join as path_join
from app import app
sys.path.insert(0, path_join(dirname(__file__), "..", ".."))

from train_score import load_data

categories = ["training", "movies", "reading", "programming", "girlfriend time",
                "work", "relax", "friends", "sleeping",
                "coffee", "good meal", "hangout with friends"]
days = 1
data_path = path_join(dirname(__file__), "..", "..", "Data", "data.csv")

layout = html.Div(
    [
        html.H2("Sleepyfit"),
        html.Div(
            [
                dcc.Dropdown(
                    id="categories",
                    options=[
                        {'label': "{}".format(category), 'value': category}
                        for category in categories ], value="coffee"
                ),
                dcc.Graph(id="category"),
            ]
        ),
    ]
)


@app.callback(
        Output("category", "figure"),
        [Input("categories", "value")]
        )
def update_graph(value):
    df = pd.read_csv(data_path)

    ytrace0, ytrace1, x_data = [], [], []
    for hour in df[["activity", "hour", "score"]].itertuples():
        if hour.activity == value:
            if hour.score >= 0:
                ytrace0.append(hour.score)
                ytrace1.append(0)
            else:
                ytrace0.append(0)
                ytrace1.append(hour.score)
        else:
            ytrace0.append(0)
            ytrace1.append(0)

        x_data.append(hour.hour)

    trace0 = go.Bar(
            x=x_data,
            y=ytrace0,
            marker=dict(
              color='rgb(49,130,189)',
            ),
        )

    trace1 = go.Bar(
        x=x_data,
        y=ytrace1,
        marker=dict(
            color='rgba(219, 64, 82, 1.0)'
        ),
        )

    layout = go.Layout(
            title="Activity Impact on sleep quality",
            showlegend=False
    )

    data = [trace0, trace1]

    return go.Figure(data=data, layout=layout)
