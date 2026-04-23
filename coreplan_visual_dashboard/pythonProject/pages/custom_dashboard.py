import uuid

import dash
from dash import html, dcc, callback, Output, Input, State, ALL, ctx, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash.dash_table import DataTable

from data.db_custom_queries import load_performance_data, load_financial_data, load_planning_data, load_reporting_data, load_departments
from dash.exceptions import PreventUpdate
from uuid import uuid4


dash.register_page(__name__, path="/custom-dashboard", name="Custom Dashboard")

layout = html.Div(className="custom-dashboard-container", children=[
    dcc.Store(id="canvas-items", data=[]),

    html.H2("Custom Dashboard Builder", className="page-title"),

    html.Div(className="top-row", children=[
        html.Div(className="toolbar-column", children=[
            dbc.Button("📝 Text", id="btn-text", className="toolbar-btn", n_clicks=0, style={"color": "#4a4a4a", "fontSize": "15px", "width": "100%", "textAlign": "left", "marginBottom": "10px"}),
            dbc.Button("📊 Chart", id="btn-chart", className="toolbar-btn", n_clicks=0, style={"color": "#4a4a4a", "fontSize": "15px", "width": "100%", "textAlign": "left", "marginBottom": "10px"}),
            dbc.Button("📋 Table", id="btn-table", className="toolbar-btn", n_clicks=0, style={"color": "#4a4a4a", "fontSize": "15px", "width": "100%", "textAlign": "left", "marginBottom": "10px"}),
        ]),

        html.Div(id="config-panel", className="config-panel", children=[
            html.H3("🔧 Configuration Panel", className="config-title", style={"fontSize": "20px"}),
            html.Div("Select a section from the toolbar to configure it.", className="config-description")
        ])
    ]),

    html.Div(className="canvas-wrapper", children=[
        html.Img(
            src="/assets/export-file.png",
            className="export-icon",
            title="Export to PDF",
            id="export-pdf-icon",
            style={"cursor": "pointer"}
        ),

        html.H3("📄 Custom Canvas", className="canvas-title", style={"fontSize": "20px"}),
        html.Div(id="canvas-area", className="canvas-area"),
        dcc.Store(id="canvas-items", data=[])
    ])
])

@callback(
    Output("config-panel", "children"),
    Input("btn-text", "n_clicks"),
    Input("btn-chart", "n_clicks"),
    Input("btn-table", "n_clicks"),
    prevent_initial_call=True
)
def show_config_panel(n_text, n_chart, n_table):
    triggered_id = ctx.triggered_id

    if triggered_id == "btn-text":
        return html.Div([
            html.H3("📝 Text Configuration", className="config-title", style={
                "fontSize": "20px", "marginBottom": "15px", "color": "#2c3e50"
            }),
            html.Div([
                html.Label("Text Font:", style={"marginRight": "5px", "fontWeight": "bold"}),
                dcc.Dropdown(
                    id="text-font",
                    options=[{"label": f, "value": f} for f in ["Arial", "Times New Roman", "Courier New", "Verdana"]],
                    value="Arial",
                    style={"width": "150px", "marginRight": "10px"}
                ),
                html.Label("Text Size:", style={"marginRight": "5px", "fontWeight": "bold"}),
                dcc.Dropdown(
                    id="text-size",
                    options=[{"label": str(s), "value": str(s)} for s in [12, 14, 16, 18, 20, 24, 28]],
                    value="16",
                    style={"width": "80px", "marginRight": "15px"}
                ),
                dbc.Checklist(
                    id="text-style",
                    options=[
                        {"label": html.Span("Bold", style={"fontWeight": "bold"}), "value": "bold"},
                        {"label": html.Span("Italic", style={"fontStyle": "italic"}), "value": "italic"},
                        {"label": html.Span("Underline", style={"textDecoration": "underline"}), "value": "underline"}
                    ],
                    value=[],
                    inline=True
                ),
                html.Label("Color:", style={"marginRight": "5px", "fontWeight": "bold"}),
                dcc.Dropdown(
                    id="text-color",
                    options=[
                        {"label": html.Span("🔴 Red", style={"color": "red"}), "value": "red"},
                        {"label": html.Span("🟢 Green", style={"color": "green"}), "value": "green"},
                        {"label": html.Span("🔵 Blue", style={"color": "blue"}), "value": "blue"},
                        {"label": html.Span("⚫ Black", style={"color": "black"}), "value": "black"},
                        {"label": html.Span("🟠 Orange", style={"color": "orange"}), "value": "orange"},
                        {"label": html.Span("🟣 Purple", style={"color": "purple"}), "value": "purple"},
                        {"label": html.Span("🟤 Brown", style={"color": "brown"}), "value": "brown"},
                        {"label": html.Span("⚪ White", style={"color": "gray"}), "value": "white"}
                    ],
                    value="black",
                    style={"width": "120px"}
                )
            ], style={"display": "flex", "alignItems": "center", "gap": "10px", "marginBottom": "15px"}),

            dcc.Textarea(
                id="text-content",
                placeholder="Enter your text here...",
                style={
                    "width": "100%", "height": "120px", "padding": "10px", "fontSize": "16px",
                    "border": "1px solid #ccc", "borderRadius": "6px", "backgroundColor": "#f9f9f9",
                    "resize": "vertical", "boxShadow": "none"
                }
            ),

            html.Div([
                dbc.Button("➕ Add to Canvas", id="btn-add-text", color="primary", outline=True, style={
                    "fontSize": "15px", "padding": "6px 16px", "float": "right",
                    "border": "1.5px solid #4a4a4a", "backgroundColor": "transparent", "color": "#0d6efd"
                })
            ], style={"marginTop": "10px"})
        ])

    elif triggered_id == "btn-chart":
        return show_chart_config()

    elif triggered_id == "btn-table":
        return show_table_config()

    raise PreventUpdate


