import dash
import pandas as pd
from dash import html, dcc, dash_table, Input, Output, State
from data.db_connector import load_performance_data
from datetime import datetime, timedelta

dash.register_page(__name__, path="/employees", name="Employees")

df = load_performance_data()
full_df = df.copy()

layout = html.Div(className="employee-dashboard-container", children=[
    html.Div([
        html.H2("Employee Performance Dashboard", style={
            "fontSize": "28px",
            "fontWeight": "bold",
            "marginBottom": "10px",
            "marginTop": "10px",
            "textAlign": "left"
        })
    ]),
    dcc.Store(id="filtered-data-store"),
    html.Div(className="filters-row", style={
        "display": "flex",
        "flexWrap": "wrap",
        "gap": "15px",
        "alignItems": "start",
        "justifyContent": "flex-start",
        "overflowX": "auto",
        "overflow": "visible",
        "position": "relative",
        "paddingBottom": "10px"
    }, children=[

        html.Div(style={"minWidth": "160px"}, children=[
            html.Label("Period", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id="date-range-filter",
                options=[
                    {"label": "Last 30 days", "value": "30d"},
                    {"label": "Last 3 months", "value": "3m"},
                    {"label": "Last 6 months", "value": "6m"},
                    {"label": "Last 12 months", "value": "12m"},
                    {"label": "All time", "value": "all"},
                ],
                value="all"
            )
        ]),

        html.Div(style={"minWidth": "170px"}, children=[
            html.Label("Efficiency (%)", style={"fontWeight": "bold"}),
            dcc.RangeSlider(
                id="efficiency-slider",
                min=0, max=100, step=1,
                marks={0: "0%", 25: "25%", 50: "50%", 75: "75%", 100: "100%"},
                value=[0, 100]
            ),
            html.Div(id="efficiency-range-text", children="Range: 0–100%", style={"fontSize": "12px", "color": "#888"})
        ]),

        html.Div(style={"minWidth": "170px"}, children=[
            html.Label("Engagement Score", style={"fontWeight": "bold"}),
            dcc.RangeSlider(
                id="engagement-slider",
                min=0, max=100, step=1,
                marks={0: "0%", 25: "25%", 50: "50%", 75: "75%", 100: "100%"},
                value=[0, 100]
            ),
            html.Div(id="engagement-range-text", children="Range: 0–100%", style={"fontSize": "12px", "color": "#888"})
        ]),

        html.Div(style={"minWidth": "170px"}, children=[
            html.Label("Burnout Probability", style={"fontWeight": "bold"}),
            dcc.RangeSlider(
                id="burnout-slider",
                min=0, max=100, step=1,
                marks={0: "0%", 25: "25%", 50: "50%", 75: "75%", 100: "100%"},
                value=[0, 100]
            ),
            html.Div(id="burnout-range-text", children="Range: 0–100%", style={"fontSize": "12px", "color": "#888"})
        ]),

        html.Div(style={"minWidth": "170px"}, children=[
            html.Label("Idle Time (min)", style={"fontWeight": "bold"}),
            dcc.RangeSlider(
                id="idle-slider",
                min=0, max=100, step=1,
                marks={0: "0%", 25: "25%", 50: "50%", 75: "75%", 100: "100%"},
                value=[0, 100]
            ),
            html.Div(id="idle-range-text", children="Range: 0–90 min", style={"fontSize": "12px", "color": "#888"})
        ]),

        html.Div(style={"minWidth": "160px"}, children=[
            html.Label("Task Complexity", style={"fontWeight": "bold"}),
            html.Div(style={"display": "flex", "flexWrap": "wrap", "gap": "5px"}, children=[
                dcc.RadioItems(
                    id="complexity-filter",
                    options=[
                        {"label": "Easy", "value": 1},
                        {"label": "Medium", "value": 2},
                        {"label": "Hard", "value": 3},
                        {"label": "All", "value": "all"},
                    ],
                    value="all",
                    labelStyle={
                        "display": "inline-block",
                        "width": "48%",
                        "whiteSpace": "nowrap"
                    },
                    style={
                        "display": "flex",
                        "flexWrap": "wrap",
                        "gap": "2px"
                    }
                )
            ])
        ]),

        html.Div(style={
            "display": "flex",
            "flexDirection": "column",
            "gap": "8px",
            "maxWidth": "140px",
            "justifyContent": "flex-start",
            "alignItems": "stretch"
        }, children=[
            html.Button("Reset Filters", id="reset-filters-button", n_clicks=0, className="btn-reset"),
            html.Button("Apply Filters", id="apply-filters-button", n_clicks=0, className="btn-apply")
        ])
    ]),

    html.Div(style={"display": "flex", "gap": "20px"}, children=[
        html.Div(style={"flex": 1}, children=[
            html.H4([
                "Top 10 Efficient Employees ",
                html.Img(
                    src="/assets/info.svg",
                    title="Displays the top 10 employees with the highest efficiency score based on the current filter selection.",
                    style={"height": "18px", "marginLeft": "6px", "cursor": "help"}
                )
            ], style={"fontSize": "20px"}),
            dcc.Graph(id="efficiency-graph", style={"height": "300px"})
        ]),
        html.Div(style={"flex": 1}, children=[
            html.H4([
                "Efficiency Score Distribution ",
                html.Img(
                    src="/assets/info.svg",
                    title="Histogram showing the distribution of efficiency scores for the Sales department.",
                    style={"height": "18px", "marginLeft": "6px", "cursor": "help"}
                )
            ], style={"fontSize": "20px"}),
            dcc.Graph(id="pie-graph", style={"height": "300px"})
        ]),
        html.Div(style={"flex": 1}, children=[
            html.H4([
                "Average Engagement Over Time ",
                html.Img(
                    src="/assets/info.svg",
                    title="Shows how the average employee engagement score evolves weekly in Sales department.",
                    style={"height": "18px", "marginLeft": "6px", "cursor": "help"}
                )
            ], style={"fontSize": "20px"}),
            dcc.Graph(id="engagement-graph", style={"height": "300px"})
        ])
    ]),

    html.Br(),

    html.Div([
        html.H3("Employee Performance Table", style={"fontSize": "22px"}),
        dash_table.DataTable(
            id="performance-table",
            columns=[{"name": i, "id": i} for i in df.columns if i != "department"],
            data=df.to_dict("records"),
            page_size=6,
            fixed_rows={"headers": True},
            style_table={
                "overflowX": "auto",
                "overflowY": "auto",
                "maxHeight": "500px"
            },
            style_cell={
                "textAlign": "left",
                "minWidth": "100px",
                "whiteSpace": "normal"
            },
            style_header={
                "fontWeight": "bold",
                "backgroundColor": "#f0f2f5",
                "borderBottom": "2px solid #ccc"
            }
        )
    ])
])

