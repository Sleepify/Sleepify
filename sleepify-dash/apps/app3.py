import sys
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
from os.path import dirname, join as path_join
from app import app
sys.path.insert(0, path_join(dirname(__file__), "..", ".."))
import base64

from train_score import load_data


logo_filename = './assets/images/top.png' # replace with your own image
encoded_logo = base64.b64encode(open(logo_filename, 'rb').read())


categories = ["training", "movies", "reading", "programming", "girlfriend time",
                "work", "relax", "friends", "sleeping",
                "coffee", "good meal", "hangout with friends"]
days = 1
data_path = path_join(dirname(__file__), "..", "..", "Data", "data.csv")

layout = html.Div(
    [
        html.Img(src='data:image/png;base64,{}'.format(encoded_logo.decode()), width="400px"),
        html.P("Predictions"),
        html.Div(
            [
                dcc.Dropdown(
                    id="categories2",
                    options=[
                        {'label': "{}".format(category), 'value': category}
                        for category in categories ], value="coffee"
                ),
                dcc.Graph(id="category2"),
            ]
        ),
    ], id='main', style={'position': 'absolute', 'left': '35%', 'width': '450px'}
)


@app.callback(
        Output("category2", "figure"),
        [Input("categories2", "value")]
        )
def update_graph(value):
    df = pd.read_csv(data_path)

    ytrace0, ytrace1, x_data = [], [], []

    if value == "coffee":
        ytrace0 = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]
        ytrace1 = [0, 0, 0, 0, 0, 0, 0, 0, -0.2, -0.4, -0.5, -0.5, -0.6, -0.7, -0.7, -0.8, -0.9]
        x_data = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22 ]
    elif value == "work":
        ytrace0 = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.6, 0.4]
        ytrace1 = [0, 0, 0, 0, 0, 0, 0, 0, -0.2, -0.2, -0.2, -0.4, -0.4, -0.5, -0.5, -0.6, -0.6]
        x_data = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22 ]
    elif value == "sleeping":
        ytrace0 = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9]
        x_data = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22 ]
    elif value == "training":
        ytrace0 = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.6, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2, 0.2]
        ytrace1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.2, -0.2, -0.7]
        x_data = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22 ]
    else:
        ytrace0 = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.6, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2, 0.2]
        ytrace1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.2, -0.2, -0.7]
        x_data = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22 ]

    trace0 = go.Bar(
            x=x_data,
            y=ytrace0,
            marker=dict(
              color='rgb(49,130,189, 0.1)',
            ),
            opacity=0.6
        )

    trace1 = go.Bar(
        x=x_data,
        y=ytrace1,
        marker=dict(
            color='rgba(219, 64, 82, 0.8)'
        ),
        opacity=0.6
        )

    layout = go.Layout(
            title="Activity Impact on sleep quality",
            showlegend=False
    )

    data = [trace0, trace1]

    return go.Figure(data=data, layout=layout)
