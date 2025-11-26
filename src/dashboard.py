import dash
from dash import html, dcc
from devices import get_all_devices
from security import analyze_device

app = dash.Dash(__name__)

def get_device_table():
    devices = get_all_devices()
    analyzed = [analyze_device(d) for d in devices]
    table = html.Table([
        html.Tr([html.Th(col) for col in analyzed[0].keys()]),
        *[html.Tr([html.Td(d[col]) for col in d.keys()]) for d in analyzed]
    ])
    return table

app.layout = html.Div([
    html.H1("IoT Device Security Dashboard"),
    get_device_table(),
    html.Button("Refresh", id="refresh")
])

if __name__ == "__main__":
    app.run_server(debug=True)
