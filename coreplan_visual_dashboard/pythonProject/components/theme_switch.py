from dash import html

theme_toggle = html.Button(
    html.Img(src="/assets/moon.svg", style={"width": "24px", "height": "24px"}),
    id="theme-switch",
    n_clicks=0,
    style={"border": "none", "background": "transparent", "cursor": "pointer"}
)
