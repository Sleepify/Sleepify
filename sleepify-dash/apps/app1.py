import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd

from app import app

categories = ["Coffee", "Entertainment", "Weather", "Mood", "Activity"]
days = 1

layout = html.Div(
    [
        dcc.Link('Go to App 2', href='/apps/app2'),
        html.Div(
            [
                html.H3("Coffee"),
                dcc.Dropdown(
                    id="categories",
                    options=[
                        {'label': "{}".format(category), 'value': category}
                        for category in categories
                    ], value="Coffee"
                ),
                *(dcc.Graph(id="coffee-0".format(i)) for i in range(days)),
            ]
        ),
    ]
)


@app.callback(
        Output("coffee-0", "figure"),
        [Input("categories", "value")]
        )

def update_graph(value):
    # df = pd.read_csv("...")
    # y_vals = pd.Series(range(100))

    x_data = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00',
            '10:00', '11:00', '12:00', '13:00', '14.00', '15:00', '16:00', '17:00', '18:00',
            '19:00', '20:00', '21:00', '22:00', '23:00', '24:00']

    trace0 = go.Bar(
            x=x_data,
            y=[0.0, 0.50, 1.0, 0.9, 0.01, 0.02, 0.25, 0.9, 0.4, 0.6,
              0.25, 0.50, 1.0, 0.9, 0.01, 0.02, 0.25, 0.9, 0.4, 0.6,
              0.5, 0.67, 0.9, 0.4],
            name='coffee-0',

            marker=dict(
              color='rgb(49,130,189)',
            ),
        )
    trace1 = go.Bar(
        x= x_data,
        y=[-0.25, -0.50, -1.0, -1.0, -0.01, -0.02, -0.2, -0.9, -0.4, -0.6,
            -0.25, -0.50, -1.0, -0.9, -0.01, -0.02, -0.25, -0.9, -0.4, -0.6,
            -0.5, -0.67, -0.9, -0.4
            ],
        name='coffee-0',
        marker=dict(
            color='rgba(219, 64, 82, 1.0)'
        ),
        )

    layout = go.Layout(
            title="Coffee Impact on sleep quality",
            showlegend=False
    )

    data = [trace0, trace1]

    return go.Figure(data=data, layout=layout)