def percent_to_real(percent, real_min, real_max):
    return real_min + (real_max - real_min) * (percent / 100.0)

@dash.callback(
    Output("date-range-filter", "value"),
    Output("efficiency-slider", "value"),
    Output("engagement-slider", "value"),
    Output("burnout-slider", "value"),
    Output("complexity-filter", "value"),
    Output("idle-slider", "value"),
    Output("filtered-data-store", "data"),
    Input("apply-filters-button", "n_clicks"),
    Input("reset-filters-button", "n_clicks"),
    State("date-range-filter", "value"),
    State("efficiency-slider", "value"),
    State("engagement-slider", "value"),
    State("burnout-slider", "value"),
    State("complexity-filter", "value"),
    State("idle-slider", "value"),
    prevent_initial_call=False
)
def unified_filter_handler(apply_clicks, reset_clicks,
                           period, efficiency_range, engagement_range,
                           burnout_range, complexity_value, idle_range):
    triggered_id = dash.callback_context.triggered_id

    df = full_df.copy()
    df = df[df["department"].str.lower() == "sales"]

    if triggered_id == "reset-filters-button":
        return (
            "all",
            [0, 100],
            [0, 100],
            [0, 100],
            "all",
            [0, 90],
            df.to_dict("records")
        )

    # Apply filters
    if period and period != "all":
        today = pd.Timestamp.today()
        if period == "30d":
            start_date = today - pd.Timedelta(days=30)
        elif period == "3m":
            start_date = today - pd.DateOffset(months=3)
        elif period == "6m":
            start_date = today - pd.DateOffset(months=6)
        elif period == "12m":
            start_date = today - pd.DateOffset(months=12)
        df["record_date"] = pd.to_datetime(df["record_date"], errors="coerce")
        df = df[df["record_date"].notna()]
        df = df[df["record_date"] >= start_date]

    if efficiency_range:
        eff_min_real = percent_to_real(efficiency_range[0], -16, 19)
        eff_max_real = percent_to_real(efficiency_range[1], -16, 19)
        df = df[(df["efficiency_score"] >= eff_min_real) & (df["efficiency_score"] <= eff_max_real)]

    if engagement_range:
        eng_min = percent_to_real(engagement_range[0], 20, 100)
        eng_max = percent_to_real(engagement_range[1], 20, 100)
        df = df[(df["engagement_score"] >= eng_min) & (df["engagement_score"] <= eng_max)]

    if burnout_range:
        burn_min = percent_to_real(burnout_range[0], 28, 100)
        burn_max = percent_to_real(burnout_range[1], 28, 100)
        df = df[(df["burnout_probability"] >= burn_min) & (df["burnout_probability"] <= burn_max)]

    if idle_range:
        idle_min = percent_to_real(idle_range[0], 0, 120)
        idle_max = percent_to_real(idle_range[1], 0, 120)
        df = df[(df["idle_time_minutes"] >= idle_min) & (df["idle_time_minutes"] <= idle_max)]

    if complexity_value != "all":
        df = df[df["task_complexity"] == complexity_value]

    return (
        period,
        efficiency_range,
        engagement_range,
        burnout_range,
        complexity_value,
        idle_range,
        df.to_dict("records")
    )

