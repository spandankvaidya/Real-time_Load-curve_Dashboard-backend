from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import os

# Import global variables if needed
from app.globals import predicted_values, actual_values, time_ticks, selected_date

def create_dash_app():
    dash_app = Dash(
        __name__,
        routes_pathname_prefix='/dashboard/',  # Dash will be served at /dashboard
    )

    dash_app.layout = html.Div([
        html.H3("🔴 Real-time Load Curve", style={"textAlign": "center"}),
        html.H4(id='selected-date-display'),
        dcc.Graph(id='live-graph', style={"height": "80vh"}),
        dcc.Interval(id='interval', interval=1000, n_intervals=0)
    ])

    @dash_app.callback(Output('live-graph', 'figure'), Input('interval', 'n_intervals'))
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

    @dash_app.callback(Output('selected-date-display', 'children'), Input('interval', 'n_intervals'))
    def update_date_display(_):
        return f"📅 Forecast for: {selected_date}" if selected_date else ""

    return dash_app
