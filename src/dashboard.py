from dash import Dash, html, dcc, Output, Input, ctx
import dash.dash_table as dt
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

# -----------------------
# Styles
# -----------------------
BG = "#0b0526"
CARD = "#1a1630"
ACCENT = "#8a5af8"
ACCENT2 = "#6bd6ff"
TEXT = "#e6e6f2"
SUBTEXT = "#bdb8d9"
GOOD = "#2ee6a6"
WARN = "#ffb86b"
BAD = "#ff6b6b"

APP_STYLE = {"backgroundColor": BG, "color": TEXT, "minHeight": "100vh", "padding": "12px 18px"}
CARD_STYLE = {"backgroundColor": CARD, "borderRadius": "10px", "padding": "14px", "boxShadow": "0 6px 18px rgba(0,0,0,0.6)", "color": TEXT}
HEADER_STYLE = {"fontSize": "22px", "fontWeight": 700, "color": TEXT, "marginBottom": "6px"}
KPI_TITLE = {"fontSize": "12px", "color": SUBTEXT}
KPI_VALUE = {"fontSize": "20px", "fontWeight": 700, "color": TEXT}

# -----------------------
# Mock data helpers
# -----------------------
def load_devices_as_df():
    now = datetime.utcnow()
    rows = [
        {"id": 1, "name": "Sensor1", "ip": "192.168.1.2", "firmware": "1.0.0", "strong_password": "No", "up_to_date": "No", "status": "Vulnerable", "last_seen": (now - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M")},
        {"id": 2, "name": "Camera1", "ip": "192.168.1.3", "firmware": "1.2.0", "strong_password": "Yes", "up_to_date": "Yes", "status": "Secure", "last_seen": (now - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")},
        {"id": 3, "name": "Thermostat-A", "ip": "10.0.0.7", "firmware": "1.1.2", "strong_password": "Yes", "up_to_date": "No", "status": "Vulnerable", "last_seen": (now - timedelta(minutes=20)).strftime("%Y-%m-%d %H:%M")},
        {"id": 4, "name": "Camera2", "ip": "192.168.1.4", "firmware": "1.0.3", "strong_password": "No", "up_to_date": "Yes", "status": "Vulnerable", "last_seen": (now - timedelta(minutes=90)).strftime("%Y-%m-%d %H:%M")},
    ]
    return pd.DataFrame(rows)

def compute_kpis(df):
    total = len(df)
    vulnerable = (df["status"] == "Vulnerable").sum()
    outdated = (df["up_to_date"] == "No").sum()
    alerts_today = vulnerable + (pd.to_datetime(datetime.utcnow()) - pd.to_datetime(df["last_seen"])).dt.total_seconds().gt(3600).sum()
    return {"total": total, "vulnerable": vulnerable, "outdated": outdated, "alerts_today": alerts_today}

# -----------------------
# Build Dash app
# -----------------------
app = Dash(__name__)
server = app.server

app.layout = html.Div(style=APP_STYLE, children=[
    html.Div(style={"display": "flex", "gap": "18px"}, children=[
        # Sidebar
        html.Div(style={"width": "260px"}, children=[
            html.Div(style={**CARD_STYLE, "padding": "18px"}, children=[
                html.H2("IoT-DSMS", style={"margin": "0 0 8px 0", "color": ACCENT}),
                html.Div("Security Operations Center (SOC) — Midnight Purple", style={"fontSize": "12px", "color": SUBTEXT}),
            ]),
        ]),
        # Main area
        html.Div(style={"flex": "1"}, children=[
            # KPIs
            html.Div(style={"display": "flex", "gap": "12px", "marginBottom": "12px"}, children=[
                html.Div(style={**CARD_STYLE, "flex": "1"}, children=[html.Div("Total devices", style=KPI_TITLE), html.Div(id="k-total", style=KPI_VALUE)]),
                html.Div(style={**CARD_STYLE, "flex": "1"}, children=[html.Div("Vulnerable", style=KPI_TITLE), html.Div(id="k-vulnerable", style=KPI_VALUE)]),
                html.Div(style={**CARD_STYLE, "flex": "1"}, children=[html.Div("Outdated", style=KPI_TITLE), html.Div(id="k-outdated", style=KPI_VALUE)]),
                html.Div(style={**CARD_STYLE, "flex": "1"}, children=[html.Div("Alerts today", style=KPI_TITLE), html.Div(id="k-alerts", style=KPI_VALUE)]),
            ]),
            # Graphs & table
            html.Div(style={"display": "flex", "gap": "12px"}, children=[
                html.Div(style={**CARD_STYLE, "flex": "1"}, children=[
                    html.Div("Firmware distribution", style=HEADER_STYLE),
                    dcc.Graph(id="firmware-chart", config={"displayModeBar": False}),
                    html.Div("Security Score timeline", style={"marginTop": "8px", "color": SUBTEXT}),
                    dcc.Graph(id="score-chart", config={"displayModeBar": False}),
                ]),
                html.Div(style={**CARD_STYLE, "width": "520px"}, children=[
                    html.Div(style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"}, children=[
                        html.Div("Devices", style=HEADER_STYLE),
                        html.Div([
                            dcc.Input(id="filter-name", placeholder="Filter by name / IP", style={"background": CARD, "color": TEXT, "border": "1px solid #2b2540", "padding": "6px", "borderRadius": "6px"}),
                            html.Button("Refresh", id="refresh-btn", n_clicks=0, style={"marginLeft": "8px", "backgroundColor": ACCENT, "color": "#fff", "border": "none", "padding": "6px 10px", "borderRadius": "6px"}),
                        ])
                    ]),
                    dt.DataTable(
                        id="devices-table",
                        columns=[
                            {"name": "id", "id": "id"},
                            {"name": "Name", "id": "name"},
                            {"name": "IP", "id": "ip"},
                            {"name": "Firmware", "id": "firmware"},
                            {"name": "PW OK", "id": "strong_password"},
                            {"name": "Up-to-date", "id": "up_to_date"},
                            {"name": "Status", "id": "status"},
                            {"name": "Last seen", "id": "last_seen"}
                        ],
                        data=[],
                        page_size=5,  # default, will be overridden dynamically
                        style_header={"backgroundColor": "transparent", "color": SUBTEXT, "fontWeight": "600"},
                        style_cell={"backgroundColor": "transparent", "color": TEXT, "border": "none", "textAlign": "left"},
                        style_data_conditional=[
                            {"if": {"column_id": "status", "filter_query": "{status} = 'Secure'"}, "color": GOOD, "fontWeight": "700"},
                            {"if": {"column_id": "status", "filter_query": "{status} = 'Vulnerable'"}, "color": BAD, "fontWeight": "700"},
                            {"if": {"column_id": "up_to_date", "filter_query": "{up_to_date} = 'Yes'"}, "color": GOOD},
                            {"if": {"column_id": "up_to_date", "filter_query": "{up_to_date} = 'No'"}, "color": WARN},
                        ]
                    )
                ])
            ])
        ])
    ])
])

# -----------------------
# Callbacks
# -----------------------
@app.callback(
    Output("devices-table", "data"),
    Output("k-total", "children"),
    Output("k-vulnerable", "children"),
    Output("k-outdated", "children"),
    Output("k-alerts", "children"),
    Output("firmware-chart", "figure"),
    Output("score-chart", "figure"),
    Output("devices-table", "page_size"),  # dynamic page_size
    Input("refresh-btn", "n_clicks"),
    Input("filter-name", "value"),
)
def refresh_dashboard(n_clicks, filter_value):
    df = load_devices_as_df()
    # Apply filter
    if filter_value:
        f = filter_value.lower()
        df = df[df["name"].str.lower().str.contains(f) | df["ip"].str.lower().str.contains(f)]
    # KPIs
    kpis = compute_kpis(df)
    # Firmware chart
    if not df.empty:
        df["firmware"] = df["firmware"].astype(str)
        df["ip"] = df["ip"].astype(str)
        fw_fig = px.pie(df, names="firmware", hole=0.5, title="Firmware distribution")
        fw_fig.update_layout(height=250 + 30*len(df), paper_bgcolor=BG, plot_bgcolor=BG, font_color=TEXT)

    else:
        fw_fig = px.pie(values=[1], names=["No data"], hole=0.5, title="Firmware distribution")
        fw_fig.update_layout(height=250, paper_bgcolor=BG, plot_bgcolor=BG, font_color=TEXT)
    # Security score timeline (mock)
    now = datetime.utcnow()
    tl_df = pd.DataFrame({"date": [now - timedelta(days=i) for i in range(6,-1,-1)],
                          "score": [100,90,95,85,80,90,88]})
    score_fig = px.line(tl_df, x="date", y="score", markers=True, title="Security Score timeline")
    score_fig.update_yaxes(range=[0,100])
    score_fig.update_layout(height=250, margin=dict(t=30,b=10,l=10,r=10),
                            paper_bgcolor=BG, plot_bgcolor=BG, font_color=TEXT)
    # Return
    page_size = max(len(df), 3)  # min 3, max number of devices
    return df.to_dict("records"), str(kpis["total"]), str(kpis["vulnerable"]), str(kpis["outdated"]), str(kpis["alerts_today"]), fw_fig, score_fig, page_size

# -----------------------
# Run server
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)