@callback(
    Output("canvas-area", "children", allow_duplicate=True),
    Output("canvas-items", "data", allow_duplicate=True),

    Output("text-content", "value", allow_duplicate=True),
    Output("text-font", "value", allow_duplicate=True),
    Output("text-size", "value", allow_duplicate=True),
    Output("text-style", "value", allow_duplicate=True),
    Output("text-color", "value", allow_duplicate=True),

    Input("btn-add-text", "n_clicks"),
    State("text-content", "value"),
    State("text-font", "value"),
    State("text-size", "value"),
    State("text-style", "value"),
    State("text-color", "value"),
    State("canvas-items", "data"),
    prevent_initial_call=True
)
def add_text_to_canvas(n_clicks, content, font, size, styles, color, current_canvas):
    if not content:
        raise PreventUpdate

    if current_canvas is None:
        current_canvas = []

    new_item = {
        "id": str(uuid.uuid4()),
        "type": "text",
        "content": {
            "text": content,
            "font": font,
            "size": size,
            "styles": styles,
            "color": color
        }
    }

    updated_canvas = current_canvas + [new_item]

    return (
        render_canvas(updated_canvas),
        updated_canvas,

        "",
        "Arial",
        "16",
        [],
        "black"
    )


def show_chart_config():
    return html.Div([
        html.H3("📊 Chart Configuration", className="config-title", style={"fontSize": "20px", "marginBottom": "15px"}),

        html.Div([
            html.Label("Select Table:", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id="chart-table",
                options=[
                    {"label": "Employee Performance", "value": "employee_performance"},
                    {"label": "Finance Data", "value": "financial_data"},
                    {"label": "Planning Data", "value": "resource_planning"},
                    {"label": "Reporting Data", "value": "reporting_data"}
                ],
                value="employee_performance",
                style={"width": "100%", "marginBottom": "10px"}
            ),

            html.Label("Chart Type:", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id="chart-type",
                options=[
                    {"label": "📊 Bar", "value": "bar"},
                    {"label": "📈 Line", "value": "line"},
                    {"label": "🥧 Pie", "value": "pie"},
                    {"label": "📦 Box", "value": "box"},
                    {"label": "🔥 Heatmap", "value": "heatmap"}
                ],
                value="bar",
                style={"width": "100%", "marginBottom": "10px"}
            ),

            html.Label("X Axis:", style={"fontWeight": "bold"}),
            dcc.Dropdown(id="chart-x", style={"width": "100%", "marginBottom": "10px"}),

            html.Label("Y Axis:", style={"fontWeight": "bold"}),
            dcc.Dropdown(id="chart-y", style={"width": "100%", "marginBottom": "10px"}),

            html.Label("Aggregation:", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id="chart-agg",
                options=[{"label": a, "value": a.lower()} for a in ["AVG", "SUM", "MIN", "MAX", "COUNT"]],
                value="avg",
                style={"width": "100%", "marginBottom": "15px"}
            )
        ]),

        dbc.Button("➕ Add to Canvas", id="btn-add-chart", color="primary", outline=True, style={
            "float": "right",
            "fontSize": "15px",
            "border": "1.5px solid #4a4a4a",
            "backgroundColor": "transparent",
            "color": "#0d6efd"
        })
    ])

