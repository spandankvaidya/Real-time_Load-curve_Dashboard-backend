from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from app import globals

def create_dash_app(server):
    app = Dash(__name__, server=server, routes_pathname_prefix='/dashboard/')

    app.layout = html.Div([
        html.H2("🔴 Real-time Power Consumption Prediction"),
        html.H4(id='selected-date-display'),
        dcc.Graph(id='live-graph'),
        dcc.Interval(id='interval', interval=1000, n_intervals=0)
    ])

    @app.callback(Output('live-graph', 'figure'), Input('interval', 'n_intervals'))
    def update_graph(n):
        if not globals.predicted_values:
            return {
                'data': [],
                'layout': go.Layout(title="Waiting for data...", height=600)
            }

        return {
            'data': [
                go.Scatter(x=globals.timestamps[:n], y=globals.predicted_values[:n], name='Predicted', line=dict(color='blue')),
                go.Scatter(x=globals.timestamps[:n], y=globals.actual_values[:n], name='Actual', line=dict(color='red'))
            ],
            'layout': go.Layout(
                xaxis={'title': 'Time'},
                yaxis={'title': 'Power Consumption'},
                height=600
            )
        }

    @app.callback(Output('selected-date-display', 'children'), Input('interval', 'n_intervals'))
    def update_date_display(_):
        return f"📅 Forecast for: {globals.selected_date}"

    return app
