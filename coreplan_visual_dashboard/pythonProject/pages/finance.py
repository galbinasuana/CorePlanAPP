import dash
import pandas as pd
from dash import html, dcc, dash_table, Input, Output, State, callback
from data.db_connector import load_financial_data
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__, path="/finance", name="Finance")

df = load_financial_data()
df = df[df["department_name"] == "Sales"]

layout = html.Div(className="finance-dashboard-container", children=[
    html.Div([
        html.H2("Financial Overview Dashboard")
    ], style={"marginBottom": "10px"}),
    dcc.Store(id="finance-filtered-data-store", data=df.to_dict("records")),


    html.Div([
        html.Div([
            html.Div(style={"minWidth": "160px"}, children=[
                html.Label("Period", style={"fontWeight": "bold"}),
                dcc.Dropdown(
                    id="finance-period-filter",
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

            html.Div([
                html.Label("Profit Range (€)"),
                dcc.RangeSlider(
                    id="profit-slider",
                    min=-5000, max=120000, step=1000,
                    value=[-5000, 120000],
                    marks={-5000: "-5K", 60000: "60K", 120000: "120K"}
                ),
                html.Div(id="profit-range-text", style={"fontSize": "12px", "marginTop": "4px"})
            ], style={"flex": "2", "maxWidth": "200px"}),

            html.Div([
                html.Label("Budget Usage (%)"),
                dcc.RangeSlider(
                    id="budget-slider",
                    min=0, max=100, step=5,
                    value=[0, 100],
                    marks={i: f"{i}%" for i in range(0, 101, 25)}
                ),
                html.Div(id="budget-range-text", style={"fontSize": "12px", "marginTop": "4px"})
            ], style={"flex": "2", "maxWidth": "200px"}),

            html.Div([
                html.Label("Expenses (€)"),
                dcc.RangeSlider(
                    id="expenses-slider",
                    min=30000, max=100000, step=1000,
                    value=[30000, 100000],
                    marks={30000: "30K", 65000: "65K", 100000: "100K"}
                ),
                html.Div(id="expenses-range-text", style={"fontSize": "12px", "marginTop": "4px"})
            ], style={"flex": "2", "maxWidth": "200px"}),

            html.Div([
                html.Label("Risk Level"),
                dcc.RadioItems(
                    id="risk-filter",
                    options=[
                        {"label": "Low", "value": "Low"},
                        {"label": "Medium", "value": "Medium"},
                        {"label": "High", "value": "High"},
                        {"label": "All", "value": "All"},
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

            html.Div([
                html.Button("Reset Filters", id="reset-finance-filters", className="btn-reset", style={"margin-bottom": "40px"}),
                html.Button("Apply Filters", id="apply-finance-filters", className="btn-apply")
            ], style={"display": "flex", "flexDirection": "column", "alignItems": "flex-start"}),
        ], style={
            "display": "flex",
            "flexWrap": "wrap",
            "gap": "15px",
            "alignItems": "start",
            "justifyContent": "flex-start",
            "overflowX": "auto",
            "overflow": "visible",
            "position": "relative",
            "paddingBottom": "10px"
        }),
    ]),

    html.Div(style={"display": "flex", "gap": "20px"}, children=[
        html.Div(style={"flex": 1}, children=[
            html.H4([
                "Quarterly Profit Trend ",
                html.Img(
                    src="/assets/info.svg",
                    title="Displays total profit evolution per quarter for the Sales department based on filtered financial data.",
                    style={"height": "18px", "marginLeft": "6px", "cursor": "help"}
                )
            ], style={"fontSize": "20px"}),
            dcc.Graph(id="profit-quarterly-sales", style={"height": "300px"}, config={"displayModeBar": False})
        ]),
        html.Div(style={"flex": 1}, children=[
            html.H4([
                "Allocated vs. Used Budget ",
                html.Img(
                    src="/assets/info.svg",
                    title="Tracks monthly budget allocation and usage for the Sales department, with efficiency percentage to highlight overspending or underutilization.",
                    style={"height": "18px", "marginLeft": "6px", "cursor": "help"}
                )
            ], style={"fontSize": "20px"}),
            dcc.Graph(id="budget-vs-used", style={"height": "300px"}, config={"displayModeBar": False})
        ]),
        html.Div(style={"flex": 1}, children=[
            html.H4([
                "Net Profit Over Time ",
                html.Img(
                    src="/assets/info.svg",
                    title="Shows the net profit evolution over time, allowing managers to track financial trends and detect performance anomalies.",
                    style={"height": "18px", "marginLeft": "6px", "cursor": "help"}
                )
            ], style={"fontSize": "20px"}),
            dcc.Graph(id="net-profit-trend", style={"height": "300px"}, config={"displayModeBar": False})
        ])
    ]),

    html.Div([
        html.H3("Financial Summary Table", style={"fontSize": "22px"}),
        dash_table.DataTable(
            id="finance-summary-table",
            columns=[{"name": i, "id": i} for i in df.columns if i not in ["department_id", "department_name"]],
            data=df.to_dict("records"),
            page_size=6,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "minWidth": "100px"}
        )
    ])
])


@callback(
    Output("finance-period-filter", "value"),
    Output("profit-slider", "value"),
    Output("budget-slider", "value"),
    Output("expenses-slider", "value"),
    Output("risk-filter", "value"),
    Output("finance-filtered-data-store", "data"),
    Input("apply-finance-filters", "n_clicks"),
    Input("reset-finance-filters", "n_clicks"),
    State("finance-period-filter", "value"),
    State("profit-slider", "value"),
    State("budget-slider", "value"),
    State("expenses-slider", "value"),
    State("risk-filter", "value"),
    prevent_initial_call=True
)
def apply_or_reset_filters(apply_clicks, reset_clicks, period, profit_range, budget_range, expenses_range, risk_level):
    ctx = dash.callback_context

    # Dacă a fost apăsat RESET
    if ctx.triggered and ctx.triggered[0]["prop_id"].startswith("reset-finance-filters"):
        df = load_financial_data()
        df = df[df["department_name"] == "Sales"]
        df["budget_usage_percent"] = df.apply(
            lambda row: (row["budget_used"] / row["budget_allocated"]) * 100 if row["budget_allocated"] > 0 else 0,
            axis=1
        )
        return (
            "all",
            [-5000, 120000],
            [0, 100],
            [30000, 100000],
            "All",
            df.to_dict("records")
        )

    # Altfel, se aplică filtrele curente
    df = load_financial_data()
    df["record_date"] = pd.to_datetime(df["record_date"], errors="coerce")

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

    df = df[df["department_name"] == "Sales"]

    df["budget_usage_percent"] = df.apply(
        lambda row: (row["budget_used"] / row["budget_allocated"]) * 100 if row["budget_allocated"] > 0 else 0,
        axis=1
    )

    df = df[
        (df["profit"].between(profit_range[0], profit_range[1])) &
        (df["budget_usage_percent"].between(budget_range[0], budget_range[1])) &
        (df["expenses"].between(expenses_range[0], expenses_range[1]))
    ]

    if risk_level != "All":
        df = df[df["financial_risk_level"] == risk_level]

    return (
        period,
        profit_range,
        budget_range,
        expenses_range,
        risk_level,
        df.to_dict("records")
    )



@callback(
    Output("profit-quarterly-sales", "figure"),
    Input("finance-filtered-data-store", "data")
)
def update_quarterly_profit_sales(data):
    if not data:
        return go.Figure()

    df = pd.DataFrame(data)
    df["record_date"] = pd.to_datetime(df["record_date"], errors="coerce")

    df["quarter"] = df["record_date"].dt.to_period("Q").astype(str)

    grouped = df.groupby("quarter")["profit"].sum().reset_index()

    fig = px.bar(
        grouped,
        x="quarter",
        y="profit",
        template="plotly",
        labels={"quarter": "Quarter", "profit": "Profit (€)"},
        color_discrete_sequence=["#1f77b4"]
    )

    fig.update_layout(
        title=None,
        xaxis_title="Quarter",
        yaxis_title="Profit (€)",
        hoverlabel=dict(bgcolor="white", font_size=12),
        margin=dict(t=20, b=40, l=40, r=10),
        height=300
    )

    fig.update_traces(marker=dict(line=dict(width=0)))
    return fig

@callback(
    Output("budget-vs-used", "figure"),
    Input("finance-filtered-data-store", "data")
)
def update_budget_vs_actual(data):
    if not data:
        return go.Figure()

    df = pd.DataFrame(data)
    df["record_date"] = pd.to_datetime(df["record_date"], errors="coerce")
    df["month"] = df["record_date"].dt.to_period("M").astype(str)  # agregare lunară

    # Agregăm datele per lună
    grouped = df.groupby("month").agg({
        "budget_allocated": "sum",
        "budget_used": "sum"
    }).reset_index()

    grouped["budget_usage_percent"] = grouped.apply(
        lambda row: (row["budget_used"] / row["budget_allocated"]) * 100 if row["budget_allocated"] > 0 else 0,
        axis=1
    )

    fig = go.Figure()

    # Bar: Allocated
    fig.add_trace(go.Bar(
        x=grouped["month"],
        y=grouped["budget_allocated"],
        name="Allocated",
        marker_color="#d3d3d3"
    ))

    # Bar: Used
    fig.add_trace(go.Bar(
        x=grouped["month"],
        y=grouped["budget_used"],
        name="Used",
        marker_color="#1f77b4"
    ))

    # Line: Usage %
    fig.add_trace(go.Scatter(
        x=grouped["month"],
        y=grouped["budget_usage_percent"],
        name="Usage (%)",
        mode="lines+markers",
        yaxis="y2",
        line=dict(color="#ff7f0e", width=3),
        marker=dict(size=6)
    ))

    fig.update_layout(
        barmode="group",
        yaxis=dict(title="Amount (€)"),
        yaxis2=dict(
            title="Usage (%)",
            overlaying="y",
            side="right",
            range=[0, 120],
            showgrid=False
        ),
        margin=dict(t=20, b=40, l=40, r=10),
        height=300,
        legend=dict(title="", orientation="h", x=0.5, xanchor="center", y=-0.2),
        hovermode="x unified"
    )

    return fig


@callback(
    Output("net-profit-trend", "figure"),
    Input("finance-filtered-data-store", "data")
)
def update_net_profit_trend(data):
    if not data:
        return go.Figure()
    df = pd.DataFrame(data)
    df["record_date"] = pd.to_datetime(df["record_date"], errors="coerce")
    grouped = df.groupby("record_date")["profit"].sum().reset_index()
    fig = px.line(grouped, x="record_date", y="profit", template=None)
    fig.update_layout(
        title=None,
        yaxis_title="Profit (€)",
        xaxis_title="Date",
        margin=dict(t=10, b=40, l=40, r=10),
        height=300
    )
    return fig


# @callback(
#     Output("budget-usage-graph", "figure"),
#     Output("profit-trend-graph", "figure"),
#     Output("risk-distribution-graph", "figure"),
#     Input("finance-filtered-data-store", "data")
# )
# def update_graphs(data):
#     if not data:
#         return go.Figure(), go.Figure(), go.Figure()
#     df = pd.DataFrame(data)
#     df["record_date"] = pd.to_datetime(df["record_date"], errors="coerce")
#     df["budget_usage_percent"] = (df["budget_used"] / df["budget_allocated"]) * 100
#
#     fig1 = px.bar(df, x="department_name", y="budget_usage_percent", color="department_name")
#     fig1.update_layout(
#         yaxis_title="Budget Usage (%)",
#         yaxis=dict(range=[0, 100])
#     )
#
#     fig2 = px.line(df.groupby("record_date")["profit"].sum().reset_index(), x="record_date", y="profit")
#     risk = df["financial_risk_level"].value_counts().reset_index()
#     risk.columns = ["Risk Level", "Count"]
#     fig3 = px.pie(risk, names="Risk Level", values="Count")
#     return fig1, fig2, fig3


@callback(
    Output("finance-summary-table", "data"),
    Input("finance-filtered-data-store", "data")
)
def update_table(data):
    return data


@callback(
    Output("profit-range-text", "children"),
    Input("profit-slider", "value")
)
def update_profit_text(val):
    return f"Range: {val[0]:,} – {val[1]:,} €"


@callback(
    Output("budget-range-text", "children"),
    Input("budget-slider", "value")
)
def update_budget_text(val):
    return f"Range: {val[0]}% – {val[1]}%"


@callback(
    Output("expenses-range-text", "children"),
    Input("expenses-slider", "value")
)
def update_expenses_text(val):
    return f"Range: {val[0]:,} – {val[1]:,} €"
