import dash
import pandas as pd
from dash import html, dcc, dash_table, Input, Output, State, callback
from dash.exceptions import PreventUpdate
from data.db_connector import load_reporting_data
import plotly.express as px

dash.register_page(__name__, path="/reports", name="Reports")

df = load_reporting_data()

layout = html.Div(className="reports-dashboard-container", children=[
    html.Div([
        html.H1("Reports Dashboard", className="dashboard-title")
    ], className="dashboard-header"),

    dcc.Store(id="reports-filtered-data-store", data=df.to_dict("records")),

    html.Div(style={"display": "flex", "flexWrap": "wrap", "gap": "30px", "marginTop": "20px"}, children=[

        html.Div(style={"minWidth": "160px"}, children=[
            html.Label("Period", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id="reports-period-filter",
                options=[
                    {"label": "Last 30 days", "value": "30d"},
                    {"label": "Last 3 months", "value": "3m"},
                    {"label": "Last 6 months", "value": "6m"},
                    {"label": "Last 12 months", "value": "12m"},
                    {"label": "All time", "value": "all"}
                ],
                value="all"
            )
        ]),

        html.Div(style={"flex": "1", "maxWidth": "200px"}, children=[
            html.Label("Recommendation Type"),
            dcc.Dropdown(
                id="reports-recommendation-filter",
                options=[{"label": r, "value": r} for r in df["recommendation_type"].unique()],
                multi=True,
                placeholder="Select type(s)"
            )
        ]),

        html.Div(style={"flex": "1", "maxWidth": "200px"}, children=[
            html.Label("Planning Accuracy (%)"),
            dcc.RangeSlider(
                id="reports-accuracy-slider",
                min=0, max=100, step=5,
                value=[0, 100],
                marks={i: f"{i}%" for i in range(0, 101, 25)},
                tooltip={"always_visible": False}
            ),
            html.Div(id="reports-accuracy-range-text", style={"fontSize": "12px", "marginTop": "4px"})
        ]),

        html.Div(style={"flex": "1", "maxWidth": "200px"}, children=[
            html.Label("Employee Morale Index"),
            dcc.RangeSlider(
                id="reports-morale-slider",
                min=0, max=100, step=5,
                value=[0, 100],
                marks={i: str(i) for i in range(0, 101, 25)},
                tooltip={"always_visible": False}
            ),
            html.Div(id="reports-morale-range-text", style={"fontSize": "12px", "marginTop": "4px"})
        ]),

        html.Div(style={"flex": "1", "maxWidth": "200px"}, children=[
            html.Label("Budget Risk"),
            dcc.Checklist(
                id="reports-budget-risk-filter",
                options=[{"label": "Only At Risk", "value": "Yes"}, {"label": "No Risk", "value": "No"}],
                value=["Yes", "No"],
                labelStyle={"display": "block"},
                inputStyle={"marginRight": "6px"}
            )
        ]),

        html.Div(style={"display": "flex", "flexDirection": "column", "alignItems": "flex-start"}, children=[
            html.Button("Reset Filters", id="reset-reports-filters", className="btn-reset", style={"marginBottom": "40px"}),
            html.Button("Apply Filters", id="apply-reports-filters", className="btn-apply")
        ])
    ]),

    html.Div(
        style={"display": "flex", "gap": "20px", "flexWrap": "wrap", "marginTop": "10px"},
        children=[
            html.Div(
                style={"flex": "1", "minWidth": "300px"},
                children=[
                    html.H4([
                        "Anomalies by Department",
                        html.Img(
                            src="/assets/info.svg",
                            title="Displays the total number of anomalies detected per department.",
                            className="info-icon"
                        )
                    ], style={"fontSize": "20px"}),
                    dcc.Graph(
                        id="anomalies-bar",
                        style={"height": "260px", "width": "100%", "paddingTop": "0", "marginTop": "-10px"},
                        config={"displayModeBar": False}
                    )
                ]
            ),
            html.Div(
                style={"flex": "1", "minWidth": "300px"},
                children=[
                    html.H4([
                        "Morale Trend Over Time",
                        html.Img(
                            src="/assets/info.svg",
                            title="Shows the evolution of employee morale index by department over time.",
                            className="info-icon"
                        )
                    ], style={"fontSize": "20px"}),
                    dcc.Graph(
                        id="morale-line",
                        style={"height": "260px", "width": "100%", "paddingTop": "0", "marginTop": "-10px"},
                        config={"displayModeBar": False}
                    )
                ]
            ),
            html.Div(
                style={"flex": "1", "minWidth": "300px"},
                children=[
                    html.H4([
                        "Urgency Index Distribution",
                        html.Img(
                            src="/assets/info.svg",
                            title="Boxplot of urgency index per department.",
                            className="info-icon"
                        )
                    ], style={"fontSize": "20px"}),
                    dcc.Graph(
                        id="urgency-box",
                        style={"height": "260px", "width": "100%", "paddingTop": "0", "marginTop": "-10px"},
                        config={"displayModeBar": False}
                    )
                ]
            ),
            html.Div(
                style={"flex": "1", "minWidth": "300px"},
                children=[
                    html.H4([
                        "Budget Risk Heatmap",
                        html.Img(
                            src="/assets/info.svg",
                            title="Heatmap showing budget variance alerts per department.",
                            className="info-icon"
                        )
                    ], style={"fontSize": "20px"}),
                    dcc.Graph(
                        id="budget-heatmap",
                        style={"height": "260px", "width": "100%", "paddingTop": "0", "marginTop": "-10px"},
                        config={"displayModeBar": False}
                    )
                ]
            )
        ]
    ),

    html.Div([
        html.H3("Filtered Reports Table", style={"fontSize": "22px"}),
        dash_table.DataTable(
            id="reports-data-table",
            columns=[
                {"name": col.replace("_", " ").title(), "id": col}
                for col in df.columns
                if col not in ["report_id", "department_focus"]
            ],
            page_size=6,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "padding": "6px"},
            style_header={"fontWeight": "bold", "backgroundColor": "#f0f0f0"}
        )
    ])
])

