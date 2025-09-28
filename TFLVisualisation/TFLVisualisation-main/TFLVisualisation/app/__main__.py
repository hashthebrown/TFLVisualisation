from app.components import navbar
from app.config import settings
from app.pages.average_enteries import (
    average_chart_page,
    setup_average_entries_callback,
)
from app.pages.busiest_quietest_page import chart_page, register_chart_callbacks
from app.pages.map import map_view, setup_map_callback
from dash import Dash, Input, Output, html
from dash.dcc import Location
from dash_bootstrap_components.themes import DARKLY

app = Dash(__name__, external_stylesheets=[DARKLY])

# Layout
app.layout = html.Div(
    [
        Location(id="url", refresh=False),
        navbar,
        html.Div(
            id="page-content",
            style={"padding": "20px"},
        ),
    ],
)


@app.callback(
    Output("page-content", "children"),
    [
        Input("url", "pathname"),
    ],
)
def display_page(pathname: str) -> html:
    if pathname == "/":
        return map_view
    elif pathname == "/chart":
        return chart_page
    elif pathname == "/average":
        return average_chart_page
    else:
        return "404 Page Not Found"


register_chart_callbacks(app)
setup_average_entries_callback(app)
setup_map_callback(app)

app.run(
    debug=settings.debug,
    dev_tools_ui=False,
    dev_tools_prune_errors=False,
)