@callback(
    Output("chart-x", "options"),
    Output("chart-x", "value"),
    Output("chart-y", "options"),
    Output("chart-y", "value"),
    Input("chart-table", "value"),
    prevent_initial_call=True
)
def update_axis_dropdowns(table):
    if not table:
        raise PreventUpdate

    try:
        df = {
            "employee_performance": load_performance_data,
            "financial_data": load_financial_data,
            "resource_planning": load_planning_data,
            "reporting_data": load_reporting_data
        }.get(table, lambda: pd.DataFrame())()

        department_mapping = {}
        if "department_id" in df.columns:
            dept_df = load_departments()
            department_mapping = dict(zip(dept_df["department_id"], dept_df["department_name"]))

        x_options = []
        for col in df.columns:
            if col == "department_id":
                x_options.append({
                    "label": "Department (Name)",
                    "value": col
                })
            else:
                x_options.append({"label": col, "value": col})

        numeric_cols = df.select_dtypes(include=["int64", "float64", "float32"]).columns
        y_options = [{"label": col, "value": col} for col in numeric_cols]

        x_value = df.columns[0] if not df.empty else None
        y_value = numeric_cols[0] if len(numeric_cols) > 0 else None

        return x_options, x_value, y_options, y_value

    except Exception as e:
        print(f"Dropdown update error: {e}")
        return [], None, [], None


@callback(
    Output("canvas-area", "children", allow_duplicate=True),
    Output("canvas-items", "data", allow_duplicate=True),
    Output("chart-table", "value", allow_duplicate=True),
    Output("chart-type", "value", allow_duplicate=True),
    Output("chart-x", "value", allow_duplicate=True),
    Output("chart-y", "value", allow_duplicate=True),
    Output("chart-agg", "value", allow_duplicate=True),
    Input("btn-add-chart", "n_clicks"),
    State("chart-table", "value"),
    State("chart-type", "value"),
    State("chart-x", "value"),
    State("chart-y", "value"),
    State("chart-agg", "value"),
    State("canvas-items", "data"),
    prevent_initial_call=True
)
def add_chart_to_canvas(n_clicks, table, chart_type, x_col, y_col, agg_func, current_canvas):
    if not (table and chart_type and x_col and y_col and agg_func):
        raise PreventUpdate

    if current_canvas is None:
        current_canvas = []

    if agg_func == "avg":
        agg_func = "mean"

    try:
        # Load full table data
        df = {
            "employee_performance": load_performance_data,
            "financial_data": load_financial_data,
            "resource_planning": load_planning_data,
            "reporting_data": load_reporting_data
        }.get(table, lambda: pd.DataFrame())()

        x_col_label = x_col

        # Convert department_id to readable label if needed
        if x_col == "department_id" and "department_id" in df.columns:
            departments = load_departments()[["department_id", "department_name"]]
            df = df.merge(departments, on="department_id", how="left")
            x_col_label = "department_name"

        # Grouping logic
        if agg_func == "count":
            df_grouped = df.groupby(x_col_label).size().reset_index(name="Count")
            y_label = "Count"
        else:
            df_grouped = df.groupby(x_col_label)[y_col].agg(agg_func).reset_index()
            y_label = f"{agg_func.upper()}({y_col})"
            df_grouped.rename(columns={y_col: y_label}, inplace=True)

    except Exception as e:
        return render_canvas(current_canvas), current_canvas, table, chart_type, x_col, y_col, agg_func

    try:
        # Chart rendering
        fig = (
            px.bar(df_grouped, x=x_col_label, y=y_label) if chart_type == "bar" else
            px.line(df_grouped, x=x_col_label, y=y_label) if chart_type == "line" else
            px.pie(df_grouped, names=x_col_label, values=y_label) if chart_type == "pie" else
            px.box(df, x=x_col_label, y=y_col) if chart_type == "box" else
            px.imshow(df.pivot_table(index=x_col_label, columns=y_col, aggfunc='size', fill_value=0)) if chart_type == "heatmap" else
            None
        )
        if fig is None:
            return current_canvas + [html.Div("❌ Unknown chart type", style={"color": "red"})], table, chart_type, x_col, y_col, agg_func

        fig.update_layout(margin=dict(t=20, b=20, l=10, r=10), height=400)

        new_item = {
            "id": str(uuid.uuid4()),
            "type": "chart",
            "content": fig.to_plotly_json()  # important pentru serializare
        }

        if current_canvas is None:
            current_canvas = []

        updated_canvas = current_canvas + [new_item]

        return render_canvas(updated_canvas), updated_canvas, "employee_performance", "bar", None, None, "avg"

    except Exception as e:
        return current_canvas + [html.Div(f"❌ Chart error: {e}", style={"color": "red"})], table, chart_type, x_col, y_col, agg_func



