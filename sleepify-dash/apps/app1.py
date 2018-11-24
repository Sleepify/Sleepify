import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd

from app import app

categories = ["Coffee", "Entertainment", "Weather", "Mood", "Activity"]
days = 7

layout = html.Div(
    [
        dcc.Link('Go to App 2', href='/apps/app2'),
        html.Div(
            [
                html.H3("Coffee"),
                dcc.Dropdown(
                    id="categories",
                    options=[
                        {'label': f"{category}", 'value': category}
                        for category in categories
                    ]
                ),
                *(dcc.Graph(id=f"coffee-{i}") for i in range(days)),
            ]
        ),
    ]
)


@app.callback(
        Output("coffee-0", "figure"),
        [Input("categories", "value")]
        )
def update_coffee_graph(value):
    # df = pd.read_csv("...")
    # y_vals = pd.Series(range(100))

    trace = go.Scatterpolar(
        r=list(range(24)),
        theta=list(range(1, 25)),
    )

    layout = go.Layout(
        autosize=True,
        width=275,
        margin=go.Margin(
            t=10,
            b=10,
            r=30,
            l=40
        ),
        polar=dict(
            radialaxis=dict(
                visible=False
                ),
            angularaxis=dict(
                showline=False,
                tickcolor='white',
            )
        ),
        showlegend=False,
    )
    return go.Figure(data=[trace], layout=layout)
