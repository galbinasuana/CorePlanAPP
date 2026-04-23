import dash
from dash import dcc, html, page_container
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


# app = dash.Dash(__name__, use_pages=True)
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True
server = app.server

custom_css = '''
body {
    font-family: "Segoe UI", sans-serif;
    background-color: #f5f7fa;
    margin: 0;
    padding: 0;
    color: #333;
}

.sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: 180px;
    height: 100vh;
    background-color: #003366;
    color: white;
    padding: 20px;
    box-shadow: 2px 0 5px rgba(0,0,0,0.1);
}

.sidebar-title {
    font-size: 24px;
    margin-bottom: 30px;
    color: #fff;
}

.menu-link {
    display: block;
    color: #cce3ff;
    padding: 10px 0;
    text-decoration: none;
    font-weight: bold;
}

.menu-link.active {
    background-color: #0056b3;
    color: #ffffff;
    border-left: 4px solid #528BBE;
    padding-left: 12px;
    border-radius: 0 6px 6px 0;
    font-weight: bold;
}

.menu-link:hover {
    color: #ffffff;
}

.main-content {
    margin-left: 240px;
    padding: 30px;
}

.btn-apply {
    background-color: #007bff;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
}

.btn-apply:hover {
    background-color: #0056b3;
}

.question-icon {
    display: inline-block;
    background-color:#d3e1f0;
    color: white;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    text-align: center;
    line-height: 20px;
    font-weight: bold;
    margin-left: 10px;
    cursor: pointer;
    font-size: 14px;
}

.question-icon-img {
    position: fixed;
    bottom: 20px;
    left: 200px;
    width: 45px;
    height: 45px;
    cursor: pointer;
    transition: transform 0.2s ease, opacity 0.2s ease;
    z-index: 1000;
}

.question-icon-img:hover {
    transform: scale(1.15);
    opacity: 0.95;
}

.question-container {
    position: fixed;
    bottom: 80px;
    left: 200px;
    width: 50px;
    height: 50px;
    z-index: 1000;
}

.question-img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    transition: opacity 0.3s ease, transform 0.3s ease;
    cursor: pointer;
}

.question-img.static {
    z-index: 1;
}

.question-img.gif {
    z-index: 2;
    opacity: 0;
}

.question-container:hover .gif {
    opacity: 1;
    transform: scale(1.1);
}

'''

app.index_string = f"""
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>CorePlan</title>
        {{%favicon%}}
        {{%css%}}
        <style>{custom_css}</style>
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
"""

app.layout = html.Div([
    dcc.Location(id="url"),

    html.Div(className="sidebar", children=[
        html.H2("CorePlan", className="sidebar-title"),
        html.Nav(id="sidebar-menu", className="menu")

    ]),

    # html.Div(className="main-content", children=page_container)

    html.Div(className="main-content", children=[
        dbc.Container([
            page_container
        ], fluid=True)
    ])

    # html.Div([
    #     html.Img(
    #         src="/assets/question_static.png",
    #         className="question-img static"
    #     ),
    #     html.Img(
    #         src="/assets/question.gif",
    #         className="question-img gif"
    #     )
    # ], className="question-container")

])

def generate_links(current_path):
    links = [
        ("/", "🏠 Home"),
        ("/employees", "👨‍💼 Employees"),
        ("/finance", "💰 Finance"),
        ("/planning", "📅 Planning"),
        ("/reports", "📊 Reports"),
        ("/custom-dashboard", "⚙️ Custom Dashboard"),
    ]
    return [
        dcc.Link(
            label,
            href=path,
            className="menu-link active" if current_path == path else "menu-link"
        )
        for path, label in links
    ]

@app.callback(
    Output("sidebar-menu", "children"),
    Input("url", "pathname")
)
def update_sidebar(pathname):
    return generate_links(pathname)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