def show_table_config():
    return html.Div([
        html.H3("📋 Table Configuration", className="config-title", style={"fontSize": "20px", "marginBottom": "15px"}),

        html.Label("Primary Table:", style={"fontWeight": "bold"}),
        dcc.Dropdown(
            id="table-primary",
            options=[
                {"label": "Employee Performance", "value": "employee_performance"},
                {"label": "Finance Data", "value": "financial_data"},
                {"label": "Planning Data", "value": "resource_planning"},
                {"label": "Reporting Data", "value": "reporting_data"}
            ],
            value="employee_performance",
            style={"width": "100%", "marginBottom": "10px"}
        ),

        html.Label("Columns to Display:", style={"fontWeight": "bold"}),
        dcc.Dropdown(id="table-columns", multi=True, style={"width": "100%", "marginBottom": "15px"}),

        html.Hr(),

        html.Label("Join with (optional):", style={"fontWeight": "bold"}),
        dcc.Dropdown(
            id="table-secondary",
            options=[
                {"label": "Finance Data", "value": "financial_data"},
                {"label": "Planning Data", "value": "resource_planning"},
                {"label": "Reporting Data", "value": "reporting_data"},
                {"label": "Employee Performance", "value": "employee_performance"},
            ],
            placeholder="Select table to join",
            style={"width": "100%", "marginBottom": "10px"}
        ),

        html.Label("Columns from Joined Table:", style={"fontWeight": "bold"}),
        dcc.Dropdown(
            id="table-secondary-columns",
            multi=True,
            placeholder="Select columns from joined table...",
            style={"width": "100%", "marginBottom": "10px"}
        ),

        html.Label("Join Type:", style={"fontWeight": "bold"}),
        dcc.Dropdown(
            id="table-join-type",
            options=[{"label": j, "value": j} for j in ["inner", "left", "right", "outer"]],
            value="inner",
            style={"width": "100%", "marginBottom": "10px"}
        ),

        html.Label("Primary Key Column:", style={"fontWeight": "bold"}),
        dcc.Dropdown(id="primary-key", style={"width": "100%", "marginBottom": "10px"}),

        html.Label("Foreign Key Column:", style={"fontWeight": "bold"}),
        dcc.Dropdown(id="foreign-key", style={"width": "100%", "marginBottom": "10px"}),

        html.Label("Row Limit (optional):", style={"fontWeight": "bold"}),
        dcc.Input(
            id="row-limit",
            type="number",
            placeholder="Max rows to display (default: 100)",
            min=1,
            style={"width": "100%", "marginBottom": "20px"}
        ),

        dbc.Button("➕ Add to Canvas", id="btn-add-table", color="primary", outline=True, style={
            "float": "right",
            "fontSize": "15px",
            "border": "1.5px solid #4a4a4a",
            "backgroundColor": "transparent",
            "color": "#0d6efd"
        })
    ])


