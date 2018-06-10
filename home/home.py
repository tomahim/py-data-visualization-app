import dash_html_components as html
import dash_core_components as dcc

layout = html.Div([
    html.H1('Home'),
    dcc.Link('USA gun violence study', href="/data-visualization/usa-gun-violence")
])