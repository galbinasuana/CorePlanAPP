from dash import html, register_page

register_page(__name__, path="/", name="Home")

def create_card(title, icon, subtitle, description, href):
    return html.A(
        href=href,
        className="home-card",
        children=[
            html.Div(className="card-logo-box", children=[
                html.Div(icon, className="icon"),
                html.H3(title)
            ]),
            html.P(subtitle, className="card-subtitle"),
            html.P(description, className="card-description")
        ]
    )

layout = html.Div(className="home-container", children=[

    html.Div(className="home-header", children=[
        html.H1("Welcome to CorePlan", className="home-title"),
        html.P(
            "Your all-in-one platform for smarter planning, team performance, and business clarity.",
            className="home-subtext"
        )
    ]),

    html.Div(className="card-row", children=[
        create_card(
            "Employees", "👨‍💼", "Team Performance",
            "Monitor individual and departmental efficiency, identify trends, and highlight areas for improvement.",
            "/employees"
        ),
        create_card(
            "Finance", "💰", "Financial Overview",
            "Get real-time insights into budget usage, spending trends, and opportunities for optimization.",
            "/finance"
        ),
        create_card(
            "Planning", "📅", "Project Scheduling",
            "Visualize timelines, manage tasks, and improve time allocation across all ongoing projects.",
            "/planning"
        ),
    ]),

    html.Div(className="card-row", children=[
        create_card(
            "Reports", "📊", "Smart Reporting",
            "Automatically generate high-quality reports with KPIs, anomalies, and strategic suggestions.",
            "/reports"
        ),
        create_card(
            "Custom Dashboard", "⚙️", "Interactive Dashboards",
            "Design your own visual analytics tailored to your decision-making needs.",
            "/custom-dashboard"
        ),
    ])
])
