from dash import html, dcc, dash_table
from data.db_connector import load_performance_data
from components.theme_switch import theme_toggle

def serve_layout():
    df = load_performance_data()

    return html.Div([
        html.Div([
            html.H1("CorePlan – Data Visualizer", style={"margin": 0}),
            theme_toggle
        ], style={
            "padding": "20px",
            "display": "flex",
            "justifyContent": "space-between",
            "alignItems": "center",
            "backgroundColor": "inherit",
            "boxShadow": "0 2px 5px rgba(0,0,0,0.05)"
        }),

        html.Div(className="card", children=[
            html.H3("Filters", style={"marginBottom": "15px"}),

            html.Div(style={
                "display": "flex",
                "gap": "20px",
                "flexWrap": "wrap",
                "alignItems": "flex-end"
            }, children=[

                html.Div(style={"minWidth": "220px"}, children=[
                    html.Label("Department", style={"fontWeight": "bold"}),
                    dcc.Dropdown(
                        id="dept-filter",
                        options=[{"label": dep, "value": dep} for dep in df["department"].unique()],
                        placeholder="Select Department",
                        style={
                            "backgroundColor": "white",
                            "border": "1px solid #ccc",
                            "borderRadius": "6px",
                            "padding": "6px"
                        }
                    )
                ]),

                html.Div(style={"minWidth": "300px"}, children=[
                    html.Label("Date Range", style={"fontWeight": "bold"}),
                    dcc.DatePickerRange(
                        id="date-filter",
                        min_date_allowed=df["record_date"].min(),
                        max_date_allowed=df["record_date"].max(),
                        start_date=df["record_date"].min(),
                        end_date=df["record_date"].max(),
                        display_format="MM/DD/YYYY",
                        style={
                            "backgroundColor": "white",
                            "border": "1px solid #ccc",
                            "borderRadius": "6px",
                            "padding": "6px"
                        }
                    )
                ]),

                html.Div(style={"flexGrow": 1}, children=[
                    html.Label("Efficiency Score", style={"fontWeight": "bold"}),
                    dcc.RangeSlider(
                        id="efficiency-filter",
                        min=df["efficiency_score"].min(),
                        max=df["efficiency_score"].max(),
                        value=[df["efficiency_score"].min(), df["efficiency_score"].max()],
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True}
                    )
                ])
            ])
        ]),

        html.Button("Aplică filtrele", id="apply-filters-btn", n_clicks=0, style={
            "marginTop": "10px",
            "padding": "10px 20px",
            "backgroundColor": "#007bff",
            "color": "white",
            "border": "none",
            "borderRadius": "5px",
            "cursor": "pointer"
        }),

        html.Div(className="container", children=[
            html.Div(className="content", children=[

                html.Div(className="card", children=[
                    html.Div(style={"display": "flex", "gap": "20px"}, children=[
                        dcc.Graph(id="efficiency-graph", style={"flex": 1}),
                        dcc.Graph(id="pie-graph", style={"flex": 1})
                    ])
                ]),

                html.Div(className="card", children=[
                    html.H3("Employee Performance Table"),
                    dash_table.DataTable(
                        id="performance-table",
                        columns=[{"name": i, "id": i} for i in df.columns],
                        page_size=10,
                        page_current=0,
                        style_table={"overflowX": "auto"},
                        style_cell={"textAlign": "left", "minWidth": "100px", "whiteSpace": "normal"},
                        style_header={
                            "backgroundColor": "var(--table-header-bg)",
                            "fontWeight": "bold",
                            "color": "var(--text-color)"
                        }
                    )
                ])
            ])
        ])

    ])