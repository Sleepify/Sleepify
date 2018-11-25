import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import base64
from app import app


logo_filename = './assets/images/top.png' # replace with your own image
encoded_logo = base64.b64encode(open(logo_filename, 'rb').read())

start_filename = './assets/images/start_screen.png' # replace with your own image
encoded_start = base64.b64encode(open(start_filename, 'rb').read())

sleep_filename = './assets/images/sleep_info.png' # replace with your own image
encoded_sleep = base64.b64encode(open(sleep_filename, 'rb').read())

bad_filename = './assets/images/bad_day.png' # replace with your own image
encoded_bad = base64.b64encode(open(bad_filename, 'rb').read())

calendar_filename = './assets/images/calendar.png' # replace with your own image
encoded_calendar = base64.b64encode(open(calendar_filename, 'rb').read())

layout = html.Div([
    html.Div([
        html.Img(src='data:image/png;base64,{}'.format(encoded_logo.decode()), width="400px"),
        html.P(),
        dcc.Link(html.Img(src='data:image/png;base64,{}'.format(encoded_start.decode()), width="400px"), href='#', id="1"),
        html.P(),
        dcc.Link(html.Img(src='data:image/png;base64,{}'.format(encoded_sleep.decode()), width="400px"), id="2", href='#', style={'visibility': 'hidden'}),

        html.P(),
        dcc.Link(html.Img(src='data:image/png;base64,{}'.format(encoded_calendar.decode()), width="400px"), id="3", href='#', style={'visibility': 'hidden'}),

        html.P(),
        dcc.Link(html.Img(src='data:image/png;base64,{}'.format(encoded_bad.decode()), width="400px"), id="4", href='#', style={'visibility': 'hidden'}),

    ], id='main', style={'position': 'absolute', 'left': '35%', 'width': '450px'})
])