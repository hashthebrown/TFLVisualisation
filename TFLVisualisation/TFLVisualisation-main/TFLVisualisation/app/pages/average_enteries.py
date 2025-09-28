import dash
import plotly.express as px
from app.utils.data_processing import DataProcessing
from dash import Dash, Input, Output, dcc, html

average_chart_page = html.Div(
    [
        html.H1("Average Entries per Station"),
        dcc.Graph(id="average-entries-graph"),
    ],
)


def setup_average_entries_callback(app: Dash) -> px.bar:
    """
    Set up the callback for the average entries page. This callback will update the graph with the average entries per
    station over five years.
    :param app:
    :return:
    """

    @app.callback(
        Output(
            "average-entries-graph",
            "figure",
        ),
        [
            Input("url", "pathname"),
        ],
    )
    def update_average_graph(pathname: str) -> px.bar:
        if pathname != "/average":
            return dash.no_update

        years = list(range(2017, 2023))  # Define the range of years
        combined_data = DataProcessing.load_combined_data(years)
        average_data = DataProcessing.calculate_average_entries(combined_data)

        fig = px.bar(
            average_data,
            x="Station Name",
            y="Average Entries",
            title="Average Entries Per Station Over Five Years",
        )
        return fig
