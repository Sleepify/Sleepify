import sys
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
from os.path import dirname, join as path_join
from app import app
from os.path import join as path_join, dirname
sys.path.insert(0, path_join(dirname(__file__), "..", ".."))

from train_score import load_data



# TODO: when a drop down menu is chosen, update the graph with the new data
#
categories = ["training", "movies", "reading", "programming","girlfriend time" ,
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

    x_data, ytrace0, ytrace1 = [], [], []

    sorted_df = df[["activity", "time", "score"]].sort_values(by="time")
    for row in sorted_df.itertuples():
        activity, time, score = row[1], row[2], row[3]
        if activity == value:
            if score >=0:
                x_data.append(time)
                ytrace0.append(score)
            else:
                ytrace1.append(score)
        else:
            x_data.append(time)
            ytrace0.append(0)
            ytrace1.append(0)

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
    print(x_data)

    layout = go.Layout(
            title="Activity Impact on sleep quality",
            showlegend=False
    )

    data = [trace0, trace1]

    return go.Figure(data=data, layout=layout)