# @dash.callback(
#     Output("filtered-data-store", "data"),
#     Input("apply-filters-button", "n_clicks"),
#     State("date-range-filter", "value"),
#     State("efficiency-slider", "value"),
#     State("engagement-slider", "value"),
#     State("burnout-slider", "value"),
#     State("complexity-filter", "value"),
#     State("idle-slider", "value"),
#     prevent_initial_call=False
# )
# def apply_filters(n_clicks, period,
#                   efficiency_range, engagement_range, burnout_range,
#                   complexity_value, idle_range):
#     df = full_df.copy()
#
#     # Filter logic
#     if period and period != "all":
#         today = pd.Timestamp.today()
#         if period == "30d":
#             start_date = today - pd.Timedelta(days=30)
#         elif period == "3m":
#             start_date = today - pd.DateOffset(months=3)
#         elif period == "6m":
#             start_date = today - pd.DateOffset(months=6)
#         elif period == "12m":
#             start_date = today - pd.DateOffset(months=12)
#
#         # 🔧 Conversie corectă
#         df["record_date"] = pd.to_datetime(df["record_date"], errors="coerce")
#         df = df[df["record_date"].notna()]
#         df = df[df["record_date"] >= start_date]
#
#     df = df[df["department"].str.lower() == "sales"]
#
#     if efficiency_range:
#         eff_min_real = percent_to_real(efficiency_range[0], -16, 19)
#         eff_max_real = percent_to_real(efficiency_range[1], -16, 19)
#         df = df[(df["efficiency_score"] >= eff_min_real) & (df["efficiency_score"] <= eff_max_real)]
#
#     if engagement_range:
#         eng_min = percent_to_real(engagement_range[0], 20, 100)
#         eng_max = percent_to_real(engagement_range[1], 20, 100)
#         df = df[(df["engagement_score"] >= eng_min) & (df["engagement_score"] <= eng_max)]
#
#     if burnout_range:
#         burn_min = percent_to_real(burnout_range[0], 28, 100)
#         burn_max = percent_to_real(burnout_range[1], 28, 100)
#         df = df[(df["burnout_probability"] >= burn_min) & (df["burnout_probability"] <= burn_max)]
#
#     if idle_range:
#         idle_min = percent_to_real(idle_range[0], 0, 120)
#         idle_max = percent_to_real(idle_range[1], 0, 120)
#         df = df[(df["idle_time_minutes"] >= idle_min) & (df["idle_time_minutes"] <= idle_max)]
#
#     if complexity_value != "all":
#         df = df[df["task_complexity"] == complexity_value]
#
#     return df.to_dict("records")
#
# @dash.callback(
#     Output("date-range-filter", "value"),
#     Output("efficiency-slider", "value"),
#     Output("engagement-slider", "value"),
#     Output("burnout-slider", "value"),
#     Output("complexity-filter", "value"),
#     Output("idle-slider", "value"),
#     Output("filtered-data-store", "data"),  # ADĂUGAT
#     Input("reset-filters-button", "n_clicks"),
#     prevent_initial_call=True
# )
#
# def reset_ui_filters(n_clicks):
#     # Valorile implicite pentru filtre
#     default_period = "all"
#     default_efficiency = [0, 100]
#     default_engagement = [0, 100]
#     default_burnout = [0, 100]
#     default_complexity = "all"
#     default_idle = [0, 90]
#
#     df = full_df.copy()
#     df = df[df["department"].str.lower() == "sales"]
#
#     return (
#         default_period,
#         default_efficiency,
#         default_engagement,
#         default_burnout,
#         default_complexity,
#         default_idle,
#         df.to_dict("records")
#     )

