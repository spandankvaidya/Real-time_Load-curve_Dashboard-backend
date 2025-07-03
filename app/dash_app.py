from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from app.model import predicted_values, actual_values, time_ticks

# Define the Dash app with proper prefix
dash_app = Dash(
    __name__,
    routes_pathname_prefix="/dashboard/",  # <- required for FastAPI mount
    requests_pathname_prefix="/dashboard/"
)

# Define layout
dash_app.layout = html.Div([
    html.H3("🔴 Real-time Load Curve", style={"textAlign": "center"}),
    dcc.Graph(id='live-graph', style={"height": "80vh"}),
    dcc.Interval(id='interval', interval=1000, n_intervals=0)
])

# Update logic
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

# Export server for mounting
server = dash_app.server