@callback(
    Output("table-columns", "options"),
    Output("primary-key", "options"),
    Output("foreign-key", "options"),
    Output("table-secondary-columns", "options"),
    Input("table-primary", "value"),
    Input("table-secondary", "value"),
    prevent_initial_call=True
)
def update_table_columns(primary, secondary):
    if not primary:
        raise PreventUpdate

    def get_schema(table):
        loader = {
            "employee_performance": load_performance_data,
            "financial_data": load_financial_data,
            "resource_planning": load_planning_data,
            "reporting_data": load_reporting_data
        }.get(table)
        if loader:
            return list(loader().columns)
        return []

    # Coloane pentru tabelul principal
    primary_schema = get_schema(primary)
    primary_columns = [{"label": col, "value": col} for col in primary_schema]

    # Coloane pentru tabelul secundar
    foreign_columns = []
    secondary_columns = []
    if secondary:
        secondary_schema = get_schema(secondary)
        foreign_columns = [{"label": col, "value": col} for col in secondary_schema]
        secondary_columns = [{"label": col, "value": col} for col in secondary_schema]

    return primary_columns, primary_columns, foreign_columns, secondary_columns



@callback(
    Output("canvas-area", "children", allow_duplicate=True),
    Output("canvas-items", "data", allow_duplicate=True),
    Output("table-primary", "value", allow_duplicate=True),
    Output("table-columns", "value", allow_duplicate=True),
    Output("table-secondary", "value", allow_duplicate=True),
    Output("table-join-type", "value", allow_duplicate=True),
    Output("primary-key", "value", allow_duplicate=True),
    Output("foreign-key", "value", allow_duplicate=True),
    Input("btn-add-table", "n_clicks"),
    State("table-primary", "value"),
    State("table-columns", "value"),
    State("table-secondary", "value"),
    State("table-secondary-columns", "value"),
    State("table-join-type", "value"),
    State("primary-key", "value"),
    State("foreign-key", "value"),
    State("row-limit", "value"),
    State("canvas-items", "data"),
    prevent_initial_call=True
)
def add_table_to_canvas(n, primary, columns, secondary, secondary_columns,
                        join_type, pk, fk, limit, current_canvas):
    if not n or not primary:
        raise PreventUpdate

    if current_canvas is None:
        current_canvas = []

    loaders = {
        "employee_performance": load_performance_data,
        "financial_data": load_financial_data,
        "resource_planning": load_planning_data,
        "reporting_data": load_reporting_data
    }

    try:
        df = loaders[primary]() if primary in loaders else pd.DataFrame()

        if secondary and pk and fk:
            df_secondary = loaders[secondary]() if secondary in loaders else pd.DataFrame()
            df = df.merge(df_secondary, how=join_type, left_on=pk, right_on=fk)

        # Combinăm coloanele selectate din ambele tabele
        all_columns = (columns or []) + (secondary_columns or [])
        if all_columns:
            df = df[all_columns]

        if limit and isinstance(limit, int) and limit > 0:
            df = df.head(limit)

    except Exception as e:
        error_msg = {"id": str(uuid.uuid4()), "type": "error", "content": f"❌ Error loading table: {e}"}
        return render_canvas(current_canvas + [error_msg]), current_canvas + [error_msg], primary, [], None, "inner", None, None

    new_item = {
        "id": str(uuid.uuid4()),
        "type": "table",
        "content": {
            "columns": list(df.columns),
            "rows": df.to_dict("records")
        }
    }

    updated_canvas = current_canvas + [new_item]

    return render_canvas(updated_canvas), updated_canvas, "employee_performance", [], None, "inner", None, None


