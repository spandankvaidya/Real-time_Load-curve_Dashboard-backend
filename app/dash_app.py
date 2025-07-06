from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from app.model import predicted_values, actual_values, time_ticks

from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
import os

# Create a Dash app
dash_app = Dash(__name__)
app = dash_app  # alias for clarity
server = dash_app.server  # needed if you run standalone

# Dash layout
dash_app.layout = html.Div([
    html.H3("🔴 Real-time Load Curve", style={"textAlign": "center"}),
    dcc.Graph(id='live-graph', style={"height": "80vh"}),
    dcc.Interval(id='interval', interval=1000, n_intervals=0)
])

# Callback to update graph
@dash_app.callback(
    Output('live-graph', 'figure'),
    Input('interval', 'n_intervals')
)
def update_graph(n):
    return {
        'data': [
            go.Scatter(x=time_ticks[:n], y=predicted_values[:n], name='Predicted', line=dict(color='blue')),
            go.Scatter(x=time_ticks[:n], y=actual_values[:n], name='Actual', line=dict(color='red'))
        ],
        'layout': go.Layout(
            xaxis={'title': 'Time'},
            yaxis={'title': 'Power Consumption'},
            height=600
        )
    }