@dash.callback(
    Output("performance-table", "data"),
    Input("filtered-data-store", "data")
)
def update_table(filtered_data):
    if filtered_data is None:
        raise dash.exceptions.PreventUpdate
    return filtered_data

@dash.callback(
    Output("efficiency-graph", "figure"),
    Input("filtered-data-store", "data")
)
def update_efficiency_graph(filtered_data):
    import plotly.express as px
    import plotly.graph_objects as go

    if not filtered_data:
        return go.Figure()

    df = pd.DataFrame(filtered_data)
    if "efficiency_score" not in df.columns:
        return go.Figure()

    df = df[df["efficiency_score"].notna()]
    df = df[df["efficiency_score"] >= 0]
    df = df.sort_values("efficiency_score", ascending=False).head(10)

    fig = px.bar(
        df,
        x="employee_name",
        y="efficiency_score",
        title="",
        template="plotly",
        labels={"employee_name": "Employee", "efficiency_score": "Efficiency"}
    )
    fig.update_layout(
        title=None,
        showlegend=False,
        margin=dict(t=20, b=40, l=40, r=10),
        xaxis_tickangle=-45,
        xaxis_title="Employee",
        yaxis_title="Efficiency (%)",
        hoverlabel=dict(bgcolor="white", font_size=12)
    )
    return fig

@dash.callback(
    Output("pie-graph", "figure"),
    Input("filtered-data-store", "data")
)
def update_efficiency_boxplot(filtered_data):
    import plotly.express as px
    import plotly.graph_objects as go

    if not filtered_data:
        return go.Figure()

    df = pd.DataFrame(filtered_data)
    if "efficiency_score" not in df.columns:
        return go.Figure()

    fig = px.histogram(
        df,
        x="efficiency_score",
        nbins=20,
        title="",
        template="plotly",
        labels={"efficiency_score": "Efficiency (%)"}
    )
    fig.update_layout(
        title=None,
        showlegend=False,
        margin=dict(t=20, b=40, l=40, r=10),
        xaxis_title="Efficiency (%)",
        yaxis_title="Count",
        hoverlabel=dict(bgcolor="white", font_size=12)
    )
    return fig


@dash.callback(
    Output("engagement-graph", "figure"),
    Input("filtered-data-store", "data")
)
def update_engagement_graph(filtered_data):
    import plotly.express as px
    import plotly.graph_objects as go

    if not filtered_data:
        return go.Figure()

    df = pd.DataFrame(filtered_data)
    if "record_date" not in df.columns or "engagement_score" not in df.columns:
        return go.Figure()

    df["record_date"] = pd.to_datetime(df["record_date"], errors="coerce")
    df = df[df["engagement_score"].notna()]
    df["week"] = df["record_date"].dt.to_period("W").dt.start_time

    weekly_avg = df.groupby("week")["engagement_score"].mean().reset_index()

    fig = px.line(
        weekly_avg,
        x="week",
        y="engagement_score",
        title="",
        template="plotly",
        labels={"engagement_score": "Engagement (%)"}
    )
    fig.update_layout(
        title=None,
        showlegend=False,
        margin=dict(t=20, b=40, l=40, r=10),
        xaxis_title="Week",
        yaxis_title="Engagement (%)",
        hoverlabel=dict(bgcolor="white", font_size=12)
    )
    return fig

@dash.callback(Output("efficiency-range-text", "children"), Input("efficiency-slider", "value"))
def update_efficiency_range(value): return f"Range: {value[0]}–{value[1]}%"

@dash.callback(Output("engagement-range-text", "children"), Input("engagement-slider", "value"))
def update_engagement_range(val): return f"Range: {val[0]}–{val[1]}%"

@dash.callback(Output("burnout-range-text", "children"), Input("burnout-slider", "value"))
def update_burnout_range(val): return f"Range: {val[0]}–{val[1]}%"

@dash.callback(Output("idle-range-text", "children"), Input("idle-slider", "value"))
def update_idle_range(val): return f"Range: {val[0]}–{val[1]} min"