def generate_canvas_components(items):
    components = []
    for index, item in enumerate(items):
        controls = html.Div([
            dbc.Button("⬆", id={"type": "move-up", "index": item["id"]}, size="sm", color="light", style={"marginRight": "5px"}),
            dbc.Button("⬇", id={"type": "move-down", "index": item["id"]}, size="sm", color="light")
        ], style={"textAlign": "right", "marginBottom": "5px"})

        content = html.Div(item["content"], style=item.get("style", {}))
        full_block = html.Div([controls, content], style={"marginBottom": "25px"}, className="canvas-block")

        components.append(full_block)

    return components


def render_canvas(items):
    components = []

    for idx, item in enumerate(items):
        move_buttons = html.Div([
            html.Button("⬆", id={"type": "move-up", "index": item["id"]}, n_clicks=0,
                        style={"marginRight": "5px", "padding": "4px 8px"}),
            html.Button("⬇", id={"type": "move-down", "index": item["id"]}, n_clicks=0,
                        style={"marginRight": "5px", "padding": "4px 8px"}),
            html.Button("🗑️", id={"type": "delete-item", "index": item["id"]}, n_clicks=0,
                        style={"padding": "4px 8px"})
        ], style={"marginBottom": "8px", "textAlign": "right"})

        content = None

        if item["type"] == "text":
            text_data = item["content"]
            styles = {
                "fontFamily": text_data.get("font", "Arial"),
                "fontSize": f"{text_data.get('size', '16')}px",
                "color": text_data.get("color", "black"),
                "marginBottom": "10px",
                "whiteSpace": "pre-wrap"
            }

            # Stiluri adiționale
            if "bold" in text_data.get("styles", []):
                styles["fontWeight"] = "bold"
            if "italic" in text_data.get("styles", []):
                styles["fontStyle"] = "italic"
            if "underline" in text_data.get("styles", []):
                styles["textDecoration"] = "underline"

            content = html.Div(text_data.get("text", ""), style=styles)

        elif item["type"] == "chart":
            fig = go.Figure(item["content"])
            content = dcc.Graph(figure=fig, config={"displayModeBar": False},
                                style={"marginBottom": "10px"})


        elif item["type"] == "table":
            df = pd.DataFrame(item["content"]["rows"], columns=item["content"]["columns"])
            content = dash_table.DataTable(
                data=df.to_dict("records"),
                columns=[{"name": col, "id": col} for col in df.columns],
                page_size=6,
                page_current=0,
                style_table={"overflowX": "auto", "marginBottom": "10px"},
                style_cell={"padding": "6px"},
                style_header={"backgroundColor": "#f2f2f2", "fontWeight": "bold"},
                style_data={"backgroundColor": "#ffffff"},
            )


        else:
            content = html.Div("⚠️ Unknown item type", style={"color": "red"})

        # Card final cu tot (conținut + butoane)
        components.append(
            html.Div([
                content,
                move_buttons
            ], style={
                "backgroundColor": "#ffffff",
                "padding": "15px",
                "marginBottom": "20px",
                "borderRadius": "12px",
                "boxShadow": "0 2px 6px rgba(0,0,0,0.1)"
            })
        )

    return components

@callback(
    Output("canvas-area", "children"),
    Output("canvas-items", "data"),
    Input({"type": "move-up", "index": ALL}, "n_clicks"),
    Input({"type": "move-down", "index": ALL}, "n_clicks"),
    Input({"type": "delete-item", "index": ALL}, "n_clicks"),
    State("canvas-items", "data"),
    prevent_initial_call=True
)
def reorder_or_delete_canvas(up_clicks, down_clicks, delete_clicks, items):
    triggered = ctx.triggered_id
    if not triggered:
        raise PreventUpdate

    item_id = triggered["index"]
    idx = next((i for i, x in enumerate(items) if x["id"] == item_id), None)
    if idx is None:
        raise PreventUpdate

    if triggered["type"] == "move-up" and idx > 0:
        items[idx - 1], items[idx] = items[idx], items[idx - 1]
    elif triggered["type"] == "move-down" and idx < len(items) - 1:
        items[idx + 1], items[idx] = items[idx], items[idx + 1]
    elif triggered["type"] == "delete-item":
        items.pop(idx)

    return render_canvas(items), items


