import dash
import pandas as pd
import numpy as np
from dash import html, dcc, dash_table, Input, Output, State, callback
from dash.exceptions import PreventUpdate
from data.db_connector import load_planning_data
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__, path="/planning", name="Planning")

df = load_planning_data()
df.rename(columns={
    "planned_efficiency_score": "planning_accuracy",
    "is_overloaded": "overload_status",
    "slippage_days": "schedule_slippage_days"
}, inplace=True)

df["planning_accuracy"] = df["planning_accuracy"].round(2)

layout = html.Div(className="planning-dashboard-container", children=[
    html.Div([
        html.H2("Planning Overview Dashboard")
    ], style={"marginBottom": "10px"}),
    dcc.Store(id="planning-filtered-data-store", data=df.to_dict("records")),

    html.Div(style={"display": "flex",
            "flexWrap": "wrap",
            "gap": "15px",
            "alignItems": "start",
            "justifyContent": "flex-start",
            "overflowX": "auto",
            "overflow": "visible",
            "position": "relative",
            "paddingBottom": "10px"}, children=[

        html.Div(style={"flex": "1", "maxWidth": "200px"}, children=[
            html.Label("Period"),
            dcc.Dropdown(
                id="planning-period-filter",
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

        html.Div(style={"flex": "2", "maxWidth": "200px"}, children=[
            html.Label("Required Headcount"),
            dcc.RangeSlider(
                id="headcount-slider",
                min=0, max=100, step=1,
                value=[0, 100],
                marks={0: "0", 50: "50", 100: "100"},
                tooltip={"always_visible": False}
            ),
            html.Div(id="headcount-range-text", style={"fontSize": "12px", "marginTop": "4px"})
        ]),

        html.Div(style={"flex": "2", "maxWidth": "200px"}, children=[
            html.Label("Planning Accuracy (%)"),
            dcc.RangeSlider(
                id="accuracy-slider",
                min=0, max=100, step=5,
                value=[0, 100],
                marks={i: f"{i}%" for i in range(0, 101, 25)},
                tooltip={"always_visible": False}
            ),
            html.Div(id="accuracy-range-text", style={"fontSize": "12px", "marginTop": "4px"})
        ]),

        html.Div(style={"flex": "2", "maxWidth": "200px"}, children=[
            html.Label("Schedule Slippage (days)"),
            dcc.RangeSlider(
                id="slippage-slider",
                min=0, max=90, step=1,
                value=[0, 90],
                marks={0: "0", 45: "45", 90: "90"},
                tooltip={"always_visible": False}
            ),
            html.Div(id="slippage-range-text", style={"fontSize": "12px", "marginTop": "4px"})
        ]),

        html.Div([
            html.Label("Priority Level"),
            dcc.RadioItems(
                id="priority-filter",
                options=[
                    {"label": "Low", "value": "Low"},
                    {"label": "Medium", "value": "Medium"},
                    {"label": "High", "value": "High"},
                    {"label": "All", "value": "All"}
                ],
                value="All",
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
        ], style={"flex": "1", "maxWidth": "200px"}),

        html.Div(style={"display": "flex", "flexDirection": "column", "alignItems": "flex-start"}, children=[
            html.Button("Reset Filters", id="reset-planning-filters", className="btn-reset", style={"margin-bottom": "40px"}),
            html.Button("Apply Filters", id="apply-planning-filters", className="btn-apply")
        ])
    ]),

    html.Div(style={"display": "flex", "gap": "20px"}, children=[

        html.Div(style={"flex": "1", "minWidth": "300px"}, children=[
            html.H4([
                "Efficiency Gap by Priority & Tasks",
                html.Img(
                    src="/assets/info.svg",
                    title="Heatmap showing the average efficiency gap segmented by task priority level and task volume (bucketed). Helps identify performance drop-offs.",
                    style={"height": "18px", "marginLeft": "6px", "cursor": "help"}
                )
            ], style={"fontSize": "20px"}),
            dcc.Graph(id="overload-percentage-graph", style={"height": "300px", "width": "100%"},
                      config={"displayModeBar": False})
        ]),

        html.Div(style={"flex": "1", "minWidth": "300px"}, children=[
            html.H4([
                "Accuracy per Priority Level",
                html.Img(
                    src="/assets/info.svg",
                    title="Boxplot showing the variability of planning accuracy across different task priorities. Useful to assess consistency.",
                    style={"height": "18px", "marginLeft": "6px", "cursor": "help"}
                )
            ], style={"fontSize": "20px"}),
            dcc.Graph(id="planning-accuracy-trend", style={"height": "300px", "width": "100%"},
                      config={"displayModeBar": False})
        ]),

        html.Div(style={"flex": "1", "minWidth": "300px"}, children=[
            html.H4([
                "Weekly Headcount Demand",
                html.Img(
                    src="/assets/info.svg",
                    title="Shows the weekly average of required headcount, helping identify seasonal demands or understaffed periods.",
                    style={"height": "18px", "marginLeft": "6px", "cursor": "help"}
                )
            ], style={"fontSize": "20px"}),
            dcc.Graph(id="complexity-vs-efficiency", style={"height": "300px", "width": "100%"},
                      config={"displayModeBar": False})
        ]),

        html.Div(style={"flex": "1", "minWidth": "300px"}, children=[
            html.H4([
                "Efficiency vs. Delay",
                html.Img(
                    src="/assets/info.svg",
                    title="Shows how schedule slippage correlates with efficiency gap. Highlights how delays impact efficiency.",
                    style={"height": "18px", "marginLeft": "6px", "cursor": "help"}
                )
            ], style={"fontSize": "20px"}),
            dcc.Graph(id="accuracy-vs-overload", style={"height": "300px", "width": "100%"},
                      config={"displayModeBar": False})
        ])
    ]),

    html.Div([
        html.H3("Planning Summary Table", style={"fontSize": "22px"}),

        dash_table.DataTable(
            id="planning-summary-table",

            columns=[
                {"name": "employee_id", "id": "employee_id"},
                {"name": "planned_hours", "id": "planned_hours"},
                {"name": "actual_hours", "id": "actual_hours"},
                {"name": "task_count", "id": "task_count"},
                {"name": "priority_level", "id": "priority_level"},
                {"name": "required_headcount", "id": "required_headcount"},
                {"name": "record_date", "id": "record_date"},
                {"name": "planning_accuracy", "id": "planning_accuracy"},
                {"name": "efficiency_gap", "id": "efficiency_gap"},
                {"name": "overload_status", "id": "overload_status"},
                {"name": "schedule_slippage_days", "id": "schedule_slippage_days"}
            ],

            data=df[[
                "employee_id", "planned_hours", "actual_hours", "task_count",
                "priority_level", "required_headcount", "record_date",
                "planning_accuracy", "efficiency_gap", "overload_status", "schedule_slippage_days"
            ]].to_dict("records"),

            page_size=6,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "minWidth": "100px"}
        )
    ])

])


@callback(
    Output("planning-filtered-data-store", "data"),
    Output("planning-period-filter", "value"),
    Output("headcount-slider", "value"),
    Output("accuracy-slider", "value"),
    Output("slippage-slider", "value"),
    Input("apply-planning-filters", "n_clicks"),
    Input("reset-planning-filters", "n_clicks"),
    State("planning-period-filter", "value"),
    State("headcount-slider", "value"),
    State("accuracy-slider", "value"),
    State("slippage-slider", "value"),
    prevent_initial_call=True
)
def update_filtered_data(apply_clicks, reset_clicks, period, headcount_range, accuracy_range, slippage_range):
    from dash import callback_context
    ctx = callback_context

    df = load_planning_data()
    df.rename(columns={
        "planned_efficiency_score": "planning_accuracy",
        "is_overloaded": "overload_status",
        "slippage_days": "schedule_slippage_days"
    }, inplace=True)

    df["record_date"] = pd.to_datetime(df["record_date"], errors="coerce")
    df = df[df["department_name"] == "Sales"]

    triggered_id = ctx.triggered_id

    if triggered_id == "reset-planning-filters":
        # Setări implicite
        default_period = "all"
        default_headcount = [0, 100]
        default_accuracy = [0, 100]
        default_slippage = [0, 90]
        df["planning_accuracy"] = df["planning_accuracy"].round(2)
        return df.to_dict("records"), default_period, default_headcount, default_accuracy, default_slippage

    # Aplicare filtre la Apply
    if period and period != "all":
        today = pd.Timestamp.today()
        if period == "30d":
            start = today - pd.Timedelta(days=30)
        elif period == "3m":
            start = today - pd.DateOffset(months=3)
        elif period == "6m":
            start = today - pd.DateOffset(months=6)
        elif period == "12m":
            start = today - pd.DateOffset(months=12)
        df = df[df["record_date"] >= start]

    df = df[
        (df["required_headcount"].between(headcount_range[0], headcount_range[1])) &
        (df["planning_accuracy"].between(accuracy_range[0], accuracy_range[1])) &
        (df["schedule_slippage_days"].between(slippage_range[0], slippage_range[1]))
    ]

    df["planning_accuracy"] = df["planning_accuracy"].round(2)

    return df.to_dict("records"), period, headcount_range, accuracy_range, slippage_range



@callback(
    Output("overload-percentage-graph", "figure"),
    Output("planning-accuracy-trend", "figure"),
    Output("complexity-vs-efficiency", "figure"),
    Output("accuracy-vs-overload", "figure"),
    Input("planning-filtered-data-store", "data")
)
def update_core_planning_graphs(data):
    if not data:
        raise PreventUpdate

    df = pd.DataFrame(data)
    df["record_date"] = pd.to_datetime(df["record_date"], errors="coerce")
    df["overload_status"] = df["overload_status"].str.lower()

    # === FIG 1===
    max_count = df["task_count"].max()

    last_bin = max(50, int(np.ceil(max_count / 10.0) * 10))

    bins = [0, 10, 20, 30, 40, last_bin]
    labels = ["0–10", "11–20", "21–30", "31–40", f"{40}+"]
    df["task_count_bucket"] = pd.cut(df["task_count"], bins=bins, labels=labels, include_lowest=True)

    heatmap_df = df.groupby(["priority_level", "task_count_bucket"])["efficiency_gap"].mean().reset_index()
    heatmap_df["efficiency_gap"] = heatmap_df["efficiency_gap"].round(1)

    heatmap_pivot = heatmap_df.pivot(index="priority_level", columns="task_count_bucket", values="efficiency_gap")
    heatmap_pivot = heatmap_pivot.fillna("")

    fig1 = px.imshow(
        heatmap_pivot,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        zmin=-15,
        zmax=5,
        aspect="auto",
        labels={"color": "Efficiency Gap"}
    )

    fig1.update_layout(
        title=None,
        plot_bgcolor="white",
        margin=dict(t=30, l=0, r=0, b=0),
        xaxis_title="Task Count Bucket",
        yaxis_title="Priority Level"
    )

    # === FIG 2===
    fig2 = px.box(
        df,
        x="priority_level",
        y="planning_accuracy",
        color="priority_level",
        labels={"planning_accuracy": "Accuracy (%)", "priority_level": "Priority Level"}
    )

    fig2.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        title=None,
        margin=dict(t=30, l=0, r=0, b=0),
        xaxis_title="Priority Level",
        yaxis_title="Planning Accuracy (%)"
    )

    # === FIG 3 ===
    area_df = df.copy()
    area_df["record_date"] = pd.to_datetime(area_df["record_date"])
    area_df = area_df.groupby(pd.Grouper(key="record_date", freq="W"))[
        "required_headcount"
    ].mean().reset_index()

    fig3 = px.area(
        area_df,
        x="record_date",
        y="required_headcount",
        labels={"required_headcount": "Avg Headcount", "record_date": "Date"},
    )

    fig3.update_layout(
        title=None,
        plot_bgcolor="white",
        xaxis_title="Date",
        yaxis_title="Required Headcount",
        margin=dict(t=30, l=0, r=0, b=0)
    )

    # === FIG 4 ===
    max_slip = int(df["schedule_slippage_days"].max())
    if max_slip <= 20:
        final_edge = 21  # forțăm un bin peste 20
    else:
        final_edge = max_slip + 1

    df["slippage_bucket"] = pd.cut(
        df["schedule_slippage_days"],
        bins=[-1, 0, 5, 10, 20, final_edge],
        labels=["On Time", "1–5d", "6–10d", "11–20d", "20+d"]
    )

    slip_df = df.groupby("slippage_bucket")["efficiency_gap"].mean().reset_index()
    slip_df["efficiency_gap"] = slip_df["efficiency_gap"].round(2)

    fig4 = px.bar(
        slip_df,
        x="efficiency_gap",
        y="slippage_bucket",
        orientation="h",
        labels={
            "efficiency_gap": "Avg Efficiency Gap",
            "slippage_bucket": "Slippage Range"
        },
        color="slippage_bucket",
        color_discrete_sequence=px.colors.sequential.Teal
    )

    fig4.update_layout(
        title=None,
        plot_bgcolor="white",
        margin=dict(t=30, l=0, r=0, b=0),
        showlegend=False,
        xaxis_title="Efficiency Gap",
        yaxis_title="Slippage Range"
    )

    return fig1, fig2, fig3, fig4


@callback(
    Output("planning-summary-table", "data"),
    Input("planning-filtered-data-store", "data")
)
def update_table(data):
    return data


@callback(
    Output("headcount-range-text", "children"),
    Input("headcount-slider", "value")
)
def update_headcount_text(val):
    return f"Range: {val[0]} – {val[1]}"


@callback(
    Output("accuracy-range-text", "children"),
    Input("accuracy-slider", "value")
)
def update_accuracy_text(val):
    return f"Range: {val[0]}% – {val[1]}%"


@callback(
    Output("slippage-range-text", "children"),
    Input("slippage-slider", "value")
)
def update_slippage_text(val):
    return f"Range: {val[0]} – {val[1]} days"