@callback(
    Output("reports-accuracy-range-text", "children"),
    Input("reports-accuracy-slider", "value")
)
def update_accuracy_text(value):
    return f"Selected range: {value[0]}% – {value[1]}%"


@callback(
    Output("reports-morale-range-text", "children"),
    Input("reports-morale-slider", "value")
)
def update_morale_text(value):
    return f"Selected range: {value[0]} – {value[1]}"


@callback(
    Output("reports-filtered-data-store", "data"),
    Input("apply-reports-filters", "n_clicks"),
    Input("reset-reports-filters", "n_clicks"),
    State("reports-period-filter", "value"),
    State("reports-recommendation-filter", "value"),
    State("reports-accuracy-slider", "value"),
    State("reports-morale-slider", "value"),
    State("reports-budget-risk-filter", "value"),
    prevent_initial_call=True
)
def update_reports_data(apply_clicks, reset_clicks, period, recommendation, acc_range, morale_range, budget_risk):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    df_filtered = df.copy()
    df_filtered = df_filtered[df_filtered["department_focus"] == "Sales"]

    if triggered_id == "reset-reports-filters":
        return df_filtered.to_dict("records")

    # Apply filters
    if period != "all":
        today = pd.to_datetime("today")
        if period == "30d":
            threshold = today - pd.Timedelta(days=30)
        elif period == "3m":
            threshold = today - pd.DateOffset(months=3)
        elif period == "6m":
            threshold = today - pd.DateOffset(months=6)
        elif period == "12m":
            threshold = today - pd.DateOffset(months=12)
        else:
            threshold = None

        if threshold is not None:
            df_filtered = df_filtered[pd.to_datetime(df_filtered["report_date"]) >= threshold]

    if recommendation:
        df_filtered = df_filtered[df_filtered["recommendation_type"].isin(recommendation)]

    df_filtered = df_filtered[
        (df_filtered["planning_accuracy"].between(acc_range[0], acc_range[1])) &
        (df_filtered["employee_morale_index"].between(morale_range[0], morale_range[1])) &
        (df_filtered["budget_variance_alert"].isin(budget_risk))
    ]

    return df_filtered.to_dict("records")

@callback(
    Output("reports-period-filter", "value"),
    Output("reports-recommendation-filter", "value"),
    Output("reports-accuracy-slider", "value"),
    Output("reports-morale-slider", "value"),
    Output("reports-budget-risk-filter", "value"),
    Input("reset-reports-filters", "n_clicks"),
    prevent_initial_call=True
)
def reset_reports_filters(n_clicks):
    return "all", None, [0, 100], [0, 100], ["Yes", "No"]



@callback(
    Output("anomalies-bar", "figure"),
    Output("morale-line", "figure"),
    Output("urgency-box", "figure"),
    Output("budget-heatmap", "figure"),
    Output("reports-data-table", "data"),
    Input("reports-filtered-data-store", "data")
)
def update_reports_charts(data):
    if not data:
        raise PreventUpdate

    df_vis = pd.DataFrame(data)
    df_vis["report_date"] = pd.to_datetime(df_vis["report_date"])
    df_vis["week"] = df_vis["report_date"].dt.to_period("W").apply(lambda r: r.start_time)
    df_vis["quarter"] = df_vis["report_date"].dt.to_period("Q").astype(str)

    # === Anomalies Bar Chart (by Quarter) ===
    anomalies_q = df_vis.groupby("quarter")["anomalies_detected"].sum().reset_index()
    anomalies_fig = px.bar(
        anomalies_q,
        x="quarter",
        y="anomalies_detected",
        text="anomalies_detected",
        labels={
            "quarter": "Quarter",
            "anomalies_detected": "Anomalies"
        }
    )
    anomalies_fig.update_layout(
        title=None,
        showlegend=False,
        margin=dict(t=40, b=40, l=40, r=10)
    )

    # === Morale Line Chart (weekly average) ===
    morale_weekly = df_vis.groupby("week")["employee_morale_index"].mean().reset_index()
    morale_fig = px.line(
        morale_weekly,
        x="week",
        y="employee_morale_index",
        labels={
            "employee_morale_index": "Morale Index",
            "week": "Week"
        }
    )
    morale_fig.update_layout(
        title=None,
        margin=dict(t=40, b=40, l=40, r=10)
    )

    # === Urgency Box Chart (by Quarter) ===
    urgency_fig = px.box(
        df_vis,
        x="quarter",
        y="urgency_index",
        labels={
            "quarter": "Quarter",
            "urgency_index": "Urgency Index"
        }
    )
    urgency_fig.update_layout(
        title=None,
        showlegend=False,
        margin=dict(t=40, b=40, l=40, r=10)
    )

    # === Budget Risk Heatmap ===
    heatmap_data = df_vis.groupby(["recommendation_type", "budget_variance_alert"]).size().reset_index(name="count")
    heatmap_fig = px.density_heatmap(
        heatmap_data,
        x="recommendation_type",
        y="budget_variance_alert",
        z="count",
        color_continuous_scale="YlOrRd",
        labels={
            "recommendation_type": "Recommendation",
            "budget_variance_alert": "Risk",
            "count": "Count"
        }
    )
    heatmap_fig.update_layout(
        title=None,
        margin=dict(t=40, b=40, l=40, r=10)
    )

    return anomalies_fig, morale_fig, urgency_fig, heatmap_fig, df_vis.to_dict("records")

